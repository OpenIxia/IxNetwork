#!/usr/bin/env python
# coding: utf-8
################################################################################
#                                                                              #
#    Copyright 1997 - 2023 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################


################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF BGP EVPN-VXLAN REST    #
#    API.                                                                      #
#    About Topology:                                                           #
#       It will create 2 BGP EVPN-VXLAN topologies, BGP is configured at both  #
#       connected as well as unconnected Device Group. EVPN-VXLAN is           # 
#       configured in chained device along with Mac/IP pools connected behind  # 
#       the chained Device Group. Hosts are configured behind MAC/IP Pool.     # 
# Script Flow:                                                                 #
#        Step 1. Configuration of protocols.                                   #
#                                                                              #
#    Configuration flow of the script is as follow:                            #
#       i.    Adding of Ethernet and IP within both topologies,                # 
#       ii.   Ading and BGP over IP act as Spine                               #
#       iii.  Adding of Route Range behind DG of each topology                 #
#       iv.   Configuring loopback address as Router ID                        #
#       v.    Adding of chain DG for both topologies, act as VTEP              #
#       vi.  Adding of EVPN-VXLAN EVI in VTEP within both topologies           #
#       vii. Adding of MAC/IP cloud behind each EVPN-VXLAN EVI                 #
#       viii.   Configuring another Device Group which act as Hosts behind VTEP#
#               value and No. of MAC pools                                     #
#                                                                              #
#    1. Start all protocol.                                                    #
#    2. Retrieve protocol statistics.                                          #
#    3. Retrieve protocol learned info.                                        #
#    6. Stop all protocols.                                                    #
################################################################################
# 	Ixia Software:                                                             #
#    IxOS      10.00 EA                                                        #
#    IxNetwork 10.00 EA                                                        #
#                                                                              #
################################################################################
import sys, re, time, traceback

# Import the RestPy module
from ixnetwork_restpy import SessionAssistant
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant

apiServerIp = '10.39.34.225'

ixChassisIpList = ['10.39.50.212']
portList = [[ixChassisIpList[0], 1,3], [ixChassisIpList[0], 1, 4]]

# For Linux API server only
# username = 'admin'
# password = 'Keysight@123456'

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = False

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True

# For Linux API server and Windows Connection Mgr only.
#    debugMode=True:  Leave the session opened for debugging.
#    debugMode=False: Remove the session when the script is done.
debugMode = False

# LogLevel: none, info, warning, request, request_response, all
session = SessionAssistant(IpAddress=apiServerIp, RestPort=11111, UserName='admin', Password='Keysight@123456', 
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True,LogLevel="info", LogFilename='restpy.log')
ixNetwork = session.Ixnetwork
ixNetwork.info('Assign ports')
portMap = session.PortMapAssistant()
vport = dict()
for index,port in enumerate(portList):
    portName = 'Port_{}'.format(index+1)
    vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)

portMap.Connect(forceTakePortOwnership)
    
    
ixNetwork.info("Creating Topology 1")
topology1 = ixNetwork.Topology.add(Name="EVPN VXLAN 1", Ports=vport['Port_1'])

ixNetwork.info("Adding Device Group")
dg1 = topology1.DeviceGroup.add(Name='Router 1', Multiplier=1)

ixNetwork.info("Adding Ethernet/MAC endpoints")
mac1 = dg1.Ethernet.add()
mac1.Mac.Increment(start_value="00:11:01:00:00:01", step_value="00:00:00:00:00:01")


ixNetwork.info("Addding Ipv4")
ip1 = mac1.Ipv4.add()
ip1.Address.Single("23.23.23.2")
ip1.GatewayIp.Single("23.23.23.1")
ip1.Prefix.Single(24)
ip1.ResolveGateway.Single(True)


ixNetwork.info("Adding BGP over IPv4")
bgp1 = ip1.BgpIpv4Peer.add()


ixNetwork.info("Setting IPs in BGP DUT IP tab")
bgp1.DutIp.Single("23.23.23.1")

ixNetwork.info("Enabling EVPN Learned Information for BGP Router")
bgp1.FilterEvpn.Single("true")

ixNetwork.info("Adding NetworkGroup behing  dg")
networkGroup1 = dg1.NetworkGroup.add(Name="VTEP Loopback Address Pool 1", Multiplier=1)
prefixPool1 = networkGroup1.Ipv4PrefixPools.add()


ixNetwork.info("Configuring  Prefix Pool")
prefixPool1.NetworkAddress.Single("20.33.33.11")
prefixPool1.PrefixLength.Single("32")


ixNetwork.info("Adding  DeviceGroup behind VTEP Loopback Address Pool 1")
chaineddg1 = networkGroup1.DeviceGroup.add(Multiplier=1, Name="VTEP 1")
loopback1 = chaineddg1.Ipv4Loopback.add(StackedLayers=[], Name="IPv4 Loopback 1")
addressSet1 = loopback1.Address
addressSet1.Increment(start_value="20.33.33.11", step_value="0.0.0.1")

ixNetwork.info("Adding BGP over IPv4 loopback in Chained DG")
bgp2_1 = loopback1.BgpIpv4Peer.add()

