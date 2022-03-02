'''
Author: mengzonefire
Date: 2021-09-24 21:04:29
LastEditTime: 2022-03-03 02:14:55
LastEditors: mengzonefire
Description: 任务类基类
'''
from abc import abstractmethod
from common.text import task_finish
from common.tools import downloadFile, saveText


class Task:
    userName = ''
    savePath = ''
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
                    self.userName, self.dataList[key][serverFileName]['twtId'], serverFileName)
                downloadFile(url, fileName, self.savePath)

        for twtId in self.dataList['textList']:
            content = self.dataList['textList'][twtId]
            fileName = '{}_{}.txt'.format(
                self.userName, twtId)
            saveText(content, fileName, self.savePath)

        print(task_finish.format(self.savePath))
