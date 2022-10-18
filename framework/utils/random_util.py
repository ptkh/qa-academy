import random
import string


class RandomUtil:
    @staticmethod
    def get_string(str_len):
        letters = string.ascii_letters
        return ''.join([random.choice(letters) for _ in range(str_len)])

    @staticmethod
    def random_choice(iterable):
        return random.choice(iterable)

    @staticmethod
    def get_password(pwd_len):
        symbols = string.ascii_letters + string.digits
        return ''.join([random.choice(symbols) for _ in range(pwd_len)]) + str(random.randint(0, 10))

    @staticmethod
    def get_integer_key(key_len):
        symbols = string.digits
        return ''.join([random.choice(symbols) for _ in range(key_len)])

    @staticmethod
    def get_randint(a, b):
        return random.randint(a, b)
