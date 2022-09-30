from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from framework.pages.base_page import BasePage
from framework.elements.label import Label
from framework.elements.text_box import TextBox
from framework.elements.button import Button
from framework.utils.random_util import RandomUtil
from framework.browser.browser import Browser
from framework.scripts.scripts_js import SCROLL_INTO_VIEW
import pyautogui
import os


class LoginPage(BasePage):
    search_condition = By.XPATH
    login_form_container_loc = "//div[@class='login-form__container']"
    txb_password_loc = "//input[@placeholder='Choose Password']"
    txb_email_loc = "//input[@placeholder='Your email']"
    txb_email_domain_loc = "//input[@placeholder='Domain']"
    domain_dropdown_list_loc = "//div[@class='dropdown__list']"
    lbl_dropdown_field_loc = 'dropdown__field'
    btn_domain_dropdown_opener_loc = "//div[@class='dropdown__opener']"
    cbx_terms_conditions_loc = "//span[@class='checkbox__box']"
    btn_card_1_next_loc = "//a[text()='Next']"
    cbx_interest_list_loc = "//input[contains(@id,'interest_')]//following::span[@class='checkbox__box']"
    cbx_interests_unselect_all_loc = "//input[@id='interest_unselectall']//following::span[@class='checkbox__box']"
    cbx_interests_select_all_loc = "//input[@id='interest_selectall']//following::span[@class='checkbox__box']"
    btn_card_2_next_loc = "//button[text()='Next']"
    btn_upload_image_loc = "//a[@class='avatar-and-interests__upload-button']"
    page_indicator_loc = "//div[@class='page-indicator']"
    btn_send_to_bottom_loc = "//button[contains(@class,'send-to-bottom')]"
    btn_accept_cookies_loc = "//button[text()='Not really, no']"
    lbl_timer_loc = "//div[contains(@class,'timer')]"

    @property
    def page_indicator(self):
        return Label(search_condition=LoginPage.search_condition, locator=LoginPage.page_indicator_loc,
                     name="Page indicator")

    @property
    def txb_password(self):
        return TextBox(search_condition=LoginPage.search_condition, locator=LoginPage.txb_password_loc, name='Password')

    @property
    def txb_email(self):
        return TextBox(search_condition=LoginPage.search_condition, locator=LoginPage.txb_email_loc, name='Email')

    @property
    def txb_email_domain(self):
        return TextBox(search_condition=LoginPage.search_condition, locator=LoginPage.txb_email_domain_loc,
                       name='Email Domain')

    @property
    def btn_domain_dropdown_opener(self):
        return TextBox(search_condition=LoginPage.search_condition, locator=LoginPage.btn_domain_dropdown_opener_loc,
                       name='Domain Dropdown Opener')

    @property
    def domain_list(self):
        return self.driver.find_elements(LoginPage.search_condition, LoginPage.domain_dropdown_list_loc)

    @property
    def lbl_dropdown_field(self):
        return Label(search_condition=By.CLASS_NAME, locator=LoginPage.lbl_dropdown_field_loc, name='Dropdown field')

    @property
    def cbx_terms_conditions(self):
        return Button(search_condition=LoginPage.search_condition, locator=LoginPage.cbx_terms_conditions_loc,
                      name="Terms and Conditions Checkbox")

    @property
    def btn_card_1_next(self):
        return Button(search_condition=LoginPage.search_condition, locator=LoginPage.btn_card_1_next_loc,
                      name="Next on card 1")

    @property
    def cbx_interests_list(self):
        return self.driver.find_elements(By.XPATH, LoginPage.cbx_interest_list_loc)

    @property
    def cbx_interests_unselect_all(self):
        return self.driver.find_element(LoginPage.search_condition, LoginPage.cbx_interests_unselect_all_loc)

    @property
    def cbx_interests_select_all(self):
        return self.driver.find_element(LoginPage.search_condition, LoginPage.cbx_interests_select_all_loc)

    @property
    def btn_upload_image(self):
        return Button(search_condition=LoginPage.search_condition, locator=LoginPage.btn_upload_image_loc,
                      name="upload")

    @property
    def btn_card_2_next(self):
        return Button(search_condition=LoginPage.search_condition, locator=LoginPage.btn_card_2_next_loc,
                      name="Next on card 2")

    @property
    def btn_send_to_bottom(self):
        return Button(search_condition=LoginPage.search_condition, locator=LoginPage.btn_send_to_bottom_loc,
                      name="Send to bottom")

    @property
    def btn_accept_cookies(self):
        return Button(search_condition=LoginPage.search_condition, locator=LoginPage.btn_accept_cookies_loc,
                      name="Not really, no")

    @property
    def lbl_timer(self):
        return Label(search_condition=LoginPage.search_condition, locator=LoginPage.lbl_timer_loc, name="Timer")

    def __init__(self):
        super().__init__(search_condition=LoginPage.search_condition, locator=LoginPage.login_form_container_loc,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()
        self.driver = Browser().get_driver()

    def card_is_open(self, card_num):
        self.page_indicator.wait_for_text(f"{card_num} / 4", 10)
        return f"{card_num} / 4" == self.page_indicator.get_text()

    def input_random_password(self):
        password = RandomUtil.get_password(11) + 'a'
        self.txb_password.click()
        self.txb_password.clear_field()
        self.txb_password.send_keys(password)

    def input_random_email(self):
        email = RandomUtil.get_string(7).lower() + 'a'
        self.txb_email.click()
        self.txb_email.clear_field()
        self.txb_email.send_keys(email)
        email_domain = RandomUtil.get_string(8).lower()
        self.txb_email_domain.click()
        self.txb_email_domain.clear_field()
        self.txb_email_domain.send_keys(email_domain)
        while True:
            self.btn_domain_dropdown_opener.click()
            random_domain = RandomUtil.random_choice(self.domain_list)
            self.driver.execute_script(SCROLL_INTO_VIEW, random_domain)
            WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(random_domain))
            random_domain.click()
            if self.lbl_dropdown_field.get_text() != 'other':
                break

    def accept_terms_of_use(self):
        self.cbx_terms_conditions.click()

    def fill_card_1_and_click_next(self):
        self.input_random_password()
        self.input_random_email()
        self.accept_terms_of_use()
        self.btn_card_1_next.click()

    def upload_image(self):
        image_path = os.path.join(os.path.dirname(__file__), os.pardir, "avatar.png")
        self.btn_upload_image.click()
        pyautogui.sleep(3)
        pyautogui.write(image_path)
        pyautogui.press('enter')

    def choose_random_interests(self):
        interests = self.cbx_interests_list
        self.cbx_interests_unselect_all.click()
        interests.remove(self.cbx_interests_unselect_all)
        interests.remove(self.cbx_interests_select_all)
        for _ in 1, 2, 3:
            item = RandomUtil.random_choice(self.cbx_interests_list)
            item.click()
            self.cbx_interests_list.remove(item)

    def fill_card_2_and_click_next(self):
        self.upload_image()
        self.choose_random_interests()
        self.btn_card_2_next.click()

    def hide_help_form(self):
        self.btn_send_to_bottom.click()

    def help_form_is_hidden(self):
        self.btn_send_to_bottom.wait_for_invisibility()
        return not self.btn_send_to_bottom.is_displayed()

    def accept_cookies(self):
        self.btn_accept_cookies.click()
        pyautogui.sleep(1)
        pyautogui.write(os.path.join(os.getcwd(), '../tests/avatar.png'))
        pyautogui.press('return')

    def cookies_form_is_hidden(self):
        self.btn_accept_cookies.wait_for_invisibility()
        return not self.btn_accept_cookies.is_displayed()

    def initial_timer_value_is(self, value):
        return self.lbl_timer.get_text() == value
