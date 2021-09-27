import os
import random
import json
import pickle
from selenium import webdriver
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, Popularity
import csv
from mega import Mega
from datetime import datetime
import string
class SetUp:
    selenium_hub = ""
    proxy_url = None
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
            if self.proxy_urls is not None or self.proxy_url is not None:
                if self.proxy_url:
                    proxy_url = self.proxy_url
                else:
                   proxy_url = random.choice(self.proxy_urls)
                raw_input = proxy_url.split('//')
                proxy = raw_input[1].split(':')
                profile = webdriver.FirefoxProfile()
                profile.set_preference("network.proxy.type", 1)
                profile.set_preference("network.proxy.http", proxy[0])
                profile.set_preference("network.proxy.http_port", proxy[1])
                profile.set_preference("network.proxy.https", proxy[0])
                profile.set_preference("network.proxy.https_port", proxy[1])
                profile.update_preferences()
                return webdriver.Remote(self.selenium_hub, firefoxcaps, browser_profile=profile)
            else:
                return webdriver.Remote(self.selenium_hub, firefoxcaps)

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
                    print('Using proxy: {}'.format(proxy))
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
        date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S")
        path = '/tmp/data_{}.csv'.format(date)
        headers = {"Name": None, "Username": None, "Messages": None, "Links": None, "Dead": None, 'Scrapped by': None}
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

    def get_list_links(self, path):
        myfile = open(path, 'r')
        contents = myfile.readlines()
        links = []
        for content in contents:
            links.append(content.strip())
        return links

    def download_mg_file(self, **kwargs):
        mega = Mega()
        path = kwargs['path']
        try:
            m = mega.login(kwargs['mg_email'], kwargs['mg_password'])
            print('Login success')
            print('Downloading profile links...')
            f = m.find(kwargs['file'])
            m.download(f, path)
            print('Downloaded')
            ret = f"{path}/{kwargs['file']}"
        except Exception as e:
            ret = str(e)
        return ret

    def sync_to_mega(self, filename, delete=False, **kwargs):
        mega = Mega()
        try:
            m = mega.login(kwargs['mg_email'], kwargs['mg_password'])
            print('Login success')
            u = m.get_user()
            print('Hi ! {}'.format(u['name']))
            storage = m.get_storage_space(giga=True)
            print('Current account storage space: {}/{} Gb'.format(round(storage['used']), storage['total']))
            try:
                if delete is True:
                    f = filename.split('/')
                    file = f[1]
                    delete_file = m.find(file)
                    m.delete(delete_file[0])
                destination = m.find(kwargs['folder'])
                f = m.upload(filename, destination[0])
                getDetails = m.get_upload_link(f)
                print('This file is uploaded to folder - {}'.format(kwargs['folder']))
                print('Get public link file: {}'.format(getDetails))
                ret = str(getDetails)

            except:
                print('This folder not exist')
                f = m.upload(filename)
                getDetails = m.get_upload_link(f)
                print('Get public link file: {}'.format(getDetails))
                ret = str(getDetails)
        except Exception as e:
            print(str(e))
            ret = str(e)
        return ret

    def distributed_links(self, **kwargs):
        try:
            filenames=[]
            download=self.download_mg_file(**kwargs)
            for i in range(1, 22):
                list_remove = []
                links = 0
                list_return = self.get_list_links(download)
                if len(list_return) > 0:
                    dis_file = 'links/{}.txt'.format(''.join(random.choice(string.ascii_lowercase) for i in range(4)))
                    with open(dis_file, 'w') as f1:
                        for link in list_return:
                            if links <= 50:
                                f1.write(link + "\n")
                                list_remove.append(link)
                                links += 1
                        for remove in list_remove:
                            list_return.remove(remove)

                        new_file = open("links.txt", "w")
                        for update in list_return:
                            new_file.write(update + "\n")
                        new_file.close()
                    f1.close()
                    filenames.append(dis_file)
                else:
                    break
            ret = filenames
        except Exception as e:
            ret=str(e)
        return ret

    def download_mg_conf_file(self, **kwargs):
        mega = Mega()
        path = kwargs['configure_path']
        try:
            m = mega.login(kwargs['mg_email'], kwargs['mg_password'])
            print('Login success')
            print('Downloading profile links...')
            f = m.find(kwargs['configure_file'])
            m.download(f, path)
            print('Downloaded')
            ret = f"{path}/{kwargs['configure_file']}"
        except Exception as e:
            ret = str(e)
        return ret

    def distributed_configures(self, **kwargs):
        try:
            filenames=[]
            download = self.download_mg_conf_file(**kwargs)
            with open(download, encoding='utf-8') as json_data_file:
                file = json.load(json_data_file)
            numb = 0
            for conf in file['configures']:
                dis_file = 'configures/{}-config.json'.format(numb)
                with open(dis_file, 'w') as f1:
                    f1.write(json.dumps(conf))
                    f1.close()
                filenames.append(dis_file)
                numb+=1
            os.remove(download)
            ret = filenames
        except Exception as e:
            ret=str(e)
        return ret

    def update_data_csv(self, datas):
        results = []
        des_file = 'raw/data.json'
        with open(des_file, encoding='utf-8') as json_data_file:
            raw = json.load(json_data_file)
        for r in raw:
            results.append(r)
        results.append(datas)
        #results.extend(datas)
        with open(des_file, 'w') as f1:
            f1.write(json.dumps(results))
            f1.close()
        print('Updated')

    def write_file(self, path, list_return):
        new_file = open(path, "w")
        for update in list_return:
            new_file.write(update + "\n")
        new_file.close()
        return path

