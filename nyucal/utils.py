# -*- coding: utf-8 -*-

from functools import wraps
import logging


def log_begin(func):
    """Log the beginning of function :code:`func`

    As long as :code:`logging.basicConfig` sets the level to be
    :code:`logging.INFO` or below, a message will be sent at the
    function's beginning.

        >>> @log_begin
        ... def f(x):
        ...     return x*x
        ...
        >>> f(2)
        4
        >>> logging.basicConfig(level=logging.INFO)
        >>> f(2)
        INFO:f:begin
        4
    """
    @wraps(func)
    def wrapper(*args, **kwds):
        logging.getLogger(f.__name__).info("begin")
        return f(*args, **kwds)
    return wrapper


def log_end(func):
    """Log the end of function :code:`func`

        >>> @log_end
        ... def g(x):
        ...     return x+5
        ...
        >>> logging.basicConfig(level=logging.INFO)
        >>> g(3)
        INFO:g:end
        8
    """
    @wraps(func)
    def wrapper(*args, **kwds):
        res = f(*args, **kwds)
        logging.getLogger(f.__name__).info("end")
        return res
    return wrapper


def log_result(func):
    """Log the result of function :code:`func`

        >>> @log_result
        ... def f(x):
        ...     return x*x
        ...
        >>> logging.basicConfig(level=logging.INFO)
        >>> y=f(3)
        INFO:f:result: 9
        >>> @log_begin
        ... @log_end
        ... @log_result
        ... def f(x):
        ...     return x*x
        ...
        >>> f(3)
        INFO:f:begin
        INFO:f:result: 9
        INFO:f:end
        9
    """
    @wraps(func)
    def wrapper(*args, **kwds):
        res = f(*args, **kwds)
        logging.getLogger(f.__name__).info("result: %s", repr(res))
        return res
    return wrapper
