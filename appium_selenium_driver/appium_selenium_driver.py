from appium import webdriver as appium_driver
from selenium import webdriver
from appium_selenium_driver.wait_for_elements_tools import WaitForElementTools
from appium_selenium_driver.elements_tools.appium_elements_tools import AppiumElementsTools
from appium_selenium_driver.elements_tools.selenium_elements_tools import SeleniumElementsTools


class Driver:

    def __init__(self, address='http://localhost:4723/wd/hub', desired_capabilities=None, browser_profile=None,
                 remote=True):

        if browser_profile == "chrome" and not remote:
            self.driver = webdriver.Chrome()
            self.wait = WaitForElementTools(self.driver)
            self.tools = SeleniumElementsTools(self.driver, self.wait)

        elif browser_profile == "firefox" and not remote:
            self.driver = webdriver.Firefox()
            self.wait = WaitForElementTools(self.driver)
            self.tools = SeleniumElementsTools(self.driver, self.wait)
        elif browser_profile and remote:
            if not address:
                address = 'http://127.0.0.1:4444/wd/hub'
            self.driver = webdriver.Remote(command_executor=address, desired_capabilities=desired_capabilities)
            self.wait = WaitForElementTools(self.driver)
            self.tools = SeleniumElementsTools(self.driver, self.wait)
        else:
            self.driver = appium_driver.Remote(address, desired_capabilities, browser_profile=browser_profile)
            self.wait = WaitForElementTools(self.driver)
            self.tools = AppiumElementsTools(self.driver, self.wait)
