# coding=utf-8
# 2020-12-16
# TaoXB
# 此文件是自动化测试Public接口:

import os
import sys, pytest, shutil
# 当前文件所在目录都添加到sys.path中，系统可以找到需要引用的模块
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from Action.extract import *
# 从文件所在目录中导入Log.py文件中所有内容
from Action.Log import *
from Config.VarConfig import *


def del_dir(path, dir):
    ls = os.listdir(path)
    # print(ls)
    for i in ls:
        c_path = os.path.join(path, i)
        if i == dir:
            shutil.rmtree(c_path, True)
        elif os.path.isdir(c_path):
            del_dir(c_path, dir)


def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)


if __name__ == '__main__':
    filepath1 = baseDir + "/allure-results/"
    # print(filepath1)
    print("开始删除上次的报告文件：allure-results下面的数据文件......")
    logging.info("开始删除上次的报告文件：allure-results下面的数据文件......")
    del_file(filepath1)
    print("已删除上次的报告文件：allure-results下面的数据文件！" + "\n" + "=" * 80)
    logging.info("已删除上次的报告文件：allure-results下面的数据文件！" + "\n" + "=" * 80)

    CUR_PATH = baseDir + "/XML/Public/"
    print("开始删除临时文件夹：request_pre和下面的数据......")
    logging.info("开始删除临时文件夹：request_pre和下面的数据......")
    del_dir(CUR_PATH, 'request_pre')
    print("已删除临时文件夹：request_pre和下面的数据！" + "\n" + "=" * 80)
    logging.info("已删除临时文件夹：request_pre和下面的数据！" + "\n" + "=" * 80)

    print("开始删除临时文件夹：response和下面的数据......")
    logging.info("开始删除临时文件夹：response和下面的数据......")
    del_dir(CUR_PATH, 'response')
    print("已删除临时文件夹：response和下面的数据！" + "\n" + "=" * 80)
    logging.info("已删除临时文件夹：response和下面的数据！" + "\n" + "=" * 80)
