'''
Author: mengzonefire
Date: 2021-09-21 15:48:35
LastEditTime: 2021-09-23 11:36:33
LastEditors: mengzonefire
Description: 程序主函数入口
'''
import sys
import os
from const import *
from text import *
from common.tools import *
from common.console import cmdMode
from common.exceptHandler import except_handler


def main():
    initalArgs()
    getEnv()
    if len(sys.argv) == 1:  # 命令行参数为空 -> 双击运行程序
        print('version: {}\nissue page: {}\n'.format(version, issue_page))
        getProxy()
        getHeader()
        cmdMode()
    else:
        argsHandler()
    saveEnv()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        except_handler(e)
        if input(reset_ask):
            if sys.platform in ['win32', 'win64']:  # 判断是否为win平台
                os.system('cls')
            else:
                os.system('clear')
            main()
