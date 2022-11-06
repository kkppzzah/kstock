# -*- coding:utf-8 -*-
import datetime
import os.path
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd

from kstock.misc.trie_tree import Tag

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


def load_tdx_exported_candles_day(candle_file_path: str) -> pd.DataFrame:
    """
    加载从通达信导出的日线蜡烛图。数据格式如：
        2022/10/25,50.25,54.27,45.10,45.18
    各个字段表示：日期、开盘价、最高价、最低价、收盘价。
    :param candle_file_path: 蜡烛图文件路径。
    :return:
    """
    candles = pd.read_csv(
        candle_file_path, names=['time', 'open', 'high', 'low', 'close', 'volume', ],
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
