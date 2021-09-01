import re

version = '1.1.1-dev'

# api url
host_url = 'https://api.twitter.com/1.1/guest/activate.json'
api_url = 'https://api.twitter.com/2/timeline/conversation/{' \
          '}.json?include_entities=false&include_user_entities=false&tweet_mode=extended'
media_api_url = 'https://twitter.com/i/api/graphql/OBcjbNAUqhXAWVk2kCWQ8Q/UserMedia?variables={}'

# api parameter
media_api_par = '{{"userId":"{}","count":{},"withHighlightedLabel":false,"withTweetQuoteCount":false,' \
                '"includePromotedContent":false,"withTweetResult":false,"withReactions":false,' \
                '"withSuperFollowsTweetFields":false,"withSuperFollowsUserFields":false,"withUserResults":false,' \
                '"withClientEventToken":false,"withBirdwatchNotes":false,"withBirdwatchPivots":false,' \
                '"withVoice":false}} '
user_api_url = 'https://twitter.com/i/api/graphql/Vf8si2dfZ1zmah8ePYPjDQ/UserByScreenNameWithoutResults?variables={}'
user_api_par = '{{"screen_name":"{}","withHighlightedLabel":false}}'

# api auth token
authorization = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs" \
                "%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

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
p_vid_link = re.compile(r'(https://video.twimg.com/ext_tw_video/(\d+)/pu/vid/(\d+x\d+)/(.+?\.mp4))')
