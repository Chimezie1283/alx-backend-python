#!/usr/bin/env python3
"""
Module with a type-annotated function make_multiplier.
"""


from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Return a function that multiplies a float by the given multiplier.
    """
    def multiplier_function(x: float) -> float:
        return x * multiplier
    return multiplier_function
