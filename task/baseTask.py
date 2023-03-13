'''
Author: mengzonefire
Date: 2021-09-24 21:04:29
LastEditTime: 2023-03-13 20:09:00
LastEditors: mengzonefire
Description: 任务类基类
'''

import json
import os
import math
import time
import threading
from queue import Queue
from abc import abstractmethod
import traceback
from common.logger import writeLog
from common.text import *
from common.const import getContext
from common.tools import downloadFile, parseData
from concurrent.futures import ThreadPoolExecutor, wait


class Task(object):

    def __init__(self):
        self.tasks = set()  # 任务线程对象容器
        self.userName = ''   # 推主id（不是昵称）
        self.savePath = ''   # 下载路径
        self.twtId = None  # 推文id(int)
        self.userId = None  # 推主rest_id(int)
        self.cfg = {}   # 爬取media页的时候会强制覆盖全局配置参数，故在类成员内单独添加标记
        self.stop = False   # 进度条与生产者停止信号
        self.total = Queue()   # 任务总量计数器
        self.done = Queue()    # 已完成任务计数器
        self.dataList = Queue()  # 任务数据队列
        self.pageContent = None  # 接口元数据(用于debug)
        self.errFlag = False

    @abstractmethod
    def getDataList(self):
        raise NotImplemented

    def parseData(self, rest_id_list, cursor):
        try:
            cursor, rest_id_list = parseData(
                self.pageContent, self.total, self.userName, self.dataList, self.cfg, rest_id_list, cursor)
        except KeyError:
            self.errFlag = True
            print(parse_warning)
            writeLog(f'{self.userName}_unexpectData',
                     f'{traceback.format_exc()}\n\n{json.dumps(self.pageContent)}')  # debug
        except Exception:
            self.errFlag = True
            print(crash_warning)
            writeLog(f'{self.userName}_crash',
                     traceback.format_exc())  # debug
        finally:
            if self.errFlag or not cursor:
                self.stopGetDataList()
                return True  # 结束
            else:
                return False  # 未结束

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
                    progress = (done / total) * 50  # 缩短进度条长度防止cmd自动换行
                    length = time.perf_counter() - start
                    print(f"\r@{self.userName} {round(progress, 1)}% [{'█' * math.floor(progress)}"
                          f"{' ' * (50 - math.ceil(progress))}] [{done}/{total}] {round(length, 1)}s {i}", end='')
                    if self.stop:
                        return
                    time.sleep(0.1)

    def start(self):
        self.savePath = os.path.normpath(self.savePath)
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
        elif self.pageContent and not self.errFlag:
            print(dl_nothing_warning)
            writeLog(f'{self.twtId or self.userName}_noMedia',
                     json.dumps(self.pageContent))  # debug
