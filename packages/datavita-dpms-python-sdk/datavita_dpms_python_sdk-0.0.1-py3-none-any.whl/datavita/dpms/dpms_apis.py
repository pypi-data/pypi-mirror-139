#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   dpms_apis.py    
@Author  :   YinJian
@Time    :   2022/1/20 4:28 PM 
"""
dpms_apis_dict = {
    'GetClfDataRs': {'url': '{base_url}/product/getClfDataRs',
                     'method': 'GET',
                     'name': '按照分类 code 提取数据'},
    'GetSupplyChainRs': {'url': '{base_url}/product/getSupplyChainRs',
                         'method': 'GET',
                         'name': '按照产品名提取产业链上下游产品'},
    'GetProductRs': {'url': '{base_url}/product/getProductRs',
                     'method': 'GET',
                     'name': '按照产品名提取产业链子父级产品'},
    'GetProductDataRs': {'url': '{base_url}/product/getProductDataRs',
                         'method': 'GET',
                         'name': '按照产品 code 提取数据'},
    'GetDataInfo': {'url': '{base_url}/time/dataInfo',
                    'method': 'GET',
                    'name': '按 datacode 或 windcode 提取数据属性'},
    'GetEdb': {'url': '{base_url}/time/tsdData',
               'method': 'GET',
               'name': '按 datacode 或 windcode 提取数据值'},
    'GetPanelData': {'url': '{base_url}/nontime/unTsdData',
                     'method': 'GET',
                     'name': '非时间序列表数据提取'}

}
