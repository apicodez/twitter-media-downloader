'''
Author: mengzonefire
Date: 2021-09-21 09:19:02
LastEditTime: 2021-09-24 21:07:46
LastEditors: mengzonefire
Description: 推主推文批量爬取任务类
'''
from task.baseTask import Task


class UserMediaTask(Task):
    userId = None

    def __init__(self, userId):
        self.userId = userId

    def start():
        pass
