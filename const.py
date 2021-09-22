import re
import os
import configparser
import requests

version = '1.1.1-dev'

# const
twt_count = 100  # 推主媒体批量爬取时, 每次api抓取的推文计数
url_args_help = \
    '''tw url to gather media, must be like:
    1. https://twitter.com/***/status/***
    2. https://t.co/*** (tweets short url)
    3. https://twitter.com/*** (user page, *** is user_id)
    # 3. will gather all media files of user's tweets'''
conf = configparser.RawConfigParser()
conf_path = os.path.expanduser('~') + '/tw_media_downloader.conf'

# api auth token
authorization = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

# context/config
context = {
    'globalSession': requests.Session(),
    'proxy': {},
    'headers': {'authorization': authorization, 'Cookie': '', 'User-Agent': ''},
    'dl_path': './twitter_media_download',
    'log_path': './media_downloader_log'
}


def setContext(key, value):
    context[key] = value


def getContext(key):
    return context[key]


# api url
host_url = 'https://api.twitter.com/1.1/guest/activate.json'
api_url = 'https://api.twitter.com/2/timeline/conversation/{}.json?include_entities=false&include_user_entities=false&tweet_mode=extended'
media_api_url = 'https://twitter.com/i/api/graphql/p7Yt7EGxv3YSk7z8MnUNFA/UserMedia?variables={}'
user_api_url = 'https://twitter.com/i/api/graphql/Vf8si2dfZ1zmah8ePYPjDQ/UserByScreenNameWithoutResults?variables={}'

# api parameter
media_api_par = '{{"userId":"{}","count":{},"withTweetQuoteCount":false,"includePromotedContent":false,"withSuperFollowsUserFields":false,"withUserResults":false,"withBirdwatchPivots":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":false,"withClientEventToken":false,"withBirdwatchNotes":false,"withVoice":false}}'
user_api_par = '{{"screen_name":"{}","withHighlightedLabel":false}}'

# re pattern
p_csrf_token = re.compile(r'ct0=(.+?);?$')
p_proxy = re.compile(r'.+?:(\d+)$')
p_user_id = re.compile(r'"rest_id":"(\d+)"')
p_tw_id = re.compile(r'conversation_id_str":"(\d+)')
p_user_media_count = re.compile(r'"media_count":(\d+),')
p_user_link = re.compile(r'https://twitter.com/([^/]+?)(?:/media)?$')
p_tw_link = re.compile(r'https://twitter.com/.+?/status/(\d+)')
p_pic_link = re.compile(r'''(https://pbs.twimg.com/media/(.+?))['"]''')
p_gif_link = re.compile(r'(https://video.twimg.com/tweet_video/(.+?\.mp4))')
p_vid_link = re.compile(
    r'(https://video.twimg.com/ext_tw_video/(\d+)/pu/vid/(\d+x\d+)/(.+?\.mp4))')
