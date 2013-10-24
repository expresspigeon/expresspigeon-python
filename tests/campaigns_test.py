import os
import unittest
from expresspigeon import ExpressPigeon
from tests import ExpressPigeonTest


class CampaignsTest(ExpressPigeonTest):
    def __request_hook__(self, request):
        super(CampaignsTest, self).request_hook(request)
        request.headers["Content-type"] = "text/html"

    def test_json_type(self):
        ExpressPigeon.request_hook = self.__request_hook__
        res = self.api.campaigns.send(list_id=-1, template_id=-1, name="", from_name="", reply_to="", subject="",
                                      google_analytics=False)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "required Content-type: application/json")

    def test_get_all_campaigns(self):
        res = self.api.campaigns.get_all()
        self.assertIsNotNone(res)
        self.assertIsInstance(res, list)

    def test_send_without_params(self):
        res = self.api.campaigns.send(list_id=-1, template_id=-1, name="", from_name="", reply_to="", subject="",
                                      google_analytics=False)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "required parameters: list_id, template_id, name, from_name, reply_to, subject, "
                                      "google_analytics")

    def test_send_with_bad_reply_to(self):
        res = self.api.campaigns.send(list_id=-1, template_id=-1, name="My Campaign", from_name="John", reply_to="j",
                                      subject="Hi", google_analytics=False)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "reply_to should be valid email address")

    def test_send_with_non_existent_template(self):
        res = self.api.campaigns.send(list_id=-1, template_id=-1, name="My Campaign", from_name="John",
                                      reply_to="j@j.j",
                                      subject="Hi", google_analytics=False)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "template=-1 is not found")

    def test_send_with_non_existent_list(self):
        res = self.api.campaigns.send(list_id=-1, template_id=347, name="My Campaign", from_name="John",
                                      reply_to="j@j.j",
                                      subject="Hi", google_analytics=False)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "list=-1 is not found")

    def test_send_with_disabled_list(self):
        res = self.api.campaigns.send(list_id=130, template_id=347, name="My Campaign", from_name="John",
                                      reply_to="j@j.j",
                                      subject="Hi", google_analytics=False)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "list=130 is disabled")

    def test_campaign_report(self):
        res = self.api.campaigns.report(-1)
        self.assertEqual(res.code, 404)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "campaign=-1 not found")

    def test_send_successful_campaign(self):
        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        self.api.contacts.upsert(list_resp.list.id, {"email": os.environ['EXPRESSPIGEON_API_USER']})
        res = self.api.campaigns.send(list_id=list_resp.list.id, template_id=347, name="My Campaign", from_name="John",
                                      reply_to=os.environ['EXPRESSPIGEON_API_USER'], subject="Hi",
                                      google_analytics=False)
        self.assertEqual(res.code, 200)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.message, "new campaign created successfully")
        self.assertIsNotNone(res.campaign_id)

        report = self.api.campaigns.report(res.campaign_id)
        self.assertEquals(report.delivered, 0)
        self.assertEquals(report.clicked, 0)
        self.assertEquals(report.opened, 0)
        self.assertEquals(report.spam, 0)
        self.assertEquals(report.in_transit, 1)
        self.assertEquals(report.unsubscribed, 0)
        self.assertEquals(report.bounced, 0)

        self.api.contacts.delete(os.environ['EXPRESSPIGEON_API_USER'], list_resp.list.id)
        self.api.lists.delete(list_resp.list.id)

    def test_schedule_campaign_with_bad_date(self):
        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        res = self.api.campaigns.schedule(list_id=list_resp.list.id, template_id=347, name="My Campaign", from_name="John",
                                          reply_to=os.environ['EXPRESSPIGEON_API_USER'], subject="Hi",
                                          google_analytics=False, schedule_for="2013-05-28")
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "schedule_for is not in ISO date format, example: 2013-05-28T17:19:50.779+0300")

        self.api.lists.delete(list_resp.list.id)

    def test_schedule_campaign_with_date_in_the_past(self):
        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        res = self.api.campaigns.schedule(list_id=list_resp.list.id, template_id=347, name="My Campaign", from_name="John",
                                          reply_to=os.environ['EXPRESSPIGEON_API_USER'], subject="Hi",
                                          google_analytics=False, schedule_for="2013-05-28T17:19:50.779+0300")
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "schedule_for should be in the future")

        self.api.lists.delete(list_resp.list.id)

if __name__ == '__main__':
    unittest.main()
