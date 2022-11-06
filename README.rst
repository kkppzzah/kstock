A股数据处理工具
============================

功能
------
* 通达信：K线文件读取、自定义板块读写。
* 技术指标：MACD指标计算。
* 统计：收盘价N日内新高和新低计算。
* 杂类：标记文本。

安装
------

.. code-block:: bash

    pip install kstock

API
----

* 通达信
    * 环境变量

        - TDX_ROOT

            通达信安装目录。用来计算自定义板块文件的目录。可以不设置，调用计算自定义板块文件路径的API的时候，需要明确指定通达信安装目录参数。

        - TDX_VIPDOC

            通达信K线文件所在根目录。用来计算K线文件的路径。可以不设置，调用计算K线文件路径API的时候，需要明确指定K线文件所在根目录。

    * K线文件读取

        周期类型，d：日；M5：5分钟；M1：1分钟。

        .. code-block:: python

            >>> from kstock.tdx.candle_loader import load_candle_day
            >>> from kstock.tdx import utils
            >>> candle_file_path = utils.stock_candle_file_path('3001389', 'd', vipdoc_root_path='D:\\海王星金融终端-中国银河证券\\vipdoc')
            >>> candle_file_path
            'D:\\海王星金融终端-中国银河证券\\vipdoc\\sz\\lday\\sz301389.day'
            >>> candles = load_candle_day(candle_file_path)
            >>> candles
                             time   open   high    low  close       amount    volume
            time
            2022-10-31 2022-10-31  20.89  22.02  19.91  20.94  538447616.0  26176828
            2022-11-01 2022-11-01  20.03  20.40  19.61  20.30  309263840.0  15384969
            2022-11-02 2022-11-02  20.29  21.50  20.10  20.55  314957216.0  15179596
            2022-11-03 2022-11-03  20.00  20.50  19.63  20.33  213598800.0  10662210
            2022-11-04 2022-11-04  20.40  20.66  20.12  20.33  221527104.0  10869630


    * 自定义板块读写

        .. code-block:: python

            >>> from kstock.tdx.block import UserCustomBlockCatalog, UserCustomBlock
            >>> from kstock.tdx import utils
            >>> import os
            >>> block_file_dir = utils.block_file_dir(tdx_root_path='D:\\海王星金融终端-中国银河证券')
            >>> block_file_dir
            'D:\\海王星金融终端-中国银河证券\\T0002\\blocknew'
            >>> block = UserCustomBlock(os.path.join(block_file_dir, 'DQCC.blk'))
            >>> block.load()
            >>> block.codes
            ['600438', '600141', '600196']
            >>> block.add_stocks(['000001'], overwrite=False)
            >>> block.load()
            >>> block.codes
            ['600438', '600141', '600196', '000001']

* 技术指标
    - MACD指标计算

        .. code-block:: python

            >>> import numpy as np
            >>> from kstock.ta.indicator.macd import macd
            >>> closes = np.array([20.94, 20.30, 20.55, 20.33, 20.33], dtype=np.float64)
            >>> dif, dem, osc = macd(close_set)
            >>> np.around(dif, 2)
            array([ 0.  , -0.05, -0.07, -0.1 , -0.13])
            >>> np.around(dem, 2)
            array([ 0.  , -0.01, -0.02, -0.04, -0.06])
            >>> np.around(osc, 2)
            array([ 0.  , -0.08, -0.1 , -0.13, -0.14])



* 统计
    * 收盘价N日内新高和新低计算

        .. code-block:: python

            >>> import numpy as np
            >>> from kstock.stats.stat_utils import calculate_nd_h_l
            >>> closes = np.array([
            ...                 134.80, 127.72, 121.77, 119.50, 106.48, 102.50, 97.50, 91.50, 90.85, 94.25,
            ...                 92.31, 95.25, 97.74, 94.88, 92.00, 97.88, 95.69, 100.66, 103.50, 103.00,
            ...                 104.70, 108.26, 109.63, 108.30, 105.32, 113.24, 112.14, 112.14
            ...             ])

            >>> nd_h, nd_l = calculate_nd_h_l(closes)
            >>> nd_h
            array([ 0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  5,  7,  0,  0, 10,  0,
                    12, 14,  0, 16, 18, 19,  0,  0, 22,  0,  0], dtype=int64)
            >>> nd_l
            array([0, 2, 3, 4, 5, 6, 7, 8, 9, 0, 2, 0, 0, 3, 6, 0, 2, 0, 0, 2, 0, 0,
                   0, 2, 4, 0, 2, 3], dtype=int64)



* 杂类
    * 标记文本

        .. code-block:: python

            >>> from kstock.misc.trie_tree import TrieTree
            >>> words = [
            ...                     {'word': '复星医药', 'meta': {'type': 'stock', 'code': 'sh.600196'}},
            ...                     {'word': '天齐锂业', 'meta': {'type': 'stock', 'code': 'sz.002466'}},
            ...                     {'word': '比亚迪', 'meta': {'type': 'stock', 'code': 'sz.002594'}},
            ...                     {'word': '潞安环能', 'meta': {'type': 'stock', 'code': 'sh.601699'}},
            ...                     {'word': '韦尔股份', 'meta': {'type': 'stock', 'code': 'sh.603501'}},
            ...                     {'word': '派能科技', 'meta': {'type': 'stock', 'code': 'sh.688063'}},
            ...                     {'word': '兖矿能源', 'meta': {'type': 'stock', 'code': 'sh.600188'}},
            ...                 ]
            >>> doc = ("""【宁德时代、天齐锂业等17股获北向资金增持额超亿元】统计显示，10月31日共有750只个股获北向资金持股量环比上一个交易日增"""
            ...                  """加。以增持的股份数量和当日收盘价为基准进行测算，加仓股中，增持市值在1亿元以上的有17只，增持市值最多的是宁德时代，最新"""
            ...                  """持股量为1.63亿股，环比增加0.88%，增持市值为5.27亿元；增持市值较多还有天齐锂业、比亚迪、潞安环能、韦尔股份、派能科技"""
            ...                  """、兖矿能源、德业股份、复星医药等股""")
            >>> for word_info in words:
            ...     word, meta = word_info['word'], word_info['meta']
            ...     tree.insert(word, meta)
            ...
            >>> tags = tree.tag(doc)
            >>> tags
            [[start:6, end:9, meta:{'type': 'stock', 'code': 'sz.002466'}], [start:163, end:166, meta:{'type': 'stock', 'code': 'sz.002466'}], [start:168, end:170, meta:{'type': 'stock', 'code': 'sz.002594'}], [start:172, end:175, meta:{'type': 'stock', 'code': 'sh.601699'}], [start:177, end:180, meta:{'type': 'stock', 'co
            de': 'sh.603501'}], [start:182, end:185, meta:{'type': 'stock', 'code': 'sh.688063'}], [start:187, end:190, meta:{'type': 'stock', 'code': 'sh.600188'}], [start:197, end:200, meta:{'type': 'stock', 'code': 'sh.600196'}]]

