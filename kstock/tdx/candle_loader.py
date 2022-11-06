# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np


def load_candle_day(candle_file_path: str) -> pd.DataFrame:
    """
    读取通达信日K线。
    :param candle_file_path:
    :return:
    """
    dt = np.dtype([
        ('time', np.uint32),
        ('open', np.uint32),
        ('high', np.uint32),
        ('low', np.uint32),
        ('close', np.uint32),
        ('amount', np.float32),
        ('volume', np.uint32),
        ('reserved', np.uint32),
    ])
    data = np.fromfile(candle_file_path, dtype=dt)
    dt = np.dtype([
        ('time', np.uint32),
        ('open', np.float64),
        ('high', np.float64),
        ('low', np.float64),
        ('close', np.float64),
        ('amount', np.float64),
        ('volume', np.int64),
        ('reserved', np.uint32),
    ])
    candles = pd.DataFrame(data.astype(dt))
    candles['time'] = pd.to_datetime(
        dict(
            year=candles['time'].div(10000).round(0).astype(np.int32),
            month=candles['time'].mod(10000).div(100).round(0).astype(np.int32),
            day=candles['time'].mod(100)
        )
    )
    candles['open'], candles['high'], = candles['open'] / 100, candles['high'] / 100
    candles['low'], candles['close'] = candles['low'] / 100, candles['close'] / 100
    candles.set_index('time', drop=False, inplace=True)
    candles.drop(columns=['reserved'], inplace=True)
    return candles


def load_candle_minute(candle_file_path: str) -> pd.DataFrame:
    """
    读取通信分钟级K线。
    :param candle_file_path:
    :return:
    """
    dt = np.dtype([
        ('day', np.uint16),
        ('minute', np.uint16),
        ('open', np.float32),
        ('high', np.float32),
        ('low', np.float32),
        ('close', np.float32),
        ('amount', np.float32),
        ('volume', np.uint32),
        ('reserved', np.uint32),
    ])
    data = np.fromfile(candle_file_path, dtype=dt)
    dt = np.dtype([
        ('day', np.uint32),
        ('minute', np.uint16),
        ('open', np.float64),
        ('high', np.float64),
        ('low', np.float64),
        ('close', np.float64),
        ('amount', np.float64),
        ('volume', np.int64),
        ('reserved', np.uint32),
    ])
    candles = pd.DataFrame(data.astype(dt))
    candles['time'] = pd.to_datetime(
        dict(
            year=(candles['day'] / 2048 + 2004).astype('uint32'),
            month=(candles['day'] % 2048 / 100).astype('uint32'),
            day=(candles['day'] % 2048 % 100).astype('uint32'),
            hour=(candles['minute'] / 60).astype('uint32'),
            minute=(candles['minute'] % 60).astype('uint32')
        )
    )
    candles.drop(columns=['day', 'minute', 'reserved'], inplace=True)
    candles.set_index('time', drop=False, inplace=True)
    return candles.round(2)
