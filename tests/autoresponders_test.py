import os
from tests import ExpressPigeonTest


class AutoRespondersTest(ExpressPigeonTest):
    def test_get_all_auto_responders(self):
        auto_responders = self.api.auto_responders.find_all()
        self.assertEquals(len(auto_responders), 3)

    def test_auto_responder_start_stop(self):
        auto_responder = list(filter(lambda auto_responder: auto_responder.name == 'Test',
                                     self.api.auto_responders.find_all()))[0]

        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        self.api.contacts.upsert(list_resp.list.id, {"email": os.environ['EXPRESSPIGEON_API_USER']})

        res = self.api.auto_responders.start(auto_responder.auto_responder_id, os.environ['EXPRESSPIGEON_API_USER'])
        self.assertEquals(res.code, 200)
        self.assertEquals(res.status, "success")
        self.assertEquals(res.message, "auto_responder={0} started successfully for contact={1}".format(
            auto_responder.auto_responder_id,
            os.environ['EXPRESSPIGEON_API_USER']))

        res = self.api.auto_responders.stop(auto_responder.auto_responder_id, os.environ['EXPRESSPIGEON_API_USER'])
        self.assertEquals(res.code, 200)
        self.assertEquals(res.status, "success")
        self.assertEquals(res.message, "auto_responder={0} stopped successfully for contact={1}".format(
            auto_responder.auto_responder_id,
            os.environ['EXPRESSPIGEON_API_USER']))

        self.api.contacts.delete(os.environ['EXPRESSPIGEON_API_USER'])
        self.api.lists.delete(list_resp.list.id)

    def test_start_unknown_auto_responder(self):
        res = self.api.auto_responders.start(-1, "")
        self.assertEquals(res.code, 404)
        self.assertEquals(res.status, "error")
        self.assertEquals(res.message, "auto_responder=-1 not found")

    def test_start_disabled_auto_responder(self):
        auto_responder = list(filter(lambda auto_responder: auto_responder.name == 'Disabled Autoresponder',
                                     self.api.auto_responders.find_all()))[0]

        res = self.api.auto_responders.start(auto_responder.auto_responder_id, "")
        self.assertEquals(res.code, 400)
        self.assertEquals(res.status, "error")
        self.assertEquals(res.message, "auto_responder={0} disabled".format(auto_responder.auto_responder_id))

    def test_start_without_email(self):
        auto_responder = list(filter(lambda auto_responder: auto_responder.name == 'Test',
                                     self.api.auto_responders.find_all()))[0]

        res = self.api.auto_responders.start(auto_responder.auto_responder_id, "")
        self.assertEquals(res.code, 400)
        self.assertEquals(res.status, "error")
        self.assertEquals(res.message, "'email' required")

    def test_start_with_non_existent_email(self):
        auto_responder = list(filter(lambda auto_responder: auto_responder.name == 'Test',
                                     self.api.auto_responders.find_all()))[0]

        res = self.api.auto_responders.start(auto_responder.auto_responder_id, "non_existent_email@e.e")
        self.assertEquals(res.code, 404)
        self.assertEquals(res.status, "error")
        self.assertEquals(res.message, "contact=non_existent_email@e.e not found")

    def test_start_without_newsletter(self):
        auto_responder = list(filter(lambda auto_responder: auto_responder.name == 'No newsletter',
                                     self.api.auto_responders.find_all()))[0]

        list_resp = self.api.lists.create("My list", "John", os.environ['EXPRESSPIGEON_API_USER'])
        self.api.contacts.upsert(list_resp.list.id, {"email": os.environ['EXPRESSPIGEON_API_USER']})

        res = self.api.auto_responders.start(auto_responder.auto_responder_id, os.environ['EXPRESSPIGEON_API_USER'])
        self.assertEquals(res.code, 400)
        self.assertEquals(res.status, "error")
        self.assertEquals(res.message, "auto_responder={0} does not have any newsletters".format(auto_responder.auto_responder_id))

        self.api.contacts.delete(os.environ['EXPRESSPIGEON_API_USER'])
        self.api.lists.delete(list_resp.list.id)


    def test_report_for_unknown_auto_responder(self):
        res = self.api.auto_responders.report(-1)
        self.assertEquals(res.code, 404)
        self.assertEquals(res.status, "error")
        self.assertEquals(res.message, "auto_responder=-1 not found")

    def test_report(self):
        auto_responder = self.api.auto_responders.find_all()[0]
        res = self.api.auto_responders.report(auto_responder.auto_responder_id)[0]
        self.assertEquals(res.auto_responder_part_id, auto_responder.auto_responder_id)
        self.assertTrue(res.delivered is not None)
        self.assertTrue(res.clicked is not None)
        self.assertTrue(res.opened is not None)
        self.assertTrue(res.spam is not None)
        self.assertTrue(res.in_transit is not None)
        self.assertTrue(res.unsubscribed is not None)
        self.assertTrue(res.bounced is not None)

    def test_bounced(self):
        auto_responder = self.api.auto_responders.find_all()[0]
        auto_responder_parts = auto_responder.auto_responder_parts[0]
        res = self.api.auto_responders.bounced(auto_responder.auto_responder_id,
                                               auto_responder_parts.auto_responder_part_id)
        self.assertEquals(len(res), 0)

    def test_spam(self):
        auto_responder = self.api.auto_responders.find_all()[0]
        auto_responder_parts = auto_responder.auto_responder_parts[0]
        res = self.api.auto_responders.spam(auto_responder.auto_responder_id,
                                            auto_responder_parts.auto_responder_part_id)
        self.assertEquals(len(res), 0)

    def test_unsubscribed(self):
        auto_responder = self.api.auto_responders.find_all()[0]
        auto_responder_parts = auto_responder.auto_responder_parts[0]
        res = self.api.auto_responders.unsubscribed(auto_responder.auto_responder_id,
                                                    auto_responder_parts.auto_responder_part_id)
        self.assertEquals(len(res), 0)