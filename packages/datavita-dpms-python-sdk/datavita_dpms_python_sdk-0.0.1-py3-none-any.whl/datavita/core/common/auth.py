#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2022-02-02 15:20
    @Author : Yin Jian
    @Version：V 0.1
    @File : auth.py
    @desc :
"""
import base64
import hashlib
import hmac

# from Crypto.Cipher import AES


class Auth:
    """格式化传入参数后进行的 hmac_sha1

     :param access_id:
     :param access_secret:
     """

    def __init__(self, access_id: str, access_secret: str):
        self.access_id = access_id
        self.access_secret = access_secret

    def make_authorization(self, data) -> str:
        """
            生成sign字符串
        """
        hmac_code = hmac.new(self.access_secret.encode(), data.encode(), hashlib.sha1).digest()
        vr = base64.b64encode(hmac_code).decode()
        return vr
