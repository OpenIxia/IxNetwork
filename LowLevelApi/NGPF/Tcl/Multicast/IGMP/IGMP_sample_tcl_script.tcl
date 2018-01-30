#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    11/01/2012 - Chandan Mishra - created sample                                #
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
#    This script intends to demonstrate how to use NGPF IGMP API.              #
#                                                                              #
#    1. It will create 2 IGMP topologies, each having an ipv4 network          #
#       topology                                                               #
#    2. Add IGMP over ipv4 stack.                                              #
#    3. Change IGMP parameters like general query interval and general query   #
#       response interval                                                      #
#    4. Change protocol version of IGMP host and querier.                      #
#    5. Start IGMP protocol.                                                   #
#    6. Configure L2-L3 traffic.                                               #
#    7. Start L2/L3 protocol.                                                  #
#    8. Retreive protocol statistics                                           #                                                                         #
#    9. Retreive  L2/L3 protocol statistics.                                   #
#   10. Change igmpstart group address and applyOnTheFly                       #                                                #
#   11. Stop protocol and L2/L3 traffic.                                       #
#   12. Configure few parameters of IGMP host and querier which can be changed #
#       when protocol is not started.                                          #
#   13. Start protocol.                                                        #
#   14. Retreive protocol statistics                                           #
#   15. Stop all protocols.                                                    #                
# Ixia Softwares:                                                           #
#    IxOS      6.80 EB (6.80.1101.95)                                          #
#    IxNetwork 7.40 EB (7.40.0.336)                                            #
#                                                                              #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.25.83
    set ixTclPort   8009
    set ports       {{10.205.25.83 1 1} { 10.205.25.83 1 2}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# protocol configuration section
################################################################################ 
puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

after 10000

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force
puts "Adding 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet add [ixNet getRoot] topology -vports $vportRx
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

puts "Adding 2 device groups"
ixNet add $topo1 deviceGroup
ixNet add $topo2 deviceGroup
ixNet commit

set t1devices [ixNet getList $topo1 deviceGroup]
set t2devices [ixNet getList $topo2 deviceGroup]

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]

puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $t1dev1 -multiplier 2
ixNet setAttr $t2dev1 -multiplier 1
ixNet commit

puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]
set mac2 [ixNet getList $t2dev1 ethernet]

puts "Configuring the mac addresses"
ixNet setMultiAttr [ixNet getAttr $mac1 -mac]/counter\
	-direction  increment                        \
        -start      {18:03:73:C7:6C:B1}              \
        -step       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
        -value      {18:03:73:C7:6C:01}
ixNet commit

puts "Add ipv4"
ixNet add $mac1 ipv4
ixNet add $mac2 ipv4
ixNet commit

set ip1 [ixNet getList $mac1 ipv4]
set ip2 [ixNet getList $mac2 ipv4]

set mvAdd1 [ixNet getAttr $ip1 -address]
set mvAdd2 [ixNet getAttr $ip2 -address]
set mvGw1  [ixNet getAttr $ip1 -gatewayIp]
set mvGw2  [ixNet getAttr $ip2 -gatewayIp]

puts "Configuring ipv4 addresses"
ixNet setMultiAttr [ixNet add $mvAdd1 counter]\
	-step 0.0.0.1 \
	-start 20.20.20.2 \
	-direction increment
ixNet commit
ixNet setAttr $mvAdd2/singleValue -value "20.20.20.1"
ixNet setAttr $mvGw1/singleValue  -value "20.20.20.1"
ixNet setAttr $mvGw2/singleValue  -value "20.20.20.2"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit
################################################################################
# adding IGMP over ipv4 stack
################################################################################ 
puts "Adding IGMP over IP4 stack"
ixNet add $ip1 igmpHost
ixNet add $ip2 igmpQuerier
ixNet commit
set igmphost [ixNet getList $ip1 igmpHost]
set igmpquerier [ixNet getList $ip2 igmpQuerier]
puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "IGMPHost Topology 1"
ixNet setAttr $topo2  -name "IGMPQuerier Topology 2"
ixNet commit

################################################################################
# change genaral query interval
################################################################################
puts "Changing genaral query interval"
set gqueryi [ixNet getAttr $igmpquerier -generalQueryInterval]
ixNet setMultiAttr $gqueryi\
     -clearOverlays false \
	 -pattern counter
ixNet commit
ixNet setMultiAttr [ixNet add $gqueryi counter]\
     -step 1 \
	 -start 140 \
	 -direction increment
ixNet commit

