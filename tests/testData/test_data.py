import os


class TestData:
    db_name = 'database_task'
    db_user = 'a1qa'
    db_password = 'password'
    dump_db_fp = os.path.realpath('dump.sql')

    PASSWORD_LENGTH = 11
    EMAIL_LENGTH = 7
    COMMON_LETTER_IN_PWD_EMAIL = 'a'
    IMAGE_FILEPATH = os.path.abspath("avatar.png")
    INTERESTS_NUM = 3
    TIMER_VALUE = "00:00:00"
