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
#    This script intends to demonstrate how to use NGPF BGP+ API               #
#    It will create 2 BGP+ topologies, it will start the emulation and         #
#    than it will retrieve and display few statistics                          #
# Module:                                                                      #
#    The sample was tested on an XMVDC16 module.                               #
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
# Give chassis/client/ixNetwork server port/ chassis port HW port information   #
# below                                                                         #
#################################################################################
ixApiServer = '10.200.115.203'
ixApiPort   = '8009'
ports       = [['10.200.115.151', '2', '7'], ['10.200.115.151', '2', '8']]

# get IxNet class
@ixNet = IxNetwork.new
puts("connecting to IxNetwork client")
@ixNet.connect(ixApiServer, '-port', ixApiPort, '-version', '7.40',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
puts("cleaning up the old configfile, and creating an empty config")
@ixNet.execute('newConfig')

# assigning ports
assignPorts(@ixNet, ports[0], ports[1])
sleep(5)

root    = @ixNet.getRoot()
vportTx = @ixNet.getList(root, 'vport')[0]
vportRx = @ixNet.getList(root, 'vport')[1]

puts("adding topologies")
@ixNet.add(root, 'topology', '-vports', vportTx)
@ixNet.add(root, 'topology', '-vports', vportRx)
@ixNet.commit()

topologies = @ixNet.getList(@ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

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

puts("Adding ethernet/mac endpoints")
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

puts("Add ipv6")
@ixNet.add(mac1, 'ipv6')
@ixNet.add(mac2, 'ipv6')
@ixNet.commit()

ip1 = @ixNet.getList(mac1, 'ipv6')[0]
ip2 = @ixNet.getList(mac2, 'ipv6')[0]

mvAdd1 = @ixNet.getAttribute(ip1, '-address')
mvAdd2 = @ixNet.getAttribute(ip2, '-address')
mvGw1  = @ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = @ixNet.getAttribute(ip2, '-gatewayIp')

puts("configuring ipv6 addresses")
@ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '11:0:0:0:0:0:0:1')
@ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '11:0:0:0:0:0:0:2')
@ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '11:0:0:0:0:0:0:2')
@ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '11:0:0:0:0:0:0:1')

@ixNet.setAttribute(@ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '64')
@ixNet.setAttribute(@ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '64')

