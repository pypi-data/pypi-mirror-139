import inspect
from typing import Any, Awaitable, Callable, TypeVar, cast

from jetpack import utils
from jetpack._task.errors import NotAsyncError
from jetpack._task.jetpack_function import JetpackFunction
from jetpack._task.jetpack_function_with_client import schedule as schedule
from jetpack.config import symbols

T = TypeVar("T")


# @function is our general remote work decorator. It does not specify how the
# work will be done (RPC, job, queue, etc) and instead leaves that as an
# implementation detail.
def function(fn: Callable[..., T]) -> Callable[..., Awaitable[T]]:
    # Use asyncio.iscoroutine() instead?
    if not inspect.iscoroutinefunction(fn):
        raise NotAsyncError(
            f"Jetpack functions must be async. {utils.qualified_func_name(fn)} is not async."
        )
    task: JetpackFunction[T] = JetpackFunction(fn)
    symbols.get_symbol_table().register(fn)
    return task


jet = function
jetroutine = function
