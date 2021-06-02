import winreg, traceback, requests, os, time, json, argparse
from argparse import RawTextHelpFormatter
from urllib.parse import quote
from const import *
from warning import *

proxy = {}
headers = {'Cookie': ''}
dl_path = './twitter_media_download'
log_path = './media_downloader_log'
s = requests.Session()

description = \
    '''[url] argument must be like:
    1. https://twitter.com/***/status/***
    2. https://t.co/*** (tweets short url)
    3. https://twitter.com/*** (user page, *** is user_id)
    # 3. will gather all media files of user's tweets'''
# usage info
parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
parser.add_argument('-c', '--cookie', dest='cookie', type=str,  help='set cookie to access locked tweets')
parser.add_argument('-p', '--proxy', dest='proxy', type=str, help='set network proxy, must be http proxy')
parser.add_argument('-u', '--user_agent', dest='user_agent', type=str, help='set user-agent')
parser.add_argument('-t', '--tweet_id', dest='tweet_id', type=str, help='convert tweet_id to tweet_url')
parser.add_argument('-d', '--dir', dest='dir', type=str, help='set download path')
parser.add_argument('-v', '--version', action='store_true', help='show version')
parser.add_argument('url', type=str, nargs='*', help='twitter url to gather media')
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
    if headers['Cookie']:
        return
    response = s.post(host_url, proxies=proxy, headers=headers).json()
    if 'guest_token' in response:
        x_guest_token = response['guest_token']
        headers['x-guest-token'] = x_guest_token
    else:
        print(token_warning)
        input(exit_ask)
        exit()


def match_media_link(tw_content, page_id):
    link_dict = {}

    # get pic links
    pic_links = p_pic_link.findall(tw_content)
    # get [(media_url, file_name)], add query '?name=orig' can get original pic file
    if pic_links:
        for pic_link in pic_links:
            file_name = '{}_{}'.format(page_id, pic_link[1])
            link_dict[file_name] = pic_link[0] + '?name=orig'
        return link_dict

    # get gif links(.mp4)
    gif_links = p_gif_link.findall(tw_content)
    # get [(media_url, file_name)]
    if gif_links:
        for gif_link in gif_links:
            file_name = '{}_{}'.format(page_id, gif_link[1])
            link_dict[file_name] = gif_link[0]
        return link_dict

    # get video links(.mp4)
    vid_links = p_vid_link.findall(tw_content)
    # [(media_url, resolution, file_name)]
    if vid_links:
        best_choice = {'resolution': 0, 'file_name': None, 'url': None}
        # choose largest resolution
        for vid_link in vid_links:
            resolution = eval(vid_link[2].replace('x', '*'))
            if resolution > best_choice['resolution']:
                best_choice['resolution'] = resolution
                best_choice['file_name'] = vid_link[3]
                best_choice['url'] = vid_link[0]
        file_name = '{}_{}'.format(page_id, best_choice['file_name'])
        link_dict[file_name] = best_choice['url']

    # get [file_name: media_url] as link_dict
    return link_dict


def get_page_media_link(page_id, get_url=False):
    response = s.get(api_url.format(page_id), proxies=proxy, headers=headers)
    if response.status_code != 200:
        print(http_warning.format(response.status_code, issue_page))
        return None
    page_content = response.text
    # debug
    # print(page_content)
    if '"{}":'.format(page_id) in page_content:
        tw_content = str(json.loads(page_content)['globalObjects']['tweets'][page_id])

        # convert tweet_id to tweet_url
        if get_url:
            tw_link = p_tw_link.search(tw_content)
            if tw_link:
                return tw_link.group()
            else:
                print(api_warning)
                return None

        media_links = match_media_link(tw_content, page_id)
        if not media_links:
            print(nothing_warning)
        return media_links
    else:
        if 'Sorry, that page does not exist' in page_content:
            print(not_exist_warning)
        elif 'unable to view this Tweet' in page_content:
            print(tweet_unavailable_warning)
        else:
            print(api_warning)
            write_log(page_id, page_content)
        return None


