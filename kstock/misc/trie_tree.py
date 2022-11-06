# -*- coding:utf-8 -*-
from __future__ import annotations
from typing import Any, List


class Node(object):
    def __init__(self):
        self._childes = {}
        self._meta = None

    @property
    def childes(self):
        return self._childes

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, meta: Any):
        self._meta = meta

    def add_child(self, char: str) -> Node:
        node = self._childes.get(char)
        if node is None:
            node = Node()
            self._childes[char] = node
        return node

    def get_child(self, char: str) -> Node:
        return self._childes.get(char)


class Tag(object):
    def __init__(self, start: int, end: int, meta: Any):
        self._start = start
        self._end = end
        self._meta = meta

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def meta(self):
        return self._meta

    def __eq__(self, other):
        if not isinstance(other, Tag):
            return False
        return self._start == other._start and self._end == other._end and self._meta == other._meta

    def __repr__(self):
        return f'[start:{self._start}, end:{self._end}, meta:{self._meta}]'


class TrieTree(object):
    def __init__(self):
        self._root = Node()
        self._max_word_len = 0

    def insert(self, word: str, meta: Any) -> None:
        node = self._root
        for char in word:
            node = node.add_child(char)
        node.meta = meta
        self._max_word_len = max(self._max_word_len, len(word))

    def search(self, word: str) -> Any:
        node = self._root
        for char in word:
            node = node.get_child(char)
            if not node:
                return None
        return node.meta if node is not None else None

    def tag(self, doc: str) -> List[Tag]:
        index, doc_len = 0, len(doc)
        tags = []
        while index < doc_len:
            current_word_index = 0
            node = self._root
            while current_word_index < self._max_word_len and (index + current_word_index) < doc_len:
                char = doc[index + current_word_index]
                node = node.get_child(char)
                if node is not None:
                    current_word_index += 1
                    if node.meta is not None:
                        break
                else:
                    break
            if node is not None and node.meta is not None:
                tags.append(Tag(index, index + current_word_index - 1, node.meta))
                index += current_word_index
            else:
                index += 1
        return tags
