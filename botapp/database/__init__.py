#!/usr/bin/env python3
# encoding: utf-8
import logging
import pymongo
import os

logging.basicConfig(level=logging.ERROR)


def get_collection():
    db_address='mongodb'
    db_port='27017'
    db_name = os.getenv('MONGO_INITDB_DATABASE')
    collection_name = os.getenv('MONGO_INITDB_COLLECTION')
    user_name = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    user_passwd = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    client = pymongo.MongoClient(f'mongodb://{user_name}:{user_passwd}@{db_address}:{db_port}')
    db = client[db_name]
    return db[collection_name]


def record(cpf, result):
    collection = get_collection()
    output = collection.insert_one({
        "cpf": cpf,
        "result": result,
    })
