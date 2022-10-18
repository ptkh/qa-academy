from mysql.connector import MySQLConnection
from framework.utils.logger import Logger


class DB:
    def __init__(self, database: MySQLConnection):
        self.database = database
        self.cursor = database.cursor(buffered=True)
        self.cursor.execute("SET autocommit=1")

    def insert_item(self, table, column, value):
        query = f"INSERT IGNORE INTO {table} ({column}) VALUES ({value});"
        Logger.info("Executing query: %s" % query)
        self.cursor.execute(query)

    def fetch_item(self, table, column, value):
        query = f"SELECT * FROM {table} WHERE {column}={value};"
        Logger.info("Executing query: %s" % query)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetch_many_items(self, num: int, table: str, condition: str):
        query = f"SELECT * FROM {table} WHERE {condition};"
        Logger.info("Executing query: %s" % query)
        self.cursor.execute(query)
        return self.cursor.fetchmany(num)

    def delete_item(self, table: str, column: str, value: str):
        query = f"DELETE FROM {table} WHERE {column}={value};"
        Logger.info("Executing query: %s" % query)
        self.cursor.execute(query)
