import os
import json
from collections import namedtuple
from expresspigeon.autoresponders import AutoResponders
from expresspigeon.campaigns import Campaigns
from expresspigeon.contacts import Contacts
from expresspigeon.lists import Lists
from expresspigeon.messages import Messages
from expresspigeon.templates import Templates
from expresspigeon.dictionaries import Dictionaries

try:
    from urllib import request as url_lib
except ImportError:
    import urllib2 as url_lib


class InvalidAuthKey(Exception):
    pass


class ExpressPigeonException(Exception):
    pass


class ExpressPigeon(object):
    ROOT = "https://api.expresspigeon.com/"

    class Request(url_lib.Request):
        METHODS = ["get", "post", "put", "delete"]

        def __init__(self, url, method=None, headers=None, data=None, origin_req_host=None, unverifiable=False):
            if not headers:
                headers = {}
            url_lib.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)
            self.method = method

        def get_method(self):
            if self.method:
                return self.method

            return url_lib.Request.get_method(self)

    def __init__(self, auth_key=None):
        """ Initialize the ExpressPigeon API client.

        :param auth_key: ExpressPigeon API key.  If not provided, the API key will be acquired from
        the EXPRESSPIGEON_AUTH_KEY environment variable.
        :type auth_key: string

        :returns: ExpressPigeon object for query API
        :rtype: ExpressPigeon

        :raises: :py:class:`InvalidAuthKey`: if the ExpressPigeon API key not found
        """
        if auth_key is None:
            if 'EXPRESSPIGEON_AUTH_KEY' in os.environ:
                auth_key = os.environ['EXPRESSPIGEON_AUTH_KEY']
            else:
                raise InvalidAuthKey('You must provide a ExpressPigeon API key')

        self.auth_key = auth_key
        self.lists = Lists(self)
        self.contacts = Contacts(self)
        self.campaigns = Campaigns(self)
        self.messages = Messages(self)
        self.templates = Templates(self)
        self.auto_responders = AutoResponders(self)
        self.dictionaries = Dictionaries(self)

    def __getattr__(self, name):
        """
        This is metaprogramming trick to send get, post, put, delete requests implicitly
        """
        return (
            lambda endpoint, **kwargs: self.__send_request__(endpoint, name, **kwargs)
            if name in self.Request.METHODS
            else super(ExpressPigeon, self).__getattribute__(name)
        )

    def __send_request__(self, endpoint, method, **kwargs):
        content_type = kwargs["content_type"] if "content_type" in kwargs else "application/json"
        body = kwargs["body"] if "body" in kwargs else json.dumps(kwargs["params"] if "params" in kwargs else {})
        
        opener = url_lib.build_opener(url_lib.HTTPSHandler)

        req = self.Request(url=(self.ROOT if self.ROOT.endswith("/") else self.ROOT + "/") + endpoint,
                           method=method.upper(),
                           headers={"X-auth-key": self.auth_key, "Content-type": content_type, "User-Agent": "Mozilla/5.0"},
                           data=body.encode("utf-8"))

        self.request_hook(req)
        
        try:
            return json.loads(opener.open(req).read().decode("utf-8"), encoding="UTF-8",
                              object_hook=lambda d: namedtuple('EpResponse', d.keys())(*d.values()))
        except url_lib.HTTPError as e:
            return json.loads(e.fp.read().decode("utf-8"), encoding="UTF-8",
                              object_hook=lambda d: namedtuple('EpResponse', d.keys())(*d.values()))

    def read_stream(self, endpoint, **kwargs):
        opener = url_lib.build_opener(url_lib.HTTPSHandler)

        req = self.Request(url=(self.ROOT if self.ROOT.endswith("/") else self.ROOT + "/") + endpoint,
                           method="GET", headers={"X-auth-key": self.auth_key, "User-Agent": "Mozilla/5.0"})

        self.request_hook(req)

        try:
            return opener.open(req).read().decode("utf-8")
        except url_lib.HTTPError as e:
            return json.loads(e.fp.read().decode("utf-8"), encoding="UTF-8",
                              object_hook=lambda d: namedtuple('EpResponse', d.keys())(*d.values()))

    def request_hook(self, request):
        pass