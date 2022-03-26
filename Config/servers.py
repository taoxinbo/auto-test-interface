# -*- coding: utf-8 -*-
# @Time : 2021/12/28 15:58
# @Author : chengguo
# @File : servers.py
# @脚本功能描述：
import logging
import time, os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from Config.jenkins_common import jenkins_operation
from Config.read_share_directory import clean_file

jenkins_server_url = 'http://10.60.48.154:8080'
# 定义用户的User Id 和 API Token，获取方式同上文
user_id = 'fanek'
api_token = 'fanek'


def run_server(start_servername, stop_servername, api_token, user_id, jenkins_server_url):
    """
    :param start_servername: 要启动的job名称
    :param stop_servername: 要停用的job名称
    :param api_token: 密码
    :param user_id: 账号
    :param jenkins_server_url: 登录地址
    :return:None
    """
    stop_server_build_list = jenkins_operation(api_token=api_token, user_id=user_id, job_name=stop_servername,
                                               jenkins_server_url=jenkins_server_url).job_all_build_list()
    new_stop_server_build_list = []
    for i in stop_server_build_list:
        new_stop_server_build_list.append(i)
    logging.info(f"开始停止环境第一步")
    jenkins_operation(api_token=api_token, user_id=user_id, job_name=stop_servername,
                      jenkins_server_url=jenkins_server_url).run_job()
    time.sleep(120)
    # while True:
    #     print(len(new_stop_server_build_list) + 1)
    #     data = jenkins_operation(api_token=api_token, user_id=user_id, job_name=stop_servername,
    #                              jenkins_server_url=jenkins_server_url).job_all_build_list()
    #     print(len(data))
    #     if len(new_stop_server_build_list) + 1 == len(data):
    #         print(f"停止第一步成功了")
    #         break
    clean_file()
    logging.info("日志文件清理成功")
    start_server_build_list = jenkins_operation(api_token=api_token, user_id=user_id, job_name=start_servername,
                                                jenkins_server_url=jenkins_server_url).job_all_build_list()
    new_start_server_build_list = []
    for j in start_server_build_list:
        new_start_server_build_list.append(j)
    logging.info(f"开始启动环境第一步")
    jenkins_operation(api_token=api_token, user_id=user_id, job_name=start_servername,
                      jenkins_server_url=jenkins_server_url).run_job()
    time.sleep(60)
    logging.info(f"服务启动成功了")
    # while True:
    #     if len(new_start_server_build_list) + 1 == len(data):
    #         print(f"{i}服务启动成功了")
    #         break

    start_server_build_list = jenkins_operation(api_token=api_token, user_id=user_id,
                                                job_name='oracle_config-center_interface_auto',
                                                jenkins_server_url=jenkins_server_url).job_all_build_list()
    new_start_server_build_list = []
    for j in start_server_build_list:
        new_start_server_build_list.append(j)
    logging.info(f"开始启动环境第二步")
    jenkins_operation(api_token=api_token, user_id=user_id, job_name='oracle_config-center_interface_auto',
                      jenkins_server_url=jenkins_server_url).server.build_job("oracle_config-center_interface_auto",
                                                                              {"PROJECTNAME": "default",
                                                                               "PROJECTTITLE": r"\u591A\u94F6\u884C\u8D44\u91D1\u7BA1\u7406\u7CFB\u7EDF"})
    time.sleep(60)
    logging.info(f"服务启动成功了")
    # data = jenkins_operation(api_token=api_token, user_id=user_id, job_name='oracle_config-center_interface_auto',
    #                          jenkins_server_url=jenkins_server_url).job_all_build_list()
    # while True:
    #     if len(new_start_server_build_list) == len(data):
    #         print(f"第二步启动成功了")
    #         break
    logging.info(f"开始启动环境第二步")
    start_server_build_list = jenkins_operation(api_token=api_token, user_id=user_id,
                                                job_name='oracle_config-center_interface_auto',
                                                jenkins_server_url=jenkins_server_url).job_all_build_list()
    new_start_server_build_list = []
    for j in start_server_build_list:
        new_start_server_build_list.append(j)
    jenkins_operation(api_token=api_token, user_id=user_id, job_name='oracle_ats_interface_auto_pipline',
                      jenkins_server_url=jenkins_server_url).server.build_job("oracle_ats_interface_auto_pipline",
                                                                              {"PROJECTNAME": "default",
                                                                               "PROJECTTITLE": r"\u591A\u94F6\u884C\u8D44\u91D1\u7BA1\u7406\u7CFB\u7EDF"})
    time.sleep(1000)
    logging.info("环境全部启动完毕开始执行测试用例")
    # data = jenkins_operation(api_token=api_token, user_id=user_id, job_name='oracle_ats_interface_auto_pipline',
    #                          jenkins_server_url=jenkins_server_url).job_all_build_list()
    # while True:
    #     if len(new_start_server_build_list) == len(data):
    #         print(f"第三步启动成功了")
    #         break


if __name__ == '__main__':
    run_server("oracle_stopAll_interfaceauto", api_token, user_id, jenkins_server_url)
