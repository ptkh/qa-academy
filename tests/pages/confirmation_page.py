from selenium.webdriver.common.by import By
from framework.elements.button import Button
from framework.elements.label import Label
from framework.pages.base_page import BasePage


class ConfirmationPage(BasePage):
    search_condition = By.XPATH
    lbl_success_message_loc = "//h1[text()='Your subscription has been successfully confirmed.']"
    btn_back_to_site_loc = "//a[@aria-label='Back to the site']"

    @property
    def lbl_success_message(self):
        return Label(search_condition=self.search_condition, locator=self.lbl_success_message_loc,
                     name="Success message")

    @property
    def btn_back_to_site(self):
        return Button(search_condition=self.search_condition, locator=self.btn_back_to_site_loc,
                      name="Back to the site")

    def __init__(self):
        super().__init__(search_condition=self.search_condition, locator=self.lbl_success_message_loc,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()

    def confirmation_success_message_is_displayed(self):
        return self.lbl_success_message.is_displayed()

    def click_back_to_the_site(self):
        self.btn_back_to_site.click()
