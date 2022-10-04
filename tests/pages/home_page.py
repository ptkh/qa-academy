from framework.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from framework.elements.button import Button


class HomePage(BasePage):
    by = By.XPATH
    div_topstories_loc = "//div[contains(@class,'b-topstories-home')]"
    link_newsletters_loc = "//a//span[text()='Newsletters']"
    btn_continue_without_agreeing_loc = "//span[contains(@class,'continue-without-agreeing')]"

    @property
    def link_newsletters(self):
        return Button(search_condition=self.by, locator=self.link_newsletters_loc, name="Newsletters")

    @property
    def btn_continue_without_agreeing(self):
        return Button(search_condition=self.by, locator=self.btn_continue_without_agreeing_loc,
                      name="Continue without agreeing")

    def __init__(self):
        super().__init__(search_condition=self.by, locator=self.div_topstories_loc,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()
        self.btn_continue_without_agreeing.click()

    def navigate_to_newsletters(self):
        self.link_newsletters.click()
