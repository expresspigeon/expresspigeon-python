import os
import unittest
from datetime import datetime
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
        # we know there are 2 campaigns at least
        res = self.api.campaigns.get_all()
        self.assertTrue(res is not None)
        self.assertTrue(isinstance(res, list))
        self.assertTrue(len(res) > 1)

        json = ('from_name', 'name', 'template_id', 'template_name', 'list_id', 'send_time', 'reply_to', 'total', 'id', 'subject')
        self.assertTrue(sorted(res[0]._fields) == sorted(json))

        start_date = datetime.strptime(res[0].send_time, "%Y-%m-%dT%H:%M:%S.%f+0000")
        end_date = datetime(start_date.year + int(start_date.month / 12), int((start_date.month % 12) + 1), 1)

        from_id = res[0].id

        dates_res = self.api.campaigns.get_all(
            start_date.strftime("%Y-%m-%dT%H:%M:%S.%f+0000"),
            end_date.strftime("%Y-%m-%dT%H:%M:%S.%f+0000"),
            from_id)
        self.assertTrue(dates_res is not None)
        self.assertTrue(isinstance(dates_res, list))
        self.assertTrue(len(dates_res) > 0)

        second_campaign = [c for c in dates_res if c.id == res[1].id]
        self.assertTrue(second_campaign[0] == res[1])

        first_campaign = [c for c in dates_res if c.id == res[0].id]
        self.assertFalse(len(first_campaign))

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
        res = self.api.campaigns.send(list_id=-1, template_id=self.template_id, name="My Campaign", from_name="John",
                                      reply_to="j@j.j",
                                      subject="Hi", google_analytics=False)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "list=-1 is not found")

    def test_send_with_disabled_list(self):
        res = self.api.campaigns.send(list_id=130, template_id=self.template_id, name="My Campaign", from_name="John",
                                      reply_to="j@j.j",
                                      subject="Hi", google_analytics=False)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "list=130 is disabled")

    def test_campaign_report_for_non_existent_campaign(self):
        res = self.api.campaigns.report(-1)
        self.assertEqual(res.code, 404)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "campaign=-1 not found")

    def test_send_successful_campaign(self):
        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        self.api.contacts.upsert(list_resp.list.id, {"email": os.environ['EXPRESSPIGEON_API_USER']})
        res = self.api.campaigns.send(list_id=list_resp.list.id, template_id=self.template_id, name="My Campaign",
                                      from_name="John",
                                      reply_to=os.environ['EXPRESSPIGEON_API_USER'], subject="Hi",
                                      google_analytics=False)
        self.assertEqual(res.code, 200)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.message, "new campaign created successfully")
        self.assertTrue(res.campaign_id is not None)

        report = self.api.campaigns.report(res.campaign_id)
        self.assertTrue(report.delivered == 0 or report.delivered == 1)
        self.assertEquals(report.clicked, 0)
        self.assertEquals(report.opened, 0)
        self.assertEquals(report.spam, 0)
        self.assertTrue(report.in_transit == 1 or report.in_transit == 0)
        self.assertEquals(report.unsubscribed, 0)
        self.assertEquals(report.bounced, 0)

        bounced = self.api.campaigns.bounced(res.campaign_id)
        unsubscribed = self.api.campaigns.unsubscribed(res.campaign_id)
        spam = self.api.campaigns.spam(res.campaign_id)
        self.assertTrue(len(bounced) == 0 and len(unsubscribed) == 0 and len(spam) == 0)

        self.api.contacts.delete(os.environ['EXPRESSPIGEON_API_USER'], list_resp.list.id)
        self.api.lists.delete(list_resp.list.id)

    def test_schedule_campaign_with_bad_date(self):
        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        res = self.api.campaigns.schedule(list_id=list_resp.list.id, template_id=self.template_id, name="My Campaign",
                                          from_name="John",
                                          reply_to=os.environ['EXPRESSPIGEON_API_USER'], subject="Hi",
                                          google_analytics=False, schedule_for="2013-05-28")
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "schedule_for is not in ISO date format, example: 2013-05-28T17:19:50.779+0300")

        self.api.lists.delete(list_resp.list.id)

    def test_schedule_campaign_with_date_in_the_past(self):
        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        res = self.api.campaigns.schedule(list_id=list_resp.list.id, template_id=self.template_id, name="My Campaign",
                                          from_name="John",
                                          reply_to=os.environ['EXPRESSPIGEON_API_USER'], subject="Hi",
                                          google_analytics=False, schedule_for="2013-05-28T17:19:50.779+0300")
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "schedule_for should be in the future")

        self.api.lists.delete(list_resp.list.id)


if __name__ == '__main__':
    unittest.main()
