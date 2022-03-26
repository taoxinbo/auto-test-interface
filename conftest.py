import logging

import pytest
from Config.VarConfig import *
from Config.servers import run_server


@pytest.fixture(scope='session')
def clear_auto_test_data():
    # run_server("oracle_startAll_interfaceauto", "oracle_stopAll_interfaceauto", 'fanek', 'fanek',
    #            'http://10.60.48.154:8080')
    # print("重启jenkins脚本执行完成了")
    logging.info("调用'Del_Request_pre_and_Response.py'" + "\n" + "-" * 137)
    os.system(r'python ' + baseDir + '\TestScript\Del_Request_pre_and_Response.py')
    logging.info("调用'Clean_Oracle_DB.py'" + "\n" + "-" * 137)
    os.system(r'python ' + baseDir + '\TestScript\Clean_Oracle_DB.py')
    yield


