from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()

options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=ChromeService(
        ChromeDriverManager().install()
    ),
    options=options
)

class DriverFactory:

    @staticmethod
    def get_driver(browser="chrome"):

        browser = browser.lower()

        if browser == "chrome":

            driver = webdriver.Chrome(
                service=ChromeService(
                    ChromeDriverManager().install()
                )
            )

        elif browser == "edge":

            driver = webdriver.Edge(
                service=EdgeService(
                    EdgeChromiumDriverManager().install()
                )
            )

        elif browser == "firefox":

            driver = webdriver.Firefox(
                service=FirefoxService(
                    GeckoDriverManager().install()
                )
            )

        else:

            raise Exception(
                f"Browser '{browser}' is not supported."
            )

        driver.maximize_window()
        driver.implicitly_wait(5)

        return driver   