@ixNet.setMultiAttribute(@ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.setMultiAttribute(@ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.commit()

puts('@ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6\')')
puts(@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6'))

puts("Adding BGP+ over IPv6 stacks")
@ixNet.add(ip1, 'bgpIpv6Peer')
@ixNet.add(ip2, 'bgpIpv6Peer')
@ixNet.commit()

bgp1 = @ixNet.getList(ip1, 'bgpIpv6Peer')[0]
bgp2 = @ixNet.getList(ip2, 'bgpIpv6Peer')[0]

puts("Renaming the topologies and the device groups")
@ixNet.setAttribute(topo1, '-name', 'BGP+ Topology 1')
@ixNet.setAttribute(topo2, '-name', 'BGP+ Topology 2')

@ixNet.setAttribute(t1dev1, '-name', 'BGP+ Topology 1 Router')
@ixNet.setAttribute(t2dev1, '-name', 'BGP+ Topology 2 Router')
@ixNet.commit()

puts("Setting IPs in BGP+ DUT IP tab")
@ixNet.setAttribute(@ixNet.getAttribute(bgp1, '-dutIp') + '/singleValue', '-value', '11:0:0:0:0:0:0:2')
@ixNet.setAttribute(@ixNet.getAttribute(bgp2, '-dutIp') + '/singleValue', '-value', '11:0:0:0:0:0:0:1')
@ixNet.commit()

puts("Adding NetworkGroup behind BGP+ DG")
@ixNet.execute('createDefaultStack', t1devices, 'ipv6PrefixPools')
@ixNet.execute('createDefaultStack', t2devices, 'ipv6PrefixPools')

networkGroup1 = @ixNet.getList(t1dev1, 'networkGroup')[0]
networkGroup2 = @ixNet.getList(t2dev1, 'networkGroup')[0]

@ixNet.setAttribute(networkGroup1, '-name', 'BGP+_1_Network_Group1')
@ixNet.setAttribute(networkGroup2, '-name', 'BGP+_2_Network_Group1')
@ixNet.commit()

# Add ipv6 loopback1 for applib traffic
puts("Adding ipv6 loopback1 for applib traffic")
chainedDg1 = @ixNet.add(networkGroup1, 'deviceGroup')
@ixNet.setMultiAttribute(chainedDg1, '-multiplier', '1', '-name', 'Device Group 4')
@ixNet.commit()
chainedDg1 = @ixNet.remapIds(chainedDg1)[0]

loopback1 = @ixNet.add(chainedDg1, 'ipv6Loopback')
@ixNet.setMultiAttribute(loopback1, '-stackedLayers', [], '-name', 'IPv6 Loopback 2')
@ixNet.commit()

addressSet1 = @ixNet.getAttribute(loopback1, '-address')
@ixNet.setMultiAttribute(addressSet1, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()

addressSet1 = @ixNet.add(addressSet1, 'counter')
@ixNet.setMultiAttribute(addressSet1, '-step', '0:0:0:0:0:0:0:1', '-start', '3000:0:1:1:0:0:0:0', '-direction', 'increment')
@ixNet.commit()
addressSet1 = @ixNet.remapIds(addressSet1)[0]

# Add ipv6 loopback2 for applib traffic
puts("Adding ipv6 loopback2 for applib traffic")
chainedDg2 = @ixNet.add(networkGroup2, 'deviceGroup')
@ixNet.setMultiAttribute(chainedDg2, '-multiplier', '1', '-name', 'Device Group 3')
@ixNet.commit()
chainedDg2 = @ixNet.remapIds(chainedDg2)[0]

loopback2 = @ixNet.add(chainedDg2, 'ipv6Loopback')
@ixNet.setMultiAttribute(loopback2, '-stackedLayers', [], '-name', 'IPv6 Loopback 1')
@ixNet.commit()

addressSet2 = @ixNet.getAttribute(loopback2, '-address')
@ixNet.setMultiAttribute(addressSet2, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()

addressSet2 = @ixNet.add(addressSet2, 'counter')
@ixNet.setMultiAttribute(addressSet2, '-step', '0:0:0:0:0:0:0:1', '-start', '3000:1:1:1:0:0:0:0', '-direction', 'increment')
@ixNet.commit()
addressSet2 = @ixNet.remapIds(addressSet2)[0]

################################################################################
#  Start BGP+ protocol and wait for 45 seconds                                 #
################################################################################
puts("Starting protocols and waiting for 45 seconds for protocols to come up")
@ixNet.execute('startAllProtocols')
sleep(45)

################################################################################
#  Retrieve protocol statistics                                                #
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

################################################################################
#  Enabling the BGP IPv6 Learned Information on the fly                        #
################################################################################
puts("Enabling IPv6 Unicast Learned Information for BGP+ Router")
@ixNet.setAttribute(@ixNet.getAttribute(bgp1, '-filterIpV6Unicast') + '/singleValue', '-value', 'true')
@ixNet.setAttribute(@ixNet.getAttribute(bgp2, '-filterIpV6Unicast') + '/singleValue', '-value', 'true')
@ixNet.commit()

globalObj = @ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
puts("Applying changes on the fly")
begin
    @ixNet.execute('applyOnTheFly', topology)
rescue
    puts("error in applying on the fly change")
end
sleep(10)

###############################################################################
#  Retrieve protocol learned info again and compare with                      #
#  previouly retrieved learned info                                           #
###############################################################################
puts("Fetching BGP+ learned info after enabling ipv6 learned info")
@ixNet.execute('getIPv6LearnedInfo', bgp1, '1')
sleep(5)
linfo  = @ixNet.getList(bgp1, 'learnedInfo')[0]
values = @ixNet.getAttribute(linfo, '-values')

puts("***************************************************")
for v in values
    puts(v)
end
puts("***************************************************")

################################################################################
#  Configure L2-L3 traffic                                                     #
################################################################################
puts("Congfiguring L2-L3 Traffic Item")
trafficItem1 = @ixNet.add(@ixNet.getRoot() + '/traffic', 'trafficItem')
@ixNet.setMultiAttribute(trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv6')
@ixNet.commit()

trafficItem1 = @ixNet.remapIds(trafficItem1)[0]
endpointSet1 = @ixNet.add(trafficItem1, 'endpointSet')
source       = [networkGroup1 + '/ipv6PrefixPools:1']
destination  = [networkGroup2 + '/ipv6PrefixPools:1']

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

################################################################################
#  Configure Application traffic                                               #
################################################################################
puts("Configuring Applib traffic")
trafficItem2 = @ixNet.add(@ixNet.getRoot() + '/traffic', 'trafficItem')

@ixNet.setMultiAttribute(trafficItem2,
    '-name',                     'Traffic Item 2',             
    '-trafficItemType',          'applicationLibrary',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType',              'ipv6ApplicationTraffic')
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
# Apply and start L2/L3 traffic                                               #
###############################################################################
puts('applying L2/L3 traffic')
@ixNet.execute('apply', @ixNet.getRoot() + '/traffic')
sleep(5)

puts('starting L2/L3 traffic')
@ixNet.execute('start', @ixNet.getRoot() + '/traffic')

###############################################################################
#  Apply and start applib traffic                                             #
###############################################################################
puts('applying applib traffic')
@ixNet.execute('applyStatefulTraffic', @ixNet.getRoot() + '/traffic')
sleep(5)

puts('starting applib traffic')
@ixNet.execute('startStatefulTraffic', @ixNet.getRoot() + '/traffic')

puts('Let traffic run for 1 minute')
sleep(60)

###############################################################################
#  Retrieve Applib traffic item statistics                                    #
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
#  Retrieve L2/L3 traffic item statistics                                     #
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
#  Stop applib traffic                                                         #
################################################################################
puts('Stopping applib traffic')
@ixNet.execute('stopStatefulTraffic', @ixNet.getRoot() + '/traffic')
sleep(15)

################################################################################
#  Stop L2/L3 traffic                                                          #
################################################################################
puts('Stopping L2/L3 traffic')
@ixNet.execute('stop', @ixNet.getRoot() + '/traffic')
sleep(5)

################################################################################
#  Stop all protocols                                                          #
################################################################################
puts('Stopping protocols')
@ixNet.execute('stopAllProtocols')

puts('!!! Test Script Ends !!!')
