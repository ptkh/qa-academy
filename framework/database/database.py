import mysql
from mysql.connector import MySQLConnection
from framework.utils.logger import Logger


class DB:
    def __init__(self, database: MySQLConnection):
        self.database = database
        self.cursor = database.cursor()

    def insert_item(self, table: str, columns: str, values: str):
        query = "INSERT INTO %s (%s) VALUES %s;", (table, columns, values)
        Logger.info("Executing query: %s" % query)
        self.cursor.execute(query)
        self.cursor.execute("SELECT LAST_INSERT_ID() FROM %s;", table)
        return self.cursor.fetchone()

    def fetch_item(self, table: str, column: str, value: str):
        query = "SELECT * FROM %s WHERE %s=%s;", (table, column, f"'{value}'")
        Logger.info("Executing query: %s" % query)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetch_many_items(self, num: int, table: str, condition: str):
        query = "SELECT * FROM %s WHERE %s;", (table, condition)
        Logger.info("Executing query: %s" % query)
        self.cursor.execute(query)
        return self.cursor.fetchmany(size=num)

    def delete_item(self, table: str, column: str, value: str):
        query = "DELETE FROM %s WHERE %s=%s;", (table, column, f"'{value}'")
        Logger.info("Executing query: %s" % query)
        self.cursor.execute(query)

    def create_db(self, db_name):
        try:
            Logger.info("Creating database %s" % db_name)
            self.cursor.execute("CREATE DATABASE %s;" % db_name)
        except mysql.connector.errors.DatabaseError as e:
            if 'database exists' in str(e):
                Logger.info("Database %s already exists" % db_name)
            else:
                raise
        finally:
            Logger.info("Using database %s" % db_name)
            self.cursor.execute("USE %s;" % db_name)

    def restore_db(self, filepath):
        self.cursor.execute("SHOW TABLES;")
        tables = self.cursor.fetchall()
        if not len(tables):
            Logger.info("Tables already exist in database. Skipping database restoration step.")
            return

        Logger.info("Restoring database from filepath: %s" % filepath)
        with open(filepath, 'r') as f:
            Logger.info("Reading contents of sql file")
            sql_file = f.read()
        Logger.info("Splitting contents of sql file (delimiter ';') into commands")
        sql_commands = sql_file.split(';')
        for command in sql_commands:
            try:
                if command.strip() != '':
                    Logger.info("Executing sql command from dump file. command: %s" % command)
                    self.cursor.execute(command)
            except IOError as e:
                Logger.info("Command skipped due to error: %s" % e)
        self.database.commit()
