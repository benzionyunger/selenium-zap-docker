from appium import webdriver
from android_appium_driver.wait_for_elements_tools import WaitForElementTools
from android_appium_driver.elements_tools import ElementsTools


class AndroidDriver:

    def __init__(self, address='http://localhost:4723/wd/hub', desired_capabilities=None, browser_profile=None):
        self.driver = webdriver.Remote(address, desired_capabilities, browser_profile=browser_profile)
        self.wait = WaitForElementTools(self.driver)
        self.tools = ElementsTools(self.driver, self.wait)
