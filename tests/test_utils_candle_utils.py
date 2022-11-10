# -*- coding:utf-8 -*-
import pandas as pd
import pytest

from kstock.common.consts import AggregateTimeType
from kstock.utils.candle_utils import aggregate_candles_day_to_week, aggregate_candles_day_to_month
from .test_utils import (
    data_path as dp, load_tdx_exported_candles_day,
    aggregate_candles_day_to_week_hard, aggregate_candles_day_to_month_hard
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
