import winreg, traceback, requests, re, os, time, json
version = '1.1'
proxy = None
headers = {}
host_url = 'https://api.twitter.com/1.1/guest/activate.json'
api_url = 'https://api.twitter.com/2/timeline/conversation/{}.json?include_entities=false&include_user_entities=false&tweet_mode=extended'
authorization = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
dl_path = 'twitter_download'
log_path = 'twitter_log'
p_tw_link = re.compile(r'status/(\d+)')
p_media_link = re.compile(r"(https://pbs.twimg.com/media/.+?)'")
s = requests.Session()


def get_proxy():
    global proxy
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings")
    proxy_enable, key_type = winreg.QueryValueEx(key, "ProxyEnable")
    if proxy_enable:
        proxy_server, key_type = winreg.QueryValueEx(key, "ProxyServer")
        proxy = {'http': 'http://'+proxy_server, 'https': 'https://'+proxy_server}


def set_header():
    global headers
    headers = {'authorization': authorization}
    respone = s.post(host_url, proxies=proxy, headers=headers).json()
    if 'guest_token' in respone:
        x_guest_token = respone['guest_token']
        headers = {'authorization': authorization, 'x-guest-token': x_guest_token}
    else:
        print("guest_token获取失败, 请前往issue页反馈:\nhttps://github.com/mengzonefire/twitter-media-scraper/issues")
        input("\n按回车键退出程序\n")
        exit()


def get_media_link(page_id):
    page_content = s.get(api_url.format(page_id), proxies=proxy, headers=headers).text
    if '"{}":'.format(page_id) in page_content:
        tw_content = json.loads(page_content)['globalObjects']['tweets'][page_id]
        media_link = p_media_link.findall(str(tw_content))
        return media_link
    else:
        if 'Sorry, that page does not exist' in page_content:
            print('提取失败: 该条推特已删除')
        else:
            print('提取失败: 接口访问错误, 请检查log文件, 并前往issue页反馈:\nhttps://github.com/mengzonefire/twitter-media-scraper/issues')
            write_log(page_id, page_content)
        return 'error'


def download_media(links):
    if not os.path.exists(dl_path):
        os.mkdir(dl_path)
    for link in links:
        filename = link.replace('https://pbs.twimg.com/media/', '')
        prog_text = '\r正在下载: {}'.format(filename) + ' ...{}'
        print(prog_text.format('0%'), end="")
        r = s.get(link+'?name=orig', proxies=proxy, stream=True)
        dl_size = 0
        content_size = int(r.headers['content-length'])
        with open('./{}/{}'.format(dl_path, filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*2):
                f.write(chunk)
                dl_size += len(chunk)
                prog = '{}%'.format(int(round(dl_size/content_size, 2)*100))
                print(prog_text.format(prog), end="")
        print(prog_text.format('下载完成'))
        time.sleep(1)


def start_crawl():
    page_urls = []
    print('输入链接(支持批量,一行一条,双击回车确认):')
    while True:
        temp = input()
        if not temp:
            break
        if '//t.co/' in temp or '//twitter.com/' in temp:
            page_urls.append(temp)

    for page_url in page_urls:
        if '//t.co/' in page_url:
            page_id = p_tw_link.search(s.get(page_url, proxies=proxy).text)
            if page_id:
                page_id = page_id.group(1)
            else:
                print('提取失败: 该条推特已删除')
                continue
        else:
            page_id = p_tw_link.findall(page_url)
            if page_id:
                page_id = page_id[0]
            else:
                continue
        print('开始提取: ' + page_url)
        media_link = get_media_link(page_id)
        if media_link:
            if media_link != 'error':
                download_media(media_link)
        else:
            print('提取失败: 该条推特不包含媒体内容')

    if input('回车键退出, 输入任意内容继续提取\n'):
        start_crawl()


def write_log(page_id, page_content):
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    with open('./{}/{}.txt'.format(log_path, page_id), 'w', encoding='utf-8') as f:
        f.write(page_content)


def main():
    get_proxy()
    set_header()
    start_crawl()


if __name__ == '__main__':
    try:
        print('version: {}'.format(version))
        main()
    except Exception as e:
        if 'WinError 10060' in str(e):
            print('连接twitter.com超时，请检查代理设置')
        else:
            traceback.print_exc()
            print(e)
        if input('回车键退出, 输入任意内容重置脚本\n'):
            main()
