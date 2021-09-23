'''
Author: mengzonefire
Date: 2021-09-21 09:20:19
LastEditTime: 2021-09-23 15:17:46
LastEditors: mengzonefire
Description: 
'''
import os
from typing import List
from text import *
from const import *
from common.tools import get_token, saveEnv


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
                        download_media(
                            user_media_links[file_name], file_name, save_path)
            else:
                print(nothing_warning)
            continue

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


def urlHandler(url: str):
    user_link = p_user_link.findall(url)
    if user_link:
        user_name = user_link[0]
        return

    page_id = p_tw_link.findall(url)
    if page_id:
        page_id = page_id[0]
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
