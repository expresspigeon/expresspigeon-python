import os
from random import randint
from tests import ExpressPigeonTest, Gmail


class IntegrationTest(ExpressPigeonTest):

    gmail = Gmail()

    def test_campaign_sent(self):
        number = randint(0, 9999)
        subject = "Hi, #{0}".format(number)
        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        self.api.contacts.upsert(list_resp.list.id, {"email": os.environ['EXPRESSPIGEON_API_USER']})
        res = self.api.campaigns.send(list_id=list_resp.list.id, template_id=self.template_id,
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

        res = self.wait_until(self.gmail.get_by_subject, 300, subject=subject)
        self.assertTrue(res is not None)
        self.assertEquals(len(res), 1)

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
