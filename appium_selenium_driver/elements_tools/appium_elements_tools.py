import os
from pathlib import Path
from time import ctime
from appium_selenium_driver.elements_tools.selenium_elements_tools import SeleniumElementsTools


class AppiumElementsTools(SeleniumElementsTools):

    def __init__(self, driver, wait_element):
        SeleniumElementsTools.__init__(driver=driver,wait_element=wait_element)

    def wait_and_click(self, selector, driver=None, timeout=30, raise_exception=True):
        driver = driver or self.driver
        element = self.wait.wait_for_element_to_be_clickable(selector=selector, driver=driver, timeout=timeout,
                                                             raise_exception=raise_exception)
        self.take_screenshot(driver=self.driver)
        if element:
            return element.click()

    def get_text_from_element(self, selector, driver=None, timeout=30):
        driver = driver or self.driver
        element_text = self.wait.wait_for_element_to_be_present(selector=selector, driver=driver, timeout=timeout).text
        self.take_screenshot(driver=self.driver)
        return element_text

    def set_text(self, selector, text, driver=None, timeout=30):
        driver = driver or self.driver
        element = self.wait.wait_for_element_to_be_present(selector=selector, driver=driver, timeout=timeout)
        element.send_keys(text)
        self.take_screenshot(driver=self.driver)

    @staticmethod
    def take_screenshot(driver, filename=None):
        pic_path = Path(os.environ.get('CURRENT_LOGS_DIR', '_'.join(ctime().replace(':', '.').split())))
        filename = pic_path / "{}.png".format(filename) if filename else pic_path / "{}.png". \
            format('_'.join(ctime().replace(':', '.').split()))
        driver.save_screenshot(filename=str(filename))

    def make_list_of_strings_from_elements(self, selector, driver=None, timeout=30):
        driver = driver or self.driver
        elements = self.wait.wait_for_elements_to_be_present(selector=selector, driver=driver, timeout=timeout)
        elements_text = []
        for element in elements:
            elements_text.append(element.text)
        return elements_text

    def element_contain_text(self, text, selector, driver=None, timeout=30):
        driver = driver or self.driver
        if text in self.wait.wait_for_element_to_be_present(selector=selector, driver=driver, timeout=timeout).text:
            self.take_screenshot(driver=self.driver)
            return True
        return False

    # work only with appium driver not selenium
    def scroll_from_element_to_element_by_selector(self, from_element_selector=None, to_element_selector=None):
        from_element = self.wait.wait_for_element_to_be_present(selector=from_element_selector)
        to_element = self.wait.wait_for_element_to_be_present(selector=to_element_selector)
        self.driver.scroll(from_element, to_element)

    # work only with appium driver not selenium
    def scroll_from_element_to_element(self, from_element=None, to_element=None):
        self.driver.scroll(from_element, to_element)

    # noinspection PyBroadException
    def scroll_to_element(self, selector, from_x=100, from_y=900, to_x=100, to_y=400):
        page_source = self.driver.page_source
        while True:
            try:
                element = self.wait.wait_for_element_to_be_present(selector=selector, timeout=10)
                if element:
                    return element
            except Exception:
                self.driver.swipe(from_x, from_y, to_x, to_y)
                new = self.driver.page_source
                if new == page_source:
                    break
                page_source = new
        return False

    def scroll_to_end_of_page(self, from_x=100, from_y=900, to_x=100, to_y=400):
        page_source = self.driver.page_source
        while True:
            self.driver.swipe(from_x, from_y, to_x, to_y)
            new = self.driver.page_source
            if new == page_source:
                break
            page_source = new
