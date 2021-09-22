'''
Author: mengzonefire
Date: 2021-09-21 09:22:57
LastEditTime: 2021-09-22 17:11:40
LastEditors: mengzonefire
Description: 异常处理模块
'''
import traceback
from text import network_error_warning
from common.logger import write_log


def except_handler(err):
    if 'Connection' in str(err):
        print(network_error_warning)
    else:
        traceback.print_exc()
        write_log('crash', traceback.format_exc())
