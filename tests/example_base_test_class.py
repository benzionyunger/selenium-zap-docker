from appium_selenium_driver.base_test_class import *

desired_caps = emulator_desired_caps
desired_caps["app"] = app_path


class ExampleBaseTestClass(BaseTestClass):
    desired_caps = desired_caps

    # pre conditions for tests to all classes
    def success_login(self):
        self.driver.tools.wait_and_click(ExamplePage.permission_allow_btn)
        self.driver.tools.wait_and_click(ExamplePage.add_user_btn)
        self.driver.tools.set_text(ExamplePage.factory_name, "dev")
        self.driver.tools.set_text(ExamplePage.factory_url, "dev")
        self.driver.tools.set_text(ExamplePage.user_name, "ravtech2")
        self.driver.tools.set_text(ExamplePage.password, "ravtech@1")
        self.driver.tools.wait_and_click(ExamplePage.done_btn)
        self.driver.tools.wait_and_click(ExamplePage.user_Added_done_btn)

    def success_login_and_get_online_tab(self):
        self.success_login()
        self.driver.tools.wait_and_click(ExamplePage.pie_btn)

    def success_login_and_get_shift_tab(self):
        self.success_login_and_get_online_tab()
        self.driver.tools.wait_and_click(ExamplePage.shift_report_tab)
