#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/12/2014 - Sayantan Pramanick - created sample                          #
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
#    This script intends to demonstrate how to use NGPF Audio Video Bridging   #
#     API.                                                                     #
#                                                                              #
#    1. It will create one MSRP Talker in one topology and 2 MSRP Listeners    #
#       in another topology. gPTP clocks will be added in talkers and          #
#       listeners.                                                             #
#    2. Start all protocols.                                                   #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    7. Configure L2-L3 traffic.                                               #
#    9. Start the L2-L3 traffic.                                               #
#   12. Retrieve L2-L3 traffic stats.                                          #
#   13. Stop L2-L3 traffic.                                                    #
#   15. Stop all protocols.                                                    #                                                                                          
# Ixia Softwares:                                                              #
#    IxOS      6.80 EB (6.80.1101.110)                                         #
#    IxNetwork 7.40 EB (7.40.0.355)                                            #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.25.88
    set ixTclPort   7777
    set ports       {{10.205.28.65 2 3} { 10.205.28.65 2 4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure AVB protocols as per the
#    description given above
################################################################################ 
puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

puts "Adding 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet add [ixNet getRoot] topology -vports $vportRx
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

puts "Adding 1 device groups in topology 1"
ixNet add $topo1 deviceGroup

puts "Adding 2 device groups in topology 2"
ixNet add $topo2 deviceGroup
ixNet add $topo2 deviceGroup
ixNet commit


set t1devices [ixNet getList $topo1 deviceGroup]
set t2devices [ixNet getList $topo2 deviceGroup]

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]
set t2dev2 [lindex $t2devices 1]

puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $t1dev1 -multiplier 1
ixNet setAttr $t2dev1 -multiplier 2
ixNet setAttr $t2dev2 -multiplier 1
ixNet commit

puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet add $t2dev2 ethernet
ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]
set mac2 [ixNet getList $t2dev1 ethernet]
set mac3 [ixNet getList $t2dev2 ethernet]

puts "Configuring the mac addresses"
ixNet setMultiAttr [ixNet getAttr $mac1 -mac]/counter\
        -direction  increment                        \
        -start      {22:22:22:22:22:22}              \
        -step       {00:00:00:00:00:01}

ixNet setMultiAttr [ixNet getAttr $mac2 -mac]/counter\
        -direction  increment                        \
        -start      {44:44:44:44:44:44}              \
        -step       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac3 -mac]/singleValue\
        -value      {66:66:66:66:66:66}
ixNet commit

puts "Adding MSRP talker in topology 1"
set talker1 [ixNet add $mac1 msrpTalker]
ixNet commit
set talker1 [ixNet remapIds $talker1]

puts "Configuring 2 streams in talker"
ixNet setAttr $talker1 -streamCount 2
ixNet commit

puts "Adding gPTP clock in topology 1"
set ptp1 [ixNet add $mac1 ptp]
ixNet commit
set ptp1 [ixNet remapIds $ptp1]

puts "Setting clock role as master in AVB talker"
ixNet setAttr [ixNet getAttr $ptp1 -role]/singleValue\
        -value master
ixNet commit

puts "Adding MSRP listener in topology 2"
set listener1 [ixNet add $mac2 msrpListener]
ixNet commit
set listener1 [ixNet remapIds $listener1]

puts "Adding gptp clock in topology 2"
set ptp2 [ixNet add $mac3 ptp]
ixNet commit
set ptp2 [ixNet remapIds $ptp2]

ixNet setAttr [ixNet getAttr $ptp2 -profile]/singleValue\
        -value ieee8021as
ixNet commit

################################################################################
# 2. Start AVB protocols and wait for 60 seconds
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
puts "Fetching all Protocol Summary Stats\n"
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
# 4. Retrieve protocol learned info
################################################################################
puts "Fetching MSRP Talker Learned Info"
ixNet exec getTalkerDatabases $talker1
after 5000
set linfo [ixNet getList $talker1 learnedInfo]
set streamDb [lindex $linfo 0]
set domainDb [lindex $linfo 1]
set vlanDb   [lindex $linfo 2]


set values [ixNet getAttribute $streamDb -values]
set column [ixNet getAttribute $streamDb -columns]
puts "***************************************************"
puts "****  MSRP Talker stream database learned info ****"
for {set index 0} {$index < [llength $values]} {incr index} {
     set rowValue [lindex $values $index]
     for {set col 0} {$col < [llength $column]} {incr col} {
         puts [format "%*s:%*s" -30 [lindex $column $col] -10 [lindex $rowValue \
              $col]]
     }
     puts "\n"
}
puts "***************************************************"

