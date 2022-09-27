class WaitPresentWithCustomAction(object):
    def __init__(self, element, action, *args):
        self.element = element
        self.action = action
        self.args = args

    def __call__(self, driver):
        self.action(*self.args)
        return self.element.is_exist()
