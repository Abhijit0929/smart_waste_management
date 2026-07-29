import os
import time
from PIL import Image
import pytest
from pages.report_page import ReportPage


@pytest.fixture
def dummy_image():
    path = os.path.join("testdata", "dummy.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        img = Image.new("RGB", (100, 100), color="green")
        img.save(path)
    yield os.path.abspath(path)


def test_report_waste_submission(logged_in_user, dummy_image):
    driver = logged_in_user
    report_page = ReportPage(driver)

    # 1. Open the report waste page
    report_page.open()
    assert report_page.is_loaded(), "Report waste page should be loaded"

    # 2. Enter location, description, and upload photo
    report_page.enter_location("Pune, Maharashtra, India")
    report_page.upload_photo(dummy_image)
    report_page.enter_description("Automated test: Pile of garbage detected near the smart bin.")

    # 3. Submit
    report_page.click_submit()
    time.sleep(2)

    # 4. Assert redirect to the reports summary list
    current_url = driver.current_url.lower()
    assert "reports" in current_url, f"Expected redirect to /reports/, but was: {current_url}"
