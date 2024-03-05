#!/usr/bin/ruby
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
#    This script intends to demonstrate how to use NGPF BGP API                #
#    It will create 2 BGP topologies, it will start the emulation and          #
#    than it will retrieve and display few statistics                          #
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
ixTclServer = '10.200.115.203'
ixTclPort   = '8009'
ports       = [['10.200.115.151', '4', '1'], ['10.200.115.151', '4', '2']]

# get IxNet class
@ixNet = IxNetwork.new
puts("connecting to IxNetwork client")
@ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '7.40',
'-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
puts("cleaning up the old configfile, and creating an empty config")
@ixNet.execute('newConfig')

################################################################################
# protocol configuration section                                               #
################################################################################
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

print "Adding 2 device groups"
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

puts("Add ISISL3\n")
@ixNet.add(mac1, 'isisL3')
@ixNet.add(mac2, 'isisL3')
@ixNet.commit()

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

puts("Adding BGP over IP4 stacks")
@ixNet.add(ip1, 'bgpIpv4Peer')
@ixNet.add(ip2, 'bgpIpv4Peer')
@ixNet.commit()

bgp1 = @ixNet.getList(ip1, 'bgpIpv4Peer')[0]
bgp2 = @ixNet.getList(ip2, 'bgpIpv4Peer')[0]

puts("Enabling BGPLS Capability")
cap1 = @ixNet.getAttribute(bgp1, '-capabilityLinkStateNonVpn')
cap2 = @ixNet.getAttribute(bgp2, '-capabilityLinkStateNonVpn')
sv1 = @ixNet.getList(cap1, 'singleValue')[0]
sv2 = @ixNet.getList(cap2, 'singleValue')[0]
@ixNet.setAttribute(sv1, '-value', 'true')
@ixNet.setAttribute(sv2, '-value', 'true')

puts("Enabling BGPLS Filter Link State")
filter1 = @ixNet.getAttribute(bgp1, '-filterLinkState')
filter2 = @ixNet.getAttribute(bgp2, '-filterLinkState')
sv1 = @ixNet.getList(filter1, 'singleValue')[0]
sv2 = @ixNet.getList(filter2, 'singleValue')[0]
@ixNet.setAttribute(sv1, '-value', 'true')
@ixNet.setAttribute(sv1, '-value', 'true')

puts("Adding OSPFv2 over IP4 stacks")
ospf1 = @ixNet.add(ip1, 'ospfv2')
ospf2 = @ixNet.add(ip2, 'ospfv2')
@ixNet.commit()

puts("Changing OSPFv2 Network Type")
networkTypeMultiValue1 = @ixNet.getAttribute(ospf1, '-networkType')
@ixNet.setAttribute(@ixNet.getAttribute(ospf1, '-networkType') + '/singleValue', '-value', 'pointtopoint')
@ixNet.commit()

puts("Changing OSPFv2 Network Type")
networkTypeMultiValue1 = @ixNet.getAttribute(ospf2, '-networkType')
@ixNet.setAttribute(@ixNet.getAttribute(ospf2, '-networkType') + '/singleValue', '-value', 'pointtopoint')
@ixNet.commit()

puts("Renaming the topologies and the device groups")
@ixNet.setAttribute(topo1,  '-name', 'BGP Topology 1')
@ixNet.setAttribute(topo2,  '-name', 'BGP Topology 2')

@ixNet.setAttribute(t1dev1,  '-name', 'BGP Topology 1 Router')
@ixNet.setAttribute(t2dev1,  '-name', 'BGP Topology 2 Router')
@ixNet.commit()

puts("Setting IPs in BGP DUT IP tab")
@ixNet.setAttribute(@ixNet.getAttribute(bgp1, '-dutIp') + '/singleValue', '-value', '20.20.20.1')
@ixNet.setAttribute(@ixNet.getAttribute(bgp2, '-dutIp') + '/singleValue', '-value', '20.20.20.2')
@ixNet.commit()

puts("Adding the NetworkGroup with Routers at back of it")
prefixpool1  = @ixNet.execute('createDefaultStack', t2dev1, 'ipv4PrefixPools')
prefixpool2  = @ixNet.execute('createDefaultStack', t2dev1, 'ipv6PrefixPools')
prefixpool3  = @ixNet.execute('createDefaultStack', t2dev1, 'ipv4PrefixPools')
simulatedtopology  = @ixNet.execute('createDefaultStack', t2dev1, 'networkTopology')

networkGroup1 = (@ixNet.getList(t2dev1, 'networkGroup'))[0]
networkGroup2 = (@ixNet.getList(t2dev1, 'networkGroup'))[1]
networkGroup3 = (@ixNet.getList(t2dev1, 'networkGroup'))[2]
networkGroup4 = (@ixNet.getList(t2dev1, 'networkGroup'))[3]

@ixNet.setAttribute(networkGroup1, '-name', 'Direct/Static Routes')

ip4pool = (@ixNet.getList(networkGroup1, 'ipv4PrefixPools'))[0]
bgpIPRouteProperty = (@ixNet.getList(ip4pool, 'bgpIPRouteProperty'))[0]
adver = (@ixNet.getAttribute(bgpIPRouteProperty, '-advertiseAsBGPLSPrefix'))
sv1 = @ixNet.getList(adver, 'singleValue')[0]
@ixNet.setAttribute(sv1, '-value', 'true')
@ixNet.setAttribute(@ixNet.getAttribute(ip4pool, '-networkAddress') + '/singleValue', '-value', '30.30.30.1')

