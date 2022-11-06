# -*- coding:utf-8 -*-
import numpy
import pytest
import numpy as np

from kstock.stats.stat_utils import calculate_nd_h_l
from .test_utils import cal_nd_h_l_hard


@pytest.mark.parametrize(
    "data_list", [
        np.array([
            134.80, 127.72, 121.77, 119.50, 106.48, 102.50, 97.50, 91.50, 90.85, 94.25,
            92.31, 95.25, 97.74, 94.88, 92.00, 97.88, 95.69, 100.66, 103.50, 103.00,
            104.70, 108.26, 109.63, 108.30, 105.32, 113.24, 112.14, 112.14
        ]),
    ]
)
def test_stats_stat_utils_calculate_nd_h_l(data_list: np.ndarray) -> None:
    test_nd_h, test_nd_l = cal_nd_h_l_hard(data_list)
    nd_h, nd_l = calculate_nd_h_l(data_list)
    assert numpy.array_equal(test_nd_h, nd_h)
    assert numpy.array_equal(test_nd_l, nd_l)
