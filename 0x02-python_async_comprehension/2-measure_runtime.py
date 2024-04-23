#!/usr/bin/env python3
""" asyncio.gather """

import asyncio
import random
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ executes comprehension func 4 times in parallel, returns runtime """

    start_time = time.time()
    tasks = [async_comprehension() for _ in range(4)]
    await asyncio.gather(*tasks)
    end_time = time.time()
    return end_time - start_time