set values [ixNet getAttribute $domainDb -values]
set column [ixNet getAttribute $domainDb -columns]
puts "***************************************************"
puts "****  MSRP Talker Domain database learned info ****"
for {set index 0} {$index < [llength $values]} {incr index} {
     set rowValue [lindex $values $index]
     for {set col 0} {$col < [llength $column]} {incr col} {
         puts [format "%*s:%*s" -30 [lindex $column $col] -10 [lindex $rowValue \
              $col]]
     }
     puts "\n"
}
puts "***************************************************"

set values [ixNet getAttribute $vlanDb -values]
set column [ixNet getAttribute $vlanDb -columns]
puts "***************************************************"
puts "*****  MSRP Talker VLAN database learned info *****"
for {set index 0} {$index < [llength $values]} {incr index} {
     set rowValue [lindex $values $index]
     for {set col 0} {$col < [llength $column]} {incr col} {
         puts [format "%*s:%*s" -30 [lindex $column $col] -10 [lindex $rowValue \
              $col]]
     }
     puts "\n"
}
puts "***************************************************"
puts "\n"

puts "Fetching MSRP Listener Learned Info for listener 1"
ixNet exec getListenerDatabases $listener1 1
after 5000
set linfo [ixNet getList $listener1 learnedInfo]
set streamDb [lindex $linfo 0]
set domainDb [lindex $linfo 1]
set vlanDb   [lindex $linfo 2]

set values [ixNet getAttribute $streamDb -values]
set column [ixNet getAttribute $streamDb -columns]
puts "***************************************************"
puts "*** MSRP Listener stream database learned info ****"
for {set index 0} {$index < [llength $values]} {incr index} {
     set rowValue [lindex $values $index]
     for {set col 0} {$col < [llength $column]} {incr col} {
         puts [format "%*s:%*s" -30 [lindex $column $col] -10 [lindex $rowValue \
              $col]]
     }
     puts "\n"
}
puts "***************************************************"

set values [ixNet getAttribute $domainDb -values]
set column [ixNet getAttribute $domainDb -columns]
puts "***************************************************"
puts "*** MSRP Listener Domain database learned info ****"
for {set index 0} {$index < [llength $values]} {incr index} {
     set rowValue [lindex $values $index]
     for {set col 0} {$col < [llength $column]} {incr col} {
         puts [format "%*s:%*s" -30 [lindex $column $col] -10 [lindex $rowValue \
              $col]]
     }
     puts "\n"
}
puts "***************************************************"

set values [ixNet getAttribute $vlanDb -values]
set column [ixNet getAttribute $vlanDb -columns]
puts "***************************************************"
puts "**** MSRP Listener VLAN database learned info *****"
for {set index 0} {$index < [llength $values]} {incr index} {
     set rowValue [lindex $values $index]
     for {set col 0} {$col < [llength $column]} {incr col} {
         puts [format "%*s:%*s" -30 [lindex $column $col] -10 [lindex $rowValue \
              $col]]
     }
     puts "\n"
}
puts "***************************************************"

################################################################################
# 5. Disable streams and apply changes On The Fly (OTF). Enable again.
################################################################################
puts "Deactivating the streams"
set streams [ixNet getList $mac1 streams]
set multiValue [ixNet getAttr $streams -active]
ixNet setAttribute $multiValue/singleValue -value false
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
puts "Applying changes on the fly"
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
after 5000

puts "Activating the streams"
ixNet setAttribute $multiValue/singleValue -value true
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
puts "Applying changes on the fly"
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
after 5000

################################################################################
# 7. Configure L2-L3 traffic 
################################################################################
puts "Congfiguring L2-L3 Traffic Item"
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {avb_traffic}           \
    -roundRobinPacketOrdering false  \
    -trafficType avb1722
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set mcastDestination \
    [list [list false none 22:22:22:22:22:22:00:01 00:00:00:00:00:00:00:00 1] \
    [list false none 22:22:22:22:22:22:00:02 00:00:00:00:00:00:00:00 1]]
set mcastReceiver \
    [list [list $listener1/subscribedStreams 0 0 0] \
          [list $listener1/subscribedStreams 0 0 1] \
          [list $listener1/subscribedStreams 0 1 0] \
          [list $listener1/subscribedStreams 0 1 1]]

ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"\
    -multicastDestinations $mcastDestination\
    -scalableSources       [list]\
    -multicastReceivers    $mcastReceiver\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               [list]\
    -destinations          [list]\    
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy [list trackingenabled0 avbStreamName0]
ixNet commit

###############################################################################
# 9. Apply and start L2/L3 traffic
###############################################################################
puts "applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "starting L2/L3 traffic"
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
# 14. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 15. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
