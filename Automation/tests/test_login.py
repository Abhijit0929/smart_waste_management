import json

from pages.login_page import LoginPage


def test_valid_login(driver):

    with open("testdata/login_data.json") as file:
        data = json.load(file)

    login = LoginPage(driver)

    login.open()

    login.login(
        data["username"],
        data["password"]
    )

    assert "dashboard" in driver.current_url.lower()