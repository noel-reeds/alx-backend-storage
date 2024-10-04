#!/usr/bin/env python3
from functools import wraps
from typing import Callable, Optional
import redis
from typing import Union
import uuid


def count_calls(method: Callable) -> Callable:
    """Decorator function to count the number of calls to `store`"""
    fn_name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """docstring for wrapper"""
        res = method(self, *args, **kwargs)
        self._redis.incr(fn_name, amount=1)
        return res

    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a function"""
    fn_name = method.__qualname__
    inputs = f'{fn_name}:inputs'
    outputs = f'{fn_name}:outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        res = method(self, *args, **kwargs)
        try:
            self._redis.rpush(inputs, str(args))
            self._redis.rpush(outputs, res)
        except Exception as e:
            print('err: {e}')
        return res
    return wrapper


def replay(method: Callable) -> str:
    """Displays the history of a function"""
    fn_name = method.__qualname__
    inputs = f"{fn_name}:inputs"
    outputs = f"{fn_name}:outputs"

    redis = method.__self__._redis
    calls = int(redis.get(fn_name))
    print(f"{fn_name} was called {calls} times")
    inputs = redis.lrange(inputs, 0, -1)
    outputs = redis.lrange(outputs, 0, -1)
    zipped = list(zip(inputs, outputs))
    for tup in zipped:
        args, res = tup
        args = args.decode('utf-8')
        res = res.decode('utf-8')
        print(f"{fn_name}(*{args}) -> {res}")


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
