#!/usr/bin/env python3
# encoding: utf-8
import logging
from selenium.webdriver import Remote
import time

logging.basicConfig(level=logging.DEBUG)

def main():
    time.sleep(5)
    try:
        logging.info('iniciando aplicacao')
        browser = Remote(
            command_executor='http://firefox:4444/wd/hub',
            desired_capabilities={
                'browserName':'firefox'
            }
        )
        browser.get('http://google.com')
        browser.save_screenshot('/tmp/teste.png')
        browser.quit()

    except:
        logging.exception("Uma falha inesperada ocorreu")

    finally:
        logging.info('encerrando aplicacao')


if __name__ == '__main__':
    main()
