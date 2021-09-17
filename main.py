from twitter import Twitter
from setup import SetUp
import json
import logging
import sys
import os
import random

setting = SetUp()
logger = logging.getLogger('Twitter-test')
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
random_conf = random.choice(conf_files)

with open('configures/{}'.format(random_conf), encoding='utf-8') as json_data_file:
    kwargs = json.load(json_data_file)

results = []
links_path = file['links_path']
link_files = os.listdir(links_path)

try:

    random_file = random.choice(link_files)
    profiles = setting.get_list_links(links_path+f"/{random_file}")
    twitter = Twitter(logger=logger, **kwargs)
    for link in profiles:
        result = twitter.search(link)
        results.append(result)
    logger.info('Generating CSV file ...')
    generateCSV = setting.generate_csv(results)
    logger.info('The path of file located at: {}'.format(generateCSV))
    logger.info('Syncing data to Mega Storage Cloud')
    upload=setting.sync_to_mega(generateCSV,**kwargs)
    logger.info('Result: {}'.format(upload))
    os.remove(links_path+f"/{random_file}")
except Exception as e:
    logger.info(str(e))
logger.info('Finished')

