import pytest
import allure
from framework.browser.browser import Browser
from tests.api.gmail_api import GmailAPI
from tests.config.browser import BrowserConfig
from tests.config.browser import Grid


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=BrowserConfig.BROWSER,
                     help="Name of browser")
    parser.addoption("--grid_port", action="store", default=Grid.GRID_PORT,
                     help="Port of remote connection")


@pytest.fixture
def browser(request):
    """
        Создание сессии браузера с именем из конфиг файла.
    Args:
    """
    with allure.step("Создание сессии браузера из конфиг файла"):
        browser = request.config.getoption('--browser')
        Browser.get_browser().set_up_driver(browser_key=browser, grid_port=request.config.getoption('--grid_port'))
        Browser.get_browser().maximize(browser_key=browser)

    yield Browser.get_browser()

    with allure.step("Закрытие сессий всех браузеров"):
        for browser_key in list(Browser.get_browser().get_driver_names()):
            Browser.get_browser().quit(browser_key=browser_key)


@pytest.fixture
def gmail():
    return GmailAPI()
