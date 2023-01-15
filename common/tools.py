'''
Author: mengzonefire
Date: 2021-09-21 09:20:04
LastEditTime: 2022-09-29 20:29:05
LastEditors: mengzonefire
Description: 工具模块
'''
import sys
import time
import queue
import httpx
import argparse
from common.text import *
from common.const import *
from common.logger import write_log
from argparse import RawTextHelpFormatter

if sys.platform in ['win32', 'win64']:
    import winreg


def getHttpText(httpCode):
    httpCode = str(httpCode)
    if httpCode in httpCodeText:
        return httpCodeText[httpCode]
    return f'请前往issue页反馈:\n{issue_page}'


def initalArgs():
    # prog argument
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-c', '--cookie', dest='cookie', type=str,
                        help='set cookie to access locked users or tweets, input " " to clear')
    parser.add_argument('-p', '--proxy', dest='proxy', type=str,
                        help='set network proxy, must be http proxy, input " " to clear')
    parser.add_argument('-u', '--user_agent', dest='user_agent',
                        type=str, help='set user-agent, input " " to clear')
    parser.add_argument('-d', '--dir', dest='dir',
                        type=str, help='set download path')
    parser.add_argument('-n', '--num', dest='concurrency', type=int,
                        help='set the downloader concurrency')
    parser.add_argument('-q', '--quoted', action="store_true", dest='quoted',
                        help='set whether to include quoted tweets')
    parser.add_argument('-r', '--retweeted', action="store_true", dest='retweeted',
                        help='set whether to include retweeted')
    parser.add_argument('-t', '--type', dest='type', type=str,
                        help='set the desired media type, optional: photo&animated_gif&video&full_text')
    parser.add_argument('-v', '--version', action='store_true',
                        help='show version')
    parser.add_argument('url', type=str, nargs='*', help=url_args_help)
    args = parser.parse_args()
    setContext('args', args)


def getProxy():
    if getContext('proxy'):  # proxy已配置
        return
    if sys.platform not in ['win32', 'win64']:
        return
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings")
    proxy_enable, key_type = winreg.QueryValueEx(key, "ProxyEnable")
    if proxy_enable:
        proxy_server, key_type = winreg.QueryValueEx(key, "ProxyServer")
        setContext('proxy', {'http://': 'http://' + proxy_server,
                             'https://': 'http://' + proxy_server})


def getHeader():  # 获取游客token
    headers = getContext('headers')
    if headers['Cookie']:  # 已设置cookie, 无需游客token
        return
    with httpx.Client(proxies=getContext('proxy'), headers=getContext('headers'), timeout=5, verify=False) as client:
        for i in range(1, 6):
            try:
                response = client.post(hostUrl).json()
                break
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError):
                print(timeout_warning.format(i))
            time.sleep(1)
    if 'guest_token' in response:
        x_guest_token = response['guest_token']
        headers['x-guest-token'] = x_guest_token
        setContext('headers', headers)
    else:
        print(token_warning)
        input(exit_ask)
        exit()


def get_token(cookie):
    csrf_token = p_csrf_token.findall(cookie)
    if len(csrf_token) != 0:
        return csrf_token[0]
    else:
        return None


def setProxy(proxy_str):
    proxyMatch = pProxy.match(proxy_str)
    if proxyMatch and 1024 <= int(proxyMatch.group(1)) <= 65535:
        setContext('proxy', {'http://': 'http://' + proxy_str,
                             'https://': 'https://' + proxy_str})
        print('代理设置为: {}'.format(proxy_str))
    else:
        print(proxy_warning)


def argsHandler():
    args = getContext('args')
    headers = getContext('headers')
    if args.version:
        print('version: {}\ndonate page: {}\nissue page: {}\n'.format(
            version, donate_page, issue_page))
        return
    if args.proxy:
        if args.proxy == ' ':
            setContext('proxy', {})
        else:
            setProxy(args.proxy)
    elif sys.platform in ['win32', 'win64']:
        getProxy()
    if args.cookie:
        if args.cookie == ' ':
            headers['Cookie'] = ''  # 清除cookie
        else:
            args.cookie = args.cookie.strip()
            token = get_token(args.cookie)
            if token:
                headers['x-csrf-token'] = token
                headers['Cookie'] = args.cookie
            else:
                print(cookie_warning)
                return
    if args.user_agent:
        if args.user_agent == ' ':
            headers['User-Agent'] = ''
        else:
            headers['User-Agent'] = args.user_agent
    if args.dir:
        setContext('dl_path', args.dir)
    if args.concurrency:
        setContext('concurrency', args.concurrency)
    if args.type:
        setContext('type', args.type)
    setContext('quoted', args.quoted)
    setContext('retweeted', args.retweeted)
    setContext('header', headers)


