'''
Author: mengzonefire
Date: 2023-03-01 09:46:48
LastEditTime: 2023-03-10 04:57:41
LastEditors: mengzonefire
Description: 关注列表爬取任务类
'''

import json
import time
import httpx

from common.const import *
from common.logger import writeLog
from common.text import *
from common.tools import getFollower, getHttpText


class UserFollowingTask():
    dataList = []
    stop = False
    pageContent = None

    def __init__(self, userName: str, userId: int):
        self.userName = userName
        self.userId = userId
        self.savePath = os.path.join(getContext('dl_path'), userName)

    def getDataList(self, cursor=''):
        while True:
            cursorPar = cursor and '"cursor":"{}",'.format(cursor)
            response = None
            for i in range(1, 6):
                try:
                    with httpx.Client(proxies=getContext('proxy'), headers=getContext('headers'), verify=False) as client:
                        response = client.get(userFollowingApi, params={
                            'variables': userFollowingApiPar.format(self.userId, twtCount, cursorPar),
                            'features': commonApiPar})
                    break
                except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError, httpx.RemoteProtocolError):
                    if i >= 5:
                        print(network_error_warning)
                        return
                    else:
                        print(timeout_warning.format(i))
                time.sleep(1)
            if not response:
                return
            if response.status_code != httpx.codes.OK:
                print(http_warning.format('UserFollowingTask.getDataList',
                                          response.status_code, getHttpText(response.status_code)))
                return
            self.pageContent = response.json()
            cursor = getFollower(self.pageContent, self.dataList)
            if not cursor:
                return

    def saveDataList(self):
        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)
        with open(os.path.join(self.savePath, 'following.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.dataList))

    def start(self):
        self.getDataList()
        if len(self.dataList):
            self.saveDataList()
            print(fo_Task_finish.format(
                os.path.join(self.savePath, 'following.txt')))
        elif self.pageContent:
            print(dl_nothing_warning)
            writeLog(f'{self.userName}_noFollowing',
                     json.dumps(self.pageContent))  # debug
