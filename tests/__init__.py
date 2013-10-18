import base64
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
        self.gmail = Gmail()

    def wait_until(self, predicate, timeout, period=0.5):
        must_end = time.time() + timeout
        while time.time() < must_end:
            res = predicate()
            if res:
                return res
            time.sleep(period)
        return None


class Gmail(object):
    def __extract_body__(self, payload):
        if isinstance(payload, str):
            return payload
        else:
            return '\n'.join([self.__extract_body__(part.get_payload()) for part in payload])

    def get_unseen(self, removeAll=False):
        messages = []
        conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        conn.login(os.environ['EXPRESSPIGEON_API_USER'], os.environ['EXPRESSPIGEON_API_PASSWORD'])
        conn.select()
        typ, data = conn.search(None, 'unseen')
        try:
            for num in data[0].split():
                typ, msg_data = conn.fetch(num, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1])
                        messages.append({'subject': msg['subject'], 'body': self.__extract_body__(msg.get_payload())})

                if removeAll:
                    conn.store(num, '+FLAGS', '\\Deleted')

            return messages
        finally:
            try:
                conn.close()
            except:
                pass
            conn.logout()