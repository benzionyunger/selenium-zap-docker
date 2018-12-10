import os

from appium_selenium_driver.appium_selenium_driver import Driver
from appium_selenium_driver.report_tools.create_logs_dir import LogsDir
from appium_selenium_driver.report_tools.logcat_file_report import LogcatFile
# need this import for all classes that inheritance
from appium_selenium_driver.desired_capabilities.android_desired_capabilities import *
# need this import for all classes that inheritance
from import_pages import *
# for android test locally
if os.environ.get("LOCAL_TEST", None):
    app_path = "C:\\Users\\elnatan\\Downloads\\emarald-debug.apk"
else:
    app_path = "{}/app/build/outputs/apk/emarald/debug/app-emarald-debug.apk".format(os.environ.get('WORKSPACE', None))

# make main log dir
log_reports = LogsDir(path_to_main_dir_log=os.environ.get('WORKSPACE', None))
log_reports.create_main_logs_dir()

desired_caps = "....select from desired_capabilities file...."
''''

example for android to add path of apk
desired_caps["app"] = emulator_desired_caps["app"].format(app_path)
'''


class BaseTestClass:
    logcat_file = None
    driver = None
    # you need to override this parameter on inheritance
    desired_caps = desired_caps

    def setup(self):
        pass

    def setup_method(self, method):
        test_name = method.__name__
        # make current test logs and screenshots dir
        log_reports.create_test_log_dir(dir_name=test_name)
        # create and open logcat file with filter option
        self.logcat_file = LogcatFile(file_path=log_reports.current_test_dir, filter_by="replace with what you want "
                                                                                        "package.....")
        self.logcat_file.open_logcat_file()
        # start webdriver for current test
        self.driver = Driver(desired_capabilities=desired_caps)

    def teardown_method(self):
        # stop logcat process
        self.logcat_file.stop_logcat()
        # stop webdriver for current test
        self.driver.driver.quit()
