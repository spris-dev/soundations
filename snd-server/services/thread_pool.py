import functools


from typing import TypeVar, Callable
from typing_extensions import ParamSpec
from anyio import Semaphore, to_thread


T = TypeVar("T")
P = ParamSpec("P")


class ThreadPool:
    def __init__(self, max_concurrent_threads: int = 10) -> None:
        self.max_threads_guard = Semaphore(max_concurrent_threads)

    async def run_async(
        self, func: Callable[P, T], *args: P.args, **kwargs: P.kwargs
    ) -> T:
        if kwargs:
            func = functools.partial(func, **kwargs)
        async with self.max_threads_guard:
            return await to_thread.run_sync(func, *args)
