#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/1/13 19:27
# @Author  : 178
import time
import httpx

from common.const import *
from common.text import *
from common.tools import getHttpText, parseData
from task.baseTask import Task


class UserHomeTask(Task):

    def __init__(self, userName: str, userId: int):
        super(UserHomeTask, self).__init__()
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
                        response = client.get(userHomeApi, params={
                            'variables': userHomeApiPar.format(self.userId, twtCount, cursorPar),
                            'features': userHomeApiPar2})
                    break
                except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError, httpx.RemoteProtocolError):
                    print(timeout_warning.format(i))
                time.sleep(1)
            if not response:
                self.stopGetDataList()
                return
            if response.status_code != httpx.codes.OK:
                print(http_warning.format('UserHomeTask.getDataList',
                                          response.status_code, getHttpText(response.status_code)))
                self.stopGetDataList()
                return
            pageContent = response.json()
            cursor, rest_id_list = parseData(
                pageContent, self.total, self.userName, self.dataList, rest_id_list=rest_id_list)
            if not cursor:
                self.stopGetDataList()
                return
