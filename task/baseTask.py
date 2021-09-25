'''
Author: mengzonefire
Date: 2021-09-24 21:04:29
LastEditTime: 2021-09-25 17:33:22
LastEditors: mengzonefire
Description: 任务类基类
'''
from _typeshed import Self
from abc import abstractmethod
from typing import AbstractSet
from common.tools import downloadFile


class Task:
    userName = None
    savePath = None
    config = {}  # 任务配置列表， 即const.context

    dataList = {  # 自定义爬取数据结构
        'picList': {},  # DATA: {serverFileName: {url: , twtId: }}
        'gifList': {},  # DATA: ↑
        'vidList': {},  # DATA: ↑
        'textList': {},  # DATA: {twtId: textContent}
    }

    @abstractmethod
    def getDataList(self):
        pass

    def start(self):
        self.getDataList()
        for key in ['picList', 'gifList', 'vidList']:
            for serverFileName in self.dataList[key]:
                url = self.dataList[key][serverFileName]['url']
                fileName = '{}_{}_{}'.format(
                    self.userName, self.dataList[key][serverFileName]['url'], serverFileName)
                downloadFile(url, fileName, self.savePath)
