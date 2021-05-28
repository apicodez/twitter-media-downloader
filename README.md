# twitter-media-scraper
用于提取推特页面中包含的媒体数据（支持图片, 视频, 动图）的脚本

支持输入如下三种格式的链接:
1. https://<span></span>twitter.com/\*\*\*/status/\*\*\* (推文)  
2. https://<span></span>t.co/****** (短链, 部分短链会跳转至非推文页面, 脚本会自动跳过)  
3. https://<span></span>twitter.com/\*\*\* (推主主页, \*\*\*为推主id, 用于批量爬取)  

PS:    
1. 获取到的媒体文件自动下载到路径下的twitter_scraper_download文件夹  
2. 已知单条推文仅可能出现4张以内的图片或1个动图/视频

默认使用系统代理，无需配置，若提取出现任何问题，请反馈log文件

# TODO (待实现需求)  
1. ~~支持cmd传参调用~~ (完成)
2. ~~支持爬取视频/动图文件~~ (完成)
3. 支持遍历爬取推主所有媒体
4. ~~下载进度显示~~ (完成)
5. 支持linux平台
6. 支持手动设置UA和代理
7. 支持设置cookie用于爬取锁推
8. 完善程序错误log导出

<a href="https://sm.ms/image/wvPBc4mgVy9aCxo" target="_blank"><img src="https://i.loli.net/2020/08/13/wvPBc4mgVy9aCxo.png" ></a>
