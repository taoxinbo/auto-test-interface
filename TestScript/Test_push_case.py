# -*- coding: utf-8 -*-
# @Time : 2021/12/23 17:50
# @Author : chengguo
# @File : Test_push_case.py
# @脚本功能描述：
import os
import sys, pytest

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from Action.extract import *
from Config.VarConfig import *
from Config.DBConfig import *
from Config.read_excel import DoExcsl
from Config.common_requests import Httprequests
from Config.read_share_directory import read_log

sheet1 = 'Push_case'
excel_path1 = baseDir + "/ExcelData/" + "Public.xlsx"
data = DoExcsl(case_id='all', sheet=sheet1, excel_path=excel_path1).read_case()
read_excel = DoExcsl(case_id='all', sheet=sheet1, excel_path=excel_path1)
# 对'执行结果列'和‘异常信息列’进行清空
for j in range(2, get_row_num(excel_path1, sheet1) + 1):
    read_excel.write_excel(j, test_res_col, '')
    read_excel.write_excel(j, test_inf_col, '')


# @pytest.mark.test
@pytest.mark.usefixtures("clear_auto_test_data")
class Test_Auto:
    @pytest.mark.parametrize("test_data", [tuple(i.values()) for i in data if i['is_run'] == "Y"])
    def test_inter(self, test_data, clear_auto_test_data):
        logging.info(f"---先发送错误请求 在会话中获取请求头，方便会话存取token-----")
        res = Httprequests.send_http_request(url=url, method='post', data=payload, headers=headers)
        logging.info(f"----------开始进行读取 token----------")
        token = re.match('JSESSIONID=.{32}', res.headers.get("Set-Cookie")).group().split("=")[1]
        logging.info(f"----------读取的 token为：{token}----------")
        logging.info(f"开始执行接口名称为:{test_data[2]}的接口")
        logging.info(f"发起请求的方式为：{test_data[4]}")
        logging.info(f"发起请求的参数为：{eval(test_data[6])}")
        logging.info(f"请求头的参数为：{headers}")
        res = Httprequests.send_http_request(url=test_data[3], method=test_data[4], data=eval(test_data[6]),
                                             headers=headers)
        try:
            logging.info(f"接口请求之后的返回值是：{res.json()}")
        except Exception as e:
            logging.info(f"接口请求失败:{e}")

        Err_l = {}
        # 当数据库和SQL检查点，都有值，进行校验判断
        # if (len(CheckPointsql) > 0) and (len(str(APIDB)) > 0):
        if test_data[9]:
            if test_data[8]:
                # 遍历SQL检查点内容
                for db_type, sql in eval(test_data[9]).items():
                    # print(typ,":",sql)
                    # print(APIDB)
                    # 校验Oracle数据库返回的各种情况
                    if test_data[8] == 'ORA':
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
                    elif test_data[8] == 'MYS':
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
                        Err_l['错误的数据库类型'] = test_data[8]

        # 执行 定时任务
        # 获取 消息中心 数据
        # res = Httprequests.send_http_request(url=url_msgList, method='post', data=msgList_params, headers=headers)
        # logging.info(f'{res.json()["data"]["listData"][0]["msg_content"]}')
        # if re.search(r"(?<=成功:)\d+", res.json()["data"]["listData"][0]["msg_content"]):
        #     success_data = re.search(r"(?<=成功:)\d+", res.json()["data"]["listData"][0]["msg_content"]).group()
        # else:
        #     success_data = re.search(r"(?<=成功)\d+", res.json()["data"]["listData"][0]["msg_content"].split(".")[0]).group()
        # if re.search(r"(?<=失败:)\d+", res.json()["data"]["listData"][0]["msg_content"]):
        #     fail_data = re.search(r"(?<=失败:)\d+", res.json()["data"]["listData"][0]["msg_content"]).group()
        # else:
        #     fail_data = re.search(r"(?<=失败)\d+", res.json()["data"]["listData"][0]["msg_content"].split(".")[0]).group()
        # logging.info(f"提取任务成功的条数为：{success_data}")
        # logging.info(f"提取任务失败的条数为：{success_data}")
        # logging.info(f"开始断言成功的条数")
        # logging.info(f'预期成功的条数：{eval(test_data[7])["Success"]}')
        # logging.info(f'实际成功的条数：{success_data}')
        # assert success_data == eval(test_data[7])["Success"]
        # logging.info(f"开始断言失败的条数")
        # logging.info(f'预期失败的条数：{eval(test_data[7])["Fail"]}')
        # logging.info(f'实际失败的条数：{fail_data}')
        # assert fail_data == eval(test_data[7])["Fail"]
        logging.info("传入关键字进行判断 接口是否请求成功")
        read_log(eval(test_data[7])['keyword'])