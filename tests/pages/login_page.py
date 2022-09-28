from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from framework.pages.base_page import BasePage
from framework.elements.text_box import TextBox
from framework.elements.button import Button
from framework.utils.random_util import RandomUtil
from framework.browser.browser import Browser
from framework.scripts.scripts_js import SCROLL_INTO_VIEW
from time import sleep



class LoginPage(BasePage):
    search_condition = By.XPATH
    login_form_container_loc = "//div[@class='login-form__container']"
    txb_password_loc = "//input[@placeholder='Choose Password']"
    txb_email_loc = "//input[@placeholder='Your email']"
    txb_email_domain_loc = "//input[@placeholder='Domain']"
    domain_dropdown_list_loc = "//div[@class='dropdown__list']"
    btn_domain_dropdown_opener_loc = "//div[@class='dropdown__opener']"
    cbx_terms_conditions_loc = "//span[@class='checkbox__box']"
    btn_terms_conditions_loc = "//span[@class='login-form__terms-conditions-underline']"
    div_terms_conditions_loc = "//div[@class='terms-and-conditions__text-content']"
    btn_accept_terms_conditions_loc = "//button[text()='Accept']"
    btn_next_loc = "//a[@class='button-secondary' and text()=next]"

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
    def cbx_terms_conditions(self):
        return Button(search_condition=LoginPage.search_condition, locator=LoginPage.cbx_terms_conditions_loc,
                      name="Terms and Conditions Checkbox")

    @property
    def btn_terms_conditions(self):
        return Button(search_condition=LoginPage.search_condition, locator=LoginPage.btn_terms_conditions_loc,
                      name="Terms and Conditions button")

    @property
    def btn_accept_terms_conditions(self):
        return Button(search_condition=LoginPage.search_condition, locator=LoginPage.btn_accept_terms_conditions_loc,
                      name="Accept Terms and Conditions")

    @property
    def btn_next(self):
        return Button(search_condition=LoginPage.search_condition, locator=LoginPage.btn_next_loc, name="Next")

    def __init__(self):
        super().__init__(search_condition=LoginPage.search_condition, locator=LoginPage.login_form_container_loc,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()
        self.driver = Browser().get_driver()

    def input_random_password(self):
        password = 'a' + RandomUtil.get_password(11)
        self.txb_password.click()
        self.txb_password.clear_field()
        self.txb_password.send_keys(password)

    def input_random_email(self):
        email = 'a' + RandomUtil.get_string(7)
        self.txb_email.click()
        self.txb_email.clear_field()
        self.txb_email.send_keys(email)

        email_domain = RandomUtil.get_string(8)
        self.txb_email_domain.click()
        self.txb_email_domain.clear_field()
        self.txb_email_domain.send_keys(email_domain)

        self.btn_domain_dropdown_opener.click()
        domain_list = self.driver.find_elements(By.XPATH, LoginPage.domain_dropdown_list_loc)
        random_domain = RandomUtil.random_choice(domain_list)
        self.driver.execute_script(SCROLL_INTO_VIEW, random_domain)
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(random_domain))
        random_domain.click()

    def accept_terms_conditions(self):
        self.cbx_terms_conditions.click()
        self.btn_terms_conditions.click()
        scroller = self.driver.find_element(By.CLASS_NAME, "terms-and-conditions__text-scrollbar__scroller")
        for _ in range(100):
            close = self.driver.find_elements(By.XPATH, "//span[@class='modal__close-copyright']//span")
            if close:
                if close[0].is_displayed():
                    close[0].click()
            ActionChains(self.driver).drag_and_drop_by_offset(scroller, 0, 500).perform()
        sleep(10)
        # div_terms_conditions = self.driver.find_element(By.XPATH, LoginPage.div_terms_conditions_loc)
        self.btn_accept_terms_conditions.wait_for_clickable()
        self.btn_accept_terms_conditions.click()
        sleep(5)

    def fill_login_form_and_click_next(self):
        self.input_random_password()
        self.input_random_email()
        self.accept_terms_conditions()
        self.btn_next.wait_for_clickable()
        self.btn_next.click()
