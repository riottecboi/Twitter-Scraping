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

    def needEmail(self, driver):
        self.logger.info('Email input challenge')
        username = driver.find_element_by_name('text')
        username.clear()
        self.logger.info('Send email input')
        username.send_keys(self.email)
        inputb = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div')
        inputb.click()
        password = driver.find_element_by_name('password')
        password.clear()
        self.logger.info('Send password')
        password.send_keys(self.password)
        login = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div')
        login.click()
        self.logger.info('Submit')

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

    def get_followers(self, driver):
        users = []
        list_followers = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/section/div')
        href = list_followers.find_elements_by_tag_name('a')
        for username in href:
            l = username.get_attribute('href')
            if 'search?q=' in l or 't.co' in l:
                continue
            users.append(l)
        return users

    def search(self, link, followers=False):
        follower = []
        f = []
        crashed = False
        path = '/tmp/{}.txt'.format(''.join(random.choice(string.ascii_lowercase) for i in range(4)))
        url = 'https://twitter.com/login'
        driver = super().webdriver_init()
        driver.find_elements_by_tag_name('a')
        result = {'Name': None, 'Username': None, 'Messages': None, 'Links': link, 'Dead': None,'Scrapped by': self.username}
        seleniumerrors = 0
        errors = 0
        anotherLogin = "To get started, first enter your phone, email, or @username"
        needUsername = "There was unusual login activity on your account. To help keep your account safe, please enter your phone number or username to verify it’s you."
        needPhone = 'Verify your identity by entering the phone number associated with your Twitter account.'
        needEmail = "There was unusual login activity on your account. To help keep your account safe, please enter your phone number or email address to verify it’s you."
        error = 'Something went wrong, but don\'t fret'
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
                            elif needEmail in driver.page_source:
                                self.needEmail(driver)
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
                    if needPhone in driver.page_source and 'Hint: ending in' in driver.page_source:
                        crashed = True
                        self.logger.info('Need to phone verification for {}'.format(self.username))
                        result = {'Name': None, 'Username': None, 'Messages': 'Need phone verification', 'Links': link, 'Dead': None,
                                  'Scrapped by': self.username}
                        break

                    if needPhone in driver.page_source:
                        self.needPhone(driver)

                    if needUsername in driver.page_source:
                        self.needUsername(driver)
                self.save_cookie(driver, path)
                self.load_cookie(driver, path)
                if followers is True:
                    self.logger.info('Get number of followers from {}'.format(link))
                    driver.get(link)
                    get_followers = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[1]/div/div[5]/div[2]/a/span[1]/span')
                    raw_followers = get_followers.text
                    if len(raw_followers) > 1 and 'K' in raw_followers:
                        numb_followers = float(raw_followers.replace('K', '')) * 1000
                    else:
                        numb_followers = float(raw_followers.replace(',', '.')) * 1000
                    link = link + '/followers'
                    driver.get(link)
                    self.logger.info('Collecting {} follower\'s accounts'.format(numb_followers))
                    sleep(3)
                    last_height = driver.execute_script('return window.pageYOffset')
                    self.logger.info('Last height: {}'.format(last_height))
                    self.logger.info('Updating follower\'s account ...')
                    initial = self.get_followers(driver)
                    follower.extend(initial)
                    plus = 0
                    while True:
                        # Scroll down to bottom
                        pixels = 1200 + plus
                        self.logger.info('Scrolling down')
                        driver.execute_script("window.scrollTo(0, {})".format(pixels))
                        # Wait to load page
                        sleep(1)
                        self.logger.info('Updating follower\'s account ...')
                        users = self.get_followers(driver)
                        # Calculate new scroll height and compare with last scroll height
                        new_height = driver.execute_script('return window.pageYOffset')
                        self.logger.info('Updated height: {}px'.format(new_height))
                        follower.extend(users)
                        f=sorted(set(follower))
                        # break condition
                        if len(f) >=numb_followers:
                            result={}
                            self.logger.info('Finished for follower\'s account: {} followers'.format(len(f)))
                            break
                        else:
                            self.logger.info('Updated {} followers'.format(len(f)))
                            if len(f) >=numb_followers:
                                result = {}
                                self.logger.info('Finished for follower\'s account: {} followers'.format(len(f)))
                                break
                            last_height = new_height
                            self.logger.info('Last height: {}px'.format(last_height))
                            plus += 1300

                    break

                else:
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
                        try:
                            sleep(2)
                            raw_username = driver.find_element_by_xpath(
                                '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div/span')
                            username = raw_username.get_attribute('innerHTML')
                        except:
                            username = None
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
                if error in driver.page_source:
                    self.logger.info('Error occured - Refresh page')
                    errors += 1
                    if errors > 3:
                        result = {'Name': None, 'Username': None, 'Messages': 'Error', 'Links': link, 'Dead': None,
                                  'Scrapped by': self.username}
                        break
                    else:
                        self.logger.info('{} try'.format(errors))
                        continue
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
        return result, crashed, f

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
