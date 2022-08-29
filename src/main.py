# Standard library
from lib2to3.pgen2.token import OP
from time import sleep
import schedule

# Application libraries
from logger.init_logger import getLogger
from aws_secrets import get_secret

# Third party libraries
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

log = getLogger(__file__)


def identify_cancellation(post_text: str):
    cancellation_keywords = ["afbud", "afbudstid"]
    if any(keyword in post_text.lower() for keyword in cancellation_keywords):
        return True
    else:
        return False


def check_if_any_post_is_cancellation(post_texts: list):
    for post_text in post_texts:
        if identify_cancellation(post_text):
            return True
    return False


def click_only_essential_cookies(driver: webdriver):
    # Fetch the button
    element = driver.find_element(
        By.XPATH, "//*[contains(text(), 'Only allow essential cookies')]")

    # Click on parent
    element.find_element(By.XPATH, "..").click()

    log.debug(f"Clicked on the Only allow essential cookies button")


def extract_posts_from_page(driver: webdriver):
    log.debug("Extract the posts from the page")
    post_texts = []
    try:
        elements = driver.find_elements(
            By.XPATH, "//*[@data-ad-preview='message']")
        log.debug("Found {} posts".format(len(elements)))
        for _, element in enumerate(elements):
            post_texts.append(element.text)

    except Exception as e:
        log.debug("No posts found")
        log.error("Error: {}".format(e))

    return post_texts


def send_message_to_user(secrets: dict):
    account_sid = secrets["CURLY_TWILIO_ACCOUNT_SID"]
    auth_token = secrets["CURLY_TWILIO_AUTH_TOKEN"]
    from_number = secrets["TWILIO_FROM_NUMBER"]
    to_number = secrets["ANNA_NUMBER"]

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body='Curly girl har et afbud! Skynd dig ind og book det.',
            from_=from_number,
            to=to_number
        )

    log.debug(f"Twillio message unique identifer: {message.sid}")


def check_if_any_cancellation(secrets: dict, facebook_page: str):
    log.debug("Scrape the curly girl website")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(facebook_page)
    driver.implicitly_wait(5)
    sleep(3)
    click_only_essential_cookies(driver)
    sleep(2)
    posts = extract_posts_from_page(driver)
    if check_if_any_post_is_cancellation(posts):
        log.info("Found a cancellation post - Notify the client")
        send_message_to_user(secrets)
    else:
        log.info("Did not find a cancellation post - Do not notify the client")
    driver.close()


def main():
    facebook_page = "https://www.facebook.com/Vinthersklippekaelder"

    no_error, secrets = get_secret()

    if not no_error:
        log.error("Unable to get TWILIO secrets")
        return

    schedule.every(1).minutes.do(
        check_if_any_cancellation, secrets, facebook_page)

    log.debug("Start the scheduler")
    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    main()
