#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    04/10/2015 - Sayantan Pramanick - created sample                          #
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
#    This script intends to demonstrate how to use NGPF TRILL APIs             #
#                                                                              #
#    1. It will create one TRILL RBridge per topology in two ports. Behind     #
#       RBridge it will add FAT Tree network topology. Behind network topology #
#       it will add TRILL simulated edge RBRidge. Behind simulated edge, it    #
#       will add MAC pool which will serve as endpoints in traffic.            #
#    2. Start all protocols.                                                   #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Chnage some fields and apply change on the fly                         #
#    6. Configure L2-L3 traffic.                                               #
#    7. Start the L2-L3 traffic.                                               #
#    8. Retrieve L2-L3 traffic stats.                                          #
#    9. Stop L2-L3 traffic.                                                    #
#   10. Stop all protocols.                                                    #
#                                                                              #
# Ixia Softwares:                                                              #
#    IxOS      6.90 EB (6.90.0.240)                                            #
#    IxNetwork 7.50 EB (7.50.0.160)                                            #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.25.88
    set ixTclPort   8009
    set ports       {{10.205.27.69 1 1} { 10.205.27.69 1 2}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Configuration of protocols as per above mentioned flow.
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
after 10000
puts "Adding 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet add [ixNet getRoot] topology -vports $vportRx
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "Topology 1 for TRILL"
ixNet setAttr $topo2  -name "Topology 2 for TRILL"

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

puts "Adding TRILL interfaces"
ixNet add $mac1 isisTrill
ixNet add $mac2 isisTrill
ixNet commit

set trillIf1 [ixNet getList $mac1 isisTrill]
set trillIf2 [ixNet getList $mac2 isisTrill]

puts "Setting discard LSP off in TRILL Routers"
set trillRouter1 [ixNet getList $t1dev1 isisTrillRouter]
set trillRouter2 [ixNet getList $t2dev1 isisTrillRouter]
set mv1 [ixNet getAttribute $trillRouter1 -discardLSPs]
set mv2 [ixNet getAttribute $trillRouter2 -discardLSPs]
ixNet setAttribute $mv1 -pattern singleValue
ixNet setAttribute $mv2 -pattern singleValue
ixNet commit

ixNet setAttribute $mv1/singleValue -value false
ixNet setAttribute $mv2/singleValue -value false
ixNet commit

puts "Setting Mulitcast IPv4 group in TRILL Router 2"
ixNet setAttribute $trillRouter2 -trillMCastIpv4GroupCount 1
ixNet commit

set trillMcastIpv4GroupList [ixNet getList $trillRouter2 trillMCastIpv4GroupList]
set mvMcastAddrCount [ixNet getAttribute $trillMcastIpv4GroupList -mcastAddrCnt]
set mvStartMcastAddr [ixNet getAttribute $trillMcastIpv4GroupList -startMcastAddr]

ixNet setAttribute $mvMcastAddrCount -pattern singleValue
ixNet setAttribute $mvMcastAddrCount/singleValue -value 2
ixNet setAttribute $mvStartMcastAddr -pattern singleValue
ixNet setAttribute $mvStartMcastAddr/singleValue -value "230.0.0.1"
ixNet commit

puts "Setting Multicast MAC Groups in TRILL Router 2"
ixNet setAttribute $trillRouter2 -trillMCastMacGroupCount 1
ixNet commit

set trillMCastMacGroupList [ixNet getList $trillRouter2 trillMCastMacGroupList]

set mvMcastAddrCount [ixNet getAttribute $trillMCastMacGroupList -mcastAddrCnt]
set mvStartMcastAddr [ixNet getAttribute $trillMCastMacGroupList -startMcastAddr]

ixNet setAttribute $mvMcastAddrCount -pattern singleValue
ixNet setAttribute $mvMcastAddrCount/singleValue -value 2
ixNet setAttribute $mvStartMcastAddr -pattern singleValue
ixNet setAttribute $mvStartMcastAddr/singleValue -value "01:55:55:55:55:55"
ixNet commit

puts "Setting Mulitcast IPv6 group in TRILL Router 2"
ixNet setAttribute $trillRouter2 -trillMCastIpv6GroupCount 1
ixNet commit

set trillMcastIpv6GroupList [ixNet getList $trillRouter2 trillMCastIpv6GroupList]
set mvMcastAddrCount [ixNet getAttribute $trillMcastIpv6GroupList -mcastAddrCnt]
set mvStartMcastAddr [ixNet getAttribute $trillMcastIpv6GroupList -startMcastAddr]

ixNet setAttribute $mvMcastAddrCount -pattern singleValue
ixNet setAttribute $mvMcastAddrCount/singleValue -value 2
ixNet setAttribute $mvStartMcastAddr -pattern singleValue
ixNet setAttribute $mvStartMcastAddr/singleValue -value "ff03::1111"
ixNet commit

puts "Adding network group with FAT tree topology"
ixNet add $t1dev1 networkGroup
ixNet add $t2dev1 networkGroup
ixNet commit

set netGroup1 [lindex [ixNet getList $t1dev1 networkGroup] 0]
set netGroup2 [lindex [ixNet getList $t2dev1 networkGroup] 0]

ixNet add $netGroup1 networkTopology
ixNet add $netGroup2 networkTopology
ixNet commit

set netTopo1 [lindex [ixNet getList $netGroup1 networkTopology] 0]
set netTopo2 [lindex [ixNet getList $netGroup2 networkTopology] 0]

ixNet add $netTopo1 netTopologyFatTree
ixNet add $netTopo2 netTopologyFatTree
ixNet commit

puts "Adding device group behind network group"
ixNet add $netGroup1 deviceGroup
ixNet add $netGroup2 deviceGroup
ixNet commit

set t1dev2 [lindex [ixNet getList $netGroup1 deviceGroup] 0]
set t2dev2 [lindex [ixNet getList $netGroup2 deviceGroup] 0]

puts "Adding ethernet"
ixNet add $t1dev2 ethernet
ixNet add $t2dev2 ethernet
ixNet commit

set mac3 [ixNet getList $t1dev2 ethernet]
set mac4 [ixNet getList $t2dev2 ethernet]

puts "Adding TRILL Simulated Egde"
ixNet add $mac3 isisTrillSimRouter
ixNet add $mac4 isisTrillSimRouter
ixNet commit

puts "Adding MAC Pools behind TRILL Simulated Edge Device"
ixNet add $t1dev2 networkGroup
ixNet add $t2dev2 networkGroup
ixNet commit

set netGroup3 [lindex [ixNet getList $t1dev2 networkGroup] 0]
set netGroup4 [lindex [ixNet getList $t2dev2 networkGroup] 0]
ixNet add $netGroup3 macPools
ixNet add $netGroup4 macPools
ixNet commit

set macPool1 [lindex [ixNet getList $netGroup3 macPools] 0]
set macPool2 [lindex [ixNet getList $netGroup4 macPools] 0]

set mvMac1 [ixNet getAttribute $macPool1 -mac]
set mvMac2 [ixNet getAttribute $macPool2 -mac]

ixNet setAttribute $mvMac1 -pattern counter 
ixNet setAttribute $mvMac2 -pattern counter 
ixNet commit

set mvCounter1 [ixNet getList $mvMac1 counter]
set mvCounter2 [ixNet getList $mvMac2 counter]

ixNet setMultiAttribute $mvCounter1 -step 00:00:00:00:00:01 -start 22:22:22:22:22:22 -direction increment
ixNet setMultiAttribute $mvCounter2 -step 00:00:00:00:00:01 -start 44:44:44:44:44:44 -direction increment
ixNet commit

puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000

################################################################################
# 2. Retrieve protocol statistics.
################################################################################
puts "Fetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"TRILL RTR Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -34 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

###############################################################################
# 3. Retrieve protocol learned info
###############################################################################
puts "Fetching TRILL Learned Info"
ixNet exec getLearnedInfo $trillIf1 1
after 5000
set linfo1 [ixNet getList $trillIf1 learnedInfo]
ixNet getAttr $linfo1 -columns
set values [ixNet getAttribute $linfo1 -values]

set linfoTables [ixNet getList $linfo1 table]
set table1 [lindex $linfoTables 0]
set table2 [lindex $linfoTables 1]
set table3 [lindex $linfoTables 2]
set table4 [lindex $linfoTables 3]
set table5 [lindex $linfoTables 4]
set table6 [lindex $linfoTables 5]

set values [ixNet getAttribute $table1 -values]
set column [ixNet getAttribute $table1 -columns]
puts "***************************************************"
for {set index 0} {$index < [llength $values]} {incr index} {
     set rowValue [lindex $values $index]
     for {set col 0} {$col < [llength $column]} {incr col} {
         puts [format "%*s:%*s" -30 [lindex $column $col] -10 [lindex $rowValue \
              $col]]
     }
     puts "\n"
}
puts "***************************************************"

set values [ixNet getAttribute $table2 -values]
set column [ixNet getAttribute $table2 -columns]
puts "***************************************************"
for {set index 0} {$index < [llength $values]} {incr index} {
     set rowValue [lindex $values $index]
     for {set col 0} {$col < [llength $column]} {incr col} {
         puts [format "%*s:%*s" -30 [lindex $column $col] -10 [lindex $rowValue \
              $col]]
     }
     puts "\n"
}
puts "***************************************************"
 
set values [ixNet getAttribute $table3 -values]
set column [ixNet getAttribute $table3 -columns]
puts "***************************************************"
for {set index 0} {$index < [llength $values]} {incr index} {
     set rowValue [lindex $values $index]
     for {set col 0} {$col < [llength $column]} {incr col} {
         puts [format "%*s:%*s" -30 [lindex $column $col] -10 [lindex $rowValue \
              $col]]
     }
     puts "\n"
}
puts "***************************************************"

set values [ixNet getAttribute $table4 -values]
set column [ixNet getAttribute $table4 -columns]
puts "***************************************************"
for {set index 0} {$index < [llength $values]} {incr index} {
     set rowValue [lindex $values $index]
     for {set col 0} {$col < [llength $column]} {incr col} {
         puts [format "%*s:%*s" -30 [lindex $column $col] -10 [lindex $rowValue \
              $col]]
     }
     puts "\n"
}
puts "***************************************************"

set values [ixNet getAttribute $table5 -values]
set column [ixNet getAttribute $table5 -columns]
puts "***************************************************"
for {set index 0} {$index < [llength $values]} {incr index} {
     set rowValue [lindex $values $index]
     for {set col 0} {$col < [llength $column]} {incr col} {
         puts [format "%*s:%*s" -30 [lindex $column $col] -10 [lindex $rowValue \
              $col]]
     }
     puts "\n"
}
puts "***************************************************"

set values [ixNet getAttribute $table6 -values]
set column [ixNet getAttribute $table6 -columns]
puts "***************************************************"
for {set index 0} {$index < [llength $values]} {incr index} {
     set rowValue [lindex $values $index]
     for {set col 0} {$col < [llength $column]} {incr col} {
         puts [format "%*s:%*s" -30 [lindex $column $col] -10 [lindex $rowValue \
              $col]]
     }
     puts "\n"
}
puts "***************************************************"

###############################################################################
# 4. Apply on the fly
###############################################################################
set trillMCastMacGroupList [ixNet getList $trillRouter2 trillMCastMacGroupList]
set mvMcastAddrCount [ixNet getAttribute $trillMCastMacGroupList -mcastAddrCnt]

ixNet setAttribute $mvMcastAddrCount -pattern singleValue
ixNet setAttribute $mvMcastAddrCount/singleValue -value 10
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
# 5. Configure L2-L3 traffic 
################################################################################
puts "Congfiguring L2-L3 Traffic Item"
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {Traffic Item 1}           \
    -roundRobinPacketOrdering false  \
    -trafficType ethernetVlan        \
	-biDirectional 1
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source [list $netGroup3]
set destination [list $netGroup4]

ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"\
    -multicastDestinations [list]\
    -scalableSources       [list]\
    -multicastReceivers    [list]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source\
    -destinations          $destination  
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy        [list sourceDestEndpointPair0 trackingenabled0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]
ixNet commit

###############################################################################
# 6. Apply and start L2/L3 traffic
###############################################################################
puts "applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic


###############################################################################
# 7. Retrieve L2/L3 traffic item statistics
###############################################################################
puts "Verifying all the L2-L3 traffic stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Flow Statistics"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -34 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

################################################################################
# 8. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 9. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
