'''
Author: mengzonefire
Date: 2021-09-21 09:18:34
LastEditTime: 2023-03-15 00:33:18
LastEditors: mengzonefire
Description: 单推文爬取任务类
'''

import time
import httpx

from common.text import *
from common.const import *
from common.tools import getHttpText
from task.baseTask import Task


class SinglePageTask(Task):

    def __init__(self, userName: str, twtId: int, cfg):
        super(SinglePageTask, self).__init__()
        self.twtId = twtId
        self.userName = userName
        self.cfg = cfg
        self.savePath = os.path.join(getContext('dl_path'), userName)

    def getDataList(self):
        response = None
        with httpx.Client(proxies=getContext('proxy'), headers=getContext('headers'), verify=False) as client:
            for i in range(1, 6):
                try:
                    response = client.get(singlePageApi, params={
                        'variables': singlePageApiPar.format(self.twtId),
                        'features': commonApiPar})
                    break
                except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError):
                    if i >= 5:
                        print(network_error_warning)
                        self.stopGetDataList()
                        return
                    else:
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
        self.parseData('', [])
