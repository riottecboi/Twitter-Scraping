from twitter import Twitter
from setup import SetUp
import json
import logging
import sys
import os
import random

setting = SetUp()
logger = logging.getLogger('Twitter-followers')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
with open('config.json', encoding='utf-8') as json_data_file:
    file = json.load(json_data_file)

conf_path = file['conf_path']
conf_files = os.listdir(conf_path)

results = []
account_path = file['account_path']
account_files = os.listdir(account_path)

try:
    if len(account_files) != 0:
        #random_file = random.choice(account_files)
        logger.info('Take {} to scrape data'.format('accounts.txt'))
        profiles = setting.get_list_links(account_path+f"/{'accounts.txt'}")
        for link in profiles:
            random_conf = random.choice(conf_files)
            with open('{}/{}'.format(conf_path,random_conf), 'r', encoding='utf-8') as json_data_file:
                kwargs = json.load(json_data_file)
                username = kwargs['username']
            logger.info('Using configure {} with username {}'.format(random_conf, username))
            twitter = Twitter(logger=logger, **kwargs)
            result = twitter.search(link,followers=True)
            results.extend(result[2])
except Exception as e:
    logger.info(str(e))
if len(results) !=0:
    followers = setting.write_file('/follower.txt', results)
    logger.info('{} is done scrapped - removed this'.format('accounts.txt'))
    os.remove(account_path + f"/{'accounts.txt'}")
    account_files = os.listdir(account_path)
    if len(account_files) == 0:
        logger.info('Syncing data to Mega Storage Cloud')
        upload = setting.sync_to_mega(followers, **file)
        logger.info('Result: {}'.format(upload))
    logger.info('Finished')
logger.info('Unfinished')