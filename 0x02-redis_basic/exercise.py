#!/usr/bin/env python3
import redis
from typing import Union
import uuid


class Cache:
    """class cache"""
    def __init__(self):
        """instantiates a redis db and flushes"""
        self._redis = redis.Redis()
        self._redis.flushdb

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores a str in a redis database"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
