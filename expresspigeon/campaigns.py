class Campaigns(object):
    """Campaigns endpoint
    """

    endpoint = "campaigns"

    def __init__(self, ep):
        self.ep = ep

    def get_all(self, start_date=None, end_date=None, from_id=None):
        """ Returns up to 1000 campaigns starting with smallest campaign id in date range.

        :param from_id: smallest campaign id
        :type from_id: str

        :param start_date: Start of the reporting period (UTC, for example 2013-03-16T11:22:23.210+0000)
        :type start_date: str

        :param end_date: End of the reporting period (UTC, for example 2013-03-16T11:22:23.210+0000)
        :type end_date: str

        :returns: list of campaigns EPResponse objects, e.g.
        [{
            "total":1,
            "id":1,
            "send_time":"2014-01-10T10:24:22.000+0000",
            "template_name":"1",
            "reply_to":"john@example.net",
            "from_name":"John",
            "subject":"Hi",
            "name":"My Campaign",
            "list_id":1
        }]
        :rtype: list of EpResponse objects
        """

        params = []
        if from_id is not None:
            params.append("from_id=" + str(from_id))
        if start_date is not None and end_date is not None:
            params.append("start_date=" + start_date)
            params.append("end_date=" + end_date)
        query = self.endpoint
        if params:
            query += "?" + "&".join(params)
        return self.ep.get(query)

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

        return self.ep.get("{0}/{1}".format(self.endpoint, campaign_id))
    
    def delete(self, campaign_id):
        """ Removes a campaign with a given id. Only scheduled campaigns can be deleted. Those that have already been sent cannot be deleted.

        :param campaign_id: The id of a campaign to be removed.
        :type campaign_id: long
        """

        return self.ep.delete("{0}/{1}".format(self.endpoint, campaign_id))
    
    def opened(self, campaign_id):
        """ Returns an array of opened events from a campaign.

        :param campaign_id: Campaign id the opened events are found for.
        :type campaign_id: long

        :returns: list of dicts, e.g. 
        [{
            "timestamp": "2013-09-20T11:29:57.000+0000",
            "ip_address": "127.0.0.1",
            "email": "bob@example.net",
            "event_type": "opened",
            "user_agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        }]
        :rtype: EpResponse
        """

        return self.ep.get("{0}/{1}/opened".format(self.endpoint, campaign_id))

    def clicked(self, campaign_id):
        """ Returns an array of clicked events from a campaign.

        :param campaign_id: Campaign id the clicked events are found for.
        :type campaign_id: long

        :returns: list of dicts, e.g. 
        [{
            "timestamp": "2014-01-15T13:34:27.000+0000",
            "ip_address": "127.0.0.1",
            "email": "bob@example.net",
            "event_type": "clicked",
            "user_agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
            "url": "http://example.net"
        }]
        :rtype: EpResponse
        """

        return self.ep.get("{0}/{1}/clicked".format(self.endpoint, campaign_id))
    
    def bounced(self, campaign_id):
        """ Returns bounced contacts

        :param campaign_id: Campaign ID bounced contacts is found for
        :type campaign_id: long

        :returns: list of dicts, e.g. [{'id': 1, 'email': 'a@a.a'}]
        :rtype: EpResponse
        """

        return self.ep.get("{0}/{1}/bounced".format(self.endpoint, campaign_id))

    def unsubscribed(self, campaign_id):
        """ Returns unsubscribed contacts

        :param campaign_id: Campaign ID unsubscribed contacts is found for
        :type campaign_id: long

        :returns: list of dicts, e.g. [{'id': 1, 'email': 'a@a.a'}]
        :rtype: EpResponse
        """

        return self.ep.get("{0}/{1}/unsubscribed".format(self.endpoint, campaign_id))

    def spam(self, campaign_id):
        """ Returns contacts that mark campaign as spam

        :param campaign_id: Campaign ID spam contacts is found for
        :type campaign_id: long

        :returns: list of dicts, e.g. [{'id': 1, 'email': 'a@a.a'}]
        :rtype: EpResponse
        """

        return self.ep.get("{0}/{1}/spam".format(self.endpoint, campaign_id))
    
    def all_subscribers(self, campaign_id):
        """ Returns an array of object(s) with email and id of all subscribers for a campaign.

        :param campaign_id: Campaign ID all subscribers is found for
        :type campaign_id: long

        :returns: list of dicts, e.g. 
        [{
            "id": "1",
            "email": "bob@example.net",
            "timestamp": "2013-09-20T11:29:57.000+0000"
        },
        {
            "id": "2",
            "email": "tob@example.net",
            "timestamp": "2013-09-20T11:29:59.000+0000"
        }]
        :rtype: EpResponse
        """

        return self.ep.get("{0}/{1}/all_subscribers".format(self.endpoint, campaign_id))
    
    def delivered(self, campaign_id):
        """ Returns an array of object(s) with email and id of delivered contacts from a campaign.

        :param campaign_id: Campaign ID delivered contacts is found for
        :type campaign_id: long

        :returns: list of dicts, e.g. 
        [{
            "id": "1",
            "email": "bob@example.net",
            "timestamp": "2013-09-20T11:29:57.000+0000"
        },
        {
            "id": "2",
            "email": "tob@example.net",
            "timestamp": "2013-09-20T11:29:59.000+0000"
        }]
        :rtype: EpResponse
        """

        return self.ep.get("{0}/{1}/delivered".format(self.endpoint, campaign_id))
    
    def non_opens(self, campaign_id):
        """ Returns an array of object(s) with email and id of contacts from a campaign who did not open email.

        :param campaign_id: Campaign ID delivered contacts is found for
        :type campaign_id: long

        :returns: list of dicts, e.g. 
        [{
            "id": "1",
            "email": "bob@example.net"
        },
        {
            "id": "2",
            "email": "tob@example.net"
        }]
        :rtype: EpResponse
        """

        return self.ep.get("{0}/{1}/non_opens".format(self.endpoint, campaign_id))
