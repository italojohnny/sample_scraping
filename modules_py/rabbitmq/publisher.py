#!/usr/bin/env python3
# encoding: utf-8


import pika


class Publisher:
    def __init__(self):
        self.username = None
        self.password = None
        self.channel = None
        self.host = None
        self.port = None
        self.virtual_host = None
        self.exchange = None
        self.exchange_type = 'fanout'


    def send(self, message):
        credentials = pika.PlainCredentials(
            self.username,
            self.password
        )

        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.virtual_host,
            credentials=credentials
        )

        self.connection = pika.BlockingConnection(
            parameters=parameters
        )

        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type=self.exchange_type,
            passive=False,
            durable=False,
            auto_delete=False,
            internal=False
        )

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key='',
            body=message
        )

        self.channel.close()
        self.connection.close()
