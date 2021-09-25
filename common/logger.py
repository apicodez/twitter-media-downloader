'''
Author: mengzonefire
Date: 2021-09-21 09:23:35
LastEditTime: 2021-09-25 23:29:33
LastEditors: mengzonefire
Description: log模块
'''
import os
from common.const import getContext


def write_log(log_name, log_content):
    log_path = getContext('log_path')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    file_path = '{}/{}.txt'.format(log_path, log_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(log_content)
        print('运行错误: log文件已保存到{}'.format(file_path))
