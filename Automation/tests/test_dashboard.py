from pages.dashboard_page import DashboardPage


def test_dashboard(logged_in_user):

    driver = logged_in_user

    dashboard = DashboardPage(driver)

    dashboard.open()

    assert dashboard.is_loaded()