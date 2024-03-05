class Globals(object):
    def __init__(self, ixnObj=None):
        """
        Parameters
           ixnObj: <str>: The main connection object.
        """
        self.ixnObj = ixnObj
        self.ixNetwork = ixnObj.ixNetwork

    def dhcpV4ClientStartStopRate(self, endpoint='startRate', **kwargs):
        """
        Description
           Configure startRate|stopRate settings for DHCP V4 Client.

        Parameters
           endpoint: <str|object endpoint>: startRate|stopRate

           **kwargs: Any attribute for the /globals/topology/dhcpv4client/
           startRate|stopRate endpoint.
                     enabled = bool
                     interval = int
                     maxOutstanding = int
                     rate = int
                     rowNames = list
                     scalePortMode = str: port|deviceGroup
        Usage:
           globalObj.dhcpV4ClientStartStopRate(rate=500,
                                               maxOutstanding=600,
                                               enabled=True,
                                               interval=3000,
                                               scaleMode='port'
                                               )

        """
        rateObj = None

        if endpoint == 'startRate':
            rateObj = self.ixNetwork.Globals.Topology.Dhcpv4client.StartRate
        if endpoint == 'stopRate':
            rateObj = self.ixNetwork.Globals.Topology.Dhcpv4client.StopRate
        for key, value in kwargs.items():
            key = key[0].capitalize() + key[1:]
            try:
                multiValueObj = getattr(rateObj, key)
                self.ixnObj.configMultivalue(multiValueObj, 'singlevalue', {'value': value})
            except(ValueError, Exception):
                setattr(rateObj, key, value)
