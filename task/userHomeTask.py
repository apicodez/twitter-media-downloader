#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/1/13 19:27
# @Author  : 178
import time
import httpx

from common.const import *
from common.text import *
from common.tools import getHttpText
from task.baseTask import Task


class UserHomeTask(Task):

    def __init__(self, userName, userId, cfg):
        super(UserHomeTask, self).__init__()
        self.userName = userName
        self.userId = userId
        self.cfg = cfg
        self.savePath = '{}/{}'.format(getContext('dl_path'), userName)

    def getDataList(self, cursor='', rest_id_list=[]):
        while True:
            if self.stop:
                return
            cursorPar = cursor and '"cursor":"{}",'.format(cursor)
            response = None
            with httpx.Client(proxies=getContext('proxy'), headers=getContext('headers'), verify=False) as client:
                for i in range(1, 6):
                    try:
                        response = client.get(userHomeApi, params={
                            'variables': userHomeApiPar.format(self.userId, twtCount, cursorPar),
                            'features': commonApiPar})
                        break
                    except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError, httpx.RemoteProtocolError):
                        if i >= 5:
                            print(network_error_warning)
                            return False
                        else:
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
            self.pageContent = response.json()
            cursor, rest_id_list = self.parseData(cursor, rest_id_list)
            if not cursor:
                break