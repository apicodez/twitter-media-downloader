import re
import os
import configparser
import requests

version = '1.2.3'

# const
twtCount = 100  # 推主媒体批量爬取时, 每次api抓取的推文计数
url_args_help = \
    '''tw url to gather media, must be like:
    1. https://twitter.com/***/status/***
    2. https://twitter.com/***(/media) (user page, *** is user_id)
    # 2. will gather all media files of user's tweets'''
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
    'log_path': './log',
    'updateInfo': {'LastCheckDate': '', 'tagName': '', 'name': ''}
}


def setContext(key, value):
    context[key] = value


def getContext(key=None):
    if key:
        return context[key]
    else:
        return context


# api url
hostUrl = 'https://api.twitter.com/1.1/guest/activate.json'
twtApi = 'https://api.twitter.com/2/timeline/conversation/{}.json'
userMediaApi = 'https://twitter.com/i/api/graphql/ngkNnhoHF01FpsMjb57TLA/UserMedia'
userInfoApi = 'https://twitter.com/i/api/graphql/Vf8si2dfZ1zmah8ePYPjDQ/UserByScreenNameWithoutResults'
checkUpdateApi = 'https://api.github.com/repos/mengzonefire/twitter-media-downloader/releases/latest'

# api parameter
twtApiPar = {'include_entities': 'false',
             'include_user_entities': 'false', 'tweet_mode': 'extended'}
userMediaApiPar = '{{"userId":"{}","count":{},{}"includePromotedContent":false,"withSuperFollowsUserFields":false,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":false,"withClientEventToken":false,"withBirdwatchNotes":false,"withVoice":false,"withV2Timeline":true}}'
userMediaApiPar2 = '{"responsive_web_like_by_author_enabled":false,"dont_mention_me_view_api_enabled":false,"interactive_text_enabled":false,"responsive_web_uc_gql_enabled":false,"responsive_web_edit_tweet_api_enabled":false}'
userInfoApiPar = '{{"screen_name":"{}","withHighlightedLabel":false}}'

# re pattern
p_csrf_token = re.compile(r'ct0=(.+?)(?:;|$)')
p_proxy = re.compile(r'.+?:(\d+)$')
p_user_id = re.compile(r'"rest_id":"(\d+)"')
p_twt_id = re.compile(r'conversation_id_str":"(\d+)')
p_user_link = re.compile(r'https://twitter.com/([^/]+?)(?:/media)?$')
p_twt_link = re.compile(r'https://twitter.com/(.+?)/status/(\d+)')
p_pic_link = re.compile(r'''(https://pbs.twimg.com/media/(.+?))['"]''')
p_gif_link = re.compile(r'(https://video.twimg.com/tweet_video/(.+?\.mp4))')
p_vid_link = re.compile(
    r'(https://video.twimg.com/ext_tw_video/(\d+)/pu/vid/(\d+x\d+)/(.+?\.mp4))')
p_text_content = re.compile(r'''full_text['"]:\s?['"](.+?)['"]''')
p_cursor = re.compile(r'value":"(.+?)"')

# http code text warning
httpCodeText = {'403': '本机IP已被推特服务器禁止访问, 请尝试更换代理节点',
                '401': '导入的cookie无效, 请重新获取并导入'}
