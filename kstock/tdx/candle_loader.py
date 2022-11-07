# -*- coding:utf-8 -*-
import datetime
import os
from typing import IO

import pandas as pd
import numpy as np

from kstock.tdx import consts


def load_candle_day(candle_file_path: str, offset: int = 0, candle_file: IO = None) -> pd.DataFrame:
    """
    读取通达信日K线。
    :param candle_file:
    :param offset:
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
    data = np.fromfile(candle_file_path if candle_file is None else candle_file, dtype=dt, offset=offset)
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


def load_candle_minute(candle_file_path: str, offset: int = 0, candle_file: IO = None) -> pd.DataFrame:
    """
    读取通信分钟级K线。
    :param candle_file:
    :param offset:
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
    data = np.fromfile(candle_file_path if candle_file is None else candle_file, dtype=dt)
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


def get_candle_count(candle_file_path: str) -> int:
    """

    :param candle_file_path:
    :return:
    """
    stat = os.stat(candle_file_path)
    return int(stat.st_size / consts.CANDLE_ITEM_LEN)


def load_candle_day_latest(
        candle_file_path: str, count: int = None, time_after: datetime.datetime = None,
        load_candles_count_hint: int = 16
) -> pd.DataFrame:
    """
    读取最新的日K线。
    :param load_candles_count_hint:
    :param candle_file_path:
    :param count:
    :param time_after:
    :return:
    """
    if not count and not time_after:
        return load_candle_day(candle_file_path)
    candle_count = get_candle_count(candle_file_path)
    if count:
        return load_candle_day(
            candle_file_path,
            offset=(candle_count - min(candle_count, count)) * consts.CANDLE_ITEM_LEN
        )
    if time_after:
        with open(candle_file_path, 'br') as candle_file:
            candles: pd.DataFrame = load_candle_day(
                None,
                offset=(candle_count - min(candle_count, load_candles_count_hint)) * consts.CANDLE_ITEM_LEN,
                candle_file=candle_file
            )
            if candles.index.min() > time_after:
                candles = load_candle_day(None, candle_file=candle_file)
            return candles.loc[candles.index > time_after]


def load_candle_minute_latest(
        candle_file_path: str, count: int = None, time_after: datetime.datetime = None,
        load_candles_count_hint: int = 240
) -> pd.DataFrame:
    """
    读取最新的分钟级K线。
    :param load_candles_count_hint:
    :param count:
    :param time_after:
    :param candle_file_path:
    :return:
    """
    if not count and not time_after:
        return load_candle_day(candle_file_path)
    candle_count = get_candle_count(candle_file_path)
    if count:
        return load_candle_minute_latest(
            candle_file_path,
            offset=(candle_count - min(candle_count, count)) * consts.CANDLE_ITEM_LEN
        )
    if time_after:
        with open(candle_file_path, 'br') as candle_file:
            candles: pd.DataFrame = load_candle_minute_latest(
                None,
                offset=(candle_count - min(candle_count, load_candles_count_hint)) * consts.CANDLE_ITEM_LEN,
                candle_file=candle_file
            )
            if candles.index.min() > time_after:
                candles = load_candle_minute_latest(None, candle_file=candle_file)
            return candles.loc[candles.index > time_after]
