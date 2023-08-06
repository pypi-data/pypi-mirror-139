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
import json
import typing
import requests
from requests.adapters import HTTPAdapter, Retry

from datavita.core.common import contants
from datavita.core.common.auth import Auth
from datavita.core.exc.exception import ConvertException
from datavita.core.schema.apischema import RequestSchema, ResponseSchema
from datavita.core.utils import log
from datavita.dpms.dpms_apis import dpms_apis_dict


class CommonTransport(object):
    """
        统一ETL
    """

    def __init__(
            self,
            auth: typing.Optional[Auth],
    ):
        self.auth = auth
        self.logger = log.default_logger

    @staticmethod
    def load_adapter(max_retries) -> HTTPAdapter:
        backoff_factor = 0.3
        status_forcelist = (500, 502, 504)
        adapter = HTTPAdapter()
        adapter.max_retries = Retry(
            total=max_retries,
            read=max_retries,
            connect=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        return adapter

    @staticmethod
    def convert_response(r: requests.Response) -> ResponseSchema:
        """
            转换成包装过的response
        :param r: 请求结果
        :return:
        """
        content = ''
        status_code = 500
        try:
            content = json.loads(r.text)['result']
            status_code = json.loads(r.text)['code']
        except Exception:
            raise ConvertException(location_method="datavita.core.transport.apitransport.ApiTransport.convert_response",
                                   msg="结果转换出现未知错误,返回值 text 数据丢失",
                                   err_name='通用返回值转换异常')
        return ResponseSchema(
            url=r.url,
            method=r.request.method,
            status_code=status_code,
            content=content,
        )

    def _build_http_request(self, api_name, params_dict) -> RequestSchema:
        url = dpms_apis_dict.get(api_name).get('url').format(base_url=contants.BASE_URL)
        method = dpms_apis_dict.get(api_name).get('method')
        if method == 'GET':
            headers = {
                'Accept': '*/*',
                'Content-Type': 'application/json',
                'accessKey': self.auth.access_id,
                'accessSecret': self.auth.access_secret
            }
        else:
            headers = {
                'Accept': '*/*',
                'Content-Type': 'application/json',
                'accessKey': self.auth.access_id,
                'accessSecret': self.auth.access_secret
            }
        return RequestSchema(
            api_name=api_name,
            params=params_dict,
            data=json.dumps(params_dict),
            url=url,
            method=method,
            headers=headers
        )
