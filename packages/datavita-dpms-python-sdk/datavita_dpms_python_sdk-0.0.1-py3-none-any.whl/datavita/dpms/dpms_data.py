#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   dpms_data.py    
@Author  :   YinJian
@Time    :   2022/1/20 4:28 PM 
"""
import typing

import pandas as pd

from datavita.core.common import contants
from datavita.core.common.auth import Auth
from datavita.core.exc.exception import DVException
from datavita.core.transport.apitransport import ApiTransport
from datavita.core.utils import log
from datavita.core.utils.param_generate import str_list_param_check, get_now_day_num


class DpmsData(object):
    """
        中台数据
        初始化固定参数 auth 超时 最大重试次数
    """

    def __init__(
            self,
            auth: typing.Optional[Auth] = None,
            base_url: str = contants.BASE_URL,
            timeout: int = contants.SESSION_PERIOD_TIMEOUT,
            max_retries: int = contants.MAX_RETRIES,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.auth = auth
        self.logger = log.default_logger

    def _send(self, api_name, params_dict):
        res = pd.DataFrame()
        try:
            # 构建公共的请求
            response = ApiTransport(auth=self.auth,
                                    max_retries=self.max_retries,
                                    timeout=self.timeout,
                                    api_name=api_name,
                                    params_dict=params_dict).send()
            res = response.convert_df_result()
            return res
        except Exception as e:
            if isinstance(e, DVException):
                e.logg_dev_str()
            else:
                DVException(location_method="datavita.dpms.dpms_data.DpmsData._send", msg=repr(e)).logg_dev_str()
            return res

    def GetClfDataRs(self, clfCode: object = None, clfType: str = 'HC1') -> pd.DataFrame:
        """
            按照分类 code 提取数据

        :param clfCode: 分类代码
        :param clfType: 默认值 HC1
        :return: Pandas.DataFrame
        """
        clf_code = str_list_param_check(clfCode, 10)
        params = {
            'clfCode': clf_code,
            'clfType': clfType
        }
        return self._send(api_name="GetClfDataRs", params_dict=params)

    def GetSupplyChainRs(self, primaryCode: object = None, relationship: int = -1, importance: int = 4,
                         steps: int = 1) -> pd.DataFrame:
        """
            按照产品名提取产业链上下游产品

        :param primaryCode: 限制一个，为 str/list
        :param relationship: 必填 1 为父级，关联产品是主产品的父级 -1 为子级，关联产品是主产品的子级
        :param importance: （选填）：默认为4级（大于等于）
        :param steps: steps: (选填) 步数，默认1度（限制5度）
        :return: Pandas.DataFrame
        """
        product_code_list = str_list_param_check(primaryCode, 10)
        params = {
            "productCodeList": product_code_list,
            'relationship': relationship,
            'steps': steps,
            'importance': importance,
        }
        return self._send(api_name="GetSupplyChainRs", params_dict=params)

    def GetProductRs(self, productCodeList: object = None, relationship: int = -1, steps: int = 1) -> pd.DataFrame:
        """
            按照产品名提取产业链子父级产品

        :param productCodeList: 限制一个，为 str/list
        :param relationship: 必填 1 为父级，关联产品是主产品的父级 -1 为子级，关联产品是主产品的子级
        :param steps: (选填) 步数，默认1度（限制5度）
        :return: Pandas.DataFrame
        """
        product_code_list = str_list_param_check(productCodeList, 10)
        params = {
            "productCodeList": product_code_list,
            'relationship': relationship,
            'steps': steps
        }
        return self._send(api_name="GetProductRs", params_dict=params)

    def GetProductDataRs(self, primaryCode: object = None, strategy: bool = False) -> pd.DataFrame:
        """
            按照产品 code 提取数据

        :param primaryCode: 限制一个，为 str / list
        :param strategy: （选填）：默认取False
        :return: Pandas.DataFrame
        """
        primary_code = str_list_param_check(primaryCode, 10)
        params = {
            "productCode": primary_code,
            'strategy': str(strategy).lower()
        }
        return self._send(api_name="GetProductDataRs", params_dict=params)

    def GetEdb(self, dataCode: object = None, startDay: int = 19900101, endDay: int = 0, pivot: bool = False,
               windId: bool = False) -> pd.DataFrame:
        """
            按 datacode 或 windcode 提取数据值

        :param windId: (选填) 如果为 True datacode 为 wind_code, 默认为 False
        :param pivot: 如果为 True，返回宽表形式，如果为 False，返回窄表形式。默认为 True
        :param endDay: end_day 终止时间（选填），‘yyyymmdd’，默认值为今天的日期
        :param startDay: start_day 起始时间（选填），‘yyyymmdd’ ，默认值为 ‘19900101’
        :param dataCode: 如果只有一个，允许 str 格式 / list 格式，如果有多个，必须 list
        :return: Pandas.DataFrame
        """
        datacode = str_list_param_check(dataCode, 10)
        end_day = get_now_day_num(endDay)
        params = {
            'dataCode': datacode,
            'startDay': startDay,
            'endDay': end_day,
            'windId': str(windId).lower()
        }
        df = self._send(api_name="GetEdb", params_dict=params)
        if pivot:
            df['dataDay'] = pd.to_datetime(df['dataDay'], errors='coerce', format='%Y%m%d')
            del df['dataName']
            # df = df.set_index("dataDay")
            df = df.pivot(index='dataDay', columns='dataCode', values='dataValue')
            return df
        else:
            return df

    def GetDataInfo(self, dataCode: object = None, windId: bool = False) -> pd.DataFrame:
        """
            按 datacode 或 windcode 提取数据属性

        :param dataCode: (选填) 如果为 True datacode 为 wind_code, 默认为 False
        :param windId: 如果只有一个，允许 str 格式 / list 格式，如果有多个，必须 list
        :return: Pandas.DataFrame
        """
        data_code = str_list_param_check(dataCode, 10)
        params = {
            "dataCode": data_code,
            'wind_id': str(windId).lower()
        }
        return self._send(api_name="GetDataInfo", params_dict=params)

    def GetPanelData(self, dataCode: str = '', pageNum: int = 1, pageSize: int = 10000, ) -> pd.DataFrame:
        """
            非时间序列表数据提取

        :param pageSize:
        :param pageNum:
        :param dataCode: 非时序表数据编码 限制一个
        :return: Pandas.DataFrame
        """
        params = {
            "dataCode": dataCode,
            'pageNum': pageNum,
            "pageSize": pageSize
        }
        return self._send(api_name="GetPanelData", params_dict=params)
