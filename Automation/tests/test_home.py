from pages.login_page import LoginPage
from pages.home_page import HomePage
import json


def test_home_page_loaded(logged_in_user):

    driver = logged_in_user

    home = HomePage(driver)

    assert home.is_loaded()