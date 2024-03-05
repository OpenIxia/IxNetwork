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
#    This script intends to demonstrate how to use NGPF ISISL3 API.            #
#                                                                              #
#    1. It will create 2 ISISL3 topologies, each having an ipv4 & ipv6 network #
#       topology and loopback device group behind the network group(NG) with   #
#       loopback interface on it. A loopback device group(DG) behind network   #
#       group is needed to support applib traffic.                             #
#    2. Start the isisL3 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Enable the IsisL3 simulated topologies ipv4 & ipv6 node routes, which  #
#       was disabled by default and apply change on the fly.                   #
#    6. Retrieve protocol learned info again and notice the difference with    #
#       previously retrieved learned info.                                     #
#    7. Configure L2-L3 traffic.                                               #
#    8. Configure IPv4 application traffic.[application Traffic type is set    #
#       using variable "trafficType". "ipv4ApplicationTraffic" for ipv4 profile#
#       and "ipv6ApplicationTraffic" for ipv6 profile.                         #
#       Note: IPv4 & IPv6 both could not be configured in same endpoint set.   #
#    9. Start the L2-L3 traffic.                                               #
#   10. Start the application traffic.                                         #
#   11. Retrieve Application traffic stats.                                    #
#   12. Retrieve L2-L3 traffic stats.                                          #
#   13. Stop L2-L3 traffic.                                                    #
#   14. Stop Application traffic.                                              #
#   15. Stop all protocols.                                                    #
################################################################################





def assignPorts (ixNet, realPort1, realPort2)
     chassis1 = realPort1[0]
     chassis2 = realPort2[0]
     card1    = realPort1[1]
     card2    = realPort2[1]
     port1    = realPort1[2]
     port2    = realPort2[2]

     root = @ixNet.getRoot()
     vport1 = @ixNet.add(root, 'vport')
     @ixNet.commit()
     vport1 = @ixNet.remapIds(vport1)[0]

     vport2 = @ixNet.add(root, 'vport')
     @ixNet.commit()
     vport2 = @ixNet.remapIds(vport2)[0]

     chassisObj1 = @ixNet.add(root + '/availableHardware', 'chassis')
     @ixNet.setAttribute(chassisObj1, '-hostname', chassis1)
     @ixNet.commit()
     chassisObj1 = @ixNet.remapIds(chassisObj1)[0]

     if (chassis1 != chassis2) then
         chassisObj2 = @ixNet.add(root + '/availableHardware', 'chassis')
         @ixNet.setAttribute(chassisObj2, '-hostname', chassis2)
         @ixNet.commit()
         chassisObj2 = @ixNet.remapIds(chassisObj2)[0]
     else 
         chassisObj2 = chassisObj1
     end

     cardPortRef1 = chassisObj1 + '/card:'+card1+'/port:'+port1
     @ixNet.setMultiAttribute(vport1, '-connectedTo', cardPortRef1,
         '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 001')
     @ixNet.commit()

     cardPortRef2 = chassisObj2 + '/card:'+card2+'/port:'+port2
     @ixNet.setMultiAttribute(vport2, '-connectedTo', cardPortRef2,
         '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 002')
     @ixNet.commit()
end

################################################################################
# Import the ixnetwork library
# First add the library to Ruby's $LOAD_PATH:    $:.unshift <library_dir>
################################################################################
require 'ixnetwork'

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixApiServer = '10.200.115.203'
ixApiPort   = '8009'
ports       = [['10.200.115.151', '1', '5'], ['10.200.115.151', '1', '6']]

# Variable named trafficType sets type of application traffic to be configured.
# "ipv4ApplicationTraffic" for ipv4 profile & "ipv6ApplicationTraffic" for ipv6 profile.
trafficType = 'ipv6ApplicationTraffic'

