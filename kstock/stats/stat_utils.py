# -*- coding:utf-8 -*-
import sys
from typing import Tuple

import numba
import numpy as np


def calculate_nd_h_l(data_list: np.ndarray) -> Tuple:
    """
    计算价格N日新高/低。
    返回结果中，
        n_h[i]表示data_list[i]是data_list[i - n_h[i]: i + 1]这个范围内最大值；
        n_l[i]表示data_list[i]是data_list[i - n_l[i]: i + 1]这个范围内最小值。
    :param data_list:
    :return:
    """
    data_list_len = data_list.shape[0]
    n_h_checked_idx = np.full((data_list_len,), -1, dtype=np.dtype('i8'))
    n_l_checked_idx = np.full((data_list_len,), -1, dtype=np.dtype('i8'))
    n_h, n_l = np.full(data_list_len, 1, dtype=np.dtype('i8')), np.full(data_list_len, 1, dtype=np.dtype('i8'))
    cur_data, last_data = None, None

    for idx in range(data_list_len):
        cur_data = data_list[idx]
        if idx < 1:
            last_data, n_h_checked_idx[0], n_l_checked_idx[0] = cur_data, 0, 0
            continue
        if cur_data > last_data:
            tmp_idx = idx - 1
            while tmp_idx >= 0:
                if data_list[tmp_idx] > cur_data:
                    break
                if n_h_checked_idx[tmp_idx] >= 0:
                    n_h_checked_idx[idx] = n_h_checked_idx[tmp_idx]
                    n_h[idx] = n_h[idx] + n_h[tmp_idx]
                    tmp_idx = n_h_checked_idx[tmp_idx] - 1
                else:
                    n_h_checked_idx[idx] = tmp_idx
                    n_h[idx] = n_h[idx] + 1
                    tmp_idx = tmp_idx - 1
        elif cur_data < last_data:
            n_h_checked_idx[idx] = idx
            tmp_idx = idx - 1
            while tmp_idx >= 0:
                if data_list[tmp_idx] < cur_data:
                    break
                if n_l_checked_idx[tmp_idx] >= 0:
                    n_l_checked_idx[idx] = n_l_checked_idx[tmp_idx]
                    n_l[idx] = n_l[idx] + n_l[tmp_idx]
                    tmp_idx = n_l_checked_idx[tmp_idx] - 1
                else:
                    n_l_checked_idx[idx] = tmp_idx
                    n_l[idx] = n_l[idx] + 1
                    tmp_idx = tmp_idx - 1
        else:
            # 如果相等的话，按照之前的变化趋势进行处理。
            if n_h[idx - 1] > 1:
                n_h[idx] = n_h[idx - 1] + 1
            if n_l[idx - 1] > 1:
                n_l[idx] = n_l[idx - 1] + 1
        last_data = cur_data
    n_h[n_h == 1], n_l[n_l == 1] = 0, 0
    return n_h, n_l


if 'pytest' not in sys.modules:
    calculate_nd_h_l = numba.jit(calculate_nd_h_l, nopython=True, cache=True)
