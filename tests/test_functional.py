from tests.pages.home_page import HomePage
from tests.pages.login_page import LoginPage
import allure


class TestFunctional(object):
    def test_login(self, create_browser):
        with allure.step("First step"):

            home_page = HomePage()
            assert home_page.welcome_page_is_open()

            home_page.go_to_next_page()
            login_page = LoginPage()
            assert login_page.card_is_open(1)

            login_page.fill_card_1_and_click_next()
            assert login_page.card_is_open(2)

            login_page.fill_card_2_and_click_next()
            assert login_page.card_is_open(3)

    def test_hide_help(self, create_browser):
        with allure.step("First step"):

            home_page = HomePage()
            assert home_page.welcome_page_is_open()

            home_page.go_to_next_page()
            login_page = LoginPage()
            login_page.hide_help_form()
            assert login_page.help_form_is_hidden()

    def test_accept_cookies(self, create_browser):
        with allure.step("First step"):

            home_page = HomePage()
            assert home_page.welcome_page_is_open()

            home_page.go_to_next_page()
            login_page = LoginPage()
            login_page.accept_cookies()
            assert login_page.cookies_form_is_hidden()

    def test_timer(self, create_browser):
        with allure.step("First step"):

            home_page = HomePage()
            assert home_page.welcome_page_is_open()

            home_page.go_to_next_page()
            login_page = LoginPage()
            assert login_page.initial_timer_value_is("00:00:00")
