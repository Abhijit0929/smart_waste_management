import json
import os
import sys
import pytest


# We set environment variables as early as possible so that module-level imports
# of page classes (which load settings/config) get the correct environment.
def pytest_configure(config):
    env = config.getoption("--env", default="dev")
    browser = config.getoption("--browser", default="chrome")
    os.environ["TEST_ENV"] = env
    os.environ["TEST_BROWSER"] = browser


@pytest.fixture(scope="session", autouse=True)
def seed_test_data():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_project.settings")
    # Add api_project root to python path to resolve django settings
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.append(project_root)

    import django
    django.setup()

    from main.models import SmartBin
    from django.db import IntegrityError

    # Seed bins if empty, catching integrity errors for parallel workers
    if SmartBin.objects.count() == 0:
        try:
            SmartBin.objects.create(
                location="Main Street bin",
                fill_level=20,
                status="empty",
                latitude=18.5207,
                longitude=73.8587
            )
            SmartBin.objects.create(
                location="Broadway Avenue bin",
                fill_level=95,
                status="full",
                latitude=18.5308,
                longitude=73.8688
            )
            SmartBin.objects.create(
                location="Central Park bin",
                fill_level=45,
                status="empty",
                latitude=18.5109,
                longitude=73.8489
            )
            print("\nSeeded 3 smart bins in the database.")
        except IntegrityError:
            # Another parallel pytest worker has already seeded the database
            pass


from utils.driver_factory import DriverFactory
from utils.screenshot import take_screenshot

from pages.login_page import LoginPage
from pages.home_page import HomePage
from config.settings import Settings


# --------------------------
# Browser Option
# --------------------------

def pytest_addoption(parser):

    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser: chrome | edge | firefox"
    )

    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment: dev | qa | staging | prod"
    )


# --------------------------
# Driver Fixture
# --------------------------

@pytest.fixture
def driver(request):

    env = request.config.getoption("--env")

    settings = Settings(env)

    browser = request.config.getoption("--browser")

    driver = DriverFactory.get_driver(browser)

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def settings(request):

    env = request.config.getoption("--env")

    return Settings(env)


# --------------------------
# Logged In Fixture
# --------------------------

@pytest.fixture
def logged_in_user(driver):

    json_path = os.path.join(
        "testdata",
        "login_data.json"
    )

    with open(json_path) as file:

        data = json.load(file)

    login = LoginPage(driver)

    home = HomePage(driver)

    login.open()

    login.login(
        data["username"],
        data["password"]
    )

    assert home.is_loaded()

    return driver


# --------------------------
# Screenshot on Failure
# --------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver")

        if driver:

            take_screenshot(driver, item.name)