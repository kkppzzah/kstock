# -*- coding:utf-8 -*-
import datetime

import pandas as pd


def get_week_first_day(day: datetime.datetime):
    """
    获取日期对应周的第一天。
    :param day:
    :return:
    """
    return day - datetime.timedelta(days=day.weekday())


def get_week_last_day(day: datetime.datetime):
    """
    获取日期对应周的第一天。
    :param day:
    :return:
    """
    return day + datetime.timedelta(days=7 - 1 - day.weekday())