ixNetwork.info("Setting Ips in BGP DUT IP tab")
bgp2_1.DutIp.Single("1.0.0.11")

ixNetwork.info("Enabling EVPN Learned Information for BGP Router")
bgp2_1.FilterEvpn.Single("true")

ixNetwork.info("Adding EVPN VXLAN over BGPv4 in chained DG")
bgpIPv4EvpnVXLAN1 = bgp2_1.BgpIPv4EvpnVXLAN.add()

ixNetwork.info("Disabling Import RT List same as Export RT List")
bgpIPv4EvpnVXLAN1.ImportRtListSameAsExportRtList = 'false'
    
ixNetwork.info("Changing Import Route Target AS No.")
bgpImportRouteTargetList1 = bgpIPv4EvpnVXLAN1.BgpImportRouteTargetList.find()[0]  
bgpImportRouteTargetList1.TargetAsNumber.Increment(start_value = "0", step_value = "0")
bgpExportRouteTargetList1 = bgpIPv4EvpnVXLAN1.BgpExportRouteTargetList.find()[0]
bgpExportRouteTargetList1.TargetAsNumber.Increment(start_value="2000", step_value = "0")

bgpExportRouteTargetList1.TargetAssignedNumber.Increment(start_value="20001", step_value = "0")


ixNetwork.info("Adding Mac Pools behind EVPN VPWS")
networkGroup2 = chaineddg1.NetworkGroup.add(Name="Hosts-Pool 1", Multiplier=1)

macPool1 = networkGroup2.MacPools.add()

ixNetwork.info("Changing Default Values of MAC Addresses in MAC Pools")
macPool1.Mac.Single("22:22:22:22:00:01")

ixNetwork.info("Enabling using of VLAN in CMAC Ranges")
macPool1.UseVlans = "true"
cMacvlan1 = macPool1.Vlan.find()[0]
    
ixNetwork.info("Configuring VLAN ID")
cMacvlan1.VlanId.Increment(start_value = '101', step_value = '1')

ipPool1 = macPool1.Ipv4PrefixPools.add()

ixNetwork.info("Changing default Values of IP Address In Address Pools")
ipPool1.NetworkAddress.Single("222.10.0.1")
ipPool1.PrefixLength.Single("32")

ixNetwork.info("Adding DeviceGroup behind Hosts-Pool 1")
chaineddg2 = networkGroup2.DeviceGroup.add(Multiplier=1 , Name="Emulated Protocols on Host 1")

ixNetwork.info("Adding Ethernet/MAC endpoints")
mac2_1 = chaineddg2.Ethernet.add()
mac2_1.Mac.Increment(start_value="22:22:22:22:00:01", step_value="00:00:00:00:00:01")


ixNetwork.info("Addding Ipv4")
ip2_1 = mac2_1.Ipv4.add()
ip2_1.Address.Single("222.10.0.1")
ip2_1.GatewayIp.Single("222.10.0.201")
ip2_1.Prefix.Single(24)
ip2_1.ResolveGateway.Single(True)


ixNetwork.info("Creating Topology 2")
topology2 = ixNetwork.Topology.add(Name="EVPN VXLAN 2", Ports=vport['Port_2'])

ixNetwork.info("Adding Device Group")
dg2 = topology2.DeviceGroup.add(Name='Router 2', Multiplier=1)

ixNetwork.info("Adding Ethernet/MAC endpoints")
mac2 = dg2.Ethernet.add()
mac2.Mac.Increment(start_value="00:13:01:00:00:011", step_value="00:00:00:00:00:01")


ixNetwork.info("Addding Ipv4")
ip2 = mac2.Ipv4.add()
ip2.Address.Single("23.23.23.1")
ip2.GatewayIp.Single("23.23.23.2")
ip2.Prefix.Single(24)
ip2.ResolveGateway.Single(True)


ixNetwork.info("Adding BGP over IPv4")
bgp2 = ip2.BgpIpv4Peer.add()


ixNetwork.info("Setting IPs in BGP DUT IP tab")
bgp2.DutIp.Single("23.23.23.2")

ixNetwork.info("Enabling EVPN Learned Information for BGP Router")
bgp2.FilterEvpn.Single("true")

ixNetwork.info("Adding NetworkGroup behing  dg")
networkGroup3 = dg2.NetworkGroup.add(Name="VTEP Loopback Address Pool 2", Multiplier=1)
prefixPool2 = networkGroup3.Ipv4PrefixPools.add()


ixNetwork.info("Configuring  Prefix Pool")
prefixPool2.NetworkAddress.Single("200.1.0.0")
prefixPool2.PrefixLength.Single("32")


ixNetwork.info("Adding  DeviceGroup behind VTEP Loopback Address Pool 2")
chaineddg3 = networkGroup3.DeviceGroup.add(Multiplier=1, Name="VTEP 2")
loopback2 = chaineddg3.Ipv4Loopback.add(StackedLayers=[], Name="IPv4 Loopback 2")
addressSet1_2 = loopback2.Address
addressSet1_2.Increment(start_value="1.0.0.11", step_value="0.0.0.1")

