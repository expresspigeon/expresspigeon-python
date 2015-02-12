from tests import ExpressPigeonTest


class TemplatesTest(ExpressPigeonTest):
    def test_template_copy(self):
        res = self.api.templates.copy(self.template_id, "New Template", merge_fields={
            "menu": "<table class='report'><tr><td>Burger:</td></tr><tr>$9.99<td></td></tr></table>"
        })
        self.assertEquals(res.code, 200)
        self.assertEquals(res.status, "success")
        self.assertEquals(res.message, "template copied successfully")
        self.assertTrue(res.template_id is not None)

    def test_template_copy_without_name(self):
        res = self.api.templates.copy(self.template_id, "")
        self.assertEquals(res.code, 400)
        self.assertEquals(res.status, "error")
        self.assertEquals(res.message, "name is required")

    def test_template_copy_with_bad_template_id(self):
        res = self.api.templates.copy(-1, "My Name")
        self.assertEquals(res.code, 404)
        self.assertEquals(res.status, "error")
        self.assertEquals(res.message, "template=-1 not found")
