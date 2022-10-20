import platform
import time
import allure
from framework.utils.datetime_util import DatetimeUtil
from framework.utils.logger import Logger
from framework.utils.random_util import RandomUtil
from tests.config.browser import BrowserConfig
from framework.database.database import DB
from tests.testData.test_data import TestData


class UnionReportingDB(DB):
    saved_results = []
    inserted_test_ids = []

    def add_results_to_database_get_ids(self, results):
        with allure.step("Adding results to the database"):
            inserted_test_ids = set()
            for result in results:
                test = result['test']
                log = result['log']
                with allure.step("Inserting test result into test table"):
                    self.insert_test(test=test)
                    test_id = self.get_test_id_by_start_time(test['start_time'])
                with allure.step("Inserting logs into log table"):
                    if log:
                        self.insert_log(log=log['log'], is_exc=log['is_exc'], test_id=test_id)
                inserted_test_ids.add(test_id)
            return inserted_test_ids

    @staticmethod
    def parse_tests(report_list, author_id, project_id, session_id, exclude=()):
        with allure.step("Parsing test reports"):
            parsed_test_headlines = set()
            parsed_results = []
            for report_tuple in report_list:
                with allure.step("Parsing result"):
                    time_start = report_tuple[0]
                    report = report_tuple[1]
                    if report.head_line in exclude or report.head_line in parsed_test_headlines:
                        continue
                    start_time = DatetimeUtil.convert_timestamp_to_sql_datetime(time_start)
                    end_time = DatetimeUtil.convert_timestamp_to_sql_datetime(time_start + report.duration)
                    status_id = 1
                    if report.failed:
                        status_id = 2
                    elif report.skipped:
                        status_id = 3
                    parsed_test = {'name': f"'Running {report.head_line}'",
                                   'status_id': status_id,
                                   'method_name': f"'{'/'.join((report.location[0], report.head_line))}'",
                                   'project_id': project_id,
                                   'session_id': session_id,
                                   'start_time': f"'{start_time}'",
                                   'end_time': f"'{end_time}'",
                                   'env': f"'{platform.node()}|{platform.machine()}|{platform.system()}'",
                                   'browser': f"'{BrowserConfig.BROWSER}'",
                                   'author_id': author_id}
                    parsed_log = {'log': report.caplog,
                                  'is_exc': 1 if status_id == 2 else 0}
                    parsed_results.append({
                        'test': parsed_test,
                        'log': parsed_log
                    })
                    parsed_test_headlines.add(report.head_line)
            return parsed_results

    @staticmethod
    def update_tests(selected_tests, author_id, session_id):
        with allure.step("Simulate the launch of the tests and insert into database"):
            updated_tests = []
            for test in selected_tests:
                s_time = DatetimeUtil.convert_timestamp_to_sql_datetime(time.time())
                e_time = DatetimeUtil.convert_timestamp_to_sql_datetime(time.time() + RandomUtil.get_randint(0, 20))
                updated_test = ({'name': f'"{test[1]}"',
                                 'status_id': RandomUtil.get_randint(1, 4),
                                 'method_name': f'"{test[3]}"',
                                 'project_id': test[4],
                                 'session_id': session_id,
                                 'start_time': f"'{s_time}'",
                                 'end_time': f"'{e_time}'",
                                 'env': f"'{platform.node()}|{platform.machine()}|{platform.system()}'",
                                 'browser': f"'{BrowserConfig.BROWSER}'",
                                 'author_id': author_id})
                updated_tests.append({
                    'test': updated_test,
                    'log': None
                })
            return updated_tests

    def get_author_id_by_name(self, name):
        Logger.info("Fetching id of author name by name")
        return self.fetch_item(table='author', column='name', value=f'"{name}"')[0]

    def get_test_id_by_start_time(self, start_time):
        Logger.info("Fetching id of test by start time")
        return self.fetch_item(table='test', column='start_time', value=start_time)[0]

    def get_project_id_by_project_name(self, project_name):
        return self.fetch_item(table='project', column='name', value=f"'{project_name}'")[0]

    def get_session_id_by_key(self, session_key):
        with allure.step("Fetching session id by key"):
            return self.fetch_item(table='session', column='session_key', value=f'{session_key}')[0]

    def get_test_by_id(self, id_):
        result = self.fetch_item(table='test', column='id', value=id_)
        if result is None:
            Logger.info("Test with id %d not found" % id_)
            return False
        return result

    def get_tests_with_repeating_id(self, size):
        with allure.step("Selecting results with repeating digits in id"):
            temp = []
            for i in range(10):
                temp.append(f"id LIKE '%{str(i)*2}%'")
            condition = ' OR '.join(temp)
            return self.fetch_many_items(size, table='test', condition=condition)

    def insert_test(self, test: dict):
        with allure.step("Inserting test into test table"):
            temp = []
            for name in TestData.test_columns.split(', '):
                temp.append(f"{test[name]}")
            values = ', '.join(temp)
            self.insert_item(table='test', column=TestData.test_columns, value=values)

    def insert_log(self, log, is_exc, test_id):
        with allure.step("Inserting log into log table"):
            log_string = str(log).replace('"', "'")
            values = f'"{log_string}", {is_exc}, {test_id}'
            self.insert_item(table='log', column=TestData.log_columns, value=values)

    def insert_project(self, project_name):
        with allure.step("Inserting project into project table"):
            value = f"'{project_name}'"
            self.insert_item(table='project', column=TestData.project_columns, value=value)
            Logger.info('Selecting recently added project id')

    def insert_author(self, name, login, email):
        with allure.step("Inserting author into author table"):
            value = f"'{name}', '{login}', '{email}'"
            self.insert_item(table='author', column=TestData.author_columns, value=value)

    def insert_session(self, session_key):
        with allure.step("Inserting session into session table"):
            created_time = DatetimeUtil.convert_timestamp_to_sql_datetime(time.time())
            build_number = RandomUtil.get_randint(0, 50)
            value = f"'{session_key}', '{created_time}', {build_number}"
            self.insert_item(table='session', column=TestData.session_columns, value=value)

    def delete_tests(self, tests: list):
        with allure.step("Deleting given tests from the database"):
            for test in tests:
                Logger.info("Deleting test with id %d" % test[0])
                self.delete_item(table='test', column='id', value=test[0])

