from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os


class DriverFactory:

    @staticmethod
    def get_driver(browser_name="chrome"):
        browser = browser_name.lower()

        if browser == "chrome":
            options = ChromeOptions()
            if os.getenv("CI") == "true":
                options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--disable-gpu")
                options.add_argument("--disable-extensions")
            else:
                options.add_argument("--disable-infobars")
                options.add_argument("--start-maximized")

            driver = webdriver.Chrome(
                service=ChromeService(
                    ChromeDriverManager().install()
                ),
                options=options
            )

        elif browser == "firefox":
            options = FirefoxOptions()
            if os.getenv("CI") == "true":
                options.add_argument("--headless")

            driver = webdriver.Firefox(
                service=FirefoxService(
                    GeckoDriverManager().install()
                ),
                options=options
            )

        elif browser == "edge":
            options = EdgeOptions()
            if os.getenv("CI") == "true":
                options.add_argument("--headless")

            driver = webdriver.Edge(
                service=EdgeService(
                    EdgeChromiumDriverManager().install()
                ),
                options=options
            )

        else:
            raise ValueError(f"Unsupported browser type: {browser_name}")

        driver.implicitly_wait(10)

        return driver