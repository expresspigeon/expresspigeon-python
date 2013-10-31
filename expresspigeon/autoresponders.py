class Autoresponders(object):
    """Autoresponders endpoint
    """

    endpoint = "auto_responders"

    def __init__(self, ep):
        self.ep = ep

    def start(self, autoresponder_id, email):
        """ This feature allow developers to start autoresponder for a contact.

        :param autoresponder_id: autoresponder id to be started for a contact
        :type autoresponder_id: int

        :param email: contact email
        :type email: str

        :returns: EpResponse with message about autoresponder start
        :rtype: EpResponse
        """
        return self.ep.post("{0}/{1}/start".format(self.endpoint, autoresponder_id), params={"email": email})