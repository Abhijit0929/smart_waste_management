from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):

    HERO_TITLE = (
        By.XPATH,
        "//h1[contains(.,'Smart')]"
    )

    REPORT_WASTE_BUTTON = (
        By.LINK_TEXT,
        "Report Waste"
    )

    FIND_BINS_BUTTON = (
        By.LINK_TEXT,
        "Find Nearby Bins"
    )

    def __init__(self, driver):
        super().__init__(driver)

    def is_loaded(self):
        return self.is_visible(self.HERO_TITLE)

    def click_report_waste(self):
        self.click(self.REPORT_WASTE_BUTTON)

    def click_find_bins(self):
        self.click(self.FIND_BINS_BUTTON)