@ixNet.setAttribute(networkGroup2, '-name', 'IPv6 Prefix NLRI')
ip6pool = (@ixNet.getList(networkGroup2, 'ipv6PrefixPools'))[0]
bgpIPRouteProperty = (@ixNet.getList(ip6pool, 'bgpIPRouteProperty'))[0]
@ixNet.setAttribute(@ixNet.getAttribute(ip6pool, '-networkAddress') + '/singleValue', '-value', '3000::1')

@ixNet.setAttribute(networkGroup3, '-name', 'IPv4 Prefix NLRI')
ip4pool = @ixNet.getList(networkGroup3, 'ipv4PrefixPools')[0]
bgpIPRouteProperty = @ixNet.getList(ip4pool, 'bgpIPRouteProperty')[0]
@ixNet.setAttribute(@ixNet.getAttribute(ip4pool, '-networkAddress') + '/singleValue', '-value', '40.40.40.1')

@ixNet.setAttribute(networkGroup4, '-name', 'Node/Link/Prefix NLRI')
networkTopology = @ixNet.getList(networkGroup4, 'networkTopology')[0]
simRouter = (@ixNet.getList(networkTopology, 'simRouter'))[0]
ospfpseudo = (@ixNet.getList(simRouter, 'ospfPseudoRouter'))[0]
ospfPseudoRouterType1ExtRoutes = (@ixNet.getList(ospfpseudo, 'ospfPseudoRouterType1ExtRoutes'))[0]
active = (@ixNet.getAttribute(ospfPseudoRouterType1ExtRoutes, '-active'))
sv1 = (@ixNet.getList(active, 'singleValue'))[0]
@ixNet.setAttribute(sv1, '-value', 'true')
@ixNet.setAttribute(@ixNet.getAttribute(ospfPseudoRouterType1ExtRoutes, '-networkAddress') + '/singleValue', '-value', '50.50.50.1')

isisL3PseudoRouter = (@ixNet.getList(simRouter, 'isisL3PseudoRouter'))[0]
IPv4PseudoNodeRoutes = (@ixNet.getList(isisL3PseudoRouter, 'IPv4PseudoNodeRoutes'))[0]
active = (@ixNet.getAttribute(IPv4PseudoNodeRoutes, '-active'))
sv1 = (@ixNet.getList(active, 'singleValue'))[0]
@ixNet.setAttribute(sv1, '-value', 'true')
@ixNet.setAttribute(@ixNet.getAttribute(IPv4PseudoNodeRoutes, '-networkAddress') + '/singleValue', '-value', '60.60.60.1')
IPv6PseudoNodeRoutes = (@ixNet.getList(isisL3PseudoRouter, 'IPv6PseudoNodeRoutes'))[0]
active = (@ixNet.getAttribute(IPv6PseudoNodeRoutes, '-active'))
sv1 = (@ixNet.getList(active, 'singleValue'))[0]
@ixNet.setAttribute(sv1, '-value', 'true')
@ixNet.setAttribute(@ixNet.getAttribute(IPv6PseudoNodeRoutes, '-networkAddress') + '/singleValue', '-value', '6000::1')
@ixNet.commit()

################################################################################
# Start protocol and check statistics                                          #
################################################################################
puts("Starting protocols and waiting for 45 seconds for protocols to come up")
@ixNet.execute('startAllProtocols')
sleep(45)
puts("Fetching all Protocol Summary Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap   = @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList
        puts("***************************************************")
        index = 0
        for satIndv in statVal
            puts(statcap[index]+" "+satIndv)
            index = index + 1
        end
    end
end

puts("***************************************************")

puts("Verifying BGP Peer related stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"BGP Peer Per Port"/page'
statcap   = @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList
        puts("***************************************************")
        index = 0
        for satIndv in statVal
            puts(statcap[index]+" "+satIndv)
            index = index + 1
        end
    end
end

puts("***************************************************")

################################################################################
# On the fly section                                                           #
################################################################################
puts("Changing the Ipv4 & Ipv6 PrefixPool Address")
@ixNet.setAttribute(@ixNet.getAttribute(ip4pool, '-networkAddress') + '/singleValue', '-value', '90.90.90.1')
@ixNet.setAttribute(@ixNet.getAttribute(ip6pool, '-networkAddress') + '/singleValue', '-value', '7000::1')
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
# print learned info                                                          #
###############################################################################
@ixNet.execute('getLinkStateLearnedInfo', bgp1, '1')
sleep(5)

puts("Print BGP-LS Node/Link, BGP-LS IPv6 Prefix & BGP-LS IPv4 Prefix Learned Info")
linfo  = @ixNet.getList(bgp1, 'learnedInfo')[0]
linfoList = @ixNet.getList(linfo, 'table')
puts("***************************************************")
for table in linfoList :
    tableType = @ixNet.getAttribute(table, '-type')
    puts(tableType)
    puts("=================================================")
    columns = @ixNet.getAttribute(table, '-columns')
    puts(columns)
    values = @ixNet.getAttribute(table, '-values')
    for value in values :
        for word in values :
            puts(word)
        end
    end
end

sleep(15)

puts('Stopping protocols')
@ixNet.execute('stopAllProtocols')

puts('!!! Test Script Ends !!!')
