import os
import time
from appium_selenium_driver.appium_selenium_driver import Driver
from appium_selenium_driver.desired_capabilities.selenium_desired_capabilities import *
from appium_selenium_driver.report_tools.create_logs_dir import LogsDir
from appium_selenium_driver.report_tools.logcat_file_report import LogcatFile
# need this import for all classes that inheritance
from appium_selenium_driver.desired_capabilities.android_desired_capabilities import *
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from zapv2 import ZAPv2
# need this import for all classes that inheritance
from import_pages import *

# for android test locally
# if os.environ.get("LOCAL_TEST", None):
#     app_path = "C:\\Users\\elnatan\\Downloads\\emarald-debug.apk"
# else:
#     app_path = "{}/app/build/outputs/apk/emarald/debug/app-emarald-debug.apk".format(os.environ.get('WORKSPACE', None))

# make main log dir
log_reports = LogsDir(path_to_main_dir_log=os.environ.get('WORKSPACE', None))
log_reports.create_main_logs_dir()
site_url = os.getenv("SITE_URL")
# site_url = "https://test.ravtech.co.il"

# desired_caps = selenium_proxied_view
desired_caps = selenium_proxied_view
''''
example for android to add path of apk
desired_caps["app"] = emulator_desired_caps["app"].format(app_path)
'''


class BaseTestClass:
    # prox = Proxy()
    # prox.proxy_type = ProxyType.MANUAL
    # prox.http_proxy = "172.23.0.2:8081"
    # prox.socks_proxy = "172.23.0.2:8081"
    # prox.ssl_proxy = "172.23.0.2:8081"


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
        # log_reports.create_test_log_dir(dir_name=test_name)
        # self.logcat_file = LogcatFile(file_path=log_reports.current_test_dir)
        # self.logcat_file.open_logcat_file()

        # capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        #
        # self.prox.add_to_capabilities(capabilities)


        self.driver = Driver(address='http://selenium-server:4444/wd/hub', browser_profile="chrome",
                                 desired_capabilities=self.desired_caps)
        self.driver.driver.get(site_url)

    def teardown_method(self):
        # stop logcat process
        # self.logcat_file.stop_logcat()
        # stop webdriver for current test
        self.driver.driver.quit()
        self.run_zap()
        # check if need to remove test in case of success test
        # if self.remove_logs_dir:
        #     log_reports.remove_current_test_dir()

    def run_zap(self):
        proxy='172.23.0.2:8081'
        apikey = ""
        zap = ZAPv2(apikey=apikey,proxies={"http":"http://172.23.0.2:8081", "https": "http://172.23.0.2:8081"})
        alertThreshold = os.getenv("ALERT_THRESHOLD")
        attackStrength = os.getenv("ATTACK_STRENGTH")
        scan = zap.spider.scan(url="https://test.ravtech.co.il",recurse=True, apikey=apikey)
        zap.ascan.scan(url="https://test.ravtech.co.il",recurse=True, apikey=apikey)
        ascan = zap.ascan

        ascan.remove_scan_policy(scanpolicyname="my_policy"
                                     )

        ascan.add_scan_policy(scanpolicyname="my_policy")
        for policyId in range(0, 5):
                # Set alert Threshold for all scans
            ascan.set_policy_alert_threshold(id=policyId,
                                             alertthreshold=alertThreshold,
                                             scanpolicyname="my_policy")
                # Set attack strength for all scans
            ascan.set_policy_attack_strength(id=policyId,
                                             attackstrength=attackStrength,
                                             scanpolicyname="my_policy")
        # scanId = zap.ascan.scan(recurse=True, inscopeonly=None,
        #                         method=None, postdata=True)
        # print('Start Active scan. Scan ID equals ' + scanId)
        # while (int(zap.spider.status(id)) < 100):
        #     print('Active Scan progress: ' + zap.ascan.status(id) + '%')
        #     time.sleep(5)
        # print('Active Scan completed')

    # Give the passive scanner a chance to finish
        time.sleep(150)
        sample = zap.core.htmlreport()
        print(sample)
        with open('/selenium/reports/test.html', 'w', encoding="utf8") as f:
            f.write(sample)
