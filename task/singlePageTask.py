'''
Author: mengzonefire
Date: 2021-09-21 09:18:34
LastEditTime: 2021-09-25 17:56:08
LastEditors: mengzonefire
Description: 单推文爬取任务类
'''
from task.baseTask import Task


class SinglePageTask(Task):
    twtId = None

    def __init__(self, userName, twtId):
        self.userName = userName
        self.twtId = twtId

    def getDataList():
        pass
