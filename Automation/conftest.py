import pytest

from utils.driver_factory import DriverFactory
from utils.screenshot import take_screenshot

from pages.login_page import LoginPage
from pages.home_page import HomePage

from config.settings import Settings


# --------------------------------------------------
# Pytest Command Line Options
# --------------------------------------------------

def pytest_addoption(parser):

    parser.addoption(
        "--browser",
        action="store",
        default="",
        help="Browser: chrome | edge | firefox"
    )

    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment: dev | qa | staging | prod"
    )


# --------------------------------------------------
# Settings Fixture
# --------------------------------------------------

@pytest.fixture(scope="session")
def settings(request):

    env = request.config.getoption("--env")

    return Settings(env)


# --------------------------------------------------
# Driver Fixture
# --------------------------------------------------

@pytest.fixture
def driver(request, settings):

    browser = request.config.getoption("--browser")

    # Use browser from .env if not supplied
    if browser == "":
        browser = settings.BROWSER

    driver = DriverFactory.get_driver(browser)

    yield driver

    driver.quit()


# --------------------------------------------------
# Logged In User
# --------------------------------------------------

@pytest.fixture
def logged_in_user(driver, settings):

    login = LoginPage(driver, settings)

    home = HomePage(driver)

    login.open()

    login.login(
        settings.USERNAME,
        settings.PASSWORD
    )

    assert home.is_loaded()

    return driver


# --------------------------------------------------
# Screenshot on Failure
# --------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver")

        if driver:

            take_screenshot(driver, item.name)