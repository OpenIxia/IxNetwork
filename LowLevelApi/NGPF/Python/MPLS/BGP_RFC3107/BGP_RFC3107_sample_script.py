# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    14/06/2016 - Debarati Chakraborty - created sample                        #
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

#################################################################################
#                                                                               #
# Description:                                                                  #
#    This script intends to demonstrate how to use NGPF BGP RFC 3107 TCL APIs   #
#    About Topology:                                                            #
#       The scenario consists of two BGP peers.                                 #
#       Each of them capable of carrying Label information for the attached     #
#       advertising Route Range. Unidirectional Traffic is created in between   #
#       the peers.                                                              #
#         Script Flow:                                                          #
#        Step 1. Creation of 2 BGP topologies with RFC3107 IPv4 MPLS Capability #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Stat display                                          #
#        Step 4. Learned Info display                                           #
#        Step 5. Configuration L2-L3 Traffic                                    #
#        Step 6. Apply and Start of L2-L3 traffic                               #
#        Step 7. Display of L2-L3  traffic Stats                                #
#        Step 8.Stop of L2-L3 traffic                                           #
#        Step 9.Stop of all protocols                                           #
#################################################################################
# Ixia Software Used to develop the script:                                     #
#    IxOS      8.10 EA                                                          #
#    IxNetwork 8.10 EA                                                          #
#                                                                               #
#################################################################################
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
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.10-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.216.104.58'
ixTclPort   = '8239'
ports       = [('10.216.108.82', '7', '15',), ('10.216.108.82', '7', '16',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.10',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')
#################################################################################
# Step 1> protocol configuration section
#################################################################################

# assigning ports
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

root    = ixNet.getRoot()
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]
# Creating topology and device group
print("adding topologies")
ixNet.add(root, 'topology', '-vports', vportTx)
ixNet.add(root, 'topology', '-vports', vportRx)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]
print ('Renaming the topologies and the device groups')
ixNet.setAttribute(topo1, '-name', 'BGP Topology 1')
ixNet.setAttribute(topo2, '-name', 'BGP Topology 2')
print ("Adding 2 device groups")
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]
ixNet.setAttribute(t1dev1, '-name', 'BGP Router 1')
ixNet.setAttribute(t2dev1, '-name', 'BGP Router 2')
ixNet.commit()

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(t1dev1, '-multiplier', '1')
ixNet.setAttribute(t2dev1, '-multiplier', '1')
ixNet.commit()
#  Adding ethernet stack and configuring MAC
print("Adding ethernet/mac endpoints")
ixNet.add(t1dev1, 'ethernet')
ixNet.add(t2dev1, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = ixNet.getList(t2dev1, 'ethernet')[0]

print("Configuring the mac addresses %s" % (mac1))
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '22:22:22:22:22:22',
    '-step',      '00:00:00:00:00:01')

ixNet.setAttribute(ixNet.getAttribute(mac2, '-mac') + '/singleValue',
    '-value', '44:44:44:44:44:44')
ixNet.commit()
#  Adding IPv4 stack and configuring  IP Address
print("Add ipv4")
ixNet.add(mac1, 'ipv4')
ixNet.add(mac2, 'ipv4')
ixNet.commit()
ip1 = ixNet.getList(mac1, 'ipv4')[0]
ip2 = ixNet.getList(mac2, 'ipv4')[0]
mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvAdd2 = ixNet.getAttribute(ip2, '-address')
mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = ixNet.getAttribute(ip2, '-gatewayIp')

print("configuring ipv4 addresses")
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '50.50.50.2')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '50.50.50.1')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '50.50.50.1')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '50.50.50.2')
ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')
ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

#  Adding BGP and configuring it
print("Adding BGP over IP4 stacks")
ixNet.add(ip1, 'bgpIpv4Peer')
ixNet.add(ip2, 'bgpIpv4Peer')
ixNet.commit()

bgp1 = ixNet.getList(ip1, 'bgpIpv4Peer')[0]
bgp2 = ixNet.getList(ip2, 'bgpIpv4Peer')[0]

print('Enabling IPv4 MPLS Capability in the BGP Peers')
ixNet.setMultiAttribute(bgp1, '-ipv4MplsCapability', 'true')
ixNet.commit()

ixNet.setMultiAttribute(bgp2, '-ipv4MplsCapability', 'true')
ixNet.commit()

print("Setting IPs in BGP DUT IP tab")
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-dutIp') + '/singleValue', '-value', '50.50.50.1')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-dutIp') + '/singleValue', '-value', '50.50.50.2')
ixNet.commit()

print("Adding NetworkGroup behind BGP DG")
networkGroup1 = ixNet.add(t1dev1, 'networkGroup')
ixNet.commit()
networkGroup1 = ixNet.remapIds(networkGroup1)[0]
ipv4PrefixPools1 = ixNet.add(networkGroup1, 'ipv4PrefixPools')
ixNet.commit()

