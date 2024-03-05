#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    06/27/2020 - Rupkatha Guha - created sample                               #
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
#    This script intends to demonstrate how to configure ESMC.                 #
#    using TCL. Users are expected to run this against an external DUT.        #
#                                                                              #
# About Topology:                                                              #
#                                                                              #
#     On the port, configure a ESMC topology which sends DNU on receiving a    #
#     better Quality ESMC PDU. Run the protocol and check stats.               #
#                                                                              #
# Script Flow:                                                                 #
#    1. Configuration of protocols as described in topology.                   #
#    2. Start the ESMC protocol.                                               #
#    3. Retrieve protocol statistics.                                          #
#    4. Stop all protocols.                                                    #
#                                                                              #                                                                                
# Ixia Software:                                                               #
#    IxOS      9.10 EB                                                         #
#    IxNetwork 9.10 EB                                                         #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.50.134
    set ixTclPort   8779
    set ports       {{10.39.50.126 1 3}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 9.10\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure ESMC as per the description
#    give above
################################################################################ 
puts "Adding 1 vport"
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]


puts "Assigning the port"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force
after 10000
puts "Adding 1 topology"
ixNet add [ixNet getRoot] topology -vports $vportTx

ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]

puts "Adding a device group"
ixNet add $topo1 deviceGroup

ixNet commit

set t1devices [ixNet getList $topo1 deviceGroup]


set t1dev1 [lindex $t1devices 0]

puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $t1dev1 -multiplier 1

ixNet commit

puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet

ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]


puts "Configuring the mac addresses"
ixNet setMultiAttr [ixNet getAttr $mac1 -mac]/counter\
        -direction  increment                        \
        -start      {00:11:01:00:00:01}              \
        -step       {00:00:00:00:00:01}


ixNet commit

puts "Add esmc"
ixNet add $mac1 esmc

ixNet commit

set esmc1 [ixNet getList $mac1 esmc]
ixNet commit


puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "ESMC Topology"

ixNet commit


puts "Setting Quality Level to PRTC option2"

ixNet setAttr [ixNet getAttr $esmc1 -qualityLevel]/singleValue -value ql_eprtc_op2

puts "Configuring Transmission Rate to 2"

ixNet setAttr [ixNet getAttr $esmc1 -transmissionRate]/singleValue -value 2
ixNet commit

puts "Enabling send DNU if better QL Received"

ixNet setAttr [ixNet getAttr $esmc1 -sendDnuIfBetterQlReceived]/singleValue -value true
ixNet commit


################################################################################
# 2. Start ESMC protocol and wait for 30 seconds
################################################################################
puts "Starting protocols and waiting for 30 seconds for protocols to come up"
ixNet exec startAllProtocols
after 30000

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
puts "Fetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"ESMC Per Port"/page}
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
# 4. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
