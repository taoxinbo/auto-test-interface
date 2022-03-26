# coding=utf-8
# 2020-12-16
# TaoXB
# 此文件是自动化测试Public接口:

import os
import sys, pytest
# 当前文件所在目录都添加到sys.path中，系统可以找到需要引用的模块
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from Action.extract import *
# 从文件所在目录中导入Log.py文件中所有内容
from Action.Log import *
from Config.VarConfig import *
from Config.read_excel import DoExcsl
from Config.DBConfig import *
sheet1 = 'Public'
excel_path1 = baseDir + "/ExcelData/" + "Public.xlsx"
data = DoExcsl(case_id='all', sheet=sheet1, excel_path=excel_path1).read_case()
read_excel = DoExcsl(case_id='all', sheet=sheet1, excel_path=excel_path1)

# 对'执行结果列'和‘异常信息列’进行清空
for j in range(2, get_row_num(excel_path1, sheet1) + 1):
    read_excel.write_excel(j, test_res_col, '')
    read_excel.write_excel(j, test_inf_col, '')


@pytest.mark.test
@pytest.mark.usefixtures("clear_auto_test_data")
class Test_Auto:

    @pytest.mark.parametrize("test_data", [tuple(i.values()) for i in data if i['is_run'] == "Y"])
    def test_inter(self, test_data, clear_auto_test_data):
        try:
            # 对'是否执行'为'Y'内容进行执行自动化
            # 获取接口名称的内容
            APIName = test_data[2]
            logging.info(f"APIName：{APIName}")
            # print('APIName的值：',APIName)
            # 获取当前接口代码名称
            BANKname = APIName.split("_")[1]
            # 获取请求地址的内容
            RequestUrl = test_data[3]
            # 获取请求方式的内容
            RequestMethod = test_data[4]
            # 获取检查点的内容
            CheckPoint = test_data[7]
            # 检查点转化成字典格式
            CheckPoint_Dic = eval(CheckPoint)
            # print(CheckPoint_Dic)
            # 获取当前数接口的所在据库类型
            APIDB = test_data[8]
            # 获取SQL语句检查点的内容
            CheckPointsql = test_data[9]
            # print('CheckPointsql值：',CheckPointsql)
            # print('CheckPointsql类型：',type(CheckPointsql))
            # #print('长度：',len(CheckPointsql))
            # if len(CheckPointsql)>0:
            #     # 检查点转化成字典格式
            #     CheckPointsql_Dic = eval(CheckPointsql)
            #     print(CheckPointsql_Dic)
            #     # for k, v in CheckPointsql_Dic.items():
            #     #     print(k,":",v)
            # 获取‘标签内容参数化（每次跑都不一样的值）’的内容
            LabelMethod = test_data[6]

            # print('接口名称：%s，请求地址：%s，请求方式：%s'%(APIName,RequestUrl,RequestMethod))
            logging.info('接口名称：%s，请求地址：%s，请求方式：%s,检查点:%s ' % (APIName, RequestUrl, RequestMethod, CheckPoint))

            # 读取request文件中的内容
            with open(baseDir + '/XML/Public/' + BANKname + '/request/' + APIName + '.xml', encoding='utf-8') as fp:
                body1 = fp.read()

            body2 = body1

            if LabelMethod:
                print(f"LabelMethod:{LabelMethod}")
                LabelMethod_Dic = eval(LabelMethod)
                if len(LabelMethod) > 0 and isinstance(LabelMethod_Dic, dict):
                    # print(1)
                    for k, v in LabelMethod_Dic.items():
                        # print(k, ":", v)
                        body2 = v(k, body2)

            # soupUI的报文，需要加上以下内容
            headers = {'Content-Type': 'text/xml;charset=UTF-8'}
            # 遇到编码报错时候，对body进行encode，因为服务器之间传递的数据，必须是bytes
            r = requests.post(RequestUrl, data=body2.encode("utf-8"), headers=headers)
            # logging.info(f"测试结果是：{r.text}")

            # 在目录'ATS_Interface_Test_Public/XML/Public/'下的‘对应接口名称’下新建文件夹'request_pre'，存放处理过的报文
            # baseDir2=baseDir+"/ATS_Interface_Test_Public/XML/Public/CPSQ01/request_pre/"
            baseDir2 = baseDir + "/XML/Public/" + BANKname + "/request_pre/"
            if not os.path.exists(baseDir2):
                os.mkdir(baseDir2)

            dir_path2 = make_current_date_dir(baseDir2)

            # 把发之前处理过的报文body2，存储到文件夹'/ATS_Interface_Test_Public/XML/Public/某个接口/request_pre/'下
            with open(dir_path2 + '/' + APIName + '_' + 'request_pre' + '_' + str(
                    time.strftime("%Y%m%d%H%M%S")) + '.xml', 'w', encoding="utf-8") as fp:
                fp.write(body2)

            # print(APIName,'处理过发之前的报文：','\n',body2)
            # print(type(body2))

            # 在目录'/ATS_Interface_Test_Public/XML/Public/某个接口/'下新建文件夹'response'，存放返回的报文
            baseDir3 = baseDir + "/XML/Public/" + BANKname + "/response/"
            if not os.path.exists(baseDir3):
                os.mkdir(baseDir3)

            dir_path3 = make_current_date_dir(baseDir3)

            # 获取返回的报文，存储到文件夹'/ATS_Interface_Test/XML/DSP/某个银行/response/'下
            with open(dir_path3 + "/" + APIName + '_' + 'response' + '_' + str(
                    time.strftime("%Y%m%d%H%M%S")) + '.xml', 'w', encoding="utf-8") as fp:
                fp.write(r.text)

            # print(APIName,'返回的报文：','\n',r.text)

            # 放置不一致的检查点
            Err_l = {}
            # 校验检查的内容
            for Chekey, Cheval in CheckPoint_Dic.items():
                # print(Chekey, ":", Cheval)
                temp = re.search(r'&lt;%s>(.*?)&lt;/%s>' % (Chekey, Chekey), r.text)
                # 判断返回报文中检查点值不为空，获取检查点值，不然返回不存在。
                if temp is not None:
                    tempcode = re.search(r'&lt;%s>(.*?)&lt;/%s>' % (Chekey, Chekey), r.text).group(1)
                else:
                    tempcode = "返回的报文中%s不存在" % Chekey

                # assert temp is not None

                # 判断返回报文中检查点和excel是否一致
                if tempcode != Cheval:
                    Err_l[Chekey] = tempcode

                # assert tempcode == Cheval

            # 当数据库和SQL检查点，都有值，进行校验判断
            # if (len(CheckPointsql) > 0) and (len(str(APIDB)) > 0):
            if CheckPointsql:
                if APIDB:
                    # 遍历SQL检查点内容
                    for db_type, sql in eval(CheckPointsql).items():
                        # print(typ,":",sql)
                        # print(APIDB)
                        # 校验Oracle数据库返回的各种情况
                        if APIDB == 'ORA':
                            # 如果是主库，调用主库的数据连接
                            if db_type == 'mai':
                                Ora_num = Oracle_DB(mai_ora_ip, mai_ora_sid, mai_ora_user, mai_ora_pwd, sql)
                                # print('Ora_num值',Ora_num)
                                if Ora_num == 0 or Ora_num == None:
                                    Err_l['没数据或存在问题的sql'] = sql
                                    print(Err_l)
                                    break
                                elif Ora_num == "表或视图不存在":
                                    Err_l['表或视图不存在的sql'] = sql
                                    print(Err_l)
                                    break
                                elif Ora_num == "数据库登陆失败":
                                    Err_l['数据库登陆失败'] = '请检查登陆数据库用户名或密码！'
                                    print(Err_l)
                                    break
                                elif Ora_num == "执行SQL出现未知错误":
                                    Err_l['执行SQL出现未知错误'] = '请检查登陆数据库用户名或密码或sql！'
                                    print(Err_l)
                                    break
                            # 如果是中间库，调用中间库的数据连接
                            elif db_type == 'imp':
                                Ora_num = Oracle_DB(imp_ora_ip, imp_ora_sid, imp_ora_user, imp_ora_pwd, sql)
                                # print('Ora_num值',Ora_num)
                                if Ora_num == 0 or Ora_num == None:
                                    Err_l['没数据或存在问题的sql'] = sql
                                    print(Err_l)
                                    break
                                elif Ora_num == "表或视图不存在":
                                    Err_l['表或视图不存在的sql'] = sql
                                    print(Err_l)
                                    break
                                elif Ora_num == "数据库登陆失败":
                                    Err_l['数据库登陆失败'] = '请检查登陆数据库用户名或密码！'
                                    print(Err_l)
                                    break
                                elif Ora_num == "执行SQL出现未知错误":
                                    Err_l['执行SQL出现未知错误'] = '请检查登陆数据库用户名或密码或sql！'
                                    print(Err_l)
                                    break
                            else:
                                Err_l['主库或中间库填错'] = '请检查%s！' % db_type

                        # 校验mysql数据库返回的各种情况
                        elif APIDB == 'MYS':
                            # 如果是主库，调用主库的数据连接
                            if db_type == 'mai':
                                Mys_num = MySQL_DB(mai_my_host, mai_my_port, mai_my_user, mai_my_passwd, mai_my_db,
                                                   sql)
                                if Mys_num == 0 or Mys_num == None:
                                    Err_l['没数据或存在问题的sql'] = sql
                                    print(Err_l)
                                    break
                                elif Mys_num == "表或视图不存在":
                                    Err_l['表或视图不存在的sql'] = sql
                                    print(Err_l)
                                    break
                                elif Mys_num == "数据库登陆失败":
                                    Err_l['数据库登陆失败'] = '请检查登陆数据库用户名或密码！'
                                    print(Err_l)
                                    break
                                elif Mys_num == "数据库不存在":
                                    Err_l['数据库不存在'] = '请检查数据库是否正确！'
                                    print(Err_l)
                                    break
                                elif Mys_num == "执行SQL出现未知错误":
                                    Err_l['执行SQL出现未知错误'] = '请检查登陆数据库用户名或密码或sql！'
                                    print(Err_l)
                                    break
                            # 如果是中间库，调用中间库的数据连接
                            elif db_type == 'imp':
                                Mys_num = MySQL_DB(imp_my_host, imp_my_port, imp_my_user, imp_my_passwd, imp_my_db,
                                                   sql)
                                if Mys_num == 0 or Mys_num == None:
                                    Err_l['没数据或存在问题的sql'] = sql
                                    print(Err_l)
                                    break
                                elif Mys_num == "表或视图不存在":
                                    Err_l['表或视图不存在的sql'] = sql
                                    print(Err_l)
                                    break
                                elif Mys_num == "数据库登陆失败":
                                    Err_l['数据库登陆失败'] = '请检查登陆数据库用户名或密码！'
                                    print(Err_l)
                                    break
                                elif Mys_num == "数据库不存在":
                                    Err_l['数据库不存在'] = '请检查数据库是否正确！'
                                    print(Err_l)
                                    break
                                elif Mys_num == "执行SQL出现未知错误":
                                    Err_l['执行SQL出现未知错误'] = '请检查登陆数据库用户名或密码或sql！'
                                    print(Err_l)
                                    break
                            else:
                                Err_l['主库或中间库填错'] = '请检查%s！' % db_type

                        # 数据库类型填的不对，直接返回
                        else:
                            Err_l['错误的数据库类型'] = APIDB

            if len(Err_l) == 0:
                print("报文%s测试通过" % (APIName))
                print("=" * 80)
                logging.info("报文%s测试通过" % (APIName) + "\n" + "=" * 80)
                read_excel.write_excel(int(test_data[0]) + 1, test_res_col, 'Y')
            else:
                print("测试不通过，报文%s中" % (APIName) + "校验不一致的内容:" + str(Err_l))
                print("=" * 80)
                logging.info("测试不通过，报文%s中" % (APIName) + "校验不一致的内容:" + str(Err_l) + "\n" + "=" * 80)
                read_excel.write_excel(int(test_data[0] + 1), test_res_col, 'N')
                read_excel.write_excel(int(test_data[0] + 1), test_inf_col, "校验不一致的内容:" + str(Err_l))

            assert len(Err_l) == 0

        except Exception as err:
            # 发生其他异常时，打印异常堆栈信息
            # traceback.print_exc()
            print('print的内容：', traceback.format_exc())
            logging.debug('logging.debug的内容：' + str(traceback.format_exc()))
            raise err


if __name__ == '__main__':
    #  启动单元测试
    unittest.main(verbosity=2)
