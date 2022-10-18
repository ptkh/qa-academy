import time
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from framework.browser.browser import Browser
from tests.config.browser import BrowserConfig
from tests.config.browser import Grid
from tests.config.urls import Urls
from tests.database.database import MySQL
import pytest
import allure


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=BrowserConfig.BROWSER,
                     help="Name of browser")
    parser.addoption("--grid_port", action="store", default=Grid.GRID_PORT,
                     help="Port of remote connection")


@pytest.fixture(scope="function")
def create_browser(request):
    """
        Создание сессии браузера с именем из конфиг файла.
    Args:

    """
    with allure.step("Создание сессии браузера из конфиг файла"):
        browser = request.config.getoption('--browser')
        Browser.get_browser().set_up_driver(browser_key=browser, grid_port=request.config.getoption('--grid_port'))
        Browser.get_browser().maximize(browser_key=browser)
        Browser.get_browser().set_url(Urls.TEST_URL)

    yield

    with allure.step("Закрытие сессий всех браузеров"):
        for browser_key in list(Browser.get_browser().get_driver_names()):
            Browser.get_browser().quit(browser_key=browser_key)


@pytest.fixture(scope='session')
def db():
    with allure.step("Setting up MySQL database connection"):
        db = MySQL()
        yield db
        db.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    start_time = time.time()
    yield
    report = TestReport.from_item_and_call(item, call)
    MySQL.saved_results.append((start_time, report))