ixNetwork.info("Adding BGP over IPv4 loopback in Chained DG")
bgp2_2 = loopback2.BgpIpv4Peer.add()

ixNetwork.info("Setting Ips in BGP DUT IP tab")
bgp2_2.DutIp.Single("20.33.33.11")

ixNetwork.info("Enabling EVPN Learned Information for BGP Router")
bgp2_2.FilterEvpn.Single("true")

ixNetwork.info("Adding EVPN VXLAN over BGPv4 in chained DG")
bgpIPv4EvpnVXLAN2 = bgp2_2.BgpIPv4EvpnVXLAN.add()

ixNetwork.info("Disabling Import RT List same as Export RT List")
bgpIPv4EvpnVXLAN2.ImportRtListSameAsExportRtList = 'false'
    
ixNetwork.info("Changing Import Route Target AS No.")
bgpImportRouteTargetList2 = bgpIPv4EvpnVXLAN2.BgpImportRouteTargetList.find()[0]  
bgpImportRouteTargetList2.TargetAsNumber.Increment(start_value = "0", step_value = "0")
bgpExportRouteTargetList2 = bgpIPv4EvpnVXLAN2.BgpExportRouteTargetList.find()[0]
bgpExportRouteTargetList2.TargetAsNumber.Increment(start_value="2000", step_value = "0")
bgpExportRouteTargetList2.TargetAssignedNumber.Increment(start_value='20001', step_value= "0")


ixNetwork.info("Adding Mac Pools behind EVPN VXLAN")
networkGroup4 = chaineddg3.NetworkGroup.add(Name="Hosts-Pool 2", Multiplier=1)

macPool2 = networkGroup4.MacPools.add()

ixNetwork.info("Changing Default Values of MAC Addresses in MAC Pools")
macPool2.Mac.Single("A0:11:01:00:00:01")

ixNetwork.info("Enabling using of VLAN in CMAC Ranges")
macPool2.UseVlans = "true"
cMacvlan2 = macPool2.Vlan.find()[0]
    
ixNetwork.info("Configuring VLAN ID")
cMacvlan2.VlanId.Increment(start_value = '1', step_value = '1')

ipPool2 = macPool2.Ipv4PrefixPools.add()

ixNetwork.info("Changing default Values of IP Address In Address Pools")
ipPool2.NetworkAddress.Single("222.10.0.201")
ipPool2.PrefixLength.Single("32")

ixNetwork.info("Adding DeviceGroup behind Hosts-Pool 2")
chaineddg4 = networkGroup4.DeviceGroup.add(Multiplier=1 , Name="Emulated Protocols on Host2 2")

ixNetwork.info("Adding Ethernet/MAC endpoints")
mac2_2 = chaineddg4.Ethernet.add()
mac2_2.Mac.Increment(start_value="A0:11:01:00:00:01", step_value="00:00:00:00:00:01")


ixNetwork.info("Addding Ipv4")
ip2_2 = mac2_2.Ipv4.add()
ip2_2.Address.Single("222.10.0.201")
ip2_2.GatewayIp.Single("222.10.0.1")
ip2_2.Prefix.Single(24)
ip2_2.ResolveGateway.Single(True)
ixNetwork.info("Starting protocols and waiting 60 seconds for protcols to come up")
ixNetwork.StartAllProtocols()
time.sleep(60)

#######################################################
protocolsSummary = StatViewAssistant(ixNetwork, 'Protocols Summary')
print("###############################################")
print(protocolsSummary)
allSessionsStarted = protocolsSummary.CheckCondition('Sessions Not Started', StatViewAssistant.EQUAL, 0)
protocolsSummary.AddRowFilter('Protocol Type', protocolsSummary.REGEX, '(?i)^BGP?')
noSessionsDown = protocolsSummary.CheckCondition('Sessions Down', StatViewAssistant.EQUAL, 0)
print("All Sessions Started : {}".format(allSessionsStarted))
print("No Sessions Down     : {}".format(noSessionsDown))

####################################################################
BgpPerPortStats = StatViewAssistant(ixNetwork, 'BGP Peer Per Port')
print("#############################################################")
print(BgpPerPortStats)
#print("#############################################################")
BgpPerPortStats.AddRowFilter('Port', BgpPerPortStats.EQUAL, 'Ethernet - 001')
print("#############################################################")
print("All Routes Received at Port Ethernet 001 : {}".format(BgpPerPortStats))

BgpPerPortStats.CheckCondition(ColumnName='Routes Rx', Comparator=StatViewAssistant.EQUAL, 
                               ConditionValue=100, CheckInterval=5, Timeout=60)

ixNetwork.info("Displaying EVPN-VXLAN Learned Info")
bgp2_2.GetEVPNLearnedInfo("1")

learnedInfo = bgp2_2.LearnedInfo.find()[0].Table.find()[0]

for table in learnedInfo:
    print("Table Type "+str(table.Type))
    print("Columns "+str(table.Columns))
    values = table.Values
    for value in values:
        for word in values:
            print(word)

ixNetwork.info("Stopping Protocols")
ixNetwork.StopAllProtocols()

ixNetwork.info("Test Script Ends")

