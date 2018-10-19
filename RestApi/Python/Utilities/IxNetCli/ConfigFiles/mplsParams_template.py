params = {
    "trafficType": "raw",
    "ixChassisIp": '192.168.70.128',
    "portList": [["192.168.70.128", "1", "1"],
                 ["192.168.70.128", "1", "2"]
                ],
    "trafficItems": [
        {
            'trafficType':'raw',
	    "name": "Port1 to Port2",
            "enabled": True,
            "bidirectional": True,
	    "trackBy": ["flowGroup0"],
	    "endpoints": [{'name': 'FlowGroup-1',
                           "sources": [["192.168.70.128", "1", "1"]],
                           "destinations": [["192.168.70.128", "1", "2"]]
                       }
	    ],
	    "configElements": [
                {
                    "transmissionType": "fixedPacketCount",
                    "frameCount": 2000000,
                    "frameRate": 100,
                    "frameRateType": "percentLineRate",
                    "frameSize": 64,
                    "packetHeaders": {
                        "mac": {
                            "src": {"startValue": "00:0c:29:aa:86:e0",
                                    "stepValue": "00:00:00:00:00:01",
                                    "valueType": "increment",
                                    "countValue": 1},
                            "dest": {"startValue": "00:0c:29:84:37:16",
                                     "stepValue": "00:00:00:00:00:01",
                                     "valueType": "increment",
                                     "countValue": 1}
                        },
                        "mpls": [
                            {"startValue": 16, "stepValue": 1, "valueType": "increment", "countValue": 2, "auto": False},
                            {"startValue": 18, "stepValue": 1, "valueType": "increment", "countValue": 2, "auto": False}
                        ],
                        "ipv4": {
                            "src": {"startValue": "1.1.1.1", "stepValue": "0.0.0.1",
                                    "valueType": "increment", "countValue": 2, "auto": False},
                            "dest": {"startValue": "1.1.1.2", "stepValue": "0.0.0.1",
                                    "valueType": "increment", "countValue": 2, "auto": False}
                        }
                    }
                }
            ]
        }
    ]
}



 
