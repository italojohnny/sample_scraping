#!/usr/bin/env python3
# encoding: utf-8
import logging
import pymongo
import os

logging.basicConfig(level=logging.INFO)


class SingletonMeta(type):
    _instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __get_collection(self):
        db_address='mongodb'
        db_port='27017'
        db_name = os.getenv('MONGO_INITDB_DATABASE')
        collection_name = os.getenv('MONGO_INITDB_COLLECTION')
        user_name = os.getenv('MONGO_INITDB_ROOT_USERNAME')
        user_passwd = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
        client = pymongo.MongoClient(f'mongodb://{user_name}:{user_passwd}@{db_address}:{db_port}')
        db = client[db_name]
        return db[collection_name]


    def record(self, cpf, result):
        collection = self.__get_collection()
        output = collection.insert_one({
            "cpf": cpf,
            "result": result,
        })
        logging.info(f'CPF: "{cpf}" Result: "{result}"; Gravado no Banco!')
