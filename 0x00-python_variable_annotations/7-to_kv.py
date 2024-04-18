#!/usr/bin/env python3
"""
Module with a type-annotated function to_kv.
"""


from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Function that takes a string k and an int OR float v as arguments and
    returns a tuple. The first element of the tuple is the string k.
    """
    return (k, v ** 2.0)
