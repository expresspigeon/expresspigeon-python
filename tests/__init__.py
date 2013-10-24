import base64
import logging
import os
import unittest
import imaplib
import email
import time
from expresspigeon import ExpressPigeon

try:
    from urllib import request as url_lib
except ImportError:
    import urllib2 as url_lib


class ExpressPigeonTest(unittest.TestCase):
    def request_hook(self, request):
        user_and_password = base64.b64encode("%s:%s".format(os.environ['EXPRESSPIGEON_USER'],
                                                            os.environ['EXPRESSPIGEON_PASSWORD']).encode("utf-8"))
        request.add_header('Authorization', 'Basic %s' % user_and_password)

    def setUp(self):
        ExpressPigeon.ROOT = os.environ['EXPRESSPIGEON_ROOT']
        ExpressPigeon.request_hook = self.request_hook
        self.api = ExpressPigeon()

    def wait_until(self, predicate, timeout, period=0.5):
        must_end = time.time() + timeout
        while time.time() < must_end:
            res = predicate()
            if res:
                return res
            time.sleep(period)
        return None
