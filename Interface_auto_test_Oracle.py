# coding=utf-8
# 2020-12-21
# TaoXB
# 此文件是读取excel路径判断测试DSP还是ATS

from Action.extract import *
from Config.VarConfig import *

try:
    logging.info("调用'Del_Request_pre_and_Response.py'" + "\n" + "-" * 137)
    os.system(r'python ' + baseDir + '\TestScript\Del_Request_pre_and_Response.py')
    logging.info("调用'Clean_Oracle_DB.py'" + "\n" + "-" * 137)
    os.system(r'python ' + baseDir + '\TestScript\Clean_Oracle_DB.py')
    if (file_path.split("/")[2]).split(".")[0] == 'DSP':
        logging.info("调用'interface_auto_test_xml_DSP.py'" + "\n" + "-" * 137)
        os.system(r'python ' + baseDir + '\TestScript\interface_auto_test_xml_DSP.py')
    elif (file_path.split("/")[2]).split(".")[0] == 'Public':
        logging.info("调用'Test_interface_auto_test_xml_Public.py'" + "\n" + "-" * 137)
        os.system(r'python ' + baseDir + '\TestScript\Test_interface_auto_test_xml_Public.py')
    else:
        logging.info("指定excel未能识别" + "\n" + "-" * 137)

except Exception as err:
    # 发生其他异常时，打印异常堆栈信息
    # traceback.print_exc()
    print('print的内容：', traceback.format_exc())
    logging.debug('logging.debug的内容：' + str(traceback.format_exc()))
