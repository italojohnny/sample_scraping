#!/usr/bin/env python3
# encoding: utf-8
import logging
import pika
import time
import random
import string

logging.basicConfig(level=logging.DEBUG)
def get_number():
    return ''.join(random.choice(string.digits) for i in range(11))

def test_send_message():
    logging.info('inicia envio de mensagem')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body=get_number()
    )
    connection.close()
    logging.info('encerra envio de mensagem')

def main():
    time.sleep(5)
    try:
        logging.info('iniciando aplicacao')
        while True:
            time.sleep(3)
            test_send_message()

    except:
        logging.exception("Uma falha inesperada ocorreu")

    finally:
        logging.info('encerrando aplicacao')


if __name__ == '__main__':
    main()
