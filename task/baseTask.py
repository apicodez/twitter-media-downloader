'''
Author: mengzonefire
Date: 2021-09-24 21:04:29
LastEditTime: 2023-02-22 03:03:42
LastEditors: mengzonefire
Description: 任务类基类
'''
import os
import math
import time
import threading
from queue import Queue
from abc import abstractmethod
from common.text import *
from common.const import getContext
from common.tools import downloadFile
from concurrent.futures import ThreadPoolExecutor, wait


class Task(object):
    savePath: str
    userName: str
    twtId: int
    userId: int
    # config = {}  # 任务配置列表， 即const.context

    def __init__(self):
        self.tasks = set()
        self.userName = ''
        self.savePath = ''
        self.twtId = 0
        self.userId = 0
        self.stop = False  # 进度条与生产者停止信号
        self.total = Queue()  # 总媒体数量
        self.done = Queue()  # 已下载媒体数量
        self.dataList = Queue()  # 媒体下载队列
        # {
        #     'userName': {       # 自定义爬取数据结构
        #         'picList': {},  # DATA: {serverFileName: {url: , twtId: }}
        #         'gifList': {},  # DATA: ↑
        #         'vidList': {},  # DATA: ↑
        #         'textList': {}  # DATA: {twtId: textContent}
        #     }
        # }

    @abstractmethod
    def getDataList(self):
        raise NotImplemented

    def stopGetDataList(self):
        for _ in range(getContext('concurrency')):
            self.dataList.put(None)

    def progressBar(self, start):
        while True:
            for i in ['|', '/', '一', '\\', '|', '/', '一', '\\']:
                for _ in range(5):
                    done = self.done.qsize()
                    total = self.total.qsize()
                    if total == 0:
                        if self.stop:
                            return
                        continue
                    progress = (done / total) * 100
                    length = time.perf_counter() - start
                    print(f"\r@{self.userName} {round(progress, 1)}% [{'█' * math.floor(progress)}"
                          f"{' ' * (100 - math.ceil(progress))}] [{done}/{total}] {round(length, 1)}s {i}", end="")
                    if self.stop:
                        return
                    time.sleep(0.1)

    def start(self):
        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)
        start = time.perf_counter()
        t1, t2 = threading.Thread(target=self.getDataList), threading.Thread(
            target=self.progressBar, args=(start,))
        t1.start()
        t2.start()
        with ThreadPoolExecutor(max_workers=getContext('concurrency')) as executor:
            for _ in range(getContext('concurrency')):
                task = executor.submit(
                    downloadFile, self.savePath, self.dataList, self.done)
                self.tasks.add(task)
        wait(self.tasks)
        self.stop = True
        t1.join()
        t2.join()
        if self.total.qsize():
            print(task_finish.format(self.done.qsize(), self.total.qsize(),
                                     round(time.perf_counter() - start, 1), self.savePath))
        else:
            print(dl_nothing_warning)
