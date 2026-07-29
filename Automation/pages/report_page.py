from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import BASE_URL
from utils.logger import get_logger


class ReportPage(BasePage):

    logger = get_logger(__name__)

    URL = BASE_URL + "report/"

    # Locators
    LOCATION_INPUT = (By.ID, "location")
    PHOTO_INPUT = (By.ID, "photo-input")
    DESCRIPTION_INPUT = (By.NAME, "description")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(@class, 'submit-btn')]")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        self.logger.info("Opening Report Page")
        self.driver.get(self.URL)

    def is_loaded(self):
        self.logger.info("Checking if Report Page is loaded")
        return self.is_visible(self.LOCATION_INPUT)

    def enter_location(self, location_text):
        self.logger.info(f"Entering location text: {location_text}")
        self.enter_text(self.LOCATION_INPUT, location_text)

    def upload_photo(self, photo_path):
        self.logger.info(f"Uploading photo from path: {photo_path}")
        # Use get_element (presence wait) directly since the file input is styled as display:none
        element = self.get_element(self.PHOTO_INPUT)
        element.send_keys(photo_path)

    def enter_description(self, description_text):
        self.logger.info(f"Entering description: {description_text}")
        self.enter_text(self.DESCRIPTION_INPUT, description_text)

    def click_submit(self):
        self.logger.info("Clicking report submit button")
        self.click(self.SUBMIT_BUTTON)
