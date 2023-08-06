#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-01-29 16:16
    @Author : Yin Jian
    @Version：V 0.1
    @File : contants.py
    @desc : 常量类,保存常用信息
"""
from datavita import __version__

# 版本信息
DATA_VITA_VERSION = __version__

# 接口控制

# 最大重试次数
MAX_RETRIES = 3

# 接口超时时间
SESSION_PERIOD_TIMEOUT = 10

# 默认URL
BASE_URL = 'https://dpms.datavita.com.cn/api/sdk'
# BASE_URL = 'http://8.130.169.56:8199'
# BASE_URL = 'http://172.16.17.219:8199'
# BASE_URL = 'http://219.143.244.230:8082'
# BASE_URL = 'http://39.97.171.103:8099'

# 默认开始时间
# DEFAULT_START_DATE = "2015-01-01"

EXCEPTION_DICT = {
    500: "服务器出现错误",
    404: "未找到资源",
    20002: "账号不存在或密码错误",
    20003: "账号已被禁用",
    20004: "用户不存在",
    20031: "缺少Authorization",
    20032: "header头格式错误",
    20033: "access_key已经被禁用",
    20034: "access_key已经过期",
    20035: "签名错误",
    20036: "此接口当前分钟请求次数已达上限",
    20037: "此接口当日请求书已经达到上限",
    20038: "客户端请求时间过了有效期",
    10001: "系统繁忙",
    10002: "没有权限",
    10003: "非法访问",
    10004: "非法 IP ",
    10006: "标签代码不能为空",
    10007: "组ID不能为空",
    10008: "数据集ID和名称不能同时为空",
    10009: "windCode不能为空",
    10010: "windCode个数超出上限",
    10011: "dataCode不能为空",
    10012: "dataCode个数据超出上限",
    10013: "dataName不能为空",
    10014: "dataName个数超出上限"
}
