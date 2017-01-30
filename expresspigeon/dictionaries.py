import json

class Dictionaries(object):
    """
    Dictionaries endpoint
    """

    endpoint = "dictionaries"

    def __init__(self, ep):
        self.ep = ep
        
    def find_all(self):
        """ Query all dictionaries

        :returns: List of JSON of all dictionaries for user
        :rtype: EpResponse
        """

        return self.ep.get(self.endpoint)
    
    def lookup(self, dict_id):
        """ Lookup a single dictionary

        :param dict_id: is a dictionary ID
        :type campaign_id: long

        :returns: information dict, e.g.:
        {
            "id":1,
            "values":[
                {"name":"product1","value":"Swing set"},
                {"name":"product2","value":"Weber grill"},
                {"name":"product3","value":"IPhone"},
                {"name":"product4","value":"Eye glasses"},
                {"name":"sale1","value":"30% off"},
                {"name":"sale2","value":"50% off"}],
            "updated_at":"2014-05-14T21:58:31.000+0000",
            "name":"dict1",
            "created_at":"2014-05-14T21:58:31.000+0000"
        }
        :rtype: EpResponse
        """

        return self.ep.get("{0}/{1}".format(self.endpoint, dict_id))
    
    def create(self, dictionaries):
        """ JSON document represents a list of dictionaries to be created.
        You can create multiple dictionaries in a single API call..

        :param dictionaries: List of dictionaries describes new dictionaries.
        :type contacts: list

        :returns: JSON response with dictionaries' IDs
        :rtype: EpResponse
        """
        
        return self.ep.post(self.endpoint, params=dictionaries)