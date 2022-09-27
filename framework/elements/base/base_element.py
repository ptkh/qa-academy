# coding=utf-8
from collections import OrderedDict

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from scripts import scripts_js
from utils.logger import Logger
from browser.browser import Browser
from selenium.webdriver.common.by import By
from waits.wait_for_absence_of_element import WaitForAbsenceOfElementLocated
from waits.wait_present_with_custom_action import WaitPresentWithCustomAction
from waits.wait_for_contains_class import WaitForContainsClass
from selenium.webdriver.common.action_chains import ActionChains
from tests.config.waits import Waits


class BaseElement(object):
    coordinate_x = 'x'
    coordinate_y = 'y'

    # @abstractmethod
    def __init__(self, search_condition_of, loc, name_of):
        self.__search_condition = search_condition_of
        self.__locator = loc
        self.__name = name_of

    def __getitem__(self, key):
        if self.__search_condition != By.XPATH:
            raise TypeError("__getitem__ for BaseElement possible only when __search_condition == By.XPATH")
        else:
            return type(self)(By.XPATH, self.__locator + "[" + str(key) + "]", self.__name)
            # return type(self)(By.XPATH, "(" + self.__locator + ")" + "[" + str(key) + "]", self.__name)

    def __call__(self, sublocator, new_name_of=None):
        if new_name_of is not None:
            return type(self)(By.XPATH, self.__locator + sublocator, new_name_of)
        else:
            return type(self)(By.XPATH, self.__locator + sublocator, self.__name)

    # @abstractmethod
    def get_element_type(self):
        pass

    def get_locator(self):
        return self.__locator

    def get_search_condition(self):
        return self.__search_condition

    def get_name(self):
        return self.__name

    def find_element(self):
        waiter = ec.presence_of_element_located((self.get_search_condition(), self.get_locator()))
        element = self.wait_for_check_by_condition(method_to_check=waiter, message=" не был найден")
        return element

    @staticmethod
    def get_displayed_elements(condition, locator):
        element_size = len(Browser.get_browser().get_driver().find_elements(condition, locator))
        result_elements = []
        try:
            for ele_number in range(1, element_size + 1):
                element_locator = "({locator})[{number}]".format(locator=locator, number=ele_number)
                Logger.info("Поиск элемента с локатором " + element_locator)
                element = WebDriverWait(Browser.get_browser().get_driver(), Waits.EXPLICITLY_WAIT_SEC).until(
                    ec.visibility_of_element_located((condition, element_locator)))
                result_elements.append(element)
        except TimeoutException:
            error_msg = "элемент с локатором не был найден"
            Logger.error(error_msg)
            raise TimeoutException(error_msg)
        return result_elements

    def get_elements(self):
        return Browser.get_browser().get_driver().find_elements(self.__search_condition, self.__locator)

    def is_enabled(self):
        return self.find_element().is_enabled()

    def is_disabled(self):
        return self.find_element().is_disabled()

    def is_selected(self):
        return self.find_element().is_selected()

    def is_displayed(self):
        try:
            if not self.is_exist():
                return False
            return self.find_element().is_displayed()
        except TimeoutException:
            return False

    def is_exist(self):
        return self.get_elements_count() > 0

    def get_elements_count(self):
        elements_count = len(Browser.get_browser().get_driver().find_elements(self.__search_condition, self.__locator))
        return elements_count

    def send_keys(self, key):
        self.click()
        self.send_keys_without_click(key)

    def send_keys_without_click(self, key):
        Logger.info("send_keys: Изменение текста для элемента '" + self.get_name() + " " + self.__class__.__name__ +
                    "'" + "' на текст => '" + key + "'")
        self.wait_for_is_visible()
        element = self.wait_for_clickable()
        element.send_keys(key)

    # def click(self):
    #     RobotLogger.info("click: Щелчок по элемету '" + self.get_name() + "'")
    #     element = self.wait_for_clickable()
    #     element.click()

    def click(self):
        Logger.info("click: Щелчок по элемету '" + self.get_name() + " " + self.__class__.__name__ + "'")

        def func():
            self.find_element().click()
            return True

        self.wait_for(func)

    def wait_for(self, condition, *args, **kwargs):
        def func(driver):
            try:
                value = condition(*args, **kwargs)
                return value
            except StaleElementReferenceException:
                return False

        return WebDriverWait(Browser.get_browser().get_driver(), Waits.EXPLICITLY_WAIT_SEC,
                             ignored_exceptions=[StaleElementReferenceException]).until(func)

    def js_click(self):
        element = self.wait_for_clickable()
        Browser.get_browser().get_driver().execute_script("arguments[0].click();", element)

    def actions_click(self):
        actions = ActionChains(Browser.get_browser().get_driver())
        actions.click(on_element=self.find_element())
        actions.perform()

    def actions_click_with_key(self, key):
        actions = ActionChains(Browser.get_browser().get_driver())
        actions.key_down(value=key).click(self.find_element()).key_up(value=key).perform()

    def key_down(self, key):
        actions = ActionChains(Browser.get_browser().get_driver())
        actions.key_down(value=key, element=self.find_element())
        actions.perform()

    def key_up(self, key):
        actions = ActionChains(Browser.get_browser().get_driver())
        actions.key_up(value=key, element=self.find_element())
        actions.perform()

    def actions_send_keys(self, keys):
        actions = ActionChains(Browser.get_browser().get_driver())
        actions.move_to_element(self.find_element()).send_keys(keys)
        actions.perform()

    def send_keys_to_element(self, keys):
        actions = ActionChains(Browser.get_browser().get_driver())
        actions.send_keys_to_element(self.find_element(), keys)
        actions.perform()

    def get_text(self):
        Logger.info("get_text: Получение текста для элемента '" + self.get_name() + "'")
        self.wait_for_is_present()
        text = self.find_element().text
        Logger.info("get_text: Получен текст '" + text + "'")
        return text

    def get_text_content(self):
        self.wait_for_is_visible()
        return Browser.get_browser().get_driver().\
            execute_script("return arguments[0].textContent;", self.find_element())

    def get_attribute(self, attr):
        Logger.info("get_attribute: Получение атрибута " + attr + " для элемента '" + self.get_name() + "'")
        self.wait_for_is_visible()
        return self.find_element().get_attribute(name=attr)

    def get_css_value(self, property_name):
        Logger.info("get_attribute: Получение атрибута CSS" + property_name + " для элемента '" + self.get_name() + "'")
        self.wait_for_is_visible()
        return self.find_element().value_of_css_property(property_name=property_name)

    def get_attribute_class(self):
        return self.get_attribute("class")

    def scroll_by_script(self):
        self.wait_for_is_visible()
        Logger.info("Скролл к элементу '" + self.get_name() + "'")
        Browser.get_browser().execute_script(scripts_js.SCROLL_INTO_VIEW, self.find_element())

    def double_click(self):
        self.wait_for_is_visible()
        Logger.info("double_click: Двойной щелчок по элементу '" + self.get_name() + "'")
        ActionChains(Browser.get_browser().get_driver()).double_click(self.find_element()).perform()

    def wait_for_clickable(self):
        waiter = ec.element_to_be_clickable((self.get_search_condition(), self.get_locator()))
        return self.wait_for_check_by_condition(method_to_check=waiter, message=" не доступен для щелчка")

    def wait_for_is_visible(self):
        self.wait_for_is_present()
        waiter = ec.visibility_of_element_located((self.get_search_condition(), self.get_locator()))
        self.wait_for_check_by_condition(method_to_check=waiter, message=" не видим")

    def wait_for_is_present(self):
        waiter = ec.presence_of_element_located((self.get_search_condition(), self.get_locator()))
        self.wait_for_check_by_condition(method_to_check=waiter, message=" не существует")

    def wait_for_is_present_with_action(self, action, *args):
        waiter = WaitPresentWithCustomAction(self, action, *args)
        self.wait_for_check_by_condition(method_to_check=waiter, message="не существует")

    def wait_for_is_displayed(self):
        Browser.get_browser().wait_for_true(self.is_displayed)

    def wait_for_is_absent(self, msg=" существует"):
        waiter = WaitForAbsenceOfElementLocated(self)
        self.wait_for_check_by_condition(method_to_check=waiter, message=msg)

    def wait_for_element_disappear(self):
        waiter = ec.staleness_of(self.find_element())
        self.wait_for_check_by_condition(method_to_check=waiter,
                                         message=" не пропал")

    def wait_for_text(self, text, wait_time_sec=Waits.EXPLICITLY_WAIT_SEC):
        waiter = ec.text_to_be_present_in_element((self.get_search_condition(), self.get_locator()), text)
        self.wait_for_check_by_condition(method_to_check=waiter,
                                         message=" не содержит " + text, wait_time_sec=wait_time_sec)

    def wait_for_visibility(self):
        waiter = ec.visibility_of(self.find_element())
        self.wait_for_check_by_condition(method_to_check=waiter, message=" не стал видимым")

    def wait_for_invisibility(self):
        waiter = ec.invisibility_of_element_located((self.get_search_condition(), self.get_locator()))
        self.wait_for_check_by_condition(method_to_check=waiter, message=" остался видимым")

    def wait_for_class_contains(self, class_value, is_contains=True):
        waiter = WaitForContainsClass(self, class_value, is_contains)
        if is_contains:
            msg = "класс не содержит "
        else:
            msg = "класс содержит "
        self.wait_for_check_by_condition(method_to_check=waiter, message=msg + class_value)

    def wait_for_check_by_condition(self, method_to_check, message,
                                    wait_time_sec=Waits.EXPLICITLY_WAIT_SEC, use_default_msg=True):
        try:
            element = WebDriverWait(Browser.get_browser().get_driver(), wait_time_sec).until(method=method_to_check)
        except TimeoutException:
            result_message = ("элемент '" + self.get_name() + "' с локатором " + self.get_locator() + message
                              if use_default_msg else message)
            Logger.warning(result_message)
            raise TimeoutException(result_message)
        return element

    def get_n_element_from_top(self, number_from_top):
        elements_count = self.get_elements_count()
        elements = []
        for i in range(1, elements_count + 1):
            elements.append(self[i])
        y_pos_element_dict = {}
        for element in elements:
            y_pos_element_dict[element.find_element().location[BaseElement.coordinate_y]] = element
        sorted_keys = sorted(y_pos_element_dict.keys())
        element = y_pos_element_dict[sorted_keys[int(number_from_top) - 1]]
        return element

    def get_lowest_element(self):
        elements_count = self.get_elements_count()
        elements = []
        for i in range(1, elements_count + 1):
            elements.append(self[i])
        y_pos_element_dict = {}
        for element in elements:
            y_pos_element_dict[element.find_element().location[BaseElement.coordinate_y]] = element
        sorted_keys = sorted(y_pos_element_dict.keys())
        element = y_pos_element_dict[sorted_keys[len(y_pos_element_dict) - 1]]
        return element

    def get_n_element_from_top_index(self, number_from_top):
        element = self.get_n_element_from_top(number_from_top)
        return element.__locator.rpartition('[')[2].replace(']', '')

    def get_element_number_from_top(self, element_index=1):
        elements = self.get_elements()
        number_from_top_and_index_list = {}
        for i in range(0, len(elements)):
            number_from_top_and_index_list[i] = elements[i].location[BaseElement.coordinate_y]
        indices_dict = OrderedDict(sorted(number_from_top_and_index_list.items(), key=lambda t: t[1]))
        return list(indices_dict.keys()).index(element_index)

    def get_location(self):
        return self.find_element().location

    def get_location_vertical(self):
        return self.find_element().location[BaseElement.coordinate_y]

    def get_location_horizontal(self):
        return self.find_element().location[BaseElement.coordinate_x]

    @staticmethod
    def get_list_of_elements_vertical_locations(condition, locator):
        other_elements = BaseElement.get_displayed_elements(condition, locator)
        return [element.location[BaseElement.coordinate_y] for element in other_elements]

    @staticmethod
    def get_dict_of_elements_vertical_locations_and_text(condition, locator):
        events_time_elements = BaseElement.get_displayed_elements(condition, locator)
        events_info = {}
        for element in events_time_elements:
            events_info[element.location[BaseElement.coordinate_y]] = element.text
        return events_info

    @staticmethod
    def get_dict_of_elements_attribute_and_vertical_location(condition, locator, attribute_name):
        events_time_elements = BaseElement.get_displayed_elements(condition, locator)
        events_info = {}
        for element in events_time_elements:
            events_info[element.location[BaseElement.coordinate_y]] = element.get_attribute(attribute_name)
        return events_info
