from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import BASE_URL
from utils.logger import get_logger


class HomePage(BasePage):

    logger = get_logger(__name__)

    URL = BASE_URL

    PAGE_TITLE = (
        By.XPATH,
        "//h1[contains(.,'Smart') and contains(.,'Waste')]"
    )

    REPORT_WASTE_BTN = (
        By.XPATH,
        "//a[contains(@href, '/report/')]"
    )

    FIND_BINS_BTN = (
        By.XPATH,
        "//a[contains(@href, '/bins/')]"
    )

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        self.logger.info("Opening Home Page")
        self.driver.get(self.URL)

    def is_loaded(self):
        self.logger.info("Checking if Home Page is loaded")
        return self.is_visible(self.PAGE_TITLE)

    def click_report_waste(self):
        self.logger.info("Clicking Report Waste button")
        self.click(self.REPORT_WASTE_BTN)

    def click_find_bins(self):
        self.logger.info("Clicking Find Bins button")
        self.click(self.FIND_BINS_BTN)
