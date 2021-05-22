#!/usr/bin/env python3
# encoding: utf-8
import logging
import time
import sys

sys.path.insert(0, '..')
from rabbitmq.consumer import Consumer
import cpf_validator
from database import Database

logging.basicConfig(level=logging.INFO)


def callback_rabbitmq(channel, method, properties, cpf):
    """
    Permite escalar facilmente novos metodos de validacao de cpf em novos sites.
    Assim como, alternar entre os metodos dependendo da regra de negocio
    """
    if False:
        validator = cpf_validator.ValidatorA()
    else:
        validator = cpf_validator.ValidatorB()

    result = validator.verify(cpf)
    db = Database()
    db.record(cpf, result)
    logging.info(f'{cpf}: {result}')


    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():

    try:
        time.sleep(60)
        logging.info('iniciando aplicacao')

        rabbitmq = Consumer(
            username='guest'
            password='guest'
            queue='hello'
            exchange='hello'
            virtual_host='/'
            host='rabbitmq'
            port=5672
            callback=callback_rabbitmq
        )
        rabbitmq.config()
        rabbitmq.start()
        logging.error('Fim do loop')

    except:
        logging.exception("Uma falha inesperada ocorreu")

    finally:
        logging.info('encerrando aplicacao')


if __name__ == '__main__':
    main()
