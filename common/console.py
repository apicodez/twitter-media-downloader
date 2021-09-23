'''
Author: mengzonefire
Date: 2021-09-21 09:20:19
LastEditTime: 2021-09-23 11:38:37
LastEditors: mengzonefire
Description: 
'''
from text import *
from const import getContext, setContext
from common.tools import get_token, saveEnv


def cmdMode():
    twt_page = []
    user_page = []
    print(input_ask)
    while True:
        temp = input()
        if not temp:
            break
        if '//t.co/' in temp or '//twitter.com/' in temp:
            page_urls.append(temp)
        else:
            cmdCommand(temp)
            return
    if page_urls:
        start_crawl(page_urls)

    if input(continue_ask):
        cmdMode()


def cmdCommand(command):
    if command == 'exit':
        return
    elif command == 'set cookie':
        cookie = input(input_cookie_ask)
        token = get_token(cookie)
        if token:
            headers = getContext("headers")
            headers['x-csrf-token'] = token
            headers['Cookie'] = cookie
            setContext('headers', headers)
            saveEnv()
    else:
        print(input_warning)
    cmdMode()