################################################################################
# change general query response interval
################################################################################
puts "Changing general query response interval"
set gqueryrespvi [ixNet getAttr $igmpquerier -generalQueryResponseInterval]
ixNet setMultiAttr $gqueryrespvi\
     -clearOverlays false \
	 -pattern counter
 ixNet commit
ixNet setMultiAttr [ixNet add $gqueryrespvi counter]\
     -step 1 \
	 -start 11000 \
	 -direction increment
ixNet commit

################################################################################
# change version of IGMP HOST
################################################################################
puts "Changing version of IGMP HOST to v3"
set igmpport1  [ixNet getList $igmphost port]
set vesriontypehost [ixNet getAttr $igmpport1 -versionType]
set versionvaluehost [ixNet getList $vesriontypehost singleValue]
ixNet setAttr $versionvaluehost -value version3
ixNet commit

################################################################################
# change version of IGMP querier
################################################################################
puts "Changing version of IGMP querier to v3"
set igmpport2  [ixNet getList $igmpquerier port]
set vesriontypequerier [ixNet getAttr $igmpport2 -versionType]
set versionvaluequerier [ixNet getList $vesriontypequerier singleValue]
ixNet setAttr $versionvaluequerier -value version3
ixNet commit

################################################################################
# Discard learned info
################################################################################
puts "Disabling disacrd learned info "
set discardLearntInfo1 [ixNet getAttr $igmpquerier -discardLearntInfo]
ixNet setMultiAttr $discardLearntInfo1\
	-clearOverlays false \
	-pattern singleValue
ixNet commit
ixNet setMultiAttr [ixNet add $discardLearntInfo1 singleValue]\
	-value false
ixNet commit

################################################################################
# Start protocol and check statistics
################################################################################
puts "Starting protocols and waiting for 20 seconds for protocols to come up"
ixNet exec startAllProtocols
after 20000
puts "Verifying all the stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Protocols Summary"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

################################################################################
# change state of IGMP Groupranges(only when the protocol is started)
################################################################################
set ipv4grouplist1 [ixNet getList $igmphost igmpMcastIPv4GroupList]
puts "Change state of IGMP Groupranges to leave"
ixNet exec  igmpLeaveGroup $ipv4grouplist1

###############################################################################
# print learned info
###############################################################################
puts "Getting learnedInfo"
ixNet exec igmpGetLearnedInfo $igmpquerier
after 5000
set learnedInfo [ixNet getList $igmpquerier learnedInfo]
after 1000
set table [ixNet getList $learnedInfo table]
ixNet getAttr $table -value
ixNet getAttr $table -values
puts "[ixNet getAttr $table -values]"

################################################################################
# L2/L3 Traffic configuration/apply/start section
################################################################################
puts "L2/L3 Traffic configuring"
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
	-name {Traffic Item 1}           \
	-roundRobinPacketOrdering false  \
	-trafficType ipv4
ixNet commit
set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source [list $topo2/deviceGroup:1/ethernet:1/ipv4:1]
set destination  [list $topo1/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList]
ixNet commit
ixNet setMultiAttribute $endpointSet1\
	-name                  "EndpointSet-1"\
	-multicastDestinations [list [list false none 225.0.0.1 0.0.0.0 1]]\
	-scalableSources       [list]\
	-multicastReceivers    [list [list $topo1/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList 0 0 0]\
                           [list $topo1/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList 0 1 0]] \
	-scalableDestinations  [list]\
	-ngpfFilters           [list]\
	-trafficGroups         [list]\
	-sources               $source\
	-destinations          $destination\	
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking\
	-trackBy [list trackingenabled0 ipv4DestIp0] \
        -values [list ] \
        -fieldWidth thirtyTwoBits \
        -protocolOffset Root.0
ixNet commit

###############################################################################
# 9. Apply and start L2/L3 traffic
###############################################################################
puts "Applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000
puts "Starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

###############################################################################
# 12. Retrieve L2/L3 traffic item statistics
###############################################################################
puts "Verifying all the L2-L3 traffic stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Flow Statistics"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

################################################################################
# change igmpstart group address and apply
################################################################################
puts "Changing igmpstart group address and applyOnTheFly changes"
set mcastaddr1 [ixNet getAttr $ipv4grouplist1 -startMcastAddr]
puts "Changing IGMP start group address"
ixNet setAttr $mcastaddr1 -clearOverlays false
ixNet setAttr $mcastaddr1 -pattern counter
ixNet commit
puts "Configuring the igmpstart group address"
ixNet setMultiAttr [ixNet add $mcastaddr1 counter]\
        -step 0.0.0.1 \
        -start 225.1.1.1 \
        -direction increment
