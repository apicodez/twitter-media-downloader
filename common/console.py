'''
Author: mengzonefire
Date: 2021-09-21 09:20:19
LastEditTime: 2021-09-25 17:54:41
LastEditors: mengzonefire
Description: 
'''
import os
from task.singlePageTask import SinglePageTask
from task.userMediaTask import UserMediaTask
from typing import List
from text import *
from const import *
from common.tools import get_token, getUserId, saveEnv


def cmdMode():
    url_list = []
    print(input_ask)
    while True:
        temp = input()
        if not temp:
            break
        if '//t.co/' in temp or '//twitter.com/' in temp:
            url_list.append(temp)
        else:
            cmdCommand(temp)
            return
    if url_list:
        startCrawl(url_list)

    if input(continue_ask):
        cmdMode()


def startCrawl(url_list: List):
    dl_path = getattr('dl_path')
    if not os.path.exists(dl_path):
        os.mkdir(dl_path)

    for page_url in url_list:
        print('\n正在提取: {}'.format(page_url))
        urlHandler(page_url)


def urlHandler(url: str):
    # userHomePage
    user_link = p_user_link.findall(url)
    if user_link:
        userName = user_link[0]
        userId = getUserId(userName)
        if userId:
            UserMediaTask(userName, userId).start
        return

    # SinglePage
    twt_link = p_twt_link.findall(url)
    if twt_link:
        userName = twt_link[0]
        twtId = twt_link[1]
        SinglePageTask(twtId, userName).start()
        return


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
