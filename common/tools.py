'''
Author: mengzonefire
Date: 2021-09-21 09:20:04
LastEditTime: 2022-09-29 20:29:05
LastEditors: mengzonefire
Description: 工具模块
'''

import sys
import time
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
        setContext('proxy', {'http': 'http://'+proxy_server,
                   'https': 'http://'+proxy_server})


def getHeader():  # 获取游客token
    headers = getContext('headers')
    if headers['Cookie']:  # 已设置cookie, 无需游客token
        return
    response = getContext('globalSession').post(hostUrl, proxies=getContext('proxy'),
                                                headers=headers, timeout=5).json()
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
        setContext('proxy', {'http': 'http://' + proxy_str,
                   'https': 'https://' + proxy_str})
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
            setContext('headers', headers)


def getUserId(userName: str):
    response = getContext('globalSession').post(userInfoApi, params={'variables': userInfoApiPar.format(
        userName)}, proxies=getContext('proxy'), headers=getContext('headers'))
    if response.status_code != 200:
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


def downloadFile(url, fileName, savePath):
    prog_text = '\r正在下载: {}'.format(fileName) + ' ...{}'
    filePath = '{}/{}'.format(savePath, fileName)
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    if os.path.exists(filePath):
        print(prog_text.format('文件已存在'))
        return
    print(prog_text.format('0%'), end="")
    response = getContext('globalSession').get(
        url, proxies=getContext('proxy'), headers=getContext('headers'), stream=True)
    if response.status_code != 200:
        print(http_warning.format('downloadFile',
              response.status_code, getHttpText(response.status_code)))
        return
    dl_size = 0
    content_size = 0
    if 'content-length' in response.headers:
        content_size = int(response.headers['content-length'])
    elif 'Content-Length' in response.headers:
        content_size = int(response.headers['Content-Length'])
    with open(filePath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024 * 2):
            f.write(chunk)
            if content_size:
                dl_size += len(chunk)
                prog = '{}%'.format(
                    int(round(dl_size / content_size, 2) * 100))
                print(prog_text.format(prog), end="")
    print(prog_text.format('下载完成'))
    time.sleep(1)


def saveText(content, fileName, savePath):
    if p_tw_link_text.match(content):  # 跳过空的文本内容
        return
    filePath = '{}/{}'.format(savePath, fileName)
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    if os.path.exists(filePath):
        return
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(content)


def parseData(strContent, twtId):
    picDic = {}
    gifDic = {}
    vidDic = {}
    textDic = {}

    # get pic links
    pic_links = p_pic_link.findall(strContent)
    # get [(media_url, file_name)], add query '?name=orig' can get original pic file
    if pic_links:
        for pic_link in pic_links:
            picDic[pic_link[1]] = {'url': pic_link[0] +
                                   '?name=orig', 'twtId': twtId}

    # get gif links(.mp4)
    gif_links = p_gif_link.findall(strContent)
    # get [(media_url, file_name)]
    if gif_links:
        for gif_link in gif_links:
            gifDic[gif_link[1]] = {'url': gif_link[0], 'twtId': twtId}

    # get video links(.mp4)
    vid_links = p_vid_link.findall(strContent)
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
        vidDic[best_choice['file_name']] = {
            'url': best_choice['url'], 'twtId': twtId}

    # get twt text content
    twtText = p_text_content.findall(strContent)
    if twtText:
        textDic = {twtId: twtText[0]}

    # return {serverFileName: {url: , twtId: }}
    return picDic, gifDic, vidDic, textDic


def checkUpdate():
    # 从本地缓存获取更新信息
    updateInfo = getContext('updateInfo')
    date = time.strftime("%m-%d", time.localtime())

    tagName = updateInfo['tagName']
    name = updateInfo['name']

    if updateInfo['LastCheckDate'] != date:
        # 从api获取更新信息
        response = requests.get(checkUpdateApi, proxies=getContext('proxy'))
        jsonData = response.json()

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
