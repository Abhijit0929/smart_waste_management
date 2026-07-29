from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()

    def enter_text(self, locator, value):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(value)

    def get_text(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).text

    def is_visible(self, locator):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except:
            return False

    def get_element(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def get_elements(self, locator):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )