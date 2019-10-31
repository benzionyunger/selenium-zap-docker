import os
import time
from pprint import pprint
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

# make main log dir
# log_reports = LogsDir(path_to_main_dir_log=os.environ.get('WORKSPACE', None))
# log_reports.create_main_logs_dir()

target = os.getenv("SITE_URL")
desired_caps = selenium_zap_proxy_view


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
        # log_reports.create_test_log_dir(dir_name=test_name)
        # self.logcat_file = LogcatFile(file_path=log_reports.current_test_dir)
        # self.logcat_file.open_logcat_file()

        self.driver = Driver(address='http://selenium-server:4444/wd/hub', browser_profile="chrome",
                                 desired_capabilities=self.desired_caps)
        self.driver.driver.get(target)

    def teardown_method(self):
        self.driver.driver.quit()
        self.run_zap()

        # stop logcat process
        # self.logcat_file.stop_logcat()
        # stop webdriver for current test
        # check if need to remove test in case of success test
        # if self.remove_logs_dir:
        #     log_reports.remove_current_test_dir()

    @staticmethod
    def run_zap():
        alertThreshold = os.getenv("ALERT_THRESHOLD")
        attackStrength = os.getenv("ATTACK_STRENGTH")
        desired_passive_scanners = os.getenv("PASSIVE_SCANNERS")
        desired_active_scanners = os.getenv("ACTIVE_SCANNERS")
        isWhiteListPolicy = os.getenv("WHITELIST_POLICY")
        print("desired variable is type " + str(type(desired_passive_scanners)))
        print("desirde active scanners -> "
              + desired_active_scanners)

        api_key=""
        proxy_address = 'http://zap:8081'
        isNewSession = True
        sessionName = 'Near Test Session'
        globalExcludeUrl = []
        useScanPolicy = True
        scanPolicyName = 'my_policy'
        pscanIds = []
        ascanIds=[]
        useAjaxSpider = True
        shutdownOnceFinished = False
        # useProxyChain = False
        # useProxyScript = False
        # useContextForScan = False
        # You can specify other URL in order to help ZAP discover more site locations
        # List can be empty
        # applicationURL = ['http://localhost:8081/WebGoat/start.mvc',
        #                   'http://localhost:8081/WebGoat/welcome.mvc',
        #                   'http://localhost:8081/WebGoat/attack']
        zap = ZAPv2(proxies={"http":proxy_address, "https": proxy_address}, apikey=api_key)

        all_pscan_scanners = zap.pscan.scanners
        for scanner in desired_passive_scanners:
            for pscanner in all_pscan_scanners:
                if scanner in pscanner['name']:
                    pscanIds.append(pscanner['id'])
        all_ascan_scanners = zap.ascan.scanners()
        for scanner in desired_active_scanners:
            for ascanner in all_ascan_scanners:
                if scanner in ascanner['name']:
                    ascanIds.append(ascanner['id'])

        core = zap.core
        if isNewSession:
            pprint('Create ZAP session: ' + sessionName + ' -> ' +
                   core.new_session(name=sessionName, overwrite=True))
        else:
            pprint('Load ZAP session: ' + sessionName + ' -> ' +
                   core.load_session(name=sessionName))

        # Configure ZAP global Exclude URL option
        print('Add Global Exclude URL regular expressions:')
        for regex in globalExcludeUrl:
            pprint(regex + ' ->' + core.exclude_from_proxy(regex=regex))

        # pprint('Enable all passive scanners -> ' +
        #        zap.pscan.enable_all_scanners())

        pprint('Enabling given passive scanner ids -> ' +
               zap.pscan.enable_scanners(pscanIds))
        ascan = zap.ascan

        if useScanPolicy:
            ascan.remove_scan_policy(scanpolicyname=scanPolicyName)
            pprint('Add scan policy ' + scanPolicyName + ' -> ' +
                   ascan.add_scan_policy(scanpolicyname=scanPolicyName))
            for policyId in range(0, 5):
                # Set alert Threshold for all scans
                ascan.set_policy_alert_threshold(id=policyId,
                                                 alertthreshold=alertThreshold,
                                                 scanpolicyname=scanPolicyName)
                # Set attack strength for all scans
                ascan.set_policy_attack_strength(id=policyId,
                                                 attackstrength=attackStrength,
                                                 scanpolicyname=scanPolicyName)
            if isWhiteListPolicy:
                # Disable all active scanners in order to enable only what you need
                pprint('Disable all scanners -> ' +
                       ascan.disable_all_scanners(scanpolicyname=scanPolicyName))
                # Enable some active scanners
                pprint('Enable given scan IDs -> ' +
                       ascan.enable_scanners(ids=ascanIds,
                                             scanpolicyname=scanPolicyName))
            else:
                # Enable all active scanners
                pprint('Enable all scanners -> ' +
                       ascan.enable_all_scanners(scanpolicyname=scanPolicyName))
                # Disable some active scanners
                pprint('Disable given scan IDs -> ' +
                       ascan.disable_scanners(ids=ascanIds,
                                              scanpolicyname=scanPolicyName))
        else:
            print('No custom policy used for scan')
            scanPolicyName = None

        spider = zap.spider
        ajax = zap.ajaxSpider
        scanId = 0
        print('Starting Scans on target: ' + target)

        scanId = spider.scan(url=target, maxchildren=None, recurse=True,
                             contextname=None, subtreeonly=None)
        print('Scan ID equals ' + scanId)
        # Give the Spider a chance to start
        time.sleep(2)
        while (int(spider.status(scanId)) < 100):
            print('Spider progress ' + spider.status(scanId) + '%')
            time.sleep(2)
        print('Spider scan completed')
        if useAjaxSpider:
            # Ajax Spider the target URL
            pprint('Start Ajax Spider -> ' + ajax.scan(url=target, inscope=None))
            # Give the Ajax spider a chance to start
            time.sleep(10)
            while (ajax.status != 'stopped'):
                print('Ajax Spider is ' + ajax.status)
                time.sleep(5)
            # for url in applicationURL:
            #     # Ajax Spider every url configured
            #     pprint('Ajax Spider the URL: ' + url + ' -> ' +
            #            ajax.scan(url=url, inscope=None))
            #     # Give the Ajax spider a chance to start
            #     time.sleep(10)
            #     while (ajax.status != 'stopped'):
            #         print('Ajax Spider is ' + ajax.status)
            #         time.sleep(5)
            print('Ajax Spider scan completed')

        scanId = zap.ascan.scan(url=target, recurse=True, inscopeonly=None,
                                scanpolicyname=scanPolicyName, method=None, postdata=True)
        print('Start Active scan. Scan ID equals ' + scanId)
        while (int(ascan.status(scanId)) < 100):
            print('Active Scan progress: ' + ascan.status(scanId) + '%')
            time.sleep(5)
        print('Active Scan completed')

        time.sleep(10)

        # If you want to retrieve alerts:
        ## pprint(zap.core.alerts(baseurl=target, start=None, count=None))

        # To retrieve ZAP report in XML or HTML format
        ## print('XML report')
        ## core.xmlreport()
        print('HTML report:')
        test_report = core.htmlreport()
        pprint(test_report)
        with open('/selenium/reports/test.html', 'w', encoding="utf8") as f:
            f.write(test_report)


        if shutdownOnceFinished:
            # Shutdown ZAP once finished
            pprint('Shutdown ZAP -> ' + core.shutdown())


