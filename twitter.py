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
        result = {'Name': None, 'Username': None, 'Messages': None, 'Links': link, 'Dead': None}
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
                    result = {'Name': None, 'Username': None, 'Messages': canMg, 'Links': link, 'Dead': True}
                    break
                else:
                    try:
                        raw_name = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[1]'
                                                                '/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div/span[1]/span')
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
                            result = {'Name': name, 'Username': username, 'Messages': canMg, 'Links': link, 'Dead': False}

                        except:
                            canMg = False
                            check.click()
                            self.logger.info(f"This {link} profile not available for message -- {canMg}")
                            result = {'Name': name, 'Username': username, 'Messages': canMg, 'Links': link, 'Dead': False}

                    except:
                        self.logger.info(str(e))
                        canMg = False
                        self.logger.info(f"This {link} profile not available for message -- {canMg}")
                        result = {'Name': name, 'Username': username, 'Messages': canMg, 'Links': link, 'Dead': False}
                    break

            except Exception as e:
                canMg = "Error"
                self.logger.info("Error found")
                self.logger.info("Exception detected: {}".format(str(e)))
                seleniumerrors += 1
                if seleniumerrors > 3:
                    result = {'Name': None, 'Username': None, 'Messages': canMg, 'Links': link, 'Dead': None}
                    break
                else:
                    self.logger.info('{} try'.format(seleniumerrors))
                    continue

        driver.close()
        driver.quit()
        return result
