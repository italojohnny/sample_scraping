#!/usr/bin/env python3
# encoding: utf-8
import logging
import pika
import pymongo
import time
import random
import string
import os

logging.basicConfig(level=logging.ERROR)

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
    logging.error(result)
    if number in result:
        return True
    return False


def test_send_message(number):
    try:
        logging.error('inicia envio de mensagem')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()

        channel.queue_declare(queue='hello')
        channel.basic_publish(
            exchange='',
            routing_key='hello',
            body=number
        )
        connection.close()
        logging.error('encerra envio de mensagem')
    except:
        logging.exception("Uma falha inesperada ocorreu")

def main():
    time.sleep(5)
    try:
        logging.info('iniciando aplicacao')
        while True:
            number = get_number()
            if not find(number):
                logging.error('NENHUM CPF ENCONTRADO')
                test_send_message(number)
            else:
                logging.error('CPF ENCONTRADO')
            time.sleep(10)

    except:
        logging.exception("Uma falha inesperada ocorreu")

    finally:
        logging.info('encerrando aplicacao')


if __name__ == '__main__':
    main()
