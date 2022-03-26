# encoding=utf-8
import os
import sys

# 获取当前文件所在目录的父目录的绝对路径
baseDir = os.path.dirname(os.path.dirname(__file__))
# 指定excel的位置
# file_path = baseDir + "/ExcelData/"+"DSP.xls"
file_path = baseDir + "/ExcelData/" + "Public.xls"
# 接口地址相关内容
# 接口的IP地址
# ip="10.60.44.245"
ip = "10.60.47.127"
# 接口对应的端口
# port="5150"
port = "3130"


##########=======测试用例集合sheet对应的序号====############
# excel中'是否执行'所在的列，因为从0开始算，5代表是第6列
test_act_col = 5
# excel中'APIName'所在的列，因为从0开始算，2代表是第3列
test_api_col = 2
# excel中'RequestUrl'所在的列，因为从0开始算，3代表是第4列
test_url_col = 3
# excel中'请求方式'所在的列，因为从0开始算，4代表是第5列
test_meth_col = 4
# excel中'标签内容参数化（每次跑都不一样的值）'所在的列，因为从0开始算，6代表是第7列
test_lab_col = 6
# excel中'检查点'所在的列，因为从1开始算，7代表是第8列
test_che_col = 7
# excel中'数据库类型'所在的列，因为从1开始算，8代表是第9列
test_sql_db = 8
# excel中'SQL语句检查点'所在的列，因为从1开始算，9代表是第10列
test_che_sql = 9
# excel中'执行结果'所在的列，因为从1开始算，11代表是第11列
test_res_col = 11
# excel中'异常信息'所在的列，因为从1开始算，12代表是第12列
test_inf_col = 12

########====Oracle数据库的设置====##########


# # 本机Oracle数据库
# ora_ip = "127.0.0.1"
# # Oracle数据库对应的实例
# ora_sid = "ATSDB"
# # Oracle数据库对应的用户名
# ora_user = "jats003"
# # Oracle数据库对应的密码
# ora_pwd = "jats003"

# # 92服务器Oracle数据库
# ora_ip = "10.60.44.92"
# # Oracle数据库对应的实例
# ora_sid = "ATSDB"
# # Oracle数据库对应的用户名
# ora_user = "jats034"
# # Oracle数据库对应的密码
# ora_pwd = "jats034"

########====mysql数据库的设置====##########

# # 本机mysql数据库
# my_host = "127.0.0.1"
# # mysql数据库对应的端口
# my_port = 3306
# # mysql数据库对应的用户名
# my_user = "root"
# # mysql数据库对应的密码
# my_passwd = "123456"
# # mysql数据库对应的数据库
# my_db = "jats268reg"

# my_host = "10.60.44.221"
# # mysql数据库对应的端口
# my_port = 3306
# # mysql数据库对应的用户名
# my_user = "root"
# # mysql数据库对应的密码
# my_passwd = "Mysql@123"
# # mysql数据库对应的数据库
# my_db = "jats2610reg"

#---推送接口的配置---
# 消息中心接口
url_msgList = 'http://10.60.47.127:3130/newmbs/bizframe/default/jsp/msgList.jsp'
# 查询消息接口参数
msgList_params = {"msgTitle": "贷款合同导出", "start": 1, "limit": 20, "pageNum": 1, "pageCount": 2, "totalCount":30,"_respType": "page"}

# 登陆用户名
LoginName = "Felix"
# 登陆密码
PassWord = "fingard@1"
# 登陆租户ID
TenantId = "10001"
# 拼接的接口的URI
url = "http://" + ip + ":" + port + "/newmbs/systemlogin/login!login.do"
# 拼接的接口登陆信息
payload = "loginName=" + LoginName + "&password=" + PassWord + "&bizEncryptFalg=&resCode=bizSign&opCode=bizSignIn2&lockuserflag=&userlanguage=zh_CN&tenantid=" + TenantId + "&_token=638ecd47f97848609908af2341011157&undefined="
# 请求头信息
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
    'Postman-Token': "f4427f26-622d-4e84-8793-0028566dba14"
}
#---推送接口的配置---