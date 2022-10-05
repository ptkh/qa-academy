from selenium.webdriver.common.by import By
from framework.elements.checkbox import CheckBox
from framework.pages.base_page import BasePage
from framework.elements.label import Label
from framework.elements.button import Button
from framework.utils.random_util import RandomUtil
from framework.browser.browser import Browser
from tests.config.waits import Waits
from tests.testData.testData import TestData
import pyautogui


class InterestsPage(BasePage):
    search_condition = By.XPATH
    cbx_interest_list_loc = "//input[contains(@id,'interest_')]//following::span[@class='checkbox__box']"
    cbx_interests_unselect_all_loc = "//input[@id='interest_unselectall']//following::span[@class='checkbox__box']"
    cbx_interests_select_all_loc = "//input[@id='interest_selectall']//following::span[@class='checkbox__box']"
    btn_next_loc = "//button[text()='Next']"
    btn_upload_image_loc = "//a[@class='avatar-and-interests__upload-button']"
    page_indicator_loc = "//div[@class='page-indicator']"

    @property
    def page_indicator(self):
        return Label(search_condition=InterestsPage.search_condition, locator=InterestsPage.page_indicator_loc,
                     name="Page indicator")

    @property
    def cbx_interests_list(self):
        return self.driver.find_elements(By.XPATH, InterestsPage.cbx_interest_list_loc)

    @property
    def cbx_interests_unselect_all(self):
        return CheckBox(search_condition=InterestsPage.search_condition, locator=InterestsPage.cbx_interests_unselect_all_loc,
                        name="Unselect all")

    @property
    def cbx_interests_select_all(self):
        return CheckBox(search_condition=InterestsPage.search_condition, locator=InterestsPage.cbx_interests_select_all_loc,
                        name="Select all")

    @property
    def btn_upload_image(self):
        return Button(search_condition=InterestsPage.search_condition, locator=InterestsPage.btn_upload_image_loc,
                      name="upload")

    @property
    def btn_next(self):
        return Button(search_condition=InterestsPage.search_condition, locator=InterestsPage.btn_next_loc,
                      name="Next on card 2")

    def __init__(self):
        super().__init__(search_condition=InterestsPage.search_condition, locator=InterestsPage.page_indicator_loc,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()
        self.driver = Browser().get_driver()

    def card_is_open(self):
        self.page_indicator.wait_for_text("2 / 4", Waits.EXPLICITLY_WAIT_SEC)
        return "2 / 4" == self.page_indicator.get_text()

    def upload_image(self):
        self.btn_upload_image.click()
        pyautogui.sleep(1)
        pyautogui.write(TestData.IMAGE_FILEPATH)
        pyautogui.press('enter')

    def choose_random_interests(self):
        interests = [] + self.cbx_interests_list
        self.cbx_interests_unselect_all.click()
        interests.remove(self.cbx_interests_unselect_all.find_element())
        interests.remove(self.cbx_interests_select_all.find_element())
        for _ in range(TestData.INTERESTS_NUM):
            item = RandomUtil.random_choice(interests)
            item.click()
            interests.remove(item)

    def fill_interests_page_and_click_next(self):
        self.upload_image()
        self.choose_random_interests()
        self.btn_next.click()

