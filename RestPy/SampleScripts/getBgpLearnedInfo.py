"""
getBgpLearnedInfo.py

   - Get the device ID index by the IPv4 address
   - Optional: Control individual BGP session protocol (start|stop) by the index ID
   - Get BGP learned info with the index ID
   
Requirements:
   - IxNetwork 9.10

How to get BGP learned info on the Windows GUI:
   - In BGP Peer, enabled filterIpv4Unicast
   - Restart protocols
   - On BGP Peer tab, right click on a device ID session and
     select "Get Non-VPN Learned Info" and select "Get IPv4 learned info".
   - An "IPv4 Prefixes" tab will appear.  
   - In the tab, view all the BGP learned info
"""

import traceback

from ixnetwork_restpy import SessionAssistant
     
try:
   session = SessionAssistant(IpAddress='192.168.70.113', RestPort=None, UserName='admin', Password='admin', 
                              SessionName=None, SessionId=1, ApiKey=None, ClearConfig=False, LogLevel='all')

   ixNetwork = session.Ixnetwork


   bgp = ixNetwork.Topology.find()[0].DeviceGroup.find().Ethernet.find().Ipv4.find().BgpIpv4Peer.find()
   ipv4 = ixNetwork.Topology.find()[0].DeviceGroup.find().Ethernet.find().Ipv4.find()
   
   # Get one device ID
   index = ipv4.get_device_ids(Address='1.1.1.2')
      
   # Get a list of device ID
   #index = ipv4.get_device_ids(Address='(1.1.1.2|1.1.1.3)')

   #bgp.Stop(index)
   bgp.Start(index)
   
   # This API will create the IPv4 Prefixes tab on IxNetwork in
   # order to get all the BGP learned info
   bgp.GetIPv4LearnedInfo(index)
   
   for y in bgp.LearnedInfo.find():
      print(y.Columns)
      print()
      print(y.Values)

except Exception as errMsg:
    print('\nError: %s' % traceback.format_exc())
    print('\nrestPy.Exception:', errMsg)
