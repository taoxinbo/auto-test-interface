# coding=utf-8
import re
import pytest
from Config.DingDingUtil import DingDingUtil
#
# # 本地使用这个执行
# pytest.main(["-vs",  "-m", "test", r'--alluredir=pytest_report/report/dirallure'])

# jenkins路径
pytest.main(["-vs", "-m", "test", r'--alluredir=allure-results'])
reportUrl = 'http://10.60.47.13:8080/job/ATS_%E6%8E%A5%E5%8F%A3%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95%E6%A1%86%E6%9E%B6/allure/'
DingDingUtil().sendUrl(url=reportUrl, title="ATS_接口自动化测试报告", message="ATS_接口自动化测试报告")
