from tests.example_base_test_class import *

desired_caps = emulator_desired_caps
desired_caps["app"] = app_path


class TestLoginExample(ExampleBaseTestClass):
    desired_caps = desired_caps

    def test_login_success(self):
        self.success_login()
        self.driver.tools.get_text_from_element(ExamplePage.user_added_msg)
        self.driver.tools.wait_and_click(ExamplePage.user_Added_done_btn)

    def test_login_failed_wrong_url(self):
        self.driver.tools.wait_and_click(ExamplePage.permission_allow_btn)
        self.driver.tools.wait_and_click(ExamplePage.add_user_btn)
        self.driver.tools.set_text(ExamplePage.factory_name, "dev")
        self.driver.tools.set_text(ExamplePage.factory_url, "ved")
        self.driver.tools.set_text(ExamplePage.user_name, "ravtech2")
        self.driver.tools.set_text(ExamplePage.password, "ravtech@1")
        self.driver.tools.wait_and_click(ExamplePage.done_btn)
        assert self.driver.wait.wait_for_element_to_be_present(ExamplePage.login_error_msg)
        # assert 'No communication' in self.driver.tools.get_text_from_element(LoginPage.login_error_msg)
