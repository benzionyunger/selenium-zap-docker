import os

from android_appium_driver.android_driver import AndroidDriver
from android_appium_driver.report_tools.create_logs_dir import LogsDir
from android_appium_driver.report_tools.logcat_file_report import LogcatFile
from import_pages import *

if os.environ.get("LOCAL_TEST", None):
    app_path = "C:\\Users\\elnatan\\Downloads\\emarald-debug.apk"
else:
    app_path = "{}/app/build/outputs/apk/emarald/debug/app-emarald-debug.apk".format(os.environ.get('WORKSPACE', None))

# make main log dir
log_reports = LogsDir(path_to_main_dir_log=os.environ.get('WORKSPACE', None))
log_reports.create_main_logs_dir()
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# desired_caps = {'platformName': 'Android',
#                 'platformVersion': '6.0',
#                 'deviceName': 'Android Emulator',
#                 'app': app_path,
#                 'appPackage': 'com.leadermes.managerapp',
#                 'appActivity': 'com.leadermes.emerald.activities.MainActivity'}

desired_caps = {
    "browserName": "chrome",
    "version": "",
    'app': "C:\\Users\\elnatan\\Desktop\\chromedriver_win32\\chromedriver.exe",
    "platformName": "windows",
    "platform": "ANY",
    'deviceName': 'WindowsPC',
}


class TestLogin(object):
    """
    # only android
    logcat_file = None
    """
    driver = None

    def setup(self):
        pass

    def setup_method(self, method):
        test_name = method.__name__
        # make current test logs and screenshots dir
        log_reports.create_test_log_dir(dir_name=test_name)
        # create and open logcat file with filter option
        """
            only android
            self.logcat_file = LogcatFile(file_path=log_reports.current_test_dir,
                                      filter_by="replace with what you want package.....")
            self.logcat_file.open_logcat_file()
        """

        # start webdriver for current test
        self.driver = AndroidDriver(desired_capabilities=desired_caps, browser_profile="chrome", remote=False)
        # self.driver.driver.get("https://www.google.co.il/")

    def teardown_method(self):
        """
        # stop logcat process
        self.logcat_file.stop_logcat()
        stop webdriver for current test

        """
        # stop webdriver for current test
        self.driver.driver.close()

    def test_example_test(self):
        self.driver.tools.wait_and_click(ExamplePage.first)
        # self.driver.tools.wait_and_click(ExamplePage.add_user_btn)
        # self.driver.tools.set_text(ExamplePage.factory_name, "dev")
        # self.driver.tools.set_text(ExamplePage.factory_url, "ved")
        # self.driver.tools.set_text(ExamplePage.user_name, "ravtech2")
        # assert self.driver.wait.wait_for_element_to_be_present(ExamplePage.login_error_msg)
