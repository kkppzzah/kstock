# -*- coding:utf-8 -*-
import datetime

import pandas as pd


def get_week_first_day(day: datetime.datetime) -> datetime.datetime:
    """
    获取日期对应周的第一天。
    :param day:
    :return:
    """
    return day - datetime.timedelta(days=day.weekday())


def get_week_last_day(day: datetime.datetime) -> datetime.datetime:
    """
    获取日期对应周的第一天。
    :param day:
    :return:
    """
    return day + datetime.timedelta(days=7 - 1 - day.weekday())


def get_month_first_day(day: datetime.datetime) -> datetime.datetime:
    """
    获取日期对应月的第一天。
    :param day:
    :return:
    """
    return datetime.datetime(day.year, day.month, 1)


def get_month_last_day(day: datetime.datetime) -> datetime.datetime:
    """
    获取日期对应月的第一天。
    :param day:
    :return:
    """
    if day.month < 12:
        return datetime.datetime(day.year, day.month + 1, 1) - datetime.timedelta(days=1)
    else:
        return datetime.datetime(day.year, 12, 31)


def get_m30_first_m5(time: datetime.datetime) -> datetime.datetime:
    """
    获取30分钟K线对应的第一个5分钟K线时间。
    :param time:
    :return:
    """
    if time.minute == 0:
        return datetime.datetime(time.year, time.month, time.day, hour=time.hour, minute=35) - \
               datetime.timedelta(hours=1)
    else:
        return datetime.datetime(time.year, time.month, time.day, hour=time.hour, minute=5 if time.minute < 35 else 35)


def get_m30_last_m5(time: datetime.datetime) -> datetime.datetime:
    """
    获取30分钟K线对应的最后一个5分钟K线时间。
    :param time:
    :return:
    """
    if time.minute > 30:
        return datetime.datetime(time.year, time.month, time.day, hour=time.hour) + datetime.timedelta(hours=1)
    else:
        return datetime.datetime(time.year, time.month, time.day, hour=time.hour, minute=30)
