import os
from framework.utils.random_util import RandomUtil


class TestData:
    session_key = RandomUtil.get_integer_key(13)
    num_tests = 10
    project_name = 'L2-p.khachidze'
    author_name = 'p.khachidze'
    author_login = 'p.khachidze'
    author_email = 'p.khachidze@qa-academy.by'
    test_columns = "name, status_id, method_name, project_id, session_id, start_time, end_time, env, browser, author_id"
    session_columns = 'session_key, created_time, build_number'
    log_columns = 'content, is_exception, test_id'
    project_columns = 'name'
    author_columns = 'name, login, email'
    PASSWORD_LENGTH = 11
    EMAIL_LENGTH = 7
    COMMON_LETTER_IN_PWD_EMAIL = 'a'
    IMAGE_FILEPATH = os.path.join(os.path.dirname(__file__), "avatar.png")
    INTERESTS_NUM = 3
    TIMER_VALUE = "00:00:00"
