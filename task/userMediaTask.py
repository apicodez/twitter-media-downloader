'''
Author: mengzonefire
Date: 2021-09-21 09:19:02
LastEditTime: 2022-09-29 20:21:42
LastEditors: mengzonefire
Description: 推主推文批量爬取任务类
'''
from task.baseTask import Task
from common.tools import getHttpText, parseData
from common.text import *
from common.const import *


class UserMediaTask(Task):

    def __init__(self, userName, userId):
        super(UserMediaTask, self).__init__()
        self.userName = userName
        self.userId = userId
        self.savePath = '{}/{}'.format(getContext('dl_path'), userName)

    def getDataList(self, cursor=''):
        cursorPar = cursor and '"cursor":"{}",'.format(cursor)
        response = getContext('globalSession').get(
            userMediaApi, params={'variables': userMediaApiPar.format(self.userId, twtCount, cursorPar), 'features': userMediaApiPar2}, proxies=getContext(
                'proxy'), headers=getContext('headers'))

        if response.status_code != 200:
            print(http_warning.format('UserMediaTask.getDataList',
                                      response.status_code, getHttpText(response.status_code)))
            return

        pageContent = response.text
        # print(pageContent)  # debug
        if 'UserUnavailable' in pageContent:
            print(user_unavailable_warning)
            return
        elif 'Age-restricted adult content' in pageContent:
            print(age_restricted_warning)
            return
        elif '"timeline_v2":{}' in pageContent:
            print(need_cookie_warning)
            return
        twtIdList = p_twt_id.findall(pageContent)
        if not twtIdList:
            return
        contentList = pageContent.split('conversation_id_str')
        contentDict = dict(zip(twtIdList, contentList[1:]))
        for twtId in contentDict:
            picList, gifList, vidList, textList = parseData(
                contentDict[twtId].split('extended_entities')[-1], twtId)
            self.dataList['picList'] = dict(
                self.dataList['picList'], **picList)
            self.dataList['gifList'] = dict(
                self.dataList['gifList'], **gifList)
            self.dataList['vidList'] = dict(
                self.dataList['vidList'], **vidList)
            self.dataList['textList'] = dict(
                self.dataList['textList'], **textList)
        cursor = p_cursor.findall(
            pageContent.split('TimelineTimelineCursor')[-1])
        if cursor:
            self.getDataList(cursor[0])
