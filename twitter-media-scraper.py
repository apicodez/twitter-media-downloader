import winreg, traceback, requests, re, os, time, json, argparse
from urllib.parse import quote

version = '1.1'
UA = None
cookie = None
proxy = {}
headers = {}
host_url = 'https://api.twitter.com/1.1/guest/activate.json'
api_url = 'https://api.twitter.com/2/timeline/conversation/{' \
          '}.json?include_entities=false&include_user_entities=false&tweet_mode=extended'
media_api_url = 'https://twitter.com/i/api/graphql/ep3EdGK189uKvABB-8uIlQ/UserMedia?variables={}'
media_api_par = '{{"userId":"{}","count":{},"withHighlightedLabel":false,' \
                '"withTweetQuoteCount":false,"includePromotedContent":false,"withTweetResult":false,' \
                '"withReactions":false,"withUserResults":false,"withClientEventToken":false,' \
                '"withBirdwatchNotes":false,"withBirdwatchPivots":false,"withVoice":false,"withNonLegacyCard":false}}'
user_api_url = 'https://twitter.com/i/api/graphql/Vf8si2dfZ1zmah8ePYPjDQ/UserByScreenNameWithoutResults?variables={}'
user_api_par = '{{"screen_name":"{}","withHighlightedLabel":false}}'
authorization = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs" \
                "%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA "
dl_path = 'twitter_scraper_download'
log_path = 'twitter_scraper_log'
p_proxy = re.compile(r'.+?:(\d+)$')
p_user_id = re.compile(r'"rest_id":"(\d+)"')
p_user_media_count = re.compile(r'"media_count":(\d+),')
p_user_link = re.compile(r'https://twitter.com/([^/]+)$')
p_tw_link = re.compile(r'https://twitter.com/.+?/status/(\d+)')
p_pic_link = re.compile(r'''(https://pbs.twimg.com/media/(.+?))['"]''')
p_gif_link = re.compile(r'(https://video.twimg.com/tweet_video/(.+?\.mp4))')
p_vid_link = re.compile(r'(https://video.twimg.com/ext_tw_video/(\d+)/pu/vid/(\d+x\d+)/(.+?\.mp4))')
issue_page = 'https://github.com/mengzonefire/twitter-media-scraper/issues'
api_warning = '提取失败: 接口访问错误, 请检查log文件, 并前往issue页反馈:\n{}'
nothing_warning = '提取失败: 该推文不含媒体内容, 若包含, 请到issue页反馈:\n{}'
s = requests.Session()

description = \
    '''[urls] argument must be like:
    1. https://twitter.com/***/status/***
    2. https://t.co/*** (tweets short url)
    3. https://twitter.com/*** 
    (user page url, *** is userid, will gather all media of user's tweets)
    '''
# usage info
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-c', '--cookie', dest='cookie', type=str,  help='set cookie to access locked tweets')
parser.add_argument('-p', '--proxy', dest='proxy', type=str, help='set network proxy, must be http proxy')
parser.add_argument('-u', '--user_agent', dest='user_agent', type=str, help='set user-agent')
parser.add_argument('--version', '-v', action='store_true', help='show version')
parser.add_argument('urls', type=str, nargs='*', help='twitter url to gather media')
args = parser.parse_args()


def get_proxy():
    global proxy
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings")
    proxy_enable, key_type = winreg.QueryValueEx(key, "ProxyEnable")
    if proxy_enable:
        proxy_server, key_type = winreg.QueryValueEx(key, "ProxyServer")
        proxy = {'http': 'http://'+proxy_server, 'https': 'https://'+proxy_server}


def set_header():
    global headers
    headers['authorization'] = authorization
    if UA:
        headers['User-Agent'] = UA
    response = s.post(host_url, proxies=proxy, headers=headers).json()
    if 'guest_token' in response:
        x_guest_token = response['guest_token']
        headers['x-guest-token'] = x_guest_token
    else:
        print('guest_token获取失败, 请前往issue页反馈:\n{}'.format(issue_page))
        input('\n按回车键退出程序\n')
        exit()


def match_media_link(tw_content):
    link_dict = {}

    # get pic links
    pic_links = p_pic_link.findall(tw_content)
    # get [(media_url, file_name)], add query '?name=orig' can get original pic file
    if pic_links:
        for pic_link in pic_links:
            link_dict[pic_link[1]] = pic_link[0] + '?name=orig'

    # get gif links(.mp4)
    gif_links = p_gif_link.findall(tw_content)
    # get [(media_url, file_name)]
    if gif_links:
        for gif_link in gif_links:
            link_dict[gif_link[1]] = gif_link[0]

    # get video links(.mp4)
    vid_links = p_vid_link.findall(tw_content)
    # [(media_url, resolution, file_name)]
    if vid_links:
        best_choices = {}
        # choose largest resolution
        for vid_link in vid_links:
            resolution = eval(vid_link[2].replace('x', '*'))
            if vid_link[1] not in best_choices:
                best_choices[vid_link[1]] = {'resolution': 0, 'file_name': None, 'url': None}
            if resolution > best_choices[vid_link[1]]['resolution']:
                best_choices[vid_link[1]]['resolution'] = resolution
                best_choices[vid_link[1]]['file_name'] = vid_link[3]
                best_choices[vid_link[1]]['url'] = vid_link[0]
        for vid_id in best_choices:
            link_dict[best_choices[vid_id]['file_name']] = best_choices[vid_id]['url']

    if not link_dict:
        print(nothing_warning.format(issue_page))
    # get [file_name: media_url] as link_dict
    return link_dict


