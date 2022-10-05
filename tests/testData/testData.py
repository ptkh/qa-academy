import os


class TestData:
    PASSWORD_LENGTH = 11
    EMAIL_LENGTH = 7
    COMMON_LETTER_IN_PWD_EMAIL = 'a'
    IMAGE_FILEPATH = os.path.join(os.path.dirname(__file__), "../avatar.png")
    INTERESTS_NUM = 3
    TIMER_VALUE = "00:00:00"
