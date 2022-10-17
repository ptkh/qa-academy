import allure
from framework.utils.logger import Logger
from tests.database.config import Config
from framework.database.database import DB
import mysql.connector as my_sql

from tests.testData.test_data import TestData


class MySQL(DB):
    tbl_test_columns = "name, status_id, method_name, project_id, " \
                       "session_id, start_time, end_time, env, browser, author_id"
    session_columns = 'session_key, created_time, build_number'
    log_columns = 'content, is_exception, test_id'

    def __init__(self):
        super().__init__(my_sql.connect(**Config.dbinfo()))
        self.create_db(TestData.db_name)
        self.restore_db(TestData.dump_db_fp)
        self.project_id = None
        self.session_id = None
        self.author_id = None
        self.test_id = None

    def insert_test(self, result: dict):
        with allure.step("Inserting test into test table"):
            temp = []
            for name in self.tbl_test_columns.split(', '):
                temp.append(f"{result[name]}")
            values = ', '.join(temp)
            self.test_id = self.insert_item(table='test', columns=self.tbl_test_columns, values=values)

    def insert_log(self, log, is_exc):
        with allure.step("Inserting log into log table"):
            values = f"{log}, {is_exc}, {self.test_id}"
            self.insert_item(table='log', columns=self.log_columns, values=values)

    def insert_project(self, project_name):
        with allure.step("Inserting project into project table"):
            self.project_id = self.insert_item(table='project', columns='name', values=project_name)

    def insert_author(self, author):
        with allure.step("Inserting author into author table"):
            self.author_id = self.insert_item(table='author', columns='name', values=author)

    def insert_session(self, session):
        with allure.step("Inserting session into session table"):
            # NOT SURE
            session_key = 'NULL'
            created_time = 'NULL'
            build_number = 'NULL'
            values = f"{session_key}, {created_time}, {build_number}"
            self.session_id = self.insert_item(table='session', columns=self.session_columns, values=values)

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
                self.delete_item(table='test', column='id', value=str(test[0]))


if __name__ == '__main__':
    db = MySQL()
