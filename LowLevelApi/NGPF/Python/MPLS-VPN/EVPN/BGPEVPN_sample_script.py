# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    04/12/2015 - Poulomi Chatterjee - created sample                          #
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
#    This script intends to demonstrate how to use NGPF BGP EVPN Python API.   #
#                                                                              #
#    1. It will create 2 BGP EVPN topologies, each having LDP configured in    #
#        connected Device Group .BGP EVPN configured in chained device group   #
#        along with Mac pools connected behind the chained Device Group.       #
#    2. Start all protocol.                                                    #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Configure L2-L3 traffic.                                               #
#    6. Start the L2-L3 traffic.                                               #
#    7. Retrieve L2-L3 traffic stats.                                          #
#    8. Stop L2-L3 traffic.                                                    #
#    9. Stopallprotocols.                                                      #
# Ixia Software:                                                               #
#    IxOS      8.00 EA                                                         #
#    IxNetwork 8.00 EA                                                         # 
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
# IxNetwork.pm file somewhere else where we python can autoload it.
# "IxNetwork.pm" is available in <IxNetwork_installer_path>\API\Python
################################################################################
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.00.1026.7-EB\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.216.104.58'
ixTclPort   = '8350'
#ports       = [('10.216.108.82', '2', '7'), ('10.216.108.82', '2', '8')]
ports       = [('10.216.108.46', '2', '3'), ('10.216.108.46', '2', '4')]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.00',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

# assigning ports
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

root    = ixNet.getRoot()
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]

print("adding topologies")
ixNet.add(root, 'topology', '-vports', vportTx)
ixNet.add(root, 'topology', '-vports', vportRx)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

print "Adding 2 device groups"
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

print("Adding ethernet/mac endpoints")
ixNet.add(t1dev1, 'ethernet')
ixNet.add(t2dev1, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = ixNet.getList(t2dev1, 'ethernet')[0]

print("Configuring the mac addresses %s" % (mac1))
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '18:03:73:C7:6C:B1',
    '-step',      '00:00:00:00:00:01')

ixNet.setAttribute(ixNet.getAttribute(mac2, '-mac') + '/singleValue',
    '-value', '18:03:73:C7:6C:01')
ixNet.commit()

#print ("ixNet.help ::ixNet::OBJ-/topology/deviceGroup/ethernet")
#print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet'))

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
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '20.20.20.2')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '20.20.20.2')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

#print ("ixNet.help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4")
#print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4'))

print("Adding ldp over IP4 stacks")
ixNet.add(ip1, 'ldpBasicRouter')
ixNet.add(ip2, 'ldpBasicRouter')
ixNet.commit()

ldp1 = ixNet.getList(ip1, 'ldpBasicRouter')[0]
ldp2 = ixNet.getList(ip2, 'ldpBasicRouter')[0]

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'EVPN Topology 1')
ixNet.setAttribute(topo2, '-name', 'EVPN  Topology 2')

ixNet.setAttribute(t1dev1, '-name', 'LDP Router1')
ixNet.setAttribute(t2dev1, '-name', 'LDP Router2')
ixNet.commit()


#print ("ixNet.help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp")
#print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp'))

print("Adding NetworkGroup behind ldp DG")
ixNet.execute('createDefaultStack', t1devices, 'ipv4PrefixPools')
ixNet.execute('createDefaultStack', t2devices, 'ipv4PrefixPools')

networkGroup1 = ixNet.getList(t1dev1, 'networkGroup')[0]
networkGroup2 = ixNet.getList(t2dev1, 'networkGroup')[0]

ixNet.setAttribute(networkGroup1, '-name', 'LDP_1_Network_Group1')
ixNet.setAttribute(networkGroup2, '-name', 'LDP_2_Network_Group1')
ixNet.setAttribute(networkGroup1, '-multiplier', '1')
ixNet.setAttribute(networkGroup2, '-multiplier', '1')

print("Configuring LDP prefixes")
ldpPrefixPool1 = ixNet.getList(networkGroup1, 'ipv4PrefixPools')[0]
ldpPrefixPool2 = ixNet.getList(networkGroup2, 'ipv4PrefixPools')[0]
ixNet.setAttribute(ixNet.getAttribute(ldpPrefixPool1, '-networkAddress') + '/singleValue', '-value', '2.2.2.2')
ixNet.setAttribute(ixNet.getAttribute(ldpPrefixPool2, '-networkAddress') + '/singleValue', '-value', '3.2.2.2')
ixNet.setAttribute(ixNet.getAttribute(ldpPrefixPool1, '-prefixLength') + '/singleValue', '-value', '32')
ixNet.setAttribute(ixNet.getAttribute(ldpPrefixPool2, '-prefixLength') + '/singleValue', '-value', '32')
ixNet.commit()

