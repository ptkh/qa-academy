from _pytest.fixtures import FixtureRequest
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.runner import CallInfo
from _pytest.terminal import TerminalReporter
from framework.utils.datetime_util import DatetimeUtil
from framework.browser.browser import Browser
from tests.config.browser import BrowserConfig
from tests.config.browser import Grid
from tests.database.database import MySQL
import platform
import pytest
import allure


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=BrowserConfig.BROWSER,
                     help="Name of browser")
    parser.addoption("--grid_port", action="store", default=Grid.GRID_PORT,
                     help="Port of remote connection")


@pytest.fixture(scope="session")
def create_browser(request):
    """
        Создание сессии браузера с именем из конфиг файла.
    Args:

    """
    with allure.step("Создание сессии браузера из конфиг файла"):
        browser = request.config.getoption('--browser')
        Browser.get_browser().set_up_driver(browser_key=browser, grid_port=request.config.getoption('--grid_port'))
        Browser.get_browser().maximize(browser_key=browser)

    yield

    with allure.step("Закрытие сессий всех браузеров"):
        for browser_key in list(Browser.get_browser().get_driver_names()):
            Browser.get_browser().quit(browser_key=browser_key)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(terminalreporter: TerminalReporter, request: FixtureRequest, item: Item, call: CallInfo,
                              session: Session):
    yield
    with allure.step("Setting up MySQL database connection"):
        db = MySQL()
        # NOT SURE about restoring dump.sql, restored data doesn't persist in database

    with allure.step("Inserting project, author and session into corresponding tables"):
        db.insert_project('L2-p.khachidze')

        db.insert_author('p.khachidze')
        # NOT SURE about author table, no columns, empty table

        db.insert_session(session=session)
        # NOT SURE about session_key/ created_time /build_number

    with allure.step("Checking status of the test (1: PASSED/ 2: FAILED/ 3: SKIPPED)"):
        passed = [passed.nodeid for passed in terminalreporter.stats.get('passed', [])]
        if item.nodeid in passed:
            status_id = 1
        else:
            failed = [failed.nodeid for failed in terminalreporter.stats.get('failed', [])]
            if item.nodeid in failed:
                status_id = 2
            else:
                status_id = 3

    with allure.step("Inserting test result into test table"):
        db.insert_test(result={'name': 'NULL',
                               'status_id': status_id,
                               'method_name': request.function,
                               'project_id': db.project_id,
                               'session_id': db.session_id,
                               'start_time': DatetimeUtil.convert_timestamp_to_sql_datetime(call.start),
                               'end_time': DatetimeUtil.convert_timestamp_to_sql_datetime(call.stop),
                               'env': f"{platform.node()}|{platform.machine()}|{platform.system()}",
                               'browser': request.config.getoption('--browser'),
                               'author_id': db.author_id})
