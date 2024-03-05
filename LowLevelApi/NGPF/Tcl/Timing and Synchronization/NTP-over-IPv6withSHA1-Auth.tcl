#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    06/13/2017 - Ashis Nandy - created sample                                 #
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
#    This script intends to demonstrate how to configure NTP client over IPv6  #
#    using python. Users are expected to run this against an external NTP      #
#    Server and assign the Server IP address accordingly.                      #
#                                                                              #
# About Topology:                                                              #
#                                                                              #
#     On the port, configure an NTP client over IPv6 with SHA1 authentication  #
#     poll interval as 4. Provide the server IP address as the one in the      #
#     Server and run the protocol. 					                           #
#                                                                              #
# Script Flow:                                                                 #
#    1. Configuration of protocols as described in topology.                   #
#    2. Connect it to an External server and Provide the server IP accordingly #
#    3. Start the NTP protocol.                                                #
#    4. Retrieve protocol statistics.                                          #
#    5. Deactivate the NTP client and  apply change on the fly                 #
#    6. Retrieve protocol protocol stat  again.                                #
#    7. Stop all protocols.                                                    #
#                                                                              #                                                                                
# Ixia Software:                                                               #
#    IxOS      8.50 EB                                                         #
#    IxNetwork 8.50 EB                                                         #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.50.128
    set ixTclPort   8500
    set ports       {{10.39.50.120 7 11}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.30\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure MPLSOAM as per the description
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



puts "Add ipv6"
ixNet add $mac1 ipv6

ixNet commit

set ip1 [ixNet getList $mac1 ipv6]


set mvAdd1 [ixNet getAttr $ip1 -address]

set mvGw1  [ixNet getAttr $ip1 -gatewayIp]


puts "configuring ipv4 addresses"
ixNet setAttr $mvAdd1/singleValue -value "2000::1"

ixNet setAttr $mvGw1/singleValue  -value "2000::64"


ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 64


ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true

ixNet commit



puts "Adding NTP over IPv6 stack"
ixNet add $ip1 ntpclock

ixNet commit

set ntpclient [ixNet getList $ip1 ntpclock]


ixNet commit

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "NTP Client Topology"


ixNet setAttr $t1dev1 -name "NTP Client"
ixNet commit


puts "Setting Authnetication mode to SHA1"
set ntp_server1 [lindex [ixNet getList $ntpclient ntpServers] 0]
ixNet setAttr [ixNet getAttr $ntp_server1 -authentication]/singleValue -value sha1



puts "Configuring Server IP address in NTP servers"
set networkAddress1 [ixNet getAttribute $ntp_server1 -serverIPv6Address]
ixNet setMultiAttribute $networkAddress1\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet1 [ixNet add $networkAddress1 "counter"]
ixNet setMultiAttribute $addressSet1\
    -step  ::0.0.0.1\
    -start 2000::64\
    -direction increment
ixNet commit


puts "Configuring Min poll interval to 4 in the NTP server"

ixNet setAttr [ixNet getAttr $ntp_server1 -minPollInterval]/singleValue -value 4
ixNet commit


################################################################################
# 2. Start NTP protocol and wait for 30 seconds
################################################################################
puts "Starting protocols and waiting for 30 seconds for protocols to come up"
ixNet exec startAllProtocols
after 30000

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
puts "Fetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"NTP Per Port"/page}
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
# 5. Deactivate an NTP client (OTF).
################################################################################
puts "Deactivating the NTP client"
set root [ixNet getRoot]
set active_1 [ixNet getAttribute $ntpclient -active]
set ntp_active1_s $active_1/singleValue
ixNet setMulA $ntp_active1_s  -value false
ixNet commit
if {[catch {ixNet exec applyOnTheFly $root/globals/topology}]} {
        puts "Could not apply changes on the fly: $::errorInfo"
        return $FAILED
}
after 30000

################################################################################
# 3. Retrieve protocol statistics after deactivating the client
################################################################################
puts "Fetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"NTP Per Port"/page}
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
# 5. Activate an NTP client (OTF).
################################################################################
puts "activating the NTP client"
set  active_1 [ixNet getAttribute $ntpclient -active]
set ntp_active1_s $active_1/singleValue
ixNet setMulA $ntp_active1_s  -value true
ixNet commit
if {[catch {ixNet exec applyOnTheFly $root/globals/topology}]} {
        puts "Could not apply changes on the fly: $::errorInfo"
        return $FAILED
}
after 30000

################################################################################
# 3. Retrieve protocol statistics after activating the client
################################################################################
puts "Fetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"NTP Per Port"/page}
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
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