def saveEnv():
    conf.read(conf_path, encoding='utf-8')
    if 'global' not in conf.sections():
        conf.add_section('global')
    conf.set("global", "proxy", getContext("proxy"))
    conf.set("global", "download_path", getContext("dl_path"))
    conf.set("global", "user-agent", getContext("headers")["User-Agent"])
    conf.set("global", "cookie", getContext("headers")['Cookie'])
    conf.set("global", "updateinfo", getContext("updateInfo"))
    conf.set("global", "concurrency", getContext("concurrency"))
    conf.set("global", "type", getContext("type"))
    conf.set("global", "quoted", getContext("quoted"))
    conf.set("global", "retweeted", getContext("retweeted"))
    conf.write(open(conf_path, 'w', encoding='utf-8'))


def getEnv():
    if os.path.exists(conf_path):
        conf.read(conf_path, encoding='utf-8')
        if 'global' in conf.sections():
            headers = getContext("headers")
            items = conf.items('global')
            for item in items:
                if item[0] == 'cookie' and item[1]:
                    token = get_token(item[1])
                    if token:
                        headers['x-csrf-token'] = token
                        headers['Cookie'] = item[1]
                elif item[0] == 'user-agent' and item[1]:
                    headers['User-Agent'] = item[1]
                elif item[0] == 'proxy' and item[1]:
                    setContext('proxy', eval(item[1]))
                elif item[0] == 'download_path' and item[1]:
                    setContext('dl_path', item[1])
                elif item[0] == 'updateinfo' and item[1]:
                    setContext('updateInfo', eval(item[1]))
                elif item[0] == 'concurrency' and item[1]:
                    setContext('concurrency', eval(item[1]))
                elif item[0] == 'type' and item[1]:
                    setContext('type', item[1])
                elif item[0] == 'quoted' and item[1]:
                    setContext('quoted', item[1])
                elif item[0] == 'retweeted' and item[1]:
                    setContext('retweeted', item[1])
            setContext('headers', headers)


def getUserId(userName: str):
    with httpx.Client(proxies=getContext('proxy'), headers=getContext('headers'), verify=False) as client:
        for i in range(1, 6):
            try:
                response = client.post(userInfoApi, params={'variables': userInfoApiPar.format(
                    userName)})
                break
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError):
                print(timeout_warning.format(i))
            time.sleep(1)
    if response.status_code != httpx.codes.OK:
        print(http_warning.format('getUserId',
                                  response.status_code, getHttpText(response.status_code)))
        return None
    page_content = response.text
    userId = p_user_id.findall(page_content)
    if userId:
        userId = userId[0]
        return userId
    else:
        print(user_warning)
        write_log(userName, page_content)
        return None


def downloader(client, url, filePath, fileName):
    for i in range(1, 6):
        try:
            with client.stream('GET', url) as response:
                if response.status_code != httpx.codes.OK:
                    print(http_warning.format('downloadFile', response.status_code, getHttpText(response.status_code)))
                    return False
                with open(f'{filePath}.cache', 'wb') as f:
                    for chunk in response.iter_bytes(chunk_size=1024*128):
                        if chunk:
                            f.write(chunk)
                os.rename(f'{filePath}.cache', filePath)
                return True
        except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError, httpx.RemoteProtocolError):
            # print(download_timeout_warning.format(fileName, '正在重试...', i))
            pass
        time.sleep(1)
    print(download_timeout_warning.format(fileName, '失败次数过多...', ''))
    return False


def downloadFile(savePath, dataList, done):
    while True:
        if dataList.qsize():
            break
    while True:
        try:
            datalist = dataList.get(timeout=30)
            dataList.task_done()
        except queue.Empty:
            print(queue_empty_warning)
            return
        if not datalist:
            return
        userName = list(datalist.keys())[0]
        headers = getContext('headers')
        with httpx.Client(proxies=getContext('proxy'), headers=headers, verify=False) as client:
            for datatype, typelayer in datalist.get(userName).items():
                if datatype in ['picList', 'gifList', 'vidList']:
                    for serverFileName, datalayer in typelayer.items():
                        url = datalayer.get('url')
                        fileName = '{}_{}_{}'.format(
                            userName, datalayer.get('twtId'), serverFileName)
                        filePath = '{}/{}'.format(savePath, fileName)
                        if os.path.exists(filePath):
                            done.put('done')
                            continue
                        if os.path.exists(f'{filePath}'):
                            continue
                        if downloader(client, url, filePath, fileName):
                            done.put('done')
                else:
                    for twtId, content in typelayer.items():
                        fileName = '{}_{}.txt'.format(
                            userName, twtId)
                        filePath = '{}/{}'.format(savePath, fileName)
                        if saveText(filePath, content['content'], content['date']):
                            done.put('done')


