from twitter import Twitter
from setup import SetUp
import json
import logging
import sys
import os
import random

setting = SetUp()
logger = logging.getLogger('Formatting')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

with open('config.json', encoding='utf-8') as json_data_file:
    file = json.load(json_data_file)

myfile = open(file['twitch_file'], 'r')
contents = myfile.readlines()

conf_path = file['conf_path']
conf_files = os.listdir(conf_path)

random_conf = random.choice(conf_files)
with open('{}/{}'.format(conf_path, random_conf), 'r', encoding='utf-8') as json_data_file:
    kwargs = json.load(json_data_file)
twitter = Twitter(logger=logger, **kwargs)

links = []
twitter_list = []
twitch_list = []
external_list = []
try:
    logger.info('We have total {} links'.format(len(contents)))
    count = 1
    for content in contents:
        logger.info('Link no.{}'.format(count))
        logger.info('Current link {}'.format(content.strip()))
        if 'www' in content.strip():
            word = content.strip().replace('www', 'm')
            logger.info('Modified link format into {}'.format(word))
        else:
            word = content.strip()
            logger.info('Keeps the same format of link - No changed')
        check = word.split('https://')[1].split('/')
        kind = check[1]
        if kind == 'videos' or kind == 'clip':
            logger.info('This link is video/clip link')
            get_links = twitter.get_profile_by_video_clip_link(word)
            links.extend(get_links)
            print('\n')
        elif kind != 'directory':
            logger.info('This link is profile link')
            get_links = twitter.get_profile_by_profile_link(word)
            links.extend(get_links)
            print('\n')
        # elif kind == 'directory':
        #     logger.info('This is directory link')
        #     if check[2] == 'game':
        #         get_links = twitter.get_profile_by_directory_link(word)
        #     else:
        #         get_links = twitter.get_profile_by_directory_link(word, v2=True)
        #     links.extend(get_links)
        #     print('\n')
        count += 1
    logger.info('Appending data')
    for data in links:
        if data is None:
            continue
        if 'twitter' in data:
            logger.info('Appending {} to twitter list'.format(data))
            twitter_list.append(data)
        elif 'twitch' in data:
            logger.info('Appending {} to twitch list'.format(data))
            twitch_list.append(data)
        else:
            logger.info('Appending {} to external list'.format(data))
            external_list.append(data)

    try:
        logger.info('Write Twitch links file')
        p = setting.write_file('twitchLinks.txt', twitch_list)
        logger.info('File Twitch located at: {}'.format(p))
        if len(twitch_list) != 0:
            logger.info('Syncing Twitch data to Mega Storage Cloud')
            upload = setting.sync_to_mega(twitch_list, **file)
            logger.info('Result: {}'.format(upload))
    except Exception as e:
        logger.info('Exception occured: {}'.format(str(e)))
        pass

    try:
        logger.info('Write Twitter links file')
        p = setting.write_file('twitterLinks.txt', twitter_list)
        logger.info('File Twitter located at: {}'.format(p))
        if len(twitch_list) != 0:
            logger.info('Syncing Twitter data to Mega Storage Cloud')
            upload = setting.sync_to_mega(twitch_list, **file)
            logger.info('Result: {}'.format(upload))
    except Exception as e:
        logger.info('Exception occured: {}'.format(str(e)))
        pass

    try:
        logger.info('Write external links file')
        p = setting.write_file('externalLinks.txt', external_list)
        logger.info('File external links located at: {}'.format(p))
        if len(external_list) != 0:
            logger.info('Syncing External links data to Mega Storage Cloud')
            upload = setting.sync_to_mega(external_list, **file)
            logger.info('Result: {}'.format(upload))
    except Exception as e:
        logger.info('Exception occured: {}'.format(str(e)))
        pass
    logger.info('Finished')

except Exception as e:
    logger.info(str(e))
    logger.info('Unfinished')