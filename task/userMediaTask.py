'''
Author: mengzonefire
Date: 2021-09-21 09:19:02
LastEditTime: 2021-09-25 17:56:29
LastEditors: mengzonefire
Description: 推主推文批量爬取任务类
'''
from task.baseTask import Task


class UserMediaTask(Task):
    userId = None

    def __init__(self, userName, userId):
        self.userName = userName
        self.userId = userId

    def getDataList():
        pass
