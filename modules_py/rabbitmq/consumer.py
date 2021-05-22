#!/usr/bin/env python3
# encoding: utf-8


import pika


class Consumer:
    def __init__(self, username, password, queue, exchange, virtual_host, host, port, callback):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.callback = callback
        self.heartbeart = 1500
        self.blocked_connection_timeout=1200

        self.queue = None
        self.exchange = None
        self.channel = None
        self.connection = None


    def config(self):
        credentials = pika.PlainCredentials(
            self.username,
            self.password
        )
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.virtual_host,
            credentials=credentials,
            blocked_connection_timeout=self.blocked_connection_timeout,
#            heartbeart=self.heartbeart
        )
        self.connection = pika.SelectConnection(
            parameters=parameters,
            on_open_callback=self.ampq_connected,
            on_close_callback=self.ampq_disconnected
        )

    def start(self):
        self.connection.ioloop.start()


    def stop(self):
        self.connection.close()
        self.connection.ioloop.stop()


    def ampq_connected(self, connection):
        connection.channel(
            on_open_callback=self.ampq_channel_open
        )


    def ampq_channel_open(self, new_channel):
        if new_channel:
            self.channel = new_channel

        self.channel.queue_declare(
            queue=self.queue,
            durable=False,
            exclusive=False,
            auto_delete=True,
            callback=self.ampq_queue_declared
        )


    def ampq_queue_declared(self, method):
        self.channel.queue_bind(
            queue=self.queue,
            exchange=self.exchange,
            routing_key=''
        )
        self.channel.basic_qos(
            prefetch_count=1
        )
        self.channel.add_on_close_callback(
            self.ampq_channel_close
        )
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.callback,
            auto_ack=False,
            exclusive=False,
            consumer_tag=None,
            arguments=None
        )


    def ampq_channel_close(self, connection, exception):
        pass


    def ampq_disconnected(self, Connection, exception):
        pass
