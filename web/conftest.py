import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope='class')
def web_driver(request):
    chrome_options = Options()

    # Set up the Chrome WebDriver instance
    service = Service('/usr/local/bin/chromedriver')

    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()
