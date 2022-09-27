class WaitForCustomEvent(object):
    def __init__(self, event, expected_result, *args):
        self.event = event
        self.expected_result = expected_result
        self.args = args

    def __call__(self, driver):
        return self.event(*self.args) == self.expected_result
