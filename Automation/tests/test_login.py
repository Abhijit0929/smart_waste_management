import json

from pages.login_page import LoginPage
from pages.home_page import HomePage


def test_valid_login(driver):

    with open("testdata/login_data.json") as file:
        data = json.load(file)

    login = LoginPage(driver)
    home = HomePage(driver)

    login.open()

    login.login(
        data["username"],
        data["password"]
    )

    assert home.is_loaded()