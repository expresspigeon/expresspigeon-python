import os
import unittest
import time
from tests import ExpressPigeonTest


class ListsTest(ExpressPigeonTest):

    def test_create_new_list(self):
        res = self.api.lists.create(name="Active customers", from_name="Bob", reply_to="bob@acmetools.com")
        self.assertEqual(res.status, "success")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.list.name, "Active customers")
        self.assertEqual(res.list.from_name, "Bob")
        self.assertEqual(res.list.reply_to, "bob@acmetools.com")
        self.assertEqual(res.list.contact_count, 0)
        self.assertEqual(res.list.zip, '220000')
        self.assertEqual(res.list.state, "AL")
        self.assertEqual(res.list.address1, "Coolman 11")
        self.assertEqual(res.list.city, "Minsk")
        self.assertEqual(res.list.country, "Belarus")
        self.assertEqual(res.list.organization, "ExpressPigeon")

    def test_delete_all_lists(self):
        lists = self.api.lists.get_all()
        for contact_list in lists:
            res = self.api.lists.delete(contact_list.id)
            self.assertEqual(res.status, "success")
            self.assertEqual(res.code, 200)
            self.assertEqual(res.message, "list=%d deleted successfully" % contact_list.id)
        self.assertEqual(len(self.api.lists.get_all()), 0)

    def test_update_existing_list(self):
        existing_list = self.api.lists.create("Update", "Bob", "bob@acmetools.com")
        res = self.api.lists.update(existing_list.list.id, {"name": "Updated Name", "from_name": "Bill"})
        self.assertEqual(res.status, "success")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.list.name, "Updated Name")
        self.assertEqual(res.list.from_name, "Bill")
        self.api.lists.delete(res.list.id)

    def test_contacts_upload(self):
        file_to_upload = os.path.split(os.path.abspath(__file__))[0] + os.path.sep + "emails.csv"
        # list name with last 4 digits from time
        list_name = "Upload_{0}".format(str(round(time.time() * 1000))[-4:])
        existing_list = self.api.lists.create(list_name, "Bob", "bob@acmetools.com")
        res = self.api.lists.upload(existing_list.list.id, file_to_upload)
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

        messages = self.wait_until(lambda: self.gmail.get_unseen(), timeout=60)
        if messages:
            message = [m for m in messages if list_name in m["body"]]
            self.assertEqual(len(message), 1)
            self.assertEqual(message[0]["subject"], "Your contacts import was completed")
            self.assertTrue("Contact upload report" in message[0]["body"])
            self.api.lists.delete(existing_list.list.id)
        else:
            self.fail("Cannot read Gmail messages")

if __name__ == '__main__':
    unittest.main()
