from framework.browser.browser import Browser
from tests.pages.home_page import HomePage
import allure


class TestFunctional(object):
    def test_framework(self, create_browser):
        with allure.step("First step"):
            Browser.get_browser().set_url('https://userinyerface.com/')
            home_page = HomePage()
            login = 'TestAccNik'
            password = 'qwaszx@1'
            home_page.login(login, password)

            # Logger.info('13123')
            # home_page.wait_for_page_opened()
            # log = logging.getLogger("Logger")
            # log.info('sdf')
            # logging.info('sdfsdfdsfsdf')
            # logging.error('sdfsdfdsfsdf')
            # logging.warning('sdfsdfdsfsdf')
        # finally:
        #     Browser.quit('chrome')
