# external page url
donate_page = 'https://afdian.net/@mengzonefire'
issue_page = 'https://github.com/mengzonefire/twitter-media-downloader/issues'
release_page = 'https://github.com/mengzonefire/twitter-media-downloader/releases'
cookie_tips_page = 'https://git.io/how_to_get_cookies_cn'

# warning str
log_warning = '\n运行错误: log文件已保存到 {}\n'
api_warning = '提取失败: 数据解析失败, 请将log文件反馈到issue页:\n{}'.format(issue_page)
user_warning = '提取失败: 该用户不存在, 若存在, 请前往issue页反馈:\n{}'.format(issue_page)
token_warning = '运行失败: guest_token获取失败, 请前往issue页反馈:\n{}'.format(issue_page)
cookie_warning = '参数错误: 输入的cookie格式错误, 请参考教程获取cookie:\n{}\n'.format(
    cookie_tips_page)
http_warning = '提取失败{}: http访问异常, 状态码: {} -> {}'
proxy_warning = '参数错误: 代理格式错误, 格式: [ip/域名]:[端口], 示例: 127.0.0.1:7890'
user_unavailable_warning = '提取失败: 该用户已锁定/冻结, 访问锁定用户需要设置已关注账号的cookie(输入set cookie命令)'
age_restricted_warning = '提取失败: 该用户已设置年龄限制, 访问需要设置账号cookie(输入set cookie命令)'
tweet_unavailable_warning = '提取失败: 该推文的用户已锁定/冻结, 访问锁定推文需要设置已关注账号的cookie(输入set cookie命令)'
network_error_warning = '网络连接失败, 请检查代理设置(程序默认使用系统代理)'
proxy_error_warning = '代理连接失败, 请检查代理是否开启/代理设置是否正确'
wrong_url_warning = '提取失败: 错误的推文/推主主页链接'
not_exist_warning = '提取失败: 该推文已删除/不存在'
tw_id_waring = '格式错误: 推文id必须为纯数字串'
input_warning = '解析失败: 错误的链接或命令'
check_update_warning = '检查更新失败, 程序继续运行, 失败信息:\n{}'
need_cookie_warning = '目前访问推特的media列表接口需要登录账号, 故请先设置cookie再爬取(输入set cookie命令)'
dl_nothing_warning = '未爬取到任何有效数据'

# normal str
task_finish = '全部文件下载完成, 保存到路径: {}\n'
cookie_purge_success = '自定义cookie清除成功\n'
cookie_success = '\n自定义cookie导入成功\n'
input_cookie_ask = f'请复制cookie并粘贴到下方, 再单击回车确认(留空直接回车为清除cookie)\n* cookie获取教程：{cookie_tips_page}\n'
input_tw_id_ask = '请输入推文id(支持批量, 空格分隔), 再单击回车确认\n'
reset_ask = '单击回车键->退出程序, 输入任意内容+回车->重置脚本\n'
continue_ask = '单击回车键->退出程序, 输入任意内容+回车->继续提取\n'
input_ask = '请输入1.或2.\n' \
            '1. 命令: "exit"、"set cookie" (不输入双引号, 单击回车确认)\n' \
            '# "exit"退出程序, "set cookie"用于设置cookie\n' \
            '2. 推文/推主链接 (支持批量, 一行一条, 双击回车确认):'
exit_ask = '\n单击回车键退出程序\n'
