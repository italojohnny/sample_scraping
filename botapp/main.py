#!/usr/bin/env python3
# encoding: utf-8
import logging
import cpf_validator as CPF
import pymongo
import pika
import os
import time

logging.basicConfig(level=logging.ERROR)

def callback_rabbitmq(ch, method, properties, cpf):
    if CPF.is_valid(cpf):
        logging.error(f'{cpf}:valid!')
    else:
        logging.error(f'{cpf}: invalid!')


def test_receiver_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.basic_consume(
        queue='hello',
        auto_ack=True,
        on_message_callback=callback_rabbitmq
    )
    logging.info('esperando na fila por mensagem.')
    channel.start_consuming()


def test_mongodb():
    logging.info('inicia teste mongodb')

    user_name = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    user_passwd = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    db_name = os.getenv('MONGO_INITDB_DATABASE')
    db_address='mongodb'
    db_port='27017'

    logging.info('conexao com mongodb')
    uri =  f'mongodb://{user_name}:{user_passwd}@{db_address}:{db_port}'
    logging.info(uri)
    client = pymongo.MongoClient(uri)
    db = client['italo']
    collection = db['collection']

    logging.info('criacao de dados')
    data = [
        { "name": "John", "address": "Highway 37" },
        { "name": "Adam", "address": "Highway 37" },
    ]
    x = collection.insert_many(data)
    logging.info(x)

    logging.info('recuperacao de dados')
    query = collection.find({}, {'name': 1})
    for item in query:
        logging.info(item)

    logging.info('encerra teste mongodb')


def main():
    time.sleep(5)
    try:
        logging.info('iniciando aplicacao')
        while True:
            time.sleep(5)
            test_receiver_rabbitmq()

    except:
        logging.exception("Uma falha inesperada ocorreu")

    finally:
        logging.info('encerrando aplicacao')


if __name__ == '__main__':
    main()
