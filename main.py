from twitter import Twitter
from setup import SetUp
import json
import logging
import sys
import os
import random
from time import sleep

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

results = []
links_path = file['links_path']
link_files = os.listdir(links_path)

try:
    if len(link_files) != 0:
        for l in link_files:
            #random_file = random.choice(link_files)
            logger.info('Take {} to scrape data'.format(l))
            profiles = setting.get_list_links(links_path+f"/{l}")
            for link in profiles:
                random_conf = random.choice(conf_files)
                with open('{}/{}'.format(conf_path,random_conf), 'r', encoding='utf-8') as json_data_file:
                    kwargs = json.load(json_data_file)
                    username = kwargs['username']
                logger.info('Using configure {} with username {}'.format(random_conf, username))
                twitter = Twitter(logger=logger, **kwargs)
                result = twitter.search(link)
                logger.info('Updating raw data ...')
                update = setting.update_data_csv(result[0])
                results.append(result[0])
            logger.info('{} is done scrapped - removed this'.format(l))
            os.remove(links_path+f"/{l}")
            link_files = os.listdir(links_path)
            if len(link_files) == 0:
                logger.info('Finish scrapping')
                with open('raw/data.json', encoding='utf-8') as json_data_file:
                    results = json.load(json_data_file)
                logger.info('Generating CSV file ...')
                generateCSV = setting.generate_csv(results)
                logger.info('The path of file located at: {}'.format(generateCSV))
                logger.info('Syncing data to Mega Storage Cloud')
                upload = setting.sync_to_mega(generateCSV, **file)
                logger.info('Result: {}'.format(upload))
                if generateCSV != 'Can\'t generate CSV':
                    with open('raw/data.json', 'w') as clean:
                        clean.write(json.dumps([]))
                        clean.close()
                    logger.info('Cleaned raw data')
            else:
                logger.info('Take a break time for 30 min')
                sleep(900)
    else:
        with open('raw/data.json', 'w') as clean:
            clean.write(json.dumps([]))
            clean.close()
        logger.info('Cleaned raw data')
except Exception as e:
    logger.info(str(e))
logger.info('Finished')

