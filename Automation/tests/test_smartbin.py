import pytest

from pages.smartbin_page import SmartBinPage


def test_full_filter(logged_in_user):

    driver = logged_in_user

    smartbin = SmartBinPage(driver)

    smartbin.open()

    smartbin.click_full()

    statuses = smartbin.get_visible_statuses()

    if len(statuses) == 0:
        pytest.skip("No full bins available to test.")

    assert all(status == "full" for status in statuses)