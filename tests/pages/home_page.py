from framework.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from framework.elements.button import Button


class HomePage(BasePage):
    search_condition = By.XPATH
    btn_go_to_next_page_loc = "//a[@class='start__link']"

    def __init__(self):
        super().__init__(search_condition=HomePage.search_condition,
                         locator=HomePage.btn_go_to_next_page_loc,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()
        self.btn_go_to_next_page = Button(search_condition=HomePage.search_condition,
                                          locator=HomePage.btn_go_to_next_page_loc,
                                          name="HERE")

    def go_to_next_page(self):
        self.btn_go_to_next_page.click()

    def welcome_page_is_open(self):
        return self.btn_go_to_next_page.is_displayed()
