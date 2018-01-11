# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    11/01/2012 - Chandan Mishra - created sample                              #
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
#    This script intends to demonstrate how to use NGPF MLD API.               #
#                                                                              #
#    1. It will create 2 MLD topologies, each having an ipv6 network           #
#       topology                                                               #
#    2. Add MLD over ipv6 stack.                                               #
#    3. Change MLD parameters like general query interval and general query    #
#       response interval                                                      #
#    4. Change protocol version of MLD host and querier.                       #
#    5. Start MLD protocol.                                                    #
#    6. Configure L2-L3 traffic.                                               #
#    7. Start L2/L3 protocol.                                                  #
#    8. Retreive protocol statistics                                           #
#    9. Retreive  L2/L3 protocol statistics.                                   #
#   10. Change mldstart group address and applyOnTheFly                        #
#   11. Stop protocol and L2/L3 traffic.                                       #
#   12. Configure few parameters of MLD host and querier which can be changed  #
#       when protocol is not started.                                          #
#   13. Start protocol.                                                        #
#   14. Retreive protocol statistics                                           #
#   15. Stop all protocols.                                                    #                
# Ixia Softwares:                                                              #
#    IxOS      6.80 EB (6.80.1100.7)                                           #
#    IxNetwork 7.40 EB (7.40.929.15)                                           #
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
@ixNet.setAttribute(t1dev1, '-multiplier', '2')
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

#puts('@ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet\')')
#puts(@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet'))

puts("Add ipv4")
@ixNet.add(mac1, 'ipv6')
@ixNet.add(mac2, 'ipv6')
@ixNet.commit()

ip1 = @ixNet.getList(mac1, 'ipv6')[0]
ip2 = @ixNet.getList(mac2, 'ipv6')[0]

mvAdd1 = @ixNet.getAttribute(ip1, '-address')
mvAdd2 = @ixNet.getAttribute(ip2, '-address')
mvGw1  = @ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = @ixNet.getAttribute(ip2, '-gatewayIp')
puts("Configuring ipv4 addresses")
@ixNet.setMultiAttribute(@ixNet.add(mvAdd1, 'counter'),
    '-step', '0:0:0:0:0:0:0:1',
    '-start', '2001:0:0:1:0:0:0:2',
    '-direction', 'increment')
@ixNet.commit()
@ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', "2001:0:0:1:0:0:0:1")
@ixNet.setAttribute(mvGw1 + '/singleValue',  '-value', "2001:0:0:1:0:0:0:1")
@ixNet.setAttribute(mvGw2 + '/singleValue',  '-value', "2001:0:0:1:0:0:0:2")

@ixNet.setAttribute(@ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '64')
@ixNet.setAttribute(@ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '64')

