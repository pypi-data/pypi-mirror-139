# -*- coding: utf-8 -*-
from .default_consumer import DefaultConsumer


class BufferedConsumer(DefaultConsumer):

    def __init__(self, product_id, data_source_id, server_host, max_size=50,
                 retry_limit=3, request_timeout=2, retry_backoff_factor=0.25, verify_cert=True):
        super(BufferedConsumer, self).__init__(product_id, data_source_id, server_host,
                                               retry_limit, request_timeout, retry_backoff_factor, verify_cert)
        self._events = []
        self._max_size = min(200, max_size)

    def send(self, message):
        if hasattr(message, 'event_type'):
            request_url = self.endpoints['collect']
            buf = self._events
            buf.append(message)
            if len(buf) >= self._max_size:
                self._flush_event(request_url)
        else:
            request_url = self.endpoints['item']
            messages = [message]
            data = self._data_parse.get_bytes(messages)
            self.send_data(
                request_url,
                data,
                headers={'content-type': 'application/json'}
            )

    def _flush_event(self, request_url):
        buf = self._events

        while buf:
            batch = buf[:self._max_size]
            data = self._data_parse.get_bytes(batch)
            self.send_data(
                request_url,
                data,
                headers={'content-type': 'application/json'}
            )
            buf = buf[self._max_size:]
        self._events = buf

    def flush(self):
        request_url = self.endpoints['collect']
        self._flush_event(request_url)
