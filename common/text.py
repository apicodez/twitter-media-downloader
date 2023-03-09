'''
Author: mengzonefire
Date: 2023-01-15 23:14:36
LastEditTime: 2023-03-10 00:22:49
LastEditors: mengzonefire
Description: 存放公用提示文本和链接
'''

# external
donate_page = 'https://afdian.net/@mengzonefire'
issue_page = 'https://github.com/mengzonefire/twitter-media-downloader/issues'
release_page = 'https://github.com/mengzonefire/twitter-media-downloader/releases'
cookie_tips_page = 'https://git.io/how_to_get_cookies_cn'

# warning text
log_warning = '\rlog文件已保存到 {}\n'
crash_warning = f'\r未知错误, 请前往issue页反馈log文件:\n{issue_page}'
user_warning = f'\r提取失败: 该用户不存在, 若存在, 请前往issue页反馈:\n{issue_page}'
token_warning = f'\r运行失败: Guest Token获取失败, 请前往issue页反馈:\n{issue_page}'
parse_warning = f'\r解析失败, 跳过此数据, 请前往issue页反馈log文件:\n{issue_page}'
http_warning = '\r提取失败{}: http访问异常, 状态码: {} -> {}'
timeout_warning = '\r网络超时, 服务器未响应或断开链接, 正在重试...{}'
download_timeout_warning = '\r{} {}{}'
proxy_input_warning = '代理格式错误（回车继续）'
cookie_input_warning = 'cookie格式错误（回车继续）'
proxy_arg_warning = \
    '参数错误: 代理格式错误, 格式:\n' \
    '[协议]://host:port 或 [协议]://user:pass@host:port [协议]为http或socks5'
cookie_arg_warning = f'参数错误: cookie格式错误, 请参考教程获取cookie:\n{cookie_tips_page}'
user_unavailable_warning = '\r提取失败: 该用户已锁定/冻结, 访问锁定用户需要设置已关注账号的cookie'
age_restricted_warning = '\r提取失败: 该用户已设置年龄限制, 访问需要设置账号cookie'
network_error_warning = '\r网络连接失败, 请检查代理设置'
input_warning = '\r链接或命令格式错误（回车继续）'
check_update_warning = '\r检查更新失败, 程序继续运行, 失败信息:\n{}\n'
need_cookie_warning = '\r目前访问推特的media列表接口需要登录账号, 故请先设置cookie再爬取'
dl_nothing_warning = f'\r未爬取到任何有效数据, 请前往issue页反馈log文件:\n{issue_page}'
queue_empty_warning = '\r超过30秒未从任务队列中获取到数据'
unexpectVar_arg_warning = '参数错误: 自定义文件名格式错误, 存在错误的变量名'
unexpectVar_input_warning = '\r存在错误的变量名, 请重新输入（回车继续）'
input_num_warning = '请输入正确数字（回车继续）'

# normal text
task_finish = '\r文件下载任务已完成 {}/{}, 用时 {}s, 保存路径: {}'
fo_Task_finish = '\r关注列表爬取任务已完成, 保存路径: {}'
input_cookie_ask = \
    '请输入cookie, 单击回车确认(留空直接回车清除cookie)\n' \
    f'* cookie获取教程：{cookie_tips_page}\n' \
    '请输入 (输入0返回)：'
input_proxy_ask = \
    '请输入代理, 单击回车确认(留空直接回车为不使用代理), 格式:\n' \
    '[协议]://host:port 或 [协议]://user:pass@host:port [协议]为http或socks5\n' \
    '请输入 (输入0返回,输入1获取系统代理)：'
max_concurrency_ask = \
    '下载线程数过高会使下载变慢，请勿设置过大\n\n' \
    '0.返回\n\n' \
    '请输入下载线程数，建议设置1~32之间（默认8）：'
set_type_ask = \
    '输入数字选择，可多选，如“13”就是包含图片和视频\n\n' \
    '0.返回\n' \
    '1.下载图片\n' \
    '2.下载动图\n' \
    '3.下载视频\n' \
    '4.下载文本\n' \
    '5.所有\n\n' \
    '请输入（默认所有）：'
set_fileName_ask = \
    '输入自定义文件名, 可选变量：\n\n' \
    '{userName} : 推主id\n' \
    '{twtId} : 推文id\n' \
    '{date} : 推文日期, 例如20230213\n' \
    '{time} : 推文时间, 例如114210\n' \
    '{type} : 数据类型+序号(1-4,文本没序号), 例如img1/vid1/gif1/text\n' \
    '{ori} : 服务器文件名(文本文件没有此项), 例如FAGkEkFVEAI8GSd\n\n' \
    '请输入 (输入0返回)：'
retweeted_status_ask = \
    '是否下载转推\n\n' \
    '0.返回\n' \
    '1.是\n' \
    '2.否\n\n' \
    '请输入：'
quoted_status_ask = \
    '是否下载引用推文\n\n' \
    '0.返回\n' \
    '1.是\n' \
    '2.否\n\n' \
    '请输入：'
media_status_ask = \
    '是否下载非媒体(纯文本)推文\n\n' \
    '0.返回\n' \
    '1.是\n' \
    '2.否\n\n' \
    '请输入：'
download_settings_ask = \
    '输入数字\n\n' \
    '0.返回\n' \
    '1.设置下载类型\n' \
    '2.设置下载线程数\n' \
    '3.设置是否下载引用推文\n' \
    '4.设置是否下载转推\n' \
    '5.设置是否下载非媒体\n' \
    '6.设置自定义保存文件名\n\n' \
    '请输入：'
continue_ask = '\n单击回车键->退出程序, 输入任意内容+回车->继续提取\n'
input_ask = \
    '输入命令数字或链接 (支持批量, 一行一条, 双击回车确认)\n\n' \
    '0.退出脚本\n' \
    '1.设置cookie\n' \
    '2.设置网络代理\n' \
    '3.设置下载参数\n\n' \
    '请输入：'
exit_ask = '\n单击回车键退出程序\n'
config_info = \
    '当前配置: 线程数: {concurrency}, 已设置cookie: {cookie}, 代理设置: {proxy}\n' \
    '排除转推: {retweeted}, 排除引用: {quoted}, 排除非媒体: {media}, 爬取类型: {type}\n' \
    '自定义文件名: {fileName}, 下载路径: {dl_path}\n'
save_cfg_finsh = '以下参数保存到配置文件：{}'
