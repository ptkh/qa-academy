from selenium.webdriver.common.by import By
from framework.pages.base_page import BasePage
from framework.elements.label import Label
from tests.config.waits import Waits


class DetailsPage(BasePage):
    search_condition = By.XPATH
    page_indicator_loc = "//div[@class='page-indicator']"

    @property
    def page_indicator(self):
        return Label(search_condition=DetailsPage.search_condition, locator=DetailsPage.page_indicator_loc,
                     name="Page indicator")

    def __init__(self):
        super().__init__(search_condition=DetailsPage.search_condition, locator=DetailsPage.page_indicator_loc,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()

    def card_is_open(self):
        self.page_indicator.wait_for_text("3 / 4", Waits.EXPLICITLY_WAIT_SEC)
        return "3 / 4" == self.page_indicator.get_text()