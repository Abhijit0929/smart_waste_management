from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL
from utils.logger import get_logger


class SmartBinPage(BasePage):

    logger = get_logger(__name__)

    URL = BASE_URL + "bins/"

    # Page Title
    PAGE_TITLE = (
        By.XPATH,
        "//h1[contains(.,'Nearby Smart')]"
    )

    # Bin Cards
    BIN_CARDS = (
        By.CLASS_NAME,
        "bin-card"
    )

    BIN_LOCATION = (
        By.CLASS_NAME,
        "bin-location"
    )

    FILL_LEVEL = (
        By.CLASS_NAME,
        "fill-pct"
    )

    # Filter Buttons
    ALL_BUTTON = (
        By.XPATH,
        "//button[text()='All']"
    )

    AVAILABLE_BUTTON = (
        By.XPATH,
        "//button[text()='Available']"
    )

    FULL_BUTTON = (
        By.XPATH,
        "//button[text()='Full']"
    )

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        self.logger.info("Opening Smart Bin Page")
        self.driver.get(self.URL)

    def is_loaded(self):
        return self.is_visible(self.PAGE_TITLE)

    def get_bin_cards(self):
        self.logger.info("Fetching Smart Bin cards")
        return self.get_elements(self.BIN_CARDS)

    def get_total_bins(self):
        return len(self.get_bin_cards())

    def get_locations(self):
        self.logger.info("Fetching bin locations")

        locations = self.get_elements(self.BIN_LOCATION)

        return [location.text.strip() for location in locations]

    def get_fill_levels(self):
        self.logger.info("Fetching fill levels")

        fills = self.get_elements(self.FILL_LEVEL)

        values = []

        for fill in fills:

            text = fill.text.replace("%", "").strip()

            try:
                values.append(int(text))
            except ValueError:
                continue

        return values

    def click_all(self):
        self.logger.info("Clicking All Filter")
        self.click(self.ALL_BUTTON)

    def click_available(self):
        self.logger.info("Clicking Available Filter")
        self.click(self.AVAILABLE_BUTTON)

    def click_full(self):
        self.logger.info("Clicking Full Filter")
        self.click(self.FULL_BUTTON)

    def get_visible_cards(self):

        cards = self.get_elements(self.BIN_CARDS)

        return [
            card
            for card in cards
            if card.is_displayed()
        ]

    def get_visible_statuses(self):

        cards = self.get_visible_cards()

        return [
            card.get_attribute("data-status")
            for card in cards
        ]