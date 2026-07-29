from utils.wait_utils import WaitUtils


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WaitUtils(driver)

    def click(self, locator):
        self.wait.wait_for_clickable(locator).click()

    def enter_text(self, locator, text):
        element = self.wait.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.wait.wait_for_element(locator).text

    def is_visible(self, locator):
        try:
            return self.wait.wait_for_element(locator).is_displayed()
        except:
            return False

    def get_element(self, locator):
        return self.wait.wait_for_element(locator)

    def get_elements(self, locator):
        return self.driver.find_elements(*locator)