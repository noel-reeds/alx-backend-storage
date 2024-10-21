#!/usr/bin/env python3
"""List all documents in a collection"""

def list_all(mongo_collection):
    """Function def"""
    docs = mongo_collection.find()
    return list(docs)