ixNet commit
set root [ixNet getRoot]
set globals $root/globals
set topology $globals/topology
ixNet exec applyOnTheFly $topology

################################################################################
# 14. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# stop protocol 
################################################################################
puts "Stopping protocol"
ixNet exec stopAllProtocols
after 10000

################################################################################
# changing sourcemode
################################################################################
puts "Changing sourcemode"
set sourcemode [ixNet getAttr $ipv4grouplist1 -sourceMode]
ixNet setMultiAttr [ixNet add $sourcemode singleValue]\
	-value exclude
ixNet commit

################################################################################
# change number of source address count
#(to be changed only when the protocol is not started)
################################################################################
puts "Changing number of source address count" 
set ipv4sourcelist1 [ixNet getList $ipv4grouplist1 igmpUcastIPv4SourceList]
set ucastSrcAddrCnt [ixNet getAttr $ipv4sourcelist1 -ucastSrcAddrCnt]
ixNet setAttr $ucastSrcAddrCnt/singleValue -value 2
ixNet commit

################################################################################
# change general query responsemode
################################################################################
puts "Changing general query responsemode"
set gQResponseMode [ixNet getAttr $igmphost -gQResponseMode]
ixNet setMultiAttr $gQResponseMode\
	-clearOverlays false \
	-pattern singleValue
ixNet commit
ixNet setMultiAttr [ixNet add $gQResponseMode singleValue]\
	-value false
ixNet commit
		
################################################################################
# change group specific query responsemode
################################################################################
puts "Disabling group specific query responsemode"
set gSResponseMode [ixNet getAttr $igmphost -gSResponseMode]
ixNet setMultiAttr $gSResponseMode\
	-clearOverlays false \
	-pattern singleValue
ixNet commit
ixNet setMultiAttr [ixNet add $gSResponseMode singleValue]\
        -value false
ixNet commit

################################################################################
# change immediate responsemode
################################################################################
puts "Disabling immediate responsemode"
set imResponse [ixNet getAttr $igmphost -imResponse]
ixNet setMultiAttr $imResponse\
	-clearOverlays false \
	-pattern singleValue
ixNet commit
ixNet setMultiAttr [ixNet add $imResponse singleValue]\
        -value true
ixNet commit

################################################################################
# configure jlMultiplier value
################################################################################
puts "Configuring jlMultiplier value"
ixNet setAttr $igmphost -jlMultiplier 2
ixNet commit

################################################################################
# change router alert value
################################################################################
puts "Changing router alert value"
set routerAlert [ixNet getAttr $igmphost -routerAlert]
ixNet setMultiAttr $routerAlert\
	-clearOverlays false \
	-pattern singleValue
ixNet commit
ixNet setMultiAttr [ixNet add $routerAlert singleValue]\
        -value false
ixNet commit

################################################################################
# change value of number of group ranges
################################################################################
puts "Change value of number of group ranges"
ixNet setAttr $igmphost -noOfGrpRanges 2
ixNet commit

################################################################################
# Change unsolicit response mode
################################################################################
puts "Change unsolicit response mode to true"
set uSResponseMode [ixNet getAttr $igmphost -uSResponseMode]
ixNet setMultiAttr $uSResponseMode\
	-clearOverlays false \
	-pattern singleValue
ixNet commit
ixNet setMultiAttr [ixNet add $uSResponseMode singleValue]\
	-value true
ixNet commit

################################################################################
# enable proxy reporting
################################################################################
puts "Enable proxy reporting"
set enableProxyReporting [ixNet getAttr $igmphost -enableProxyReporting]
ixNet setMultiAttr $enableProxyReporting\
	-clearOverlays false \
	-pattern singleValue
 ixNet commit
ixNet setMultiAttr [ixNet add $enableProxyReporting singleValue]\
        -value true
	ixNet commit
	
################################################################################
# change number of source ranges
#(to be changed only when the protocol is not started)
################################################################################
puts "Change number of source ranges"
ixNet setAttr $ipv4grouplist1 -noOfSrcRanges 2
ixNet commit

################################################################################
# change state of IGMP sourceranges
################################################################################
puts "Changing state of IGMP sourceranges"
set ipv4sourcelist1 [ixNet getList $ipv4grouplist1 igmpUcastIPv4SourceList]
ixNet exec igmpJoinSource $ipv4sourcelist1

################################################################################
# Start protocol and check statistics
################################################################################
puts "Starting protocols and waiting for 20 seconds for protocols to come up"
ixNet exec startAllProtocols
after 20000
puts "Verifying all the stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Protocols Summary"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

################################################################################
# 15. Stop all protocols
################################################################################
puts "Stopping protocol"
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"

