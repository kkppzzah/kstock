import datetime
import os
import shutil
import struct
from typing import List

from kstock.tdx.utils import is_stock_market_sh


class UserCustomBlockCatalog:
    def __init__(self, block_catalog_file: str):
        self._block_catalog_file = block_catalog_file
        self._blocks = {}

    @property
    def blocks(self):
        return self._blocks

    def load(self) -> None:
        """
        读取模块数据。
        :return:
        """
        if not os.path.exists(self._block_catalog_file):
            return
        with open(self._block_catalog_file, 'br') as f:
            data = f.read()
            self._blocks = dict([
                (r[0].decode('gbk').strip('\x00'), r[1].decode('gbk').strip('\x00'))
                for r in struct.iter_unpack('50s70s', data)
            ])

    def add_block(self, block_name: str, block_abbr: str) -> None:
        self.load()
        # 如果需要则写板块列表文件。
        if block_name not in self._blocks:
            if os.path.exists(self._block_catalog_file):
                # 备份。
                now = datetime.datetime.now()
                shutil.copy(
                    self._block_catalog_file, '%s.%s' % (self._block_catalog_file, now.strftime('%Y%m%d%H%M%S'))
                )
            # 写入板块名称及相应文件名。
            with open(self._block_catalog_file, 'ab') as f:
                f.write(struct.pack('50s70s', block_name.encode('gbk'), block_abbr.encode('gbk')))


class UserCustomBlock:
    def __init__(self, block_file_path):
        self._block_file_path = block_file_path
        self._codes = []

    @property
    def codes(self):
        return self._codes

    def load(self) -> None:
        if not os.path.exists(self._block_file_path):
            self._codes = []
            return
        with open(self._block_file_path, 'r') as f:
            self._codes = [code[1:].strip() for code in f.readlines()]

    def add_stocks(self, code_list: List[str], overwrite: bool = True) -> None:
        """
        写入股票代码到特定的板块。
        :param overwrite:
        :param code_list:
        :return:
        """
        self.load()
        code_list = [code for code in code_list if code not in self._codes]
        if not code_list:
            return
        # 写入股票代码列表到特定的板块文件中。
        with open(self._block_file_path, 'a') as f:
            if overwrite:
                f.truncate(0)
            for code in code_list:
                f.write('%s%s\n' % ('1' if is_stock_market_sh(code) else '0', code))
