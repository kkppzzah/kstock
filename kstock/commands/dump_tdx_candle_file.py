# -*- coding:utf-8 -*-
import argparse

import pandas as pd

from kstock.tdx import utils, candle_loader, consts


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--vipdoc-root', action='store', help='K线文件根目录', default=None)
    parser.add_argument('-f', '--candle-file-path', action='store', help='K线文件路径', default=None)
    parser.add_argument('-p', '--candle-period-type', action='store', help='K线周期类型', default=None)
    parser.add_argument('-c', '--code', action='store', help='股票代码', default=None)
    args = parser.parse_args()
    return args


def parse_candle_file_path(vipdoc_root: str, candle_file_path: str, candle_period_type: str, code: str) -> str:
    if candle_file_path:
        return candle_file_path
    if not candle_period_type or not code:
        raise Exception('--candle-period-type and --code are required')
    return utils.stock_candle_file_path(code, candle_period_type, vipdoc_root_path=utils.vipdoc_root(vipdoc_root))


def load_candle_file(candle_period_type: str, candle_file_path: str) -> pd.DataFrame:
    if candle_period_type == consts.CANDLE_PERIOD_TYPE_D:
        return candle_loader.load_candle_day(candle_file_path)
    return candle_loader.load_candle_minute(candle_file_path)


def dump_candles(candles: pd.DataFrame) -> None:
    print(candles.to_string(index=False, columns=['time', 'open', 'high', 'low', 'close', 'volume']))


def main() -> None:
    args = parse_arguments()
    candle_file_path = parse_candle_file_path(
        args.vipdoc_root, args.candle_file_path, args.candle_period_type, args.code
    )
    candles = load_candle_file(args.candle_period_type, candle_file_path)
    dump_candles(candles)


if __name__ == '__main__':
    main()
