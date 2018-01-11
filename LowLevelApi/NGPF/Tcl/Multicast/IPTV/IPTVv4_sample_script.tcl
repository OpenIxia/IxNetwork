#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
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

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.28.41
    set ixTclPort   8921
    set ports       {{10.205.28.101 3 1} { 10.205.28.101 3 2}}
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
ixNet setAttr $t1dev1 -multiplier 1
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

puts "configuring ipv4 addresses"
ixNet setAttr $mvAdd1/singleValue -value "20.20.20.2"
ixNet setAttr $mvAdd2/singleValue -value "20.20.20.1"
ixNet setAttr $mvGw1/singleValue -value "20.20.20.1"
ixNet setAttr $mvGw2/singleValue -value "20.20.20.2"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

################################################################################
# adding IGMP Host over ipv4 stack
################################################################################ 
puts "Adding IGMP Host over IPv4 stack"
ixNet add $ip1 igmpHost
ixNet commit

set igmpHost [ixNet getList $ip1 igmpHost]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "IGMP Topology 1"
ixNet setAttr $topo2  -name "IPv4 Topology 2"
ixNet commit

################################################################################
# Enabling IPTV in IGMP host 
################################################################################
puts "Enabling IPTV"
set enableIptv [ixNet getAttr $igmpHost -enableIptv]
set singleValue [ixNet getList $enableIptv singleValue]
ixNet setAttr $singleValue -value true
ixNet commit

################################################################################
# Changing STB Leave Join Delay in IPTV tab of IGMP host
################################################################################
puts "Changing STB Leave Join Delay"
set iptv [ixNet getList $igmpHost iptv]
set stbLeaveJoinDelay [ixNet getAttr $iptv -stbLeaveJoinDelay]
set singleValue [ixNet getList $stbLeaveJoinDelay singleValue]
ixNet setAttr $singleValue -value 3000
ixNet commit

################################################################################
# Changing join latency threshold in IPTV tab of IGMP host
################################################################################
puts "Changing join latency threshold"
set joinLatencyThreshold [ixNet getAttr $iptv -joinLatencyThreshold]
set singleValue [ixNet getList $joinLatencyThreshold singleValue]
ixNet setAttr $singleValue -value 10000
ixNet commit

################################################################################
# Changing leave latency threshold in IPTV tab of IGMP host
################################################################################
puts "Changing leave latency threshold"
set leaveLatencyThreshold [ixNet getAttr $iptv -leaveLatencyThreshold]
set singleValue [ixNet getList $leaveLatencyThreshold singleValue]
ixNet setAttr $singleValue -value 10000
ixNet commit

################################################################################
# Changing zap behavior in IPTV tab of IGMP host
################################################################################
puts "Changing zap behavior"
set zapBehavior [ixNet getAttr $iptv -zapBehavior]
set singleValue [ixNet getList $zapBehavior singleValue]
ixNet setAttr $singleValue -value zapandview
ixNet commit

################################################################################
# Start protocol 
################################################################################
puts "Starting protocols and waiting for 20 seconds for protocols to come up"
ixNet exec startAllProtocols
after 20000

################################################################################
# Check statistics
################################################################################
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
set source       [list $topo2/deviceGroup:1/ethernet:1/ipv4:1]
set destination  [list $topo1/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList]
ixNet commit
ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"\
	-multicastDestinations [list [list false none 225.0.0.1 0.0.0.0 1]]\
	-scalableSources       [list]\
	-multicastReceivers    [list [list $topo1/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList 0 0 0]] \
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
# Apply and start L2/L3 traffic
###############################################################################
puts "applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

###############################################################################
# Starting IPTV
###############################################################################
puts "Starting IPTV"
ixNet exec startIptv $iptv
after 5000

###############################################################################
# Retrieve L2/L3 traffic item statistics
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
# Making on the fly changes for zapDirection, zapIntervalType, zapInterval,
# numChannelChangesBeforeView and viewDuration in IPTV tab of IGMP host
################################################################################
puts "Making on the fly chnages for zapDirection, zapIntervalType, zapInterval,\
    numChannelChangesBeforeView and viewDuration"
set zapDirection [ixNet getAttr $iptv -zapDirection]
set singleValue [ixNet getList $zapDirection singleValue]
ixNet setAttr $singleValue -value down

set zapIntervalType [ixNet getAttr $iptv -zapIntervalType]
set singleValue [ixNet getList $zapIntervalType singleValue]
ixNet setAttr $singleValue -value multicasttoleave

set zapInterval [ixNet getAttr $iptv -zapInterval]
set singleValue [ixNet getList $zapInterval singleValue]
ixNet setAttr $singleValue -value 10000


set numChannelChangesBeforeView [ixNet getAttr $iptv -numChannelChangesBeforeView]
set singleValue [ixNet getList $numChannelChangesBeforeView singleValue]
ixNet setAttr $singleValue -value 1

set viewDuration [ixNet getAttr $iptv -viewDuration]
set singleValue [ixNet getList $viewDuration singleValue]
ixNet setAttr $singleValue -value 10000
ixNet commit


################################################################################
# Applying changes one the fly
################################################################################
puts "Applying changes on the fly"
set root [ixNet getRoot]
set globals $root/globals
set topology $globals/topology
ixNet exec applyOnTheFly $topology
after 5000

###############################################################################
# Stopping IPTV
###############################################################################
puts "Stopping IPTV"
ixNet exec stopIptv $iptv
after 5000

################################################################################
# Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# Stop protocol 
################################################################################
puts "Stopping protocol"
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"

