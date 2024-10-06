#!/usr/bin/env python3
"""An expiring web cache and tracker"""
import redis
import requests
from functools import wraps


def get_page(url: str) -> str:
    """implementation of an expiring web cache and tracker"""
    r = redis.Redis()
    res = requests.get(url)
    cache_name = f"count:{url}"

    r.incr(cache_name, amount=1)
    r.expire(cache_name, 10)
    return res.text
