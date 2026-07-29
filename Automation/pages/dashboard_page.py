from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL
from utils.logger import get_logger


class DashboardPage(BasePage):

    logger = get_logger(__name__)

    URL = BASE_URL + "dashboard/"

    PAGE_TITLE = (
        By.XPATH,
        "//h1[contains(.,'Dashboard')]"
    )

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        self.logger.info("Opening Dashboard Page")
        self.driver.get(self.URL)

    def is_loaded(self):
        self.logger.info("Checking Dashboard Page")
        return self.is_visible(self.PAGE_TITLE)