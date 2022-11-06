# -*- coding:utf-8 -*-
import pytest
import pandas as pd

from kstock.tdx.candle_loader import load_candle_day, load_candle_minute
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
