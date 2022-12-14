# -*- coding:utf-8 -*-
import datetime
import os.path
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd

from kstock.common.consts import AggregateTimeType
from kstock.misc.trie_tree import Tag
from kstock.utils import datetime_utils

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


def load_tdx_exported_candles_day(
        candle_file_path: str, names=['time', 'open', 'high', 'low', 'close', 'volume', ]
) -> pd.DataFrame:
    """
    加载从通达信导出的日线蜡烛图。数据格式如：
        2022/10/25,50.25,54.27,45.10,45.18
    各个字段表示：日期、开盘价、最高价、最低价、收盘价。
    :param names:
    :param candle_file_path: 蜡烛图文件路径。
    :return:
    """
    candles = pd.read_csv(
        candle_file_path, names=names,
        parse_dates=['time']
    )
    candles.set_index('time', drop=False, inplace=True)
    return candles


def load_tdx_exported_candles_minute(candle_file_path: str) -> pd.DataFrame:
    """
    加载从通达信导出的日线蜡烛图。数据格式如：
        2022/10/31-09:35,20.89,22.02,20.59,21.56,2830100
    各个字段表示：时间、开盘价、最高价、最低价、收盘价。
    :param candle_file_path: 蜡烛图文件路径。
    :return:
    """
    candles = pd.read_csv(
        candle_file_path, names=['time', 'open', 'high', 'low', 'close', 'volume', ],
        parse_dates=['time'], date_parser=lambda x: datetime.datetime.strptime(x, '%Y/%m/%d-%H:%M')
    )
    candles.set_index('time', drop=False, inplace=True)
    return candles


def data_path(filename: str) -> str:
    """
    获取测试文件路径。
    :param filename: 测试文件名，不包含路径。
    :return:
    """
    return os.path.join(TEST_DATA_PATH, filename)


