# twitter-media-downloader
用于下载推特页面中包含的媒体文件（支持图片, 视频, 动图）的脚本  
<br/>

支持输入如下三种格式的链接:
1. https://<span></span>twitter.com/\*\*\*/status/\*\*\* (推文)  
2. https://<span></span>t.co/****** (短链, 部分短链会跳转至非推文页面, 脚本会自动跳过)  
3. https://<span></span>twitter.com/\*\*\* (推主主页, \*\*\*为推主id, 用于批量爬取)  
<br/>

PS:    
1. 获取到的媒体文件自动下载到路径下的twitter_media_download文件夹  
2. 已知单条推文仅可能出现4张以内的图片或1个动图/视频
3. 默认使用系统代理，无需配置 (仅win平台, 其余平台请手动设置)
4. 爬取视频文件时, 会自动选择最高分辨率下载
5. 推特上的动图gif文件实际都是mp4文件
6. 若出现任何问题, 请反馈log文件
7. 若需要提意见/需求, 请移步issue

# 使用方法

    usage: python3 twitter-media-downloader.py [-h] [-c COOKIE] [-p PROXY] [-u USER_AGENT]
                                       [-t TWEET_ID] [-d DIR] [-v]
                                       [url [url ...]]

    [url] argument must be like:
        1. https://twitter.com/***/status/***
        2. https://t.co/*** (tweets short url)
        3. https://twitter.com/*** (user page, *** is user_id)
        # 3. will gather all media files of user's tweets

    positional arguments:
      url                   twitter url to gather media

    optional arguments:
      -h, --help            show this help message and exit
      -c COOKIE, --cookie COOKIE
                            set cookie to access locked users or tweets
      -p PROXY, --proxy PROXY
                            set network proxy, must be http proxy
      -u USER_AGENT, --user_agent USER_AGENT
                            set user-agent
      -t TWEET_ID, --tweet_id TWEET_ID
                            convert tweet_id to tweet_url
      -d DIR, --dir DIR     set download path
      -v, --version         show version


# TODO (待实现需求)  
1. ~~支持cmd传参调用~~ (完成)
2. ~~支持爬取视频/动图文件~~ (完成)
3. ~~支持批量爬取推主所有媒体~~ (完成)
4. ~~下载进度显示~~ (完成)
6. ~~支持手动设置UA和代理~~ (完成)
7. ~~支持设置cookie用于爬取锁推~~ (完成)
8. 完善程序错误log导出
9. 批量爬取时输出进度记录, 并在程序异常退出重启后导入进度继续下载
10. ~~在文件名前添加推文id, 方便定位推文~~ (完成)
11. ~~支持自定义下载路径~~ (完成)
12. ~~提供推文id转推文url功能~~ (完成)
13. 提供语言设置(中/英), 翻译warning文本和readme页面
14. 设置UA/代理后, 自动保存到配置文件, 下次运行程序自动读取设置

<img src="https://pic.rmb.bdstatic.com/bjh/e7bb8983c155712b6175e99f9f66ff35.png">
