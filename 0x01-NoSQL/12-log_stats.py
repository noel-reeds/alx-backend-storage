#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


def log_nginx_stats():
    """Provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient()
    db = client.logs
    collection = db.nginx
    documents = collection.find()
    num_docs = 0
    for docs in documents:
        num_docs += 1
    print(f"{num_docs} logs")
    print(f"Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        num = 0
        docs = collection.find({'method': method})
        for doc in docs:
            num += 1
        print(f"\tmethod {method}: {num}")
