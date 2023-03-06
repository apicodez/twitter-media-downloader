'''
Author: mengzonefire
Date: 2023-03-01 13:58:17
LastEditTime: 2023-03-06 15:44:42
LastEditors: mengzonefire
Description: likes页爬取任务类
'''

import time
import httpx

from common.const import *
from common.text import *
from common.tools import getHttpText, parseData
from task.baseTask import Task


class UserLikesTask(Task):

    def __init__(self, userName: str, userId: int, media: bool):
        super(UserLikesTask, self).__init__()
        self.userName = userName
        self.userId = userId
        self.media = media
        self.savePath = '{}/{}'.format(getContext('dl_path'), userName)

    def getDataList(self, cursor='', rest_id_list=None):
        while True:
            if self.stop:
                return
            cursorPar = cursor and '"cursor":"{}",'.format(cursor)
            response = None
            for i in range(1, 6):
                try:
                    with httpx.Client(proxies=getContext('proxy'), headers=getContext('headers'), verify=False) as client:
                        response = client.get(userLikesApi, params={
                            'variables': userLikesApiPar.format(self.userId, twtCount, cursorPar),
                            'features': commonApiPar})
                    break
                except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError, httpx.RemoteProtocolError):
                    print(timeout_warning.format(i))
                time.sleep(1)
            if not response:
                self.stopGetDataList()
                return
            if response.status_code != httpx.codes.OK:
                print(http_warning.format('UserLikesTask.getDataList',
                                          response.status_code, getHttpText(response.status_code)))
                self.stopGetDataList()
                return
            self.pageContent = response.json()
            cursor, rest_id_list = parseData(
                self.pageContent, self.total, self.userName, self.dataList, rest_id_list=rest_id_list)
            if not cursor:
                self.stopGetDataList()
                return
