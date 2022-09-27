from random import randint


class RandomUtil:
    @staticmethod
    def get_password():
        return 'Dummystr1ng'

    @staticmethod
    def get_string():
        return 'dummystring'

    @staticmethod
    def random_choice(iterable):
        return iterable[randint(0, len(iterable))]