# Add ipv4 loopback1 for applib traffic
print("Adding ipv4 loopback1 for applib traffic")
chainedDg1 = ixNet.add(networkGroup1, 'deviceGroup')
ixNet.setMultiAttribute(chainedDg1, '-multiplier', '1', '-name', 'Device Group 3')
ixNet.commit()
chainedDg1 = ixNet.remapIds(chainedDg1)[0]

loopback1 = ixNet.add(chainedDg1, 'ipv4Loopback')
ixNet.setMultiAttribute(loopback1, '-stackedLayers', [], '-name', 'IPv4 Loopback 1')
ixNet.commit()

connector1 = ixNet.add(loopback1, 'connector')
ixNet.setMultiAttribute(connector1, '-connectedTo', networkGroup1 + '/ipv4PrefixPools:1')
ixNet.commit()
connector1 = ixNet.remapIds(connector1)[0]

addressSet1 = ixNet.getAttribute(loopback1, '-address')
ixNet.setMultiAttribute(addressSet1, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

addressSet1 = ixNet.add(addressSet1, 'counter')
ixNet.setMultiAttribute(addressSet1, '-step', '0.0.0.1', '-start', '2.2.2.2', '-direction', 'increment')
ixNet.commit()
addressSet1 = ixNet.remapIds(addressSet1)[0]

# Add ipv4 loopback2 for applib traffic
print("Adding ipv4 loopback2 for applib traffic")
chainedDg2 = ixNet.add(networkGroup2, 'deviceGroup')
ixNet.setMultiAttribute(chainedDg2, '-multiplier', '1', '-name', 'Device Group 4')
ixNet.commit()
chainedDg2 = ixNet.remapIds(chainedDg2)[0]

loopback2 = ixNet.add(chainedDg2, 'ipv4Loopback')
ixNet.setMultiAttribute(loopback2, '-stackedLayers', [], '-name', 'IPv4 Loopback 2')
ixNet.commit()

connector2 = ixNet.add(loopback2, 'connector')
ixNet.setMultiAttribute(connector2, '-connectedTo', networkGroup2 + '/ipv4PrefixPools:1')
ixNet.commit()
connector1 = ixNet.remapIds(connector2)[0]

addressSet2 = ixNet.getAttribute(loopback2, '-address')
ixNet.setMultiAttribute(addressSet2, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

addressSet2 = ixNet.add(addressSet2, 'counter')
ixNet.setMultiAttribute(addressSet2, '-step', '0.0.0.1 ', '-start', '3.2.2.2', '-direction', 'increment')
ixNet.commit()
addressSet2 = ixNet.remapIds(addressSet2)[0]

print("Adding BGP over IPv4 loopback interfaces")
ixNet.add(loopback1, 'bgpIpv4Peer')
ixNet.add(loopback2, 'bgpIpv4Peer')
ixNet.commit()
bgp1 = ixNet.getList(loopback1, 'bgpIpv4Peer')[0]
bgp2 = ixNet.getList(loopback2, 'bgpIpv4Peer')[0]

print("Setting IPs in BGP DUT IP tab")
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-dutIp') + '/singleValue', '-value', '3.2.2.2')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-dutIp') + '/singleValue', '-value', '2.2.2.2')
ixNet.commit()

print("Enabling EVPN Learned Information for BGP Router")
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterEvpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterEvpn') + '/singleValue', '-value', 'true')
ixNet.commit()

print("Adding EVPN EVI over BGP in both ports")
ixNet.add(bgp1, 'bgpIPv4EvpnEvi')
ixNet.add(bgp2, 'bgpIPv4EvpnEvi')
ixNet.commit()

EvpnEvi1 = ixNet.getList(bgp1, 'bgpIPv4EvpnEvi')[0]
EvpnEvi2 = ixNet.getList(bgp2, 'bgpIPv4EvpnEvi')[0]

print("Configuring ESI value in both ports")
ethernetSegment1 = ixNet.getList(bgp1, 'bgpEthernetSegmentV4')[0]
ethernetSegment2 = ixNet.getList(bgp2, 'bgpEthernetSegmentV4')[0]
ixNet.setAttribute(ixNet.getAttribute(ethernetSegment1, '-esiValue') + '/singleValue', '-value', '1')
ixNet.setAttribute(ixNet.getAttribute(ethernetSegment2, '-esiValue') + '/singleValue', '-value', '2')
ixNet.commit()

