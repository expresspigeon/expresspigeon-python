import unittest
from tests import ExpressPigeonTest

class DictionariesTest(ExpressPigeonTest):
    def test_create_new_dictionaries(self):
        resp = self.api.dictionaries.create([{
            "name": "sandwich1",
            "values": {
                "name": "ORGANIC GRASS FED SIRLOIN",
                "price": "$7.00",
                "image": "http://yourdomain.com/contnet/sandwich1.png",
                "url": "http://yourdomain.com/sandwich1",
                "description": "certified organic grass fed sirloin, Swiss Gruy?re cheese, vine tomatoes, organic mixed greens, caramelized organic onions and housemade horseradish aioli on organic bretzel baguette"
                }
            },
            {
            "name": "sandwich2",
            "values": {
                "name": "ORGANIC ROASTED TOFU",
                "price": "$4.99",
                "image": "http://yourdomain.com/contnet/sandwich1.png",
                "url": "http://yourdomain.com/sandwich2",
                "description": "certified organic smoked turkey, local white cheddar, fresh organic apple crisps, organic mixed greens and housemade roasted pepper aioli on organic bretzel baguette"
                }
            }])
        self.assertEqual(resp.status, "success")
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.message, "dictionaries created/updated successfully")
        self.assertEqual(len(resp.ids), 2)
        
        dicts = self.api.dictionaries.find_all()
        self.assertEqual(len(dicts), 2)
        self.assertEqual(resp.ids.count(dicts[0].id), 1)
        self.assertEqual(resp.ids.count(dicts[1].id), 1)
        
        found = self.api.dictionaries.lookup(resp.ids[0])
        self.assertEqual(found.id, resp.ids[0])