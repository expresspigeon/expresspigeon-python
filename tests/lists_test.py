import os
from random import randint
import unittest
from tests import ExpressPigeonTest


class ListsTest(ExpressPigeonTest):
    file_to_upload = "{0}{1}emails.csv".format(os.path.split(os.path.abspath(__file__))[0], os.path.sep)

    def test_create_new_list(self):
        res = self.api.lists.create(name="Active customers", from_name="Bob", reply_to="bob@acmetools.com")
        self.assertEqual(res.status, "success")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.message, "list={0} created/updated successfully".format(res.list.id))
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
        lists = self.api.lists.find_all()
        for contact_list in lists:
            if contact_list.name != 'Disabled list':
                res = self.api.lists.delete(contact_list.id)
                self.assertEqual(res.status, "success")
                self.assertEqual(res.code, 200)
                self.assertEqual(res.message, "list=%d deleted successfully" % contact_list.id)
        self.assertEqual(len(self.api.lists.find_all()), 1)

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
        self.assertTrue(res.upload_id is not None)

        res = self.api.lists.upload_status(res.upload_id)
        self.assertEqual(res.message, "upload complete")
        self.assertEqual(res.status, "complete")
        report = res.report
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

    def enabled_list_removal(self):
        pass #TODO

    def test_remove_disabled_list(self):
        res = self.api.lists.delete(130)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "could not delete disabled list=130")

    def test_upload_without_id(self):
        res = self.api.lists.upload("", self.file_to_upload)
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "you must provide list_id in URL")

    def test_upload_with_non_existen_id(self):
        res = self.api.lists.upload(-1, self.file_to_upload)
        self.assertEqual(res.code, 404)
        self.assertEqual(res.message, "list=-1 not found")

    def test_upload_status_without_upload_id(self):
        res = self.api.lists.upload_status("")
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "you must provide upload id")


if __name__ == '__main__':
    unittest.main()
