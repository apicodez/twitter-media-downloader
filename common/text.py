# external page url
issue_page = 'https://github.com/mengzonefire/twitter-media-downloader/issues'
release_page = 'https://github.com/mengzonefire/twitter-media-downloader/releases'
cookie_tips_page = 'https://git.io/how_to_get_cookies_cn'

# warning str
api_warning = '提取失败: 解析失败, 请检查log, 并前往issue页反馈:\n{}'.format(issue_page)
user_warning = '提取失败: 该用户不存在, 若存在, 请前往issue页反馈:\n{}'.format(issue_page)
token_warning = '运行失败: guest_token获取失败, 请前往issue页反馈:\n{}'.format(issue_page)
cookie_warning = '参数错误: 输入的cookie格式错误, 请参考教程获取cookie:\n{}'.format(
    cookie_tips_page)
cookie_para_warning = '参数错误: 请使用一对双引号" "包含全部cookie'
http_warning = '提取失败{}: http访问异常, 状态码: {}, 请前往issue页反馈:\n{}'
proxy_warning = '参数错误: 代理格式错误, 格式: [ip/域名]:[端口], 示例: 127.0.0.1:7890'
user_unavailable_warning = '提取失败: 该用户已锁定/冻结, 访问锁定用户需要设置已关注账号的cookie'
tweet_unavailable_warning = '提取失败: 该推文的用户已锁定/冻结, 访问锁定推文需要设置已关注账号的cookie'
network_error_warning = '网络连接失败, 请检查代理设置'
proxy_error_warning = '代理连接错误, 请检查代理设置是否正确'
wrong_url_warning = '提取失败: 错误的推文/推主主页链接'
not_exist_warning = '提取失败: 该推文已删除/不存在'
tw_id_waring = '格式错误: 推文id必须为纯数字串'
input_warning = '解析失败: 错误的链接或命令'

# normal str
cookie_success = '自定义cookie导入成功'
input_cookie_ask = '请复制cookie并粘贴到此处, 再单击回车确认\n'
input_tw_id_ask = '请输入推文id(支持批量, 空格分隔), 再单击回车确认\n'
reset_ask = '单击回车键->退出程序, 输入任意内容+回车->重置脚本\n'
continue_ask = '单击回车键->退出程序, 输入任意内容+回车->继续提取\n'
input_ask = '请输入1.或2.\n' \
            '1. 命令: "exit"、"set cookie" (不输入双引号, 单击回车确认)\n' \
            '# "exit"退出程序, "set cookie"用于设置cookie\n' \
            '2. 推文/推主链接 (支持批量, 一行一条, 双击回车确认):'
exit_ask = '\n单击回车键退出程序\n'
