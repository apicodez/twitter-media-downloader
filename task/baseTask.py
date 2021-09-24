from abc import abstractmethod
from typing import AbstractSet


'''
Author: mengzonefire
Date: 2021-09-24 21:04:29
LastEditTime: 2021-09-24 21:07:10
LastEditors: mengzonefire
Description: 任务类基类
'''


class Task:
    dataList = {
        'picList': {},  # DATA: {serverFileName: url}
        'gifList': {},  # DATA: ↑
        'vidList': {},  # DATA: ↑
        'textList': {},  # DATA: {twtId: textContent}
    }

    @abstractmethod
    def start():
        pass
