# coding=utf-8
from framework.elements.base.base_element import BaseElement
from selenium.webdriver.common.keys import Keys

from framework.utils.logger import Logger


class TextBox(BaseElement):
    def __init__(self, search_condition, locator, name):
        super(TextBox, self).__init__(search_condition_of=search_condition, loc=locator, name_of=name)

    def __getitem__(self, key):
        new_element = super(TextBox, self).__getitem__(key=key)
        return TextBox(new_element.get_search_condition(), new_element.get_locator(), new_element.get_name())

    def __call__(self, sublocator, new_name_of=None):
        new_element = super(TextBox, self).__call__(sublocator=sublocator, new_name_of=new_name_of)
        return TextBox(new_element.get_search_condition(), new_element.get_locator(), new_element.get_name())

    def get_element_type(self):
        return "TextBox"

    def get_value(self):
        self.wait_for_is_present()
        value = super(TextBox, self).get_attribute("value")
        Logger.info("Метод get_value в элементе " + self.get_name() + " " + self.get_element_type() +
                    " получил значение: " + str(value))
        return value

    def clear_field(self):
        Logger.info("Удание текста в элементе " + self.get_name() + self.get_element_type() + "'" +
                    self.get_name() + "'")
        self.send_keys(Keys.CONTROL + 'a')
        self.send_keys_without_click(Keys.DELETE)

    def selenium_clear(self):
        self.click()
        Logger.info("Очистка элемента " + self.get_name() + self.get_element_type() + "'" + self.get_name() + "'")
        self.find_element().clear()
