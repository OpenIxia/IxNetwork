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
#    This script intends to demonstrate how to use Low Level Ruby APIs to      #
#    import BGP IPv4 Routes in Ixia csv format.                                #
#    1. It will create 2 BGP topologies.                                       #
#    2. Generate Statistical IPv4 routes in topology2.                         #
#    3. Start the BGP protocol.                                                #
#    4. Retrieve protocol statistics.                                          #
#    5. Retrieve protocol learned info.                                        #
#    6. Stop all protocols.                                                    #
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
ports       = [['10.200.115.151', '4', '1'], ['10.200.115.151', '4', '2']]

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

puts("Renaming the topologies and the device groups")
@ixNet.setAttribute(topo1, '-name', 'BGP Topology 1')
@ixNet.setAttribute(topo2, '-name', 'BGP Topology 2')

@ixNet.setAttribute(t1dev1, '-name', 'BGP Topology 1 Router')
@ixNet.setAttribute(t2dev1, '-name', 'BGP Topology 2 Router')
@ixNet.commit()

puts("Setting IPs in BGP DUT IP tab")
@ixNet.setAttribute(@ixNet.getAttribute(bgp1, '-dutIp') + '/singleValue', '-value', '20.20.20.1')
@ixNet.setAttribute(@ixNet.getAttribute(bgp2, '-dutIp') + '/singleValue', '-value', '20.20.20.2')
@ixNet.commit()

################################################################################
# Import BGP IPv4 Routes in ixia csv format in Topology2                       #
################################################################################
puts("Importing BGP Routes in Ixia Format")
networkGroup = @ixNet.add(t2dev1, 'networkGroup')
@ixNet.commit()
networkGroup = @ixNet.remapIds(networkGroup)[0]
ipv4PrefixPools = @ixNet.add(networkGroup, 'ipv4PrefixPools')
@ixNet.commit()
ipv4PrefixPools = @ixNet.remapIds(ipv4PrefixPools)[0]
bgpIPRouteProperty = @ixNet.getList(ipv4PrefixPools, 'bgpIPRouteProperty')[0]
importBgpRoutesParams = bgpIPRouteProperty + '/importBgpRoutesParams'
@ixNet.setMultiAttribute(importBgpRoutesParams,
    '-routeDistributionType', 'roundRobin',
    '-bestRoutes', 'false',
    '-nextHop', 'overwriteTestersAddress',
    '-fileType', 'csv',
    '-dataFile', @ixNet.readFrom('BGP_RouteImport_sample.csv')
)
@ixNet.commit()
@ixNet.execute('importBgpRoutes', importBgpRoutesParams)
puts("Successfully imported BGP IPv4 Routes")

################################################################################
# Start BGP protocol and wait for 45 seconds                                   #
################################################################################
puts("Starting protocols and waiting for 45 seconds for protocols to come up")
@ixNet.execute('startAllProtocols')
sleep(45)

################################################################################
# Retrieve protocol statistics                                              #
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
# Enabling the BGP IPv4 Unicast Learned Info Filter on the fly                 #
################################################################################
puts("Enabling IPv4 Unicast Learned Information for BGP Router")
@ixNet.setAttribute(@ixNet.getAttribute(bgp1, '-filterIpV4Unicast') + '/singleValue', '-value', 'true')
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
# puts learned info                                                          #
###############################################################################
puts("Fetching BGP learned info after enabling ipv4 learned info")
@ixNet.execute('getIPv4LearnedInfo', bgp1, '1')
sleep(5)
linfo  = @ixNet.getList(bgp1, 'learnedInfo')[0]
values = @ixNet.getAttribute(linfo, '-values')

puts("***************************************************")
for v in values
    puts(v)
end
puts("***************************************************")

################################################################################
# Stop all protocols                                                           #
################################################################################
puts('Stopping protocols')
@ixNet.execute('stopAllProtocols')

puts('!!! Test Script Ends !!!')
