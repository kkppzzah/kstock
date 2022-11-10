# -*- coding:utf-8 -*-
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
