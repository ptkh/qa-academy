# -*- coding: utf-8 -*-
import json
import os


class Config(object):
    """
    Use:
        mysql.connector.Connect(**Config.dbinfo())
    """

    @classmethod
    def dbinfo(cls):
        """config.json contents
        {
          "host": "localhost",
          "port": 3306,
          "database": {database},
          "user": {user},
          "password": {password},
          "charset": "utf-8",
          "unicode": true,
          "warnings": true
        }"""
        with open(os.path.join(os.path.dirname(__file__), 'config.json')) as conf:
            return json.load(conf)
