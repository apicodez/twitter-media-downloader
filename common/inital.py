'''
Author: mengzonefire
Date: 2021-09-21 09:20:04
LastEditTime: 2021-09-22 11:00:50
LastEditors: mengzonefire
Description: 程序初始化
'''
import argparse
from argparse import RawTextHelpFormatter
from const import url_args_help


def inital():
    # prog argument
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-c', '--cookie', dest='cookie', type=str,
                        help='set cookie to access locked users or tweets')
    parser.add_argument('-p', '--proxy', dest='proxy', type=str,
                        help='set network proxy, must be http proxy')
    parser.add_argument('-u', '--user_agent', dest='user_agent',
                        type=str, help='set user-agent')
    parser.add_argument('-d', '--dir', dest='dir',
                        type=str, help='set download path')
    parser.add_argument('-v', '--version', action='store_true',
                        help='show version')
    parser.add_argument('url', type=str, nargs='*', help=url_args_help)
    args = parser.parse_args()
