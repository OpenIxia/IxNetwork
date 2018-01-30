#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    5/09/2014 - Irina Popa - created sample                         #
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
#   This script intends to demonstrate how to configure VxLAN with DHCPv6      #
#   Client and DHCPv6 Server. It configures one topology with one Device Group # 
#   with VxLAN and a chained Device Group with the DHCPv6 Client stack         #
#   and a corresponding topology containing one Device Group with VxLAN and a  #
#   chained Device Group with DHCPv6 Server stack.                             #
# Module:                                                                      #
#    The sample was tested on an XMVAE module.                          #
# Software:                                                                    #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer localhost
    set ixTclPort   8009
    set ports       {{10.205.15.90 1 1} {10.205.15.90 1 2}}
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

# Rebooting the ports
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

puts "In each topology, add one Device Group and set the multiplier to 1."
ixNet add $topo1 deviceGroup -multiplier 1
ixNet add $topo2 deviceGroup -multiplier 1
ixNet commit

set topo1_DG1 [ixNet getList $topo1 deviceGroup]
set topo2_DG1 [ixNet getList $topo2 deviceGroup]


puts "Add ethernet/mac stack layer in each Device Group."
ixNet add $topo1_DG1 ethernet
ixNet add $topo2_DG1 ethernet
ixNet commit

set eth1 [ixNet getList $topo1_DG1 ethernet]
set eth2 [ixNet getList $topo2_DG1 ethernet]


puts "Create the PTP layer."
ixNet add $eth1 ptp
ixNet add $eth2 ptp
ixNet commit

set ptp1 [ixNet getList $eth1 ptp]
set ptp2 [ixNet getList $eth2 ptp]



puts "Set the 802.1AS profile on both DGs"
ixNet setMultiAttribute [ixNet getA $ptp1 -profile]/singleValue -value ieee8021as
ixNet setMultiAttribute [ixNet getA $ptp2 -profile]/singleValue -value ieee8021as
ixNet commit

puts "Set Delay Mechanism Peer Delay on both DGs"
ixNet setMultiAttribute [ixNet getA $ptp1 -delayMechanism]/singleValue -value peerdelay
ixNet setMultiAttribute [ixNet getA $ptp2 -delayMechanism]/singleValue -value peerdelay
ixNet commit

puts "Set Step Mode on both DGs"
ixNet setMultiAttribute [ixNet getA $ptp1 -stepMode]/singleValue -value twostep
ixNet setMultiAttribute [ixNet getA $ptp2 -stepMode]/singleValue -value twostep
ixNet commit

puts "Set Role on the Master DG"
ixNet setMultiAttribute [ixNet getA $ptp1 -role]/singleValue -value master
ixNet commit
puts "Wait 5 sec"
after 5000

puts "Starting the PTP DGs."
ixNet exec start $topo1_DG1
ixNet exec start $topo2_DG1
puts "Wait 5 sec"
after 5000

puts "Send Signalling messages from gPTP slave using 'ixNet execute gPtpSendSignaling $ptp2 {enumOpt-DoNotChange} {enumOpt-DoNotChange} {enumOpt-V2_1_per_4_seconds_} {false} {false}' command "
#ixNet help $ptp2
ixNet execute gPtpSendSignaling $ptp2 {enumOpt-DoNotChange} {enumOpt-DoNotChange} {enumOpt-V2_1_per_4_seconds_} {false} {false}

puts "Stopping the slave"
ixNet exec stop $topo1_DG1
after 5000
puts "Stopping the master"
ixNet exec stop $topo2_DG1
after 1000


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