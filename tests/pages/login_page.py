from framework.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from framework.elements.text_box import TextBox
from selenium.webdriver.support import expected_conditions as ec
from framework.elements.button import Button
from framework.utils.random_util import RandomUtil
from framework.browser.browser import Browser


class LoginPage(BasePage):
    search_condition = By.XPATH
    login_form_container_loc = "//div[@class='login-form__container']"
    txb_password_loc = "//input[@placeholder='Choose Password']"
    txb_email_loc = "//input[@placeholder,'Your email']"
    txb_email_domain_loc = "//input[@placeholder,'Domain']"
    domain_dropdown_list_loc = "//div[@class,'dropdown__list']"
    btn_domain_dropdown_opener_loc = "//div[@class,'dropdown__opener']"
    cbx_terms_conditions_loc = "//input[@id,'accept-terms-conditions']"
    btn_terms_conditions_loc = "//span[@class,'login-form__terms-conditions-underline']"
    p_terms_conditions_last_loc = "//div[@class='terms-and-conditions__text-content']//p[last()]"
    btn_accept_terms_conditions_loc = "//button[text()='Accept']"
    btn_next_loc = "//a[@class='button-secondary' and text()=next]"

    def __init__(self):
        super().__init__(search_condition=LoginPage.search_condition, locator=LoginPage.login_form_container_loc,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()
        self.driver = Browser.get_driver()

    def input_random_password_email(self):
        txb_password = TextBox(search_condition=LoginPage.search_condition,
                               locator=LoginPage.txb_password_loc,
                               name='Password')
        txb_email = TextBox(search_condition=LoginPage.search_condition,
                            locator=LoginPage.txb_email_loc,
                            name='Email')
        txb_email_domain = TextBox(search_condition=LoginPage.search_condition,
                                   locator=LoginPage.txb_email_domain_loc,
                                   name='Email Domain')

        btn_domain_dropdown_opener = Button(search_condition=LoginPage.search_condition,
                                            locator=LoginPage.btn_domain_dropdown_opener_loc,
                                            name="Domain Dropdown Opener")

        password = RandomUtil.get_password()
        email = RandomUtil.get_string()
        email_domain = RandomUtil.get_string()

        txb_password.click()
        txb_password.clear_field()
        txb_password.send_keys(password)
        txb_email.click()
        txb_email.clear_field()
        txb_email.send_keys(email)
        txb_email_domain.click()
        txb_email_domain.clear_field()
        txb_email_domain.send_keys(email_domain)
        btn_domain_dropdown_opener.click()
        domain_list = self.driver.find_elements(By.XPATH, LoginPage.domain_dropdown_list_loc)
        random_domain = RandomUtil.random_choice(domain_list)
        self.driver.execute_script("arguments[0].scrollIntoView();", random_domain)
        self.driver.wait.untill(ec.element_to_be_clickable(random_domain))
        random_domain.click()

    def accept_terms_conditions(self):
        cbx_terms_conditions = Button(search_condition=LoginPage.search_condition,
                                      locator=LoginPage.cbx_terms_conditions_loc,
                                      name="Terms and Conditions Checkbox")
        btn_terms_conditions = Button(search_condition=LoginPage.search_condition,
                                      locator=LoginPage.btn_terms_conditions_loc,
                                      name="Terms and Conditions button")
        btn_accept_terms_conditions = Button(search_condition=LoginPage.search_condition,
                                             locator=LoginPage.btn_accept_terms_conditions_loc,
                                             name="Accept Terms and Conditions")
        cbx_terms_conditions.click()
        btn_terms_conditions.click()
        p_terms_conditions_last = self.driver.find_element(By.XPATH, LoginPage.p_terms_conditions_last_loc)
        self.driver.execute_script("arguments[0].scrollIntoView();", p_terms_conditions_last)
        btn_accept_terms_conditions.wait_for_clickable()
        btn_accept_terms_conditions.click()

    def fill_login_info_click_next(self):
        self.input_random_password_email()
        self.accept_terms_conditions()
        btn_next = Button(search_condition=LoginPage.search_condition,
                          locator=LoginPage.btn_next_loc,
                          name="Next")
        btn_next.wait_for_clickable()
        btn_next.click()