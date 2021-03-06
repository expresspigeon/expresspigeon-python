import os
import datetime
import pytz
from tests import ExpressPigeonTest


class MessagesTest(ExpressPigeonTest):
    def test_sending_message_and_report_without_params(self):
        res = self.api.messages.send_message(template_id=-1, to="", reply_to="", from_name="", subject="")
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "Required fields: template_id, reply_to, from, to, and subject")

    def test_sending_message_and_report_with_wrong_email_in_to(self):
        res = self.api.messages.send_message(template_id=-1, to="e", reply_to="a@a.a", from_name="me", subject="Hi")
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "Email in the 'to' field is not valid. Please, see http://www.ietf.org/rfc/rfc822.txt and https://tools.ietf.org/html/rfc5322#section-3.4.1 for more detail.")

    def test_sending_message_and_report_with_wrong_email_in_reply_to(self):
        res = self.api.messages.send_message(template_id=-1, to="e@e.e", reply_to="a", from_name="me", subject="Hi")
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "Email in the 'reply_to' field is not valid. Please, see http://www.ietf.org/rfc/rfc822.txt and https://tools.ietf.org/html/rfc5322#section-3.4.1 for more detail.")

    def test_sending_message_and_report_with_wrong_template_id(self):
        res = self.api.messages.send_message(template_id=-1, to="e@e.e", reply_to="a@a.a", from_name="me", subject="Hi")
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "template=-1 not found")

    def test_sending_message_and_report(self):
        message_response = self.api.messages.send_message(template_id=self.template_id,
                                                          to=os.environ['EXPRESSPIGEON_API_USER'],
                                                          reply_to="a@a.a", from_name="me", subject="Hi",
                                                          merge_fields={"first_name": "Gleb"})
        self.assertEqual(message_response.code, 200)
        self.assertEqual(message_response.status, "success")
        self.assertEqual(message_response.message, "email queued")
        self.assertTrue(message_response.id is not None and message_response.id != "")

        report = self.api.messages.report(message_response.id)
        self.assertEquals(report.id, message_response.id)
        self.assertEquals(report.email, os.environ['EXPRESSPIGEON_API_USER'])
        self.assertTrue(report.in_transit is not None)

    def test_reports_with_bad_dates(self):
        res = self.api.messages.reports("abc", "")
        self.assertEquals(res.code, 400)
        self.assertEquals(res.status, "error")
        self.assertEquals(res.message, "invalid 'start_date' or 'end_date'")

    def test_reports_with_start_date_only(self):
        res = self.api.messages.reports("2013-03-16T11:22:23.210+0000", "")
        self.assertEquals(res.code, 400)
        self.assertEquals(res.status, "error")
        self.assertEquals(res.message, "'start_date' and 'end_date' should be provided together")

    def test_reports_with_end_date_only(self):
        res = self.api.messages.reports("", "2013-03-16T11:22:23.210+0000")
        self.assertEquals(res.code, 400)
        self.assertEquals(res.status, "error")
        self.assertEquals(res.message, "'start_date' and 'end_date' should be provided together")

    def test_sending_multiple_messages_and_get_reports(self):
        message_response = self.api.messages.send_message(template_id=self.template_id,
                                                          to=os.environ['EXPRESSPIGEON_API_USER'],
                                                          reply_to="a@a.a", from_name="me", subject="Hi",
                                                          merge_fields={"first_name": "Gleb"})
        self.assertEqual(message_response.code, 200)
        self.assertEqual(message_response.status, "success")
        self.assertEqual(message_response.message, "email queued")
        self.assertTrue(message_response.id is not None and message_response.id != "")

        message_response_2 = self.api.messages.send_message(template_id=self.template_id,
                                                            to=os.environ['EXPRESSPIGEON_API_USER'],
                                                            reply_to="a@a.a", from_name="me", subject="Hi 2",
                                                            merge_fields={"first_name": "Gleb"})
        self.assertEqual(message_response_2.code, 200)
        self.assertEqual(message_response_2.status, "success")
        self.assertEqual(message_response_2.message, "email queued")
        self.assertTrue(message_response_2.id is not None and message_response.id != "")

        report = self.__get_report_by_id__(message_response.id)

        self.assertEquals(report.id, message_response.id)
        self.assertEquals(report.email, os.environ['EXPRESSPIGEON_API_USER'])
        self.assertTrue(report.in_transit is not None)

        report2 = self.__get_report_by_id__(message_response_2.id)

        self.assertEquals(report2.id, message_response_2.id)
        self.assertEquals(report2.email, os.environ['EXPRESSPIGEON_API_USER'])
        self.assertTrue(report2.in_transit is not None)

    def test_sending_multiple_messages_and_get_reports_for_today(self):
        message_response = self.api.messages.send_message(template_id=self.template_id,
                                                          to=os.environ['EXPRESSPIGEON_API_USER'],
                                                          reply_to="a@a.a", from_name="me", subject="Hi",
                                                          merge_fields={"first_name": "Gleb"})                                          
        self.assertEqual(message_response.code, 200)
        self.assertEqual(message_response.status, "success")
        self.assertEqual(message_response.message, "email queued")
        self.assertTrue(message_response.id is not None and message_response.id != "")

        message_response_2 = self.api.messages.send_message(template_id=self.template_id,
                                                            to=os.environ['EXPRESSPIGEON_API_USER'],
                                                            reply_to="a@a.a", from_name="me", subject="Hi 2",
                                                            merge_fields={"first_name": "Gleb"})
        self.assertEqual(message_response_2.code, 200)
        self.assertEqual(message_response_2.status, "success")
        self.assertEqual(message_response_2.message, "email queued")
        self.assertTrue(message_response_2.id is not None and message_response.id != "")

        now = datetime.datetime.now(pytz.UTC)
        start = self.format_date(now - datetime.timedelta(hours=1))
        end = self.format_date(now + datetime.timedelta(hours=1))

        report = self.__get_report_by_id__(message_response.id, start_date=start, end_date=end)

        self.assertEquals(report.id, message_response.id)
        self.assertEquals(report.email, os.environ['EXPRESSPIGEON_API_USER'])
        self.assertTrue(report.in_transit is not None)

        report2 = self.__get_report_by_id__(message_response_2.id, start_date=start, end_date=end)

        self.assertEquals(report2.id, message_response_2.id)
        self.assertEquals(report2.email, os.environ['EXPRESSPIGEON_API_USER'])
        self.assertTrue(report2.in_transit is not None)
    
    def test_sending_bulk_messages(self):
        res = self.api.messages.send_message_bulk("{0}{1}bulk.zip".format(os.path.split(os.path.abspath(__file__))[0], os.path.sep))
        self.assertTrue('{"code":404,"message":"template=356646 not found","status":"error"}' in res)
        
    def test_sending_attachments(self):
        message_response = self.api.messages.send_message_attachment(template_id=self.template_id,
                                                          to=os.environ['EXPRESSPIGEON_API_USER'],
                                                          reply_to="a@a.a", from_name="me", subject="Hi",
                                                          merge_fields={"first_name": "Gleb"},
                                                          attachments=["{0}{1}bulk.zip".format(os.path.split(os.path.abspath(__file__))[0], os.path.sep), "{0}{1}emails.csv".format(os.path.split(os.path.abspath(__file__))[0], os.path.sep)])
        print(message_response.message)
        self.assertEqual(message_response.code, 200)
        self.assertEqual(message_response.status, "success")
        self.assertEqual(message_response.message, "email queued")
        self.assertTrue(message_response.id is not None and message_response.id != "")

    def __get_report_by_id__(self, message_id, start_date=None, end_date=None):
        reports = self.api.messages.reports() if start_date is None and end_date is None else \
            self.api.messages.reports(start_date, end_date)
        report = [r for r in reports if r.id == message_id]
        self.assertEquals(len(report), 1)
        return report[0]