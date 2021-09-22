'''
Author: mengzonefire
Date: 2021-09-21 09:20:04
LastEditTime: 2021-09-22 19:09:45
LastEditors: mengzonefire
Description: 工具模块
'''
import sys
import argparse
from argparse import RawTextHelpFormatter
from const import *
from text import *
if sys.platform in ['win32', 'win64']:
    import winreg


def initalArgs():
    # prog argument
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-c', '--cookie', dest='cookie', type=str,
                        help='set cookie to access locked users or tweets')
    parser.add_argument('-p', '--proxy', dest='proxy', type=str,
                        help='set network proxy, must be http proxy')
    parser.add_argument('-u', '--user_agent', dest='user_agent',
                        type=str, help='set user-agent')
    parser.add_argument('-d', '--dir', dest='dir',
                        type=str, help='set download path')
    parser.add_argument('-v', '--version', action='store_true',
                        help='show version')
    parser.add_argument('url', type=str, nargs='*', help=url_args_help)
    args = parser.parse_args()
    setContext('args', args)


def getProxy():
    if getContext('proxy'):
        return
    if sys.platform not in ['win32', 'win64']:
        return
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings")
    proxy_enable, key_type = winreg.QueryValueEx(key, "ProxyEnable")
    if proxy_enable:
        proxy_server, key_type = winreg.QueryValueEx(key, "ProxyServer")
        setContext('proxy', {'http': 'http://'+proxy_server,
                   'https': 'https://'+proxy_server})


def getHeader():  # 获取游客token
    headers = getContext('headers')
    if headers['Cookie']:  # 已设置cookie, 无需游客token
        return
    proxy = getContext('proxy')
    s = getContext('globalSession')
    response = s.post(host_url, proxies=proxy,
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
    if cookie[-1] == ';':
        print(cookie_para_warning)
        return None
    csrf_token = p_csrf_token.findall(cookie)
    if csrf_token and 'auth_token' in cookie:
        print(cookie_success)
        return csrf_token[0]
    else:
        print(cookie_warning)
        return None


def set_proxy(proxy_str):
    proxy_match = p_proxy.match(proxy_str)
    if proxy_match and 1024 <= int(proxy_match.group(1)) <= 65535:
        setContext('proxy', {'http': 'http://' + proxy_str,
                   'https': 'https://' + proxy_str})
        print('代理设置为: {}'.format(proxy_str))
    else:
        print(proxy_warning)


def argsHandler():
    args = getContext('args')
    headers = getContext('headers')
    if args.version:
        print('version: {}\nissue page: {}'.format(version, issue_page))
        return
    if args.proxy:
        set_proxy(args.proxy)
    elif sys.platform in ['win32', 'win64']:
        getProxy()
    if args.cookie:
        token = get_token(args.cookie)
        if token:
            headers['x-csrf-token'] = token
            headers['Cookie'] = args.cookie
        else:
            return
    if args.user_agent:
        headers['User-Agent'] = args.user_agent
    if args.dir:
        setContext('dl_path', args.dir)
    setContext('header', headers)


def saveEnv():
    conf.read(conf_path)
    if 'global' not in conf.sections():
        conf.add_section('global')
    conf.set("global", "proxy", getContext("proxy"))
    conf.set("global", "download_path", getContext("dl_path"))
    conf.set("global", "user-agent", getContext("headers")["User-Agent"])
    conf.set("global", "cookie", getContext("headers")['Cookie'])
    conf.write(open(conf_path, 'w'))


def setEnv():
    if os.path.exists(conf_path):
        conf.read(conf_path)
        if 'global' in conf.sections():
            headers = getContext("headers")
            items = conf.items('global')
            for item in items:
                if item[0] == 'cookie':
                    token = get_token(item[1])
                    if token:
                        headers['x-csrf-token'] = token
                        headers['Cookie'] = item[1]
                elif item[0] == 'user-agent':
                    headers['User-Agent'] = item[1]
                elif item[0] == 'proxy':
                    set_proxy(item[1])
                elif item[0] == 'download_path':
                    setContext('dl_path', item[1])
            setContext('headers', headers)
