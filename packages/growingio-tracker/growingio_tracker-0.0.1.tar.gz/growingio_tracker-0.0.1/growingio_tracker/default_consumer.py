# -*- coding: utf-8 -*-

from .data_parser import JsonParser
from .consumer import Consumer


class DefaultConsumer(Consumer):
    def __init__(self, product_id, data_source_id, server_host,
                 retry_limit=3, request_timeout=2, retry_backoff_factor=0.25, verify_cert=True):
        super(DefaultConsumer, self).__init__(product_id, data_source_id, server_host,
                                              retry_limit, request_timeout, retry_backoff_factor, verify_cert)
        self._data_parse = JsonParser(product_id, data_source_id)

    def send(self, message):
        if hasattr(message, 'event_type'):
            request_url = self.endpoints['collect']
        else:
            request_url = self.endpoints['item']

        messages = [message]
        data = self._data_parse.get_bytes(messages)

        self.send_data(
            request_url,
            data,
            headers={'content-type': 'application/json'}
        )
