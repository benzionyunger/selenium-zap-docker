from appium_selenium_driver.base_test_class import *

desired_caps = selenium_zap_proxy_view


class TestBase(BaseTestClass):
    desired_caps = desired_caps

    def test_login(self):
        self.driver.tools.set_text(HomeSelectors.username_field, "dev")
        self.driver.tools.set_text(HomeSelectors.password_field, "1q2w3e4r5t")
        self.driver.tools.wait_and_js_click(HomeSelectors.submit_btn)
        self.driver.wait.wait_for_element_to_be_present(DashboardPage.menu)