#!/usr/bin/env python3
"""An expiring web cache and tracker"""
import redis
import requests
from typing import Callable
from functools import wraps


def calls_counter(method: Callable) -> Callable:
    """Returns number of times page is accessed"""
    cache_name = f"count:{url}"

    @wraps(method)
    def wrapper(*args, **kwargs):
        """wrapper function"""
        res = method(*args)
        r = redis.Redis()
        r.incr(cache_name, amount=1)
        r.expire(cache_name, 10)
        return res
    return wrapper

@calls_counter
def get_page(url: str) -> str:
    """implementation of an expiring web cache and tracker"""
    r = redis.Redis()
    res = requests.get(url)

    return res.text