def download_media(link, file_name, save_path=''):
    if not save_path:
        save_path = dl_path
    prog_text = '\r正在下载: {}'.format(file_name) + ' ...{}'
    print(prog_text.format('0%'), end="")
    response = s.get(link, proxies=proxy, stream=True)
    if response.status_code != 200:
        print(http_warning.format(response.status_code, issue_page))
        return
    dl_size = 0
    content_size = 0
    if 'content-length' in response.headers:
        content_size = int(response.headers['content-length'])
    elif 'Content-Length' in response.headers:
        content_size = int(response.headers['Content-Length'])
    with open('{}/{}'.format(save_path, file_name), 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024 * 2):
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
        print(input_ask)
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
                if user_media_links != 'error':
                    save_path = dl_path + '/{}'.format(user_name)
                    if not os.path.exists(save_path):
                        os.mkdir(save_path)
                    for file_name in user_media_links:
                        download_media(user_media_links[file_name], file_name, save_path)
            else:
                print(nothing_warning)
            continue

        # convert short url to normal
        if '//t.co/' in page_url:
            page_url = s.get(page_url, proxies=proxy).url
        # match url to tweets
        page_id = p_tw_link.findall(page_url)
        if page_id:
            page_id = page_id[0]
        else:
            print(wrong_url_warning)
            continue
        media_links = get_page_media_link(page_id)
        if media_links:
            for file_name in media_links:
                download_media(media_links[file_name], file_name)

    if input_flag and input(continue_ask):
        start_crawl([])


def get_user_media_link(user_id, media_count):
    link_dict = {}
    response = s.get(media_api_url.format(
        quote(media_api_par.format(user_id, media_count))), proxies=proxy, headers=headers)
    if response.status_code != 200:
        print(http_warning.format(response.status_code, issue_page))
        return 'error'
    page_content = response.text
    if 'UserUnavailable' in page_content:
        print(user_unavailable_warning)
        return 'error'
    page_id_list = p_tw_id.findall(page_content)
    content_split = page_content.split('conversation_id_str')
    page_id_dict = dict(zip(page_id_list, content_split[1:]))
    for page_id in page_id_dict:
        link_dict = dict(link_dict, **match_media_link(page_id_dict[page_id], page_id))
    return link_dict


def get_user_info(user_name):
    response = s.get(user_api_url.format(
        quote(user_api_par.format(user_name))), proxies=proxy, headers=headers)
    if response.status_code != 200:
        print(http_warning.format(response.status_code, issue_page))
        return None, None
    page_content = response.text
    user_id = p_user_id.findall(page_content)
    media_count = p_user_media_count.findall(page_content)
    if user_id:
        user_id = user_id[0]
    else:
        print(user_warning)
        write_log(user_name, page_content)
        return None, None
    if media_count:
        media_count = int(media_count[0])
    else:
        print(api_warning)
        write_log(user_name, page_content)
        return None, None
    return user_id, media_count


def write_log(log_name, log_content):
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    file_path = '{}/{}.txt'.format(log_path, log_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(log_content)
        print('log文件已保存到{}'.format(file_path))


def args_handler():
    global headers, dl_path
    if args.version:
        print('version: {}\nissue page: {}'.format(version, issue_page))
        return
    if args.proxy:
        set_proxy(args.proxy)
    else:
        get_proxy()
    if args.cookie:
        headers['Cookie'] = args.cookie
        csrf_token = p_csrf_token.findall(args.cookie)
        if csrf_token or 'auth_token' not in args.cookie:
            headers['x-csrf-token'] = csrf_token[0]
        else:
            print(cookie_warning)
            return
    if args.user_agent:
        headers['User-Agent'] = args.user_agent
    if args.dir:
        dl_path = args.dir
    set_header()
    save_env()
    if args.tweet_id:
        tw_link = get_page_media_link(args.tweet_id, True)
        if tw_link:
            print(tw_link)
        return
    start_crawl(args.url)


def save_env():
    pass


def set_proxy(proxy_str):
    global proxy
    proxy_match = p_proxy.match(proxy_str)
    if proxy_match and 1024 <= int(proxy_match.group(1)) <= 65535:
        proxy = {'http': 'http://' + proxy_str, 'https': 'https://' + proxy_str}
        print('代理设置为: {}'.format(proxy_str))
    else:
        print(proxy_warning)
        exit()


def main():
    args_handler()


def except_handler(err):
    if 'Connection' in str(err):
        print(network_error_warning)
    else:
        traceback.print_exc()
        write_log('crash', str(err))
    if input(rest_ask):
        main()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        except_handler(e)