# get IxNet class
@ixNet = IxNetwork.new
puts("connecting to IxNetwork client")
@ixNet.connect(ixApiServer, '-port', ixApiPort, '-version', '7.40',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
puts("cleaning up the old configfile, and creating an empty config")
@ixNet.execute('newConfig')

################################################################################
#  Protocol configuration section. Configure ISIS as per the description
#  give above
################################################################################
# assigning ports
assignPorts(@ixNet, ports[0], ports[1])
sleep(5)

root    = @ixNet.getRoot()
vportTx = @ixNet.getList(root, 'vport')[0]
vportRx = @ixNet.getList(root, 'vport')[1]

# Adding Topologies
puts("adding topologies")
@ixNet.add(root, 'topology', '-vports', vportTx)
@ixNet.add(root, 'topology', '-vports', vportRx)
@ixNet.commit()

topologies = @ixNet.getList(@ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

# Adding Device Groups
puts "Adding 2 device groups"
@ixNet.add(topo1, 'deviceGroup')
@ixNet.add(topo2, 'deviceGroup')
@ixNet.commit()

t1devices = @ixNet.getList(topo1, 'deviceGroup')
t2devices = @ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]

puts("Configuring the multipliers (number of sessions)")
@ixNet.setAttribute(t1dev1, '-multiplier', '1')
@ixNet.setAttribute(t2dev1, '-multiplier', '1')
@ixNet.commit()

# Adding Ethernet
puts("Adding Ethernet/mac endpoints")
@ixNet.add(t1dev1, 'ethernet')
@ixNet.add(t2dev1, 'ethernet')
@ixNet.commit()

mac1 = @ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = @ixNet.getList(t2dev1, 'ethernet')[0]

puts("Configuring the mac addresses %s" % (mac1))
@ixNet.setMultiAttribute(@ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '18:03:73:C7:6C:B1',
    '-step',      '00:00:00:00:00:01')

@ixNet.setAttribute(@ixNet.getAttribute(mac2, '-mac') + '/singleValue',
    '-value', '18:03:73:C7:6C:01')
@ixNet.commit()

puts('@ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet\')')
puts(@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet'))

# Adding Ipv4 stack 
puts("Add ipv4")
@ixNet.add(mac1, 'ipv4')
@ixNet.add(mac2, 'ipv4')
@ixNet.commit()

ip1 = @ixNet.getList(mac1, 'ipv4')[0]
ip2 = @ixNet.getList(mac2, 'ipv4')[0]

mvAdd1 = @ixNet.getAttribute(ip1, '-address')
mvAdd2 = @ixNet.getAttribute(ip2, '-address')
mvGw1  = @ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = @ixNet.getAttribute(ip2, '-gatewayIp')

puts("configuring ipv4 addresses")
@ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '20.20.20.2')
@ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '20.20.20.1')
@ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '20.20.20.1')
@ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '20.20.20.2')

