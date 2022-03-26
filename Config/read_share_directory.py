# -*- coding: utf-8 -*-
# @Time : 2021/12/24 15:17
# @Author : chengguo
# @File : read_share_directory.py
# @脚本功能描述：
import os,time
import logging
from pathlib import Path

logname = f"Unmi-{time.strftime('%Y-%m-%d', time.localtime(time.time()))}.log"

path = r'\\10.60.47.127\ats_task\log' + f"\\{logname}"
print(path)



def read_log(keyword):
    Data = path.replace("\\", "/", 5)
    Data = Data.replace("\\\\", "\\", 5)
    with open(Data, "rb") as f:
        for i in f.readlines():
            if keyword in i.decode().__str__():
                logging.warning(i.decode())
                logging.warning("关键字判断成功")
            else:
                logging.warning("没有这个 关键字")


def clean_file():
    if os.path.exists(f'//10.60.47.127/ats_task/log/{logname}'):
        logging.info('--开始删除文件---')
        os.remove(f'//10.60.47.127/ats_task/log/{logname}')
        logging.info(f"文件删除成功")
    else:
        logging.info("文件不存在")


if __name__ == '__main__':
    read_log('1')