from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from appium_selenium_driver.elements_tools import ElementsTools


class WaitForElementTools:

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element_to_be_present(self, selector, driver=None, timeout=30):
        driver = driver or self.driver
        try:
            element = WebDriverWait(driver=driver, timeout=timeout).until(ec.presence_of_element_located(selector))
            if not element:
                raise NoSuchElementException
            ElementsTools.take_screenshot(driver=self.driver)
            return element
        except Exception as e:
            ElementsTools.take_screenshot(driver=self.driver, filename='element_not_found')
            print("element {} not found exception: {}".format(selector, e))
            raise e

    def wait_for_element_to_be_clickable(self, selector, driver=None, timeout=30):
        driver = driver or self.driver
        try:
            element = WebDriverWait(driver=driver, timeout=timeout).until(ec.element_to_be_clickable(selector))
            if not element:
                raise NoSuchElementException
            ElementsTools.take_screenshot(driver=self.driver)
            return element
        except Exception as e:
            ElementsTools.take_screenshot(driver=self.driver, filename='element_not_found')
            print("element {} not found exception: {}".format(selector, e))
            raise e

    def wait_for_elements_to_be_present(self, selector, driver=None, timeout=30):
        driver = driver or self.driver
        try:
            elements = WebDriverWait(driver=driver, timeout=timeout). \
                until(ec.visibility_of_all_elements_located(selector))
            if not elements:
                raise NoSuchElementException
            ElementsTools.take_screenshot(driver=self.driver)
            return elements
        except Exception as e:
            ElementsTools.take_screenshot(driver=self.driver, filename='element_not_found')
            print("element {} not found exception: {}".format(selector, e))
            raise e

    def wait_for_element_contain_text(self, selector, driver=None, text_contain=None, timeout=30):
        by, selector_new = selector
        new_selector = (by, selector_new.format(text=text_contain))
        self.wait_for_elements_to_be_present(selector=new_selector, driver=driver, timeout=timeout)

    def wait_for_element_to_be_invisible(self, selector, driver=None, timeout=30):
        driver = driver or self.driver
        return WebDriverWait(driver=driver, timeout=timeout). \
            until(ec.invisibility_of_element_located(selector))


