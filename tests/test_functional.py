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
        with allure.step("Precondition: Select and copy tests from database"):
            selected_tests = db.get_tests_with_repeating_id(size=TestData.num_tests)
        with allure.step("Simulate the launch of the tests and insert into database"):
            db.insert_session(TestData.session_key)
            db.insert_author(name=TestData.author_name,
                             login=TestData.author_login,
                             email=TestData.author_email)
            updated_tests = db.update_tests(selected_tests=selected_tests,
                                            author_id=db.get_author_id_by_name(name=TestData.author_name),
                                            session_id=db.get_session_id_by_key(session_key=TestData.session_key))
            inserted_ids = db.add_results_to_database_get_ids(
                results=updated_tests,
                author_id=db.get_author_id_by_name(name=TestData.author_name),
                project_id=db.get_project_id_by_project_name(project_name=TestData.project_name),
                session_id=db.get_session_id_by_key(TestData.session_key))
        with allure.step("Check that tests are completed and information is updated"):
            for ID in inserted_ids:
                assert db.get_test_by_id(id_=ID), "Information was not updated"
        with allure.step("Postcondition: Delete previously selected tests from database"):
            db.delete_tests(selected_tests)
        with allure.step("Check that records have been deleted"):
            for test in selected_tests:
                assert not db.get_test_by_id(id_=test[0]), "Record was not deleted"

    @pytest.mark.run(order=6)
    def test_add_new_entry(self, db):
        with allure.step("Check that tests have been completed"):
            assert len(db.saved_results) > 0, "Tests didn't complete"
        with allure.step("Postcondition: add results to the database"):
            db.insert_session(session_key=TestData.session_key)
            db.insert_project(project_name=TestData.project_name)
            db.insert_author(name=TestData.author_name,
                             login=TestData.author_login,
                             email=TestData.author_email)
            inserted_ids = db.add_results_to_database_get_ids(
                results=db.saved_results,
                author_id=db.get_author_id_by_name(name=TestData.author_name),
                project_id=db.get_project_id_by_project_name(project_name=TestData.project_name),
                session_id=db.get_session_id_by_key(TestData.session_key),
                exclude=('TestFunctional.test_add_new_entry',
                         'TestFunctional.test_processing_of_test_data'))
        with allure.step("Check that information was added"):
            for ID in inserted_ids:
                assert db.get_test_by_id(id_=ID), "Information was not added"
