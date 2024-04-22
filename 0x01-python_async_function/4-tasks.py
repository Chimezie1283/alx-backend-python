#!/usr/bin/env python3
"""
This module contains the function task_wait_n.
"""
import asyncio
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Spawns task_wait_random n times with the specified max delay.
    Returns the list of all the delays (float values).
    The list of delays is sorted (in ascending order).
    """
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    completed, pending = await asyncio.wait(tasks,
            return_when=asyncio.ALL_COMPLETED)
    return [task.result() for task in completed]
