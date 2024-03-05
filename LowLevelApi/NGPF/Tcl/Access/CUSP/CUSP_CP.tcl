#!/usr/bin/tclsh
################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by Keysight                                         #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################


################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Keysight  and have#
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Keysight  and/or by the user and/or by a third party)] shall at all  #
# times remain the property of Keysight.                                       #
#                                                                              #
# Keysight  does not warrant (i) that the functions contained in the script    #
# will meet the users requirements or (ii) that the script will be without     #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND Keysight     #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL KEYSIGHT BE LIABLE FOR ANY DAMAGES RESULTING FROM OR       #
# ARISING OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART     #
# THEREOF INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR  #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF Keysight HAS BEEN ADVISED OF THE POSSIBILITY OF#
# SUCH DAMAGES IN ADVANCE.                                                     #
# Keysight  will not be required to provide any software maintenance or support#
# s.ervices of any kind (e.g. any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Keysight  may#
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Keysight  to      #
# provide any additional maintenance or support services.                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF CUSP APIs.             #
#                                                                              #
#    1. It will create 2 topologies. CUSP CP with PPPoX Server is configured   #
#       in one topology & CUSP UP with PPPoX Subscribers are configured in     #
#       another topology.                                                      # 
#    2. Start all protocol.                                                    #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. OTF change PPP Subscriber Profile attribute                            #
#    6. Stop all protocols.                                                    #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.43.12
    set ixTclPort   8114
    set ports       {{10.39.50.200 1 1} { 10.39.50.200 1 2}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 9.20 \
-setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

# ###############################################################################
# 1. Configure CUSP CP & UP
# ############################################################################### 
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
ixNet setAttr $mvGw1/singleValue  -value "20.20.20.1"
ixNet setAttr $mvGw2/singleValue  -value "20.20.20.2"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

# Add CUSP CP and CUSP UP
puts "Adding CUSP CP over IP4 stacks"
ixNet add $ip1 cuspCP
ixNet add $ip2 cuspUP
ixNet commit

set cp [ixNet getList $ip1 cuspCP]
set up [ixNet getList $ip2 cuspUP]

# Add VXLAN GPE
puts "Adding VXLAN GPE over IP4 stacks"
ixNet add $ip1 vxlangpe
ixNet add $ip2 vxlangpe
ixNet commit

set vxlangpe2 [ixNet getList $ip2 vxlangpe]

# Add UP Group Info on CUSP CP
ixNet add $cp upGroupInfo
ixNet commit

set upGroupInfo [ixNet getList $cp upGroupInfo]

# Rename topologies and devices
puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "CP with PPPoE Server"
ixNet setAttr $topo2  -name "UP with PPPoE Subscribers"

ixNet setAttr $t1dev1 -name "CUSP CP"
ixNet setAttr $t2dev1 -name "CUSP UP"
ixNet commit

# Configure UP Group Info
puts "Configuring UP Group Info"
ixNet setAttr [ixNet getAttr $upGroupInfo -iPv4Address]/singleValue -value 20.20.20.1
ixNet setAttr [ixNet getAttr $upGroupInfo -vxlanIPv4Address]/singleValue -value 20.20.20.1
ixNet setAttr [ixNet getAttr $upGroupInfo -cpVxlanIPv4Address]/singleValue -value 20.20.20.2
ixNet setAttr $upGroupInfo -numberOfPppoeUsers 1
ixNet commit

# Configure UP and VxLAN GPE
ixNet setAttr [ixNet getAttr $up -cpIpv4Address]/singleValue -value 20.20.20.2
ixNet setAttr [ixNet getAttr $vxlangpe2 -vni]/singleValue -value 1000
ixNet setAttr [ixNet getAttr $vxlangpe2 -ipv4_multicast]/singleValue -value 225.0.1.1
ixNet commit

# Add PPPoX Server behind CP 
puts "Adding PPPoX Server behind CP"
ixNet add $t1dev1 deviceGroup
ixNet commit

set t1dev2 [lindex [ixNet getList $t1dev1 deviceGroup] 0]
ixNet add $t1dev2 ethernet
ixNet commit

set mac11 [ixNet getList $t1dev2 ethernet]
set pppServer [ixNet add $mac11 pppoxserver]
ixNet commit

# Add PPPoX Client beind UP
puts "Adding PPPoX Client behind UP"
ixNet add $t2dev1 deviceGroup
ixNet commit

set t2dev2 [lindex [ixNet getList $t2dev1 deviceGroup] 0]
ixNet add $t2dev2 ethernet
ixNet commit

set mac22 [ixNet getList $t2dev2 ethernet]
set pppClient [ixNet add $mac22 pppoxclient]
ixNet commit

ixNet setAttr $t1dev2 -multiplier 1
ixNet setAttr $t2dev2 -multiplier 1
ixNet commit

# ###############################################################################
# 2. Start protocols
# ###############################################################################
puts "Starting protocols and waiting for 45 seconds for protocols to come up"
ixNet exec start $t1dev1
after 10000

ixNet exec start $t2dev1
after 10000

ixNet exec start $t1dev2
after 10000

ixNet exec start $t2dev2
after 15000

# ###############################################################################
# 3. Retrieve protocol statistics.
# ###############################################################################
puts "Fetching CUSP CP Per Port Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"CUSP CP Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index] -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

# ##############################################################################
# 4. Retrieve protocol learned info
# ##############################################################################

puts "Fetching PPP Subscriber  Learned Info"
ixNet exec getPppSubscriberInfo $upGroupInfo 1 

after 5000
set learnedInfoList [ixNet getList $upGroupInfo learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]

puts "PPP Subscriber learned info"
puts "***************************************************"
foreach table $linfoList {
    puts "***************************************************"
    set column [ixNet getAttr $table -columns]
    puts "$column"
    set values [ixNet getAttr $table -values]
    puts "$values\n"
    puts "***************************************************"
}
puts "***************************************************"

# ###############################################################################
# 5. Change PPP Subscriber Profile attributes on the fly
# ###############################################################################
puts "Changing PPP Subscriber Profile attributes on the fly ..."
set pppoEUsersList $upGroupInfo/pppoEUsersList
ixNet setAttr [ixNet getAttr $pppoEUsersList -cost]/singleValue -value 55
ixNet commit

ixNet exec applyOnTheFly [ixNet getRoot]/globals/topology

# ###############################################################################
# 6. Stop all protocols
# ###############################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
