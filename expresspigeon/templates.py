class Templates(object):
    """
    Templates endpoint
    """

    endpoint = "templates"

    def __init__(self, ep):
        self.ep = ep

    def copy(self, template_id, name, merge_fields=None):
        """ This feature allow developers to create a copy of an email template and at the same time merge data into
         a new version. It makes it possible to have the following workflow:

        1. Create a blank newsletter and add merge fields to it (using email editor)
        2. Make a new copy of this newsletter, and merge specific data into it using this API
        3. Send or schedule a new campaign with the API
        Steps 2 nd 3 can be done remotely with the API, without having to log into the website.
        Combined with ability to create new lists on the fly, and upload contacts,
        it provides an opportunity to build powerful marketing solutions.

        :param template_id: template id to be used as a source
        :type template_id: int

        :param name: name for a new template
        :type name: str

        :param merge_fields: values of merge fields
        :type merge_fields: dict

        :returns: EpResponse with 'template_id' field
        :rtype: EpResponse
        """
        return self.ep.post("{0}/{1}/copy".format(self.endpoint, template_id),
                            params={"name": name, "merge_fields": merge_fields})
                            
    def delete(self, template_id):
        """ Delete single template by id

        :param template_id: The id of a template to be removed.
        :type campaign_id: long
        """

        return self.ep.delete("{0}/{1}".format(self.endpoint, template_id))