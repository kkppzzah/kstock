# -*- coding:utf-8 -*-
import datetime

import pandas as pd

from kstock.common.consts import AggregateTimeType
from kstock.utils import datetime_utils

day_to_week_time_func_map = {
    AggregateTimeType.FIRST_DATA_TIME: 'first',
    AggregateTimeType.LAST_DATA_TIME: 'last',
    AggregateTimeType.PERIOD_START_TIME: lambda s: datetime_utils.get_week_first_day(s.iloc[0]),
    AggregateTimeType.PERIOD_END_TIME: lambda s: datetime_utils.get_week_last_day(s.iloc[0])
}

day_to_month_time_func_map = {
    AggregateTimeType.FIRST_DATA_TIME: 'first',
    AggregateTimeType.LAST_DATA_TIME: 'last',
    AggregateTimeType.PERIOD_START_TIME: lambda s: datetime_utils.get_month_first_day(s.iloc[0]),
    AggregateTimeType.PERIOD_END_TIME: lambda s: datetime_utils.get_month_last_day(s.iloc[0])
}

m5_to_m30_time_func_map = {
    AggregateTimeType.FIRST_DATA_TIME: 'first',
    AggregateTimeType.LAST_DATA_TIME: 'last',
    AggregateTimeType.PERIOD_START_TIME: lambda s: datetime_utils.get_m30_first_m5(s.iloc[0]),
    AggregateTimeType.PERIOD_END_TIME: lambda s: datetime_utils.get_m30_last_m5(s.iloc[0])
}

m5_to_h1_time_func_map = {
    AggregateTimeType.FIRST_DATA_TIME: 'first',
    AggregateTimeType.LAST_DATA_TIME: 'last',
    AggregateTimeType.PERIOD_START_TIME: lambda s: datetime_utils.get_h1_first_m5(s.iloc[0]),
    AggregateTimeType.PERIOD_END_TIME: lambda s: datetime_utils.get_h1_last_m5(s.iloc[0])
}


def aggregate_candles_day(
        candles: pd.DataFrame,
        rule: str, time_func_map: dict,
        aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """

    :param candles:
    :param rule:
    :param time_func_map:
    :param aggregate_time_type:
    :return:
    """
    result_candles = candles.resample(rule, on='time').agg({
        'time': time_func_map[aggregate_time_type],
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'amount': 'sum',
    })
    return result_candles.set_index('time', drop=False)


def aggregate_candles_day_to_week(
        candles: pd.DataFrame, aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """
    聚合日K线到周K线。
    :param aggregate_time_type:
    :param candles:
    :return:
    """
    return aggregate_candles_day(candles, 'W', day_to_week_time_func_map, aggregate_time_type=aggregate_time_type)


def aggregate_candles_day_to_month(
        candles: pd.DataFrame, aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """
    聚合日K线到周K线。
    :param candles:
    :param aggregate_time_type:
    :return:
    """
    return aggregate_candles_day(candles, 'M', day_to_month_time_func_map, aggregate_time_type=aggregate_time_type)


def aggregate_candles_minute(
        candles: pd.DataFrame,
        time_func_map: dict,
        aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """

    :param candles:
    :param time_func_map:
    :param aggregate_time_type:
    :return:
    """
    result_candles = candles.groupby('key').agg({
        'time': time_func_map[aggregate_time_type],
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'amount': 'sum',
    })
    return result_candles.set_index('time', drop=False)


def aggregate_candles_m5_to_m30(
        candles: pd.DataFrame, aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """
    聚合5分钟K线到30分钟K线。
    :param candles:
    :param aggregate_time_type:
    :return:
    """
    candles = candles.reset_index(inplace=False, drop=True)
    temp = pd.DatetimeIndex(candles['time'] - datetime.timedelta(minutes=5)).dropna().to_series()
    candles['key'] = (temp - pd.TimedeltaIndex(temp.dt.minute % 30, unit='min')).reset_index(drop=True)
    return aggregate_candles_minute(candles, m5_to_m30_time_func_map, aggregate_time_type=aggregate_time_type)


def aggregate_candles_m5_to_h1(
        candles: pd.DataFrame, aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """
    聚合5分钟K线到1小时K线。
    :param candles:
    :param aggregate_time_type:
    :return:
    """
    candles = candles.reset_index(inplace=False, drop=True)
    temp = pd.DatetimeIndex(candles['time'] - datetime.timedelta(minutes=5)).dropna().to_series()
    temp[(temp.dt.hour == 10) & (temp.dt.minute < 30)] = temp - pd.Timedelta(1, unit='h')
    temp[temp.dt.hour == 11] = temp - pd.Timedelta(1, unit='h')
    temp = (temp - pd.TimedeltaIndex(temp.dt.minute, unit='min')).reset_index(drop=True)
    candles['key'] = temp
    return aggregate_candles_minute(candles, m5_to_h1_time_func_map, aggregate_time_type=aggregate_time_type)
