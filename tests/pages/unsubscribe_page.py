from selenium.webdriver.common.by import By
from framework.elements.button import Button
from framework.elements.label import Label
from framework.elements.text_box import TextBox
from framework.pages.base_page import BasePage


class UnsubscribePage(BasePage):
    by = By.XPATH
    lbl_newsletter_unsubscription_loc = "//h3[text()='Newsletter unsubscription']"
    tbx_email_loc = "//input[@id='email']"
    btn_confirm_unsubscription_loc = "//button[text()='Confirm unsubscription']"
    lbl_subscription_cancelled_loc = "//strong[text()='You are unsubscribed.']"

    @property
    def lbl_subscription_cancelled(self):
        return Label(search_condition=self.by, locator=self.lbl_subscription_cancelled_loc, name="Subscription cancelled")

    @property
    def btn_confirm_unsubscription(self):
        return Button(search_condition=self.by, locator=self.btn_confirm_unsubscription_loc,
                      name="Confirm unsubscription")

    @property
    def tbx_email(self):
        return TextBox(By.XPATH, self.tbx_email_loc)

    def __init__(self):
        super().__init__(search_condition=self.by, locator=self.lbl_newsletter_unsubscription_loc,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()

    def enter_email_and_submit(self, email):
        self.tbx_email.send_keys(email)
        self.btn_confirm_unsubscription.click()

    def subscription_cancelled_message_is_displayed(self):
        return self.lbl_subscription_cancelled.is_displayed()

