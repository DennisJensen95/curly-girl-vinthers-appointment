# Standard library
from time import sleep
import schedule
from datetime import datetime

# Application libraries
from logger.init_logger import getLogger
from aws_secrets import get_secret
import curly_db

# Third party libraries
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pysondb

log = getLogger(__file__)


def identify_cancellation(post_text: str):
    cancellation_keywords = ["afbud", "afbudstid"]
    if any(keyword in post_text.lower() for keyword in cancellation_keywords):
        return True
    else:
        return False


def check_if_any_post_is_cancellation(post_texts: list, db: pysondb.db.JsonDatabase):
    for post_text in post_texts:
        if identify_cancellation(post_text):
            post_id = curly_db.save_post(post_text=post_text, db=db)
            time_stamp = curly_db.get_post_timestamp(post_id=post_id, db=db)
            log.debug(
                f"First message of the post was sent at: {time_stamp.strftime(curly_db.DATEFORMAT)}")
            if not is_post_too_old(5, post_time=time_stamp):
                return True
            log.debug("Not notifying the client as the post was too old")
            return False
    return False


def click_only_essential_cookies(driver: webdriver):
    try:
        # Fetch the button
        element = driver.find_element(
            By.XPATH, "//*[contains(text(), 'Only allow essential cookies')]")

        # Click on parent
        element.find_element(By.XPATH, "..").click()

        log.debug("Clicked on the Only allow essential cookies button")
    except Exception as error:
        log.debug(
            f"Not able to click on the button for only essential cookies. Error was {error}")


def extract_posts_from_page(driver: webdriver):
    log.debug("Extract the posts from the page")
    post_texts = []
    try:
        elements = driver.find_elements(
            By.XPATH, "//*[@data-ad-preview='message']")
        log.debug("Found {} posts".format(len(elements)))
        for _, element in enumerate(elements):
            log.debug(f"{element.text[:10]}...")
            post_texts.append(element.text)

    except Exception as e:
        log.debug("No posts found")
        log.error("Error: {}".format(e))

    return post_texts


def is_post_too_old(min_old_threshold: int, post_time: datetime):
    """Check if the post is too old to be relevant

    Args:
        min_old_threshold (int, optional): The number of minutes the post can be old. Defaults to 10.

    Returns:
        bool: True if the post is too old
    """
    now = datetime.now()
    time_difference = now - post_time
    if time_difference.total_seconds() / 60 > min_old_threshold:
        return True

    return False


def send_message_to_user(secrets: dict, receiver: str):
    account_sid = secrets["CURLY_TWILIO_ACCOUNT_SID"]
    auth_token = secrets["CURLY_TWILIO_AUTH_TOKEN"]
    from_number = secrets["TWILIO_FROM_NUMBER"]
    to_number = secrets[receiver]
    print(secrets)

    client = Client(account_sid, auth_token)

    message = client.messages.create(
            body='Curly girl har et afbud! Skynd dig ind og book det - https://www.facebook.com/Vinthersklippekaelder',
            from_=from_number,
            to=to_number
        )

    log.debug(f"Twillio message unique identifer: {message.sid}")


def check_if_any_cancellation(secrets: dict, facebook_page: str, db: pysondb.db.JsonDatabase):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    log.debug("Scrape the curly girl website")
    driver.get(facebook_page)
    driver.implicitly_wait(10)
    sleep(3)
    click_only_essential_cookies(driver)
    sleep(5)
    posts = extract_posts_from_page(driver)
    if check_if_any_post_is_cancellation(posts, db):
        log.info("Found a cancellation post - Notify the client")
        send_message_to_user(secrets, "ANNA_NUMBER")
        send_message_to_user(secrets, "BETTINA_NUMBER")
    else:
        log.info("Did not find a cancellation post - Do not notify the client")

    driver.close()
    driver.quit()


def main():
    facebook_page = "https://www.facebook.com/Vinthersklippekaelder"

    no_error, secrets = get_secret()

    if not no_error:
        log.error("Unable to get TWILIO secrets")
        return

    # Init database object
    db = curly_db.initialize_database()

    schedule.every(5).seconds.do(
        check_if_any_cancellation, secrets, facebook_page, db)

    check_if_any_cancellation(secrets, facebook_page, db)

    log.debug("Start the scheduler")
    while True:
        try:
            schedule.run_pending()
        except Exception as error:
            log.error(f"Error in the scheduler: {error}")
        sleep(1)

if __name__ == "__main__":
    main()
