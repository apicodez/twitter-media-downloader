'''
Author: mengzonefire
Date: 2021-09-21 09:22:57
LastEditTime: 2022-02-09 16:07:51
LastEditors: mengzonefire
Description: 异常处理模块
'''
import traceback
from common.text import *
from common.logger import write_log


def except_handler(err):
    if 'ConnectTimeoutError' in str(err):
        print(network_error_warning)
    elif 'Cannot connect to proxy' in str(err):
        print(proxy_error_warning)
    else:
        # debug
        traceback.print_exc()
        write_log('crash', traceback.format_exc())
