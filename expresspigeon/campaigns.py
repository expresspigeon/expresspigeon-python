
class Campaigns(object):
    """Campaigns endpoint
    """

    endpoint = "campaigns"

    def __init__(self, ep):
        self.ep = ep

    def get_all(self):
        """ Return an array of all campaigns IDs

        :returns: list of campaigns ids
        :rtype: list
        """
        return self.ep.get(self.endpoint)

    def send(self, list_id, template_id, name, from_name, reply_to, subject, google_analytics):
        """ Creates a campaign. Invocation of this API will trigger sending a new campaign.
        The content type of a request must be application/json.

        :param list_id: The id of a list the campaign is sent to. The list must be enabled.
        :type list_id: long

        :param template_id: The id of a newsletter template used for the campaign.
        :type template_id: long

        :param name: The name of a campaign. This name is for your reference only and will not be exposed
        to your audience. If you have Google Analytics turned on, this value will also be used for
        Google Analytics campaign.
        :type name: str

        :param from_name: This parameter is displayed as "From" field in the email program when your recipients view
        your message. Use this value to clearly state your name or name of your organization.
        :type from_name: str

        :param reply_to: This parameter specifies the email address which will be getting replies from your recipients
        should they choose to reply. The reply_to should be a valid email address.
        :type reply_to: str

        :param subject: The subject of a newsletter
        :type subject: str

        :param google_analytics: Indicates whether Google Analytics should be enabled for a campaign.
        Should be true or false.
        :type google_analytics: bool

        :returns: EpResponse with campaign_id field
        :rtype: EpResponse
        """
        return self.ep.post(self.endpoint, params={'list_id': list_id, 'template_id': template_id, 'name': name,
                                                   'from_name': from_name, 'reply_to': reply_to, 'subject': subject,
                                                   'google_analytics': google_analytics})

    def schedule(self, list_id, template_id, name, from_name, reply_to, subject, google_analytics, schedule_for):
        """ Schedules a campaign. The content type of a request must be application/json.

        :param list_id: The id of a list the campaign is sent to. The list must be enabled.
        :type list_id: long

        :param template_id: The id of a newsletter template used for the campaign.
        :type template_id: long

        :param name: The name of a campaign. This name is for your reference only and will not be exposed
        to your audience. If you have Google Analytics turned on, this value will also be used
        for Google Analytics campaign.
        :type name: str

        :param from_name: This parameter is displayed as "From" field in the email program when your recipients view
        your message. Use this value to clearly state your name or name of your organization.
        :type from_name: str

        :param reply_to: This parameter specifies the email address which will be getting replies from your recipients
        should they choose to reply. The reply_to should be a valid email address.
        :type reply_to: str

        :param subject: The subject of a newsletter
        :type subject: str

        :param google_analytics: Indicates whether Google Analytics should be enabled for a campaign.
        Should be true or false.
        :type google_analytics: bool

        :param schedule_for: Specifies what time a campaign should be sent. The schedule_for must be in ISO date format
        and should be in the future.
        :type schedule_for: str

        :returns: EpResponse with campaign_id field
        :rtype: EpResponse
        """

        if schedule_for is None or schedule_for == "":
            raise Exception("schedule_for cannot be None or empty")

        return self.ep.post(self.endpoint, params={'list_id': list_id, 'template_id': template_id, 'name': name,
                                                   'from_name': from_name, 'reply_to': reply_to, 'subject': subject,
                                                   'google_analytics': google_analytics, 'schedule_for': schedule_for})

    def report(self, campaign_id):
        """ Returns report for specific campaign

        :param campaign_id: Campaign ID the report is generated for
        :type campaign_id: long

        :returns: report dict, e.g. {delivered=0, clicked=0, opened=0, spam=0, in_transit=1, unsubscribed=0, bounced=0}
        :rtype: EpResponse
        """

        return self.ep.get("{0}/report/{1}".format(self.endpoint, campaign_id))

    def bounced(self, campaign_id):
        """ Returns bounced contacts

        :param campaign_id: Campaign ID bounced contacts is found for
        :type campaign_id: long

        :returns: list of dicts, e.g. [{'id': 1, 'email': 'a@a.a'}]
        :rtype: EpResponse
        """

        return self.ep.get("{0}/bounced/{1}".format(self.endpoint, campaign_id))

    def unsubscribed(self, campaign_id):
        """ Returns unsubscribed contacts

        :param campaign_id: Campaign ID unsubscribed contacts is found for
        :type campaign_id: long

        :returns: list of dicts, e.g. [{'id': 1, 'email': 'a@a.a'}]
        :rtype: EpResponse
        """

        return self.ep.get("{0}/unsubscribed/{1}".format(self.endpoint, campaign_id))

    def spam(self, campaign_id):
        """ Returns contacts that mark campaign as spam

        :param campaign_id: Campaign ID spam contacts is found for
        :type campaign_id: long

        :returns: list of dicts, e.g. [{'id': 1, 'email': 'a@a.a'}]
        :rtype: EpResponse
        """

        return self.ep.get("{0}/spam/{1}".format(self.endpoint, campaign_id))
