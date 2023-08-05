# -*- coding: utf-8 -*-

from __future__ import absolute_import
import threading
from datetime import datetime, timedelta
from .default_consumer import DefaultConsumer


class FlushThread(threading.Thread):
    '''
    FlushThread is used to asynchronously flush the events stored in
    the AsyncBufferedConsumer buffers.
    '''

    def __init__(self, consumer):
        threading.Thread.__init__(self)
        self.consumer = consumer

    def run(self):
        self.consumer._sync_flush()


class AsyncBufferedConsumer(DefaultConsumer):

    def __init__(self, product_id, data_source_id, server_host,
                 flush_after=timedelta(0, 10), flush_first=False,
                 max_size=50, request_timeout=2,
                 retry_limit=3, retry_backoff_factor=0.25, verify_cert=True):

        super(AsyncBufferedConsumer, self).__init__(
            product_id, data_source_id, server_host,
            request_timeout=request_timeout,
            retry_limit=retry_limit,
            retry_backoff_factor=retry_backoff_factor,
            verify_cert=verify_cert,
        )

        # remove the minimum max size that the SynchronousBufferedConsumer
        self._max_size = max_size
        self.flush_after = flush_after
        self.flush_first = flush_first

        self._async_events = []
        self._async_items = []

        self._async_buffers = {
            'events': [],
            'items': [],
        }

        if not self.flush_first:
            self.last_flushed = datetime.now()
        else:
            self.last_flushed = None

        self.flush_lock = threading.Lock()
        self.flushing_thread = None

    def _flush_thread_is_free(self):
        '''
        Check whether a thread is currently being used to flush events. This
        guarantees that only one thread is ever used at a time to flush.
        '''
        return self.flushing_thread is None or not self.flushing_thread.is_alive()

    def _should_flush(self):
        '''
        Checks whether the events in the AsyncBufferedConsumer should be flushed.
        '''
        full = len(self._async_events) >= self._max_size or len(self._async_items) > 0

        # always flush the first event
        stale = self.last_flushed is None

        if not stale and self.flush_after:
            stale = datetime.now() - self.last_flushed > self.flush_after

        if stale:
            return True

        if full:
            return True

        return False

    def send(self, message):

        if hasattr(message, 'event_type'):
            buf = self._async_events
            buf.append(message)
        else:
            buf = self._async_items
            buf.append(message)

        should_flush = self._should_flush()
        if should_flush:
            self.flush()

    def flush(self):

        with self.flush_lock:
            if self._flush_thread_is_free():

                self.transfer_buffers()

                self.flushing_thread = FlushThread(self)
                self.flushing_thread.start()

                flushing = True
            else:
                flushing = False

        if flushing:
            self.last_flushed = datetime.now()

        return flushing

    def transfer_buffers(self):
        buf = self._async_events
        while buf:
            self._async_buffers['events'].append(buf.pop(0))
        buf = self._async_items
        while buf:
            self._async_buffers['items'].append(buf.pop(0))

    def _sync_flush(self):
        if len(self._async_buffers['events']) > 0:
            request_url = self.endpoints['collect']
            buf = self._async_buffers['events']
            while buf:
                batch = buf[:self._max_size]
                data = self._data_parse.get_bytes(batch)
                self.send_data(
                    request_url,
                    data,
                    headers={'content-type': 'application/json'}
                )
                buf = buf[self._max_size:]
            self._async_buffers['events'] = buf

        if len(self._async_buffers['items']) > 0:
            request_url = self.endpoints['item']
            buf = self._async_buffers['items']
            while buf:
                batch = buf[:self._max_size]
                data = self._data_parse.get_bytes(batch)
                self.send_data(
                    request_url,
                    data,
                    headers={'content-type': 'application/json'}
                )
                buf = buf[self._max_size:]
            self._async_buffers['items'] = buf
