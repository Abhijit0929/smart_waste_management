from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger


class LoginPage(BasePage):

    logger = get_logger(__name__)

    # Locators
    USERNAME = (By.ID, "id_username")
    PASSWORD = (By.ID, "id_password")
    LOGIN_BUTTON = (By.ID, "loginBtn")

    def __init__(self, driver, settings):
        super().__init__(driver)
        self.settings = settings

    def open(self):
        self.logger.info("Opening Login Page")
        self.driver.get(f"{self.settings.BASE_URL}/login/")

    def enter_username(self, username):
        self.logger.info("Entering Username")
        self.enter_text(self.USERNAME, username)

    def enter_password(self, password):
        self.logger.info("Entering Password")
        self.enter_text(self.PASSWORD, password)

    def click_login(self):
        self.logger.info("Clicking Login Button")
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        self.logger.info("Starting Login Process")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        self.logger.info("Login Request Submitted")