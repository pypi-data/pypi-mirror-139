# -*- coding: UTF-8 -*-
"""
This will fire a delayed task without blocking.
https://stackoverflow.com/questions/53587063/using-subprocess-to-avoid-long-running-task-from-disconnecting-discord-py-bot
https://stackoverflow.com/questions/53368203/passing-args-kwargs-to-run-in-executor/53369236
https://stackoverflow.com/questions/51583924/python-typeerror-multiple-arguments-with-functools-partial
https://www.pythonpool.com/functools-partial/
"""
from concurrent.futures import ThreadPoolExecutor
import asyncio
import functools


async def slow_exec(callback, *args, **kwargs):
    """
    :return: Callback results.
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        ThreadPoolExecutor(),
        functools.partial(
            callback,
            *args,
            **kwargs
        )
    )
    return result
