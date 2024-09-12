import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import platform


@pytest.fixture(scope='class')
def web_driver(request):
    chrome_options = Options()
    if request.config.getoption("--headless"):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")

    # Detect the OS platform and set driver path accordingly
    if platform.system() == "Windows":
        service = Service('C:\\chromedriver.exe')
    else:
        service = Service('/usr/local/bin/chromedriver')  # Path for Linux

    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()
