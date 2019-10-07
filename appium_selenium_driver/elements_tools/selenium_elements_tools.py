import os
from pathlib import Path
from time import ctime


class SeleniumElementsTools:

    def __init__(self, driver, wait_element):
        self.driver = driver
        self.wait = wait_element

    def wait_and_click(self, selector, driver=None, timeout=60, raise_exception=True):
        driver = driver or self.driver
        element = self.wait.wait_for_element_to_be_clickable(selector=selector, driver=driver, timeout=timeout,
                                                             raise_exception=raise_exception)
        self.take_screenshot(driver=self.driver)
        if element:
            return element.click()

    def wait_and_js_click(self, selector, driver=None, timeout=60, raise_exception=True):
        driver = driver or self.driver
        element = self.wait.wait_for_element_to_be_clickable(selector=selector, driver=driver, timeout=timeout,
                                                             raise_exception=raise_exception)
        self.take_screenshot(driver=self.driver)
        if element:
            return driver.execute_script("arguments[0].click();", element)

    def click_on_web_element_by_js(self, web_element, driver=None):
        driver = driver or self.driver
        self.take_screenshot(driver=self.driver)
        return driver.execute_script("arguments[0].click();", web_element)

    def get_text_from_element(self, selector, driver=None, timeout=60):
        driver = driver or self.driver
        element_text = self.wait.wait_for_element_to_be_present(selector=selector, driver=driver, timeout=timeout).text
        self.take_screenshot(driver=self.driver)
        return element_text

    def set_text(self, selector, text, driver=None, timeout=60):
        driver = driver or self.driver
        element = self.wait.wait_for_element_to_be_present(selector=selector, driver=driver, timeout=timeout)
        element.send_keys(text)
        self.take_screenshot(driver=self.driver)

    def scroll_to_top(self, driver=None):
        driver = driver or self.driver
        self.take_screenshot(driver=self.driver)
        return driver.execute_script("document.body.scrollTop = 0;"), \
               driver.execute_script("document.documentElement.scrollTop = 0;")

    def scroll_into_view(self, selector, driver=None, timeout=60):
        driver = driver or self.driver
        self.take_screenshot(driver=self.driver)
        element = self.wait.wait_for_element_to_be_present(selector=selector, driver=driver, timeout=timeout)
        return driver.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_into_view_by_web_element(self, web_element, driver=None):
        driver = driver or self.driver
        self.take_screenshot(driver=self.driver)
        return driver.execute_script("arguments[0].scrollIntoView();", web_element)

    @staticmethod
    def take_screenshot(driver, filename=None):
        pic_path = Path(os.environ.get('CURRENT_LOGS_DIR', '_'.join(ctime().replace(':', '.').split())))
        filename = pic_path / "{}.png".format(filename) if filename else pic_path / "{}.png". \
            format('_'.join(ctime().replace(':', '.').split()))
        driver.save_screenshot(filename=str(filename))

    def make_list_of_strings_from_elements(self, selector, driver=None, timeout=60):
        driver = driver or self.driver
        elements = self.wait.wait_for_elements_to_be_present(selector=selector, driver=driver, timeout=timeout)
        elements_text = []
        for element in elements:
            elements_text.append(element.text)
        return elements_text

    def element_contain_text(self, text, selector, driver=None, timeout=60):
        driver = driver or self.driver
        if text in self.wait.wait_for_element_to_be_present(selector=selector, driver=driver, timeout=timeout).text:
            self.take_screenshot(driver=self.driver)
            return True
        return False

    # work only with appium driver not selenium
    def scroll_from_element_to_element_by_selector(self, from_element_selector=None, to_element_selector=None):
        # TODO make this func for selenium
        pass

    # work only with appium driver not selenium
    def scroll_from_element_to_element(self, from_element=None, to_element=None):
        # TODO make this func for selenium
        pass

    # noinspection PyBroadException
    def scroll_to_element(self, selector, from_x=100, from_y=900, to_x=100, to_y=400):
        # TODO make this func for selenium
        pass

    def scroll_to_end_of_page(self, from_x=100, from_y=900, to_x=100, to_y=400):
        # TODO make this func for selenium
        pass
