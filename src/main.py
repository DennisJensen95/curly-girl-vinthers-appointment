from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging
from logger.init_logger import getLogger

log = getLogger(__file__)


def click_only_essential_cookies(driver: webdriver):
    # Fetch the button
    element = driver.find_element(
        By.XPATH, "//*[contains(text(), 'Only allow essential cookies')]")

    # Click on parent
    element.find_element(By.XPATH, "..").click()

    log.debug(f"Clicked on the Only allow essential cookies button")


def extract_posts_from_page(driver: webdriver):
    log.debug("Extract the posts from the page")
    try:
        element = driver.find_element(
            By.XPATH, "//*[data-ad-comet-preview, 'message']")
        log.debug(
            f"What text are we finding here? Tag is: {element.tag_name} {element.text}")
    except Exception as e:
        log.debug("No posts found")
        log.error("Error: {}".format(e))


def main():

    log.debug("Scrape the curly girl website")
    facebook_page = "https://www.facebook.com/Vinthersklippekaelder"

    driver = webdriver.Firefox()
    driver.get(facebook_page)
    driver.implicitly_wait(5)

    sleep(3)
    click_only_essential_cookies(driver)
    extract_posts_from_page(driver)

    driver.close()


if __name__ == "__main__":
    main()
