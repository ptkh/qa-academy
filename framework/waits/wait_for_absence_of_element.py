class WaitForAbsenceOfElementLocated(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        return not self.element.is_exist()
