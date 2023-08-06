"""
# File       : param_generate.py
# Time       ：2021/7/30 3:15 下午
# Author     ：Yin Jian
# Description：参数校验
"""
import datetime
import sys

from datavita.core.exc.exception import ParamException


def str_list_param_check(param: object = '', param_len: int = 0):
    """
        将传入参数切分成列表,并进行去重和长度判断
    """
    if isinstance(param, str):
        param = param
    elif isinstance(param, list) and len(set(param)) <= param_len:
        param = ','.join(list(set(param)))
    else:
        ParamException(location_method='str_list_param_check', msg='入参类型不匹配', err_name='入参类型异常').logg_prod_str()
        sys.exit(1)
    return param


def get_now_day_num(end_day: int = 0):
    if isinstance(end_day, int) and end_day > 9999999:
        return end_day
    else:
        ParamException(location_method='str_list_param_check', msg='end_day 不符合规范,使用默认值',
                       err_name='入参类型异常').logg_prod_str()
        return datetime.date.today().strftime("%Y%m%d")


if __name__ == '__main__':
    print(datetime.date.today().strftime("%Y%m%d"))
