class Flows(object):
    """
    Flows endpoint
    """

    endpoint = "flows"

    def __init__(self, ep):
        self.ep = ep

    def get_all(self):
        """ Returns an array of flows.

        :returns: list of flows EPResponse objects, e.g.
        [{
            "live": true,
            "created_at": "2013-09-20T11:29:59.000+0000",
            "name": "My flow",
            "id": 1
        }]
        :rtype: list of EpResponse objects
        """
        return self.ep.get(self.endpoint)
                            
    def start(self, flow_id, email):
        """ This feature allow developers to start a flow for a contact.

        :param flow_id: flow id to be started for a contact
        :type flow_id: int

        :param email: contact email
        :type email: str

        :returns: EpResponse with message about flow start
        :rtype: EpResponse
        """
        return self.ep.post("{0}/{1}/start".format(self.endpoint, flow_id), params={"email": email})
    
    def stop(self, flow_id):
        """ This feature allow developers to stop a flow and switch it to edit mode.

        :param flow_id: flow id to be stopped
        :type flow_id: int

        :returns: EpResponse with message about flow start
        :rtype: EpResponse
        """
        return self.ep.post("{0}/{1}/start".format(self.endpoint, flow_id))
    
    def report(self, flow_id):
        """ This feature allow developers to report about all actions executed for this flow.

        :param flow_id: flow id for the report
        :type flow_id: int

        :returns: EpResponse with message about flow actions
        :rtype: EpResponse
        """
        return self.ep.post("{0}/{1}/report".format(self.endpoint, flow_id))
    
    def delete(self, flow_id):
        """ This feature allow developers to delete the flow.

        :param flow_id: flow id to be deleted
        :type flow_id: int

        :returns: EpResponse with a result
        :rtype: EpResponse
        """
        return self.ep.post("{0}/{1}/delete".format(self.endpoint, flow_id))
    
    def schedule_trigger(self, flow_id, enable):
        """ This feature allow developers to enable or disable a schedule trigger for the flow. The trigger should be created on the flow page.

        :param flow_id: flow id to be deleted
        :type flow_id: int
        
        :param enable: enable or disable a schedule trigger
        :type flow_id: bool

        :returns: EpResponse with a result
        :rtype: EpResponse
        """
        return self.ep.post("{0}/{1}/triggers/schedule".format(self.endpoint, flow_id), params={"enable": enable})
    
    def list_trigger(self, flow_id, enable):
        """ This feature allow developers to enable or disable a list trigger for the flow. The trigger should be created on the flow page.

        :param flow_id: flow id to be deleted
        :type flow_id: int
        
        :param enable: enable or disable a schedule trigger
        :type flow_id: bool

        :returns: EpResponse with a result
        :rtype: EpResponse
        """
        return self.ep.post("{0}/{1}/triggers/list".format(self.endpoint, flow_id), params={"enable": enable})
    
    def form_trigger(self, flow_id, enable):
        """ This feature allow developers to enable or disable a form trigger for the flow. The trigger should be created on the flow page.

        :param flow_id: flow id to be deleted
        :type flow_id: int
        
        :param enable: enable or disable a schedule trigger
        :type flow_id: bool

        :returns: EpResponse with a result
        :rtype: EpResponse
        """
        return self.ep.post("{0}/{1}/triggers/form".format(self.endpoint, flow_id), params={"enable": enable})