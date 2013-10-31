import os
import random
import string


class Lists(object):
    """
    Lists endpoint
    """

    endpoint = "lists"

    def __init__(self, ep):
        self.ep = ep

    def find_all(self):
        """ Query all lists

        :returns: List of JSON of all lists for user
        :rtype: EpResponse
        """

        return self.ep.get(self.endpoint)

    def create(self, name, from_name, reply_to):
        """ Create a list

        :param name: Name of a newly created list
        :type name: str

        :param from_name: Default "from" name used when sending campaigns to this list
        :type from_name: str

        :param reply_to: Default Reply To email address used when sending campaigns to this list
        :type reply_to: str

        :returns: ContactList object
        :rtype: EpResponse
        """

        params = {"name": name, "from_name": from_name, "reply_to": reply_to}
        return self.ep.post(self.endpoint, params=params)

    def delete(self, list_id):
        """ Removes a list with a given id.
            A list must be enabled and has no dependent subscriptions and/or scheduled campaigns.

        :param list_id: Id of list to be removed
        :type list_id: int

        :returns: EpResponse with status, code, and message
        :rtype: EpResponse

        """
        return self.ep.delete('{0}/{1}'.format(self.endpoint, list_id))

    def update(self, list_id, params):
        """ Updates existing list

            :param list_id: Id of list to be updated
            :type list_id: int

            :param params: JSON object represents a list to be updated
            :type params: dict

            :returns: EpResponse with status, code, message, and updated list
            :rtype: EpResponse
        """
        params['id'] = list_id
        return self.ep.put(self.endpoint, params=params)

    def upload(self, list_id, contacts_file):
        """ Creates or merges contacts from uploaded CSV file.

        :param list_id: Id of list to be updated with contacts from CSV
        :type list_id: int

        :param contacts_file: Absolute path to the CSV file with contacts
        :type contacts_file: str

        :returns: EpResponse with status, code, and upload_id field
        :rtype: EpResponse
        """

        with (open(contacts_file)) as f:
            boundary = ''.join(random.choice(string.digits + string.ascii_letters) for i in range(30))
            lines = []
            lines.extend((
                '--{0}'.format(boundary),
                'Content-Disposition: form-data; name="contacts_file"; contacts_file="{0}"'
                .format(os.path.basename(contacts_file)),
                '',
                str(f.read())
            ))

            lines.extend((
                '--{0}--'.format(boundary),
                '',
            ))
            body = '\r\n'.join(lines)

            return self.ep.post('{0}/{1}/upload'.format(self.endpoint, list_id),
                                content_type="multipart/form-data; boundary={0}".format(boundary), body=body)

    def upload_status(self, upload_id):
        """ Checks status of upload. If the upload was finished a detailed report is returned.

        :param upload_id: The id of a list uploaded(this id was returned from :func:`upload`).

        :returns: EpResponse with status, code, and "report" field, e.g:
            "report": {
                        "suppressed": 0,
                        "skipped": 0,
                        "list_name": "Active customers",
                        "merged": 1,
                        "imported": 1
                    }
        :rtype: EpResponse
        """
        return self.ep.get('{0}/{1}/{2}'.format(self.endpoint, 'upload_status', upload_id))

    def csv(self, list_id):
        """ Returns contacts as CSV

        :param list_id: list id to export as csv
        :type list_id: str

        :returns: response as is
        :rtype: str or EpResponse
        """

        return self.ep.read_stream("{0}/{1}/csv".format(self.endpoint, list_id))