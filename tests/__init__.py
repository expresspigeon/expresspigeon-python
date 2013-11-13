import base64
import email
import imaplib
import os
import unittest
import time
from expresspigeon import ExpressPigeon

try:
    from urllib import request as url_lib
except ImportError:
    import urllib2 as url_lib


class ExpressPigeonTest(unittest.TestCase):
    template_id = 347

    file_to_upload = "{0}{1}emails.csv".format(os.path.split(os.path.abspath(__file__))[0], os.path.sep)

    def request_hook(self, request):
        user_and_password = base64.b64encode("%s:%s".format(os.environ['EXPRESSPIGEON_USER'],
                                                            os.environ['EXPRESSPIGEON_PASSWORD']).encode("utf-8"))
        request.add_header('Authorization', 'Basic %s' % user_and_password)

    def setUp(self):
        ExpressPigeon.ROOT = os.environ['EXPRESSPIGEON_ROOT']
        ExpressPigeon.request_hook = self.request_hook
        self.api = ExpressPigeon()

    def wait_until(self, predicate, timeout, period=0.5, **kwargs):

        must_end = time.time() + timeout
        while time.time() < must_end:
            res = predicate(kwargs)
            if res:
                return res
            time.sleep(period)
        return None

    def format_date(self, date):
        return date.strftime('%Y-%m-%dT%H:%M:%S.') + date.strftime('%f')[:3] + date.strftime("%z")


class Gmail(object):
    def __extract_body__(self, payload):
        if isinstance(payload, str):
            return payload
        else:
            return '\n'.join([self.__extract_body__(part.get_payload()) for part in payload])

    def get_unseen(self):
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

                conn.store(num, '+FLAGS', '\\Seen')

            return messages
        finally:
            try:
                conn.close()
            except:
                pass
            conn.logout()

    def get_by_subject(self, kwargs):
        assert "subject" in kwargs
        subject = kwargs["subject"]
        conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        conn.login(os.environ['EXPRESSPIGEON_API_USER'], os.environ['EXPRESSPIGEON_API_PASSWORD'])
        conn.select("INBOX")
        email_ids = conn.search(None, '(SUBJECT "{0}")'.format(subject))[1][0].split(" ")

        if email_ids[0] == "":
            return None

        messages = []

        for email_id in email_ids:
            typ, msg_data = conn.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    messages.append({'subject': msg['subject'], 'body': self.__extract_body__(msg.get_payload())})

        return messages

    def delete_by_subject(self, subject):
        conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        conn.login(os.environ['EXPRESSPIGEON_API_USER'], os.environ['EXPRESSPIGEON_API_PASSWORD'])
        conn.select("INBOX")
        email_ids = conn.search(None, '(SUBJECT "{0}")'.format(subject))[1][0].split(" ")

        if len(email_ids) == 0:
            return False

        for email in email_ids:
            conn.store(email, '+FLAGS', '\\Deleted')

        return True if len(conn.search(None, '(SUBJECT "{0}")'.format(subject))[1][0].split(" ")) == 0 else False
