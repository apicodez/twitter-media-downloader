'''
Author: mengzonefire
Date: 2021-09-21 09:20:04
LastEditTime: 2023-03-06 03:25:40
LastEditors: mengzonefire
Description: 工具模块, 快1k行了, 抽空分模块拆分一下
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
isWinPlatform = sys.platform in ['win32', 'win64']
if isWinPlatform:
    import winreg


def clear():
    if sys.platform in ['win32', 'win64']:  # 判断是否为win平台
        os.system('cls')
    else:
        os.system('clear')


def getHttpText(httpCode: int):
    if httpCode in httpCodeText:
        return httpCodeText[httpCode]
    return f'请前往issue页反馈:\n{issue_page}'


def initalArgs():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-c', '--cookie', dest='cookie', type=str,
                        help='for access locked users&tweets, will save to cfg file, input " " to clear')
    parser.add_argument('-p', '--proxy', dest='proxy', type=str,
                        help="support http&socks5, default use system proxy(win only)")
    parser.add_argument('-d', '--dir', dest='dir',
                        type=str, help='set download path')
    parser.add_argument('-n', '--num', dest='concurrency', type=int,
                        help='downloader concurrency')
    parser.add_argument('-t', '--type', dest='type', type=str,
                        help='desired media type, optional: photo&animated_gif&video&full_text')
    parser.add_argument('-m', '--meida', action="store_true", dest='meida',
                        help='exclude non-media tweets')
    parser.add_argument('-q', '--quoted', action="store_true", dest='quoted',
                        help='exclude quoted tweets')
    parser.add_argument('-r', '--retweeted', action="store_true", dest='retweeted',
                        help='exclude retweeted')
    parser.add_argument('-v', '--version', action='store_true',
                        help='show version and check update')
    parser.add_argument('url', type=str, nargs='*', help=url_args_help)
    args = parser.parse_args()
    setContext('args', args)


def argsHandler():
    args = getContext('args')
    if args.version:
        print('version: {}\ndonate page: {}\nissue page: {}\n'.format(
            version, donate_page, issue_page))
        checkUpdate()
        return
    if args.proxy:
        if not setProxy(args.proxy):
            return
    else:
        getSysProxy()
    if args.cookie:
        if not setCookie(args.cookie):
            return
    else:
        getGuestCookie()
    if args.dir:
        setContext('dl_path', args.dir)
    if args.concurrency:
        setContext('concurrency', args.concurrency)
    if args.type:
        setContext('type', args.type)
    setContext('media', args.media)
    setContext('quoted', not args.quoted)
    setContext('retweeted', not args.retweeted)


def getGuestCookie():  # 获取游客token
    headers = getContext('headers')
    if headers['Cookie']:  # 已配置cookie, 无需游客token
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


def getToken(cookie):  # 从cookie内提取csrf token
    csrf_token = p_csrf_token.findall(cookie)
    if len(csrf_token) != 0:
        return csrf_token[0]
    else:
        return None


def getSysProxy():
    if getContext('proxy'):  # 已配置, 跳过
        return
    if isWinPlatform:  # 非win平台, 跳过
        return
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings")
    proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
    if proxy_enable:
        proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
        setContext('proxy', f'http://{proxy_server}')


def setCookie(cookie=''):  # 设置cookie
    inputFlag = False
    headers = getContext("headers")
    if not cookie:  # 输入cookie
        clear()
        inputFlag = True
        cookie = input(input_cookie_ask).strip()
    elif cookie == ' ':  # 清除cookie
        cookie = ''
    elif cookie == '0':
        return True
    else:
        cookie = cookie.strip()
    if cookie:   # 设置cookie
        token = getToken(cookie)
        if token:
            headers['x-csrf-token'] = token
            headers['Cookie'] = cookie
        else:  # 格式错误
            if inputFlag:
                input(cookie_input_warning)
                return setCookie()
            else:
                print(cookie_arg_warning)
                return False
    else:
        headers['Cookie'] = ''
        getGuestCookie()  # 重新获取游客token
    setContext('headers', headers)
    saveEnv()
    return True


def setProxy(proxy=''):
    inputFlag = False
    if not proxy:  # 输入代理
        clear()
        inputFlag = True
        proxy = input(input_proxy_ask).strip()
        clear()
    elif proxy == '0':
        return True
    else:
        proxy = proxy.strip()
    proxyMatch = pProxy.match(proxy)
    proxyMatch2 = pProxy2.match(proxy)
    if proxyMatch2:
        setContext('proxy', proxy)
        return True
    elif proxyMatch:  # 不带协议默认为http
        setContext('proxy', f'http://{proxy}')
        return True
    else:  # 格式错误
        if inputFlag:
            input(proxy_input_warning)
            return setProxy()
        else:
            print(proxy_arg_warning)
            return False


'''
description: 保存配置到本地
'''


def saveEnv():
    conf.read(conf_path, encoding='utf-8')
    if 'global' not in conf.sections():
        conf.add_section('global')
    conf.set("global", "download_path", getContext("dl_path"))
    conf.set("global", "cookie", getContext("headers")['Cookie'])
    conf.set("global", "updateinfo", getContext("updateInfo"))
    conf.set("global", "concurrency", getContext("concurrency"))
    conf.set("global", "type", getContext("type"))
    conf.set("global", "quoted", getContext("quoted"))
    conf.set("global", "retweeted", getContext("retweeted"))
    conf.set("global", "media", getContext("media"))
    conf.write(open(conf_path, 'w', encoding='utf-8'))


'''
description: 从本地读取配置
'''


def getEnv():
    if os.path.exists(conf_path):
        conf.read(conf_path, encoding='utf-8')
        if 'global' in conf.sections():
            headers = getContext("headers")
            items = conf.items('global')
            for item in items:
                if item[0] == 'cookie' and item[1]:
                    token = getToken(item[1])
                    if token:
                        headers['x-csrf-token'] = token
                        headers['Cookie'] = item[1]
                elif item[0] == 'download_path' and item[1]:
                    setContext('dl_path', item[1])
                elif item[0] == 'updateinfo' and item[1]:
                    setContext('updateInfo', eval(item[1]))
                elif item[0] == 'concurrency' and item[1]:
                    setContext('concurrency', eval(item[1]))
                elif item[0] == 'type' and item[1]:
                    setContext('type', item[1])
                elif item[0] == 'media' and item[1]:
                    setContext('meida', eval(item[1]))
                elif item[0] == 'quoted' and item[1]:
                    setContext('quoted', eval(item[1]))
                elif item[0] == 'retweeted' and item[1]:
                    setContext('retweeted', eval(item[1]))
            setContext('headers', headers)


'''
description: 推主名 -> 推主id (用于接口请求参数)
param {str} userName 推主名
return {int|None} userId 推主id
'''


def getUserId(userName: str) -> int | None:
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
        return int(userId)
    else:
        print(user_warning)
        write_log(userName, page_content)
        return None


'''
description: 从直链下载文件
param {*} client 下载器对象
param {str} url 媒体直链
param {str} filePath 下载文件路径
param {str} fileName 文件名
return {bool} True下载成功, False下载失败
'''


def downloader(client, url: str, filePath: str, fileName: str) -> bool:
    for _ in range(1, 6):
        try:
            with client.stream('GET', url) as response:
                if response.status_code != httpx.codes.OK:
                    print(http_warning.format(
                        'downloadFile', response.status_code, getHttpText(response.status_code)))
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


'''
description: 下载任务队列中的直链
param {str} savePath 下载路径
param {queue} dataList 任务队列
param {queue} done 已完成队列
'''


def downloadFile(savePath: str, dataList: queue.Queue, done: queue.Queue, media: bool):
    isMediaTw = False
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
                        isMediaTw = True
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
                        if media and not isMediaTw:  # 过滤非媒体推文
                            done.put('done')
                        elif saveText(filePath, content['content'], content['date']):
                            done.put('done')


'''
description: 保存推文文本内容
param {str} filePath 写入文件路径
param {str} content 推文内容(文本)
param {str} date 推文发布日期
'''


def saveText(filePath: str, content: str, date: str):
    if os.path.exists(filePath):
        return True
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(f'{date}\n\n')
        f.write(content)
    return True


'''
description: 单条推文数据解析器
param {*} tweet 单条推文元数据
return {*} 解析出的目标数据(内含媒体url)
'''


def getResult(tweet):
    def getresult(result): return result if result['__typename'] == 'Tweet' else \
        (result['tweet'] if result['__typename'] == 'TweetWithVisibilityResults' else
         (None if result['__typename'] == 'TweetTombstone' else None))
    if 'entryId' not in tweet:
        return tweet
    if tweet['content']['entryType'] == 'TimelineTimelineItem':
        if 'tweetDisplayType' in tweet['content']['itemContent'] and \
                tweet['content']['itemContent']['tweetDisplayType'] == 'Tweet':
            result = getresult(
                tweet['content']['itemContent']['tweet_results']['result'])
            return result
        else:
            return None
    elif tweet['content']['entryType'] == 'TimelineTimelineModule':
        if 'tweetDisplayType' in tweet['content'] and \
                tweet['content']['tweetDisplayType'] == 'VerticalConversation':
            result = getresult(tweet['content']['items']
                               [-1]['item']['tweet_results']['result'])
            return result
        else:
            return None
    else:
        print(parse_warning.format(tweet))
        return None


'''
description: 从列表api元数据解析follow用户名列表
param {Dict} pageContent api返回的元数据
param {int} cursor api翻页锚点参数
param {List} dataList 数据容器
'''


def getFollower(pageContent, dataList: list, cursor=None):
    if 'user' in pageContent['data']:
        result = pageContent['data']['user']['result']
        if result['__typename'] == 'UserUnavailable':
            return
        instructions = result['timeline']['timeline']['instructions']
        for instruction in instructions:
            if instruction['type'] == 'TimelineAddEntries':
                entries = instruction['entries']
                if len(entries) == 0 or len(entries) == 2 and 'entryId' in entries[-2] and 'cursor-bottom' in entries[-2]['entryId']:
                    # 翻页完成, 无内容, 两个fo接口的entries[-1]为cursor-top, [-2]为cursor-bottom
                    return None
                cursor = entries[-2]['content']['value'] if len(
                    entries) != 0 else None
                break
    for entry in entries:
        dataList.append(entry['content']['itemContent']
                        ['user_results']['result']['legacy']['screen_name'])
    return cursor


'''
description: 从列表api元数据解析推文id列表
param {Dict} pageContent api返回的元数据
param {int} cursor api翻页锚点参数
param {bool} isfirst 是否为第一页
'''


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
                cursor = entries[-1]['content']['value'] if len(
                    entries) != 0 else None
                break
    elif 'threaded_conversation_with_injections_v2' in pageContent['data']:
        entries = pageContent['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']
    # 搜索接口返回的entries不包括cursor
    if len(entries) == 0 or len(entries) == 2 and 'entryId' in entries[-1] and 'cursor-bottom' in entries[-1]['entryId']:
        # 翻页完成, 无内容, 搜索/主页/媒体 接口的entries[-1]为cursor-bottom, [-2]为cursor-top
        return None, None
    tweets = []
    for tweet in entries:
        if 'entryId' in tweet and 'tweet-' in tweet['entryId']:
            tweets.append(tweet)
        elif 'entryId' not in tweet:
            tweets.append(tweet)
    return tweets, cursor


'''
description: api数据解析
param {*} pageContent api返回的元数据
param {*} total 任务总量计数器
param {*} userName 推主名
param {*} dataList 任务数据队列
param {*} user_id 推主id
param {*} rest_id_list 推文id列表
param {*} cursor api翻页锚点参数
'''


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
        # 转推
        if 'legacy' in result and 'retweeted_status_result' in result['legacy']:
            if getContext('retweeted'):
                result = result['legacy']['retweeted_status_result']['result']['tweet'] \
                    if 'tweet' in result['legacy']['retweeted_status_result']['result'] \
                    else result['legacy']['retweeted_status_result']['result']
            else:
                continue
        legacylist = [[result['rest_id'] if 'rest_id' in result else result['id_str'],
                       result['legacy'] if 'legacy' in result else result]]
        media_type = getContext('type').split('&')
        if getContext('quoted'):  # 包括引用，如 https://twitter.com/Liyu0109/status/1611734998402633728
            # 判断是否有引用，以及引用是否能查看，搜索接口的引用tweet直接在tweet_list里面，其他接口则嵌套在result里面
            if 'quoted_status_result' in result and 'legacy' in result['quoted_status_result']['result']:
                legacylist.append([result['quoted_status_result']['result']
                                  ['rest_id'], result['quoted_status_result']['result']['legacy']])
        else:
            # 搜索接口的去除引用的方法是对比tweet的user_id_str是否等于userId,仅限@user等于from：user
            if 'quoted_status_id_str' in result and result['user_id_str'] != user_id:
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
                        picDic[url.split(
                            '/')[-1]] = {'url': url + '?name=orig', 'twtId': twtId}
                        if url:
                            total.put('add')

                    # get gif links(.mp4)
                    elif media['type'] == 'animated_gif' and media['type'] in media_type:  # gif
                        # [{'bitrate':filesize',url':url}]
                        variants = media['video_info']['variants'][0]
                        url = variants['url']
                        gifDic[url.split('/')[-1]
                               ] = {'url': url, 'twtId': twtId}
                        if url:
                            total.put('add')

                    # get video links(.mp4)
                    elif media['type'] == 'video' and media['type'] in media_type:  # video
                        # [{'bitrate':filesize',url':url},{}...] choose largest resolution
                        variants = sorted(media['video_info']['variants'],
                                          key=lambda s: s['bitrate'] if 'bitrate' in s else 0, reverse=True)[0]
                        url = variants['url']
                        vidDic[url.split('/')[-1].split('?')[0]
                               ] = {'url': url, 'twtId': twtId}
                        if url:
                            total.put('add')
                    # fail
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


'''
description: 从github api获取新版本信息
'''


def checkUpdate():
    # 从本地缓存获取更新信息
    updateInfo = getContext('updateInfo')
    date = time.strftime("%m-%d", time.localtime())

    tagName = updateInfo['tagName']
    name = updateInfo['name']

    if updateInfo['LastCheckDate'] != date:
        # 从api获取更新信息
        try:
            response = httpx.get(
                checkUpdateApi, proxies=getContext('proxy'), verify=False)
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
    if tagName and compare_version(version, tagName) == 2:
        print("发现新版本: {}\n下载地址: {}\n".format(name, release_page))
        # 覆盖本地缓存数据
        updateInfo['tagName'] = tagName
        updateInfo['name'] = name
    else:
        print("当前版本已是最新")

    setContext('updateInfo', updateInfo)
    saveEnv()


'''
description: 显示配置
'''


def showConfig():
    print()


'''
description: 
param {str} version1 版本号1
param {str} version2 版本号2
param {str} split_flag 版本号分隔符
return {int} 0 1 2: 0为相等， 1为1大， 2为2大
'''


def compare_version(version1=None, version2=None, split_flag="."):
    if (version1 is None) or (version1 == "") or (version2 is None) or (version2 == ""):
        if ((version1 is None) or (version1 == "")) and (version2 is not None) and (version2 != ""):
            return 2
        if ((version2 is None) or (version2 == "")) and (version1 is not None) and (version1 != ""):
            return 1
    if version1 == version2:
        return 0
    try:
        current_section_version1 = version1[:version1.index(split_flag)]
    except:
        current_section_version1 = version1
    try:
        current_section_version2 = version2[:version2.index(split_flag)]
    except:
        current_section_version2 = version2
    if int(current_section_version1) > int(current_section_version2):
        return 1
    elif int(current_section_version1) < int(current_section_version2):
        return 2
    try:
        other_section_version1 = version1[version1.index(split_flag)+1:]
    except:
        other_section_version1 = ""
    try:
        other_section_version2 = version2[version2.index(split_flag) + 1:]
    except:
        other_section_version2 = ""
    return compare_version(other_section_version1, other_section_version2)


# 模块测试入口
if __name__ == '__main__':
    getSysProxy()
