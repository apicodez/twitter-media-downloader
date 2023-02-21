'''
Author: mengzonefire
Date: 2021-09-21 09:19:02
LastEditTime: 2023-02-22 03:02:59
LastEditors: mengzonefire
Description: 推主推文批量爬取任务类
'''
import time
import httpx

from common.const import *
from common.text import *
from common.tools import getHttpText, parseData
from task.baseTask import Task


class UserMediaTask(Task):
    userId: int

    def __init__(self, userName: str, userId: int):
        super(UserMediaTask, self).__init__()
        self.userName = userName
        self.userId = userId
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
                        response = client.get(userMediaApi, params={
                            'variables': userMediaApiPar.format(self.userId, twtCount, cursorPar),
                            'features': userMediaApiPar2})
                    break
                except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError, httpx.RemoteProtocolError):
                    print(timeout_warning.format(i))
                time.sleep(1)
            if not response:
                self.stopGetDataList()
                return
            if response.status_code != httpx.codes.OK:
                print(http_warning.format('UserMediaTask.getDataList',
                                          response.status_code, getHttpText(response.status_code)))
                self.stopGetDataList()
                return
            pageContent = response.json()
            cursor, rest_id_list = parseData(
                pageContent, self.total, self.userName, self.dataList, rest_id_list=rest_id_list)
            if not cursor:
                self.stopGetDataList()
                return
