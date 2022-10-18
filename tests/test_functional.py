import platform
import time
import pytest
from framework.utils.datetime_util import DatetimeUtil
from framework.utils.random_util import RandomUtil
from tests.config.browser import BrowserConfig
from tests.pages.details_page import DetailsPage
from tests.pages.home_page import HomePage
from tests.pages.interests_page import InterestsPage
from tests.pages.email_page import EmailPage
from tests.testData.test_data import TestData
import allure


class TestFunctional(object):
    @pytest.mark.run(order=1)
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

    @pytest.mark.run(order=2)
    def test_hide_help(self, create_browser):
        with allure.step("First step"):
            home_page = HomePage()
            assert home_page.welcome_page_is_open(), "Welcome page is not open"

            home_page.go_to_next_page()
            email_page = EmailPage()
            email_page.hide_help_form()
            assert email_page.help_form_is_hidden(), "Help form is not hidden"

    @pytest.mark.run(order=3)
    def test_accept_cookies(self, create_browser):
        with allure.step("First step"):
            home_page = HomePage()
            assert home_page.welcome_page_is_open(), "Welcome page is not open"

            home_page.go_to_next_page()
            email_page = EmailPage()
            email_page.accept_cookies()
            assert email_page.cookies_form_is_hidden(), "Cookies form is not hidden"

    @pytest.mark.run(order=4)
    def test_timer(self, create_browser):
        with allure.step("First step"):
            home_page = HomePage()
            assert home_page.welcome_page_is_open(), "Welcome page is not open"

            home_page.go_to_next_page()
            email_page = EmailPage()
            assert email_page.check_initial_timer_value(TestData.TIMER_VALUE), \
                f"Timer did not start from {TestData.TIMER_VALUE}"

    @pytest.mark.run(order=5)
    def test_processing_of_test_data(self, db):
        with allure.step("Precondition: Selecting tests from database"):
            selected_tests = db.fetch_tests_with_repeating_id()
            db.insert_project('L2-p.khachidze')
            db.insert_author(name='p.khachidze', login='p.khachidze', email='p.khachidze@qa-academy.by')
            db.insert_session()
        with allure.step("Simulate the launch of the tests and insert into database"):
            s_time = DatetimeUtil.convert_timestamp_to_sql_datetime(time.time())
            e_time = DatetimeUtil.convert_timestamp_to_sql_datetime(time.time() + RandomUtil.get_randint(0, 20))
            updated_tests = []
            inserted_test_ids = []
            for test in selected_tests:
                updated_tests.append({'name': f'"{test[1]}"',
                                      'status_id': RandomUtil.get_randint(1, 4),
                                      'method_name': f'"{test[3]}"',
                                      'project_id': test[4],
                                      'session_id': db.session_id,
                                      'start_time': f"'{s_time}'",
                                      'end_time': f"'{e_time}'",
                                      'env': f"'{platform.node()}|{platform.machine()}|{platform.system()}'",
                                      'browser': f"'{BrowserConfig.BROWSER}'",
                                      'author_id': db.author_id})
            for test in updated_tests:
                db.insert_test(test)
                inserted_test_ids.append(db.test_id)
        with allure.step("Check that tests are completed and information is updated"):
            for ID in inserted_test_ids:
                assert db.select_test_by_id(id_=ID), "Information was not updated"
        with allure.step("Postcondition: Delete previously selected tests from database"):
            db.delete_tests(selected_tests)
        with allure.step("Check that records have been deleted"):
            for test in selected_tests:
                assert not db.select_test_by_id(id_=test[0]), "Record was not deleted"

    @pytest.mark.run(order=6)
    def test_add_new_entry(self, db):
        with allure.step("Check that tests have been completed"):
            assert len(db.saved_results) > 0
        inserted_test_ids = set()
        inserted_test_headlines = set()
        with allure.step("Postcondition: add results to the database"):
            for result_tuple in db.saved_results:
                with allure.step("Parsing result"):
                    start_time = result_tuple[0]
                    report = result_tuple[1]
                    if report.head_line == "TestFunctional.test_add_new_entry" or \
                            report.head_line == "TestFunctional.test_processing_of_test_data" or \
                            report.head_line in inserted_test_headlines:
                        continue
                    s_time = DatetimeUtil.convert_timestamp_to_sql_datetime(start_time)
                    e_time = DatetimeUtil.convert_timestamp_to_sql_datetime(start_time + report.duration)
                with allure.step("Inserting test result into test table"):
                    db.insert_project('L2-p.khachidze')
                    db.insert_author(name='p.khachidze', login='p.khachidze', email='p.khachidze@qa-academy.by')
                    db.insert_session()
                    status_id = 1
                    if report.failed:
                        status_id = 2
                    elif report.skipped:
                        status_id = 3
                    db.insert_test(result={'name': f"'Running {report.head_line}'",
                                           'status_id': status_id,
                                           'method_name': f"'{'/'.join((report.location[0], report.head_line))}'",
                                           'project_id': db.project_id,
                                           'session_id': db.session_id,
                                           'start_time': f"'{s_time}'",
                                           'end_time': f"'{e_time}'",
                                           'env': f"'{platform.node()}|{platform.machine()}|{platform.system()}'",
                                           'browser': f"'{BrowserConfig.BROWSER}'",
                                           'author_id': db.author_id})
                    inserted_test_ids.add(db.test_id)
                    inserted_test_headlines.add(report.head_line)
                with allure.step("Inserting log into log table"):
                    db.insert_log(log=report.caplog, is_exc=1 if status_id == 2 else 0)
        with allure.step("Check that results are added"):
            for ID in inserted_test_ids:
                assert db.select_test_by_id(id_=ID), "Information was not added"
