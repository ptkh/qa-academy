from mysql.connector import MySQLConnection


class DB:
    def __init__(self, database: MySQLConnection):
        self.database = database
        self.cursor = database.cursor()

    def insert_item(self, table: str, columns: str, values: str):
        query = "INSERT INTO %s (%s) VALUES %s;\nSELECT LAST_INSERT_ID();", (table, columns, values)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetch_item(self, table: str, column: str, value: str):
        query = "SELECT * FROM %s WHERE %s=%s;", (table, column, f"'{value}'")
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetch_many_items(self, num: int, table: str, condition: str):
        query = "SELECT * FROM %s WHERE %s;", (table, condition)
        self.cursor.execute(query)
        return self.cursor.fetchmany(size=num)

    def delete_items(self, table: str, column: str, value: str):
        query = "DELETE FROM %s WHERE %s=%s;", (table, column, f"'{value}'")
        self.cursor.execute(query)