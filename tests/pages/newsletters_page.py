import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from framework.browser.browser import Browser
from framework.elements.button import Button
from framework.elements.text_box import TextBox
from framework.pages.base_page import BasePage
from framework.utils.logger import Logger
from framework.utils.random_util import RandomUtil
from tests.config.waits import Waits


class NewslettersPage(BasePage):
    by = By.XPATH
    lbl_header_loc = "//span[text()='Our newsletters']"
    newsletters_titles_loc = "//form[@id='newsletters-form']//h2"
    tbx_email_loc = "//input[@type='email']"
    btn_submit_email_loc = "//input[@type='submit']"
    btn_unsubscribe_loc = "//a[text()='unsubscribe by clicking here']"

    @property
    def btn_unsubscribe(self):
        return Button(search_condition=self.by, locator=self.btn_unsubscribe_loc, name="Unsubscribe")

    @property
    def preview_frame_of_chosen_newsletter(self):
        Logger.info("Finding preview iframe element")
        locator = f"//div[@id='{self.newsletter_title.lower().replace(' ', '-')}_previews']//iframe"
        WebDriverWait(self.driver, Waits.EXPLICITLY_WAIT_SEC).until(ec.visibility_of_element_located((self.by,
                                                                                                      locator)))
        return self.driver.find_element(self.by, locator)

    @property
    def newsletters_titles(self):
        return self.driver.find_elements(self.by, self.newsletters_titles_loc)

    @property
    def tbx_email(self):
        return TextBox(search_condition=self.by, locator=self.tbx_email_loc, name="Email")

    @property
    def btn_submit_email(self):
        return Button(search_condition=self.by, locator=self.btn_submit_email_loc, name="Submit")

    def __init__(self):
        super().__init__(search_condition=self.by, locator=self.lbl_header_loc,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()
        self.browser = Browser()
        self.driver = self.browser.get_driver()
        self.newsletter_title = None
        self.btn_preview_random_newsletter = None

    def choose_random_newsletter(self):
        with allure.step("Selecting random newsletter"):
            self.newsletter_title = RandomUtil.random_choice(self.newsletters_titles).text
            Logger.info(f"Random newsletter title chosen: {self.newsletter_title}")
            random_newsletter = self.driver.find_element(self.by, f"//h2[text()='{self.newsletter_title}']"
                                                                  f"/following-sibling::div[2]"
                                                                  f"//label[contains(text(),'Select this newsletter')]"
                                                                  f"//..")
            Logger.info(f"Random newsletter select button found")
            WebDriverWait(self.driver, Waits.EXPLICITLY_WAIT_SEC).until(ec.element_to_be_clickable(random_newsletter))
            random_newsletter.click()
            Logger.info("Random newsletter selected")

    def click_see_preview_on_chosen_newsletter(self):
        with allure.step("Click see preview on chosen newsletter"):
            see_preview = self.driver.find_element(self.by, f"//h2[text()='{self.newsletter_title}']"
                                                            f"/following-sibling::a")
            Logger.info("See preview button found")
            WebDriverWait(self.driver, Waits.EXPLICITLY_WAIT_SEC).until(ec.element_to_be_clickable(see_preview))
            see_preview.click()
            Logger.info("See preview button clicked")

    def email_form_is_displayed(self):
        return self.tbx_email.is_displayed()

    def submit_email(self, email):
        with allure.step("Enter email and click submit"):
            self.tbx_email.send_keys(email)
            self.btn_submit_email.click()

    def preview_of_required_plan_is_displayed(self):
        return self.preview_frame_of_chosen_newsletter.is_displayed()

    def follow_unsubscribe_link(self):
        with allure.step("Finding and clicking unsubscribe link"):
            self.browser.switch_to_frame_by_locator(
                self.by, f"//div[@id='{self.newsletter_title.lower().replace(' ', '-')}_previews']//iframe")
            self.btn_unsubscribe.click()
