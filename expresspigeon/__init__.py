import os
import json
from collections import namedtuple
from expresspigeon.lists import Lists

try:
    from urllib import request as url_lib
except ImportError:
    import urllib2 as url_lib


class InvalidAuthKey(Exception):
    pass


class BadRequest(Exception):
    pass


class Forbidden(Exception):
    pass


class NotFound(Exception):
    pass


class InternalServerError(Exception):
    pass


ROOT = "https://api.expresspigeon.com/"

ERRORS = {400: BadRequest, 403: Forbidden, 404: NotFound, 500: InternalServerError}


class ExpressPigeon(object):

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

    def __getattr__(self, name):
        return (
            lambda endpoint, **kwargs: self.__call__(endpoint, name, **kwargs)
            if name in self.Request.METHODS
            else super(ExpressPigeon, self).__getattribute__(name)
        )

    def __call__(self, endpoint, method, **kwargs):
        content_type = kwargs["content_type"] if "content_type" in kwargs else "application/json"
        body = kwargs["body"] if "body" in kwargs else json.dumps(kwargs["params"] if "params" in kwargs else {})

        opener = url_lib.build_opener(url_lib.HTTPSHandler)
        req = self.Request(url=ROOT + endpoint,
                           method=method.upper(),
                           headers={"X-auth-key": self.auth_key, "Content-type": content_type},
                           data=body.encode("utf-8"))
        return json.loads(opener.open(req).read().decode("utf-8"), "UTF-8",
                          object_hook=lambda d: namedtuple('EpResponse', d.keys())(*d.values()))