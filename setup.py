import os
import random
import string
import pickle
from selenium import webdriver
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, Popularity
import csv

class SetUp:
    selenium_hub = ""
    proxy_url = ""
    phone = ""
    email = ""
    username = ""
    password = ""
    proxy_urls = None
    logger = None

    def __init__(self, logger=logger, **kwargs):
        self.logger = logger
        if "selenium_hub" in kwargs:
            self.selenium_hub = kwargs['selenium_hub']
        if "proxy_url" in kwargs:
            self.proxy_url = kwargs['proxy_url']
        if "proxy_urls" in kwargs:
            self.proxy_urls = kwargs['proxy_urls']
        if "phone" in kwargs:
            self.phone = kwargs['phone']
        if "email" in kwargs:
            self.email = kwargs['email']
        if "username" in kwargs:
            self.username = kwargs['username']
        if "password" in kwargs:
            self.password = kwargs['password']

    def webdriver_init(self, Firefox=False):
        if Firefox is True:
            if self.proxy_url:
                proxy_url = self.proxy_url
            else:
                proxy_url = random.choice(self.proxy_urls)
            raw_input = proxy_url.split('//')
            proxy = raw_input[1].split(':')
            firefoxcaps = {
                'browserName': 'firefox',
                'marionette': True,
                'acceptInsecureCerts': True,
                'moz:firefoxOptions': {
                    'args': [],
                    'prefs': {
                        'browser.download.dir': '',
                        'browser.helperApps.neverAsk.saveToDisk': 'application/octet-stream,application/pdf',
                        'browser.download.useDownloadDir': True,
                        'browser.download.manager.showWhenStarting': False,
                        'browser.download.animateNotifications': False,
                        'browser.safebrowsing.downloads.enabled': False,
                        'browser.download.folderList': 2,
                        'pdfjs.disabled': True
                    }
                }
            }
            if proxy_url is not None:
                profile = webdriver.FirefoxProfile()
                profile.set_preference("network.proxy.type", 1)
                profile.set_preference("network.proxy.http", proxy[0])
                profile.set_preference("network.proxy.http_port", proxy[1])
                profile.set_preference("network.proxy.https", proxy[0])
                profile.set_preference("network.proxy.https_port", proxy[1])
                profile.update_preferences()
                return webdriver.Remote(self.selenium_hub, firefoxcaps, browser_profile=profile)
        else:
            option = webdriver.ChromeOptions()
            self.software_names = [SoftwareName.CHROME.value]
            self.operating_systems = [OperatingSystem.WINDOWS.value]
            self.useragentgenerator = UserAgent(software_names=self.software_names,
                                                operating_systems=self.operating_systems,
                                                popularity=[Popularity.POPULAR.value])
            option.add_argument("enable-automation")
            option.add_argument("--headless")
            option.add_argument("--window-size=1366,768")
            option.add_argument("--no-sandbox")
            option.add_argument("--disable-extensions")
            option.add_argument("--dns-prefetch-disable")
            option.add_argument("--ignore-certificate-errors")
            option.add_argument("--disable-gpu")
            option.add_argument(f'user-agent={self.useragentgenerator.get_random_user_agent()}')
            if self.proxy_url is not None or self.proxy_urls is not None:
                if self.proxy_url:
                    proxy = self.proxy_url
                else:
                    proxy = random.choice(self.proxy_urls)
                option.add_argument("--proxy-server={}".format(proxy))
            return webdriver.Remote(
                desired_capabilities=option.to_capabilities(),
                command_executor=self.selenium_hub)

    def save_cookie(self, driver, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(driver.get_cookies(), filehandler)

    def load_cookie(self, driver, path):
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)
        os.remove(path)

    def generate_csv(self, raws):
        path = '/tmp/{}.csv'.format(''.join(random.choice(string.ascii_lowercase) for i in range(4)))
        headers = {"Name": None, "Username": None, "Messages": None, "Links": None}
        try:
            with open(path, 'w', encoding='UTF8') as f:
                w = csv.DictWriter(f, headers.keys())
                w.writeheader()
                for raw_dict in raws:
                    w.writerow(raw_dict)
            return path
        except Exception as e:
            print(str(e))
            return 'Can\'t generate CSV'
