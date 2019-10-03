import os

from appium_selenium_driver.appium_selenium_driver import Driver
from appium_selenium_driver.desired_capabilities.selenium_desired_capabilities import selenium_proxied_view
from appium_selenium_driver.report_tools.create_logs_dir import LogsDir
from appium_selenium_driver.report_tools.logcat_file_report import LogcatFile
# need this import for all classes that inheritance
from appium_selenium_driver.desired_capabilities.android_desired_capabilities import *
from selenium.webdriver.common.proxy import Proxy, ProxyType
from zapv2 import ZAPv2

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

desired_caps = selenium_proxied_view
''''

example for android to add path of apk
desired_caps["app"] = emulator_desired_caps["app"].format(app_path)
'''
prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = "http://zap:8081"
prox.socks_proxy = "http://zap:8081"
prox.ssl_proxy = "http://zap:8081"

class BaseTestClass:
    logcat_file = None
    driver = None
    # you need to override this parameter on inheritance

    desired_caps = desired_caps
    # if remove logs and screenshots dir of current test(in case of success test)
    remove_logs_dir = False

    def setup(self):
        pass

    def setup_method(self, method):
        test_name = method.__name__
        # make current test logs and screenshots dir
        log_reports.create_test_log_dir(dir_name=test_name)
        self.logcat_file = LogcatFile(file_path=log_reports.current_test_dir, filter_by="leadermes")
        self.logcat_file.open_logcat_file()

        prox.add_to_capabilities(self.desired_caps)

        self.driver = Driver(address='http://selenium-server:4444/wd/hub', browser_profile="chrome",
                                 desired_capabilities=self.desired_caps)

    def teardown_method(self):
        # stop logcat process
        self.logcat_file.stop_logcat()
        # stop webdriver for current test
        self.driver.driver.quit()
        # check if need to remove test in case of success test
        if self.remove_logs_dir:
            log_reports.remove_current_test_dir()

    def run_zap(self):
        proxy='http://zap:8081'
        # apikey = ""
        zap = ZAPv2(proxies=proxy)
        zap.spider.scan()
        sample = zap.core.htmlreport()
        print(sample)
        with open('test.html', 'w', encoding="utf8") as f:
            f.write(sample)
