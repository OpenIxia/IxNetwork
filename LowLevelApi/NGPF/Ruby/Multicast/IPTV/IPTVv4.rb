# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2014 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    11/01/2012 - Sumeer Kumar - created sample                                #
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
#    This script intends to demonstrate how to use NGPF IPTVv4  API            #
#    It will create IPTV in IGMP Host topology, it will start the emulation and#
#    than it will retrieve and display few statistics                          #
# Ixia Softwares:                                                              #
#    IxOS      6.80 EA (6.80.1100.4)                                           #
#    IxNetwork 7.40 EA (7.40.929.8)                                            #
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
# Either feed the ixNetwork library path in the sys.path as below, or put the
# IxNetwork.rb file somewhere else where we ruby can autoload it.
# "IxNetwork.rb" is available in <IxNetwork_installer_path>\API\Ruby
################################################################################
$:.unshift 'C:\samples\IxNetwork.rb'
require 'IxNetwork'

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixApiServer = '10.200.115.203'
ixApiPort   = '8009'
ports       = [['10.200.115.151', '4', '1'], ['10.200.115.151', '4', '2']]

# get IxNet class
@ixNet = IxNetwork.new
puts("connecting to IxNetwork client")
@ixNet.connect(ixApiServer, '-port', ixApiPort, '-version', '7.40', '-setAttribute', 'strict')

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

################################################################################
# Adding IGMP Host over ipv4 stack
################################################################################ 
puts("Adding IGMP Host over IPv4 stack")
@ixNet.add(ip1, 'igmpHost')
@ixNet.commit()

igmpHost = @ixNet.getList(ip1, 'igmpHost')[0]

puts("Renaming the topologies and the device groups")
@ixNet.setAttribute(topo1, '-name', 'IGMP Topology 1')
@ixNet.setAttribute(topo2, '-name', 'IPv4 Topology 2')
@ixNet.commit()

################################################################################
# Enabling IPTV in IGMP host 
################################################################################
puts("Enabling IPTV")
enableIptv = @ixNet.getAttribute(igmpHost, '-enableIptv')
singleValue = @ixNet.getList(enableIptv, 'singleValue')[0]
@ixNet.setAttribute(singleValue, '-value', 'true')
@ixNet.commit()

################################################################################
# Changing STB Leave Join Delay in IPTV tab of IGMP host
################################################################################
puts("Changing STB Leave Join Delay")
iptv = @ixNet.getList(igmpHost, 'iptv')[0]
stbLeaveJoinDelay = @ixNet.getAttribute(iptv, '-stbLeaveJoinDelay')
singleValue = @ixNet.getList(stbLeaveJoinDelay, 'singleValue')[0]
@ixNet.setAttribute(singleValue, '-value', '3000')
@ixNet.commit()

################################################################################
# Changing join latency threshold in IPTV tab of IGMP host
################################################################################
puts("Changing join latency threshold")
joinLatencyThreshold = @ixNet.getAttribute(iptv, '-joinLatencyThreshold')
singleValue = @ixNet.getList(joinLatencyThreshold, 'singleValue')[0]
@ixNet.setAttribute(singleValue, '-value', '10000')
@ixNet.commit()

################################################################################
# Changing leave latency threshold in IPTV tab of IGMP host
################################################################################
puts("Changing leave latency threshold")
leaveLatencyThreshold = @ixNet.getAttribute(iptv, '-leaveLatencyThreshold')
singleValue = @ixNet.getList(leaveLatencyThreshold, 'singleValue')[0]
@ixNet.setAttribute(singleValue, '-value', '10000')
@ixNet.commit()

################################################################################
# Changing zap behavior in IPTV tab of IGMP host
################################################################################
puts("Changing zap behavior")
zapBehavior = @ixNet.getAttribute(iptv, '-zapBehavior')
singleValue = @ixNet.getList(zapBehavior, 'singleValue')[0]
@ixNet.setAttribute(singleValue, '-value', 'zapandview')
@ixNet.commit()

