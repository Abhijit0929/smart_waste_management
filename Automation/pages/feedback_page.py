from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import BASE_URL
from utils.logger import get_logger


class FeedbackPage(BasePage):

    logger = get_logger(__name__)

    URL = BASE_URL + "feedback/"

    # Locators (click labels since inputs are display:none)
    CAT_BUG = (By.XPATH, "//label[@for='cat_bug']")
    CAT_FEAT = (By.XPATH, "//label[@for='cat_feat']")
    CAT_IMP = (By.XPATH, "//label[@for='cat_imp']")
    CAT_GEN = (By.XPATH, "//label[@for='cat_gen']")

    MESSAGE_INPUT = (By.ID, "fb_message")
    SUBMIT_BUTTON = (By.ID, "fbSubmitBtn")
    SUCCESS_CARD = (By.CLASS_NAME, "success-card")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        self.logger.info("Opening Feedback Page")
        self.driver.get(self.URL)

    def is_loaded(self):
        self.logger.info("Checking if Feedback Page is loaded")
        return self.is_visible(self.MESSAGE_INPUT)

    def select_category(self, category):
        self.logger.info(f"Selecting feedback category: {category}")
        cat = category.lower()
        if cat == "bug":
            self.click(self.CAT_BUG)
        elif cat == "feature":
            self.click(self.CAT_FEAT)
        elif cat == "improvement":
            self.click(self.CAT_IMP)
        else:
            self.click(self.CAT_GEN)

    def select_rating(self, rating):
        self.logger.info(f"Selecting feedback rating: {rating}")
        rating_locator = (By.XPATH, f"//label[@for='r{rating}']")
        self.click(rating_locator)

    def enter_message(self, message):
        self.logger.info(f"Entering feedback message: {message}")
        self.enter_text(self.MESSAGE_INPUT, message)

    def click_submit(self):
        self.logger.info("Clicking feedback submit button")
        self.click(self.SUBMIT_BUTTON)

    def is_success_displayed(self):
        self.logger.info("Checking for feedback submission success")
        return self.is_visible(self.SUCCESS_CARD)
