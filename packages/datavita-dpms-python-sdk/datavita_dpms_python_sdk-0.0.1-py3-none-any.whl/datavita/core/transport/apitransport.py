#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 15:20
    @Author : Yin Jian
    @Version：V 0.1
    @File : comtransport.py
    @desc :
"""
import time
import typing

import requests

from datavita.core.common import contants
from datavita.core.common.auth import Auth
from datavita.core.exc.exception import ResponseException, DVException
from datavita.core.transport.comtransport import CommonTransport


class ApiTransport(CommonTransport):
    """
        统一api 调用
    """

    def __init__(
            self,
            auth: typing.Optional[Auth],
            max_retries: int = contants.MAX_RETRIES,
            timeout: int = contants.SESSION_PERIOD_TIMEOUT,
            api_name: str = '',
            params_dict: str = ''
    ):
        super().__init__(auth=auth)
        self.api_name = api_name
        self.params_dict = params_dict
        self.timeout = timeout
        self._adapter = self.load_adapter(max_retries if max_retries in (0, 1, 2) else 3)

    def send(self):
        """
            发送请求
        :return:
        """
        req = self._build_http_request(self.api_name, self.params_dict)
        try:
            session = requests.Session()
            session.mount("http://", adapter=self._adapter)
            session.mount("https://", adapter=self._adapter)
            req.request_time = time.time()
            session_resp = session.request(
                method=req.method,
                url=req.url,
                params=req.params,
                headers=req.headers,
                timeout=self.timeout,
            )
            if session_resp.status_code != 200:
                raise ResponseException(url=req.url,
                                        msg=str(session_resp.status_code) + ' : ' + contants.EXCEPTION_DICT.get(
                                            session_resp.status_code, '未匹配状态码'),
                                        location_method='datavita.core.transport.apitransport.ApiTransport.send')
            resp = self.convert_response(session_resp)
            resp.api_name = self.api_name
            resp.request = req
            resp.response_time = time.time()
            return resp
        except Exception as e:
            if isinstance(e, DVException):
                raise e
            else:
                raise DVException(location_method="datavita.core.transport.apitransport.ApiTransport.send", msg=repr(e))
