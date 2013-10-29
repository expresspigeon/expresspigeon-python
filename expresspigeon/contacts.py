class Contacts(object):
    """Contacts endpoint
    """
    endpoint = "contacts"

    def __init__(self, ep):
        self.ep = ep

    def upsert(self, list_id, contact):
        """ JSON document represents a contact to be created or updated.
        The email field is required.
        When updating a contact, list_id is optional,
        since the contact is uniquely identified by email across all lists.

        :param list_id: Contact list ID the contact will be added to
        :type list_id: long

        :param contact: Dictionary describes new contact. The "email" field is required.
        :type contact: dict
        """
        return self.ep.post(self.endpoint, params={"list_id": list_id, "contact": contact})

    def find_by_email(self, email):
        """ Returns a single contact by email address.

        :param email: Email of contact to be selected.
        :type email: str
        """

        return self.ep.get("{0}?email={1}".format(self.endpoint, email))

    def delete(self, email, list_id=None):
        """ Delete single contact. If list_id is not provided, contact will be deleted from system.

        :param email: contact email to be deleted.
        :type email: str

        :param list_id: list id to remove contact from, if not provided, contact will be deleted from system.
        :type list_id: long

        """

        query = "{0}?email={1}".format(self.endpoint, email) if list_id is None \
            else "{0}?email={1}&list_id={2}".format(self.endpoint, email, list_id)
        return self.ep.delete(query)

    def export_csv(self, list_id):
        """ Returns everything as :class:`str`

        :param list_id: list id to export as csv
        :type list_id: str

        :returns: response as is
        :rtype: str or EpResponse
        """

        return self.ep.read_stream("{0}/export_csv/{1}".format(self.endpoint, list_id))