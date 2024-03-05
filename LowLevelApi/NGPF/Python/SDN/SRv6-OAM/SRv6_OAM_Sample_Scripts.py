#/usr/bin/tclsh

################################################################################
#                                                                              #
#    Copyright 1997 - 2021 by Keysight                                         #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

####################################################################################    
#                                                                                  #
#                                LEGAL  NOTICE:                                    #
#                                ==============                                    #
# The following code and documentation (hereinafter "the script") is an            #
# example script for demonstration purposes only.                                  #
# The script is not a standard commercial product offered by Keysight and have     #
# been developed and is being provided for use only as indicated herein. The       #
# script [and all modifications enhancements and updates thereto (whether          #
# made by Keysight and/or by the user and/or by a third party)] shall at all times #
# remain the property of Keysight.                                                 #
#                                                                                  #
# Keysight does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without              #
# omissions or error-free.                                                         #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND Keysight         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE                  #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR     #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                     #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE     #
# USER.                                                                            #
# IN NO EVENT SHALL Keysight BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF         #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR              #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR                  #
# CONSEQUENTIAL DAMAGES EVEN IF Keysight HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                         #
# Keysight will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the         #
# script or any part thereof. The user acknowledges that although Keysight may     #
# from time to time and in its sole discretion provide maintenance or support      #
# services for the script any such services are subject to the warranty and        #
# damages limitations forth herein and will not obligate Keysight to provide       #
# any additional maintenance or support services.                                  #
#                                                                                  #
####################################################################################    

##########################################################################################################              
#                                                                                                        #
# Description:                                                                                           #
#    This script intends to demonstrate how to use SRv6 OAM (Ping/TraceRoute)in L3vpn Over SRv6 TCL APIs #
#                                                                                                        #
#    1. It will create 2 ISISL3 topologies, each having an ipv6 network                                  #
#       topology and loopback device group behind the network group(NG) with                             # 
#       loopback interface on it. L3vpn configure behind IPv6 Loopback.                                  #
#       IPv4 NG configured begind L3vpn DG.                           								     # 
#    2. Start the protocol.                                                                              #
#    3. Retrieve protocol statistics.                                                                    #
#    4. Send Ping Request to VPN SID.                                                                    #
#    5. Retrieve Ping Learned information.                                                               #
#    6. Send Ping Request to VPN SID.                                                                    #
#    7. Retrieve Traceroute Learned information.                                                         #
#    8. Stop all protocols.                                                                              #                                                                                          
##########################################################################################################

# Script Starts
print "!!! Test Script Starts !!!"
import os
import sys
import time

def assignPorts (ixNet, realPort1, realPort2) :
	 chassis1 = realPort1[0]
	 chassis2 = realPort2[0]
	 card1    = realPort1[1]
	 card2    = realPort2[1]
	 port1    = realPort1[2]
	 port2    = realPort2[2]

	 root = ixNet.getRoot()
	 vport1 = ixNet.add(root, 'vport')
	 ixNet.commit()
	 vport1 = ixNet.remapIds(vport1)[0]

	 vport2 = ixNet.add(root, 'vport')
	 ixNet.commit()
	 vport2 = ixNet.remapIds(vport2)[0]

	 chassisObj1 = ixNet.add(root + '/availableHardware', 'chassis')
	 ixNet.setAttribute(chassisObj1, '-hostname', chassis1)
	 ixNet.commit()
	 chassisObj1 = ixNet.remapIds(chassisObj1)[0]

	 if (chassis1 != chassis2) :
		 chassisObj2 = ixNet.add(root + '/availableHardware', 'chassis')
		 ixNet.setAttribute(chassisObj2, '-hostname', chassis2)
		 ixNet.commit()
		 chassisObj2 = ixNet.remapIds(chassisObj2)[0]
	 else :
		 chassisObj2 = chassisObj1
	 # end if

	 cardPortRef1 = chassisObj1 + '/card:%s/port:%s' % (card1,port1)
	 ixNet.setMultiAttribute(vport1, '-connectedTo', cardPortRef1,
		 '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 001')
	 ixNet.commit()

	 cardPortRef2 = chassisObj2 + '/card:%s/port:%s' % (card2,port2)
	 ixNet.setMultiAttribute(vport2, '-connectedTo', cardPortRef2,
		 '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 002')
	 ixNet.commit()
