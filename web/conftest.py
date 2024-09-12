import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import allure
import os
from datetime import datetime

# Configure logging
import logging

logging.basicConfig(level=logging.INFO)


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run tests in headless mode"
    )
    parser.addoption(
        "--testcase", action="store", default=None, help="Specify the test case file to run"
    )


@pytest.fixture(scope='class')
def web_driver(request):
    # Set up Chrome options for headless mode if needed
    chrome_options = Options()
    if request.config.getoption("--headless"):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")

    # Set up the Chrome WebDriver instance
    service = Service('C:\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, report):
    if report.failed:
        driver = node.funcargs.get('web_driver')
        if driver:
            screenshot_path = f"screenshots/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_failure.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            driver.save_screenshot(screenshot_path)
            allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            logging.error(f"Screenshot saved to {screenshot_path}")
        logging.error(f"Test failed: {report.nodeid}")
