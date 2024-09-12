import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", help="Run tests in headless mode"
    )


@pytest.fixture(scope='class')
def web_driver(request):
    chrome_options = Options()

    # Check if --headless option is passed
    if request.config.getoption("--headless"):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")

    # Set the correct path for chromedriver on Ubuntu
    service = Service('/usr/local/bin/chromedriver')

    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()
