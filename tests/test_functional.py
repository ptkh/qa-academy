from framework.browser.browser import Browser
from tests.pages.home_page import HomePage
from tests.pages.login_page import LoginPage
import allure


class TestFunctional(object):
    def test_framework(self, create_browser):
        with allure.step("First step"):
            Browser.get_browser().set_url('https://userinyerface.com/')
            home_page = HomePage()
            home_page.go_to_next_page()
            assert 1
            login_page = LoginPage()
            login_page.fill_login_form_and_click_next()
            assert 1

            # Logger.info('13123')
            # home_page.wait_for_page_opened()
            # log = logging.getLogger("Logger")
            # log.info('sdf')
            # logging.info('sdfsdfdsfsdf')
            # logging.error('sdfsdfdsfsdf')
            # logging.warning('sdfsdfdsfsdf')
        # finally:
        #     Browser.quit('chrome')
