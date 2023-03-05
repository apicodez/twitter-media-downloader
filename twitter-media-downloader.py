'''
Author: mengzonefire
Date: 2021-09-21 15:48:35
LastEditTime: 2023-03-06 02:28:41
LastEditors: mengzonefire
Description: 主函数入口
'''

import traceback
from common.console import cmdMode, startCrawl
from common.tools import *


def main():
    exe_path, _ = os.path.split(sys.argv[0])
    if exe_path:
        os.chdir(exe_path)  # 切换工作目录到程序根目录
    initalArgs()
    getEnv()
    if len(sys.argv) == 1:  # 命令行参数为空 / 双击运行程序 -> 进入交互模式
        print('version: {}\ndonate page: {}\nissue page: {}\n'.format(
            version, donate_page, issue_page))
        getSysProxy()
        checkUpdate()
        getGuestCookie()
        cmdMode(False)
    else:
        argsHandler()
        startCrawl(getContext('args').url)
    saveEnv()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:  # 缺失异常处理
        traceback.print_exc()
        write_log('crash', traceback.format_exc())
