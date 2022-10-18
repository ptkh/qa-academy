import time
import allure
from framework.utils.datetime_util import DatetimeUtil
from framework.utils.logger import Logger
from framework.utils.random_util import RandomUtil
from tests.database.config import Config
from framework.database.database import DB
import mysql.connector as my_sql


class MySQL(DB):
    test_columns = "name, status_id, method_name, project_id, session_id, start_time, end_time, env, browser, author_id"
    session_columns = 'session_key, created_time, build_number'
    log_columns = 'content, is_exception, test_id'
    project_columns = 'name'
    author_columns = 'name, login, email'

    def __init__(self):
        super().__init__(my_sql.connect(**Config.dbinfo()))
        self.project_id = None
        self.session_id = None
        self.author_id = None
        self.test_id = None

    def insert_test(self, result: dict):
        with allure.step("Inserting test into test table"):
            temp = []
            for name in self.test_columns.split(', '):
                temp.append(f"{result[name]}")
            values = ', '.join(temp)
            self.test_id = self.insert_item(table='test', column=self.test_columns, value=values)[0]

    def insert_log(self, log, is_exc):
        with allure.step("Inserting log into log table"):
            log_string = str(log).replace('"', "'")
            values = f'"{log_string}", {is_exc}, {self.test_id}'
            self.insert_item(table='log', column=self.log_columns, value=values)

    def insert_project(self, project_name):
        with allure.step("Inserting project into project table"):
            value = f"'{project_name}'"
            self.insert_item(table='project', column=self.project_columns, value=value)
            self.project_id = self.fetch_item(table='project', column='name', value=value)[0]

    def insert_author(self, name, login, email):
        with allure.step("Inserting author into author table"):
            value = f"'{name}', '{login}', '{email}'"
            self.author_id = self.insert_item(table='author', column=self.author_columns, value=value)[0]

    def insert_session(self):
        with allure.step("Inserting session into session table"):
            session_key = RandomUtil.get_integer_key(13)
            created_time = DatetimeUtil.convert_timestamp_to_sql_datetime(time.time())
            build_number = RandomUtil.get_randint(0, 50)
            value = f"'{session_key}', '{created_time}', {build_number}"
            self.session_id = self.insert_item(table='session', column=self.session_columns, value=value)[0]

    def fetch_tests_with_repeating_id(self):
        with allure.step("Selecting results with repeating digits in id"):
            temp = []
            for i in range(10):
                temp.append(f"id LIKE '%{str(i)*2}%'")
            condition = ' OR '.join(temp)
            return self.fetch_many_items(10, table='test', condition=condition)

    def delete_tests(self, tests: list):
        with allure.step("Deleting given tests from the database"):
            for test in tests:
                Logger.info("Deleting test with id %d" % test[0])
                self.delete_item(table='test', column='id', value=test[0])

    def close(self):
        self.database.close()


if __name__ == '__main__':
    db = MySQL()
