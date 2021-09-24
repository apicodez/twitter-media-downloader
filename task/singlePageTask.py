'''
Author: mengzonefire
Date: 2021-09-21 09:18:34
LastEditTime: 2021-09-24 21:07:17
LastEditors: mengzonefire
Description: 单推文媒体爬取任务类
'''
from task.baseTask import Task


class SinglePageTask(Task):
    twtId = None

    def __init__(self, twtId):
        self.twtId = twtId

    def start():
        pass
