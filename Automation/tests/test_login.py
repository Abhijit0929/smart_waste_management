import pytest

from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.excel_reader import ExcelReader

reader = ExcelReader("testdata/login_data.xlsx")
test_data = reader.get_data("login")


@pytest.mark.parametrize("data", test_data)
def test_login(driver, settings, data):

    login = LoginPage(driver, settings)
    home = HomePage(driver)

    login.open()

    login.login(
        data["Username"],
        data["Password"]
    )

    if data["Expected"] == "Pass":

        assert home.is_loaded()

    else:

        assert not home.is_loaded()