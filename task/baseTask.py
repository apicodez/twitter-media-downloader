'''
Author: mengzonefire
Date: 2021-09-24 21:04:29
LastEditTime: 2022-09-29 20:19:57
LastEditors: mengzonefire
Description: 任务类基类
'''
from abc import abstractmethod
from common.text import task_finish, dl_nothing_warning
from common.tools import downloadFile, saveText


class Task(object):
    # config = {}  # 任务配置列表， 即const.context

    def __init__(self):
        self.dataList = {  # 自定义爬取数据结构
            'picList': {},  # DATA: {serverFileName: {url: , twtId: }}
            'gifList': {},  # DATA: ↑
            'vidList': {},  # DATA: ↑
            'textList': {},  # DATA: {twtId: textContent}
        }

    @abstractmethod
    def getDataList(self):
        raise NotImplemented

    def start(self):
        dlNothing = True
        self.getDataList()

        for key in ['picList', 'gifList', 'vidList']:
            for serverFileName in self.dataList[key]:
                url = self.dataList[key][serverFileName]['url']
                fileName = '{}_{}_{}'.format(
                    self.userName, self.dataList[key][serverFileName]['twtId'], serverFileName)
                downloadFile(url, fileName, self.savePath)
                dlNothing = False

        for twtId in self.dataList['textList']:
            content = self.dataList['textList'][twtId]
            fileName = '{}_{}.txt'.format(
                self.userName, twtId)
            saveText(content, fileName, self.savePath)
            dlNothing = False

        if not dlNothing:
            print(task_finish.format(self.savePath))
        else:
            print(dl_nothing_warning)
