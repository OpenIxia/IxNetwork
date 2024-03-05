# -*- coding: cp1252 -*-
################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
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
#    This script intends to demonstrate how to use NGPF BGP API to configure   #
#     H-L3vpn Scenario.                                                        #
#                                                                              #
#    1. It will create a BGP topology with OSPF, RSVP-TE and Targeted LDP      #
#       configured in Area Border Router.                                      #
#    2. In Provider Edge Router configuration  BGP Peer is configured.         #
#    3. BGP VRF is configured on top of BGP Peer.                              #
#    4. IPv4 & IPv6 Prefix Pools are added behind BGP VRF.                     #
#    5. IPv4 and IPv6 addresses  are configured in IPv4 and IPv6 Prefix Pools. #
#    6. Label values are configured in V4 & V6 Prefix Pools.                   #
#    3. Only one side configuration is provided.                               #
#    4. Traffic configuration will be similar to L3VPN scenario.               #
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
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.20-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
# Script Starts
print("!!!L3VPN Option C Test Script Starts !!!")
ixTclServer = '10.216.108.113'
ixTclPort   = '8650'
ports       = [('10.216.108.82', '7', '11'), ('10.216.108.82', '7', '12')]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.20',
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

print("Adding topology")
ixNet.add(root, 'topology', '-vports', vportTx)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]

print ("Adding device group")
ixNet.add(topo1, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')

t1dev1 = t1devices[0]

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(t1dev1, '-multiplier', '1')
ixNet.commit()

print("Adding ethernet/mac endpoints")
ixNet.add(t1dev1, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]

print("Configuring the mac addresses %s" % (mac1))
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '18:03:73:C7:6C:B1',
    '-step',      '00:00:00:00:00:01')

ixNet.commit()

#print ("ixNet.help ::ixNet::OBJ-/topology/deviceGroup/ethernet")
#print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet'))

print("Add ipv4")
ixNet.add(mac1, 'ipv4')
ixNet.commit()

ip1 = ixNet.getList(mac1, 'ipv4')[0]

mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')

print("configuring ipv4 addresses")
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '20.20.20.2')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '20.20.20.1')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

#print ("ixNet.help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4")
#print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4'))

print("Adding OSPF over IP4 stacks")
ixNet.add(ip1, 'ospfv2')
ixNet.commit()

ospf1 = ixNet.getList(ip1, 'ospfv2')[0]

print("Adding NetworkGroup behind Area Border Router DG")
ixNet.execute('createDefaultStack', t1devices, 'ipv4PrefixPools')

networkGroup1 = ixNet.getList(t1dev1, 'networkGroup')[0]
ixNet.setAttribute(networkGroup1, '-name', 'Network_Group')
ixNet.setAttribute(networkGroup1, '-multiplier', '1')

print("Adding IPv4 Loobcak in first Device Group")
loopback1 = ixNet.add(t1dev1, 'ipv4Loopback')
ixNet.commit()

print("Adding Targeted LDP over IPv4 Loopback")
ixNet.add(loopback1, 'ldpTargetedRouter')
ixNet.commit()

print("Adding RSVP-TE over sameIPv4 Loopback")
ixNet.add(loopback1, 'rsvpteLsps')
ixNet.commit()

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'Hl3VPN_Topology')

ixNet.setAttribute(t1dev1, '-name', 'Area Border Router')
ixNet.commit()

#print ("ixNet.help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp")
#print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp'))

print("Configuring LDP prefixes")
ldpPrefixPool1 = ixNet.getList(networkGroup1, 'ipv4PrefixPools')[0]
ixNet.setAttribute(ixNet.getAttribute(ldpPrefixPool1, '-networkAddress') + '/singleValue', '-value', '2.2.2.2')
ixNet.setAttribute(ixNet.getAttribute(ldpPrefixPool1, '-prefixLength') + '/singleValue', '-value', '32')
ixNet.commit()

