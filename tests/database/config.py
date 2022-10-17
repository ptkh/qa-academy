# -*- coding: utf-8 -*-
from tests.testData.test_data import TestData


class Config(object):
    """
    Use:
        mysql.connector.Connect(**Config.dbinfo())
    """

    HOST = 'localhost'
    DATABASE = TestData.db_name
    USER = TestData.db_user
    PASSWORD = TestData.db_password
    PORT = 3306

    CHARSET = 'utf8'
    UNICODE = True
    WARNINGS = True

    @classmethod
    def dbinfo(cls):
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'database': cls.DATABASE,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'charset': cls.CHARSET,
            'use_unicode': cls.UNICODE,
            'get_warnings': cls.WARNINGS,
        }
