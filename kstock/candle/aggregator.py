# -*- coding:utf-8 -*-
import datetime
import itertools
import sys
from typing import Dict, Tuple

import numba
import numpy as np
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

day_to_quarter_time_func_map = {
    AggregateTimeType.FIRST_DATA_TIME: 'first',
    AggregateTimeType.LAST_DATA_TIME: 'last',
    AggregateTimeType.PERIOD_START_TIME: lambda s: datetime_utils.get_quarter_first_day(s.iloc[0]),
    AggregateTimeType.PERIOD_END_TIME: lambda s: datetime_utils.get_quarter_last_day(s.iloc[0])
}


day_to_year_time_func_map = {
    AggregateTimeType.FIRST_DATA_TIME: 'first',
    AggregateTimeType.LAST_DATA_TIME: 'last',
    AggregateTimeType.PERIOD_START_TIME: lambda s: datetime_utils.get_year_first_day(s.iloc[0]),
    AggregateTimeType.PERIOD_END_TIME: lambda s: datetime_utils.get_year_last_day(s.iloc[0])
}


AGGREGATE_TIME_TYPE_FIRST_DATA_TIME = 0
AGGREGATE_TIME_TYPE_LAST_DATA_TIME = 1


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


def aggregate_candles_day_to_quarter(
        candles: pd.DataFrame, aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """
    聚合日K线到季K线。
    :param candles:
    :param aggregate_time_type:
    :return:
    """
    return aggregate_candles_day(candles, 'Q', day_to_quarter_time_func_map, aggregate_time_type=aggregate_time_type)


def aggregate_candles_day_to_year(
        candles: pd.DataFrame, aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """
    聚合日K线到年K线。
    :param candles:
    :param aggregate_time_type:
    :return:
    """
    return aggregate_candles_day(candles, 'Y', day_to_year_time_func_map, aggregate_time_type=aggregate_time_type)


@numba.jit(nopython=True, cache=True)
def _aggregate_candles_n(
        open_list: np.ndarray, high_list: np.ndarray, low_list: np.ndarray, close_list: np.ndarray,
        volume_list: np.ndarray, amount_list: np.ndarray,
        group_size: int, aggregate_time_type: int
) -> Tuple:
    """

    :param open_list:
    :param high_list:
    :param low_list:
    :param close_list:
    :param volume_list:
    :param amount_list:
    :param group_size:
    :param aggregate_time_type:
    :return:
    """
    data_len = open_list.shape[0]
    result_len = int((data_len + group_size - 1)/group_size)
    result_open: np.ndarray = np.zeros(result_len, dtype=np.dtype('f8'))
    result_high: np.ndarray = np.zeros(result_len, dtype=np.dtype('f8'))
    result_low: np.ndarray = np.zeros(result_len, dtype=np.dtype('f8'))
    result_close: np.ndarray = np.zeros(result_len, dtype=np.dtype('f8'))
    result_volume: np.ndarray = np.zeros(result_len, dtype=np.dtype('i8'))
    result_amount: np.ndarray = np.zeros(result_len, dtype=np.dtype('f8'))
    result_time_index: np.ndarray = np.zeros(result_len, dtype=np.dtype('i4'))
    result_index = 0
    current_batch_index = 0
    for i in range(data_len):
        if current_batch_index == 0 or current_batch_index == group_size:
            if current_batch_index == group_size:
                result_index += 1
            current_batch_index = 0
            result_open[result_index] = open_list[i]
            result_high[result_index] = high_list[i]
            result_low[result_index] = low_list[i]
            result_close[result_index] = close_list[i]
            result_volume[result_index] = volume_list[i]
            result_amount[result_index] = amount_list[i]
            result_time_index[result_index] = i
        if current_batch_index > 0:
            result_high[result_index] = max(result_high[result_index], high_list[i])
            result_low[result_index] = min(result_low[result_index], low_list[i])
            result_close[result_index] = close_list[i]
            result_volume[result_index] += volume_list[i]
            result_amount[result_index] += amount_list[i]
            if aggregate_time_type == AGGREGATE_TIME_TYPE_LAST_DATA_TIME:
                result_time_index[result_index] = i
        current_batch_index += 1
    return (
        'open', result_open, 'high', result_high, 'low', result_low, 'close', result_close,
        'volume', result_volume, 'amount', result_amount, 'time_index', result_time_index
    )


if 'pytest' not in sys.modules:
    _aggregate_candles_n = numba.jit(_aggregate_candles_n, nopython=True, cache=True)


def aggregate_candles_n(
        candles: pd.DataFrame, group_size: int,
        aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """
    聚合K线到任意周期，如聚合日K线到10日线。
    :param candles:
    :param group_size: 多少个K线聚合一次。
    :param aggregate_time_type:
    :return:
    """
    candles = candles.reset_index(inplace=False, drop=True)
    result = _aggregate_candles_n(
        candles['open'].to_numpy(), candles['high'].to_numpy(), candles['low'].to_numpy(), candles['close'].to_numpy(),
        candles['volume'].to_numpy(), candles['amount'].to_numpy(),
        group_size,
        (AGGREGATE_TIME_TYPE_FIRST_DATA_TIME if aggregate_time_type == AggregateTimeType.FIRST_DATA_TIME else
            AGGREGATE_TIME_TYPE_LAST_DATA_TIME)
    )
    result_candles = pd.DataFrame(dict([
        (k, v) for k, v in zip(result[0::2], result[1::2])
    ]))
    result_candles['time'] = candles['time'].iloc[result_candles['time_index']].reset_index(inplace=False, drop=True)
    result_candles.set_index('time', inplace=True, drop=False)
    result_candles.drop(columns='time_index', inplace=True)
    return result_candles.reindex(['time', 'open', 'high', 'low', 'close', 'volume', 'amount'], axis=1)
