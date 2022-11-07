# -*- coding:utf-8 -*-
import datetime

import pytest
import pandas as pd

from kstock.tdx.candle_loader import (
    load_candle_day, load_candle_minute, load_candle_day_latest, load_candle_minute_latest
)
from .test_utils import (
    load_tdx_exported_candles_day, data_path as dp, load_tdx_exported_candles_minute
)


@pytest.mark.parametrize(
    "candle_file_path, tdx_exported_candles", [
        [dp('sz301380.day'), load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.txt'))]
    ]
)
def test_load_candle_day(candle_file_path: str, tdx_exported_candles: pd.DataFrame) -> None:
    """
    测试日线加载。
    :param candle_file_path: 通达信日线文件路径。
    :param tdx_exported_candles: 从通达信导出的日线文件路径。
    :return:
    """
    candles: pd.DataFrame = load_candle_day(candle_file_path)
    assert candles is not None and isinstance(candles, pd.DataFrame)
    assert tdx_exported_candles.shape[0] == candles.shape[0]
    assert tdx_exported_candles.equals(candles[['time', 'open', 'high', 'low', 'close', 'volume']])


@pytest.mark.parametrize(
    "candle_file_path, tdx_exported_candles", [
        [dp('sz301389.lc5'), load_tdx_exported_candles_minute(dp('sz301389.lc5.tdx_exported_candles.txt'))]
    ]
)
def test_load_candle_minute(candle_file_path: str, tdx_exported_candles: pd.DataFrame) -> None:
    """
    测试分钟级K线加载。
    :param candle_file_path: 通达信日线文件路径。
    :param tdx_exported_candles: 从通达信导出的日线文件路径。
    :return:
    """
    candles: pd.DataFrame = load_candle_minute(candle_file_path)
    assert candles is not None and isinstance(candles, pd.DataFrame)
    candles = candles[candles['time'] >= tdx_exported_candles.index[0]]
    assert tdx_exported_candles.shape[0] == candles.shape[0]
    assert tdx_exported_candles.equals(candles[['time', 'open', 'high', 'low', 'close', 'volume']])


@pytest.mark.parametrize(
    "candle_file_path, tdx_exported_candles, count, time_after", [
        [dp('sz301380.day'), load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.txt')), None, None],
        [dp('sz301380.day'), load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.txt')), 1, None],
        [
            dp('sz301380.day'), load_tdx_exported_candles_day(dp('sz301380.day.tdx_exported_candles.txt')), None,
            datetime.datetime(2022, 11, 2)
         ]
    ]
)
def test_load_candle_day_latest(
        candle_file_path: str, tdx_exported_candles: pd.DataFrame, count: int, time_after: datetime.datetime
) -> None:
    """
    测试日线加载。
    :param candle_file_path: 通达信日线文件路径。
    :param tdx_exported_candles: 从通达信导出的日线文件路径。
    :return:
    """
    index = tdx_exported_candles.index
    if count:
        tdx_exported_candles = tdx_exported_candles[index[index.shape[0] - count]:]
    elif time_after:
        tdx_exported_candles = tdx_exported_candles.loc[index[index > time_after]]
    candles: pd.DataFrame = load_candle_day_latest(candle_file_path, count=count, time_after=time_after)
    assert candles is not None and isinstance(candles, pd.DataFrame)
    assert tdx_exported_candles.shape[0] == candles.shape[0]
    assert tdx_exported_candles.equals(candles[['time', 'open', 'high', 'low', 'close', 'volume']])


@pytest.mark.parametrize(
    "candle_file_path, tdx_exported_candles, count, time_after", [
        [dp('sz301389.lc5'), load_tdx_exported_candles_minute(dp('sz301389.lc5.tdx_exported_candles.txt')), None, None],
        [dp('sz301389.lc5'), load_tdx_exported_candles_minute(dp('sz301389.lc5.tdx_exported_candles.txt')), 1, None],
        [
            dp('sz301389.lc5'), load_tdx_exported_candles_minute(dp('sz301389.lc5.tdx_exported_candles.txt')),
            None,
            datetime.datetime(2022, 11, 4, hour=14, minute=40)
        ],
    ]
)
def test_load_candle_minute(
        candle_file_path: str, tdx_exported_candles: pd.DataFrame, count: int, time_after: datetime.datetime
) -> None:
    """
    测试分钟级K线加载。
    :param candle_file_path: 通达信日线文件路径。
    :param tdx_exported_candles: 从通达信导出的日线文件路径。
    :return:
    """
    index = tdx_exported_candles.index
    if count:
        tdx_exported_candles = tdx_exported_candles[index[index.shape[0] - count]:]
    elif time_after:
        tdx_exported_candles = tdx_exported_candles.loc[index[index > time_after]]
    candles: pd.DataFrame = load_candle_minute(candle_file_path)
    assert candles is not None and isinstance(candles, pd.DataFrame)
    candles = candles[candles['time'] >= tdx_exported_candles.index[0]]
    assert tdx_exported_candles.shape[0] == candles.shape[0]
    assert tdx_exported_candles.equals(candles[['time', 'open', 'high', 'low', 'close', 'volume']])
