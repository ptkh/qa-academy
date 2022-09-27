# coding=utf-8


class WaitForTrueWithAction(object):
    def __init__(self, browser, expression, action, expression_args=None, action_args=None):
        self.browser = browser
        self.action = action
        self.expression = expression
        self.expression_args = expression_args
        self.action_args = action_args

    def __call__(self, driver):
        try:
            if self.action_args is None:
                self.action()
            else:
                self.action(*self.action_args)
            if self.expression_args is None:
                return self.expression()
            else:
                return self.expression(*self.expression_args)
        except Exception:
            return False
