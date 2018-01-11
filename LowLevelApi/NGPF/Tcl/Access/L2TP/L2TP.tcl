#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2013 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    21/06/2013 - Vlad Mihai - created sample                      	       #
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
#   This script intends to demonstrate how to configure L2TP in a back 	       #
#   to back scenario.							       #
#   It configures one topology with one Device Group with LAC and PPP client   #
#   chained behind it							       # 
#   and another with LNS and PPP server on top of it.      		       #
# Module:                                                                      #
#    The sample was tested on an XM4S module.                          	       #
# Software:                                                                    #
#    IxOS      6.50 EA                                                         #
#    IxNetwork 7.11 EA                                                         #
#                                                                              #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer localhost
    set ixTclPort   8009
    set ports       {{10.205.15.62 8 3} {10.205.15.62 8 4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.11

puts "Creating a new config"
ixNet exec newConfig

puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 [lindex $vPorts 0]
set vport2 [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

puts "Rebooting the ports"
foreach vp $vPorts {lappend jobs [ixNet -async exec resetPortCpuAndFactoryDefault $vp]}
foreach j $jobs {ixNet isSuccess $j}

after 5000

puts "Add 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vport1
ixNet add [ixNet getRoot] topology -vports $vport2
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

puts "In each topology, add one Device Group and set the multiplier."
ixNet add $topo1 deviceGroup -multiplier 1
ixNet add $topo2 deviceGroup -multiplier 3
ixNet commit

set topo1_DG1 [ixNet getList $topo1 deviceGroup]
set topo2_DG1 [ixNet getList $topo2 deviceGroup]

puts "Add a chained Device Group behind the previously added Device Groups and set the multiplier to 2."
ixNet add $topo1_DG1 deviceGroup -multiplier 10
ixNet commit

set topo1_chained_DG2 [ixNet getList $topo1_DG1 deviceGroup]

puts "Add ethernet/mac stack layer in each Device Group."
ixNet add $topo1_DG1 ethernet
ixNet add $topo2_DG1 ethernet
ixNet add $topo1_chained_DG2 ethernet
ixNet commit

set eth1 [ixNet getList $topo1_DG1 ethernet]
set eth2 [ixNet getList $topo2_DG1 ethernet]
set eth3 [ixNet getList $topo1_chained_DG2 ethernet]

puts "Create the LAC/LNS stacks"
puts "First we need to add IP layer because LAC/LNS are stacked on it."
ixNet add $eth1 ipv4
ixNet add $eth2 ipv4
ixNet commit

set ip1 [ixNet getList $eth1 ipv4]
set ip2 [ixNet getList $eth2 ipv4]

puts "Add LAC/LNS on top of IPv4 stack."
ixNet add $ip1 lac
ixNet add $ip2 lns
ixNet commit

set lac_DG1 [ixNet getList $ip1 lac]
set lns_DG2 [ixNet getList $ip2 lns]

puts "Create the PPP Client stack in the chained Device Group."
ixNet add $eth3 pppoxclient
ixNet commit

set pppC [ixNet getList $eth3 pppoxclient]

puts "Create the PPP Server stack in the LNS Device Group."
ixNet add $lns_DG2 pppoxserver
ixNet commit

set pppS [ixNet getList $lns_DG2 pppoxserver]


puts "Change the custom ratio between the IPv4 and LAC layer to 3."
ixNet setAttribute $lac_DG1 -multiplier 3
ixNet commit

puts "Set the IP addresses for LAC/LNS"
ixNet setMultiAttribute [ixNet getA $ip1 -address]/counter -direction increment -start 10.1.0.1 -step 0.0.0.1
ixNet setMultiAttribute [ixNet getA $ip2 -address]/counter -direction increment -start 10.1.0.100 -step 0.0.0.1
ixNet commit

puts "Set the LNS Destination IP addresse for LAC"
ixNet setMultiAttribute [ixNet getA $lac_DG1 -baseLnsIp]/counter -direction increment -start 10.1.0.100 -step 0.0.0.1

puts "Set the number of PPP session on the Server"
ixNet setA $pppS -sessionsCount 10
ixNet commit

puts "Wait 5 sec"
after 5000

puts "Starting the PPP stacks."
ixNet exec start $pppS
after 2000
ixNet exec start $pppC

puts "Wait 2 minutes"
after 120000

puts "Printing learned info for PPP Client"
foreach add [ixNet getA $pppC -discoveredIpv4Addresses] {
	puts $add
}
puts ""


puts "Stopping the clients"
ixNet exec stop $topo1
after 5000
puts "Stopping the servers"
ixNet exec stop $topo2
after 10000


puts "Unassigning ports..."
ixTclNet::UnassignPorts
puts "Done... Ports are unassigned..."
puts ""

puts "Cleaning up IxNetwork..."
ixNet exec newConfig
ixNet disconnect

puts "Done... IxNetwork session is closed..."
puts ""
puts "!!! TEST DONE !!!"

return 0