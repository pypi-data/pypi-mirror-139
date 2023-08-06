#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   apischema.py    
@Author  :   YinJian
@Time    :   2022/1/21 10:13 AM 
"""
import json

import numpy as np
import pandas as pd

from datavita.core.schema.baseschema import BaseSchema


class RequestSchema(BaseSchema):
    def __init__(
            self,
            request_name: str = '',
            url: str = '',
            method: str = '',
            params: str = None,
            data: str = None,
            headers: dict = None,
            **kwargs
    ):
        super().__init__()
        self.request_name = request_name
        self.headers = headers
        self.url = url
        self.method = method
        self.params = params
        self.data = data
        self.request_time = 0


class ResponseSchema(BaseSchema):
    def __init__(
            self,
            url: str = '',
            api_name: str = '',
            method: str = '',
            request: RequestSchema = None,
            status_code: int = None,
            headers: dict = None,
            content: str = None,
            **kwargs
    ):
        super().__init__()
        self.api_name = api_name,
        self.url = url
        self.method = method
        self.request = request
        self.status_code = status_code
        self.content = content
        self.response_time = 0
        self.headers = headers or {}

    def convert_df_result(self):
        """
        统一返回格式
        :return:
        """
        content_list = self.content
        if content_list:
            keys = [str(x) for x in np.arange(len(content_list))]
            list_json = dict(zip(keys, content_list))
            str_json = json.dumps(list_json, indent=2, ensure_ascii=False)
            json_data = json.loads(str_json)
            temp_df = pd.DataFrame(json_data)
            temp_df = temp_df.T
            return temp_df
        else:
            return pd.DataFrame()
