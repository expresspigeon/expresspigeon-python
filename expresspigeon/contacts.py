class Contacts(object):
    """Contacts endpoint
    """
    endpoint = "contacts"

    def __init__(self, ep):
        self.ep = ep

    def upsert(self, list_id, contacts):
        """ JSON document represents a list of contacts to be created or updated.
        The email field is required.
        When updating a contact, list_id is optional,
        since the contact is uniquely identified by email across all lists.

        :param list_id: Contact list ID the contact will be added to
        :type list_id: long

        :param contacts: List of dictionaries describes new contacts. The "email" field is required.
        :type contacts: list

        :returns: EpResponse with JSON representation of a contact
        :rtype: EpResponse
        """
        return self.ep.post(self.endpoint, params={"list_id": list_id, "contacts": contacts})

    def find_by_email(self, email):
        """ Returns a single contact by email address.

        :param email: Email of contact to be selected.
        :type email: str

        :returns: EpResponse with all contact fields, e.g.
        {
             "custom_fields": {
                 "my custom field": "custom value"
             },
            "first_name": "Bob",
            "email": "bob@example.net",
           "email_format": "html",
           "created_at": "2012-10-29T14:17:58.000+0000",
           "updated_at": "2013-01-24T08:20:52.000+0000",
           "status": "ENGAGED"
           "lists": [
             {
               "id": 1
             },
             {
               "id": 2
             }]
        }
        :rtype: EpResponse
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
    
    def move(self, source, target, contacts):
        """ JSON document represents a list of contacts to be moved between source and target lists. All fields are required.

        :param source: Contact list ID from which the contact will be moved
        :type list_id: long
        
        :param target: Contact list ID the contact will be added to
        :type list_id: long

        :param contacts: Contacts to be moved, e.g.: [ "bob@example.net", "toby@example.net" ]
        :type contacts: list

        :returns: EpResponse with JSON representation of a contact
        :rtype: EpResponse
        """
        return self.ep.post("{0}/move".format(self.endpoint), params={"source_list": source, "target_list": target, "contacts": contacts})
