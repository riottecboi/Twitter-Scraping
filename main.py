from twitter import Twitter
from setup import SetUp
import json
import logging
import sys

setting = SetUp()

logger = logging.getLogger('Twitter-test')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
with open('config.json', encoding='utf-8') as json_data_file:
    kwargs = json.load(json_data_file)
results = []
profiles = kwargs['profiles']
twitter = Twitter(logger=logger, **kwargs)
for link in profiles:
    result = twitter.search(link)
    results.append(result)

generateCSV = setting.generate_csv(results)
print(generateCSV)
