#!/usr/bin/env python3
# encoding: utf-8
from abc import ABC, abstractmethod
from selenium.webdriver import Remote
import logging
import time
import re

logging.basicConfig(level=logging.INFO)

class Site(ABC):
    def get_browser(self):
        return Remote(
            command_executor='http://firefox:4444/wd/hub',
            desired_capabilities={'browserName':'firefox'}
        )

    def is_valid(self, text) -> bool:
        if re.match(r'( |^)(v.lido)', text, re.I):
            return True
        return False

    @abstractmethod
    def verify(self, cpf) -> bool:
        pass


class ValidatorFactory():
    @abstractmethod
    def factory_method(self):
        pass

    def verify(self, cpf: str) -> bool:
        site = self.factory_method() # retorna um instancia site
        return site.verify(cpf)


class ValidatorA(ValidatorFactory):
    def factory_method(self) -> Site:
        return SiteA()


class ValidatorB(ValidatorFactory):
    def factory_method(self) -> Site:
        return SiteB()


class SiteA(Site):
    def verify(self, cpf) -> bool:
        output = 'invalido'
        try:
            browser = self.get_browser()
            browser.get('https://www.geradorcpf.com/validar-cpf.htm')

            input_text = browser.find_element_by_xpath('//*[@id="cpf"]')
            input_text.send_keys(str(cpf))

            time.sleep(2)

            submit_btn = browser.find_element_by_xpath('//*[@id="botaoValidarCPF"]')
            submit_btn.click()

            output = browser.find_element_by_xpath('/html/body/div[3]/section[1]/div/div/div/div[4]/div/span/div').text

            browser.quit()
        except:
            logging.exception('erro inesperado')

        return self.is_valid(output)


class SiteB(Site):
    def verify(self, cpf) -> bool:
        output = 'invalido'
        try:
            browser = self.get_browser()
            browser.get('https://validadordecpf.clevert.com.br/v-cpf.php')

            input_text = browser.find_element_by_xpath('//*[@id="cpf"]')
            input_text.send_keys(str(cpf))

            time.sleep(3)

            submit_btn = browser.find_element_by_xpath('//*[@id="gerar"]')
            submit_btn.click()

            output = browser.find_element_by_xpath('//*[@id="resposta1"]').text
            if not output:
                output = browser.find_element_by_xpath('//*[@id="resposta2"]').text

            browser.quit()

        except:
            logging.exception('erro inesperado')

        return self.is_valid(output)
