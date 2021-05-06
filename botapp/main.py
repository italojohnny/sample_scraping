#!/usr/bin/env python3
# encoding: utf-8
import logging
import pika
import time

import cpf_validator as CPF
import database as DB

logging.basicConfig(level=logging.ERROR)

def callback_rabbitmq(ch, method, properties, cpf):
    result = CPF.is_valid(cpf)
    DB.record(cpf, result)
    logging.error(f'{cpf}: {result}')


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
