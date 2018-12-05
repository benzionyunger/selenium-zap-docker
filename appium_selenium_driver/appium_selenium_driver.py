from appium import webdriver as appium_driver
from selenium import webdriver
from appium_selenium_driver.wait_for_elements_tools import WaitForElementTools
from appium_selenium_driver.elements_tools import ElementsTools


class AndroidDriver:

    def __init__(self, address='http://localhost:4723/wd/hub', desired_capabilities=None, browser_profile=None, remote=True):
        if browser_profile == "chrome" and not remote:
            self.driver = webdriver.Chrome()
        elif browser_profile == "firefox" and not remote:
            self.driver = webdriver.Firefox()
        elif browser_profile and remote:
            if not address:
                address = 'http://127.0.0.1:4444/wd/hub'
            self.driver = webdriver.Remote(command_executor=address, desired_capabilities=desired_capabilities)
        else:
            self.driver = appium_driver.Remote(address, desired_capabilities, browser_profile=browser_profile)
        self.wait = WaitForElementTools(self.driver)
        self.tools = ElementsTools(self.driver, self.wait)
