# external page url
donate_page = 'https://afdian.net/@mengzonefire'
issue_page = 'https://github.com/mengzonefire/twitter-media-downloader/issues'
release_page = 'https://github.com/mengzonefire/twitter-media-downloader/releases'
cookie_tips_page = 'https://git.io/how_to_get_cookies_cn'

# warning str
log_warning = '\n运行错误: log文件已保存到 {}\n'
# api_warning = '提取失败: 数据解析失败, 请将log文件反馈到issue页:\n{}'.format(issue_page)
user_warning = '提取失败: 该用户不存在, 若存在, 请前往issue页反馈:\n{}'.format(issue_page)
token_warning = '运行失败: guest_token获取失败, 请前往issue页反馈:\n{}'.format(issue_page)
parse_warning = '解析失败: 跳过解析此数据, 请带上错误数据信息前往issue页反馈:\n{}\n{}'.format(
    issue_page, '{}')
cookie_warning = '参数错误: 输入的cookie格式错误, 请参考教程获取cookie:\n{}\n'.format(
    cookie_tips_page)
http_warning = '\r提取失败{}: http访问异常, 状态码: {} -> {}'
timeout_warning = '\r网络超时: 服务器未响应或断开链接, 正在重试...{}'
download_timeout_warning = '\r{} {}{}'
proxy_warning = '参数错误: 代理格式错误, 格式: [ip/域名]:[端口], 示例: 127.0.0.1:7890'
user_unavailable_warning = '\r提取失败: 该用户已锁定/冻结, 访问锁定用户需要设置已关注账号的cookie'
age_restricted_warning = '\r提取失败: 该用户已设置年龄限制, 访问需要设置账号cookie'
# tweet_unavailable_warning = '\r提取失败: 该推文的用户已锁定/冻结, 访问锁定推文需要设置已关注账号的cookie'
network_error_warning = '网络连接失败, 请检查代理设置(程序默认使用系统代理)'
proxy_error_warning = '代理连接失败, 请检查代理是否开启/代理设置是否正确'
# wrong_url_warning = '提取失败: 错误的推文/推主主页链接'
# not_exist_warning = '提取失败: 该推文已删除/不存在'
# tw_id_waring = '格式错误: 推文id必须为纯数字串'
input_warning = '解析失败: 错误的链接或命令'
check_update_warning = '检查更新失败, 程序继续运行, 失败信息:\n{}'
need_cookie_warning = '\r目前访问推特的media列表接口需要登录账号, 故请先设置cookie再爬取'
dl_nothing_warning = '未爬取到任何有效数据'
input_num_warning = '请输入正确数字（回车继续）'
queue_empty_warning = '\r超过30秒未从任务队列中获取到数据'

# normal str
task_finish = '\r文件下载任务已完成 {}/{}, 用时 {}s, 保存路径: {}'
cookie_purge_success = '自定义cookie清除成功\n'
cookie_success = '\n自定义cookie导入成功\n'
input_cookie_ask = f'请复制cookie并粘贴到下方, 再单击回车确认(留空直接回车为清除cookie)\n* cookie获取教程：{cookie_tips_page}\n'
max_concurrency_ask = '下载线程数过高会使下载变慢，请勿设置过大\n\n' \
                      '0.返回\n\n' \
                      '请输入下载线程数，建议设置1~32之间（默认8）：'
set_type_ask = '输入数字选择，可多选，如“13”就是包含图片和视频\n\n' \
               '0.返回\n' \
               '1.下载图片\n' \
               '2.下载动图\n' \
               '3.下载视频\n' \
               '4.下载文字\n' \
               '5.所有\n\n' \
               '请输入（默认所有）：'
retweeted_status_ask = '是否下载转推\n\n' \
                       '0.返回\n' \
                       '1.是\n' \
                       '2.否\n' \
                       '请输入（默认是）：\n\n'
quoted_status_ask = '是否下载引用推文\n\n' \
                    '0.返回\n' \
                    '1.是\n' \
                    '2.否\n' \
                    '请输入（默认是）：\n\n'
download_settings_ask = '输入数字\n\n' \
                        '0.返回\n' \
                        '1.设置下载类型\n' \
                        '2.设置下载线程数\n' \
                        '3.设置是否下载引用推文\n' \
                        '4.设置是否下载转推\n\n' \
                        '请输入：'
# input_tw_id_ask = '请输入推文id(支持批量, 空格分隔), 再单击回车确认\n'
reset_ask = '单击回车键->退出程序, 输入任意内容+回车->重置脚本\n'
continue_ask = '单击回车键->退出程序, 输入任意内容+回车->继续提取\n'
input_ask = '输入命令数字或推文/推主链接 (支持批量, 一行一条, 双击回车确认)\n\n' \
            '0.退出脚本\n' \
            '1.设置自定义cookie\n' \
            '2.设置下载参数\n\n' \
            '请输入命令或链接：'
exit_ask = '\n单击回车键退出程序\n'
