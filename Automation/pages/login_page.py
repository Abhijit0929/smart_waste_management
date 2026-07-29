from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import BASE_URL
from utils.logger import get_logger


class LoginPage(BasePage):

    logger = get_logger(__name__)

    # URL
    URL = BASE_URL + "login/"

    # Locators
    USERNAME = (By.ID, "id_username")
    PASSWORD = (By.ID, "id_password")
    LOGIN_BUTTON = (By.ID, "loginBtn")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        print("logger method excuted")
        self.logger.info("Opening Login Page")
        self.driver.get(self.URL)

    def enter_username(self, username):
        self.logger.info(f"Entering Username: {username}")
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