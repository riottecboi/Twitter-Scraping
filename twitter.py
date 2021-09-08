from setup import SetUp
import random
import string
from time import sleep

class Twitter(SetUp):

    def search(self, link):
        path = '/tmp/{}.txt'.format(''.join(random.choice(string.ascii_lowercase) for i in range(4)))
        url = 'https://twitter.com/login'
        driver = super().webdriver_init(Firefox=True)
        seleniumerrors = 0
        result = {'Name': None, 'Username': None, 'Messages': False, 'Links': link}
        needUsername = "There was unusual login activity on your account. To help keep your account safe, please enter your phone number or username to verify it’s you."
        needPhone = 'Verify your identity by entering the phone number associated with your Twitter account.'
        while True:
            try:
                if link == "":
                    self.logger.info("No input given")
                    break
                driver.get(url)
                sleep(3)
                self.logger.info('Send the profile links: {}'.format(link))
                if needPhone in driver.page_source:
                    self.logger.info('Phone input challenge')
                    self.logger.info('Send phone number')
                    numbInput = driver.find_element_by_id('challenge_response')
                    numbInput.clear()
                    # numbInput.send_keys('212614634771')
                    numbInput.send_keys(self.phone)
                    inputBut = driver.find_element_by_id('email_challenge_submit')
                    self.logger.info('Submit')
                    inputBut.submit()
                else:
                    self.logger.info('Normal input challenge')
                    username = driver.find_element_by_name('session[username_or_email]')
                    username.clear()
                    self.logger.info('Send email input')
                    # username.send_keys('horace.tguess@gmail.com')
                    username.send_keys(self.email)
                    password = driver.find_element_by_name('session[password]')
                    password.clear()
                    self.logger.info('Send password')
                    # password.send_keys('yuPhieLa4d')
                    password.send_keys(self.password)
                    login = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')
                    self.logger.info('Submit')
                    login.click()
                sleep(3)
                if needPhone in driver.page_source:
                    self.logger.info('Phone input challenge')
                    self.logger.info('Send phone number')
                    numbInput = driver.find_element_by_id('challenge_response')
                    numbInput.clear()
                    #numbInput.send_keys('212614634771')
                    numbInput.send_keys(self.phone)
                    inputBut = driver.find_element_by_id('email_challenge_submit')
                    self.logger.info('Submit')
                    inputBut.submit()

                if needUsername in driver.page_source:
                    self.logger.info('Username input challenge')
                    username = driver.find_element_by_name('session[username_or_email]')
                    username.clear()
                    self.logger.info('Send username input')
                    #username.send_keys('GuessHorace')
                    username.send_keys(self.username)
                    password = driver.find_element_by_name('session[password]')
                    password.clear()
                    self.logger.info('Send password')
                    #password.send_keys('yuPhieLa4d')
                    password.send_keys(self.password)
                    login = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')
                    self.logger.info('Submit')
                    login.click()

                self.save_cookie(driver, path)
                self.load_cookie(driver, path)
                driver.get(link)
                self.logger.info('Get profile: {}'.format(link))
                if "This account doesn’t exist" in driver.page_source:
                    canMg = False
                    self.logger.info('This account no longer exist')
                    result = {'Name': None, 'Username': None, 'Messages': canMg, 'Links': link}
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
                            result = {'Name': name, 'Username': username, 'Messages': canMg, 'Links': link}

                        except Exception as e:
                            self.logger.info(str(e))
                            canMg = False
                            check.click()
                            self.logger.info(f"This {link} profile not available for message -- {canMg}")
                            result = {'Name': name, 'Username': username, 'Messages': canMg, 'Links': link}

                    except Exception as e:
                        self.logger.info(str(e))
                        canMg = False
                        self.logger.info(f"This {link} profile not available for message -- {canMg}")
                        result = {'Name': name, 'Username': username, 'Messages': canMg, 'Links': link}
                    break

            except Exception as e:
                canMg = False
                self.logger.info("Error found")
                self.logger.info("Exception detected: {}".format(str(e)))
                seleniumerrors += 1
                if seleniumerrors > 3:
                    result = {'Name': None, 'Username': None, 'Messages': canMg, 'Links': link}
                    break
                else:
                    self.logger.info('{} try'.format(seleniumerrors))
                    continue

        #driver.close()
        driver.quit()
        return result