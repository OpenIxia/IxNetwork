#!/usr/bin/tclsh
################################################################################
#                                                                              #
#    Copyright 1997 - 2021 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
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

#################################################################################
#                                                                               #
# Description:                                                                  #
#    This script intends to demonstrate how to use NGPF gRIBI API to configure  #
#    gRIBI client topology.                                                     #
#                                                                               #
#    About Topology:                                                            #
#       Within topology gRIBI Client is configured in one port. Other port will #
#    be connected to gRIBI server. gRIBI Client is emulated in the Device Group #
#    which consists of 1 gRPC channel, 1 gRIBI clinet, 2 Next-Hop Group and 3   #
#    next hops per next hop group.                                              #
#      The Network Group consists of gRIBI IPv4 entries which will be advertised#
#    by gRIBI client.                                                           #
#                                                                               #
# Script Flow:                                                                  #
#    Configuration flow of the script is as follows:                            #
#    Step 1. Configuration of protocols.                                        #
#          i.   Adding of gRIBI client topology.                                #
#          ii.  Adding of Network Topology.                                     #
#          iii. Configuring some default paramaters.                            #
#          iv.  Add IPv4 topology in other port. gRIBI Server will run behind   #
#                this port.                                                     #
#          Note: IxNetwork 9.20 EA does not support gRIBI server yet. User can  #
#               connect a real server connected to emualted gRIBI cliente.      #
#               We are running a demo server in the gRIBI server port using some#
#               cli commands. For example purpose the command to run demo server#
#               is provided in sample script, but it will not run the commands. #
#               so gRIBI client sessions will not be up unless we connect it to # 
#               real server  session  with matching IP and port number.         #
#                                                                               #
#               The script flow only gives an example of how to configure gRIBI #
#               client topology and related parameters in IxNetwork using low   #
#               level TCL API.                                                  #
#                                                                               #
#        Step 2. Start of protocol.                                             #
#        Step 3. Protocol Statistics display.                                   #
#        Step 4. On The Fly(OTF) change of protocol parameter.                  #
#        Step 5. Again Statistics display to see OTF changes took place.        #
#        Step 6. Stop of all protocols.                                         #
#################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.66.47.72
    set ixTclPort   8961
    set ports       {{10.39.50.126 1  3} { 10.39.50.126 1  4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Disconnecting if any already connected"
ixNet disconnect $::ixia::ixTclServer

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 9.20\
    setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

#################################################################################
# Step 1> protocol configuration section
#################################################################################
puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

# Creating topology and device group
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

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "gRIBI Client Topology"
ixNet setAttr $topo2  -name "gRIBI Server Topology"

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]
ixNet commit
puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $t1dev1 -multiplier 1
ixNet setAttr $t2dev1 -multiplier 1
ixNet commit

#  Adding ethernet stack and configuring MAC
puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]
set mac2 [ixNet getList $t2dev1 ethernet]

puts "Configuring the mac addresses"
ixNet setMultiAttr [ixNet getAttr $mac1 -mac]/counter\
        -direction  increment                        \
        -start      {22:22:22:22:22:22}              \
        -step       {00:00:00:00:01:00}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
        -value      {44:44:44:44:44:44}
ixNet commit

#  Adding IPv4 stack and configuring  IP Address
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
ixNet setAttr $mvAdd1/singleValue -value "50.50.50.2"
ixNet setAttr $mvAdd2/singleValue -value "50.50.50.1"
ixNet setAttr $mvGw1/singleValue  -value "50.50.50.1"
ixNet setAttr $mvGw2/singleValue  -value "50.50.50.2"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

#  Adding gRPC Client and configuring it in topology 1 
puts "Adding gRPC Client and configuring it in topology 1"
ixNet add $ip1 gRPCClient
ixNet commit
set gRPCClient [ixNet getList $ip1 gRPCClient]

puts "Configuring remote ip and remote port in gRPC Client"
set remoteIpMultiValue1 [ixNet getAttr $gRPCClient -remoteIp]
ixNet setAttribute $remoteIpMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttribute $remoteIpMultiValue1/singleValue -value "50.50.50.1"
set remotePortMultiValue1 [ixNet getAttr $gRPCClient -remotePort]
ixNet setAttribute $remotePortMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttribute $remotePortMultiValue1/singleValue -value "50001"
ixNet commit

#  Adding gRIBI Client stack over gRPC Client in topology 1 
puts "Adding gRIBI Client stack over gRPC Client in topology 1"
ixNet add $gRPCClient gRIBIClient
ixNet commit
set gRIBIClient [ixNet getList $gRPCClient gRIBIClient]

puts "Configuring Client Redundancy and election IDs in gRIBI Client"
set countMV1 [ixNet getAttr $gRIBIClient -count]

set clientRedundancyMultiValue1 [ixNet getAttr $gRIBIClient -clientRedundancy]
ixNet setAttribute $clientRedundancyMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttribute $clientRedundancyMultiValue1/singleValue -value "singleprimary"

