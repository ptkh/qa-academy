import time
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from framework.utils.datetime_util import DatetimeUtil
from framework.browser.browser import Browser
from framework.utils.logger import Logger
from framework.utils.random_util import RandomUtil
from tests.config.browser import BrowserConfig
from tests.config.browser import Grid
from tests.config.urls import Urls
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
        Browser.get_browser().set_url(Urls.TEST_URL)

    yield

    with allure.step("Закрытие сессий всех браузеров"):
        for browser_key in list(Browser.get_browser().get_driver_names()):
            Browser.get_browser().quit(browser_key=browser_key)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    start_time = time.time()
    yield
    with allure.step("Setting up MySQL database connection"):
        db = MySQL()
    with allure.step("Inserting project, author and session into corresponding tables"):
        db.insert_project('L2-p.khachidze')
        db.insert_author(name='p.khachidze', login='p.khachidze', email='p.khachidze@qa-academy.by')
        db.insert_session()
    report = TestReport.from_item_and_call(item, call)
    with allure.step("Checking status of the test (1: PASSED/ 2: FAILED/ 3: SKIPPED)"):
        status_id = 1
        if report.failed:
            status_id = 2
        elif report.skipped:
            status_id = 3
    with allure.step("Inserting test result into test table"):
        s_time = DatetimeUtil.convert_timestamp_to_sql_datetime(start_time)
        e_time = DatetimeUtil.convert_timestamp_to_sql_datetime(start_time + report.duration)
        db.insert_test(result={'name': f"'{report.head_line}'",
                               'status_id': status_id,
                               'method_name': f"'{report.location[0]}'",
                               'project_id': db.project_id,
                               'session_id': db.session_id,
                               'start_time': f"'{s_time}'",
                               'end_time': f"'{e_time}'",
                               'env': f"'{platform.node()}|{platform.machine()}|{platform.system()}'",
                               'browser': f"'{BrowserConfig.BROWSER}'",
                               'author_id': db.author_id})
    with allure.step("Inserting log into log table"):
        db.insert_log(log=report.caplog, is_exc=1 if status_id == 2 else 0)
    db.close()


@pytest.fixture(scope='session', autouse=True)
def processing_of_test_data():
    with allure.step("Setting up database"):
        db = MySQL()
    with allure.step("Selecting tests from database"):
        tests = db.fetch_tests_with_repeating_id()
    with allure.step("Inserting project, author and session into corresponding tables"):
        db.insert_project('L2-p.khachidze')
        db.insert_author(name='p.khachidze', login='p.khachidze', email='p.khachidze@qa-academy.by')
        db.insert_session()
    with allure.step("Mutating tests"):
        s_time = DatetimeUtil.convert_timestamp_to_sql_datetime(time.time())
        e_time = DatetimeUtil.convert_timestamp_to_sql_datetime(time.time() + RandomUtil.get_randint(0, 20))
        mutated_tests = []
        for test in tests:
            Logger.info(str(test))
            mutated_tests.append({'name': f'"{test[1]}"',
                                  'status_id': RandomUtil.get_randint(1, 4),
                                  'method_name': f'"{test[3]}"',
                                  'project_id': test[4],
                                  'session_id': db.session_id,
                                  'start_time': f"'{s_time}'",
                                  'end_time': f"'{e_time}'",
                                  'env': f"'{platform.node()}|{platform.machine()}|{platform.system()}'",
                                  'browser': f"'{BrowserConfig.BROWSER}'",
                                  'author_id': db.author_id})
    with allure.step("Inserting tests into database"):
        for test in mutated_tests:
            db.insert_test(test)
    with allure.step("Deleting previously selected tests from database"):
        db.delete_tests(tests)
    db.close()
    yield