print("Adding Mac Pools behind EVPN DG")
ixNet.execute('createDefaultStack', chainedDg1, 'macPools')
ixNet.execute('createDefaultStack', chainedDg2, 'macPools')

networkGroup3 = ixNet.getList(chainedDg1, 'networkGroup')[0]
networkGroup4 = ixNet.getList(chainedDg2, 'networkGroup')[0]

ixNet.setAttribute(networkGroup3, '-name', 'MAC_Pool_1')
ixNet.setAttribute(networkGroup4, '-name', 'MAC_Pool_2')
ixNet.setAttribute(networkGroup3, '-multiplier', '1')
ixNet.setAttribute(networkGroup4, '-multiplier', '1')

print("Adding IPv4 addresses over MAC pools")
macPool1 = ixNet.getList(networkGroup3, 'macPools')[0]
macPool2 = ixNet.getList(networkGroup4, 'macPools')[0]
ixNet.add(macPool1, 'ipv4PrefixPools')
ixNet.add(macPool2, 'ipv4PrefixPools')
ixNet.commit()

print("Changing default values of MAC Addresses in MAC Pools")
ixNet.setAttribute(ixNet.getAttribute(macPool1, '-mac') + '/singleValue', '-value', 'A0:11:01:00:00:03')
ixNet.setAttribute(ixNet.getAttribute(macPool2, '-mac') + '/singleValue', '-value', 'A0:12:01:00:00:03')

print("Changing default values of MAC labels")
cMAC1 = ixNet.getList(macPool1, 'cMacProperties')[0]
cMAC2 = ixNet.getList(macPool2, 'cMacProperties')[0]
ixNet.setAttribute(ixNet.getAttribute(cMAC1, '-firstLabelStart') + '/singleValue', '-value', '1000')
ixNet.setAttribute(ixNet.getAttribute(cMAC2, '-firstLabelStart') + '/singleValue', '-value', '2000')

print("Changing default values of IP prefixes")
ipv4PrefixPool1 = ixNet.getList(macPool1, 'ipv4PrefixPools')[0]
ipv4PrefixPool2 = ixNet.getList(macPool2, 'ipv4PrefixPools')[0]
ixNet.setAttribute(ixNet.getAttribute(ipv4PrefixPool1, '-networkAddress') + '/singleValue', '-value', '11.11.11.1')
ixNet.setAttribute(ixNet.getAttribute(ipv4PrefixPool2, '-networkAddress') + '/singleValue', '-value', '12.12.12.1')
ixNet.commit()

################################################################################
# 2. Start protocols and wait for 60 seconds
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
# 4. Retrieve protocol learned info
###############################################################################
print("Fetching EVPN Learned Info")
ixNet.execute('getEVPNLearnedInfo', bgp1)
time.sleep(5)

linfo  = ixNet.getList(bgp1, 'learnedInfo')[0]
linfoList = ixNet.getList(linfo, 'table')

print("***************************************************")
for table in linfoList :
     tableType = ixNet.getAttribute(table, '-type')
     print(tableType)
     print("=================================================")
     columns = ixNet.getAttribute(table, '-columns')
     print(columns)
     values = ixNet.getAttribute(table, '-values')
     for value in values :
          for word in values :
               print(word)
          #end for
      # end for
# end for
print("***************************************************")

################################################################################
# 5. Configure L2-L3 traffic
################################################################################
print("Congfiguring L2-L3 Traffic Item")
trafficItem1 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ethernetVlan')
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
source       = [networkGroup3 + '/macPools:1']
destination  = [networkGroup4 + '/macPools:1']

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
    '-trackBy',        ['mplsFlowDescriptor0', 'trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         [])
ixNet.commit()


###############################################################################
# 6. Apply and start L2/L3 traffic
###############################################################################
print ('applying L2/L3 traffic')
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)

print ('starting L2/L3 traffic')
ixNet.execute('start', ixNet.getRoot() + '/traffic')

###############################################################################
# 7. Retrieve L2/L3 traffic item statistics
###############################################################################
print ('Verifying all the L2-L3 traffic stats')
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

################################################################################
# 8. Stop L2/L3 traffic
################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)

################################################################################
# 9. Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
