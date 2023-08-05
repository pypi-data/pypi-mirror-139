from itertools import chain
from typing import List, Union

from .utils import to_bytes


class BfItem:
    char_table: bytearray
    length: int

    def __init__(self, length: int,
                 char_table: Union[str, bytes, List[Union[str, bytes]]],
                 encoding: str = 'utf-8'):
        self.length = length
        self.char_table = bytearray()
        if isinstance(char_table, str):
            self.char_table.extend(to_bytes(char_table, encoding))
        elif isinstance(char_table, bytes):
            self.char_table.extend(char_table)
        elif isinstance(char_table, list):
            self.char_table.extend(
                chain(*map(lambda x: to_bytes(x, encoding), char_table)))
        else:
            raise TypeError(f'char_table must be str, '
                            f'bytes or list, not {type(char_table)}')

        # remove repeated chars
        self.char_table = bytearray(set(self.char_table))

    def __len__(self):
        return self.length


class ConstItem:
    literal_string: bytearray

    def __init__(self, string: Union[str, bytes], encoding='utf-8'):
        self.literal_string = bytearray()
        if isinstance(string, str):
            self.literal_string.extend(to_bytes(string, encoding))
        elif isinstance(string, bytes):
            self.literal_string.extend(string)
        else:
            raise TypeError(f'string must be str or bytes, not {type(string)}')

    def __len__(self):
        return len(self.literal_string)


class Problem():
    item_pos: List[int]  # record the start position of each item
    item_list: List[Union[BfItem, ConstItem]]  # recprd every item
    length: int  # literal length of the whole string

    def __init__(self,
                 item_list: List[Union[BfItem, str, bytes]],
                 encoding='utf-8'):
        self.item_list = list()
        self.item_pos = list()
        self.length = 0
        for item in item_list:
            self.item_pos.append(self.length)
            self.length += len(item)
            if isinstance(item, BfItem):
                self.item_list.append(item)
            elif isinstance(item, str) or isinstance(item, bytes):
                self.item_list.append(ConstItem(item, encoding))
            else:
                raise TypeError(f'item must be bruteforce_item'
                                f' or str or bytes, not {type(item)}')
