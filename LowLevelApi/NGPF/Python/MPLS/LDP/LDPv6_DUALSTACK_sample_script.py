################################################################################
# Version 1.0    Revision: 1                                                   #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    04/09/2015 - Sumeer Kumar - created sample                                #
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
#                                                                              #
# About Topology:                                                              #
#     On each port, it will create one topology of LDP dual stack router.      #
#     In each topology, there will be one device group and a network group.    #
#     The device group will simulate as a LDP dual stack router having LDP and #
#     LDPv6 interface over IPv4 and IPv6 stack respectively and a basic LDP    #
#     dual stack router connected to both IPv4 and IPv6 interface. The         #
#     transport connection preference in LDP router is set to IPv6.            #
#     The network groups consists of both IPv4 and IPv6 prefix pools.          #
#     Traffic is configured in between IPv6 prefix pools as end points.        #       
#                                                                              #
# Script Flow:                                                                 #
#    1. Configuration of protocols as described in topology.                   #
#    2. Start the LDP protocol.                                                #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Change LDP FEC labels & apply change on the fly                        #
#    6. Retrieve protocol learned info again.                                  #
#    7. Configure L2-L3 traffic.                                               #
#    8. Start the L2-L3 traffic.                                               #
#   11. Retrieve L2-L3 traffic stats.                                          #
#   12. Stop L2-L3 traffic.                                                    #
#   13. Stopallprotocols.                                                      #
#                                                                              #                                                                                
# Ixia Software:                                                               #
#    IxOS      6.90 EA                                                         #
#    IxNetwork 7.50 EA                                                         #
#                                                                              #
################################################################################

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
# IxNetwork.py file somewhere else where we python can autoload it.
# "IxNetwork.py" is available in <IxNetwork_installer_path>\API\Python
################################################################################
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\7.40-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.205.28.41'
ixTclPort   = '8981'
ports       = [('10.205.28.12', '6', '1',), ('10.205.28.12', '6', '2',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("Connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '7.40', '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("Cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

# assigning ports
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

root    = ixNet.getRoot()
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]


print("Adding two topologies")
ixNet.add(ixNet.getRoot(), 'topology', '-vports', vportTx)
ixNet.add(ixNet.getRoot(), 'topology', '-vports', vportRx)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

print("Adding one device group in each topology")
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(t1dev1, '-multiplier', '1')
ixNet.setAttribute(t2dev1, '-multiplier', '1')
ixNet.commit()

print("Adding Ethernet/MAC endpoints for the device groups")
ixNet.add(t1dev1, 'ethernet')
ixNet.add(t2dev1, 'ethernet')
ixNet.commit()

mac1 = (ixNet.getList(t1dev1, 'ethernet'))[0]
mac2 = (ixNet.getList(t2dev1, 'ethernet'))[0]

print("Configuring the MAC addresses for the device groups")
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
        '-direction', 'increment',
        '-start',     '00:11:01:00:00:01',
        '-step',      '00:00:00:00:00:01')

ixNet.setAttribute(ixNet.getAttribute(mac2, '-mac') + '/singleValue',
        '-value', '00:12:01:00:00:01')
ixNet.commit()

print("Adding IPv4 and IPv6 over Ethernet stack for both device groups")
ixNet.add(mac1, 'ipv4')
ixNet.add(mac2, 'ipv4')
ixNet.add(mac1, 'ipv6')
ixNet.add(mac2, 'ipv6')
ixNet.commit()

ipv41 = (ixNet.getList(mac1, 'ipv4'))[0]
ipv42 = (ixNet.getList(mac2, 'ipv4'))[0]
ipv61 = (ixNet.getList(mac1, 'ipv6'))[0]
ipv62 = (ixNet.getList(mac2, 'ipv6'))[0]

mvAddv41 = ixNet.getAttribute(ipv41, '-address')
mvAddv42 = ixNet.getAttribute(ipv42, '-address')
mvAddv61 = ixNet.getAttribute(ipv61, '-address')
mvAddv62 = ixNet.getAttribute(ipv62, '-address')

mvGwv41  = ixNet.getAttribute(ipv41, '-gatewayIp')
mvGwv42  = ixNet.getAttribute(ipv42, '-gatewayIp')
mvGwv61  = ixNet.getAttribute(ipv61, '-gatewayIp')
mvGwv62  = ixNet.getAttribute(ipv62, '-gatewayIp')

print("Configuring IPv4 addresses for both device groups")
ixNet.setAttribute(mvAddv41 + '/singleValue', '-value', '100.1.0.2')
ixNet.setAttribute(mvAddv42 + '/singleValue', '-value', '100.1.0.1')
ixNet.setAttribute(mvGwv41 + '/singleValue', '-value', '100.1.0.1')
ixNet.setAttribute(mvGwv42 + '/singleValue', '-value', "100.1.0.2")

print("Configuring IPv6 addresses for both device groups")
ixNet.setAttribute(mvAddv61 + '/singleValue', '-value', '2000:0:0:1:0:0:0:2')
ixNet.setAttribute(mvAddv62 + '/singleValue', '-value', '2000:0:0:1:0:0:0:1')
ixNet.setAttribute(mvGwv61 + '/singleValue', '-value', '2000:0:0:1:0:0:0:1')
ixNet.setAttribute(mvGwv62 + '/singleValue', '-value', "2000:0:0:1:0:0:0:2")

print("Configuring IPv4 prefix for both device groups")
ixNet.setAttribute(ixNet.getAttribute(ipv41, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ipv42, '-prefix') + '/singleValue', '-value', '24')

print("Configuring IPv6 prefix for both device groups")
ixNet.setAttribute(ixNet.getAttribute(ipv61, '-prefix') + '/singleValue', '-value', '64')
ixNet.setAttribute(ixNet.getAttribute(ipv62, '-prefix') + '/singleValue', '-value', '64')

ixNet.setMultiAttribute(ixNet.getAttribute(ipv41, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv42, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv61, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv62, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

print("Adding LDP Connected Interface over IPv4 stack")
ixNet.add(ipv41, 'ldpConnectedInterface')
ixNet.add(ipv42, 'ldpConnectedInterface')
ixNet.commit()

ldpIf1 = ixNet.getList(ipv41, 'ldpConnectedInterface')[0]
ldpIf2 = ixNet.getList(ipv42, 'ldpConnectedInterface')[0]

print("Adding LDPv6 Connected Interface over IPv6 stack")
ixNet.add(ipv61, 'ldpv6ConnectedInterface')
ixNet.add(ipv62, 'ldpv6ConnectedInterface')
ixNet.commit()

ldpv6If1 = ixNet.getList(ipv61, 'ldpv6ConnectedInterface')[0]
ldpv6If2 = ixNet.getList(ipv62, 'ldpv6ConnectedInterface')[0]

print("Adding LDPv6 dual stack router in both device groups")
ixNet.add(t1dev1, 'ldpBasicRouterV6')
ixNet.add(t2dev1, 'ldpBasicRouterV6')
ixNet.commit()

ldpv6DualStackRouter1 = ixNet.getList(t1dev1, 'ldpBasicRouterV6')[0]
ldpv6DualStackRouter2 = ixNet.getList(t2dev1, 'ldpBasicRouterV6')[0]

ixNet.setAttribute(ipv41, '-stackedLayers', ldpv6DualStackRouter1)
ixNet.setAttribute(ipv61, '-stackedLayers', ldpv6DualStackRouter1)

ixNet.setAttribute(ipv42, '-stackedLayers', ldpv6DualStackRouter2)
ixNet.setAttribute(ipv62, '-stackedLayers', ldpv6DualStackRouter2)
ixNet.commit()

print("Setting IPv6 as transport connection preference")
sessionPreference1 = ixNet.getAttribute(ldpv6DualStackRouter1, '-sessionPreference')
sessionPreference2 = ixNet.getAttribute(ldpv6DualStackRouter2, '-sessionPreference')

singleValue1 = ixNet.getList(sessionPreference1, 'singleValue')[0]
singleValue2 = ixNet.getList(sessionPreference2, 'singleValue')[0]

ixNet.setAttribute(singleValue1, '-value', 'ipv6')
ixNet.setAttribute(singleValue2, '-value', 'ipv6')
ixNet.commit()

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'LDPv6 Topology 1')
ixNet.setAttribute(topo2, '-name', 'LDPv6 Topology 2')

ixNet.setAttribute(t1dev1, '-name', 'LDP Dual Stack Router 1')
ixNet.setAttribute(t2dev1, '-name', 'LDP Dual Stack Router 2')
ixNet.commit()

print("Adding Network Group behind LDPv6 dual stack DG")
ixNet.add(t1dev1, 'networkGroup')
ixNet.add(t2dev1, 'networkGroup')
ixNet.commit()

networkGroup1 = ixNet.getList(t1dev1, 'networkGroup')[0]
networkGroup2 = ixNet.getList(t2dev1, 'networkGroup')[0]

ixNet.setAttribute(networkGroup1, '-name', 'LDP_1_Network_Group1')
ixNet.setAttribute(networkGroup2, '-name', 'LDP_2_Network_Group1')
ixNet.setAttribute(networkGroup1, '-multiplier', '1')
ixNet.setAttribute(networkGroup2, '-multiplier', '1')
ixNet.commit()

print("Adding IPv4 and Ipv6 prefix pools in Network Groups")
ixNet.add(networkGroup1, 'ipv6PrefixPools')
ixNet.add(networkGroup1, 'ipv4PrefixPools')
ixNet.add(networkGroup2, 'ipv6PrefixPools')
ixNet.add(networkGroup2, 'ipv4PrefixPools')
ixNet.commit()

ipv6PrefixPools1 = ixNet.getList(networkGroup1, 'ipv6PrefixPools')[0]
ipv4PrefixPools1 = ixNet.getList(networkGroup1, 'ipv4PrefixPools')[0]

ipv6PrefixPools2 = ixNet.getList(networkGroup2, 'ipv6PrefixPools')[0]
ipv4PrefixPools2 = ixNet.getList(networkGroup2, 'ipv4PrefixPools')[0]

print("Changing count of network group address")
ixNet.setMultiAttribute(ipv6PrefixPools1, '-numberOfAddresses', '5')
ixNet.setMultiAttribute(ipv4PrefixPools1, '-numberOfAddresses', '5')
ixNet.setMultiAttribute(ipv6PrefixPools2, '-numberOfAddresses', '5')
ixNet.setMultiAttribute(ipv4PrefixPools2, '-numberOfAddresses', '5')
ixNet.commit()

print("All configuration is completed..Wait for 5 seconds...")
time.sleep(5)

################################################################################
# Start LDPv6 protocol and wait for 60 seconds                                 #  
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')      
time.sleep(60)

################################################################################
# Retrieve protocol statistics                                                 #
################################################################################
print("Fetching LDP Per Port Stats")
viewPage  = '::ixNet::OBJ-/statistics/view:"LDP Per Port"/page'
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

#################################################################################
# Retrieve protocol learned info                                                #
#################################################################################
print("Fetching LDPv6 Basic Learned Info")
ixNet.execute('getIPv4FECLearnedInfo', ldpv6DualStackRouter1, '1')
ixNet.execute('getIPv6FECLearnedInfo', ldpv6DualStackRouter1, '1')
time.sleep(5)
linfoList  = (ixNet.getList(ldpv6DualStackRouter1, 'learnedInfo'))
for linfo in linfoList :
    values = ixNet.getAttribute(linfo, '-values')
    print("***************************************************")
    for v in values :
        print(v)
    # end for
    print("***************************************************")
# end for

################################################################################
# Change the labels of FEC elements                                            #
################################################################################
print("Changing Labels of LDP and LDPv6 FEC Range on second Network Group")
ldpFEC2 = ixNet.getList(ipv4PrefixPools2, 'ldpFECProperty')[0]
ldpv6FEC2 = ixNet.getList(ipv6PrefixPools2, 'ldpIpv6FECProperty')[0]

labelV4MultiValue2 = ixNet.getAttribute(ldpFEC2, '-labelValue')
ixNet.setMultiAttribute(labelV4MultiValue2, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()
labelSetV4 = ixNet.add(labelV4MultiValue2, 'counter')
ixNet.setMultiAttribute(labelSetV4, '-step', '5', '-start', '30', '-direction', 'increment')

labelV6MultiValue2 = ixNet.getAttribute(ldpv6FEC2, '-labelValue')
ixNet.setMultiAttribute(labelV6MultiValue2, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()
labelSetV6 = ixNet.add(labelV6MultiValue2, 'counter')
ixNet.setMultiAttribute(labelSetV6, '-step', '10', '-start', '60', '-direction', 'decrement')
ixNet.commit()
time.sleep(2)

################################################################################
# Applying changes one the fly                                                 #
################################################################################
print("Applying changes on the fly")
globals   = ixNet.getRoot() + '/globals'
topology  = globals + '/topology'
ixNet.execute('applyOnTheFly', topology)
time.sleep(5)

#################################################################################
# Retrieve protocol learned info again                                          #
#################################################################################
print("Fetching LDPv6 Basic Learned Info again after changing labels on the fly")
ixNet.execute('getIPv4FECLearnedInfo', ldpv6DualStackRouter1, '1')
ixNet.execute('getIPv6FECLearnedInfo', ldpv6DualStackRouter1, '1')
time.sleep(5)
linfoList  = (ixNet.getList(ldpv6DualStackRouter1, 'learnedInfo'))
for linfo in linfoList :
    values = ixNet.getAttribute(linfo, '-values')
    print("***************************************************")
    for v in values :
        print(v)
    # end for
    print("***************************************************")
# end for


#################################################################################
# Configure L2-L3 traffic                                                       #
#################################################################################
print ("Congfiguring L2/L3 Traffic Item")
trafficItem1 = ixNet.add((ixNet.getRoot()) + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-biDirectional', 'true',
    '-trafficType', 'ipv6')
ixNet.commit()

trafficItem1    = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
source       = [networkGroup1 + '/ipv6PrefixPools:1']
destination  = [networkGroup2 + '/ipv6PrefixPools:1']

ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', (''),
    '-scalableSources',       (''),
    '-multicastReceivers',    (''),
    '-scalableDestinations',  (''),
    '-ngpfFilters',           (''),
    '-trafficGroups',         (''),
    '-sources',               source,
    '-destinations',          destination)
ixNet.commit()

ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['mplsFlowDescriptor0','trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''))
ixNet.commit()

###############################################################################
# Apply L2/L3 traffic                                                         #
###############################################################################
print("Applying L2/L3 traffic")
ixNet.execute('apply', (ixNet.getRoot()) + '/traffic')
time.sleep(5)

###############################################################################
# Start L2/L3 traffic                                                         #
###############################################################################
print("Starting L2/L3 traffic")
ixNet.execute('start', (ixNet.getRoot()) + '/traffic')

print("Let traffic run for 60 seconds")
time.sleep(60)

###############################################################################
# Retrieve L2/L3 traffic item statistics                                      #
###############################################################################
print("Retrieving all L2/L3 traffic stats")
viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page'
statcap =  ixNet.getAttribute(viewPage, '-columnCaptions')
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

#################################################################################
# Stop L2/L3 traffic                                                            #
#################################################################################
print("Stopping L2/L3 traffic")
ixNet.execute('stop', (ixNet.getRoot()) + '/traffic')
time.sleep(5)

################################################################################
# Stop all protocols                                                          #
################################################################################
print("Stopping all protocols")
ixNet.execute('stopAllProtocols')

print("!!! Test Script Ends !!!")
