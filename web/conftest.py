import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import allure
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run tests in headless mode"
    )


@pytest.fixture(scope='class')
def web_driver(request):
    chrome_options = Options()

    # Set headless mode based on environment (CI or local) and user option
    if os.getenv('CI'):  # In CI environment (like GitHub Actions)
        chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = "/usr/bin/google-chrome"  # Path to Chrome in CI
        driver_path = "/usr/bin/chromedriver"  # Path to ChromeDriver in CI
    else:  # Local environment
        if request.config.getoption("--headless"):
            chrome_options.add_argument("--headless")
        driver_path = 'C:\\chromedriver.exe'  # Path to ChromeDriver locally

    driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
    driver.maximize_window()

    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, report):
    if report.failed:
        driver = node.funcargs.get('web_driver', None)
        if driver:
            screenshot_path = f"screenshots/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_failure.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            driver.save_screenshot(screenshot_path)
            allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            logging.error(f"Screenshot saved to {screenshot_path}")
        logging.error(f"Test failed: {report.nodeid}")
