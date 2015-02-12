import unittest
from tests import ExpressPigeonTest


class ContactsTest(ExpressPigeonTest):
    def test_contact_creation_without_contact_dict(self):
        res = self.api.contacts.upsert(-1, [{}])
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "email is required")

    def test_contact_creation_without_email(self):
        res = self.api.contacts.upsert(-1, [{"email": "",
                                             "first_name": "Marylin",
                                             "last_name": "Monroe"}])
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "email is required")

    def test_create_with_many_custom_fields(self):
        custom_fields = dict(("custom_field_{0}".format(i), "custom_value_{0}".format(i)) for i in range(1, 25, 1))
        res = self.api.contacts.upsert(-1, [
            {
                "email": "mary@e.e",
                "custom_fields": custom_fields,
            }
        ])
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "You cannot create more than 20 custom fields. Use one of the 'custom_fields'.")

    def test_create_non_existent_contact_without_list_id(self):
        res = self.api.contacts.upsert(-1, [{"email": "ee@e.e",
                                             "first_name": "Marylin",
                                             "last_name": "Monroe"}])
        self.assertEqual(res.code, 404)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "contact=ee@e.e not found")

    def test_create_with_suppressed_contact(self):
        list_response = self.api.lists.create("My List", "a@a.a", "a@a.a")
        self.assertEqual(list_response.code, 200)

        res = self.api.contacts.upsert(list_response.list.id, [{"email": "suppressed@e.e"}])
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "contact=suppressed@e.e is in suppress list")

    def test_create_list_with_contacts(self):
        list_response = self.api.lists.create("My List", "a@a.a", "a@a.a")
        self.assertEqual(list_response.code, 200)
        res = self.api.contacts.upsert(list_response.list.id, [{"email": "mary@e.e",
                                                                "custom_fields": {
                                                                    "custom_field_1": "custom_value_1",
                                                                }}])
        self.assertEqual(res.code, 200)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.message, "contacts created/updated successfully")

        self.assertEqual(res.contacts[0], "mary@e.e")

        self.api.lists.delete(list_response.list.id)

    def test_create_list_non_existent_custom_field(self):
        list_response = self.api.lists.create("My List", "a@a.a", "a@a.a")
        self.assertEqual(list_response.code, 200)
        res = self.api.contacts.upsert(list_response.list.id, [{"email": "mary@e.e",
                                                                "custom_fields": {
                                                                    "c": "c",
                                                                }}])
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "You cannot create more than 20 custom fields. Use one of the 'custom_fields'.")

        self.api.lists.delete(list_response.list.id)

    def test_export_contacts_from_list_without_list_id(self):
        res = self.api.lists.csv("-1")
        self.assertEqual(res.code, 404)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "list=-1 not found")

    def test_get_contacts_from_suppress_list(self):
        res = self.api.lists.csv("suppress_list").split('\n')
        self.assertEqual(len(res), 2)
        self.assertEqual(res[1], '"suppressed@e.e","Suppressed","Doe",,,,,,,,,,"UNSUBSCRIBED",,,,,,,,,,,,,,,,,,,,,')

    def test_get_single_contact(self):
        res = self.api.contacts.find_by_email("suppressed@e.e")
        self.assertEqual(res.email, "suppressed@e.e")

    def test_get_single_non_existent_contact(self):
        res = self.api.contacts.find_by_email("a@a.a")
        self.assertEqual(res.code, 404)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "contact=a@a.a not found")

    def test_update_contact(self):
        list_response = self.api.lists.create("My List", "a@a.a", "a@a.a")
        self.assertEqual(list_response.code, 200)

        res = self.api.contacts.upsert(list_response.list.id, [
            {
                "email": "mary@e.e",
                "first_name": "Mary",
                "last_name": "Doe"
            }
        ])
        self.assertEqual(res.code, 200)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.message, "contacts created/updated successfully")
        self.assertEqual(self.api.contacts.find_by_email("mary@e.e").last_name, "Doe")

        res = self.api.contacts.upsert(list_response.list.id, [
            {
                "email": "mary@e.e",
                "first_name": "Mary",
                "last_name": "Johns"
            }
        ])
        self.assertEqual(res.code, 200)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.message, "contacts created/updated successfully")
        self.assertEqual(self.api.contacts.find_by_email("mary@e.e").last_name, "Johns")

    def test_delete_contact_with_non_existent_email(self):
        res = self.api.contacts.delete("g@g.g")
        self.assertEqual(res.code, 404)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "contact=g@g.g not found")

    def test_delete_supressed_contact(self):
        res = self.api.contacts.delete("suppressed@e.e")
        self.assertEqual(res.code, 400)
        self.assertEqual(res.status, "error")
        self.assertEqual(res.message, "contact=suppressed@e.e is in suppress list")

    def test_delete_single_contact_from_all_lists(self):
        list_response = self.api.lists.create("My List", "a@a.a", "a@a.a")
        self.assertEqual(list_response.code, 200)

        self.api.contacts.upsert(list_response.list.id, [{"email": "mary@e.e"}])

        res = self.api.contacts.delete("mary@e.e")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.message, "contact=mary@e.e deleted successfully")

        self.api.lists.delete(list_response.list.id)

    def test_delete_single_contact_from_single_list(self):
        list_response = self.api.lists.create("My List", "a@a.a", "a@a.a")
        self.assertEqual(list_response.code, 200)

        list_response_2 = self.api.lists.create("My List2", "a@a.a", "a@a.a")
        self.assertEqual(list_response_2.code, 200)

        self.api.contacts.upsert(list_response.list.id, [{"email": "mary@e.e"}])
        self.api.contacts.upsert(list_response_2.list.id, [{"email": "mary@e.e"}])

        res = self.api.contacts.delete("mary@e.e", list_response.list.id)
        self.assertEqual(res.code, 200)
        self.assertEqual(res.status, "success")
        self.assertEqual(res.message, "contact=mary@e.e deleted successfully")

        contacts_exported = self.api.lists.csv(list_response.list.id).split("\n")
        self.assertEqual(len(contacts_exported), 1)
        contact_exported_2 = self.api.lists.csv(list_response_2.list.id).split("\n")
        self.assertEqual(len(contact_exported_2), 2)
        self.assertEqual(contact_exported_2[1], '"mary@e.e",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')

        self.api.lists.delete(list_response.list.id)
        self.api.lists.delete(list_response_2.list.id)
        self.api.contacts.delete("mary@e.e")


if __name__ == '__main__':
    unittest.main()
