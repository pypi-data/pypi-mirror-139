from typing import Union


def to_bytes(x: Union[str, bytes], encoding: str) -> bytes:
    if isinstance(x, str):
        return x.encode(encoding)
    else:
        return x
