# -*- coding:utf-8 -*
from typing import List, Dict

import pytest

from kstock.misc.trie_tree import TrieTree
from .test_utils import tag_hard


class TestTrieTree:
    def test_basic(self):
        tree: TrieTree = TrieTree()
        test_data_list = [
            {'word': '复星医药', 'meta': {'type': 'stock', 'code': 'sh.600196'}, 'need_insert': True},
            {'word': '复旦复华', 'meta': {'type': 'stock', 'code': 'sh.600624'}, 'need_insert': True},
            {'word': '青岛啤酒', 'meta': {'type': 'stock', 'code': 'sh.600600'}, 'need_insert': False},
        ]
        for test_data in test_data_list:
            if test_data['need_insert']:
                tree.insert(test_data['word'], test_data['meta'])
        for test_data in test_data_list:
            if test_data['need_insert']:
                assert test_data['meta'] == tree.search(test_data['word'])
            else:
                assert tree.search(test_data['word']) is None

    @pytest.mark.parametrize(
        "words, doc", [
            [
                [
                    {'word': '复星医药', 'meta': {'type': 'stock', 'code': 'sh.600196'}},
                    {'word': '复旦复华', 'meta': {'type': 'stock', 'code': 'sh.600624'}},
                    {'word': '青岛啤酒', 'meta': {'type': 'stock', 'code': 'sh.600600'}},
                ],
                ("""【复星医药携多款创新产品亮相第五届进博会 “网红”达芬奇手术机器人将实现本土制造】据每日经济新闻，11月5日至11月10日，"""
                 """第五届中国国际进口博览会将于上海举办。作为五届进博老友，复星医药将再次携手海外成员企业和全球医药健康产业合作伙伴参展。"""
                 """今年进博会，复星医药还将首次展示多款全球领先的创新药品与医疗器械，其中包括全球首款银屑病口服靶向药物欧泰乐（阿普米司特"""
                 """片）、全新第三代COMT抑制剂Ongentys（奥吡卡朋）以及器械方面的源自以色列能量源技术的医美级家用美容仪LMNTone等。 """)
            ],
            [
                [
                    {'word': '复星医药', 'meta': {'type': 'stock', 'code': 'sh.600196'}},
                    {'word': '天齐锂业', 'meta': {'type': 'stock', 'code': 'sz.002466'}},
                    {'word': '比亚迪', 'meta': {'type': 'stock', 'code': 'sz.002594'}},
                    {'word': '潞安环能', 'meta': {'type': 'stock', 'code': 'sh.601699'}},
                    {'word': '韦尔股份', 'meta': {'type': 'stock', 'code': 'sh.603501'}},
                    {'word': '派能科技', 'meta': {'type': 'stock', 'code': 'sh.688063'}},
                    {'word': '兖矿能源', 'meta': {'type': 'stock', 'code': 'sh.600188'}},
                ],
                ("""【宁德时代、天齐锂业等17股获北向资金增持额超亿元】统计显示，10月31日共有750只个股获北向资金持股量环比上一个交易日增"""
                 """加。以增持的股份数量和当日收盘价为基准进行测算，加仓股中，增持市值在1亿元以上的有17只，增持市值最多的是宁德时代，最新"""
                 """持股量为1.63亿股，环比增加0.88%，增持市值为5.27亿元；增持市值较多还有天齐锂业、比亚迪、潞安环能、韦尔股份、派能科技"""
                 """、兖矿能源、德业股份、复星医药等股""")
            ]
        ]
    )
    def test_tag(self, words: List[Dict], doc: str):
        tree: TrieTree = TrieTree()
        for word_info in words:
            word, meta = word_info['word'], word_info['meta']
            tree.insert(word, meta)
        tags = tree.tag(doc)
        tags_result = tag_hard(words, doc)
        assert len(tags_result) == len(tags)
        assert tags_result == tags