@ixNet.setAttribute(@ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
@ixNet.setAttribute(@ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

@ixNet.setMultiAttribute(@ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.setMultiAttribute(@ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.commit()

puts('@ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4\')')
puts(@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4'))

# Adding ISIS over Ethernet stack
puts("Adding ISISl3 over Ethernet stacks")
@ixNet.add(mac1, 'isisL3')
@ixNet.add(mac2, 'isisL3')
@ixNet.commit()

isisL3_1 = @ixNet.getList(mac1, 'isisL3')[0]
isisL3_2 = @ixNet.getList(mac2, 'isisL3')[0]

puts("Renaming topologies and device groups")
@ixNet.setAttribute(topo1, '-name', 'ISISL3 Topology 1')
@ixNet.setAttribute(topo2, '-name', 'ISISL3 Topology 2')

@ixNet.setAttribute(t1dev1, '-name', 'ISISL3 Topology 1 Router')
@ixNet.setAttribute(t2dev1, '-name', 'ISISL3 Topology 2 Router')
@ixNet.commit()

# Enable host name in ISIS router1
puts("Enabling Host name in Emulated ISIS Routers\n")
deviceGroup1 = @ixNet.getList(topo1, 'deviceGroup')[0]
isisL3Router1 = @ixNet.getList(deviceGroup1, 'isisL3Router')[0]
enableHostName1 = @ixNet.getAttribute(isisL3Router1, '-enableHostName')
@ixNet.setAttribute(enableHostName1 + '/singleValue', '-value', 'true')
@ixNet.commit()
sleep(5)
configureHostName1 = @ixNet.getAttribute(isisL3Router1, '-hostName')
@ixNet.setAttribute(configureHostName1 + '/singleValue', '-value', 'isisL3Router1')
@ixNet.commit()


# Enable host name in ISIS router2
deviceGroup2 = @ixNet.getList(topo2, 'deviceGroup')[0]
isisL3Router2 = @ixNet.getList(deviceGroup2, 'isisL3Router')[0]
enableHostName2 = @ixNet.getAttribute(isisL3Router2, '-enableHostName')
@ixNet.setAttribute(enableHostName2 + '/singleValue', '-value', 'true')
@ixNet.commit()
sleep(5)
configureHostName2 = @ixNet.getAttribute(isisL3Router2, '-hostName')
@ixNet.setAttribute(configureHostName2 + '/singleValue', '-value', 'isisL3Router2')
@ixNet.commit

# Change Network type
puts("Making the NetworkType to Point to Point in the first ISISL3 router")
networkTypeMultiValue1 = @ixNet.getAttribute(isisL3_1, '-networkType')
@ixNet.setMultiAttribute(networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'false')
@ixNet.setMultiAttribute(networkTypeMultiValue1 + '/singleValue', '-value', 'pointpoint')

puts("Making the NetworkType to Point to Point in the Second ISISL3 router")
networkTypeMultiValue2 = @ixNet.getAttribute(isisL3_2, '-networkType')
@ixNet.setMultiAttribute(networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'false')
@ixNet.setMultiAttribute(networkTypeMultiValue2 + '/singleValue', '-value', 'pointpoint')

# Disable Discard Learned LSP
puts("Disabling the Discard Learned Info CheckBox")
isisL3RouterDiscardLearnedLSP1 = @ixNet.getAttribute(@ixNet.getList(t1dev1, 'isisL3Router')[0], '-discardLSPs')
isisL3RouterDiscardLearnedLSP2 = @ixNet.getAttribute(@ixNet.getList(t2dev1, 'isisL3Router')[0], '-discardLSPs')

@ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP1, '-pattern', 'singleValue', '-clearOverlays', 'false')
@ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP1 + '/singleValue', '-value', 'false')

@ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP2, '-pattern', 'singleValue', '-clearOverlays', 'false')
@ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP2 + '/singleValue', '-value', 'false')

puts('@ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/isisL3\')')
puts(@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/isisL3'))

# Adding Network group behind DeviceGroup
puts("Adding NetworkGroup behind ISISL3 DG")
@ixNet.execute('createDefaultStack', t1devices, 'networkTopology')
@ixNet.execute('createDefaultStack', t2devices, 'networkTopology')

networkGroup1 = @ixNet.getList(t1dev1, 'networkGroup')[0]
networkGroup2 = @ixNet.getList(t2dev1, 'networkGroup')[0]

@ixNet.setAttribute(networkGroup1, '-name', 'ISIS_1_Network_Group1')
@ixNet.setAttribute(networkGroup2, '-name', 'ISIS_2_Network_Group1')
@ixNet.commit()

# Enabling Host name in Simulated ISIS Routers
puts("Enabling Host name in Simulated ISIS Routers\n")
networkTopology1 = @ixNet.getList(networkGroup1, 'networkTopology')[0]
isisL3SimulatedTopologyConfig1 = @ixNet.getList(networkTopology1, 'isisL3SimulatedTopologyConfig')[0]
enableHostName1 = @ixNet.getAttribute(isisL3SimulatedTopologyConfig1, '-enableHostName')
@ixNet.setAttribute(enableHostName1 + '/singleValue', '-value', 'true')
@ixNet.commit()
sleep(2)
configureHostName1 = @ixNet.getAttribute(isisL3SimulatedTopologyConfig1, '-hostName')
@ixNet.setAttribute(configureHostName1 + '/singleValue', '-value', 'isisL3SimulatedRouter1')
@ixNet.commit()

networkTopology2 = @ixNet.getList(networkGroup2, 'networkTopology')[0]
isisL3SimulatedTopologyConfig2 = @ixNet.getList(networkTopology2, 'isisL3SimulatedTopologyConfig')[0]
enableHostName2 = @ixNet.getAttribute(isisL3SimulatedTopologyConfig2, '-enableHostName')
@ixNet.setAttribute(enableHostName2 + '/singleValue', '-value', 'true')
@ixNet.commit()
sleep(2)
configureHostName2 = @ixNet.getAttribute(isisL3SimulatedTopologyConfig2, '-hostName')
@ixNet.setAttribute(configureHostName2 + '/singleValue', '-value', 'isisL3SimulatedRouter2')
@ixNet.commit()


# Add ipv4 loopback1 for applib traffic
puts("Adding ipv4 loopback1 for applib traffic")
chainedDg1 = @ixNet.add(networkGroup1, 'deviceGroup')
@ixNet.setMultiAttribute(chainedDg1, '-multiplier', '7', '-name', 'Device Group 4')
@ixNet.commit()
chainedDg1 = @ixNet.remapIds(chainedDg1)[0]

loopback1 = @ixNet.add(chainedDg1, 'ipv4Loopback')
@ixNet.setMultiAttribute(loopback1, '-stackedLayers', [], '-name', 'IPv4 Loopback 2')
@ixNet.commit()

connector1 = @ixNet.add(loopback1, 'connector')
@ixNet.setMultiAttribute(connector1, '-connectedTo', networkGroup1 + '/networkTopology/simRouter:1')
@ixNet.commit()
connector1 = @ixNet.remapIds(connector1)[0]

addressSet1 = @ixNet.getAttribute(loopback1, '-address')
@ixNet.setMultiAttribute(addressSet1, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()

addressSet1 = @ixNet.add(addressSet1, 'counter')
@ixNet.setMultiAttribute(addressSet1, '-step', '0.1.0.0', '-start', '201.1.0.0', '-direction', 'increment')
@ixNet.commit()
addressSet1 = @ixNet.remapIds(addressSet1)[0]

# Add ipv4 loopback2 for applib traffic
puts("Adding ipv4 loopback2 for applib traffic")
chainedDg2 = @ixNet.add(networkGroup2, 'deviceGroup')
@ixNet.setMultiAttribute(chainedDg2, '-multiplier', '7', '-name', 'Device Group 3')
@ixNet.commit()
chainedDg2 = @ixNet.remapIds(chainedDg2)[0]

loopback2 = @ixNet.add(chainedDg2, 'ipv4Loopback')
@ixNet.setMultiAttribute(loopback2, '-stackedLayers', [], '-name', 'IPv4 Loopback 1')
@ixNet.commit()

connector2 = @ixNet.add(loopback2, 'connector')
@ixNet.setMultiAttribute(connector2, '-connectedTo', networkGroup2 + '/networkTopology/simRouter:1')
@ixNet.commit()
connector1 = @ixNet.remapIds(connector2)[0]

addressSet2 = @ixNet.getAttribute(loopback2, '-address')
@ixNet.setMultiAttribute(addressSet2, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()

addressSet2 = @ixNet.add(addressSet2, 'counter')
@ixNet.setMultiAttribute(addressSet2, '-step', '0.1.0.0 ', '-start', '206.1.0.0', '-direction', 'increment')
@ixNet.commit()
addressSet2 = @ixNet.remapIds(addressSet2)[0]

# Add ipv6 loopback1 for applib traffic
puts "Adding ipv6 loopback1 for applib traffic"
chainedDg3 = @ixNet.add(networkGroup1, 'deviceGroup')
@ixNet.setMultiAttribute(chainedDg3, '-multiplier', '7', '-name', 'Device Group 6')
@ixNet.commit()
chainedDg3 = @ixNet.remapIds(chainedDg3)[0]

loopback1 = @ixNet.add(chainedDg3, 'ipv6Loopback')
@ixNet.setMultiAttribute(loopback1, '-stackedLayers', [], '-name', 'IPv6 Loopback 2')
@ixNet.commit()

connector1 =  @ixNet.add(loopback1, 'connector')
@ixNet.setMultiAttribute(connector1,  '-connectedTo', networkGroup1 + '/networkTopology/simRouter:1')
@ixNet.commit()
connector1 = @ixNet.remapIds(connector1)[0]

addressSet1 = @ixNet.getAttribute(loopback1, '-address')
@ixNet.setMultiAttribute(addressSet1, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()

addressSet1 = @ixNet.add(addressSet1, 'counter')
@ixNet.setMultiAttribute(addressSet1, '-step', '::1', '-start', '2010::1', '-direction', 'increment')
@ixNet.commit()
addressSet1 = @ixNet.remapIds(addressSet1)[0]

# Add ipv6 loopback2 for applib traffic
puts "Adding ipv6 loopback2 for applib traffic"
chainedDg4 = @ixNet.add(networkGroup2, 'deviceGroup')
@ixNet.setMultiAttribute(chainedDg4, '-multiplier', '7', '-name', 'Device Group 5')
@ixNet.commit()
chainedDg4 = @ixNet.remapIds(chainedDg4)[0]

loopback2 = @ixNet.add(chainedDg4, 'ipv6Loopback')
@ixNet.setMultiAttribute(loopback2, '-stackedLayers', [], '-name', 'IPv6 Loopback 1')
@ixNet.commit()

connector2 =  @ixNet.add(loopback2, 'connector')
@ixNet.setMultiAttribute(connector2,  '-connectedTo', networkGroup2 + '/networkTopology/simRouter:1')
@ixNet.commit()
connector1 = @ixNet.remapIds(connector2)[0]

addressSet2 = @ixNet.getAttribute(loopback2, '-address')
@ixNet.setMultiAttribute(addressSet2, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()

addressSet2 = @ixNet.add(addressSet2, 'counter')
@ixNet.setMultiAttribute(addressSet2, '-step', '::1', '-start', '2060::1', '-direction', 'increment')
@ixNet.commit()
addressSet2 = @ixNet.remapIds(addressSet2)[0]


################################################################################
# Start ISISL3 protocol and wait for 60 seconds
################################################################################
puts("Starting protocols and waiting for 60 seconds for protocols to come up")
@ixNet.execute('startAllProtocols')
sleep(60)

################################################################################
# Retrieve protocol statistics.
################################################################################
puts("Fetching all Protocol Summary Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap   = @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues')
    for  statVal in statValList
        puts("***************************************************")
        index = 0
        for satIndv in statVal
            puts(statcap[index]+' '+satIndv)
            index = index + 1
        end
    end
end
puts("***************************************************")

###############################################################################
# Retrieve protocol learned info
###############################################################################
puts("Fetching ISISL3 Learned Info")
@ixNet.execute('getLearnedInfo', isisL3_1, '1')
sleep(5)
linfo  = @ixNet.getList(isisL3_1, 'learnedInfo')[0]
values = @ixNet.getAttribute(linfo, '-values')

puts("***************************************************")
for v in values
    puts(v)
end
puts("***************************************************")


################################################################################
#  Enable ISISL3 simulated topology's ISIS Simulated IPv4 & v6 Node Routes, which
#  was disabled by default. And apply changes On The Fly (OTF).
################################################################################
puts("Enabling IPv4 & IPv6 Simulated Node Routes")
netTopology1           = @ixNet.getList(networkGroup1, 'networkTopology')[0]
simRouter1             = @ixNet.getList(netTopology1, 'simRouter')[0]
isisL3PseudoRouter1    = @ixNet.getList(simRouter1, 'isisL3PseudoRouter')[0]
IPv4PseudoNodeRoutes1  = @ixNet.getList(isisL3PseudoRouter1, 'IPv4PseudoNodeRoutes')[0]
activeMultivalue1      = @ixNet.getAttribute(IPv4PseudoNodeRoutes1, '-active')
@ixNet.setAttribute(activeMultivalue1 + '/singleValue', '-value', 'true')
@ixNet.commit()
sleep(5)
ipv6PseudoNodeRoutes1 = @ixNet.getList(isisL3PseudoRouter1, 'IPv6PseudoNodeRoutes')[0]
ipv6PseudoNodeRouteMultivalue1 = @ixNet.getAttribute(ipv6PseudoNodeRoutes1, '-active')
@ixNet.setAttribute(ipv6PseudoNodeRouteMultivalue1 + '/singleValue', '-value', 'true')
@ixNet.commit()

netTopology2           = @ixNet.getList(networkGroup2, 'networkTopology')[0]
simRouter2             = @ixNet.getList(netTopology2, 'simRouter')[0]
isisL3PseudoRouter2    = @ixNet.getList(simRouter2, 'isisL3PseudoRouter')[0]
IPv4PseudoNodeRoutes2  = @ixNet.getList(isisL3PseudoRouter2, 'IPv4PseudoNodeRoutes')[0]
activeMultivalue2      = @ixNet.getAttribute(IPv4PseudoNodeRoutes2, '-active')
@ixNet.setAttribute(activeMultivalue2 + '/singleValue', '-value', 'true')
@ixNet.commit()
sleep(5)
ipv6PseudoNodeRoutes2 = @ixNet.getList(isisL3PseudoRouter2, 'IPv6PseudoNodeRoutes')[0]
ipv6PseudoNodeRouteMultivalue2 = @ixNet.getAttribute(ipv6PseudoNodeRoutes2, '-active')
@ixNet.setAttribute(ipv6PseudoNodeRouteMultivalue2 + '/singleValue', '-value', 'true')
@ixNet.commit() 

################################################################################
# Stop/Start ISIS Router on both ports and apply changes on-the-fly
################################################################################
puts("Stop ISIS Router on both ports and apply changes on-the-fly")
deviceGroup1 = @ixNet.getList(topo1, 'deviceGroup')[0]
isisL3Router1 = @ixNet.getList(deviceGroup1, 'isisL3Router')[0]
isisL3RouterDeactivate1 = @ixNet.getAttribute(isisL3Router1, '-active')

deviceGroup2 = @ixNet.getList(topo2, 'deviceGroup')[0]
isisL3Router2 = @ixNet.getList(deviceGroup2, 'isisL3Router')[0]
isisL3RouterDeactivate2 = @ixNet.getAttribute(isisL3Router2, '-active')

@ixNet.setAttribute(isisL3RouterDeactivate1 + '/singleValue', '-value', 'false')
@ixNet.setAttribute(isisL3RouterDeactivate2 + '/singleValue', '-value', 'false')
@ixNet.commit()

globalObj = @ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
puts("Applying changes on the fly")
begin
    @ixNet.execute('applyOnTheFly', topology)
rescue
    puts("error in applying on the fly change")
end
puts("Wait for 30 seconds ...")
sleep(30)


################################################################################
# Start ISIS Router on both ports and apply changes on-the-fly
################################################################################
puts("Start ISIS Router on both ports and apply changes on-the-fly")
deviceGroup1 = @ixNet.getList(topo1, 'deviceGroup')[0]
isisL3Router1 = @ixNet.getList(deviceGroup1, 'isisL3Router')[0]
isisL3RouterActivate1 = @ixNet.getAttribute(isisL3Router1, '-active')

deviceGroup2 = @ixNet.getList(topo2, 'deviceGroup')[0]
isisL3Router2 = @ixNet.getList(deviceGroup2, 'isisL3Router')[0]
isisL3RouterActivate2 = @ixNet.getAttribute(isisL3Router2, '-active')

@ixNet.setAttribute(isisL3RouterActivate1 + '/singleValue', '-value', 'true')
@ixNet.setAttribute(isisL3RouterActivate2 + '/singleValue', '-value', 'true')
@ixNet.commit()

globalObj = @ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
puts("Applying changes on the fly")
begin
    @ixNet.execute('applyOnTheFly', topology)
rescue
    puts("error in applying on the fly change")
end
puts("Wait for 30 seconds ...")
sleep(30)

###############################################################################
# Retrieve protocol learned info again and compare with
# previously retrieved learned info.
###############################################################################
puts("Fetching ISISL3 learned info after enabling IPv4 Node Routes")
@ixNet.execute('getLearnedInfo', isisL3_1, '1')
sleep(5)
linfo  = @ixNet.getList(isisL3_1, 'learnedInfo')[0]
values = @ixNet.getAttribute(linfo, '-values')

puts("***************************************************")
for v in values
    puts(v)
end
puts("***************************************************")

puts("Fetching ISISL3 IPv6 Learned Info\n")
@ixNet.execute('getLearnedInfo', isisL3_1, '1')
sleep(5)
linfo = @ixNet.getList(isisL3_1, 'learnedInfo')[0]
ipv6table = @ixNet.getList(linfo, 'table')[1]
values    = @ixNet.getAttribute(ipv6table, '-values')
     

puts("***************************************************\n")
for v in values
    puts(v)
end
puts("***************************************************")

################################################################################
# Configure L2-L3 traffic
################################################################################
#Configuring L2-L3 IPv4 Traffic Item
puts("Configuring L2-L3 IPV4 Traffic Item")
trafficItem1 = @ixNet.add(@ixNet.getRoot() + '/traffic', 'trafficItem')
@ixNet.setMultiAttribute(trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv4')
@ixNet.commit()

trafficItem1 = @ixNet.remapIds(trafficItem1)[0]
endpointSet1 = @ixNet.add(trafficItem1, 'endpointSet')
source       = [networkGroup1 + '/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1']
destination  = [networkGroup2 + '/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1']

@ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', [],
    '-scalableSources',       [],
    '-multicastReceivers',    [],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source,
    '-destinations',          destination)
@ixNet.commit()

@ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         [])
@ixNet.commit()

#Configuring L2-L3 IPv6 Traffic Item
puts("Configuring L2-L3 IPv6 Traffic Item\n")
trafficItem2 = @ixNet.add(@ixNet.getRoot() + '/traffic', 'trafficItem')
@ixNet.setMultiAttribute(trafficItem2, '-name', 'Traffic Item 2',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv6')
@ixNet.commit()

trafficItem2    = @ixNet.remapIds(trafficItem2)[0]
endpointSet1 = @ixNet.add(trafficItem2, 'endpointSet')
source       = [networkGroup1 + '/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1']
destination  = [networkGroup2 + '/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1']

@ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', [],
    '-scalableSources',       [],
    '-multicastReceivers',    [],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source,
    '-destinations',          destination)
@ixNet.commit()

@ixNet.setMultiAttribute(trafficItem2 + '/tracking',
    '-trackBy',        ['sourceDestEndpointPair0','trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',          [])
@ixNet.commit()
################################################################################
# Configure Application traffic
################################################################################
# Configuring Applib traffic
puts"Configuring Applib traffic profile %s." % trafficType
trafficItem2 = @ixNet.add(@ixNet.getRoot() + '/traffic', 'trafficItem')

@ixNet.setMultiAttribute(trafficItem2,
    '-name',                     'Traffic Item 3',             
    '-trafficItemType',          'applicationLibrary',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType',              trafficType)
@ixNet.commit()
trafficItem2 = @ixNet.remapIds(trafficItem2)[0]

endpointSet2 = @ixNet.add(trafficItem2, 'endpointSet')
source_app   = [@ixNet.getList(t1dev1, 'networkGroup')[0]]
destin_app   = [@ixNet.getList(t2dev1, 'networkGroup')[0]]

@ixNet.setMultiAttribute(endpointSet2,
    '-name',                  "EndpointSet-2",
    '-multicastDestinations', [],
    '-scalableSources',       [],
    '-multicastReceivers',    [],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source_app,
    '-destinations',          destin_app)    
@ixNet.commit()

endpointSet2 = @ixNet.remapIds(endpointSet2)[0]

appLibProfile = @ixNet.add(trafficItem2, 'appLibProfile')
flows_configured  = ['Bandwidth_BitTorrent_File_Download',
                            'Bandwidth_eDonkey',
                            'Bandwidth_HTTP',
                            'Bandwidth_IMAPv4',
                            'Bandwidth_POP3',
                            'Bandwidth_Radius',
                            'Bandwidth_Raw',
                            'Bandwidth_Telnet',
                            'Bandwidth_uTorrent_DHT_File_Download',
                            'BBC_iPlayer',
                            'BBC_iPlayer_Radio',
                            'BGP_IGP_Open_Advertise_Routes',
                            'BGP_IGP_Withdraw_Routes',
                            'Bing_Search',
                            'BitTorrent_Ares_v217_File_Download',
                            'BitTorrent_BitComet_v126_File_Download',
                            'BitTorrent_Blizzard_File_Download',
                            'BitTorrent_Cisco_EMIX',
                            'BitTorrent_Enterprise',
                            'BitTorrent_File_Download',
                            'BitTorrent_LimeWire_v5516_File_Download',
                            'BitTorrent_RMIX_5M']

@ixNet.setMultiAttribute(appLibProfile,

    '-enablePerIPStats', 'false',
    '-objectiveDistribution', 'applyFullObjectiveToEachPort',
    '-configuredFlows', flows_configured)
@ixNet.commit()
appLibProfile = @ixNet.remapIds(appLibProfile)[0]

puts('@ixNet.help(@ixNet.getRoot() + \'/traffic\')')
puts(@ixNet.help(@ixNet.getRoot() + '/traffic'))

###############################################################################
# Apply and start L2/L3 traffic
###############################################################################
puts('Applying L2/L3 traffic')
@ixNet.execute('apply', @ixNet.getRoot() + '/traffic')
sleep(5)

puts('Starting L2/L3 traffic')
@ixNet.execute('start', @ixNet.getRoot() + '/traffic')

###############################################################################
# Apply and start applib traffic
###############################################################################
puts('Applying applib traffic')
@ixNet.execute('applyStatefulTraffic', @ixNet.getRoot() + '/traffic')
sleep(5)

puts('Starting applib traffic')
@ixNet.execute('startStatefulTraffic', @ixNet.getRoot() + '/traffic')

puts('Let traffic run for 1 minute')
sleep(60)

###############################################################################
# Retrieve Applib traffic item statistics
###############################################################################
puts('Verifying all the applib traffic stats')
viewPage = '::ixNet::OBJ-/statistics/view:"Application Traffic Item Statistics"/page'
statcap = @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues')
    for  statVal in statValList
        puts("***************************************************")
        index = 0
        for satIndv in statVal
            puts(statcap[index]+' '+satIndv)
            index = index + 1
        end
    end
end
puts("***************************************************")

###############################################################################
# Retrieve L2/L3 traffic item statistics
###############################################################################
puts('Verifying all the L2-L3 traffic stats')
viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page'
statcap =  @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues')
    for  statVal in statValList
        puts("***************************************************")
        index = 0
        for satIndv in statVal
            puts(statcap[index]+' '+satIndv)
            index = index + 1
        end
    end
end
puts("***************************************************")

################################################################################
# Stop applib traffic
################################################################################
puts('Stopping applib traffic')
@ixNet.execute('stopStatefulTraffic', @ixNet.getRoot() + '/traffic')
sleep(5)

################################################################################
# Stop L2/L3 traffic
################################################################################
puts('Stopping L2/L3 traffic')
@ixNet.execute('stop', @ixNet.getRoot() + '/traffic')
sleep(5)

################################################################################
# Stop all protocols
################################################################################
puts('Stopping protocols')
@ixNet.execute('stopAllProtocols')

puts('!!! Test Script Ends !!!')