# end def assignPorts
################################################################################
# Either feed the ixNetwork library path in the sys.path as below, or put the
# IxNetwork.pm file somewhere else where we python can autoload it.
# "IxNetwork.pm" is available in <IxNetwork_installer_path>\API\Python
################################################################################
#ixNetPath = r'C:\Program Files (x86)\Keysight\IxNetwork\9.10.2007.7\API\Python'
#sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.39.43.12'
ixTclPort   = '8023'
ports       = [('10.39.50.200', '1', '5',), ('10.39.50.200', '1', '6',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.50',
	 '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

################################################################################
# 1. Protocol configuration section. Configure ISIS as per the description
#    give above
################################################################################ 
root = ixNet.getRoot()
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

print ("Adding 2 vports")
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]

print "Adding 2 topologies"
print("adding topologies")
ixNet.add(root, 'topology', '-vports', vportTx)
ixNet.add(root, 'topology', '-vports', vportRx)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

print ('Renaming the topologies and the device groups')
ixNet.setAttribute(topo1, '-name', 'Egress Topology: Sender')
ixNet.setAttribute(topo2, '-name', 'Ingress Topology: Receiver')

print "Adding 2 device groups"
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices [0]
t2dev1 = t2devices [0]

ixNet.setAttribute(t1dev1, '-name', 'Sender PE Router')
ixNet.setAttribute(t2dev1, '-name', 'Receiver PE Router')
ixNet.commit()
print "Configuring the multipliers (number of sessions)"
ixNet.setAttribute(t1dev1, '-multiplier', '1')
ixNet.setAttribute(t2dev1, '-multiplier', '1')
ixNet.commit()

print "Adding ethernet/mac endpoints"
ixNet.add(t1dev1, 'ethernet')
ixNet.add(t2dev1, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = ixNet.getList(t2dev1, 'ethernet')[0]

print "Configuring the mac addresses"
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
	'-direction', 'increment',
	'-start',     '00:11:01:00:00:01',
	'-step',     '00:00:00:00:00:01')

ixNet.setMultiAttribute(ixNet.getAttribute(mac2, '-mac') + '/counter',
	'-direction', 'increment',
	'-start',     '00:12:01:00:00:01',
	'-step',     '00:00:00:00:00:01')
ixNet.commit()

print "Add ipv6"
ixNet.add(mac1, 'ipv6')
ixNet.add(mac2, 'ipv6')
ixNet.commit()

ip1 = ixNet.getList(mac1, 'ipv6')[0]
ip2 = ixNet.getList(mac2, 'ipv6')[0]
mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvAdd2 = ixNet.getAttribute(ip2, '-address')
mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = ixNet.getAttribute(ip2, '-gatewayIp')

print "configuring ipv6 addresses"
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '2000:0:0:1:0:0:0:1')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '2000:0:0:1:0:0:0:2')
ixNet.setAttribute(mvGw1 + '/singleValue',  '-value', '2000:0:0:1:0:0:0:2')
ixNet.setAttribute(mvGw2 + '/singleValue',  '-value', '2000:0:0:1:0:0:0:1')


#ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '64')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '64')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()
print "Adding isisL3 over IPv6 stacks"
ixNet.add(mac1, 'isisL3')
ixNet.add(mac2, 'isisL3')
ixNet.commit()

isisL3_1 = (ixNet.getList(mac1, 'isisL3'))[0]
isisL3_2 = (ixNet.getList(mac2, 'isisL3'))[0]

print "Renaming the topologies and the device groups"
ixNet.setAttribute(topo1, '-name', 'isisL3 Topology 1')
ixNet.setAttribute(topo2, '-name', 'isisL3 Topology 2')

ixNet.setAttribute(t1dev1, '-name', 'isisL3 Topology 1 Router')
ixNet.setAttribute(t2dev1, '-name', 'isisL3 Topology 2 Router')
ixNet.commit()

#Change the property of ISIS-L3
print "Change the Property of ISIS-L3"
Network_Type_1 = ixNet.getAttribute(isisL3_1, '-networkType')
ixNet.setMultiAttribute(Network_Type_1, '-clearOverlays', 'false')
ixNet.commit()
singleValue_1 = ixNet.add(Network_Type_1, 'singleValue')
ixNet.setMultiAttribute(singleValue_1, '-value', 'pointpoint')
ixNet.commit()
Network_Type_1 = ixNet.getAttribute(isisL3_2, '-networkType')
ixNet.setMultiAttribute(Network_Type_1, '-clearOverlays', 'false')
ixNet.commit()
singleValue_1 = ixNet.add(Network_Type_1, 'singleValue')
ixNet.setMultiAttribute(singleValue_1, '-value', 'pointpoint')
ixNet.commit()

