'''
Author: mengzonefire
Date: 2021-09-21 09:18:34
LastEditTime: 2022-05-13 14:39:15
LastEditors: mengzonefire
Description: 单推文爬取任务类
'''
import json
from common.logger import write_log
from task.baseTask import Task
from common.tools import getHttpText, parseData
from common.text import *
from common.const import *


class SinglePageTask(Task):
    twtId = ''

    def __init__(self, userName, twtId):
        super(SinglePageTask, self).__init__()
        self.twtId = twtId
        self.userName = userName
        self.savePath = getContext('dl_path')

    def getDataList(self):
        response = getContext('globalSession').get(twtApi.format(self.twtId), params=twtApiPar, proxies=getContext(
            'proxy'), headers=getContext('headers'))

        if response.status_code != 200:
            print(http_warning.format('SinglePageTask.getDataList',
                                      response.status_code, getHttpText(response.status_code)))
            return

        page_content = response.text
        # response data correct
        if '"{}":'.format(self.twtId) in page_content:
            tw_content = str(json.loads(page_content)[
                'globalObjects']['tweets'][self.twtId])
            # debug
            # print(tw_content)
            self.dataList['picList'], self.dataList['gifList'], self.dataList['vidList'], self.dataList['textList'] = parseData(
                tw_content, self.twtId)

        # response data error
        elif 'Sorry, that page does not exist' in page_content:
            print(not_exist_warning)
        elif 'unable to view this Tweet' in page_content:
            print(tweet_unavailable_warning)
        elif '"text":"Age-restricted adult content.' in page_content:
            print(age_restricted_warning)
            return
        else:
            print(api_warning)
            write_log(self.twtId, page_content)
