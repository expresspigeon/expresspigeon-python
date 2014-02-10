class AutoResponders(object):
    """AutoResponders endpoint
    """

    endpoint = "auto_responders"

    def __init__(self, ep):
        self.ep = ep

    def start(self, autoresponder_id, email):
        """ This feature allow developers to start auto responder for a contact.

        :param autoresponder_id: auto responder id to be started for a contact
        :type autoresponder_id: int

        :param email: contact email
        :type email: str

        :returns: EpResponse with message about autoresponder start
        :rtype: EpResponse
        """
        return self.ep.post("{0}/{1}/start".format(self.endpoint, autoresponder_id), params={"email": email})

    def stop(self, autoresponder_id, email):
        """ This feature allow developers to stop auto responder for a contact.

        :param autoresponder_id: auto responder id to be stopped for a contact
        :type autoresponder_id: int

        :param email: contact email
        :type email: str

        :returns: EpResponse with message about autoresponder stop
        :rtype: EpResponse
        """
        return self.ep.post("{0}/{1}/stop".format(self.endpoint, autoresponder_id), params={"email": email})

    def find_all(self):
        """ Returns all auto responders.

        :returns: list of auto responders, e.g.
        [
            {
                "auto_responder_parts": [
                    {
                        "auto_responder_part_id": 9,
                        "subject": "Test autoresponder",
                        "template_id": 347
                    }
                ],
                "name": "Test",
                "auto_responder_id": 9
            }
        ]
        :rtype: list
        """

        return self.ep.get(self.endpoint)

    def report(self, autoresponder_id):
        """ Returns report for auto responder

        :param autoresponder_id: auto responder id the report is generated for
        :type autoresponder_id: long

        :returns: list of EpResponse with report dict, e.g.
        [{delivered=4, clicked=0, opened=0, spam=0, in_transit=0, unsubscribed=0, bounced=0, auto_responder_part_id=9}]
        :rtype: list of EpResponse
        """

        return self.ep.get("{0}/{1}".format(self.endpoint, autoresponder_id))

    def bounced(self, autoresponder_id, auto_responder_part_id):
        """ Returns a list of object(s) with email and id of bounced contacts
        associated with given autoresponder part.

        :param autoresponder_id: auto responder id the bounced contacts are found for
        :type autoresponder_id: long

        :param auto_responder_part_id: autoresponder part id the bounced contacts are found for
        :type auto_responder_part_id: long

        :returns: list of of object(s) with email and id
        :rtype: list
        """
        return self.ep.get("{0}/{1}/{2}/bounced".format(self.endpoint, autoresponder_id, auto_responder_part_id))

    def unsubscribed(self, autoresponder_id, auto_responder_part_id):
        """ Returns an array of object(s) with email and id of unsubscribed contacts
        associate with this autoresponder part.

        :param autoresponder_id: auto responder id the unsubscribed contacts are found for
        :type autoresponder_id: long

        :param auto_responder_part_id: autoresponder part id the bounced contacts are found for
        :type auto_responder_part_id: long

        :returns: list of contacts ids
        :rtype: list
        """

        return self.ep.get("{0}/{1}/{2}/unsubscribed".format(self.endpoint, autoresponder_id, auto_responder_part_id))

    def spam(self, autoresponder_id, auto_responder_part_id):
        """ Returns an array of object(s) with email and id of spam contacts associated with this autoresponder part.

        :param autoresponder_id: auto responder id the spam contacts are found for
        :type autoresponder_id: long

        :param auto_responder_part_id: autoresponder part id the bounced contacts are found for
        :type auto_responder_part_id: long

        :returns: list of contacts ids
        :rtype: list
        """

        return self.ep.get("{0}/{1}/{2}/spam".format(self.endpoint, autoresponder_id, auto_responder_part_id))