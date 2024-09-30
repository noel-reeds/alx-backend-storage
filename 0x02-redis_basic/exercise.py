#!/usr/bin/env python3
from collections.abc import Callable, Optional
import redis
from typing import Union
import uuid


class Cache:
    """class cache"""
    def __init__(self):
        """instantiates a redis db and flushes"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores a str in a redis database"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: Optional[Callable] = None):
        """simulates redis.Redis get method"""
        # check if key exists.
        if key in self._redis.keys():
            value = self._redis.get(key)
            if fn:
                return fn(value)
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
