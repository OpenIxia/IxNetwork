import re

from IxNetRestApiProtocol import Protocol

class Globals(object):
    def __init__(self, ixnObj=None):
        """
        Parameters
           ixnObj: <str>: The main connection object.
        """
        self.ixnObj = ixnObj
        self.protocolObj = Protocol(ixnObj)

    def dhcpV4ClientStartStopRate(self, endpoint='startRate', **kwargs):
        """
        Description
           Configure startRate|stopRate settings for DHCP V4 Client.

        Parameters
           endpoint: <str|object endpoint>: startRate|stopRate

           **kwargs: Any attribute for the /globals/topology/dhcpv4client/startRate|stopRate endpoint.
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
        restApi = '/globals/topology/dhcpv4client/{0}?links=true'.format(endpoint)

        response = self.ixnObj.get(self.ixnObj.sessionUrl + restApi)
        for key,value in response.json().items():
            if key != 'links':
                if bool(re.search('multivalue', str(value))) == True:
                    if key in kwargs:
                        multiValue = response.json()[key]
                        self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[key]})
                else:
                    if key in kwargs:
                        self.ixnObj.patch(self.ixnObj.sessionUrl + restApi, data={key: kwargs[key]})

