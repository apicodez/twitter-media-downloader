'''
Author: mengzonefire
Date: 2021-09-21 09:22:57
LastEditTime: 2021-09-25 23:06:22
LastEditors: mengzonefire
Description: 异常处理模块
'''
import traceback
from common.text import network_error_warning
from common.logger import write_log


def except_handler(err):
    if 'Connection' in str(err):
        print(network_error_warning)
    else:
        # debug
        traceback.print_exc()
        write_log('crash', traceback.format_exc())
