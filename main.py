'''
Author: mengzonefire
Date: 2021-09-21 15:48:35
LastEditTime: 2021-09-22 18:34:01
LastEditors: mengzonefire
Description: 程序主函数入口
'''
from const import *
from text import *
from common.exceptHandler import except_handler
from common.tools import initalArgs, getProxy, setHeader, argsHandler
import sys
import os


def main():
    initalArgs()
    setEnv()
    if len(sys.argv) == 1:  # 命令行参数为空 -> 双击运行程序
        print('version: {}\nissue page: {}'.format(version, issue_page))
        if sys.platform in ['win32', 'win64']:
            getProxy()
        setHeader()
        print('\n' + input_ask)
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
