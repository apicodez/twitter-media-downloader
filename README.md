* 此分支为dev, 仅用于开发, 未测试的功能不一定能用, 使用请下 [release](https://github.com/mengzonefire/twitter-media-downloader/releases) 里的

# twitter-media-downloader 推特媒体文件下载工具

用于下载推特页面中包含的媒体文件（支持文本, 图片, 视频, 动图）的脚本工具, 使用推特网页版的 api 获取数据

支持输入如下四种格式的链接(\*\*\*为推主 id):

1. https://<span></span>twitter.com/\*\*\*/status/\*\*\* (爬取单条推文)
2. https://<span></span>twitter.com/\*\*\* (推主主页, 爬取推主所有推文)
3. https://<span></span>twitter.com/\*\*\*/media (推主媒体页, 爬取推主所有媒体推文)
4. https://<span></span>twitter.com/\*\*\*/likes (推主喜欢页, 爬取所有like推文)
5. https://<span></span>twitter.com/\*\*\*/following (推主关注页, 爬取关注列表)
6. @\*\*\* (用于搜索页爬取)

* 1.3.0版本已弃用主页接口和media接口(数据不全), 批量爬取全局使用搜索接口, 具体实现逻辑如下:
  *  twitter.com/user 转换为 @user
  *  twitter.com/user/media 转换为 -m @user
  *  twitter.com/user/likes 无法使用搜索接口实现, 使用like接口

# donate 赞助

若喜欢本项目, 欢迎前往 [爱发电](https://afdian.net/@mengzonefire) 支持作者

# tips 提示

1. 获取到的媒体文件默认下载到程序同目录下的 **twitter_media_download** 文件夹
2. 设置年龄限制/锁定 的 推主/推文 必须设置 cookie 才能爬取, 设置完成后, cookie会保存到本地, 下次运行程序自动读取
3. 下载文件名格式: **{推主 id}\_{推文 id}\_{服务器文件名}**, 例如 memidesuyo_1441613758988574723_FAGkEkFVEAI8GSd.jpg
4. 默认使用系统代理, 无需配置 (仅 win 平台, 其余平台请手动设置)，但注意程序仅支持http代理
5. 爬取视频文件时, 会自动选择最高分辨率下载, 图片文件则自动选择原图画质
6. 支持爬取推文文本, 自动保存为 **{推主 id}\_{推文 id}.txt**
7. 若出现任何问题/提意见&需求, 请前往 [issue](https://github.com/mengzonefire/twitter-media-downloader/issues) 反馈
8. 程序的配置文件路径: * 配置文件内含proxy(代理)，download_path(下载路径)，UA和cookie四项配置
    * linux: ~/tw_media_downloader.conf
    * win: %userprofile%/tw_media_downloader.conf

# usage 使用方法

* 若使用python3环境运行py代码，注意先安装依赖：

    ```
    pip install -r requirements.txt
    ```

  1. 直接运行程序:  
  运行后根据提示输入 命令 或 推文/推主链接即可.
      ```
      python twitter-media-downloader.py
      ```
      <img src="https://pic.rmb.bdstatic.com/bjh/08934029f23df12817604a44d48fb01d.png">
      
      示例：
       * 下载单条推文 ```https://<span></span>twitter.com/user/status/0000000000000000000```
       * 下载用户主页 ```https://<span></span>twitter.com/user```
       * 下载用户媒体页 ```https://<span></span>twitter.com/user/media```
       * 下载用户[搜索页](#搜索接口用法) ```@user```  
       * 下载用户[搜索页](#搜索接口用法)并指定日期 ```@user&2022-12-1|2022-12-10```  
       * 高级搜索， 包含#tag1和#tag2，并指定推文来自用户user ```@&advanced=(#tag1 AND #tag2) (from:user)```  
         * 注：脚本搜索页默认不包含回复，如需爬取回复请使用高级搜索
  2. 命令行调用:
       ```
          usage: twitter-media-downloader.py [-h] [-c COOKIE] [-p PROXY] [-d DIR] [-n CONCURRENCY] [-t TYPE] [-m] [-q] [-r] [-v] [url ...]

          positional arguments:
            url                   tw url to collect, must be like:
                                      1. https://twitter.com/***/status/***
                                      2. https://twitter.com/***(/media|likes|following) (user page, *** is user_id)
                                      3. @*** (search page, plz check README)

          options:
            -h, --help            show this help message and exit
            -c COOKIE, --cookie COOKIE
                                  for access locked users&tweets, will save to cfg file, input " " to clear
            -p PROXY, --proxy PROXY
                                  support http&socks5, default use system proxy(win only)
            -d DIR, --dir DIR     set download path
            -n CONCURRENCY, --num CONCURRENCY
                                  downloader concurrency
            -t TYPE, --type TYPE  desired media type, optional: photo&animated_gif&video&full_text
            -m, --media           exclude non-media tweets
            -q, --quoted          exclude quoted tweets
            -r, --retweeted       exclude retweeted
            -v, --version         show version and check update
       ```
      示例：
       * 下载用户主页 `python twitter-media-downloader.py https://twitter.com/user`
       * 下载用户主页，排除转推 `python twitter-media-downloader.py -r https://twitter.com/user`
       * 下载用户媒体页，排除引用 `python twitter-media-downloader.py -q https://twitter.com/user/media`
       * 下载用户搜索页，排除引用 `python twitter-media-downloader.py -q @user`
         * `-r` 和 `-q` 用于排除 转推 和 引用, `-m` 用于排除非媒体(纯文本)推文
       * 下载用户搜索页，指定下载类型为图片和视频 `python twitter-media-downloader.py -t "photo&video" @user`
       * 下载用户搜索页，指定日期为2022-12-1到2022-12-20 `python twitter-media-downloader.py "@user&2022-12-1|2022-12-20"`
       * 高级搜索 [详情](#搜索接口用法)，搜索包含#tag1和#tag2，并指定推文来自用户user `python twitter-media-downloader.py "@&advanced=(#tag1 AND #tag2) (from:user)"`
   
   ## 搜索接口用法
   3. 构成： `@用户名&附加命令`
   4. 使用 `@` 开头
   5. 使用 `&` 连接用户名与附加命令
   6. 使用 `|` 连接日期 `2020-1-1|2021-1-1`
   7. 使用命令行传入参数运行时一定要使用双引号包住 `"@user&2020-1-1|2021-1-1"`
   8. 高级搜索： 前往 [推特高级搜索页](https://twitter.com/search-advanced?f=live) 填写并搜索，然后复制搜索框内容，将内容粘贴至 `@&advanced=` 后面
   9. 关于高级搜索的tag：推特默认使用 `#taga OR #tagb` 意为包含taga或者包含tagb，但是可以手动修改为 `#taga AND #tagb` ，意为含taga并且包含tagb

# TODO 待实现需求

1. GUI (可能要等很久才能写出来)
2. 添加socks代理支持, 优化代理配置流程
3. 废弃主页,媒体页api, 直接使用搜索页api
4. 添加用户like页爬取功能
5. 修改默认输出文件名格式为 **推主id-推文id-日期_时间/-img1/-vid1/-gif1/-text**
   * 例如 \*\*\*-1614977212545844224-20230213_114210-img1.jpg
6. 添加输出文件名自定义 可选元素: 推主id, 推文id, 日期, 时间, 数据类型+序号
7. 支持推文评论爬取

<details>
<summary>已完成 [点击展开]</summary>
<ol><li>支持 cmd 传参调用</li><li>支持爬取视频/动图文件</li><li>支持批量爬取推主所有媒体</li><li>下载进度显示</li><li>分模块重构代码方便后续开发</li><li>支持手动设置 UA 和代理</li><li>支持设置 cookie 用于爬取锁推</li><li>完善程序错误 log 导出 (完成, 现会在崩溃后写入完整 log 到文件)</li><li>批量爬取时输出进度记录, 并在程序异常退出重启后导入进度继续下载 (废弃)</li><li>在文件名前添加推文 id, 方便定位推文</li><li>支持自定义下载路径</li><li>提供推文 id 转推文 url 功能</li><li>退出时保存 UA/代理/cookie 到配置文件, 下次运行程序自动读取设置</li><li>在直接运行程序的交互模式下加入 cookie,下载路径,代理的设置命令</li><li>添加自动更新功能&amp;CI 自动编译</li><li>废弃推文 id 转 url 功能, 并将下载文件的格式设置为: {推主 id}_{推文 id}_{服务器文件名} (方便定位推文 url)</li><li>添加自定义关键字/正则表达式, 提取推文中的 url 链接 (废弃, 由 TODO#23 替代)</li><li>添加媒体文件的筛选提取功能(例如 仅图片, 仅视频)</li><li>添加推主转载推文的媒体提取功能 (废弃, 转载推文没有独立的获取接口)</li><li>优化启动逻辑, 启动时网络检查失败不再强制跳出程序</li><li>下载文件时跳过目标路径下已存在的文件, 避免重复下载</li><li>添加爬取推文文本内容的功能(可选参数)</li><li>使用多线程并发下载多个文件, 提高下载速度(可选线程并发数)</li><li>已知 UserMedia api 会把已删除的推文一起返回, 占用 count, 导致爬取内容不完整, 尝试修复</li><li>支持输入空配置项(例如cookie设置), 用于重置对应配置 (完成, cookie, proxy, ua均已支持)</li><li>配置cookie时添加完整的cookie校验, 防止输错cookie导致接口返回403 (已修复, 其实是正则写错导致cookie解析错误)</li><li>userMedia接口老是缺数据, 将批量爬取的逻辑改为从userMedia提取tw_id, 然后丢到singlePageTask去执行 (已修复, 实际问题为部分用户/推文有年龄限制, 需要设置cookie才能正常访问, 1.2.3版本已加入提示)</li><li>直接运行模式下, 完善操作提示, 照顾小白</li></ol>
</details>

# preview 预览

批量下载:  
<img src="https://pic.rmb.bdstatic.com/bjh/e7bb8983c155712b6175e99f9f66ff35.png">
