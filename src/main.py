from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from logger.init_logger import getLogger

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
        for i, element in enumerate(elements):
            log.debug(
                f"Post {i + 1} text: {element.text}")
            post_texts.append(element.text)

    except Exception as e:
        log.debug("No posts found")
        log.error("Error: {}".format(e))

    return post_texts


def main():

    log.debug("Scrape the curly girl website")
    facebook_page = "https://www.facebook.com/Vinthersklippekaelder"

    driver = webdriver.Firefox()
    driver.get(facebook_page)
    driver.implicitly_wait(5)

    sleep(3)
    click_only_essential_cookies(driver)
    sleep(2)
    posts = extract_posts_from_page(driver)
    if check_if_any_post_is_cancellation(posts):
        log.info("Found a cancellation post - Notify the client")
    else:
        log.info("Did not find a cancellation post - Do not notify the client")

    driver.close()


if __name__ == "__main__":
    main()