def cal_nd_h_l_hard(data_list: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """

    :param data_list:
    :return:
    """
    data_list_len = data_list.shape[0]
    n_h, n_l = np.full(data_list_len, 0, dtype=np.dtype('i8')), np.full(data_list_len, 0, dtype=np.dtype('i8'))
    for i in range(1, data_list_len):
        if i == 0:
            continue
        cal_nd_h, cal_nd_l = False, False
        if data_list[i] == data_list[i - 1]:
            cal_nd_h = n_h[i - 1] > 0
            cal_nd_l = n_l[i - 1] > 0
        elif data_list[i] > data_list[i - 1]:
            cal_nd_h = True
        else:
            cal_nd_l = True
        if cal_nd_h:
            for idx in range(i - 1, -1, -1):
                if data_list[idx] <= data_list[i]:
                    if idx == i - 1:
                        n_h[i] = 1
                    n_h[i] = n_h[i] + 1
                else:
                    break
        if cal_nd_l:
            for idx in range(i - 1, -1, -1):
                if data_list[idx] >= data_list[i]:
                    if idx == i - 1:
                        n_l[i] = 1
                    n_l[i] = n_l[i] + 1
                else:
                    break
    return n_h, n_l


def tag_hard(words: List[Dict], doc: str) -> List[Tag]:
    """

    :param words:
    :param doc:
    :return:
    """
    tags = []
    doc_len = len(doc)
    for word_info in words:
        word, meta = word_info['word'], word_info['meta']
        index = 0
        while index < doc_len:
            word_start_index = doc.find(word, index)
            if word_start_index == -1:
                break
            tags.append(Tag(word_start_index, word_start_index + len(word) - 1, meta))
            index = word_start_index + len(word)
    return sorted(tags, key=lambda x: x.start)


def aggregate_candles_day_to_week_hard(
    candles: pd.DataFrame, aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """

    :param candles:
    :param aggregate_time_type:
    :return:
    """
    result_candles = {}
    for i in range(candles.shape[0]):
        candle: pd.Series = candles.iloc[i]
        ts: pd.Timestamp = candle['time']
        week_first_day = datetime_utils.get_week_first_day(ts)
        result_candle = result_candles.get(week_first_day)
        if result_candle is None:
            result_candle = candle.copy()
            if aggregate_time_type == AggregateTimeType.PERIOD_START_TIME:
                result_candle['time'] = week_first_day
            elif aggregate_time_type == AggregateTimeType.PERIOD_END_TIME:
                result_candle['time'] = datetime_utils.get_week_last_day(ts)
            result_candles[week_first_day] = result_candle
            continue
        if aggregate_time_type == AggregateTimeType.LAST_DATA_TIME:
            result_candle['time'] = candle['time']
        result_candle['high'] = max(result_candle['high'], candle['high'])
        result_candle['low'] = min(result_candle['low'], candle['low'])
        result_candle['close'] = candle['close']
        result_candle['volume'] = result_candle['volume'] + candle['volume']
        result_candle['amount'] = result_candle['amount'] + candle['amount']
    result_candles = pd.DataFrame(sorted(result_candles.values(), key=lambda c: c['time']))
    return result_candles.set_index('time', drop=False)


def aggregate_candles_day_to_month_hard(
    candles: pd.DataFrame, aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """

    :param candles:
    :param aggregate_time_type:
    :return:
    """
    result_candles = {}
    for i in range(candles.shape[0]):
        candle: pd.Series = candles.iloc[i]
        ts: pd.Timestamp = candle['time']
        month_first_day = datetime_utils.get_month_first_day(ts)
        result_candle = result_candles.get(month_first_day)
        if result_candle is None:
            result_candle = candle.copy()
            if aggregate_time_type == AggregateTimeType.PERIOD_START_TIME:
                result_candle['time'] = month_first_day
            elif aggregate_time_type == AggregateTimeType.PERIOD_END_TIME:
                result_candle['time'] = datetime_utils.get_month_last_day(ts)
            result_candles[month_first_day] = result_candle
            continue
        if aggregate_time_type == AggregateTimeType.LAST_DATA_TIME:
            result_candle['time'] = candle['time']
        result_candle['high'] = max(result_candle['high'], candle['high'])
        result_candle['low'] = min(result_candle['low'], candle['low'])
        result_candle['close'] = candle['close']
        result_candle['volume'] = result_candle['volume'] + candle['volume']
        result_candle['amount'] = result_candle['amount'] + candle['amount']
    result_candles = pd.DataFrame(sorted(result_candles.values(), key=lambda c: c['time']))
    return result_candles.set_index('time', drop=False)


def aggregate_candles_m5_to_m30_hard(
    candles: pd.DataFrame, aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """

    :param candles:
    :param aggregate_time_type:
    :return:
    """
    result_candles = {}
    for i in range(candles.shape[0]):
        candle: pd.Series = candles.iloc[i]
        ts: pd.Timestamp = candle['time']
        m30_first_m5 = datetime_utils.get_m30_first_m5(ts)

        result_candle = result_candles.get(m30_first_m5)
        if result_candle is None:
            result_candle = candle.copy()
            if aggregate_time_type == AggregateTimeType.PERIOD_START_TIME:
                result_candle['time'] = m30_first_m5
            elif aggregate_time_type == AggregateTimeType.PERIOD_END_TIME:
                result_candle['time'] = datetime_utils.get_m30_last_m5(ts)
            result_candles[m30_first_m5] = result_candle
            continue
        if aggregate_time_type == AggregateTimeType.LAST_DATA_TIME:
            result_candle['time'] = candle['time']
        result_candle['high'] = max(result_candle['high'], candle['high'])
        result_candle['low'] = min(result_candle['low'], candle['low'])
        result_candle['close'] = candle['close']
        result_candle['volume'] = result_candle['volume'] + candle['volume']
        result_candle['amount'] = result_candle['amount'] + candle['amount']
    result_candles = pd.DataFrame(sorted(result_candles.values(), key=lambda c: c['time']))
    return result_candles.set_index('time', drop=False)


def aggregate_candles_m5_to_h1_hard(
    candles: pd.DataFrame, aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """

    :param candles:
    :param aggregate_time_type:
    :return:
    """
    result_candles = {}
    for i in range(candles.shape[0]):
        candle: pd.Series = candles.iloc[i]
        ts: pd.Timestamp = candle['time']
        h1_first_m5 = datetime_utils.get_h1_first_m5(ts)

        result_candle = result_candles.get(h1_first_m5)
        if result_candle is None:
            result_candle = candle.copy()
            if aggregate_time_type == AggregateTimeType.PERIOD_START_TIME:
                result_candle['time'] = h1_first_m5
            elif aggregate_time_type == AggregateTimeType.PERIOD_END_TIME:
                result_candle['time'] = datetime_utils.get_h1_last_m5(ts)
            result_candles[h1_first_m5] = result_candle
            continue
        if aggregate_time_type == AggregateTimeType.LAST_DATA_TIME:
            result_candle['time'] = candle['time']
        result_candle['high'] = max(result_candle['high'], candle['high'])
        result_candle['low'] = min(result_candle['low'], candle['low'])
        result_candle['close'] = candle['close']
        result_candle['volume'] = result_candle['volume'] + candle['volume']
        result_candle['amount'] = result_candle['amount'] + candle['amount']
    result_candles = pd.DataFrame(sorted(result_candles.values(), key=lambda c: c['time']))
    return result_candles.set_index('time', drop=False)


def aggregate_candles_day_to_quarter_hard(
    candles: pd.DataFrame, aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """

    :param candles:
    :param aggregate_time_type:
    :return:
    """
    result_candles = {}
    for i in range(candles.shape[0]):
        candle: pd.Series = candles.iloc[i]
        ts: pd.Timestamp = candle['time']
        quarter_first_day = datetime_utils.get_quarter_first_day(ts)
        result_candle = result_candles.get(quarter_first_day)
        if result_candle is None:
            result_candle = candle.copy()
            if aggregate_time_type == AggregateTimeType.PERIOD_START_TIME:
                result_candle['time'] = quarter_first_day
            elif aggregate_time_type == AggregateTimeType.PERIOD_END_TIME:
                result_candle['time'] = datetime_utils.get_quarter_last_day(ts)
            result_candles[quarter_first_day] = result_candle
            continue
        if aggregate_time_type == AggregateTimeType.LAST_DATA_TIME:
            result_candle['time'] = candle['time']
        result_candle['high'] = max(result_candle['high'], candle['high'])
        result_candle['low'] = min(result_candle['low'], candle['low'])
        result_candle['close'] = candle['close']
        result_candle['volume'] = result_candle['volume'] + candle['volume']
        result_candle['amount'] = result_candle['amount'] + candle['amount']
    result_candles = pd.DataFrame(sorted(result_candles.values(), key=lambda c: c['time']))
    return result_candles.set_index('time', drop=False)


def aggregate_candles_day_to_year_hard(
    candles: pd.DataFrame, aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """

    :param candles:
    :param aggregate_time_type:
    :return:
    """
    result_candles = {}
    for i in range(candles.shape[0]):
        candle: pd.Series = candles.iloc[i]
        ts: pd.Timestamp = candle['time']
        year_first_day = datetime_utils.get_year_first_day(ts)
        result_candle = result_candles.get(year_first_day)
        if result_candle is None:
            result_candle = candle.copy()
            if aggregate_time_type == AggregateTimeType.PERIOD_START_TIME:
                result_candle['time'] = year_first_day
            elif aggregate_time_type == AggregateTimeType.PERIOD_END_TIME:
                result_candle['time'] = datetime_utils.get_year_last_day(ts)
            result_candles[year_first_day] = result_candle
            continue
        if aggregate_time_type == AggregateTimeType.LAST_DATA_TIME:
            result_candle['time'] = candle['time']
        result_candle['high'] = max(result_candle['high'], candle['high'])
        result_candle['low'] = min(result_candle['low'], candle['low'])
        result_candle['close'] = candle['close']
        result_candle['volume'] = result_candle['volume'] + candle['volume']
        result_candle['amount'] = result_candle['amount'] + candle['amount']
    result_candles = pd.DataFrame(sorted(result_candles.values(), key=lambda c: c['time']))
    return result_candles.set_index('time', drop=False)


def aggregate_candles_n_hard(
    candles: pd.DataFrame, group_size: int,
    aggregate_time_type: AggregateTimeType = AggregateTimeType.PERIOD_START_TIME
) -> pd.DataFrame:
    """

    :param candles:
    :param group_size:
    :param aggregate_time_type:
    :return:
    """
    candles = candles.reset_index(inplace=False, drop=True)
    candles_count = candles.shape[0]
    results = [
        candles.iloc[index: index + group_size].agg({
        'time': lambda x: x.iloc[0] if aggregate_time_type == AggregateTimeType.FIRST_DATA_TIME
                    else x.iloc[x.shape[0] - 1],
        'open': lambda x: x.iloc[0],
        'high': 'max',
        'low': 'min',
        'close': lambda x: x.iloc[x.shape[0] - 1],
        'volume': 'sum',
        'amount': 'sum'
    })
        for index in range(0, candles_count, group_size)
    ]
    return pd.DataFrame(results).set_index('time', drop=False)