################################################################################
# Start protocol 
################################################################################
puts("Starting protocols and waiting for 20 seconds for protocols to come up")
@ixNet.execute('startAllProtocols')
sleep(20)

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

################################################################################
# L2/L3 Traffic configuration/apply/start section
################################################################################
puts("L2/L3 Traffic configuring")
trafficItem1 = @ixNet.add(@ixNet.getRoot() + '/traffic', 'trafficItem')
@ixNet.setMultiAttribute(trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv4')
@ixNet.commit()

trafficItem1 = @ixNet.remapIds(trafficItem1)[0]
endpointSet1 = @ixNet.add(trafficItem1, 'endpointSet')
source       = [topo2 + '/deviceGroup:1/ethernet:1/ipv4:1']
destination  = [topo1 + '/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList']
@ixNet.commit()

@ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', [['false', 'none', '225.0.0.1', '0.0.0.0', '1']],
    '-scalableSources',       [],
    '-multicastReceivers',    [[topo1 + '/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList', '0', '0', '0']],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source,
    '-destinations',          destination)
@ixNet.commit()

@ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['trackingenabled0', 'ipv4DestIp0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         [])
@ixNet.commit()

###############################################################################
# Apply and start L2/L3 traffic
###############################################################################
puts("Applying L2/L3 traffic")
@ixNet.execute('apply', @ixNet.getRoot() + '/traffic')
sleep(5)

puts('starting L2/L3 traffic')
@ixNet.execute('start', @ixNet.getRoot() + '/traffic')

###############################################################################
# Starting IPTV
###############################################################################
puts("Starting IPTV")
@ixNet.execute('startIptv', iptv)
sleep(5)

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
# Making on the fly changes for zapDirection, zapIntervalType, zapInterval,
# numChannelChangesBeforeView and viewDuration in IPTV tab of IGMP host
################################################################################
puts("Making on the fly chnages for zapDirection, zapIntervalType,\
zapInterval,numChannelChangesBeforeView and viewDuration")
zapDirection = @ixNet.getAttribute(iptv, '-zapDirection')
singleValue = @ixNet.getList(zapDirection, 'singleValue')[0]
@ixNet.setAttribute(singleValue, '-value', 'down')

zapIntervalType = @ixNet.getAttribute(iptv, '-zapIntervalType')
singleValue = @ixNet.getList(zapIntervalType, 'singleValue')[0]
@ixNet.setAttribute(singleValue, '-value', 'multicasttoleave')

zapInterval = @ixNet.getAttribute(iptv, '-zapInterval')
singleValue = @ixNet.getList(zapInterval, 'singleValue')[0]
@ixNet.setAttribute(singleValue, '-value', '10000')


numChannelChangesBeforeView = @ixNet.getAttribute(iptv, '-numChannelChangesBeforeView')
singleValue = @ixNet.getList(numChannelChangesBeforeView, 'singleValue')[0]
@ixNet.setAttribute(singleValue, '-value', '1')

viewDuration =  @ixNet.getAttribute(iptv, '-viewDuration')
singleValue = @ixNet.getList(viewDuration, 'singleValue')[0]
@ixNet.setAttribute(singleValue, '-value', '10000')
@ixNet.commit()


################################################################################
# Applying changes one the fly
################################################################################
puts("Applying changes on the fly")
root = @ixNet.getRoot()
globals = root + '/globals'
topology = globals + '/topology'
@ixNet.execute('applyOnTheFly', topology)
sleep(5)

###############################################################################
# Stopping IPTV
###############################################################################
puts("Stopping IPTV")
@ixNet.execute('stopIptv', iptv)
sleep(5)

################################################################################
# Stop L2/L3 traffic
#################################################################################
puts("Stopping L2/L3 traffic")
@ixNet.execute('stop', @ixNet.getRoot() + '/traffic')
sleep(5)

################################################################################
# Stop protocol 
################################################################################
puts("Stopping protocol")
@ixNet.execute('stopAllProtocols')
puts("!!! Test Script Ends !!!")

