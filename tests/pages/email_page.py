from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from framework.elements.checkbox import CheckBox
from framework.pages.base_page import BasePage
from framework.elements.label import Label
from framework.elements.text_box import TextBox
from framework.elements.button import Button
from framework.utils.random_util import RandomUtil
from framework.browser.browser import Browser
from framework.scripts.scripts_js import SCROLL_INTO_VIEW
from tests.config.waits import Waits

from tests.test_data import TestData


class EmailPage(BasePage):
    search_condition = By.XPATH
    page_indicator_loc = "//div[@class='page-indicator']"
    txb_password_loc = "//input[@placeholder='Choose Password']"
    txb_email_loc = "//input[@placeholder='Your email']"
    txb_email_domain_loc = "//input[@placeholder='Domain']"
    domain_dropdown_list_loc = "//div[@class='dropdown__list-item']"
    lbl_dropdown_field_loc = 'dropdown__field'
    btn_domain_dropdown_opener_loc = "//div[@class='dropdown__opener']"
    cbx_terms_conditions_loc = "//span[@class='checkbox__box']"
    btn_next_loc = "//a[text()='Next']"
    btn_send_to_bottom_loc = "//button[contains(@class,'send-to-bottom')]"
    help_form_title_loc = "//h2[@class='help-form__title']"
    btn_accept_cookies_loc = "//button[text()='Not really, no']"
    lbl_timer_loc = "//div[contains(@class,'timer')]"

    @property
    def page_indicator(self):
        return Label(search_condition=EmailPage.search_condition, locator=EmailPage.page_indicator_loc,
                     name="Page indicator")

    @property
    def txb_password(self):
        return TextBox(search_condition=EmailPage.search_condition, locator=EmailPage.txb_password_loc, name='Password')

    @property
    def txb_email(self):
        return TextBox(search_condition=EmailPage.search_condition, locator=EmailPage.txb_email_loc, name='Email')

    @property
    def txb_email_domain(self):
        return TextBox(search_condition=EmailPage.search_condition, locator=EmailPage.txb_email_domain_loc,
                       name='Email Domain')

    @property
    def btn_domain_dropdown_opener(self):
        return TextBox(search_condition=EmailPage.search_condition, locator=EmailPage.btn_domain_dropdown_opener_loc,
                       name='Domain Dropdown Opener')

    @property
    def domain_list(self):
        return self.driver.find_elements(EmailPage.search_condition, EmailPage.domain_dropdown_list_loc)

    @property
    def lbl_dropdown_field(self):
        return Label(search_condition=By.CLASS_NAME, locator=EmailPage.lbl_dropdown_field_loc, name='Dropdown field')

    @property
    def cbx_terms_conditions(self):
        return CheckBox(search_condition=EmailPage.search_condition, locator=EmailPage.cbx_terms_conditions_loc,
                        name="Terms and Conditions Checkbox")

    @property
    def btn_next(self):
        return Button(search_condition=EmailPage.search_condition, locator=EmailPage.btn_next_loc,
                      name="Next on card 1")

    @property
    def btn_send_to_bottom(self):
        return Button(search_condition=EmailPage.search_condition, locator=EmailPage.btn_send_to_bottom_loc,
                      name="Send to bottom")

    @property
    def help_form_title(self):
        return self.driver.find_element(EmailPage.search_condition, EmailPage.help_form_title_loc)

    @property
    def btn_accept_cookies(self):
        return Button(search_condition=EmailPage.search_condition, locator=EmailPage.btn_accept_cookies_loc,
                      name="Not really, no")

    @property
    def lbl_timer(self):
        return Label(search_condition=EmailPage.search_condition, locator=EmailPage.lbl_timer_loc, name="Timer")

    def __init__(self):
        super().__init__(search_condition=EmailPage.search_condition, locator=EmailPage.page_indicator_loc,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()
        self.driver = Browser().get_driver()

    def card_is_open(self):
        self.page_indicator.wait_for_text("1 / 4", Waits.EXPLICITLY_WAIT_SEC)
        return "1 / 4" == self.page_indicator.get_text()

    def input_random_password(self):
        password = RandomUtil.get_password(TestData.PASSWORD_LENGTH) + TestData.COMMON_LETTER_IN_PWD_EMAIL
        self.txb_password.click()
        self.txb_password.clear_field()
        self.txb_password.send_keys(password)

    def input_random_email(self):
        email = RandomUtil.get_string(TestData.EMAIL_LENGTH).lower() + TestData.COMMON_LETTER_IN_PWD_EMAIL
        self.txb_email.click()
        self.txb_email.clear_field()
        self.txb_email.send_keys(email)

        email_domain = RandomUtil.get_string(TestData.EMAIL_LENGTH).lower()
        self.txb_email_domain.click()
        self.txb_email_domain.clear_field()
        self.txb_email_domain.send_keys(email_domain)

        self.btn_domain_dropdown_opener.click()
        random_domain = RandomUtil.random_choice(self.domain_list)
        self.driver.execute_script(SCROLL_INTO_VIEW, random_domain)
        WebDriverWait(self.driver, Waits.EXPLICITLY_WAIT_SEC).until(ec.element_to_be_clickable(random_domain))
        random_domain.click()

    def accept_terms_of_use(self):
        self.cbx_terms_conditions.click()

    def fill_login_page_and_click_next(self):
        self.input_random_password()
        self.input_random_email()
        self.accept_terms_of_use()
        self.btn_next.click()

    def hide_help_form(self):
        self.btn_send_to_bottom.click()

    def help_form_is_hidden(self):
        WebDriverWait(self.driver, Waits.EXPLICITLY_WAIT_SEC).until(ec.invisibility_of_element(self.help_form_title))
        return not self.help_form_title.is_displayed()

    def accept_cookies(self):
        self.btn_accept_cookies.click()

    def cookies_form_is_hidden(self):
        self.btn_accept_cookies.wait_for_invisibility()
        return not self.btn_accept_cookies.is_displayed()

    def check_initial_timer_value(self, value):
        return self.lbl_timer.get_text() == value
