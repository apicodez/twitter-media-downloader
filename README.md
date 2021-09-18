# twitter-media-downloader 推特媒体文件下载工具
用于下载推特页面中包含的媒体文件（支持图片, 视频, 动图）的脚本工具 

<br/>

支持输入如下三种格式的链接:
1. https://<span></span>twitter.com/\*\*\*/status/\*\*\* (推文)  
2. https://<span></span>t.co/****** (短链, 部分短链会跳转至非推文页面, 脚本会自动跳过)  
3. https://<span></span>twitter.com/\*\*\* (推主主页, \*\*\*为推主id, 用于批量爬取)

<br/>

# tips 提示  
1. 获取到的媒体文件自动下载到路径下的twitter_media_download文件夹  
2. 锁定的推主/推文必须设置cookie才能爬取, 设置完成后, 正常退出程序(exit命令)可自动保存cookie
3. release仅提供win_x86平台的可执行文件, 其他平台请自行安装python3环境运行
4. 下载文件名格式: {推文id}_{服务器文件名}, 例如1399401339331891205_16icKxB4mFrHlWHg.mp4
5. 默认使用系统代理，无需配置 (仅win平台, 其余平台请手动设置)
6. 爬取视频文件时, 会自动选择最高分辨率下载, 图片文件则自动选择原图画质
8. 若出现任何问题, 请到issue反馈log文件
9. 若需要提意见/需求, 请移步issue

<br/>

# usage 使用方法
直接运行程序:  
运行后根据提示输入 命令 或 推文/推主链接即可.

    python3 twitter-media-downloader.py

<img src="https://pic.rmb.bdstatic.com/bjh/08934029f23df12817604a44d48fb01d.png">

命令行调用:

    usage: twitter-media-downloader.py [-h] [-c COOKIE] [-p PROXY] [-u USER_AGENT]
                                   [-t [TWEET_ID [TWEET_ID ...]]] [-d DIR]
                                   [-v]
                                   [url [url ...]]

    positional arguments:
      url                   tw url to gather media, must be like:
                                1. https://twitter.com/***/status/***
                                2. https://t.co/*** (tweets short url)
                                3. https://twitter.com/*** (user page, *** is user_id)
                                # 3. will gather all media files of user's tweets
    
    optional arguments:
      -h, --help            show this help message and exit
      -c COOKIE, --cookie COOKIE
                            set cookie to access locked users or tweets
      -p PROXY, --proxy PROXY
                            set network proxy, must be http proxy
      -u USER_AGENT, --user_agent USER_AGENT
                            set user-agent
      -t [TWEET_ID [TWEET_ID ...]], --tweet_id [TWEET_ID [TWEET_ID ...]]
                            convert tweet_id to tweet_url
      -d DIR, --dir DIR     set download path
      -v, --version         show version

<br/>

# dev note 开发记录
1. 关于TODO#15: 原本想通过程序内subprocess.run再调用的方式传参, 实现交互模式(即无参直接运行脚本)的参数输入,
   但考虑到实际需要的参数并不多, 为不影响脚本的上手门槛, 遂放弃此方案, 现版本交互模式仅支持设置cookie和转换id的命令
   (个人认为这两个比较常用)  
2. ~~发现有个同名的插件, 而且还更好用, 故本项目停止开发.~~ (发现自己的脚本还是有点优势的, 继续开发吧)

    (插件地址: https://chrome.google.com/webstore/detail/twitter-media-downloader/cblpjenafgeohmnjknfhpdbdljfkndig)
3. 废弃TODO#9, 因为考虑到脚本的主要耗时是下载而非解析数据, 故用TODO#22作为替代即可

<br/>

# TODO (待实现需求)  
1. ~~支持cmd传参调用~~ (完成)
2. ~~支持爬取视频/动图文件~~ (完成)
3. ~~支持批量爬取推主所有媒体~~ (完成)
4. ~~下载进度显示~~ (完成)
5. 分模块重构代码方便后续开发
6. ~~支持手动设置UA和代理~~ (完成)
7. ~~支持设置cookie用于爬取锁推~~ (完成)
8. ~~完善程序错误log导出~~ (完成, 现会在崩溃后写入完整log到文件)
9. ~~批量爬取时输出进度记录, 并在程序异常退出重启后导入进度继续下载~~ (废弃)
10. ~~在文件名前添加推文id, 方便定位推文~~ (完成)
11. ~~支持自定义下载路径~~ (完成)
12. ~~提供推文id转推文url功能~~ (完成)
13. 提供语言设置(中/英), 翻译warning文本和readme页面
14. ~~退出时保存UA/代理/cookie到配置文件, 下次运行程序自动读取设置~~ (完成)
15. ~~在直接运行程序的交互模式下加入cookie,下载路径,代理的设置命令~~ (完成)
16. 添加自动更新功能&CI自动编译
17. 废弃推文id转url功能, 并将下载文件的格式设置为: {推主id}\_{推文id}\_{服务器文件名} (方便定位推文url)
18. ~~添加自定义关键字/正则表达式, 提取推文中的url链接~~ (废弃, 由TODO#23替代)
19. 添加媒体文件的筛选提取功能(例如 仅图片, 仅视频)
20. 添加推主转载推文的媒体提取功能
21. 优化启动逻辑, 启动网络检查时失败后不再强制跳出程序
22. ~~下载文件时跳过目标路径下已存在的文件, 避免重复下载~~ (完成)
23. 添加爬取推文文本内容的功能(可选参数)
24. 使用多线程并发下载多个文件, 提高下载速度(可选线程并发数)
25. 已知UserMedia api会把已删除的推文一起返回, 占用count, 导致爬取内容不完整, 尝试修复

批量下载:  
<img src="https://pic.rmb.bdstatic.com/bjh/e7bb8983c155712b6175e99f9f66ff35.png">
