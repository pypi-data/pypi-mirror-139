import hashlib
from itertools import product
from typing import Callable, Optional, List

from .problem import Problem, BfItem, ConstItem
from tqdm import tqdm


def generic_solver(problem: Problem, cipher: bytes, hash_func: Callable[[bytearray], bytes]) -> Optional[bytes]:
    assert isinstance(cipher, bytes)
    plaintext = bytearray()
    pos_index: List[int] = []
    char_table_list = []
    for item in problem.item_list:
        item_len = len(item)  # all item class implement __len__ to return length in the plaintext
        if isinstance(item, BfItem):
            current_index = len(plaintext)
            pos_index.extend(range(current_index, current_index + item_len))
            plaintext.extend(b'\x00' * item_len)  # append useless bytes
            char_table_list.extend([item.char_table] * item_len)
            # append item_len(as number)'s char_table, each position should be view as independent

        elif isinstance(item, ConstItem):
            plaintext.extend(item.literal_string)

    assert len(char_table_list) == len(pos_index)

    bruteforce_space = 1
    for char_table in char_table_list:
        bruteforce_space *= len(char_table)

    with tqdm(total=bruteforce_space) as pbar:
        for product_item in product(*char_table_list):
            for pos, c in zip(pos_index, product_item):
                plaintext[pos] = c
            # print(plaintext, hash_func(plaintext))
            if hash_func(plaintext) == cipher:
                return bytes(plaintext)
    return None


def sha1_solver(problem: Problem, cipher: bytes) -> Optional[bytes]:
    return generic_solver(problem, cipher, lambda x: hashlib.sha1(x).digest())
