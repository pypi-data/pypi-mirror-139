#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2022-01-31 1:43
    @Author : Yin Jian
    @Version：V 0.1
    @File : exception.py
    @desc : 统一异常
"""

from datavita.core.utils import log


class DVException(Exception):
    def __init__(self, err_name: str = "基础异常", location_method: str = '', msg: str = "华创证券统一异常处理"):
        self.err_name = err_name
        self.location_method = location_method
        self.msg = msg

    def logg_dev_str(self):
        err_log = "[{err_name}] \n[{location_method}] " \
                  "\n{msg}".format(location_method=self.location_method, err_name=self.err_name, msg=self.msg)
        return log.default_logger.error(msg=err_log)

    def logg_prod_str(self):
        err_log = "[{err_name}] \n[{location_method}] " \
                  "\n{msg}".format(location_method=self.location_method, err_name=self.err_name, msg=self.msg)
        return log.default_logger.error(msg=err_log)


class ResponseException(DVException):
    """
        Response 异常
    """

    def __init__(self, err_name: str = "Response 异常", location_method: str = '', url: str = '', msg: str = ""):
        self.err_name = err_name
        self.location_method = location_method
        self.url = url
        self.msg = msg

    def logg_dev_str(self):
        err_log = "[{err_name}] {location_method} \n" \
                  "url : {url} \n" \
                  "{msg}".format(err_name=self.err_name, location_method=self.location_method, url=self.url,
                                 msg=self.msg)
        return log.default_logger.error(msg=err_log)

    def logg_prod_str(self):
        err_log = "[{err_name}] {msg}".format(err_name=self.err_name, msg=self.msg)
        return log.default_logger.error(msg=err_log)


class ConvertException(DVException):
    """
        转换异常
    """

    def __init__(self, err_name: str = "数据转换异常", location_method: str = '', msg: str = ""):
        self.err_name = err_name
        self.location_method = location_method
        self.msg = msg


class ParamException(DVException):
    """
        参数异常
    """

    def __init__(self, err_name: str = "方法参数异常", location_method: str = '', msg: str = ""):
        self.err_name = err_name
        self.location_method = location_method
        self.msg = msg
