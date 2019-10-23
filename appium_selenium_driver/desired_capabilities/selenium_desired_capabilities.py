from selenium.webdriver.chrome.options import Options
import os
from   selenium import webdriver

selenium_mobile_view = {'browserName': 'chrome',
                                       'version': '',
                                       'platform': 'ANY',
                                       'chromeOptions': {
                                           'args': ['--headless', "--no-sandbox", "--disable-gpu"],
                                           'debuggerAddress': 'localhost: 5555',
                                           'mobileEmulation': {
                                               'deviceName': 'iPhone 6'
                                           },
                                           'extensions': [], 'args': []}
                                       }

selenium_mobile_view_for_lighthouse = {
                                        'browserName': 'chrome',
                                        'version': '',
                                        'platform': 'ANY',
                                        'goog:chromeOptions': {
                                           'mobileEmulation': {
                                               'deviceName': 'iPhone 6'
                                           },
                                            'extensions': [],
                                            'args': [
                                                'user-agent=I LIKE CHOCOLATE',
                                                f"--remote-debugging-port={os.environ.get('PORT', '5555')}",
                                                '--headless',
                                                '--disable-infobars',
                                                '--no-sandbox',
                                                '--disable-gpu'
                                            ]
                                        }
                                       }
zap_ip = os.getenv("ZAP_IP").strip("\n")
proxy_arg = f"--proxy-server={zap_ip}:8081"

selenium_proxied_view = {
                            'browserName': 'chrome',
                            'version': '',
                            'platform': 'ANY',
                            'acceptSslCerts':True,
                            'chromeOptions': {
                               'args': [
                                   '--headless',
                                   "--no-sandbox",
                                   "--disable-gpu",
                                   "--allow-running-insecure-content",
                                   "--ignore-certificate-errors",
                                   proxy_arg
                               ],
                               # 'debuggerAddress': 'localhost: 5555',
                               'extensions': []
                            }
}
