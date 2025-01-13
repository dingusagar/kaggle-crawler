"""
# Author: Yinghao Li
# Modified: January 13th, 2025
# ---------------------------------------
# Description: Load online articles and convert them to HTML strings
"""

import time
import os
import os.path as osp

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException

from tqdm.auto import tqdm

__all__ = ["load_online_html"]


def scroll_down(driver_var, value):
    driver_var.execute_script("window.scrollBy(0," + str(value) + ")")


# Scroll down the page
def scroll_down_page(driver, n_max_try=100):

    old_page = driver.page_source
    for _ in range(n_max_try):
        for i in range(2):
            scroll_down(driver, 500)
            time.sleep(0.5)
        new_page = driver.page_source
        if new_page != old_page:
            old_page = new_page
        else:
            break
    return True


def load_online_html(page) -> str:
    """
    Load online articles and convert them to HTML strings

    Parameters
    ----------
    doi: article DOI

    Returns
    -------
    HTML string
    """

    article_url = f"https://www.kaggle.com/competitions?page={page}"
    driver = load_webdriver(headless=True)

    driver.get(article_url)
    scroll_down_page(driver)
    # time.sleep(1)

    html_content = driver.page_source

    driver.quit()
    return html_content


def load_webdriver(headless: bool = True) -> WebDriver:
    """
    A more robust way to load chrome webdriver (compatible with headless mode)

    Returns
    -------
    WebDriver
    """
    try:
        options = Options()
        if headless:
            options.headless = True
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            )
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    except WebDriverException:

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver


def main():
    for page_idx in tqdm(range(1, 35)):
        html_content = load_online_html(page_idx)
        os.makedirs("pages", exist_ok=True)
        with open(osp.join("pages", f"page_{page_idx}.html"), "w") as f:
            f.write(html_content)

        time.sleep(1)


if __name__ == "__main__":
    main()
