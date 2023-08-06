# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 17:38
    @Author : Yin Jian
    @Version：V 0.1
    @File : baseschema.py
    @desc :
"""

from datavita.core.utils import log


class BaseSchema:
    """
        统一格式规范
    """

    def __init__(
            self,
            msg: str = '无消息'
    ):
        self.logger = log.default_logger
        self.msg = msg

