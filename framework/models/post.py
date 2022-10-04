class Post:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __eq__(self, other):
        for k, v in self.__dict__.items():
            if k == 'id':
                continue
            if v != other.__dict__[k]:
                return False
        return True
