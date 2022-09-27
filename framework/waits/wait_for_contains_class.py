class WaitForContainsClass(object):
    def __init__(self, element, attribute_value, is_contains=True):
        self.element = element
        self.attribute_value = attribute_value
        self.is_contains = is_contains

    def __call__(self, driver):
        return self.is_contains == (self.attribute_value in self.element.get_attribute_class())
