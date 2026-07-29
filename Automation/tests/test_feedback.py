import time
from pages.feedback_page import FeedbackPage


def test_feedback_submission(logged_in_user):
    driver = logged_in_user
    feedback_page = FeedbackPage(driver)

    # 1. Open the feedback page
    feedback_page.open()
    assert feedback_page.is_loaded(), "Feedback page should be loaded"

    # 2. Select category, rating, and fill message
    feedback_page.select_category("bug")
    feedback_page.select_rating("5")
    feedback_page.enter_message("This is an automated test feedback for waste management system.")

    # 3. Submit
    feedback_page.click_submit()
    time.sleep(1)

    # 4. Assert success message is displayed
    assert feedback_page.is_success_displayed(), "Feedback submission success screen should be displayed"