set electionIdHighMultiValue1 [ixNet getAttr $gRIBIClient -electionIdHigh]
ixNet setAttribute $electionIdHighMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttribute $electionIdHighMultiValue1/singleValue -value "1001"

set electionIdLowMultiValue1 [ixNet getAttr $gRIBIClient -electionIdLow]
ixNet setAttribute $electionIdLowMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttribute $electionIdLowMultiValue1/singleValue -value "2001"
ixNet commit

#  Adding gRIBI Next Hop Stack over gRIBI Client in topology 1 
puts "Adding gRIBI Next Hop Stack over gRIBI Client in topology 1"
ixNet add $gRIBIClient gRIBINextHopGroup
ixNet commit
set gRIBINextHopGroup [ixNet getList $gRIBIClient gRIBINextHopGroup]

ixNet setAttribute $gRIBINextHopGroup -multiplier  "5"
ixNet commit

set numberOfNextHopsMultiValue1 [ixNet getAttr $gRIBINextHopGroup -numberOfNextHops]
ixNet setAttribute $gRIBINextHopGroup -numberOfNextHops  "3"
ixNet commit

# Adding Network Topology behind Device Group
puts "Adding the Network Topology"

ixNet exec createDefaultStack $gRIBINextHopGroup ipv4PrefixPools
set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
ixNet setAttr $networkGroup1 -name "Network Group 1"
ixNet commit

puts "Configure metadata and Decapsulation Header type for gRIBI IPv4 entries"
set ipv4PrefixPools [ixNet getList $networkGroup1 ipv4PrefixPools]
set gRIBIIpv4Entry [ixNet getList $ipv4PrefixPools gRIBIIpv4Entry]

set metaDataMv1 [ixNet getAttr $gRIBIIpv4Entry -metaData]
set counter [ixNet add $metaDataMv1 counter]
ixNet setMultiAttribute $counter -direction increment -start "aabbccd1" -step "00000001"
ixNet commit

set decapsulationHeaderMv1 [ixNet getAttr $gRIBIIpv4Entry -decapsulationHeader]
ixNet setAttrbute $decapsulationHeaderMv1/singleValue -value "ipv4"
ixNet commit


################################################################################
# Configure gRIBI server on other port( topology 2) or run demo sever in the port
################################################################################
# To enable hw filters on ixia HW ports execute following command.
# filter --enable-all
#
# To enable hw filters on ixia VM ports execute following command.
# sudo /opt/Ixia/sstream/bin/filter --port=1 --enable-all
#
# To start demo server (ixia specific on server port execute following command.
#  <server_filename> -p <remote port>
# ./SyncServer -p 50051
#
# To start gribi_go_server (openconfig gribi server binary file on server port
#  execute following command.
#  <server_filename> -v -logtostderr -gRIBIPort <remote port>
# ./gribi_mips64 -v 5 -logtostderr -gRIBIPort 50051
#
################################################################################
#
# Step 2> Start of protocol.
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 10000

################################################################################
# Step 3> Retrieve protocol statistics.
################################################################################
puts "Verifying all the stats\n"
puts "Verifying Protocol Summary stats\n"
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
puts "************************************************************"

puts "Verifying gRIBI Per Port stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"gRIBI Client Per Port"/page}
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
puts "************************************************************"

################################################################################
# Step 4 > Change following parameters in Next Hop Group 1 
#          Apply changes on the fly.
################################################################################
#---------------------------------------------------------------------------
#    - Color
#    - Backup Next Hop Group
#---------------------------------------------------------------------------
puts "\n\nChange parameters in Next Hop Group 1 on-the-fly.....\n"

puts "OTF change Color.....\n"
set nhGroupMv [ixNet getAttribute $gRIBINextHopGroup -color]
ixNet setMultiAttribute $nhGroupMv -clearOverlays false
ixNet commit

set counter [ixNet add $nhGroupMv "counter"]
ixNet setMultiAttribute $counter -step 5 -start 4001 -direction increment]
ixNet commit
after 2000

puts "OTF change Backup Next Hop Group.....\n"
set nhGroupMv [ixNet getAttribute $gRIBINextHopGroup -backupNextHopGroup]
ixNet setMultiAttribute $nhGroupMv -clearOverlays false
ixNet commit

set counter [ixNet add $nhGroupMv "counter"]
ixNet setMultiAttribute $counter -step 101 -start 1 -direction increment]
ixNet commit
after 2000


set globals [ixNet getRoot]/globals
set topology $globals/topology
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
        puts "$::errorInfo"
}
after 5000

################################################################################
# Step 5> Retrieve protocol statistics.
################################################################################
puts "Verifying gRIBI Per Port stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"gRIBI Client Per Port"/page}
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
puts "************************************************************"

################################################################################
# Step 6> Stop all protocols.
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