networkGroup2 = ixNet.add(t2dev1, 'networkGroup')
ixNet.commit()
networkGroup2 = ixNet.remapIds(networkGroup2)[0]
ipv4PrefixPools2 = ixNet.add(networkGroup2, 'ipv4PrefixPools')
ixNet.commit()

print("Configuring the number of addresses")

ixNet.setMultiAttribute(ipv4PrefixPools1, '-numberOfAddresses', '5')
ixNet.commit()

ixNet.setMultiAttribute(ipv4PrefixPools2, '-numberOfAddresses', '5')
ixNet.commit()

print ('Enabling BGP 3107 advertising capability in BGP Peer')
bgpIPRouteProp1 = ixNet.getList(ipv4PrefixPools1, 'bgpIPRouteProperty')[0]
ixNet.setMultiAttribute(bgpIPRouteProp1, '-advertiseAsBgp3107', 'true')
ixNet.commit()
bgpIPRouteProp1 = ixNet.remapIds(bgpIPRouteProp1)[0]

bgpIPRouteProp2 = ixNet.getList(ipv4PrefixPools2, 'bgpIPRouteProperty')[0]
ixNet.setMultiAttribute(bgpIPRouteProp2, '-advertiseAsBgp3107', 'true')
ixNet.commit()

print ('Editing Label values in BGP IP Route Ranges')
labelStrt_1 = ixNet.getAttribute(bgpIPRouteProp1, '-labelStart')
ixNet.setMultiAttribute(labelStrt_1, '-clearOverlays', 'false')
ixNet.commit()
ixNet.add(labelStrt_1, 'singleValue')
ixNet.setMultiAttribute(labelStrt_1 + '/singleValue', '-value', '1006')
ixNet.commit()

labelStrt_2 = ixNet.getAttribute(bgpIPRouteProp2, '-labelStart')
ixNet.setMultiAttribute(labelStrt_2, '-clearOverlays', 'false')
ixNet.commit()
ixNet.add(labelStrt_2, 'singleValue')
ixNet.setMultiAttribute(labelStrt_2 + '/singleValue', '-value', '2006')
ixNet.commit()

print ('Enabling IPv4 MPLS Learned Information for BGP Routers')
filterIpV4Mpls1 = ixNet.getAttribute(bgp1, '-filterIpV4Mpls')
filterIpV4Mpls2 = ixNet.getAttribute(bgp2, '-filterIpV4Mpls')

sv1 = filterIpV4Mpls1 + '/singleValue'
sv2 = filterIpV4Mpls2 + '/singleValue'

ixNet.setAttribute(sv1, '-value', 'true')
ixNet.setAttribute(sv2, '-value', 'true')
ixNet.commit()

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(networkGroup1, '-multiplier', '5')
ixNet.setAttribute(networkGroup2, '-multiplier', '5')
ixNet.commit()
print ('************************************************************')

################################################################################
# Step 2> Start of protocol.
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)
################################################################################
# Step 3> Retrieve protocol statistics.
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
# Step 4> Retrieve protocol learned info
###############################################################################
print("Fetching BGP Learned Info")
ixNet.execute('getIPv4MplsLearnedInfo', bgp1, '1')
time.sleep(5)
linfo  = ixNet.getList(bgp1, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')
print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# Step 5> Configure L2-L3 traffic
################################################################################
print("Configuring L2-L3 Traffic Item")
trafficItem1 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, '-name', 'IPv4 Traffic 1',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv4')
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
source   = [ixNet.getList(networkGroup1, 'ipv4PrefixPools')[0]]
destination   = [ixNet.getList(networkGroup2, 'ipv4PrefixPools')[0]]

ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', [],
    '-scalableSources',       [],
    '-multicastReceivers',    [],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source,
    '-destinations',          destination)
ixNet.commit()

ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'trackingenabled0', 'mplsMplsLabelValue0', 'ipv4DestIp0', 'ipv4SourceIp0'])
ixNet.commit()

###############################################################################
# Step 8> Apply and start L2/L3 traffic
###############################################################################
print ("applying L2/L3 traffic")
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)

print ("starting L2/L3 traffic")
ixNet.execute('start', ixNet.getRoot() + '/traffic')

print ("let traffic run for 120 second")
time.sleep(120)
###############################################################################
# Step 9> Retrieve L2/L3 traffic item statistics.
###############################################################################
print ("Verifying all the L2-L3 traffic stats")
viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page'
statcap =  ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-34s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")
################################################################################
# Step 10> Stop L2/L3 traffic.
################################################################################
print ("Stopping L2/L3 traffic")
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)
################################################################################
# Step 11> Stop all protocols.
################################################################################
print ("Stopping protocols")
ixNet.execute('stopAllProtocols')
print ("!!! Test Script Ends !!!")