def saveText(filePath, content, date):
    if os.path.exists(filePath):
        return True
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(f'{date}\n\n')
        f.write(content)
    return True


def getResult(tweet):
    getresult = lambda result: result if result['__typename'] == 'Tweet' else \
        (result['tweet'] if result['__typename'] == 'TweetWithVisibilityResults' else
         (None if result['__typename'] == 'TweetTombstone' else None))
    if 'entryId' not in tweet:
        return tweet
    if tweet['content']['entryType'] == 'TimelineTimelineItem':
        if 'tweetDisplayType' in tweet['content']['itemContent'] and \
                tweet['content']['itemContent']['tweetDisplayType'] == 'Tweet':
            result = getresult(tweet['content']['itemContent']['tweet_results']['result'])
            return result
        else:
            return None
    elif tweet['content']['entryType'] == 'TimelineTimelineModule':
        if 'tweetDisplayType' in tweet['content'] and \
                tweet['content']['tweetDisplayType'] == 'VerticalConversation':
            result = getresult(tweet['content']['items'][-1]['item']['tweet_results']['result'])
            return result
        else:
            return None
    else:
        print(parse_warning.format(tweet))
        return None


def getTweet(pageContent, cursor=None, isfirst=False):
    if 'errors' in pageContent:
        message = pageContent['errors'][0]['message']
        print(f'推文已删除/不存在：{message}')
        return None, None
    elif 'globalObjects' in pageContent:  # 搜索接口
        entries = pageContent['globalObjects']['tweets'].values()
        if not entries and isfirst:
            print('\r请获取cookie')
        cursor = pageContent['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value'] \
            if len(entries) != 0 and pageContent['timeline']['instructions'][0]['addEntries']['entries'][-1]['entryId'] == 'sq-cursor-bottom' \
            else (pageContent['timeline']['instructions'][-1]['replaceEntry']['entry']['content']['operation']['cursor']['value']
                  if len(pageContent['timeline']['instructions']) != 1 and pageContent['timeline']['instructions'][-1]['replaceEntry']['entryIdToReplace'] == 'sq-cursor-bottom' else None)
    elif 'user' in pageContent['data']:
        result = pageContent['data']['user']['result']
        if result['__typename'] == 'UserUnavailable':
            print(user_unavailable_warning)
            return None, None
        elif result['__typename'] == 'Age-restricted adult content':
            print(age_restricted_warning)
            return None, None
        elif not result['timeline_v2']:
            print(need_cookie_warning)
            return None, None
        instructions = result['timeline_v2']['timeline']['instructions']
        for instruction in instructions:
            if instruction['type'] == 'TimelineAddEntries':
                entries = instruction['entries']
                cursor = entries[-1]['content']['value'] if len(entries) != 0 else None
                break
    elif 'threaded_conversation_with_injections_v2' in pageContent['data']:
        entries = pageContent['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']
    if len(entries) == 0 or len(entries) == 2 and 'entryId' in entries[-1] and 'cursor-bottom' in entries[-1]['entryId']:  # 搜索接口返回的entries不包括cursor
        return None, None
    tweets = []
    for tweet in entries:
        if 'entryId' in tweet and 'tweet-' in tweet['entryId']:
            tweets.append(tweet)
        elif 'entryId' not in tweet:
            tweets.append(tweet)
    return tweets, cursor


