'''
Author: mengzonefire
Date: 2021-09-21 09:18:34
LastEditTime: 2023-03-06 15:38:54
LastEditors: mengzonefire
Description: 单推文爬取任务类
'''

import json
import time
import httpx

from common.text import *
from common.const import *
from common.logger import writeLog
from common.tools import getHttpText, parseData
from task.baseTask import Task


class SinglePageTask(Task):

    def __init__(self, userName: str, twtId: int):
        super(SinglePageTask, self).__init__()
        self.twtId = twtId
        self.userName = userName
        self.savePath = os.path.join(getContext('dl_path'), userName)

    def getDataList(self):
        response = None
        for i in range(1, 6):
            try:
                with httpx.Client(proxies=getContext('proxy'), headers=getContext('headers'), verify=False) as client:
                    response = client.get(singlePageApi, params={
                        'variables': singlePageApiPar.format(self.twtId),
                        'features': singlePageApiPar2})
                break
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError):
                print(timeout_warning.format(i))
            time.sleep(1)
        if not response:
            self.stopGetDataList()
            return
        if response.status_code != httpx.codes.OK:
            print(http_warning.format('SinglePageTask.getDataList',
                                      response.status_code, getHttpText(response.status_code)))
            self.stopGetDataList()
            return

        self.pageContent = response.json()
        parseData(self.pageContent, self.total, self.userName, self.dataList)
        self.stopGetDataList()
        return
