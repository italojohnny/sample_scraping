#!/usr/bin/env python3
# encoding: utf-8
from selenium.webdriver import Remote
import logging
import time
import re


logging.basicConfig(level=logging.ERROR)

def is_valid(cpf):
    result = False
    logging.error(cpf)
    try:
        browser = Remote(
            command_executor='http://firefox:4444/wd/hub',
            desired_capabilities={
                'browserName':'firefox'
            }
        )
        browser.get('https://www.geradorcpf.com/validar-cpf.htm')

        submit_btn = browser.find_element_by_xpath('//*[@id="botaoValidarCPF"]')

        input_text = browser.find_element_by_xpath('//*[@id="cpf"]')
        input_text.send_keys(str(cpf))

        time.sleep(2)
        submit_btn.click()

        output = browser.find_element_by_xpath('/html/body/div[3]/section[1]/div/div/div/div[4]/div/span/div').text
        if re.match(r'( |^)(valid)', output, re.I):
            result = True

        browser.quit()
    except:
        logging.exception('erro inesperado')

    return result
