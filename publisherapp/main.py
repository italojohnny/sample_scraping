#!/usr/bin/env python3
# encoding: utf-8
import logging
import time

logging.basicConfig(level=logging.DEBUG)

def main():
    time.sleep(5)
    try:
        logging.info('iniciando aplicacao')
        while True:
            time.sleep(3)
            logging.info('teste...')

    except:
        logging.exception("Uma falha inesperada ocorreu")

    finally:
        logging.info('encerrando aplicacao')


if __name__ == '__main__':
    main()
