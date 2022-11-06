# -*- coding:utf-8 -*-
import os
import shutil
from typing import Dict

import pytest

from kstock.tdx.block import UserCustomBlockCatalog, UserCustomBlock
from .test_utils import data_path


class TestUserCustomBlockCatalog:
    @pytest.mark.parametrize(
        "block_catalog_file, blocks", [
            [
                data_path('blocknew.cfg'),
                {
                    '行业长期关注': 'HYCQGZ',
                    '当前持仓': 'DQCC',
                    '曾经持仓': 'ZJCC'
                }
            ]
        ]
    )
    def test_load(self, block_catalog_file: str, blocks: Dict) -> None:
        block_catalog = UserCustomBlockCatalog(block_catalog_file)
        block_catalog.load()
        assert blocks == block_catalog.blocks

    @pytest.mark.parametrize(
        "block_catalog_file, blocks", [
            [
                data_path('blocknew.cfg.test01'),
                {
                    '行业长期关注': 'HYCQGZ',
                }
            ]
        ]
    )
    def test_add_block(self, block_catalog_file: str, blocks: Dict) -> None:
        block_catalog = UserCustomBlockCatalog(block_catalog_file)
        for block_name, abbr in blocks.items():
            block_catalog.add_block(block_name, abbr)
        block_catalog.load()
        os.remove(block_catalog_file)
        assert blocks == block_catalog.blocks


class TestUserCustomBlock:
    @pytest.mark.parametrize(
        "block_file, codes", [
            [
                data_path('DQCC.blk'),
                [
                    '600438',
                    '600141',
                    '600196'
                ]
            ]
        ]
    )
    def test_load(self, block_file: str, codes: Dict) -> None:
        block_block = UserCustomBlock(block_file)
        block_block.load()
        assert codes == block_block.codes

    @pytest.mark.parametrize(
        "block_file, codes", [
            [
                data_path('DQCC.blk.test001'),
                [
                    '600438',
                    '600141',
                    '600196'
                ]
            ]
        ]
    )
    def test_add_stocks(self, block_file: str, codes: Dict) -> None:
        os.remove(block_file)
        block_block = UserCustomBlock(block_file)
        block_block.load()
        assert not block_block.codes
        block_block.add_stocks(codes, overwrite=True)
        block_block.load()
        assert codes == block_block.codes
