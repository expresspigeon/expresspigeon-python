import os
from random import randint
from time import sleep
import unittest
import datetime
import pytz
from tests import ExpressPigeonTest


class ListsTest(ExpressPigeonTest):
    def test_create_and_delete_new_list(self):
        contact_list = self.api.lists.create(name="Active customers", from_name="Bob", reply_to="bob@acmetools.com")
        self.assertEqual(contact_list.status, "success")
        self.assertEqual(contact_list.code, 200)
        self.assertEqual(contact_list.message, "list={0} created/updated successfully".format(contact_list.list.id))
        self.assertEqual(contact_list.list.name, "Active customers")
        self.assertEqual(contact_list.list.from_name, "Bob")
        self.assertEqual(contact_list.list.reply_to, "bob@acmetools.com")
        self.assertEqual(contact_list.list.contact_count, 0)
        self.assertEqual(contact_list.list.zip, '220000')
        self.assertEqual(contact_list.list.state, "AL")
        self.assertEqual(contact_list.list.address1, "Coolman 11")
        self.assertEqual(contact_list.list.city, "Minsk")
        self.assertEqual(contact_list.list.country, "Belarus")
        self.assertEqual(contact_list.list.organization, "ExpressPigeon")

        res = self.api.lists.delete(contact_list.list.id)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.message, "list=%d deleted successfully" % contact_list.list.id)

    def test_update_existing_list(self):
        existing_list = self.api.lists.create("Update", "Bob", "bob@acmetools.com")
        res = self.api.lists.update(existing_list.list.id, {"name": "Updated Name", "from_name": "Bill"})
        self.assertEqual(res.status, "success")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.message, "list={0} created/updated successfully".format(res.list.id))
        self.assertEqual(res.list.name, "Updated Name")
        self.assertEqual(res.list.from_name, "Bill")
        self.api.lists.delete(res.list.id)

    def test_contacts_upload(self):
        # list name with last 4 digits from time
        list_name = "Upload_{0}".format(randint(0, 9999))
        existing_list = self.api.lists.create(list_name, "Bob", "bob@acmetools.com")
        res = self.api.lists.upload(existing_list.list.id, self.file_to_upload)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.code, 200)
        self.assertEquals(res.message, "file uploaded successfully")
        self.assertTrue(res.upload_id is not None)

        sleep(5)

        res = self.api.lists.upload_status(res.upload_id)
        self.assertEqual(res.message, "file upload completed")
        self.assertEqual(res.status, "success")
        self.assertEqual(res.code, 200)
        report = res.report
        self.assertTrue(report.completed)
        self.assertFalse(report.failed)
        self.assertEqual(report.suppressed, 0)
        self.assertEqual(report.skipped, 0)
        self.assertEqual(report.list_name, list_name)
        self.assertEqual(report.imported, 2)

    def test_upsert_list_with_non_existent_id(self):
        res = self.api.lists.update(-1, {"name": "Updated Name", "from_name": "Bill"})
        self.assertEqual(res.status, "error")
        self.assertEqual(res.code, 404)
        self.assertEqual(res.message, "list=-1 not found")

    def test_delete_list_with_non_existent_id(self):
        res = self.api.lists.delete(-1)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.code, 404)
        self.assertEqual(res.message, "list=-1 not found")

    def test_remove_disabled_list(self):
        res = self.api.lists.delete(130)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "could not delete list=130, list is disabled")

    def test_upload_without_id(self):
        res = self.api.lists.upload("", self.file_to_upload)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "you must provide list_id in URL")

    def test_upload_with_non_existent_id(self):
        res = self.api.lists.upload(-1, self.file_to_upload)
        self.assertEqual(res.code, 404)
        self.assertEqual(res.message, "list=-1 not found")

    def test_upload_status_without_upload_id(self):
        res = self.api.lists.upload_status("")
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "you must provide upload id")

    def test_enabled_list_removal(self):
        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        self.api.contacts.upsert(list_resp.list.id, [{"email": os.environ['EXPRESSPIGEON_API_USER']}])

        now = datetime.datetime.now(pytz.UTC)
        schedule = self.format_date(now + datetime.timedelta(hours=1))

        res = self.api.campaigns.schedule(list_id=list_resp.list.id, template_id=self.template_id, name="My Campaign",
                                          from_name="John",
                                          reply_to=os.environ['EXPRESSPIGEON_API_USER'], subject="Hi",
                                          google_analytics=False,
                                          schedule_for=schedule)
        self.assertEqual(res.code, 200)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.message, "new campaign created successfully")
        self.assertTrue(res.campaign_id is not None)

        res = self.api.lists.delete(list_resp.list.id)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message,
                         "could not delete list={0}, list has scheduled campaigns".format(
                             list_resp.list.id))

    def test_export_csv(self):
        list_response = self.api.lists.create("My List", "a@a.a", "a@a.a")
        self.assertEqual(list_response.code, 200)

        contacts_response = self.api.contacts.upsert(list_response.list.id, [{"email": "mary@a.a"}])
        self.assertEqual(contacts_response.code, 200)

        res = self.api.lists.csv(list_response.list.id).split("\n")
        self.assertEquals(len(res), 2)
        headers = '"Email", "First name", "Last name", "City", "Phone", "Company", "Title", "Address 1", "Address 2", ' \
                  '"State", "Zip", "Country", "Date of birth", "custom_field_1", "custom_field_10", "custom_field_11", ' \
                  '"custom_field_12", "custom_field_13", "custom_field_18", "custom_field_19", "custom_field_2", ' \
                  '"custom_field_20", "custom_field_21", "custom_field_22", "custom_field_23", "custom_field_24", ' \
                  '"custom_field_3", "custom_field_4", "custom_field_5", "custom_field_6", "custom_field_7", ' \
                  '"custom_field_8", "custom_field_9"'
        self.assertEquals(res[0], headers)
        self.assertEquals(res[1], '"mary@a.a",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')

        self.api.lists.delete(list_response.list.id)
        self.api.contacts.delete("mary@a.a")


if __name__ == '__main__':
    unittest.main()
