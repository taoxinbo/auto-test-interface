# encoding=utf-8
import cx_Oracle
import time
import traceback
import xlsxwriter
import xlwt  # 操作excel模块
import os
import sys

# 当前文件所在目录都添加到sys.path中，系统可以找到需要引用的模块
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
# 从文件所在目录中导入Log.py文件中所有内容
from Action.Log import *
from Config.DBConfig import *
from Config.VarConfig import *
from Config.Del_or_Upd_SQL import *


def Clean_Oracle_DB(ora_ip, ora_sid, ora_user, ora_pwd, sql, DBName):
    # 创建数据库连接,配置监听并连接
    # cx_Oracle.connect('username','pwd','ora的tns信息')
    # oracle数据库的tns信息，从tnsnames.ora中找到plsql可用的配置项，将该配置项直接拷贝过来即可
    ora_tns = cx_Oracle.makedsn(ora_ip, 1521, ora_sid)
    conn = cx_Oracle.connect(ora_user, ora_pwd, ora_tns)
    # 操作游标
    cursor = conn.cursor()

    print("开始清除或修改Oracle环境的%s数据......" % DBName)
    logging.info("开始清除或修改Oracle环境的%s数据......" % DBName)

    try:
        # 遍历sql语句
        for sql1 in sql:
            #cursor.execute(sql,tenantid)
             cursor.execute(sql1)
            # number2 = cursor.fetchall()
            # for loanNumber in number3:
            #     print(loanNumber)
        print("已删除或修改Oracle环境的%s数据！"%DBName+ "\n" + "=" * 80)
        logging.info("已删除或修改Oracle环境的%s数据！"%DBName+ "\n" + "=" * 80)
    except Exception as err:
        # 发生其他异常时，打印异常堆栈信息
        print(traceback.print_exc())
        logging.debug("执行SQL报错：" + str(traceback.format_exc()))

    # 关闭游标
    cursor.close()
    # 提交事务
    conn.commit()
    # 关闭数据库连接
    conn.close()


if __name__ == '__main__':
    Clean_Oracle_DB(imp_ora_ip, imp_ora_sid, imp_ora_user, imp_ora_pwd, Imp_SQL, '中间库')
    Clean_Oracle_DB(mai_ora_ip, mai_ora_sid, mai_ora_user, mai_ora_pwd, Mai_SQL, '主库')