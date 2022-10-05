from tests.pages.details_page import DetailsPage
from tests.pages.home_page import HomePage
from tests.pages.interests_page import InterestsPage
from tests.pages.email_page import EmailPage
from tests.testData.testData import TestData
import allure


class TestFunctional(object):
    def test_login(self, create_browser):
        with allure.step("First step"):

            home_page = HomePage()
            assert home_page.welcome_page_is_open(), "Welcome page is not open"

            home_page.go_to_next_page()
            email_page = EmailPage()
            assert email_page.card_is_open(), "Email card is not open"

            email_page.fill_login_page_and_click_next()
            interests_page = InterestsPage()
            assert interests_page.card_is_open(), "Interests card is not open"

            interests_page.fill_interests_page_and_click_next()
            details_page = DetailsPage()
            assert details_page.card_is_open(), "Details card is not open"

    def test_hide_help(self, create_browser):
        with allure.step("First step"):

            home_page = HomePage()
            assert home_page.welcome_page_is_open(), "Welcome page is not open"

            home_page.go_to_next_page()
            email_page = EmailPage()
            email_page.hide_help_form()
            assert email_page.help_form_is_hidden(), "Help form is not hidden"

    def test_accept_cookies(self, create_browser):
        with allure.step("First step"):

            home_page = HomePage()
            assert home_page.welcome_page_is_open(), "Welcome page is not open"

            home_page.go_to_next_page()
            email_page = EmailPage()
            email_page.accept_cookies()
            assert email_page.cookies_form_is_hidden(), "Cookies form is not hidden"

    def test_timer(self, create_browser):
        with allure.step("First step"):

            home_page = HomePage()
            assert home_page.welcome_page_is_open(), "Welcome page is not open"

            home_page.go_to_next_page()
            email_page = EmailPage()
            assert email_page.check_initial_timer_value(TestData.TIMER_VALUE), f"Timer did not start from {TestData.TIMER_VALUE}"