# ***************************************
#         scan = zap.spider.scan(url=target,recurse=True)
#
#         zap.ascan.scan(url=os.getenv("SITE_URL"),recurse=True)
#         ascan = zap.ascan
#
#         # for id in range(0, 5):
#         #     ascan.set_scanner_alert_threshold(id=id, alertthreshold=alertThreshold)
#         #     ascan.set_scanner_attack_strength(id=id, attackstrength=attackStrength)
#
#         for policyID in range(0,5):
#             ascan.set_policy_alert_threshold(id=policyID,alertthreshold=alertThreshold,scanpolicyname="my_policy",apikey="")
#             ascan.set_scanner_attack_strength(id=policyID,attackstrength=attackStrength,scanpolicyname="my_policy",apikey="")
#
#         # scanId = zap.ascan.scan(recurse=True, inscopeonly=None,
#         #                         method=None, postdata=True)
#         # print('Start Active scan. Scan ID equals ' + scanId)
#         # while (int(zap.spider.status(id)) < 100):
#         #     print('Active Scan progress: ' + zap.ascan.status(id) + '%')
#         #     time.sleep(5)
#         # print('Active Scan completed')
#
#     # Give the passive scanner a chance to finish
#         time.sleep(20)
#         zap.core.htmlreport()
#         sample = zap.core.htmlreport()
#         # print(sample)
#         if(sample):
#             print("An HTML report has been successfully produced and can be found in the zap container's \'/reports\' "
#                   "folder and in the local project's \'zap_reports\' folder.")
#         else:
#             print("A report has not been produced, please check for errors in the zap container's /home/zap/.ZAP_D/logs/"
#                   " folder for possible errors.")