@ixNet.setMultiAttribute(@ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.setMultiAttribute(@ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.commit()

################################################################################
# adding MLD over ipv6 stack
################################################################################ 
puts("Adding MLD over IP6 stack")
@ixNet.add(ip1, 'mldHost')
@ixNet.add(ip2, 'mldQuerier')
@ixNet.commit()
mldHost    = @ixNet.getList(ip1, 'mldHost')[0]
mldQuerier = @ixNet.getList(ip2, 'mldQuerier')[0]
puts("Renaming the topologies and the device groups")
@ixNet.setAttribute(topo1, '-name', 'mldHost Topology 1')
@ixNet.setAttribute(topo2, '-name', 'mldQuerier Topology 2')
@ixNet.commit()

################################################################################
# change genaral query interval
################################################################################
puts("Changing genaral query interval")
gqueryi = @ixNet.getAttribute(mldQuerier, '-generalQueryInterval')
@ixNet.setMultiAttribute (gqueryi,
         '-clearOverlays', 'false',
     '-pattern', 'counter')
@ixNet.commit()
@ixNet.setMultiAttribute(@ixNet.add(gqueryi, 'counter'),
        '-step', '1', 
    '-start', '140',
    '-direction', 'increment')                        
@ixNet.commit()

################################################################################
# change general query response interval
################################################################################
puts("Changing general query response interval")
gqueryrespvi = @ixNet.getAttribute(mldQuerier, '-generalQueryResponseInterval')
@ixNet.setMultiAttribute (gqueryrespvi,
         '-clearOverlays', 'false',
     '-pattern', 'counter')
@ixNet.commit()
@ixNet.setMultiAttribute(@ixNet.add(gqueryrespvi, 'counter'),
        '-step', '1',
    '-start', '11000',
    '-direction', 'increment')
@ixNet.commit()

################################################################################
# change version of MLD HOST
################################################################################
puts("Changing version of MLD HOST to v2")
mldport1 = @ixNet.getList(mldHost, 'port')[0]
vesriontypehost = @ixNet.getAttribute(mldport1, '-versionType')
versionvaluehost = @ixNet.getList(vesriontypehost, 'singleValue')[0]
@ixNet.setAttribute(versionvaluehost, '-value', 'version2')                                
@ixNet.commit()

################################################################################
# change version of MLD querier
################################################################################
puts("Changing version of MLD querier to v2")
mldport2 =@ixNet.getList(mldQuerier, 'port')[0]
vesriontypequerier = @ixNet.getAttribute(mldport2, '-versionType')
versionvaluequerier = @ixNet.getList(vesriontypequerier, 'singleValue')[0]
@ixNet.setAttribute(versionvaluequerier, '-value', 'version2')
@ixNet.commit()

################################################################################
# Discard learned info
################################################################################
puts("Disabling disacrd learned info ")
discardLearntInfo1 = @ixNet.getAttribute(mldQuerier, '-discardLearntInfo')
@ixNet.setMultiAttribute(discardLearntInfo1,
    '-clearOverlays', 'false',
    '-pattern', 'singleValue')
@ixNet.commit()
@ixNet.setMultiAttribute(@ixNet.add(discardLearntInfo1, 'singleValue'),
    '-value', 'false')
@ixNet.commit()

################################################################################
# Start protocol and check statistics
################################################################################
puts("Starting protocols and waiting for 20 seconds for protocols to come up")
@ixNet.execute('startAllProtocols')
sleep(20)
puts("Verifying all the stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap = @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues')
    for statVal in statValList
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
# change state of MLD Groupranges(only when the protocol is started)
################################################################################
ipv6grouplist1 = (@ixNet.getList(mldHost, 'mldMcastIPv6GroupList'))[0]
puts("Change state of MLD Groupranges to leave")
@ixNet.execute('mldLeaveGroup', ipv6grouplist1)

###############################################################################
# puts learned info
###############################################################################
puts("Getting learnedInfo")
@ixNet.execute('mldGetLearnedInfo', mldQuerier)
sleep(5)
learnedInfo = @ixNet.getList(mldQuerier, 'learnedInfo')[0]
sleep(10)
table = @ixNet.getList(learnedInfo, 'table')[0]
value = @ixNet.getAttribute(table, '-values')
puts(value)

################################################################################
# L2/L3 Traffic configuration/apply/start section
################################################################################
puts("L2/L3 Traffic configuring")
trafficItem1 = @ixNet.add(@ixNet.getRoot() + '/traffic', 'trafficItem')
@ixNet.setMultiAttribute(trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv6')
@ixNet.commit()
trafficItem1 = @ixNet.remapIds(trafficItem1)[0]
endpointSet1 = @ixNet.add(trafficItem1, 'endpointSet')
source       = [topo2 + '/deviceGroup:1/ethernet:1/ipv6:1']
destination  = [topo1 + '/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList']
@ixNet.commit()

@ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', [['false', 'none', 'ff03:0:0:0:0:0:0:1', '0::0', '1']],
    '-scalableSources',       [],
    '-multicastReceivers',    [[topo1 + '/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList', '0', '0', '0'], [topo1 + '/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList', '0', '1', '0']],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source,
    '-destinations',          destination)
@ixNet.commit()

@ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['trackingenabled0', 'ipv6DestIp0'],
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
# 12. Retrieve L2/L3 traffic item statistics
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

###############################################################################
# change MLDstart group address and applyOnTheFly
################################################################################
puts("Changing mldstart group address and applyOnTheFly changes")
mcastaddr1 = @ixNet.getAttribute(ipv6grouplist1, '-startMcastAddr')
puts("Changing MLD start group address")
@ixNet.setAttribute(mcastaddr1, '-clearOverlays', 'false')
@ixNet.setAttribute(mcastaddr1, '-pattern', 'counter')
@ixNet.commit()
puts("Configuring the mldstart group address")
@ixNet.setMultiAttribute(@ixNet.add(mcastaddr1, 'counter'),
        '-step', '0:0:0:0:0:0:0:1',
        '-start', 'ff04:0:0:0:0:0:0:1',
        '-direction', 'increment')
@ixNet.commit()

globalObj = @ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
puts("Applying changes on the fly")
begin
    @ixNet.execute('applyOnTheFly', topology)
rescue
    puts("error in applying on the fly change")
end
sleep(5)

################################################################################
# 14. Stop L2/L3 traffic
################################################################################
puts('Stopping L2/L3 traffic')
@ixNet.execute('stop', @ixNet.getRoot() + '/traffic')
sleep(5)

################################################################################
# 15. Stop all protocols
################################################################################
puts('Stopping protocols')
@ixNet.execute('stopAllProtocols')
sleep(10)
puts('!!! *********** !!!')

################################################################################
# changing sourcemode
################################################################################
puts("Changing sourcemode")
sourcemode = (@ixNet.getAttribute(ipv6grouplist1, '-sourceMode'))
@ixNet.setMultiAttribute(@ixNet.add(sourcemode, 'singleValue'),
    '-value', 'exclude')
@ixNet.commit()

################################################################################
# change number of source address count
#(to be changed only when the protocol is not started)
################################################################################
puts("Changing number of source address count")
ipv4sourcelist1 = @ixNet.getList(ipv6grouplist1, 'mldUcastIPv6SourceList')[0]
ucastSrcAddrCnt = @ixNet.getAttribute(ipv4sourcelist1, '-ucastSrcAddrCnt')
singleValue = @ixNet.getList(ucastSrcAddrCnt, 'singleValue')[0] 
@ixNet.setAttribute(singleValue,
        '-value', '2')
@ixNet.commit()

################################################################################
# change general query responsemode
################################################################################
puts "Changing general query responsemode"
gQResponseMode = (@ixNet.getAttribute(mldHost, '-gQResponseMode'))
@ixNet.setMultiAttribute(gQResponseMode,
    '-clearOverlays', 'false',
    '-pattern', 'singleValue')
@ixNet.commit()
@ixNet.setMultiAttribute(@ixNet.add(gQResponseMode, 'singleValue'),
    '-value', 'false')
@ixNet.commit()

################################################################################
# change group specific query responsemode
################################################################################
puts("Disabling group specific query responsemode")
gSResponseMode = (@ixNet.getAttribute(mldHost, '-gSResponseMode'))
@ixNet.setMultiAttribute(gSResponseMode,
    '-clearOverlays', 'false',
    '-pattern', 'singleValue')
@ixNet.commit()
@ixNet.setMultiAttribute(@ixNet.add(gSResponseMode, 'singleValue'),
        '-value', 'false')
@ixNet.commit()

################################################################################
# change immediate responsemode
################################################################################
puts("Disabling immediate responsemode")
imResponse = (@ixNet.getAttribute(mldHost, '-imResponse'))
@ixNet.setMultiAttribute(imResponse,
    '-clearOverlays', 'false',
    '-pattern', 'singleValue')
@ixNet.commit()
@ixNet.setMultiAttribute(@ixNet.add(imResponse, 'singleValue'),
        '-value', 'true')
@ixNet.commit()

################################################################################
# configure jlMultiplier value
################################################################################
puts("Configuring jlMultiplier value")
@ixNet.setAttribute(mldHost, '-jlMultiplier', '2')
@ixNet.commit()

################################################################################
# change router alert value
################################################################################
puts("Changing router alert value")
routerAlert = (@ixNet.getAttribute(mldHost, '-routerAlert'))
@ixNet.setMultiAttribute(routerAlert,
    '-clearOverlays', 'false',
    '-pattern', 'singleValue')
@ixNet.commit()
@ixNet.setMultiAttribute(@ixNet.add(routerAlert, 'singleValue'),
        '-value', 'false')
@ixNet.commit()

################################################################################
# change value of number of group ranges
################################################################################
puts("Change value of number of group ranges")
@ixNet.setAttribute(mldHost, '-noOfGrpRanges', '2')
@ixNet.commit()

################################################################################
# Change unsolicit response mode
################################################################################
puts("Change unsolicit response mode to true")
uSResponseMode =(@ixNet.getAttribute(mldHost, '-uSResponseMode'))
@ixNet.setMultiAttribute(uSResponseMode,
    '-clearOverlays', 'false',
    '-pattern', 'singleValue')
@ixNet.commit()
@ixNet.setMultiAttribute(@ixNet.add(uSResponseMode, 'singleValue'),
    '-value', 'true')
@ixNet.commit()

################################################################################
# enable proxy reporting
################################################################################
puts("Enable proxy reporting")
enableProxyReporting =(@ixNet.getAttribute(mldHost, '-enableProxyReporting'))
@ixNet.setMultiAttribute(enableProxyReporting,
    '-clearOverlays', 'false',
    '-pattern', 'singleValue')
@ixNet.commit()
@ixNet.setMultiAttribute(@ixNet.add(enableProxyReporting, 'singleValue'),
        '-value', 'true')
@ixNet.commit()

################################################################################
# change number of source ranges
#(to be changed only when the protocol is not started)
################################################################################
puts("Change number of source ranges")
@ixNet.setAttribute(ipv6grouplist1, '-noOfSrcRanges', '2')
@ixNet.commit()

################################################################################
# change state of MLD sourceranges
################################################################################
puts("Changing state of MLD sourceranges")
ipv6sourcelist1 = (@ixNet.getList(ipv6grouplist1, 'mldUcastIPv6SourceList'))
@ixNet.execute('mldJoinSource',ipv6sourcelist1)

################################################################################
# Start protocol and check statistics
################################################################################
puts("Starting protocols and waiting for 20 seconds for protocols to come up")
@ixNet.execute('startAllProtocols')
sleep(20)
puts("Verifying all the stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap = @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues')
    for statVal in statValList
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
# Stop all protocols
################################################################################
puts('Stopping protocols')
@ixNet.execute('stopAllProtocols')
sleep(10)
puts('!!! Test Script Ends !!!')

