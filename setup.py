# -*- coding:utf-8 -*-
import os

from setuptools import setup, find_packages

current_dir = os.path.dirname(os.path.realpath(__file__))


def long_description():
    with open(os.path.join(current_dir, 'README.rst'),
              encoding='utf8') as fp:
        return fp.read()


setup(
    name='kstock',
    version='0.0.1',
    description='A股数据处理工具',
    long_description=long_description(),
    long_description_content_type='text/x-rst',
    keywords='A股 通达信文件读取 数据处理 K线聚合',
    author='kk',
    author_email='kkppzzah@gmail.com',
    packages=find_packages(
        include=['kstock*'],
        exclude=['tests']
    ),
    install_requires=[
        'numpy',
        'numba',
        'pandas',
        'environ-config'
    ],
    url='https://github.com/kkppzzah/kstock',
    classifiers=[
        'Topic :: Office/Business :: Financial',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    license='MIT',
    entry_points={
        'console_scripts': [
            'dump_tdx_candle_file = kstock.commands.dump_tdx_candle_file:main',
        ]
    },
    python_requires='>=3.8'
)
