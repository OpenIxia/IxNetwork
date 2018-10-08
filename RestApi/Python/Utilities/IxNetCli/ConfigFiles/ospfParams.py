params = {
    "ixChassisIp": "192.168.70.128",
    "portList": [["192.168.70.128", "1", "1"],
                 ["192.168.70.128", "1", "2"]
                ],
    "topology": [
	{
	    "name": "Topology-1",
	    "ports": [["192.168.70.128", "1", "1"]],
	    "deviceGroup": [
		{
		    "name": "DG-1",		
		    "multiplier": 1,
		    "ethernet": [
			{
			    "name": "Ethernet-1",
			    "macAddress": {"start": "00:01:01:00:00:01",
                                           "direction": "increment",
                                           "step": "00:00:00:00:00:01"},
                            "macAddressPortStep": "disabled",
			    "vlanId": {"start": 101, "direction": "increment", "step": 0},
			    "ipv4": [
				{
				    "name": "ipv4-2",
				    "address": {"start": "1.1.1.1",
                                                "direction": "increment",
                                                "step": "0.0.0.1"},
                                    "ipv4AddressPortStep": "disabled",
				    "gateway": {"start": "1.1.1.2",
                                                "direction": "increment",
                                                "step": "0.0.0.1"},
                                    "gatewayPortStep": "disabled",
				    "prefix": 24,
				    "ospf": [
					{
					    "name": "OSPF-1",
					    "neighborIp": "1.1.1.2",
					    "areaId": "0",
					    "areaIp": "0.0.0.0",
					    "helloInterval": 10,
					    "networkType": "pointtomultipoint",
					    "deadInterval": 10
					}
				    ]
				}
			    ]
			}
		    ],
		    "networkGroup": [
			{
			    "name": "bgpRouteRange1",
			    "multiplier": 100,
			    "prefix": 32,
			    "routeRange": {"start": "100.0.0.1",
                                           "direction": "increment",
                                           "step": "0.0.0.1"}
			}
		    ]
		}
	    ]
	},	
        {
	    "name": "Topology-2",
	    "ports": [["192.168.70.128", "1", "2"]],
	    "deviceGroup": [
		{
		    "name": "DG-2",		
		    "multiplier": 1,
		    "ethernet": [
			{
			    "name": "Ethernet-2",
			    "macAddress": {"start": "00:01:01:00:00:02",
                                           "direction": "increment",
                                           "step": "00:00:00:00:00:01"},
                            "macAddressPortStep": "disabled",
			    "vlanId": {"start": 101, "direction": "increment", "step": 0},
			    "ipv4": [
				{
				    "name": "ipv4-2",
				    "address": {"start": "1.1.1.2",
                                                "direction": "increment",
                                                "step": "0.0.0.1"},
                                    "ipv4AddressPortStep": "disabled",
				    "gateway": {"start": "1.1.1.1",
                                                "direction": "increment",
                                                "step": "0.0.0.1"},
                                    "gatewayPortStep": "disabled",
				    "prefix": 24,
				    "ospf": [
					{
					    "name": "OSPF-2",
					    "neighborIp": "1.1.1.1",
					    "areaId": "0",
					    "areaIp": "0.0.0.0",
					    "helloInterval": 10,
					    "networkType": "pointtomultipoint",
					    "deadInterval": 10
					}
				    ]
				}
			    ]
			}
		    ],
		    "networkGroup": [
			{
			    "name": "bgpRouteRange2",
			    "multiplier": 100,
			    "prefix": 32,
			    "routeRange": {"start": "200.0.0.1",
                                           "direction": "increment",
                                           "step": "0.0.0.1"}
			}
		    ]
		}	
	    ]
	}
    ],
    "trafficItems":  [
        {
	    "name": "Port1 to Port2",
	    "trafficType": "ipv4",
	    "bidirectional": True,
	    "trackBy": ["flowGroup0", "vlanVlanId0"],
            "endpoints": [{"name": "FlowGroup-1",
                           "sources": ["/topology/1"],
                           "destinations": ["/topology/2"]
                       }
            ],
	    "configElements": [
		{
		    "transmissionType": "fixedPacketCount",
		    "frameCount": 2000000,
		    "frameRate": 100,
		    "frameRateType": "percentLineRate",
		    "frameSize": 64
		}
	    ]
        }
    ]
}

