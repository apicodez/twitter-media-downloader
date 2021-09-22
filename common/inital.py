'''
Author: mengzonefire
Date: 2021-09-21 09:20:04
LastEditTime: 2021-09-22 14:38:16
LastEditors: mengzonefire
Description: 程序初始化
'''
import sys
import argparse
from argparse import RawTextHelpFormatter
from const import url_args_help, host_url, setContext, getContext
from text import *
if sys.platform in ['win32', 'win64']:
    import winreg


def inital():
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


def get_proxy():
    global proxy
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings")
    proxy_enable, key_type = winreg.QueryValueEx(key, "ProxyEnable")
    if proxy_enable:
        proxy_server, key_type = winreg.QueryValueEx(key, "ProxyServer")
        proxy = {'http': 'http://'+proxy_server,
                 'https': 'https://'+proxy_server}


def set_header():
    headers = getContext('headers')
    s = getContext('globalSession')
    if headers['Cookie']:
        return
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
