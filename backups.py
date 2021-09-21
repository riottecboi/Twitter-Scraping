from setup import SetUp
import logging
import sys
import json


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

path = 'raw/data.json'
logger.info('The path of file located at: {}'.format(path))
logger.info('Syncing data to Mega Storage Cloud')
upload=setting.sync_to_mega(path,**file)
logger.info('Finished')