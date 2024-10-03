#!/usr/bin/env python3
from functools import wraps
from typing import Callable, Optional
import redis
from typing import Union
import uuid


def count_calls(method: Callable) -> Callable:
    """Decorator function to count the number of calls to `store`"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """docstring for wrapper"""
        res = method(self, *args, **kwargs)
        self._redis.incr(key, amount=1)
        return res

    return wrapper

def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a function"""
    inputkey = method.__qualname__ +':inputs'
    outputkey = method.__qualname__ + 'outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        res = method(self, *args, **kwargs)
        self._redis.rpush(outputkey, res)
        for arg in args:
            self._redis.rpush(inputkey, str(arg))
        return res

    return wrapper

class Cache:
    """class cache"""
    def __init__(self):
        """instantiates a redis db and flushes db"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores a str in a redis database"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """simulates redis.Redis.get method"""
        value = self._redis.get(key)
        if fn and value:
            return fn(value)
        elif value:
            return value
        else:
            return None

    def get_str(self, key: str) -> str:
        """converts data retrieved from cache to string"""
        if self._redis.type(key) is str:
            value = self.get(key)
            return str(value)

    def get_int(self, key: str) -> int:
        """converts data retrieved from cache to integer"""
        if self._redis.type(key) is int:
            value = self.get(key)
            return int(value)
