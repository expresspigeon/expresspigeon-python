import os
from random import randint
import datetime
import re
import pytz
from tests import ExpressPigeonTest, Gmail

try:
    from urllib import request as url_lib
except ImportError:
    import urllib2 as url_lib


class IntegrationTest(ExpressPigeonTest):
    gmail = Gmail()

    def __emulate_browser_open_and_click__(self, body):
        body = body.replace("\r\n", "").replace("=3D", "").replace("=", "")
        open_url = 'http://open_tracker.expresspigeontest.com/opened?v=' + \
                   re.search('(?<=http://open_tracker.expresspigeontest.com/opened\?v).*?(?=")', body).group(0)
        click_url = 'http://clicks.expresspigeontest.com/click?v=' + \
                    re.search('(?<=http://clicks.expresspigeontest.com/click\?v).*?(?=">)', body).group(0)
        url_lib.urlopen(open_url).read()
        url_lib.urlopen(click_url).read()

    def test_campaign_sent(self):
        number = randint(0, 9999)
        subject = "Hi, #{0}".format(number)
        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        self.api.contacts.upsert(list_resp.list.id, {"email": os.environ['EXPRESSPIGEON_API_USER']})
        campaign = self.api.campaigns.send(list_id=list_resp.list.id, template_id=self.template_id,
                                           name="My Campaign#{0}".format(number), from_name="John",
                                           reply_to=os.environ['EXPRESSPIGEON_API_USER'], subject=subject,
                                           google_analytics=False)
        self.assertEqual(campaign.code, 200)
        self.assertEqual(campaign.status, "success")
        self.assertEqual(campaign.message, "new campaign created successfully")
        self.assertTrue(campaign.campaign_id is not None)

        email = self.wait_until(self.gmail.get_by_subject, 300, subject=subject)
        self.assertTrue(email is not None)
        self.assertEquals(len(email), 1)

        self.__emulate_browser_open_and_click__(email[0]['body'])
        self.__emulate_browser_open_and_click__(email[0]['body'])

        report = self.api.campaigns.report(campaign.campaign_id)
        self.assertTrue(report.in_transit == 1 or report.in_transit == 0)
        self.assertTrue(report.delivered == 1 or report.delivered == 0)
        self.assertTrue(report.opened == 1)
        self.assertTrue(report.clicked == 1)

        self.api.contacts.delete(os.environ['EXPRESSPIGEON_API_USER'])
        self.api.lists.delete(list_resp.list.id)

    def test_campaign_schedule(self):
        number = randint(0, 9999)
        subject = "Hi, #{0}".format(number)
        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        self.api.contacts.upsert(list_resp.list.id, {"email": os.environ['EXPRESSPIGEON_API_USER']})

        thirty_seconds_later = self.format_date(datetime.datetime.now(pytz.UTC) + datetime.timedelta(seconds=30))

        campaign = self.api.campaigns.schedule(list_id=list_resp.list.id, template_id=self.template_id,
                                               name="My Campaign#{0}".format(number), from_name="John",
                                               reply_to=os.environ['EXPRESSPIGEON_API_USER'], subject=subject,
                                               google_analytics=False, schedule_for=thirty_seconds_later)
        self.assertEqual(campaign.code, 200)
        self.assertEqual(campaign.status, "success")
        self.assertEqual(campaign.message, "new campaign created successfully")
        self.assertTrue(campaign.campaign_id is not None)

        email = self.wait_until(self.gmail.get_by_subject, 300, subject=subject)
        self.assertTrue(email is not None)
        self.assertEquals(len(email), 1)

        self.__emulate_browser_open_and_click__(email[0]['body'])
        self.__emulate_browser_open_and_click__(email[0]['body'])

        report = self.api.campaigns.report(campaign.campaign_id)
        self.assertTrue(report.in_transit == 0)
        self.assertTrue(report.delivered == 1)

        self.assertTrue(report.opened == 1)
        self.assertTrue(report.clicked == 1)

        self.api.contacts.delete(os.environ['EXPRESSPIGEON_API_USER'])
        self.api.lists.delete(list_resp.list.id)

    def test_transactional_email_sent(self):
        number = randint(0, 9999)
        subject = "Hi, #{0}".format(number)
        message_response = self.api.messages.send_message(template_id=self.template_id,
                                                          to=os.environ['EXPRESSPIGEON_API_USER'],
                                                          reply_to="a@a.a", from_name="me", subject=subject)
        self.assertEqual(message_response.code, 200)
        self.assertEqual(message_response.status, "success")
        self.assertEqual(message_response.message, "email queued")
        self.assertTrue(message_response.id is not None and message_response.id != "")

        email = self.wait_until(self.gmail.get_by_subject, 300, subject=subject)
        self.assertTrue(email is not None)
        self.assertEquals(len(email), 1)

        self.__emulate_browser_open_and_click__(email[0]['body'])
        self.__emulate_browser_open_and_click__(email[0]['body'])

        report = self.api.messages.report(message_response.id)
        self.assertTrue(report.in_transit is False)
        self.assertTrue(report.delivered is True)

        self.assertTrue(report.opened is True)
        self.assertTrue(report.clicked is True)
        self.assertTrue(len(report.urls) != 0)
        self.assertTrue(report.urls[0] == "http://www.expresspigeon.com")

    def test_upload_contacts_list(self):
        number = randint(0, 9999)
        list_name = "Upload_{0}".format(number)
        existing_list = self.api.lists.create(list_name, "Bob", "bob@acmetools.com")
        res = self.api.lists.upload(existing_list.list.id, self.file_to_upload)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.code, 200)
        self.assertTrue(res.upload_id is not None)

        res = self.api.lists.upload_status(res.upload_id)
        self.assertEqual(res.message, "upload complete")
        self.assertEqual(res.status, "complete")
        report = res.report
        self.assertEqual(report.suppressed, 0)
        self.assertEqual(report.skipped, 0)
        self.assertEqual(report.list_name, list_name)
        self.assertEqual(report.imported, 2)

        emails = self.wait_until(self.gmail.get_by_subject, 300, subject="Your contacts import was completed")
        self.assertTrue(emails is not None)
        for email in emails:
            if list_name in email['body']:
                return

        self.fail()

    def test_template_copy_with_merge_fields(self):
        number = randint(0, 9999)

        template = self.api.templates.copy(self.template_id, "New Template#{0}".format(number), merge_fields={
            "first_name": "<b>Gleb</b>"
        })
        self.assertEquals(template.code, 200)
        self.assertEquals(template.status, "success")
        self.assertEquals(template.message, "template copied successfully")
        self.assertTrue(template.template_id is not None)

        subject = "Hi, #{0}".format(number)
        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        self.api.contacts.upsert(list_resp.list.id, {"email": os.environ['EXPRESSPIGEON_API_USER']})
        res = self.api.campaigns.send(list_id=list_resp.list.id,
                                      template_id=template.template_id,
                                      name="My Campaign#{0}".format(number), from_name="John",
                                      reply_to=os.environ['EXPRESSPIGEON_API_USER'], subject=subject,
                                      google_analytics=False)
        self.assertEqual(res.code, 200)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.message, "new campaign created successfully")
        self.assertTrue(res.campaign_id is not None)

        res = self.wait_until(self.gmail.get_by_subject, 300, subject=subject)
        self.assertTrue(res is not None)
        self.assertEquals(len(res), 1)

        self.assertTrue("<b>Gleb</b>" in res[0]['body'])

        self.api.contacts.delete(os.environ['EXPRESSPIGEON_API_USER'])
        self.api.lists.delete(list_resp.list.id)

    def test_auto_responders(self):
        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        self.api.contacts.upsert(list_resp.list.id, {"email": os.environ['EXPRESSPIGEON_API_USER']})
        auto_responder = list(filter(lambda auto_responder: auto_responder.name == 'Test',
                                     self.api.auto_responders.find_all()))[0]
        try:
            self.assertEqual(self.api.lists.delete(list_resp.list.id).message,
                             "could not delete list={0}, it has dependent subscriptions and/or scheduled campaigns"
                                 .format(list_resp.list.id))

            old_report = self.api.auto_responders.report(auto_responder.auto_responder_id)[0]

            auto_responder_res = self.api.auto_responders.start(auto_responder.auto_responder_id,
                                                                os.environ['EXPRESSPIGEON_API_USER'])
            self.assertEquals(auto_responder_res.code, 200)
            self.assertEquals(auto_responder_res.status, "success")
            self.assertEquals(auto_responder_res.message,
                              "auto_responder={0} started successfully for contact={1}".format(
                                  auto_responder.auto_responder_id,
                                  os.environ['EXPRESSPIGEON_API_USER']))

            email = self.wait_until(self.gmail.get_by_subject, 300,
                                    subject=auto_responder.auto_responder_parts[0].subject)
            self.assertTrue(email is not None)
            self.__emulate_browser_open_and_click__(email[0]['body'])

            report = self.api.auto_responders.report(auto_responder.auto_responder_id)[0]
            self.assertEquals(report.delivered, old_report.delivered + 1)
            self.assertEquals(report.clicked, old_report.clicked + 1)
            self.assertEquals(report.opened, old_report.opened + 1)
        finally:
            self.api.contacts.delete(os.environ['EXPRESSPIGEON_API_USER'])
            self.api.lists.delete(list_resp.list.id)
            self.gmail.delete_by_subject(subject=auto_responder.auto_responder_parts[0].subject)
