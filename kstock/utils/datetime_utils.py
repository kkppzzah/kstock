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


def get_h1_first_m5(time: datetime.datetime) -> datetime.datetime:
    """
    获取1小时K线对应的第一个5分钟K线时间。
    :param time:
    :return:
    """
    if time.hour == 9 or (time.hour == 10 and time.minute < 35):
        return datetime.datetime(time.year, time.month, time.day, hour=9, minute=35)
    elif time.hour == 10 or time.hour == 11:
        return datetime.datetime(time.year, time.month, time.day, hour=10, minute=35)
    elif time.hour == 13 or (time.hour == 14 and time.minute == 0):
        return datetime.datetime(time.year, time.month, time.day, hour=13, minute=5)
    else:
        return datetime.datetime(time.year, time.month, time.day, hour=14, minute=5)


def get_h1_last_m5(time: datetime.datetime) -> datetime.datetime:
    """
    获取1小时K线对应的最后一个5分钟K线时间。
    :param time:
    :return:
    """
    if time.hour == 9 or (time.hour == 10 and time.minute < 35):
        return datetime.datetime(time.year, time.month, time.day, hour=10, minute=30)
    elif time.hour == 10 or time.hour == 11:
        return datetime.datetime(time.year, time.month, time.day, hour=11, minute=30)
    elif time.hour == 13 or (time.hour == 14 and time.minute == 0):
        return datetime.datetime(time.year, time.month, time.day, hour=14, minute=0)
    else:
        return datetime.datetime(time.year, time.month, time.day, hour=15)


def get_quarter_first_day(day: datetime.datetime) -> datetime.datetime:
    """
    获取日期对应季的第一天。
    :param day:
    :return:
    """
    return datetime.datetime(day.year, (int((day.month - 1)/3) * 3) + 1, 1)


def get_quarter_last_day(day: datetime.datetime) -> datetime.datetime:
    """
    获取日期对应季的第一天。
    :param day:
    :return:
    """
    return datetime.datetime(day.year, int((day.month + 2) / 3) * 3, 31 if (day.month > 3 or day.month < 10) else 30)


def get_year_first_day(day: datetime.datetime) -> datetime.datetime:
    """
    获取日期对应年的第一天。
    :param day:
    :return:
    """
    return datetime.datetime(day.year, 1, 1)


def get_year_last_day(day: datetime.datetime) -> datetime.datetime:
    """
    获取日期对应年的第一天。
    :param day:
    :return:
    """
    return datetime.datetime(day.year, 12, 31)
