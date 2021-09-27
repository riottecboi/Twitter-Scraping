from setup import SetUp
import random
import string
from time import sleep

class Twitter(SetUp):

    def needPhone(self, driver):
        self.logger.info('Phone input challenge')
        self.logger.info('Send phone number')
        numbInput = driver.find_element_by_id('challenge_response')
        numbInput.clear()
        numbInput.send_keys(self.phone)
        inputBut = driver.find_element_by_id('email_challenge_submit')
        self.logger.info('Submit')
        inputBut.submit()

    def needUsername(self, driver):
        self.logger.info('Username input challenge')
        username = driver.find_element_by_name('session[username_or_email]')
        username.clear()
        self.logger.info('Send username input')
        username.send_keys(self.username)
        password = driver.find_element_by_name('session[password]')
        password.clear()
        self.logger.info('Send password')
        password.send_keys(self.password)
        login = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')
        self.logger.info('Submit')
        login.click()

    def search(self, link):
        path = '/tmp/{}.txt'.format(''.join(random.choice(string.ascii_lowercase) for i in range(4)))
        url = 'https://twitter.com/login'
        driver = super().webdriver_init()
        result = {'Name': None, 'Username': None, 'Messages': None, 'Links': link, 'Dead': None,'Scrapped by': self.username}
        seleniumerrors = 0
        anotherLogin = "To get started, first enter your phone, email, or @username"
        needUsername = "There was unusual login activity on your account. To help keep your account safe, please enter your phone number or username to verify it’s you."
        needPhone = 'Verify your identity by entering the phone number associated with your Twitter account.'
        while True:
            try:
                if link == "":
                    self.logger.info("No input given")
                    break
                driver.get(url)
                sleep(3)
                try:
                    Upage = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/header/div/div/div/div[2]/div/div')
                    Upage.click()
                    noNeedLogin = True
                except:
                    noNeedLogin = False
                if noNeedLogin is False:
                    self.logger.info('Get login')
                    if needPhone in driver.page_source:
                        # self.logger.info('Phone input challenge')
                        # self.logger.info('Send phone number')
                        # numbInput = driver.find_element_by_id('challenge_response')
                        # numbInput.clear()
                        # # numbInput.send_keys('212614634771')
                        # numbInput.send_keys(self.phone)
                        # inputBut = driver.find_element_by_id('email_challenge_submit')
                        # self.logger.info('Submit')
                        # inputBut.submit()
                        self.needPhone(driver)
                    else:
                        if anotherLogin in driver.page_source:
                            self.logger.info('Get started challenge')
                            self.logger.info('Send username input')
                            userinput = driver.find_element_by_name('username')
                            userinput.clear()
                            userinput.send_keys(self.username)
                            sleep(3)
                            inputb = driver.find_element_by_xpath(
                                '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div')
                            inputb.click()
                            self.logger.info('Next')
                            sleep(3)
                            if needUsername in driver.page_source:
                                self.needUsername(driver)
                            else:
                                passinput = driver.find_element_by_name('password')
                                passinput.clear()
                                passinput.send_keys(self.password)
                                self.logger.info('Password')
                                sleep(2)
                                subb = driver.find_element_by_xpath(
                                    '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div')
                                subb.click()
                                self.logger.info('Submit')
                        else:
                            self.logger.info('Normal input challenge')
                            username = driver.find_element_by_name('session[username_or_email]')
                            username.clear()
                            self.logger.info('Send email input')
                            username.send_keys(self.email)
                            password = driver.find_element_by_name('session[password]')
                            password.clear()
                            self.logger.info('Send password')
                            password.send_keys(self.password)
                            login = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')
                            self.logger.info('Submit')
                            login.click()
                    sleep(3)
                    if needPhone in driver.page_source:
                        # self.logger.info('Phone input challenge')
                        # self.logger.info('Send phone number')
                        # numbInput = driver.find_element_by_id('challenge_response')
                        # numbInput.clear()
                        # #numbInput.send_keys('212614634771')
                        # numbInput.send_keys(self.phone)
                        # inputBut = driver.find_element_by_id('email_challenge_submit')
                        # self.logger.info('Submit')
                        # inputBut.submit()
                        self.needPhone(driver)

                    if needUsername in driver.page_source:
                        # self.logger.info('Username input challenge')
                        # username = driver.find_element_by_name('session[username_or_email]')
                        # username.clear()
                        # self.logger.info('Send username input')
                        # #username.send_keys('GuessHorace')
                        # username.send_keys(self.username)
                        # password = driver.find_element_by_name('session[password]')
                        # password.clear()
                        # self.logger.info('Send password')
                        # #password.send_keys('yuPhieLa4d')
                        # password.send_keys(self.password)
                        # login = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')
                        # self.logger.info('Submit')
                        # login.click()
                        self.needUsername(driver)
                self.save_cookie(driver, path)
                self.load_cookie(driver, path)
                driver.get(link)
                self.logger.info('Get profile: {}'.format(link))
                if "This account doesn’t exist" in driver.page_source:
                    canMg = False
                    self.logger.info('This account no longer exist')
                    result = {'Name': None, 'Username': None, 'Messages': canMg, 'Links': link, 'Dead': True, 'Scrapped by': self.username}
                    break
                else:
                    try:
                        sleep(5)
                        raw_name = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div/span[1]/span')
                        name = raw_name.get_attribute('innerHTML')
                    except:
                        name = None
                    raw_username = driver.find_element_by_xpath(
                        '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div/span')
                    username = raw_username.get_attribute('innerHTML')

                    try:
                        check = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div/div/'
                                                             'div[2]/div/div/div[1]/div/div[1]/div/div[2]')
                        check.click()
                        sleep(3)
                        try:
                            available = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/'
                            'section[2]/div[2]/div/div/div/div/aside/div[2]/div[2]/div/div/div/div/label/div[2]/div/div/div')
                            available.click()
                            canMg = True
                            self.logger.info(f"This {link} profile available for message -- {canMg}")
                            result = {'Name': name, 'Username': username, 'Messages': canMg, 'Links': link, 'Dead': False,'Scrapped by': self.username}

                        except:
                            canMg = False
                            check.click()
                            self.logger.info(f"This {link} profile not available for message -- {canMg}")
                            result = {'Name': name, 'Username': username, 'Messages': canMg, 'Links': link, 'Dead': False,'Scrapped by': self.username}

                    except:
                        canMg = False
                        self.logger.info(f"This {link} profile not available for message -- {canMg}")
                        result = {'Name': name, 'Username': username, 'Messages': canMg, 'Links': link, 'Dead': False,'Scrapped by': self.username}
                    break

            except Exception as e:
                canMg = "Error"
                if "This account doesn’t exist" in driver.page_source:
                    canMg = False
                    self.logger.info('This account no longer exist')
                    result = {'Name': None, 'Username': None, 'Messages': canMg, 'Links': link, 'Dead': True, 'Scrapped by': self.username}
                    break
                self.logger.info("Error found")
                self.logger.info("Exception detected: {}".format(str(e)))
                seleniumerrors += 1
                if seleniumerrors > 3:
                    result = {'Name': None, 'Username': None, 'Messages': canMg, 'Links': link, 'Dead': None,'Scrapped by': self.username}
                    break
                else:
                    self.logger.info('{} try'.format(seleniumerrors))
                    continue

        driver.close()
        driver.quit()
        return result

    def get_profile_by_video_clip_link(self, link):
        results = []
        driver = super().webdriver_init()
        seleniumerrors = 0
        while True:
            try:
                if link == "":
                    self.logger.info("No input given")
                    break
                driver.get(link)
                sleep(3)
                self.logger.info('Got link {}'.format(link))
                profile_link = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/section[2]/div/div[1]/a').get_attribute('href')
                link = profile_link.replace('home', 'about')
                driver.get(link)
                self.logger.info('Going to profile-about: {}'.format(driver.current_url))
                links = driver.find_elements_by_class_name('tw-col')
                for l in links:
                    try:
                        a = l.find_element_by_tag_name('a').get_attribute('href')
                        if a is not None:
                            results.append(a)
                            self.logger.info('Collecting & appending {} to the list'.format(a))
                    except:
                        continue
                self.logger.info('Collecting & appending {} to the list'.format(driver.current_url))
                results.append(driver.current_url)
                self.logger.info('Collected total {} links'.format(len(results)))
                break

            except Exception as e:
                self.logger.info("Error found")
                self.logger.info("Exception detected: {}".format(str(e)))
                seleniumerrors += 1
                if seleniumerrors > 3:
                    self.logger.info('Failed - Exited')
                    break
                else:
                    self.logger.info('{} try'.format(seleniumerrors))
                    driver.close()
                    driver = super().webdriver_init()
                    continue
        driver.close()
        driver.quit()
        return results

    def get_profile_by_profile_link(self, link):
        results = []
        driver = super().webdriver_init()
        seleniumerrors = 0
        while True:
            try:
                if link == "":
                    self.logger.info("No input given")
                    break
                driver.get(link)
                sleep(3)
                cur_link = driver.current_url
                link = cur_link.split('https://')[1].split('/')
                updateLink = 'https://' + link[0] + '/' + link[1] + '/about'
                driver.get(updateLink)
                self.logger.info('Going to profile-about: {}'.format(driver.current_url))
                links = driver.find_elements_by_class_name('tw-col')
                for l in links:
                    try:
                        a = l.find_element_by_tag_name('a').get_attribute('href')
                        if a is not None:
                            results.append(a)
                            self.logger.info('Collecting & appending {} to the list'.format(a))
                    except:
                        continue
                self.logger.info('Collecting & appending {} to the list'.format(driver.current_url))
                results.append(driver.current_url)
                self.logger.info('Collected total {} links'.format(len(results)))
                break
            except Exception as e:
                self.logger.info("Error found")
                self.logger.info("Exception detected: {}".format(str(e)))
                seleniumerrors += 1
                if seleniumerrors > 3:
                    self.logger.info('Failed - Exited')
                    break
                else:
                    self.logger.info('{} try'.format(seleniumerrors))
                    driver.close()
                    driver = super().webdriver_init()
                    continue
        driver.close()
        driver.quit()
        return results

    def get_profile_by_directory_link(self, link, v2=False):
        results = []
        links = []
        driver = super().webdriver_init()
        seleniumerrors = 0
        while True:
            try:
                if link == "":
                    self.logger.info("No input given")
                    break
                driver.get(link)
                sleep(3)
                self.logger.info('Got link {}'.format(link))
                if v2 is False:
                    r = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div/div/div/div[4]/div[2]/div[1]/div[1]')
                    raw = r.find_elements_by_class_name('tw-link')
                else:
                    raw = driver.find_elements_by_class_name('ScCoreLink-sc-1t11s9q-0')
                for l in raw:
                    try:
                        li = l.find_element_by_class_name('tw-link')
                        lin = li.get_attribute('href')
                        lik = lin.replace('videos', 'about')
                        self.logger.info('Adding new profile link')
                        links.append(lik)
                    except:
                        continue
                for link in links:
                    driver.get(link)
                    self.logger.info('Going to profile-about: {}'.format(driver.current_url))
                    raws = driver.find_elements_by_class_name('tw-col')
                    for data in raws:
                        try:
                            a = data.find_element_by_tag_name('a').get_attribute('href')
                            if a is not None:
                                results.append(a)
                                self.logger.info('Collecting & appending {} to the list'.format(a))
                        except:
                            continue
                    self.logger.info('Collecting & appending {} to the list'.format(driver.current_url))
                    results.append(driver.current_url)

                break
            except Exception as e:
                self.logger.info("Error found")
                self.logger.info("Exception detected: {}".format(str(e)))
                seleniumerrors += 1
                if seleniumerrors > 3:
                    self.logger.info('Failed - Exited')
                    break
                else:
                    self.logger.info('{} try'.format(seleniumerrors))
                    driver.close()
                    driver = super().webdriver_init()
                    continue

        driver.close()
        driver.quit()
        return results
