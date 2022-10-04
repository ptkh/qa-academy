# coding=utf-8

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from tests.config.browser import BrowserConfig, Grid
from framework.constants import browsers
from os import environ


class BrowserFactory:

    @staticmethod
    def get_browser_driver(capabilities=None, is_incognito=False, enable_performance_logging=False, test_name=None,
                           grid_port=None):
        if capabilities is None:
            capabilities = {}
        if BrowserConfig.BROWSER == browsers.BROWSER_CHROME:
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_experimental_option('w3c', False)

            if is_incognito:
                chrome_options.add_argument("--incognito")
            if enable_performance_logging:
                capabilities['loggingPrefs'] = {'performance': 'ALL'}
            if Grid.USE_GRID:
                return BrowserFactory.get_remote_driver(browser_name=BrowserConfig.BROWSER,
                                                        browser_version=BrowserConfig.CHROME_VERSION,
                                                        options=chrome_options, capabilities=capabilities,
                                                        test_name=test_name)
            else:
                return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options,
                                        desired_capabilities=capabilities)

        elif BrowserConfig.BROWSER == browsers.BROWSER_FIREFOX:
            firefox_profile = webdriver.FirefoxProfile()
            firefox_options = None
            if is_incognito:
                firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
            if enable_performance_logging:
                open("perfLog.txt", "w").close()
                environ["MOZ_LOG"] = "timestamp,sync,nsHttp:3"
            if Grid.USE_GRID:
                return BrowserFactory.get_remote_driver(browser_name=BrowserConfig.BROWSER,
                                                        browser_version=BrowserConfig.FIREFOX_VERSION,
                                                        browser_profile=firefox_profile, capabilities=capabilities,
                                                        test_name=test_name, grid_port=grid_port)
            else:
                return webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                         firefox_profile=firefox_profile,
                                         desired_capabilities=capabilities, firefox_options=firefox_options)

    @staticmethod
    def get_remote_driver(browser_name, browser_version, options=None, browser_profile=None, capabilities=None,
                          test_name=None, grid_port=None):
        if capabilities is None:
            capabilities = {}
        capabilities["browserName"] = browser_name
        capabilities["version"] = browser_version
        capabilities["name"] = test_name
        return webdriver.Remote(command_executor=Grid.GRID_URL.format(host=Grid.GRID_HOST, port=grid_port),
                                desired_capabilities=capabilities, options=options,
                                browser_profile=browser_profile)