# -*- coding: utf-8 -*-

import time


class CustomEventMessage(object):
    def __init__(self, event_time, event_name, login_user_key, login_user_id, anonymous_id, attributes):
        self.event_type = "CUSTOM"  # 1
        self.event_time = event_time
        self.event_name = event_name
        self.anonymous_id = anonymous_id
        self.login_user_key = login_user_key
        self.login_user_id = login_user_id
        self.attributes = attributes

    class EventBuilder(object):
        def __init__(self):
            self.event_time = int(time.time() * 1000)
            self.event_name = None
            self.anonymous_id = None
            self.login_user_key = None
            self.login_user_id = None
            self.attributes = None
            pass

        def set_event_time(self, timestamp):
            if timestamp is not None:
                self.event_time = timestamp
            return self

        def set_event_name(self, name):
            self.event_name = name
            return self

        def set_anonymous_id(self, device_id):
            self.anonymous_id = device_id
            return self

        def set_login_user(self, user_key=None, user_id=None):
            self.login_user_id = user_id
            self.login_user_key = user_key
            return self

        def set_login_user_key(self, user_key):
            self.login_user_key = user_key
            return self

        def set_login_user_id(self, user_id):
            self.login_user_id = user_id
            return self

        def add_attribute(self, key, value):
            if self.attributes is None:
                self.attributes = {}
            self.attributes[key] = value
            return self

        def set_attributes(self, map):
            self.attributes = map
            return self

        def build(self):
            return CustomEventMessage(self.event_time, self.event_name,
                                      self.login_user_key, self.login_user_id,
                                      self.anonymous_id,
                                      self.attributes)


class UserLoginMessage(object):
    def __init__(self, login_user_key, login_user_id, event_time, anonymous_id, attributes):
        self.event_type = "LOGIN_USER_ATTRIBUTES"  # 3
        self.login_user_key = login_user_key
        self.login_user_id = login_user_id
        self.event_time = event_time
        self.anonymous_id = anonymous_id
        self.attributes = attributes

    class UserBuilder(object):
        def __init__(self):
            self.event_time = int(time.time() * 1000)
            self.anonymous_id = None
            self.login_user_key = None
            self.login_user_id = None
            self.attributes = None

        def set_event_time(self, timestamp):
            self.event_time = timestamp
            return self

        def set_anonymous_id(self, device_id):
            self.anonymous_id = device_id
            return self

        def set_login_user(self, user_key=None, user_id=None):
            self.login_user_id = user_id
            self.login_user_key = user_key
            return self

        def set_login_user_key(self, user_key):
            self.login_user_key = user_key
            return self

        def set_login_user_id(self, user_id):
            self.login_user_id = user_id
            return self

        def add_attribute(self, key, value):
            if self.attributes is None:
                self.attributes = {}
            self.attributes[key] = value
            return self

        def set_attributes(self, map):
            self.attributes = map
            return self

        def build(self):
            return UserLoginMessage(self.login_user_key, self.login_user_id,
                                    self.event_time, self.anonymous_id,
                                    self.attributes)


class ItemMessage(object):
    def __init__(self, item_key, item_id, attrs=None):
        self.key = item_key
        self.id = item_id
        self.attrs = attrs

    class ItemBuilder(object):
        def __init__(self):
            self.id = None
            self.key = None
            self.attrs = None

        def set_item_id(self, item_id):
            self.id = item_id
            return self

        def set_item_key(self, item_key):
            self.key = item_key
            return self

        def add_attribute(self, key, value):
            if self.attrs is None:
                self.attrs = {}
            self.attrs[key] = value
            return self

        def set_attributes(self, map):
            self.attrs = map
            return self

        def build(self):
            return ItemMessage(self.key, self.id, self.attrs)