def parseData(pageContent, total, userName, dataList, user_id=None, rest_id_list=None, cursor=None):
    if rest_id_list is None:
        rest_id_list = []
    if cursor:
        tweet_list, cursor = getTweet(pageContent)
    else:
        tweet_list, cursor = getTweet(pageContent, isfirst=True)
    if not tweet_list:
        return cursor, rest_id_list
    for tweet in tweet_list:
        picDic = {}
        gifDic = {}
        vidDic = {}
        textDic = {}
        result = getResult(tweet)
        if not result:
            continue
        if 'legacy' in result and 'retweeted_status_result' in result['legacy']:  # 转推
            if getContext('retweeted'):
                result = result['legacy']['retweeted_status_result']['result']['tweet'] \
                    if 'tweet' in result['legacy']['retweeted_status_result']['result'] \
                    else result['legacy']['retweeted_status_result']['result']
            else:
                continue
        legacylist = [[result['rest_id'] if 'rest_id' in result else result['id_str'], result['legacy'] if 'legacy' in result else result]]
        media_type = getContext('type').split('&')
        if getContext('quoted'):  # 包括引用，如 https://twitter.com/Liyu0109/status/1611734998402633728
            if 'quoted_status_result' in result and 'legacy' in result['quoted_status_result']['result']:  # 判断是否有引用，以及引用是否能查看，搜索接口的引用tweet直接在tweet_list里面，其他接口则嵌套在result里面
                legacylist.append([result['quoted_status_result']['result']['rest_id'], result['quoted_status_result']['result']['legacy']])
        else:
            if 'quoted_status_id_str' in result and result['user_id_str'] != user_id:  # 搜索接口的去除引用的方法是对比tweet的user_id_str是否等于userId,仅限@user等于from：user
                continue
        for twtId, legacy in legacylist:
            if twtId in rest_id_list:
                continue
            else:
                rest_id_list.append(twtId)
            if 'extended_entities' in legacy:
                for media in legacy['extended_entities']['media']:
                    # get pic links
                    if media['type'] == 'photo' and media['type'] in media_type:  # photo
                        # get {'url', url}, add query '?name=orig' can get original pic file
                        url = media['media_url_https']
                        picDic[url.split('/')[-1]] = {'url': url + '?name=orig', 'twtId': twtId}
                        if url:
                            total.put('add')
                    # get gif links(.mp4)
                    elif media['type'] == 'animated_gif' and media['type'] in media_type:  # gif
                        # [{'bitrate':filesize',url':url}]
                        variants = media['video_info']['variants'][0]
                        url = variants['url']
                        gifDic[url.split('/')[-1]] = {'url': url, 'twtId': twtId}
                        if url:
                            total.put('add')

                    # get video links(.mp4)
                    elif media['type'] == 'video' and media['type'] in media_type:  # video
                        # [{'bitrate':filesize',url':url},{}...] choose largest resolution
                        variants = sorted(media['video_info']['variants'],
                                          key=lambda s: s['bitrate'] if 'bitrate' in s else 0, reverse=True)[0]
                        url = variants['url']
                        vidDic[url.split('/')[-1].split('?')[0]] = {'url': url, 'twtId': twtId}
                        if url:
                            total.put('add')

                    elif media['type'] and media['type'] not in ['video', 'animated_gif', 'photo']:
                        print('解析失败：', media)

            # get twt text content,Ignore empty text
            if legacy['full_text'] and 'full_text' in media_type:
                textDic[twtId] = {
                    'content': legacy['full_text'],
                    'date': time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(legacy['created_at'], "%a %b %d %H:%M:%S +0000 %Y"))
                }
                total.put('add')
        data = {
            f'{userName}': {
                'picList': dict(**picDic),
                'gifList': dict(**gifDic),
                'vidList': dict(**vidDic),
                'textList': dict(**textDic)
            }
        }
        dataList.put(data)
    return cursor, rest_id_list


def checkUpdate():
    # 从本地缓存获取更新信息
    updateInfo = getContext('updateInfo')
    date = time.strftime("%m-%d", time.localtime())

    tagName = updateInfo['tagName']
    name = updateInfo['name']

    if updateInfo['LastCheckDate'] != date:
        # 从api获取更新信息
        try:
            response = httpx.get(checkUpdateApi, proxies=getContext('proxy'), verify=False)
            jsonData = response.json()
        except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError) as e:
            print(check_update_warning.format(e))
            return

        # api返回数据不正确, 一般是触发频限了
        if "tag_name" not in jsonData:
            print(check_update_warning.format(jsonData))
            return

        tagName = jsonData["tag_name"]
        name = jsonData["name"]
        updateInfo['LastCheckDate'] = date

    # 存在新版本，弹出更新文本提示
    if tagName and version != tagName:
        print("发现新版本: {}\n下载地址: {}\n".format(name, release_page))
        # 覆盖本地缓存数据
        updateInfo['tagName'] = tagName
        updateInfo['name'] = name

    setContext('updateInfo', updateInfo)
    saveEnv()