# Add Chanied DG behind NetworkGroup
print("Add Chanied DG behind NetworkGroup")
chainedDg1 = ixNet.add(networkGroup1, 'deviceGroup')
ixNet.setMultiAttribute(chainedDg1, '-multiplier', '1', '-name', 'Provider Edge Router')
ixNet.commit()
chainedDg1 = ixNet.remapIds(chainedDg1)[0]

# Add ipv4 loopback in Chained DG
print("Adding ipv4 loopback in Chained DG")
loopback1 = ixNet.add(chainedDg1, 'ipv4Loopback')
ixNet.setMultiAttribute(loopback1, '-stackedLayers', [], '-name', 'IPv4 Loopback')
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


# Adding BGP over IPv4 loopback interfaces 
print("Adding BGP over IPv4 loopback interfaces")
ixNet.add(loopback1, 'bgpIpv4Peer')
ixNet.commit()
bgp = ixNet.getList(loopback1, 'bgpIpv4Peer')[0]

print("Setting IPs in BGP DUT IP tab")
ixNet.setAttribute(ixNet.getAttribute(bgp, '-dutIp') + '/singleValue', '-value', '3.2.2.2')
ixNet.commit()

print("Enabling L3VPN  Learned Information filters for BGP Router")
ixNet.setAttribute(ixNet.getAttribute(bgp, '-filterIpV4MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp, '-filterIpV6MplsVpn') + '/singleValue', '-value', 'true')
ixNet.commit()

print("Adding VRF over BGP Peer")
ixNet.add(bgp, 'bgpVrf')
ixNet.commit()

bgpVrf = ixNet.getList(bgp, 'bgpVrf')[0]

print("Adding IPv4 Address Pool behind bgpVrf")
networkGroup3 = ixNet.add(chainedDg1, 'networkGroup')
ixNet.commit()
ipv4PrefixPool = ixNet.add(networkGroup3, 'ipv4PrefixPools')
ixNet.commit()
ixNet.setAttribute(networkGroup3, '-multiplier', '1')
ixNet.commit()

print("Changing default values of IP prefixes")
ixNet.setAttribute(ixNet.getAttribute(ipv4PrefixPool, '-networkAddress') + '/singleValue', '-value', '203.1.0.0')
ixNet.commit()

# Changing label start value in IPv4 Prefix Pool
print("Changing label start value in IPv4 Prefix Pool")
v4RouteProperty = ixNet.getList(ipv4PrefixPool, 'bgpL3VpnRouteProperty')[0]
labelStart = ixNet.getAttribute(v4RouteProperty, '-labelStart')
ixNet.setMultiAttribute(labelStart, '-clearOverlays', 'false')

count = ixNet.add(labelStart, 'counter')
ixNet.setMultiAttribute(count, '-step', '10', '-start', '4000', '-direction', 'increment')
ixNet.commit()

# Adding IPv6 Address Pool behind bgpVrf
print("Adding IPv6 Address Pools behind bgpVrf")
networkGroup4 = ixNet.add(chainedDg1, 'networkGroup')
ixNet.commit()
ipv6PrefixPool = ixNet.add(networkGroup4, 'ipv6PrefixPools')
ixNet.commit()
ixNet.setAttribute(networkGroup4, '-multiplier', '1')
ixNet.commit()

# Changing default values of IPv6 prefixes
print("Changing default values of IPv6 prefixes")
ixNet.setAttribute(ixNet.getAttribute(ipv6PrefixPool, '-networkAddress') + '/singleValue', '-value', '2000:1:1:1:0:0:0:0')
ixNet.commit()

# Changing Label value in IPv6 Prefix Pool
print("Changing Label value in IPv6 Prefix Pool")
v6RouteProperty = ixNet.getList(ipv6PrefixPool, 'bgpV6L3VpnRouteProperty')[0]
multiValue = ixNet.getAttribute(v6RouteProperty, '-labelStart')
ixNet.setMultiAttribute(multiValue, '-clearOverlays', 'false')
count = ixNet.add(multiValue, 'counter')
ixNet.setMultiAttribute(count,  '-step', '10', '-start', '5000', '-direction', 'increment')
ixNet.commit()

print("!!! Scenario confiugrd Successfully!!!")
print ('!!! Test Script Ends !!!')
