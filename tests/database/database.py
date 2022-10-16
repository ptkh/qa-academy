from tests.database.config import Config
from framework.database.database import DB
import mysql.connector as my_sql


class MySQL(DB):
    tbl_test_columns = "name, status_id, method_name, project_id, " \
                       "session_id, start_time, end_time, env, browser, author_id"

    def __init__(self):
        with my_sql.connect(**Config.dbinfo()) as conn:
            super().__init__(conn)
        self.project_id = None
        self.session_id = None
        self.author_id = None

    def insert_test(self, result: dict):
        temp = []
        for name in self.tbl_test_columns.split(', '):
            temp.append(f"{result[name]}")
        values = ', '.join(temp)
        self.insert_item(table='test', columns=self.tbl_test_columns, values=values)

    def insert_project(self, project_name):
        self.project_id = self.insert_item(table='project', columns='name', values=project_name)

    def insert_author(self, author):
        self.author_id = self.insert_item(table='author', columns='name', values=author)

    def insert_session(self, session):
        columns = 'session_key, created_time, build_number'
        # NOT SURE
        session_key = 'NULL'
        created_time = 'NULL'
        build_number = 'NULL'
        values = f"{session_key}, {created_time}, {build_number}"
        self.session_id = self.insert_item(table='session', columns=columns, values=values)

    def fetch_tests_with_repeating_id(self):
        temp = []
        for i in range(10):
            temp.append(f"id LIKE '%{str(i)*2}%'")
        condition = ' OR '.join(temp)
        return self.fetch_many_items(10, table='test', condition=condition)
