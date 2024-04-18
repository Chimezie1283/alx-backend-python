#!/usr/bin/env python3
"""
Module with a type-annotated function sum_list.
"""


from typing import List


def sum_list(input_list: List[float]) -> float:
    """
    Function that takes a list of floats as input and returns their sum .
    """
    return sum(input_list)
