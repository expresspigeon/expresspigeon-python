class Messages(object):
    """ Transactional emails are sometimes called triggered emails. Unlike bulk emails,
    they are sent one at the time on per need basis and contain highly personalized content.
    Examples of triggered emails can be one-off messages, such as password reset,
    statement generated, etc.

    Sending Transactional emails requires that newsletter templates for these emails are created
    prior to sending. Such template can have merge fields, in a format ${field_name}.
    This feature allows a high degree of flexibility for message customization.

    The newsletter to be sent can have a number of merge fields, with data for merging dynamically
    provided during a call.
    """

    endpoint = "messages"

    def __init__(self, ep):
        self.ep = ep

    def send_message(self, template_id, to, reply_to, from_name, subject, merge_fields=None, view_online=False,
                     click_tracking=True):
        """ Send s single transactional message.
        It is possible to inject HTML chunks into specific placeholders inside your email template.
        NOTE: It is important to use only single quotes in injected HTML

        :param to: Email address to send message to.
        :type to: str

        :param reply_to: This parameter specifies the email address which will be getting replies from your recipients
        should they choose to reply. The reply_to should be a valid email address.
        :type reply_to: str

        :param from_name: This parameter is displayed as "From" field in the email program when your recipients view
        your message. Use this value to clearly state your name or name of your organization.
        :type from_name: str

        :param subject: The subject of a transactional message
        :type subject: str

        :param merge_fields: Values for merge fields.
        :type merge_fields: dict

        :param view_online: Generates online version of sent message. We will host this generated message on our servers
        :type view_online: bool

        :param click_tracking: Overwrites all URLs in email to point to http://clicks.expresspigeon.com for
        click tracking. Setting it to false will preserve all URLs intact, but click tracking will not be available,
        default is true
        :type click_tracking: bool

        :returns: EpResponse with the id represents an ID of a message that was sent.
        You can use this value in order to get a report on status of this message.
        :rtype: EpResponse
        """

        return self.ep.post(self.endpoint, params={'template_id': template_id, 'to': to,
                                                   'reply_to': reply_to, 'from': from_name,
                                                   'subject': subject,
                                                   'merger_fields': merge_fields,
                                                   'view_online': view_online,
                                                   'click_tracking': click_tracking})

    def report(self, message_id):
        """ Returns a report with properties of a sent message, such as 'delivered' or 'bounced', 'opened', 'clicked'
        only if these events occurred.

        :param message_id: An ID of a message that was sent.
        :type message_id: str

        :returns: EpResponse with a report, e.g.
        {
           "id": "10000000-0000-0000-0000-000000000001",
           "email": "john@example.net",
           "in_transit": false,
           "delivered": true,
           "bounced": false,
           "opened": true,
           "clicked": true,
           "urls": [
             "http://example.net/buy_a_burger"
           ],
           "spam": false,
           "created_at": "2013-03-15T11:20:21.770+0000",
           "updated_at": "2013-03-16T11:22:23.210+0000"
        }
        :rtype: EpResponse
        """

        return self.ep.get("{0}/{1}".format(self.endpoint, message_id))

    def reports(self, page, page_size, start_date=None, end_date=None):
        """ Returns a report for any number of transactional emails sent with this API.
        The start_date and end_date parameters should be provided together.

        :param page: Page number to be selected indexed at 0.
        :type page: int

        :param page_size: Desired size of page to be selected (max number is 100).
        :type page_size: int

        :param start_date: Start of the reporting period (UTC, example: 2013-03-16T11:22:23.210+0000)
        :type start_date: date

        :param end_date: End of the reporting period (UTC, example: 2013-03-16T11:22:23.210+0000)
        :type end_date: date

        :returns: EpResponse with array of reports, e.g.
        [{
           "id": "10000000-0000-0000-0000-000000000001",
           "email": "john@example.net",
           "in_transit": false,
           "delivered": true,
           "bounced": false,
           "opened": true,
           "clicked": true,
           "urls": [
             "http://example.net/buy_a_burger"
           ],
           "spam": false,
           "created_at": "2013-03-15T11:20:21.770+0000",
           "updated_at": "2013-03-16T11:22:23.210+0000"
          },{
           "id": "20000000-0000-0000-0000-000000000002",
           "email": "bob@example.net",
           "in_transit": false,
           "delivered": true,
           "bounced": false,
           "opened": false,
           "clicked": false,
           "spam": false,
           "created_at": "2013-04-15T11:20:21.770+0000",
           "updated_at": "2013-04-16T11:22:23.210+0000"
        }]
        :rtype: EpResponse
        """

        query = "{0}?page={1}&page_size={2}"
        if start_date is not None and end_date is not None:
            query += "&start_date={0}&end_date={1}".format(start_date, end_date)

        return self.ep.get(query.format(self.endpoint, page, page_size))