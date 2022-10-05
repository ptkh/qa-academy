import random
import string


class RandomUtil:
    @staticmethod
    def get_string(str_len):
        letters = string.ascii_letters
        return ''.join([random.choice(letters) for _ in range(str_len)])