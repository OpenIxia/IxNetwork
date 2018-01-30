#/usr/bin/tclsh

################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    05/28/2014 - Deepak Kumar Singh - created sample                          #
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
#    This script intends to demonstrate how to use TCL APIs to import          #
#    BGP Routes in Ixia CSV format.                                            #
#    1. It will create 2 BGP topologies.                                       #
#    2. Generate Statistical IPv4 routes in topology2.                         #
#    3. Start the BGP protocol.                                                #
#    4. Retrieve protocol statistics.                                          #
#    5. Retrieve protocol learned info.                                        #
#    6. Stop all protocols.                                                    #
# Ixia Softwares:                                                              #
#    IxOS      6.80 EB (6.80.1101.116)                                         #
#    IxNetwork 7.40 EB (7.40.929.3)                                            #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.25.63
    set ixTclPort   8009
    set ports       {{10.205.28.12 6 7} { 10.205.28.12 6 8}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# Protocol configuration section                                               #
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

puts "Adding BGP over IP4 stack"
ixNet add $ip1 bgpIpv4Peer
ixNet add $ip2 bgpIpv4Peer
ixNet commit

set bgp1 [ixNet getList $ip1 bgpIpv4Peer]
set bgp2 [ixNet getList $ip2 bgpIpv4Peer]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1 -name "BGP Topology 1"
ixNet setAttr $topo2 -name "BGP Topology 2"

ixNet setAttr $t1dev1 -name "BGP Topology 1 Router"
ixNet setAttr $t2dev1 -name "BGP Topology 2 Router"
ixNet commit

puts "Setting IPs in BGP DUT IP tab"
ixNet setAttr [ixNet getAttr $bgp1 -dutIp]/singleValue -value "20.20.20.1"
ixNet setAttr [ixNet getAttr $bgp2 -dutIp]/singleValue -value "20.20.20.2"
ixNet commit

################################################################################
# Import BGP Routes in Ixia csv format in Topology2                            #
################################################################################
puts "Importing BGP Routes in Ixia Format"
set networkGroup [ixNet add $t2dev1 networkGroup] 
ixNet commit
set networkGroup [ixNet remapId $networkGroup]
set ipv4PrefixPools [ixNet add $networkGroup ipv4PrefixPools]
ixNet commit
set ipv4PrefixPools [ixNet remapId $ipv4PrefixPools]
set bgpIPRouteProperty [lindex [ixNet getList $ipv4PrefixPools bgpIPRouteProperty] 0]
set importBgpRoutesParams $bgpIPRouteProperty/importBgpRoutesParams
ixNet getAttribute $importBgpRoutesParams -routeDistributionType
ixNet setMultiAttribute $importBgpRoutesParams -routeDistributionType roundRobin \
                                               -bestRoutes false \
                                               -nextHop overwriteTestersAddress \
                                               -fileType csv \
                                               -dataFile [ixNet readFrom BGP_RouteImport_sample.csv]
ixNet commit
ixNet exec importBgpRoutes $importBgpRoutesParams
puts "Successfully imported IPv4 Routes !!!"
after 2000 

################################################################################
# Start protocol and check statistics                                          #
################################################################################
puts "Starting protocols and waiting for 45 seconds for protocols to come up"
ixNet exec startAllProtocols
after 45000
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
# On the fly section                                                           #  
################################################################################
puts "Enabling IPv4 Unicast Learned Information for BGP Router"
ixNet setAttr [ixNet getAttr $bgp1 -filterIpV4Unicast]/singleValue -value true
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
after 10000

###############################################################################
# Print learned info                                                          #
###############################################################################
ixNet exec getIPv4LearnedInfo $bgp1 1
after 5000
set linfo [ixNet getList $bgp1 learnedInfo]
set values [ixNet getAttribute $linfo -values]
puts "BGP learned info"
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"

################################################################################
# Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"