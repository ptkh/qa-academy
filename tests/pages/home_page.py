from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from elements.text_box import TextBox
from elements.label import Label
from elements.button import Button
from selenium.webdriver.common.keys import Keys
from browser.browser import Browser
# from


class HomePage(BasePage):
    search_condition = By.XPATH
    # lbl_logo = "//img[@alt='Google']"
    # txb_search_line = "//input[@title='Поиск']"
    # txb_asd = "//input[@title='ksjdofkdmsfkldmsfl']"

    lbl_login_loc = "//div[contains(@class, 'auth-bar__item') and contains(text(), 'Вход')]"
    lbl_login = Label(search_condition=search_condition, locator=lbl_login_loc,
                      name="Login button")
    txb_login = TextBox(search_condition=search_condition,
                        locator='//*[contains(@class, "auth-input") and contains(@class, "auth-input_primary")][@type="text"]',
                        name='Login')
    txb_password = TextBox(search_condition=search_condition, locator='//*[contains(@class, "auth-input") and contains(@class,' +
                        ' "auth-input_primary")][@type="password"]', name='Password')
    btn_login = Button(search_condition=search_condition, locator='//button[contains(@class, "auth-button")][@type="submit"]', name='Login')

    lbl_menu = Label(search_condition=search_condition, locator='//li[@class="b-main-navigation__item"]//a', name='Menu')

    lbl_menu_bank = Label(search_condition=search_condition, locator="//div[contains(@class, 'social-likes')]", name="menu_bank")

    def __init__(self):
        super().__init__(search_condition=HomePage.search_condition, locator=HomePage.lbl_login_loc,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()

        self.lbl_login = Label(search_condition=HomePage.search_condition, locator=HomePage.lbl_login_loc,
                               name="Login button")

    def login(self, login, password):
        # a = HomePage.lbl_login#.click()

        # HomePage.txb_login.send_keys(login)
        # HomePage.txb_password.send_keys(password)

        q = HomePage.lbl_menu_bank.get_attribute(attr='title')
        # a = HomePage.lbl_menu_bank(sublocator="/div[1]")
        a = HomePage.lbl_menu_bank[2]
        w = a.get_attribute(attr='title')

        print()



        # HomePage.btn_login.click()
        # a = HomePage.lbl_menu.get_displayed_elements(By.XPATH, '//li[@class="b-main-navigation__item"]//a')[0]
        # print(HomePage.lbl_login.is_displayed())
        # a = Label(search_condition=HomePage.search_condition, locator="//span[text()='Корзина']", name='sdfdsf')
        #
        # # Browser.get_browser().set_url('https://google.com')
        #
        # Browser.get_browser().get_count_windows()
        #
        # a.key_down(Keys.LEFT_CONTROL)
        #
        # asd = Browser.get_browser().get_cookies()
        # zxc= Browser.get_browser().get_cookie(name='www.onliner.by')
        # # a.click()
        # # a.key_up(Keys.CONTROL)
        # Browser.get_browser().execute_script("window.open('https://twitter.com')")
        # Browser.get_browser().switch_new_window()
        # asd = Browser.get_browser().get_cookies()
        # sdfdsf = Browser.get_browser().get_count_windows()
        # a.wait_for_invisibility()
        # qwe = TextBox(search_condition=HomePage.search_condition, locator=HomePage.txb_search_line, name="Search line")
        # qwe.send_keys(text)
        # q = qwe.get_value()
        #

        # asd = TextBox(search_condition=HomePage.search_condition, locator=HomePage.txb_asd, name="line")
        # print(asd.is_displayed())