#Change the value', 'of, '-enableIPv6SID
print "Change the valueenableIPv6SID"
enableIPv6SID_1 = ixNet.getAttribute(isisL3_1, '-enableIPv6SID')
ixNet.setMultiAttribute(enableIPv6SID_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(enableIPv6SID_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
enableIPv6SID_1 = ixNet.getAttribute(isisL3_2, '-enableIPv6SID')
ixNet.setMultiAttribute(enableIPv6SID_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(enableIPv6SID_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Enable the ipv6Srh means Enable SR-IPv6
isisRtr_1 = ixNet.getList(t1dev1, 'isisL3Router')[0]
print "Enabling the ipv6Srh means Enable SR-IPv6"
ipv6Srh_1 = ixNet.getAttribute(isisRtr_1, '-ipv6Srh')
ixNet.setMultiAttribute(ipv6Srh_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv6Srh_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
isisRtr_2 = ixNet.getList(t2dev1, 'isisL3Router')[0]
ipv6Srh_1 = ixNet.getAttribute(isisRtr_2, '-ipv6Srh')
ixNet.setMultiAttribute(ipv6Srh_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv6Srh_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Configure Locator in isisL3Router in topology 2 
print "Configure Locator in isisL3Router in topology 2"
locator_1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList', '-locator')
ixNet.setMultiAttribute(locator_1, '-clearOverlays', 'false')
ixNet.commit()
counter_locator = ixNet.add(locator_1, 'counter')
ixNet.setMultiAttribute(counter_locator,
	'-step', '0:0:0:1:0:0:0:0',
	'-start', '5001:0:0:1:0:0:0:0',
	'-direction', 'increment')
ixNet.commit()

#Configure End SID in isisL3Router in topology 2 
print "Configure End SID in isisL3Router in topology 2"
EndSid = ixNet.getAttribute(t2dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-sid')
ixNet.setMultiAttribute(EndSid, '-clearOverlays', 'false')
ixNet.commit()
counter_EndSid = ixNet.add(EndSid, 'counter')
ixNet.setMultiAttribute(counter_EndSid,
	'-step', '0:0:0:0:1:0:0:0',
	'-start', '5001:0:0:1:10:0:0:0',
	'-direction', 'increment')
ixNet.commit()

#Create Network
IPv6_LoopBack = ixNet.add(t1dev1, 'networkGroup')
ixNet.setMultiAttribute(IPv6_LoopBack,
	'-name', 'IPv6_LoopBack_Address')
ixNet.commit()
IPv6_LoopBack = ixNet.remapIds(IPv6_LoopBack)[0]
ipv6PrefixPools = ixNet.add(IPv6_LoopBack, 'ipv6PrefixPools')
ixNet.setMultiAttribute(ipv6PrefixPools,
	'-addrStepSupported', 'true',
	'-name', 'BasicIPv6Addresses1')
ixNet.commit()
ipv6PrefixPools = ixNet.remapIds(ipv6PrefixPools)[0]
Connector = ixNet.add(ipv6PrefixPools, 'connector')
ixNet.setMultiAttribute(Connector,
	'-connectedTo', 'mac1')
ixNet.commit()
networkAddress = ixNet.getAttribute(ipv6PrefixPools, '-networkAddress')
ixNet.setMultiAttribute(networkAddress, '-clearOverlays', 'false')
ixNet.commit()
counter_networkAddress = ixNet.add(networkAddress, 'counter')
ixNet.setMultiAttribute(counter_networkAddress,
	'-step', '::0.0.0.1',
	'-start', '1111::1',
	'-direction', 'increment')
ixNet.commit()
#Create Network Group At PEER2 Side
networkGroup_P2 = ixNet.add(t2dev1, 'networkGroup')
ixNet.setMultiAttribute(networkGroup_P2,
	'-name', 'Routers')
ixNet.commit()
networkGroup_P2 = ixNet.remapIds(networkGroup_P2)[0]
Network_Topology = ixNet.add(networkGroup_P2, 'networkTopology')
ixNet.commit()
Network_Topology = ixNet.remapIds(Network_Topology)[0]
netTopologyLinear = ixNet.add(Network_Topology, 'netTopologyLinear')
ixNet.commit()
netTopologyLinear = ixNet.remapIds(netTopologyLinear)[0]
ixNet.setMultiAttribute(netTopologyLinear, '-nodes', '4')
ixNet.commit()

#Enable the filed of', 'Enable SR-IPv6"
ipv6Srh = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1', '-ipv6Srh')
ixNet.setMultiAttribute(ipv6Srh, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(ipv6Srh, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
#Change the Network Address of ISIS Simulated IPv6 Node Routers of Simulated Bridge
networkAddress = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1',
'-networkAddress')
ixNet.setMultiAttribute(networkAddress, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(networkAddress, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '2222::1')
ixNet.commit()
singleValue = ixNet.remapIds(singleValue)[0]
ixNet.setMultiAttribute(networkAddress + '/nest:1', '-enabled', 'false',
			'-step', '::0.0.0.1')
ixNet.setMultiAttribute(networkAddress + '/nest:2',
			'-enabled', 'false',
			'-step', '::0.0.0.1')
ixNet.commit()
active = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1', '-active')
ixNet.setMultiAttribute(active, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(active, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()

#Configure locator in isisL3PseudoRouter in topology 2 
print "Configure locator in isisL3PseudoRouter in topology 2"
locator = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/isisPseudoSRv6LocatorEntryList', '-locator')
ixNet.setMultiAttribute(locator, '-clearOverlays', 'false')
ixNet.commit()
counter_locator = ixNet.add(locator, 'counter')
ixNet.setMultiAttribute(counter_locator,
	'-step', '0:0:0:1:0:0:0:0',
	'-start', '5001:0:0:2:0:0:0:0',
	'-direction', 'increment')
ixNet.commit()

#Configure End SID in isisL3PseudoRouter in topology 2 
print "Configure End SID in isisL3PseudoRouter in topology 2"
EndSid = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/isisPseudoSRv6LocatorEntryList/isisPseudoSRv6EndSIDList', '-sid')
ixNet.setMultiAttribute(EndSid, '-clearOverlays', 'false')
ixNet.commit()
counter_EndSid = ixNet.add(EndSid, 'counter')
ixNet.setMultiAttribute(counter_EndSid,
	'-step', '0:0:0:1:0:0:0:0',
	'-start', '5001:0:0:2:10:0:0:0',
	'-direction', 'increment')
ixNet.commit()


#Add Device Group Behind IPv6 Network Group
deviceGroup_bgp = ixNet.add(IPv6_LoopBack, 'deviceGroup')
ixNet.setMultiAttribute(deviceGroup_bgp,
	'-multiplier', '1',
	'-name', 'BGP_L3vpn_1')
ixNet.commit()
deviceGroup_bgp = ixNet.remapIds(deviceGroup_bgp)[0]
enable = ixNet.getAttribute(deviceGroup_bgp, '-enabled')
ixNet.setMultiAttribute(enable,
	'-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(enable, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'true')
ixNet.commit()
singleValue = ixNet.remapIds(singleValue)[0]

ipv6Loopback = ixNet.add(deviceGroup_bgp, 'ipv6Loopback')
ixNet.setMultiAttribute(ipv6Loopback,
	'-stackedLayers', [],
	'-name', 'IPv6 Loopback 1')
ixNet.commit()
ipv6Loopback = ixNet.remapIds(ipv6Loopback)[0]

Connector = ixNet.add(ipv6Loopback, 'connector')
ixNet.setMultiAttribute(Connector,
	'-connectedTo', 'ipv6PrefixPools')
ixNet.commit()
Connector = ixNet.remapIds(Connector)[0]
prefix = ixNet.getAttribute(ipv6Loopback, '-prefix')
ixNet.setMultiAttribute(prefix,
	'-clearOverlays', 'false')
ixNet.commit()
Single_Value = ixNet.add(prefix, 'singleValue')
ixNet.setMultiAttribute(Single_Value,
	'-value', ' 128')
ixNet.commit()        
address = ixNet.getAttribute(ipv6Loopback, '-address')
ixNet.setMultiAttribute(address,
	'-clearOverlays', 'false')
ixNet.commit()
Counter = ixNet.add(address, 'counter')
ixNet.setMultiAttribute(Counter,
	'-step', '::0.0.0.1',
	'-start', '1111::1',
	'-direction', 'increment')
ixNet.commit()
bgpIpv6Peer_1 = ixNet.add(ipv6Loopback, 'bgpIpv6Peer')
ixNet.setMultiAttribute(bgpIpv6Peer_1,
	'-enSRv6DataPlane', 'true',
	'-stackedLayers', [],
	'-name', 'BGP6Peer2')
ixNet.commit()
bgpIpv6Peer_1 = ixNet.remapIds(bgpIpv6Peer_1)[0]
dutIp = ixNet.getAttribute(bgpIpv6Peer_1, '-dutIp')
ixNet.setMultiAttribute(dutIp,
	'-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(dutIp, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '::0.0.0.1',
	'-start', '2222::1',
	'-direction', 'increment')
ixNet.commit()

filterIpV4MplsVpn = ixNet.getAttribute(bgpIpv6Peer_1, '-filterIpV4MplsVpn')
ixNet.setMultiAttribute(filterIpV4MplsVpn, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(filterIpV4MplsVpn, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()

capabilityNHEncodingCapabilities = ixNet.getAttribute(bgpIpv6Peer_1, '-capabilityNHEncodingCapabilities')
ixNet.setMultiAttribute(capabilityNHEncodingCapabilities, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(capabilityNHEncodingCapabilities, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()


#Adding BGPVRF on top of BGP+
bgpV6Vrf_1 = ixNet.add(bgpIpv6Peer_1, 'bgpV6Vrf')
ixNet.setMultiAttribute(bgpV6Vrf_1,
	'-multiplier', '4',
	'-stackedLayers', [],
	'-name', 'BGP6VRF2')
ixNet.commit()
bgpV6Vrf_1 = ixNet.remapIds(bgpV6Vrf_1)[0]
targetAsNumber = ixNet.getAttribute(bgpV6Vrf_1 + '/bgpExportRouteTargetList:1', '-targetAsNumber')
ixNet.setMultiAttribute(targetAsNumber,
	'-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(targetAsNumber, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '1',
	'-start', '100',
	'-direction', 'increment')
ixNet.commit()
#Adding Network Group Behind BGP+
networkGroup = ixNet.add(deviceGroup_bgp, 'networkGroup')
ixNet.setMultiAttribute(networkGroup, '-name', 'IPv4_VPN_Rote')
ixNet.commit()
networkGroup = ixNet.remapIds(networkGroup)[0]
networkGroup_1 = ixNet.getAttribute(networkGroup, '-enabled')
ixNet.setMultiAttribute(networkGroup_1,
	'-clearOverlays', 'false')
ixNet.commit()
networkGroup_1 = ixNet.add(networkGroup_1, 'singleValue')
ixNet.setMultiAttribute(networkGroup_1, '-value', 'true')
ixNet.commit()
networkGroup_1 = ixNet.remapIds(networkGroup_1)[0]
ipv4PrefixPools = ixNet.add(networkGroup, 'ipv4PrefixPools')
ixNet.setMultiAttribute(ipv4PrefixPools, '-addrStepSupported', 'true',	'-name', 'BasicIPv4Addresses2')
ixNet.commit()
ipv4PrefixPools = ixNet.remapIds(ipv4PrefixPools)[0]
connector = ixNet.add(ipv4PrefixPools, 'connector')
ixNet.setMultiAttribute(connector,
	'-connectedTo', 'bgpV6Vrf_1')
ixNet.commit()
networkAddress = ixNet.getAttribute(ipv4PrefixPools, '-networkAddress')
ixNet.setMultiAttribute(networkAddress,
	'-clearOverlays', 'false')

ixNet.commit()
counter = ixNet.add(networkAddress, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '0.1.0.0',
	'-start', '1.1.1.1',
	'-direction', 'increment')
ixNet.commit()
bgpV6L3VpnRouteProperty = ixNet.getList(ipv4PrefixPools, 'bgpV6L3VpnRouteProperty')[0]
labelStep = ixNet.getAttribute(bgpV6L3VpnRouteProperty, '-labelStep')
ixNet.setMultiAttribute(labelStep,
	'-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(labelStep, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '1')
ixNet.commit()
enableSrv6Sid = ixNet.getAttribute(bgpV6L3VpnRouteProperty, '-enableSrv6Sid')
ixNet.setMultiAttribute(enableSrv6Sid, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(enableSrv6Sid, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
srv6SidLoc = ixNet.getAttribute(bgpV6L3VpnRouteProperty, '-srv6SidLoc')
ixNet.setMultiAttribute(srv6SidLoc, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(srv6SidLoc, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '::1',
	'-start', '5000:0:0:1::d100',
	'-direction', 'increment')
ixNet.commit()
#Configure BGP/BGP-vrf at PEER2 side
deviceGroup_P2 = ixNet.add(networkGroup_P2, 'deviceGroup')
ixNet.setMultiAttribute(deviceGroup_P2,
	'-multiplier', '1',
	'-name', 'BGP_L3vpn_2')
ixNet.commit()
deviceGroup_P2 = ixNet.remapIds(deviceGroup_P2)[0]
ipv6Loopback_P2 = ixNet.add(deviceGroup_P2, 'ipv6Loopback')
ixNet.setMultiAttribute(ipv6Loopback_P2,
	'-stackedLayers', [],
	'-name', 'IPv6Loopback1')
ixNet.commit()
ipv6Loopback_P2 = ixNet.remapIds(ipv6Loopback_P2)[0]
connector = ixNet.add(ipv6Loopback_P2, 'connector')
ixNet.commit()
address = ixNet.getAttribute(ipv6Loopback_P2, '-address')
ixNet.setMultiAttribute(address, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(address, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '::0.0.0.1',
	'-start', '2222::1',
	'-direction', 'increment')
ixNet.commit()
bgpIpv6Peer_p2 = ixNet.add(ipv6Loopback_P2, 'bgpIpv6Peer')
#ixNet.setMultiAttribute(bgpIpv6Peer_p2, '-stackedLayers', '-name', 'BGP6Peer1')
ixNet.commit()
bgpIpv6Peer_p2 = ixNet.remapIds(bgpIpv6Peer_p2)[0]
dutIp = ixNet.getAttribute(bgpIpv6Peer_p2, '-dutIp')
ixNet.setMultiAttribute(dutIp, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(dutIp, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '::0.0.0.1',
	'-start', '1111::1',
	'-direction', 'increment')
ixNet.commit()

filterIpV4MplsVpn_2 = ixNet.getAttribute(bgpIpv6Peer_p2, '-filterIpV4MplsVpn')
ixNet.setMultiAttribute(filterIpV4MplsVpn_2, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(filterIpV4MplsVpn_2, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()

capabilityNHEncodingCapabilities_2 = ixNet.getAttribute(bgpIpv6Peer_p2, '-capabilityNHEncodingCapabilities')
ixNet.setMultiAttribute(capabilityNHEncodingCapabilities_2, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(capabilityNHEncodingCapabilities_2, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
#Adding BGPVRF on top of BGP+ @Peer2 side
bgpV6Vrf_2 = ixNet.add(bgpIpv6Peer_p2, 'bgpV6Vrf')
ixNet.setMultiAttribute(bgpV6Vrf_2,
	'-multiplier', '4',
	'-stackedLayers', [],
	'-name', 'BGP6VRF2')
ixNet.commit()
bgpV6Vrf_2 = ixNet.remapIds(bgpV6Vrf_2)[0]
targetAsNumber = ixNet.getAttribute(bgpV6Vrf_2 + '/bgpExportRouteTargetList:1', '-targetAsNumber')
ixNet.setMultiAttribute(targetAsNumber, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(targetAsNumber, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '1',
	'-start', '100',
	'-direction', 'increment')
ixNet.commit()
#Adding Network Group Behind BGP+ AT PEER2 Side
networkGroup_P2 = ixNet.add(deviceGroup_P2, 'networkGroup')
ixNet.setMultiAttribute(networkGroup_P2,
	'-name', 'IPv4_VPN_Route_2')
ixNet.commit()
networkGroup_P2 = ixNet.remapIds(networkGroup_P2)[0]
networkGroup_2 = ixNet.getAttribute(networkGroup_P2, '-enabled')
ixNet.setMultiAttribute(networkGroup_2, '-clearOverlays', 'false')
ixNet.commit()
networkGroup_2 = ixNet.add(networkGroup_2, 'singleValue')
ixNet.setMultiAttribute(networkGroup_2, '-value', 'true')
ixNet.commit()
networkGroup_1 = ixNet.remapIds(networkGroup_2)[0]
ipv4PrefixPools_P2 = ixNet.add(networkGroup_P2, 'ipv4PrefixPools')
ixNet.setMultiAttribute(ipv4PrefixPools_P2,
	'-addrStepSupported', 'true',
	'-name', 'BasicIPv4Addresses2')
ixNet.commit()
ipv4PrefixPools_P2 = ixNet.remapIds(ipv4PrefixPools_P2)[0]
connector_P2 = ixNet.add(ipv4PrefixPools_P2, 'connector')
ixNet.setMultiAttribute(connector_P2, '-connectedTo', 'bgpV6Vrf_2')
ixNet.commit()
networkAddress_P2 = ixNet.getAttribute(ipv4PrefixPools_P2, '-networkAddress')
ixNet.setMultiAttribute(networkAddress_P2, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(networkAddress_P2, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '0.1.0.0',
	'-start', '2.2.2.2',
	'-direction', 'increment')
ixNet.commit()
bgpV6L3VpnRouteProperty_P2 = ixNet.getList(ipv4PrefixPools_P2, 'bgpV6L3VpnRouteProperty')[0]
labelStep = ixNet.getAttribute(bgpV6L3VpnRouteProperty_P2, '-labelStep')
ixNet.setMultiAttribute(labelStep, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(labelStep, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '1')
ixNet.commit()
enableSrv6Sid = ixNet.getAttribute(bgpV6L3VpnRouteProperty_P2, '-enableSrv6Sid')
ixNet.setMultiAttribute(enableSrv6Sid, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(enableSrv6Sid, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
srv6SidLoc = ixNet.getAttribute(bgpV6L3VpnRouteProperty_P2, '-srv6SidLoc')
ixNet.setMultiAttribute(srv6SidLoc, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(srv6SidLoc, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '::1',
	'-start', '5001:0:0:5::d100',
	'-direction', 'increment')
ixNet.commit()

print("\nSRv6 OAM Related Configuration begins here !!!")
#Enable srv6OAMService in ISIS-L3 Router present in Topology 1 and Topology 2
print "Enable srv6OAMService in ISIS-L3 Router present in Topology 1 and Topology 2"
#Change the value of -srv6OAMService
print "Change the value srv6OAMService"
srv6OAMService_1 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1', '-srv6OAMService')
ixNet.setMultiAttribute(srv6OAMService_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(srv6OAMService_1, "singleValue")
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

srv6OAMService_2 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1', '-srv6OAMService')
ixNet.setMultiAttribute(srv6OAMService_2, '-clearOverlays', 'false')
ixNet.commit()
single_value_2 = ixNet.add (srv6OAMService_2, 'singleValue')
ixNet.setMultiAttribute(single_value_2, '-value', 'true')
ixNet.commit()

#Enable srv6OAMService in isisL3PseudoRouter in Topology 2
print "Enable srv6OAMService in isisL3PseudoRouter in Topology 2"
srv6OAMService = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1', '-srv6OAMService')
ixNet.setMultiAttribute(srv6OAMService, '-clearOverlays', 'false')
ixNet.commit()
single_value = ixNet.add(srv6OAMService, "singleValue")
ixNet.setMultiAttribute(single_value, '-value', 'true')
ixNet.commit()

#Enable srv6OAMService in BGP+ Peer in Topology 1 and Topology 2
print "Enable srv6OAMService in BGP+ Peer in Topology 1 and Topology 2"
ixNet.setMultiAttribute(bgpIpv6Peer_1, '-enableSRv6OAMService', 'true')
ixNet.commit()

ixNet.setAttribute(bgpIpv6Peer_p2, '-enableSRv6OAMService', 'true') 
ixNet.commit()


print "Adding srv6Oam over IPv6 stacks"
ixNet.add(ip1, 'srv6Oam')
ixNet.add(ip2, 'srv6Oam')
ixNet.commit()

srv6Oam1 = ixNet.getList(ip1, 'srv6Oam')[0]
srv6Oam2 = ixNet.getList(ip2, 'srv6Oam')[0]

#Configure the value of numPingTraceRouteDest
print "Configure the value numPingTraceRouteDest"
ixNet.setAttribute(srv6Oam1, '-numPingTraceRouteDest', '1')
ixNet.commit()

#Configure the value for field tracerouteDstPort (destination Port to be used traceroute operation)
print "Configure the value for field tracerouteDstPort (destination Port to be used traceroute operation)"
ixNet.setAttribute(srv6Oam1, '-tracerouteDstPort', '33435')
ixNet.setAttribute(srv6Oam2, '-tracerouteDstPort', '33435')
ixNet.commit()

#Configure the value for field locatorBlkLen (Useful while processing compressed sid in srh)
print "Configure the value for field locatorBlkLen (Useful while processing compressed sid in srh)"
locatorBlkLen = ixNet.getAttribute(srv6Oam2, '-locatorBlkLen')
singleValue   = ixNet.add(locatorBlkLen, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '48bit')
ixNet.commit()

srv6OamDestination = ixNet.getList(srv6Oam1, 'srv6OamDestination')[0]
#Configure the value for field srv6DestAddress (Destination address)
print "Configure the value for field srv6DestAddress (Destination address)"
srv6DestAddress = ixNet.getAttribute(srv6OamDestination, '-srv6DestAddress')
singleValue = ixNet.add(srv6DestAddress, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '5001:0:0:5:0:0:0:d100')
ixNet.commit()


srv6DstName = ixNet.getAttribute(srv6OamDestination, '-srv6DstName')
ixNet.setMultiAttribute(srv6DstName, '-clearOverlays', 'false')
ixNet.commit()
string = ixNet.add(srv6DstName, 'string')
ixNet.setMultiAttribute(string, '-pattern', 'VPN SID DA-{Inc:1,1}')
ixNet.commit()

#Configure the value for field numSegments (Number of segments)
print "Configure the value for field numSegments (Number of segments)"
ixNet.setAttribute(srv6OamDestination, '-numSegments', '5')
ixNet.commit()

#Configure the value for field srv6DestAddress (Destination address)
print "Configure the value for field srv6DestAddress (Destination address)"
srv6DestAddress = ixNet.getAttribute(srv6OamDestination, '-srv6DestAddress')
singleValue = ixNet.add(srv6DestAddress, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '5001:0:0:5:0:0:0:d100')
ixNet.commit()

#Configure the value for field txCfgSrcAddrFlag (Enable Configure source address)
print "Configure the value for field txCfgSrcAddrFlag (Destination address)"
txCfgSrcAddrFlag = ixNet.getAttribute(srv6OamDestination, '-txCfgSrcAddrFlag')
singleValue = ixNet.add(txCfgSrcAddrFlag, "singleValue")
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()

#Configure the value for field txSrcAddr (source address to be used for ping/Traceroute request)
print "Configure the value for field txSrcAddr (Destination address)"
txSrcAddr = ixNet.getAttribute(srv6OamDestination, '-txSrcAddr')
singleValue = ixNet.add(txSrcAddr, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '1111:0:0:0:0:0:0:1')
ixNet.commit()

#Configure the value for field payloadLen
print "Configure the value for field payloadLen"
payloadLen = ixNet.getAttribute(srv6OamDestination, '-payloadLen')
singleValue = ixNet.add(payloadLen, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '32')
ixNet.commit()

#Configure the value for field maxTtlForTR (TTl for Traceroute)
print "Configure the value for field maxTtlForTR (TTl for Traceroute)"
maxTtlForTR = ixNet.getAttribute(srv6OamDestination, '-maxTtlForTR')
singleValue = ixNet.add(maxTtlForTR, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '60')
ixNet.commit()

#Configure the value for field ttl (TTL for Ping)
print "Configure the value for field ttl (TTL for Ping)"
ttl = ixNet.getAttribute(srv6OamDestination, '-ttl')
singleValue = ixNet.add(ttl, 'singleValue')
ixNet.setMultiAttribute(singleValue,'-value', '250')
ixNet.commit()


#Configure the value for field oFlag 
print "Configure the value for field oFlag"
oFlag = ixNet.getAttribute(srv6OamDestination, '-oFlag')
singleValue = ixNet.add(oFlag, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()


srv6oamSegmentNode = ixNet.getList(srv6OamDestination, 'srv6oamSegmentNode')[0]
#Configure the value for field segmentAddress 
print "Configure the value for field segmentAddress"
segmentAddress = ixNet.getAttribute(srv6oamSegmentNode, '-segmentAddress')
counter = ixNet.add(segmentAddress, 'counter')
ixNet.setMultiAttribute(counter,
	'-step','0:0:0:1:0:0:0:0',
	'-start','5001:0:0:1:10:0:0:0',
	'-direction', 'increment')
ixNet.commit()

#Configure the value for field gSIDEnableFlag 
print "Configure the value for field gSIDEnableFlag"
gSIDEnableFlag = ixNet.getAttribute(srv6oamSegmentNode, '-gSIDEnableFlag')
singleValue = ixNet.add(gSIDEnableFlag, "singleValue")
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()

#Configure the value for field locatorBlkLen 
print "Configure the value for field locatorBlkLen"
locatorBlkLen = ixNet.getAttribute(srv6oamSegmentNode, '-locatorBlkLen')
singleValue = ixNet.add(locatorBlkLen, "singleValue")
ixNet.setMultiAttribute(singleValue, '-value', '48')
ixNet.commit()

################################################################################
# 2. Start ISISl3/BGP+ protocol and wait for 60 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
print ("Fetching all Protocol Summary Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
	for  statVal in statValList :
		print("***************************************************")
		index = 0
		for satIndv in statVal :
			print("%-30s:%s" % (statcap[index], satIndv))
			index = index + 1
		# end for
	# end for
# end for
print("***************************************************")

###############################################################################
# Step 4> Trigger Ping Request
###############################################################################
print "Sending Ping Request for VPN SID"
print srv6OamDestination
ixNet.execute('sendPingRequest', srv6OamDestination, '1')
time.sleep(30)
###############################################################################
# Step 5> Retrieve Ping learned info
###############################################################################

linfo  = ixNet.getList(srv6Oam1, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')
print "Ping learned info"
print "***************************************************"
for v in values :
	print v
print "***************************************************"


###############################################################################
# Step 6> clear learned info
###############################################################################
ixNet.execute('clearAllLearnedInfo', srv6OamDestination , '1')

###############################################################################
# Step 7> Trigger TraceRoute Request
###############################################################################
print "Sending TraceRoute Request for VPN SID"
ixNet.execute('sendTraceRouteRequest', srv6OamDestination, '1')
time.sleep(30)
###############################################################################
# Step 8> Retrieve TraceRoute learned info
###############################################################################

linfo  = ixNet.getList(srv6Oam1, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')
print "Ping learned info"
print "***************************************************"
for v in values :
	print v
print "***************************************************"

################################################################################
# 9. Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
print ('!!! Test Script Ends !!!')