def get_page_media_link(page_id):
    page_content = s.get(api_url.format(page_id), proxies=proxy, headers=headers).text
    if '"{}":'.format(page_id) in page_content:
        tw_content = str(json.loads(page_content)['globalObjects']['tweets'][page_id])
        # debug
        # print(tw_content)
        return match_media_link(tw_content)
    else:
        if 'Sorry, that page does not exist' in page_content:
            print('提取失败: 该推文已删除/不存在')
        else:
            print(api_warning.format(issue_page))
            write_log(page_id, page_content)
        return None


def download_media(link, file_name):
    prog_text = '\r正在下载: {}'.format(file_name) + ' ...{}'
    print(prog_text.format('0%'), end="")
    r = s.get(link, proxies=proxy, stream=True)
    dl_size = 0
    content_size = 0
    if 'content-length' in r.headers:
        content_size = int(r.headers['content-length'])
    elif 'Content-Length' in r.headers:
        content_size = int(r.headers['Content-Length'])
    with open('./{}/{}'.format(dl_path, file_name), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 2):
            f.write(chunk)
            if content_size:
                dl_size += len(chunk)
                prog = '{}%'.format(int(round(dl_size / content_size, 2) * 100))
                print(prog_text.format(prog), end="")
    print(prog_text.format('下载完成'))
    time.sleep(1)


def start_crawl(page_urls):
    if not os.path.exists(dl_path):
        os.mkdir(dl_path)

    input_flag = False
    if not page_urls:
        input_flag = True
        print('输入链接(支持批量,一行一条,双击回车确认):')
        while True:
            temp = input()
            if not temp:
                break
            if '//t.co/' in temp or '//twitter.com/' in temp:
                page_urls.append(temp)

    for page_url in page_urls:
        print('\n正在提取: {}'.format(page_url))

        # check user page link
        user_link = p_user_link.findall(page_url)
        if user_link:
            user_name = user_link[0]
            user_id, media_count = get_user_info(user_name)
            if not user_id:
                continue
            user_media_links = get_user_media_link(user_id, media_count)
            if user_media_links:
                for file_name in user_media_links:
                    download_media(user_media_links[file_name], file_name)
            continue

        # convert short url to normal
        if '//t.co/' in page_url:
            page_url = s.get(page_url, proxies=proxy).url
        # match url to tweets
        page_id = p_tw_link.findall(page_url)
        if page_id:
            page_id = page_id[0]
        else:
            print('提取失败: 错误的推文/推主主页链接')
            continue
        media_links = get_page_media_link(page_id)
        if media_links:
            for file_name in media_links:
                download_media(media_links[file_name], file_name)

    if input_flag and input('回车键退出, 输入任意内容继续提取\n'):
        start_crawl([])


def get_user_media_link(user_id, media_count):
    page_content = s.get(media_api_url.format(
        quote(media_api_par.format(user_id, media_count))), proxies=proxy, headers=headers).text
    link_dict = match_media_link(page_content)
    return link_dict


def get_user_info(user_name):
    page_content = s.get(user_api_url.format(
        quote(user_api_par.format(user_name))), proxies=proxy, headers=headers).text
    user_id = p_user_id.findall(page_content)
    media_count = p_user_media_count.findall(page_content)
    if user_id:
        user_id = user_id[0]
    else:
        print(api_warning.format(issue_page))
        write_log(user_name, page_content)
        return None, None
    if media_count:
        media_count = int(media_count[0])
    else:
        print(api_warning.format(issue_page))
        write_log(user_name, page_content)
        return None, None
    return user_id, media_count


def write_log(log_name, log_content):
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    file_path = './{}/{}.txt'.format(log_path, log_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(log_content)
        print('log文件已保存到{}'.format(file_path))


def args_handler():
    global UA, cookie
    if args.version:
        print('version {}'.format(version))
    if args.proxy:
        set_proxy(args.proxy)
    else:
        get_proxy()
    if args.cookie:
        cookie = args.cookie
    if args.user_agent:
        UA = args.user_agent
    set_header()
    save_env()
    start_crawl(args.urls)


def save_env():
    pass


def set_proxy(proxy_str):
    global proxy
    proxy_match = p_proxy.match(proxy_str)
    if proxy_match and 1024 <= int(proxy_match.group(1)) <= 65535:
        proxy = {'http': proxy_str, 'https': proxy_str}
        print('代理设置为: {}'.format(proxy_str))
    else:
        print('代理格式错误, 格式: [ip/域名]:[端口], 示例: 127.0.0.1:7890')


def main():
    # debug
    # print(args.urls)
    args_handler()


def except_handler(e):
    if 'Connection' in str(e):
        print('网络连接超时, 请检查代理设置')
    else:
        traceback.print_exc()
        write_log('crash', str(e))
    if input('回车键退出, 输入任意内容重置脚本\n'):
        main()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        except_handler(e)
