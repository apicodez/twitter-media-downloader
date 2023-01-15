'''
Author: mengzonefire
Date: 2021-09-21 09:18:34
LastEditTime: 2022-09-29 20:14:27
LastEditors: mengzonefire
Description: 单推文爬取任务类
'''
import time
import httpx

from common.const import *
from common.text import *
from common.tools import getHttpText, parseData
from task.baseTask import Task


class SinglePageTask(Task):
    twtId = ''

    def __init__(self, userName, twtId):
        super(SinglePageTask, self).__init__()
        self.twtId = twtId
        self.userName = userName
        self.savePath = '{}/{}'.format(getContext('dl_path'), userName)

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

        page_content = response.json()
        # write_log(self.twtId, str(page_content))  # debug
        parseData(page_content, self.total, self.userName, self.dataList)
        self.stopGetDataList()
        return
