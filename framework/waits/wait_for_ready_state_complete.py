# coding=utf-8
from selenium.common.exceptions import StaleElementReferenceException

from framework.constants import page_states
from framework.scripts import scripts_js


class WaitForReadyStateComplete(object):
    def __init__(self, browser):
        self.browser = browser

    def __call__(self, driver):
        try:
            return self.browser.execute_script(scripts_js.GET_PAGE_READY_STATE) == page_states.COMPLETE
        except StaleElementReferenceException:
            return False
