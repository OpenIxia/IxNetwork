from ixnetwork_restpy.base import Base


class Select(object):
    """ Select infrastructure

    POST .../operations/select
    {
        "selects": [
            {
                "from": "/",
                "properties": [],
                "children": [
                    {
                        "child": "(?i)^(topology|deviceGroup|ethernet|ipv4|ipv6|bgpIpv4Peer)$",
                        "properties": ["*"],
                        "filters": []
                    }
                ],
                "inlines": [
                    {
                        "child": "multivalue",
                        "properties": ["format", "pattern"]
                    },	
                    {
                        "child": "^(singleValue)$",
                        "properties": ["*"]
                    }	
                ]
            }
        ]
    }
    """
    def __init__(self, connection, from_url, from_properties=['*'], children=[], inlines=[]):
        self._connection = connection
        self._url = '%s/operations/select' % from_url[0:from_url.index('ixnetwork') + len('ixnetwork')]
        self._payload = {
            'selects': [
                {
                    'from': from_url,
                    'properties': from_properties,
                    'children': children,
                    'inlines': inlines
                }
            ]
        }

    def go(self):
        return self._connection._execute(self._url, self._payload)
        