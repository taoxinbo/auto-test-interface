# -*- coding: utf-8 -*-
# @Time : 2021/12/23 17:48
# @Author : chengguo
# @File : common_requests.py
# @脚本功能描述：

import requests


class Httprequests:
    @classmethod
    def send_http_request(cls, url: str, method='get', **kwargs: dict) -> requests.Response:
        """
        :param url: 地址
        :param method:请求方式 默认 get
        :param kwargs: 接口参数 、请求头
        :return:
        """
        if getattr(cls, 'session', None) is None:
            cls.session = requests.session()
        method = method.lower()
        return getattr(cls.session, method)(url, **kwargs)


