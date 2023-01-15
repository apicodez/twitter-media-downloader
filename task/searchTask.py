#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/1/13 17:17
# @Author  : 178
import time
import json
import httpx

from common.const import *
from common.text import *
from common.tools import getHttpText, parseData
from task.baseTask import Task


class UserSearchTask(Task):

    def __init__(self, userName, userId, date, advanced):
        super(UserSearchTask, self).__init__()
        self.date = date
        self.advanced = advanced
        self.userName = userName
        self.userId = userId
        self.savePath = '{}/{}'.format(getContext('dl_path'), userName)

    def getDataList(self, cursor='', rest_id_list=None):
        while True:
            if self.stop:
                return
            cursorPar = cursor and '"cursor":"{}",'.format(cursor)
            if self.advanced:
                q = f'{self.advanced}'
            elif self.date:
                q = f'(from:{self.userName}) until:{self.date[1]} since:{self.date[0]} -filter:replies'
            else:
                q = f'(from:{self.userName}) -filter:replies'
            params = json.loads(
                userSearchApiPar.format(q, twtCount, cursorPar))
            response = None
            for i in range(1, 6):
                try:
                    with httpx.Client(proxies=getContext('proxy'), headers=getContext('headers'), verify=False) as client:
                        response = client.get(userSearchApi, params=params)
                    break
                except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError, httpx.RemoteProtocolError):
                    print(timeout_warning.format(i))
                time.sleep(1)
            if not response:
                self.stopGetDataList()
                return
            if response.status_code != httpx.codes.OK:
                print(http_warning.format('SearchTask.getDataList',
                                          response.status_code, getHttpText(response.status_code)))
                self.stopGetDataList()
                return
            pageContent = response.json()
            cursor, rest_id_list = parseData(
                pageContent, self.total, self.userName, self.dataList, self.userId, rest_id_list, cursor)
            if not cursor:
                self.stopGetDataList()
                return
