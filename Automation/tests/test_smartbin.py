import time
from pages.smartbin_page import SmartBinPage


def test_smartbin_filtering(logged_in_user):
    driver = logged_in_user
    smartbin_page = SmartBinPage(driver)

    # 1. Open the nearby smart bins page
    smartbin_page.open()
    assert smartbin_page.is_loaded(), "Smart Bin Page should be loaded"

    # 2. Check total bins initially loaded
    total_bins = smartbin_page.get_total_bins()
    smartbin_page.logger.info(f"Total bins found: {total_bins}")

    # 3. Test 'Available' filter (shows 'empty' status)
    smartbin_page.click_available()
    time.sleep(1)  # wait for filtering animation/DOM transition

    statuses = smartbin_page.get_visible_statuses()
    for status in statuses:
        assert status == "empty", f"Bin status should be 'empty' (Available), but got '{status}'"

    # 4. Test 'Full' filter (shows 'full' status)
    smartbin_page.click_full()
    time.sleep(1)

    statuses = smartbin_page.get_visible_statuses()
    for status in statuses:
        assert status == "full", f"Bin status should be 'full', but got '{status}'"

    # 5. Test 'All' filter restores full list
    smartbin_page.click_all()
    time.sleep(1)
    assert smartbin_page.get_total_bins() == total_bins, "Total bins count should match initial count"
