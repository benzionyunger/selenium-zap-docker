import os
from time import ctime
from pathlib import Path


class ElementsTools:

    def __init__(self, driver, wait_element):
        self.driver = driver
        self.wait = wait_element

    def wait_and_click(self, selector, driver=None, timeout=30):
        driver = driver or self.driver
        element = self.wait.wait_for_element_to_be_clickable(selector=selector, driver=driver, timeout=timeout)
        self.take_screenshot(driver=self.driver)
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
        filename = pic_path / "{}.png".format(filename) if filename else pic_path / "{}.png".\
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
