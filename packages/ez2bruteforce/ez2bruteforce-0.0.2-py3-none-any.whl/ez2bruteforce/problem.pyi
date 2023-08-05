from .utils import to_bytes as to_bytes
from typing import List, Union

class BfItem:
    char_table: bytearray
    length: int
    def __init__(self, length: int, char_table: Union[str, bytes, List[Union[str, bytes]]], encoding: str = ...): ...
    def __len__(self): ...

class ConstItem:
    literal_string: bytearray
    def __init__(self, string: Union[str, bytes], encoding: str = ...) -> None: ...
    def __len__(self): ...

class Problem:
    item_pos: List[int]
    item_list: List[Union[BfItem, ConstItem]]
    length: int
    def __init__(self, item_list: List[Union[BfItem, str, bytes]], encoding: str = ...) -> None: ...
