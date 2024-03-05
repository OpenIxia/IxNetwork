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
#                                                                              #
# About Topology:                                                              #
#                                                                              #
#     On each port, it will create one topology of LDPv6 FEC 128.              #
#     In each topology, there will be two device groups and two network groups.#
#     First device group will simulate as a LDP basic P router and other as    #
#     LDPv6 targeted PE router with pseudo wire FEC 128 is configured.         #
#     After first device group, there is one network group in which IPv6 prefix#
#     pools is configured. The other network group has mac pools which is      #
#     simulated as CE router and also is used as traffic end point.            #
#                                                                              #
# Script Flow:                                                                 #
#    1. Configuration of protocols as described in topology.                   #
#    2. Start the LDP protocol.                                                #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Change LDP PW/VPLS labels & apply change on the fly                    #
#    6. Retrieve protocol learned info again.                                  #
#    7. Configure L2-L3 traffic.                                               #
#    8. Start the L2-L3 traffic.                                               #
#   11. Retrieve L2-L3 traffic stats.                                          #
#   12. Stop L2-L3 traffic.                                                    #
#   13. Stop all protocols.                                                    #
#                                                                              #                                                                                
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
ports       = [['10.200.115.151', '4', '1'], ['10.200.115.151', '4', '2']]

# get IxNet class
@ixNet = IxNetwork.new
puts("Connecting to IxNetwork client")
@ixNet.connect(ixApiServer, '-port', ixApiPort, '-version', '7.40', '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
puts("Cleaning up the old configfile, and creating an empty config")
@ixNet.execute('newConfig')

# assigning ports
assignPorts(@ixNet, ports[0], ports[1])
sleep(5)

root    = @ixNet.getRoot()
vportTx = @ixNet.getList(root, 'vport')[0]
vportRx = @ixNet.getList(root, 'vport')[1]

puts("Adding two topologies")
@ixNet.add(@ixNet.getRoot(), 'topology', '-vports', vportTx)
@ixNet.add(@ixNet.getRoot(), 'topology', '-vports', vportRx)
@ixNet.commit()

topologies = @ixNet.getList(@ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

puts("Adding one device group in each topology")
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

puts("Adding Ethernet/MAC endpoints for the device groups")
@ixNet.add(t1dev1, 'ethernet')
@ixNet.add(t2dev1, 'ethernet')
@ixNet.commit()

mac1 = @ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = @ixNet.getList(t2dev1, 'ethernet')[0]

puts("Configuring the MAC addresses for the device groups")
@ixNet.setMultiAttribute(@ixNet.getAttribute(mac1, '-mac') + '/counter',
        '-direction', 'increment',
        '-start',     '00:11:01:00:00:01',
        '-step',      '00:00:00:00:00:01')

@ixNet.setAttribute(@ixNet.getAttribute(mac2, '-mac') + '/singleValue',
        '-value', '00:12:01:00:00:01')
@ixNet.commit()

puts("Adding IPv6 over Ethernet stack for both device groups")
@ixNet.add(mac1, 'ipv6')
@ixNet.add(mac2, 'ipv6')
@ixNet.commit()

ipv61 = @ixNet.getList(mac1, 'ipv6')[0]
ipv62 = @ixNet.getList(mac2, 'ipv6')[0]

mvAddv61 = @ixNet.getAttribute(ipv61, '-address')
mvAddv62 = @ixNet.getAttribute(ipv62, '-address')

mvGwv61  = @ixNet.getAttribute(ipv61, '-gatewayIp')
mvGwv62  = @ixNet.getAttribute(ipv62, '-gatewayIp')

puts("Configuring IPv6 addresses for both device groups")
@ixNet.setAttribute(mvAddv61 + '/singleValue', '-value', '2000:0:0:1:0:0:0:2')
@ixNet.setAttribute(mvAddv62 + '/singleValue', '-value', '2000:0:0:1:0:0:0:1')
@ixNet.setAttribute(mvGwv61 + '/singleValue', '-value', '2000:0:0:1:0:0:0:1')
@ixNet.setAttribute(mvGwv62 + '/singleValue', '-value', "2000:0:0:1:0:0:0:2")

puts("Configuring IPv6 prefix for both device groups")
@ixNet.setAttribute(@ixNet.getAttribute(ipv61, '-prefix') + '/singleValue', '-value', '64')
@ixNet.setAttribute(@ixNet.getAttribute(ipv62, '-prefix') + '/singleValue', '-value', '64')

@ixNet.setMultiAttribute(@ixNet.getAttribute(ipv61, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.setMultiAttribute(@ixNet.getAttribute(ipv62, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.commit()

puts("Adding LDPv6 Connected Interface over IPv6 stack")
@ixNet.add(ipv61, 'ldpv6ConnectedInterface')
@ixNet.add(ipv62, 'ldpv6ConnectedInterface')
@ixNet.commit()

ldpv6If1 = @ixNet.getList(ipv61, 'ldpv6ConnectedInterface')[0]
ldpv6If2 = @ixNet.getList(ipv62, 'ldpv6ConnectedInterface')[0]

puts("Adding LDPv6 basic router over IPv6 stack")
@ixNet.add(ipv61, 'ldpBasicRouterV6')
@ixNet.add(ipv62, 'ldpBasicRouterV6')
@ixNet.commit()

ldpBasicRouterV61 = @ixNet.getList(ipv61, 'ldpBasicRouterV6')
ldpBasicRouterV62 = @ixNet.getList(ipv62, 'ldpBasicRouterV6')

puts("Renaming the topologies and the device groups")
@ixNet.setAttribute(topo1, '-name', 'LDPv6 FEC128 Topology 1')
@ixNet.setAttribute(topo2, '-name', 'LDPv6 FEC128 Topology 2')

@ixNet.setAttribute(t1dev1, '-name', 'P Router 1')
@ixNet.setAttribute(t2dev1, '-name', 'P Router 2')
@ixNet.commit()

puts("Adding Network Group behind LDPv6 P router")
@ixNet.add(t1dev1, 'networkGroup')
@ixNet.add(t2dev1, 'networkGroup')
@ixNet.commit()

networkGroup1 = @ixNet.getList(t1dev1, 'networkGroup')[0]
networkGroup2 = @ixNet.getList(t2dev1, 'networkGroup')[0]

@ixNet.setAttribute(networkGroup1, '-name', 'LDP_1_Network_Group1')
@ixNet.setAttribute(networkGroup2, '-name', 'LDP_2_Network_Group1')
@ixNet.setAttribute(networkGroup1, '-multiplier', '1')
@ixNet.setAttribute(networkGroup2, '-multiplier', '1')
@ixNet.commit()

puts("Adding Ipv6 prefix pools in Network Groups")
@ixNet.add(networkGroup1, 'ipv6PrefixPools')
@ixNet.add(networkGroup2, 'ipv6PrefixPools')
@ixNet.commit()

ipv6PrefixPools1 = @ixNet.getList(networkGroup1, 'ipv6PrefixPools')[0]
ipv6PrefixPools2 = @ixNet.getList(networkGroup2, 'ipv6PrefixPools')[0]

puts("Configuring network address and prefix length of IPv6 prefix pools")
prefixLength1 = @ixNet.getAttribute(ipv6PrefixPools1, '-prefixLength')
prefixLength2 = @ixNet.getAttribute(ipv6PrefixPools2, '-prefixLength')
@ixNet.setMultiAttribute(prefixLength1, '-clearOverlays',  'false', '-pattern', 'singleValue')
@ixNet.setMultiAttribute(prefixLength2, '-clearOverlays',  'false', '-pattern', 'singleValue')
@ixNet.commit()

singleValue1 = @ixNet.add(prefixLength1, 'singleValue')
singleValue2 = @ixNet.add(prefixLength2, 'singleValue')
@ixNet.setMultiAttribute(singleValue1, '-value', '128')
@ixNet.setMultiAttribute(singleValue2, '-value', '128')
@ixNet.commit()

networkAddress1 = @ixNet.getAttribute(ipv6PrefixPools1, '-networkAddress')
networkAddress2 = @ixNet.getAttribute(ipv6PrefixPools2, '-networkAddress')
@ixNet.setMultiAttribute(networkAddress1, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.setMultiAttribute(networkAddress2, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()

counter1 = @ixNet.add(networkAddress1, 'counter')
counter2 = @ixNet.add(networkAddress2, 'counter')
@ixNet.setMultiAttribute(counter1, '-step', '0:0:0:0:0:0:0:1', '-start', '2222:0:0:0:0:0:0:1', '-direction', 'increment')
@ixNet.setMultiAttribute(counter2, '-step', '0:0:0:0:0:0:0:1', '-start', '2222:0:1:0:0:0:0:1', '-direction', 'increment')
@ixNet.commit()

puts("Adding Device Group behind Network Groups")
@ixNet.add(networkGroup1, 'deviceGroup')
@ixNet.add(networkGroup2, 'deviceGroup')
@ixNet.commit()

t1dev2 = @ixNet.getList(networkGroup1, 'deviceGroup')[0]
t2dev2 = @ixNet.getList(networkGroup2, 'deviceGroup')[0]

puts("Configuring the multipliers")
@ixNet.setAttribute(t1dev2, '-multiplier', '1')
@ixNet.setAttribute(t2dev2, '-multiplier', '1')
@ixNet.commit()

@ixNet.setAttribute(t1dev2, '-name', 'PE Router 1')
@ixNet.setAttribute(t2dev2, '-name', 'PE Router 2')
@ixNet.commit()

puts("Adding loopback in second device group of both topologies")
@ixNet.add(t1dev2, 'ipv6Loopback')
@ixNet.add(t2dev2, 'ipv6Loopback')
@ixNet.commit()

ipv6Loopback1 = @ixNet.getList(t1dev2, 'ipv6Loopback')[0]
ipv6Loopback2 = @ixNet.getList(t2dev2, 'ipv6Loopback')[0]

puts("Adding targeted LDPv6 router over these loopbacks")
@ixNet.add(ipv6Loopback1, 'ldpTargetedRouterV6')
@ixNet.add(ipv6Loopback2, 'ldpTargetedRouterV6')
@ixNet.commit()

ldpTargetedRouterV61 = @ixNet.getList(ipv6Loopback1, 'ldpTargetedRouterV6')[0]
ldpTargetedRouterV62 = @ixNet.getList(ipv6Loopback2, 'ldpTargetedRouterV6')[0]

puts("Configuring DUT IP in LDPv6 targeted peers")
iPAddress1 = @ixNet.getAttribute(ldpTargetedRouterV61 + '/ldpTargetedIpv6Peer', '-iPAddress')
iPAddress2 = @ixNet.getAttribute(ldpTargetedRouterV62 + '/ldpTargetedIpv6Peer', '-iPAddress')
@ixNet.setMultiAttribute(iPAddress1, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.setMultiAttribute(iPAddress2, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()

counter1 = @ixNet.add(iPAddress1, 'counter')
counter2 = @ixNet.add(iPAddress2, 'counter')
@ixNet.setMultiAttribute(counter1, '-step', '0:0:0:0:0:0:0:1', '-start', '2222:0:1:0:0:0:0:1', '-direction', 'increment')
@ixNet.setMultiAttribute(counter2, '-step', '0:0:0:0:0:0:0:1', '-start', '2222:0:0:0:0:0:0:1', '-direction', 'increment')
@ixNet.commit()

puts("Adding LDP PW/VPLS over these targeted routers")
@ixNet.add(ldpTargetedRouterV61, 'ldppwvpls')
@ixNet.add(ldpTargetedRouterV62, 'ldppwvpls')
@ixNet.commit()

ldppwvpls1 = @ixNet.getList(ldpTargetedRouterV61, 'ldppwvpls')[0]
ldppwvpls2 = @ixNet.getList(ldpTargetedRouterV62, 'ldppwvpls')[0]

puts("Enabling Auto Peer Address in LDP PW/VPLS")
@ixNet.setAttribute(ldppwvpls1, '-autoPeerId', 'true')
@ixNet.setAttribute(ldppwvpls2, '-autoPeerId', 'true')
@ixNet.commit()

puts("Adding Network Group behind each PE routers")
@ixNet.add(t1dev2, 'networkGroup')
@ixNet.add(t2dev2, 'networkGroup')
@ixNet.commit()

networkGroup3 = @ixNet.getList(t1dev2, 'networkGroup')[0]
networkGroup4 = @ixNet.getList(t2dev2, 'networkGroup')[0]

@ixNet.setAttribute(networkGroup3, '-name', 'MAC_POOL_1')
@ixNet.setAttribute(networkGroup4, '-name', 'MAC_POOL_2')
@ixNet.commit()

puts("Adding MAC pools in Network Groups")
@ixNet.add(networkGroup3, 'macPools')
@ixNet.add(networkGroup4, 'macPools')
@ixNet.commit()

macPools1 = @ixNet.getList(networkGroup3, 'macPools')
macPools2 = @ixNet.getList(networkGroup4, 'macPools')

puts("All configuration is completed..Wait for 5 seconds...")
sleep(5)

################################################################################
# Start LDPv6 protocol and wait for 60 seconds                                 #  
################################################################################
puts("Starting protocols and waiting for 60 seconds for protocols to come up")
@ixNet.execute('startAllProtocols')
sleep(60)

################################################################################
# Retrieve protocol statistics                                                 #
################################################################################
puts("Fetching LDP Per Port Stats")
viewPage = '::ixNet::OBJ-/statistics/view:"LDP Per Port"/page'
statcap  = @ixNet.getAttribute(viewPage, '-columnCaptions')
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

#################################################################################
# Retrieve protocol learned info                                                #
#################################################################################
puts("Fetching LDPv6 FEC128 Learned Info")
@ixNet.execute('getFEC128LearnedInfo', ldpTargetedRouterV61, '1')
sleep(5)
linfoList  = @ixNet.getList(ldpTargetedRouterV61, 'learnedInfo')
for linfo in linfoList
    values = @ixNet.getAttribute(linfo, '-values')
    puts("***************************************************")
    for v in values
        puts(v)
    end
    puts("***************************************************")
end

################################################################################
# Change the labels of LDPv6 PW/VPLS                                           #
################################################################################
puts("Changing labels of LDPv6 PW/VPLS Range")
label2 = @ixNet.getAttribute(ldppwvpls2, '-label')
@ixNet.setMultiAttribute(label2, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()
counter2 = @ixNet.add(label2, 'counter')
@ixNet.setMultiAttribute(counter2, '-step', '10', '-start', '60', '-direction', 'decrement')
@ixNet.commit()
sleep(2)

################################################################################
# Applying changes one the fly                                                 #
################################################################################
puts("Applying changes on the fly")
globals   = (@ixNet.getRoot()) + '/globals'
topology  = globals + '/topology'
@ixNet.execute('applyOnTheFly', topology)
sleep(5)

#################################################################################
# Retrieve protocol learned info again                                          #
#################################################################################
puts("Fetching LDPv6 FEC128 Learned Info again after changing labels on the fly")
@ixNet.execute('getFEC128LearnedInfo', ldpTargetedRouterV61, '1')
sleep(5)
linfoList  = @ixNet.getList(ldpTargetedRouterV61, 'learnedInfo')
for linfo in linfoList
    values = @ixNet.getAttribute(linfo, '-values')
    puts("***************************************************")
    for v in values
        puts(v)
    end
    puts("***************************************************")
end

#################################################################################
# Configure L2-L3 traffic                                                       #
#################################################################################
puts("Congfiguring L2/L3 Traffic Item")
trafficItem1 = @ixNet.add((@ixNet.getRoot()) + '/traffic', 'trafficItem')
@ixNet.setMultiAttribute(trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-biDirectional', 'true',
    '-trafficType', 'ethernetVlan')
@ixNet.commit()

trafficItem1    = (@ixNet.remapIds(trafficItem1))[0]
endpointSet1 = @ixNet.add(trafficItem1, 'endpointSet')
source       = (networkGroup1)
destination  = (networkGroup2)

@ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', (''),
    '-scalableSources',       (''),
    '-multicastReceivers',    (''),
    '-scalableDestinations',  (''),
    '-ngpfFilters',           (''),
    '-trafficGroups',         (''),
    '-sources',               source,
    '-destinations',          destination)
@ixNet.commit()

@ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['mplsFlowDescriptor0','trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''))
@ixNet.commit()

###############################################################################
# Apply L2/L3 traffic                                                         #
###############################################################################
puts("Applying L2/L3 traffic")
@ixNet.execute('apply', (@ixNet.getRoot()) + '/traffic')
sleep(5)

###############################################################################
# Start L2/L3 traffic                                                         #
###############################################################################
puts("Starting L2/L3 traffic")
@ixNet.execute('start', (@ixNet.getRoot()) + '/traffic')

puts("Let traffic run for 60 seconds")
sleep(60)


###############################################################################
# Retrieve L2/L3 traffic item statistics                                      #
###############################################################################
puts("Retrieving all L2/L3 traffic stats")
viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page'
statcap  = @ixNet.getAttribute(viewPage, '-columnCaptions')
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

#################################################################################
# Stop L2/L3 traffic                                                            #
#################################################################################
puts("Stopping L2/L3 traffic")
@ixNet.execute('stop', (@ixNet.getRoot()) + '/traffic')
sleep(5)

################################################################################
# Stop all protocols                                                          #
################################################################################
puts("Stopping all protocols")
@ixNet.execute('stopAllProtocols')

puts("!!! Test Script Ends !!!")
