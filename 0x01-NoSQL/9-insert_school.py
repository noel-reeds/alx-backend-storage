#!/usr/bin/env python3
"""Inserts a document into a mongod server"""

def insert_school(mongo_collection, **kwargs):
    """Function def"""
    new_document = mongo_collection.insert_one(kwargs)
    new_id = new_document.get('_id')
    return new_id
