#!/usr/bin/env python3
# encoding: utf-8
import logging
import pymongo
import time
import random
import string
import os
import sys

sys.path.insert(0, '..')
from rabbitmq.publisher import Publisher

logging.basicConfig(level=logging.INFO)

def get_number():
    return ''.join(random.choice(string.digits) for i in range(11))

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

def find(number):
    collection = get_collection()
    result = [str(i['cpf'], 'utf-8')for i in collection.find({},{ "_id": 0, "cpf": 1 })]
    logging.info(f'CPFs do banco: {result}')
    if number in result:
        return True
    return False


def main():
    time.sleep(5)
    logging.info('iniciando aplicacao')

    while True:
        time.sleep(10)
        number = get_number()
        publisher = Publisher()
        try:
            if not find(number):
                publisher.username = 'guest'
                publisher.password = 'guest'
                publisher.exchange = 'hello'
                publisher.virtual_host = '/'
                publisher.host = 'rabbitmq'
                publisher.port = 5672
                publisher.send(number)
                logging.info(f'CPF registrado para consulta {number}')

            else:
                logging.info('CPF ja verificado')

        except:
            logging.exception("Uma falha inesperada ocorreu")


if __name__ == '__main__':
    main()
