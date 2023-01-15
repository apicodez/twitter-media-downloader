'''
Author: mengzonefire
Date: 2021-09-21 09:22:57
LastEditTime: 2023-01-15 23:42:22
LastEditors: mengzonefire
Description: 异常处理模块
'''
import traceback
from common.text import *
from common.logger import write_log


def except_handler(err):
    err = str(err)
    if 'ConnectTimeoutError' in err or 'SSLError' in err:
        print(network_error_warning)
    elif 'Cannot connect to proxy' in err:
        print(proxy_error_warning)
    else:
        # debug
        traceback.print_exc()
        write_log('crash', traceback.format_exc())
