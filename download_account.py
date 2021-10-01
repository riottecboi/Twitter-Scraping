from setup import SetUp
import json
import logging
import sys

setting = SetUp()
logger = logging.getLogger('Twitter-file-download')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
with open('config.json', encoding='utf-8') as json_data_file:
    file = json.load(json_data_file)

try:
    logger.info('Downloading account file')
    setting.download_mg_follower_file(**file)
except Exception as e:
    logger.info(str(e))
