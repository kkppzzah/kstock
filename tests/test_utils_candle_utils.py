# -*- coding:utf-8 -*-
import time

import pandas as pd
import pytest

from kstock.common.consts import AggregateTimeType
from kstock.utils.candle_utils import (
    aggregate_candles_day_to_week, aggregate_candles_day_to_month,
    aggregate_candles_m5_to_m30, aggregate_candles_m5_to_h1, aggregate_candles_day_to_quarter,
    aggregate_candles_day_to_year
)
from .test_utils import (
    data_path as dp, load_tdx_exported_candles_day,
    aggregate_candles_day_to_week_hard, aggregate_candles_day_to_month_hard, aggregate_candles_m5_to_m30_hard,
    aggregate_candles_m5_to_h1_hard, aggregate_candles_day_to_quarter_hard, aggregate_candles_day_to_year_hard
)


candle_file_columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'amount']


@pytest.mark.parametrize(
    "day_candles, aggregate_time_type", [
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.FIRST_DATA_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.LAST_DATA_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.PERIOD_START_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.PERIOD_END_TIME
        ],
    ]
)
def test_aggregate_candles_day_to_week(day_candles: pd.DataFrame, aggregate_time_type: AggregateTimeType) -> None:
    """
    测试聚合日K线到周K线。
    :param day_candles: 日K线。
    :param aggregate_time_type: 时间聚合类型。
    :return:
    """
    result_candles: pd.DataFrame = aggregate_candles_day_to_week(day_candles, aggregate_time_type)
    candles: pd.DataFrame = aggregate_candles_day_to_week_hard(day_candles, aggregate_time_type)
    assert result_candles is not None and isinstance(result_candles, pd.DataFrame)
    assert result_candles.shape[0] == candles.shape[0]
    assert candles.equals(result_candles)


@pytest.mark.parametrize(
    "day_candles, aggregate_time_type", [
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.FIRST_DATA_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.LAST_DATA_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.PERIOD_START_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.PERIOD_END_TIME
        ],
    ]
)
def test_aggregate_candles_day_to_month(day_candles: pd.DataFrame, aggregate_time_type: AggregateTimeType) -> None:
    """
    测试聚合日K线到月K线。
    :param day_candles: 日K线。
    :param aggregate_time_type: 时间聚合类型。
    :return:
    """
    result_candles: pd.DataFrame = aggregate_candles_day_to_month(day_candles, aggregate_time_type)
    candles: pd.DataFrame = aggregate_candles_day_to_month_hard(day_candles, aggregate_time_type)
    assert result_candles is not None and isinstance(result_candles, pd.DataFrame)
    assert result_candles.shape[0] == candles.shape[0]
    assert candles.equals(result_candles)


@pytest.mark.parametrize(
    "day_candles, aggregate_time_type", [
        [
            load_tdx_exported_candles_day(dp('sz301389.lc5.tdx_exported_candles.txt'), names=candle_file_columns),
            AggregateTimeType.FIRST_DATA_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301389.lc5.tdx_exported_candles.txt'), names=candle_file_columns),
            AggregateTimeType.LAST_DATA_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301389.lc5.tdx_exported_candles.txt'), names=candle_file_columns),
            AggregateTimeType.PERIOD_START_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301389.lc5.tdx_exported_candles.txt'), names=candle_file_columns),
            AggregateTimeType.PERIOD_END_TIME
        ],
    ]
)
def test_aggregate_candles_m5_to_m30(day_candles: pd.DataFrame, aggregate_time_type: AggregateTimeType) -> None:
    """
    测试聚合日K线到月K线。
    :param day_candles: 日K线。
    :param aggregate_time_type: 时间聚合类型。
    :return:
    """
    result_candles: pd.DataFrame = aggregate_candles_m5_to_m30(day_candles, aggregate_time_type)
    candles: pd.DataFrame = aggregate_candles_m5_to_m30_hard(day_candles, aggregate_time_type)
    assert result_candles is not None and isinstance(result_candles, pd.DataFrame)
    assert result_candles.shape[0] == candles.shape[0]
    keys = ['time', 'open', 'high', 'low', 'close', 'volume']
    assert candles[keys].equals(result_candles[keys])


@pytest.mark.parametrize(
    "day_candles, aggregate_time_type", [
        [
            load_tdx_exported_candles_day(dp('sz301389.lc5.tdx_exported_candles.txt'), names=candle_file_columns),
            AggregateTimeType.FIRST_DATA_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301389.lc5.tdx_exported_candles.txt'), names=candle_file_columns),
            AggregateTimeType.LAST_DATA_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301389.lc5.tdx_exported_candles.txt'), names=candle_file_columns),
            AggregateTimeType.PERIOD_START_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301389.lc5.tdx_exported_candles.txt'), names=candle_file_columns),
            AggregateTimeType.PERIOD_END_TIME
        ],
    ]
)
def test_aggregate_candles_m5_to_h1(day_candles: pd.DataFrame, aggregate_time_type: AggregateTimeType) -> None:
    """
    测试聚合日K线到月K线。
    :param day_candles: 日K线。
    :param aggregate_time_type: 时间聚合类型。
    :return:
    """
    result_candles: pd.DataFrame = aggregate_candles_m5_to_h1(day_candles, aggregate_time_type)
    candles: pd.DataFrame = aggregate_candles_m5_to_h1_hard(day_candles, aggregate_time_type)
    assert result_candles is not None and isinstance(result_candles, pd.DataFrame)
    assert result_candles.shape[0] == candles.shape[0]
    keys = ['time', 'open', 'high', 'low', 'close', 'volume']
    assert candles[keys].equals(result_candles[keys])


@pytest.mark.parametrize(
    "day_candles, aggregate_time_type", [
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.FIRST_DATA_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.LAST_DATA_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.PERIOD_START_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.PERIOD_END_TIME
        ],
    ]
)
def test_aggregate_candles_day_to_quarter(day_candles: pd.DataFrame, aggregate_time_type: AggregateTimeType) -> None:
    """
    测试聚合日K线到月K线。
    :param day_candles: 日K线。
    :param aggregate_time_type: 时间聚合类型。
    :return:
    """
    result_candles: pd.DataFrame = aggregate_candles_day_to_quarter(day_candles, aggregate_time_type)
    candles: pd.DataFrame = aggregate_candles_day_to_quarter_hard(day_candles, aggregate_time_type)
    assert result_candles is not None and isinstance(result_candles, pd.DataFrame)
    assert result_candles.shape[0] == candles.shape[0]
    assert candles.equals(result_candles)


@pytest.mark.parametrize(
    "day_candles, aggregate_time_type", [
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.FIRST_DATA_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.LAST_DATA_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.PERIOD_START_TIME
        ],
        [
            load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.01.txt'), names=candle_file_columns),
            AggregateTimeType.PERIOD_END_TIME
        ],
    ]
)
def test_aggregate_candles_day_to_year(day_candles: pd.DataFrame, aggregate_time_type: AggregateTimeType) -> None:
    """
    测试聚合日K线到月K线。
    :param day_candles: 日K线。
    :param aggregate_time_type: 时间聚合类型。
    :return:
    """
    result_candles: pd.DataFrame = aggregate_candles_day_to_year(day_candles, aggregate_time_type)
    candles: pd.DataFrame = aggregate_candles_day_to_year_hard(day_candles, aggregate_time_type)
    assert result_candles is not None and isinstance(result_candles, pd.DataFrame)
    assert result_candles.shape[0] == candles.shape[0]
    assert candles.equals(result_candles)
