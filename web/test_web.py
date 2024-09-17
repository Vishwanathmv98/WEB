import pytest
import logging
import allure
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)


class TestGoogleSearch:

    def take_screenshot(self, driver, test_name):
        # Create a screenshot path
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir,
                                       f"{test_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")

        # Take a screenshot
        driver.save_screenshot(screenshot_path)

        # Attach screenshot to Allure report
        allure.attach.file(screenshot_path, name=f"{test_name} Screenshot", attachment_type=allure.attachment_type.PNG)
        logging.info(f"Screenshot saved to {screenshot_path}")

    @pytest.mark.basic_flows
    @pytest.mark.usefixtures("web_driver")
    def test_open_google(self, web_driver):
        driver = web_driver

        try:
            # Open Google
            driver.get("https://www.google.com")
            logging.info("Opened Google Homepage")

            # Verify the title
            assert "Google" in driver.title, "Google homepage title not found!"
            logging.info("Verified Google homepage title")

        except Exception as e:
            self.take_screenshot(driver, "test_open_google")
            raise e  # Re-raise the exception to ensure pytest records the failure
