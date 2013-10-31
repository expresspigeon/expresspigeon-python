import os
from tests import ExpressPigeonTest


class CampaignsTest(ExpressPigeonTest):
    def test_autoresponder_start(self):
        res = self.api.autoresponders.start(9, os.environ['EXPRESSPIGEON_API_USER'])
        self.assertEquals(res.code, 200)
        self.assertEquals(res.status, "success")
        self.assertEquals(res.message, "auto_responder=9 started successfully for contact={0}".format(
            os.environ['EXPRESSPIGEON_API_USER']))
