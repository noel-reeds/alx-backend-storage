#!/usr/bin/env python3
"""Change school topics"""

def update_topics(mongo_collection, name, topics):
    """Changes all topics of a school document based on the name"""
    document = mongo_collection.find_one({'name': name})
    document['topics'] = topics
    return document
