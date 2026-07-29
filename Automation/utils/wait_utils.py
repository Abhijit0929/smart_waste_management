from selenium.webdriver.support.ui import WebDriverWait

def wait(driver, timeout=10):
    return WebDriverWait(driver, timeout)
