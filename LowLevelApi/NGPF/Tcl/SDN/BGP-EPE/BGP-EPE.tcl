#!/usr/bin/tclsh
################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
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

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF BGP EPE API            #
#    It will create 2 BGP EPE topologies, it will start the emulation and      #
#    than it will retrieve and display few statistics                          #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.43.12
    set ixTclPort   8072
    set ports       {{10.39.50.123 5 7} { 10.39.50.123 5 8}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.50\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# protocol configuration section                                               #
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

################################################################################
# Topoligy section                                                             #
################################################################################ 

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

puts "Adding IPv4 protocol stack"
ixNet add $mac1 ipv4
ixNet add $mac2 ipv4
ixNet commit

set ip1 [ixNet getList $mac1 ipv4]
set ip2 [ixNet getList $mac2 ipv4]

set mvAdd1 [ixNet getAttr $ip1 -address]
set mvAdd2 [ixNet getAttr $ip2 -address]
set mvGw1  [ixNet getAttr $ip1 -gatewayIp]
set mvGw2  [ixNet getAttr $ip2 -gatewayIp]

puts "Configuring IPv4 addresses"
ixNet setAttr $mvAdd1/singleValue -value "20.20.20.2"
ixNet setAttr $mvAdd2/singleValue -value "20.20.20.1"
ixNet setAttr $mvGw1/singleValue  -value "20.20.20.1"
ixNet setAttr $mvGw2/singleValue  -value "20.20.20.2"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

puts "Adding BGP protocol stack over IP4"
ixNet add $ip1 bgpIpv4Peer
ixNet add $ip2 bgpIpv4Peer
ixNet commit

set bgp1 [ixNet getList $ip1 bgpIpv4Peer]
set bgp2 [ixNet getList $ip2 bgpIpv4Peer]

puts "Setting IPs in BGP DUT IP tab"
ixNet setAttr [ixNet getAttr $bgp1 -dutIp]/singleValue -value "20.20.20.1"
ixNet setAttr [ixNet getAttr $bgp2 -dutIp]/singleValue -value "20.20.20.2"
ixNet commit

puts "Enabling BGP Link State Non-VPN Capability"
set cap1 [ixNet getAttr $bgp1 -capabilityLinkStateNonVpn]
set cap2 [ixNet getAttr $bgp2 -capabilityLinkStateNonVpn]
set sv1 [ixNet getList $cap1 singleValue]
set sv2 [ixNet getList $cap2 singleValue]
ixNet setAttr $sv1 -value true
ixNet setAttr $sv2 -value true
ixNet commit

puts "Enabling BGP Filter Link State"
set filter1 [ixNet getAttr $bgp1 -filterLinkState]
set filter2 [ixNet getAttr $bgp2 -filterLinkState]
set sv1 [ixNet getList $filter1 singleValue]
set sv2 [ixNet getList $filter2 singleValue]
ixNet setAttr $sv1 -value true
ixNet setAttr $sv2 -value true
ixNet commit

puts "Enable BGP EPE in Topology 1"
ixNet setAttr $bgp1 -noOfEpePeers 3
ixNet commit

set bgpEpePeerList [ixNet getList $bgp1 bgpEpePeerList]
set bgpEpePeerLinkList [ixNet getList $bgpEpePeerList bgpEpePeerLinkList]

puts "Setting Number of Links for BGP EPE to 2 in Topology 1"
ixNet setAttr $bgpEpePeerList -noOflinks 2
ixNet commit

puts "Setting Number of EPE Peer Set to 3 in Topology 1"
ixNet setAttr $bgpEpePeerList -noOfPeerSet 2
ixNet commit

puts "Selection of Peer Set Group"
set peerSetGroup [ixNet getAttr $bgpEpePeerList -peerSetGroup]
ixNet setMultiAttribute $peerSetGroup -clearOverlays true
set activeOverlay [ixNet add $peerSetGroup "overlay"]
set activeOverlay [ixNet add $peerSetGroup "singleValue"]
ixNet setMultiAttribute $activeOverlay -value "peersetgroup1 peersetgroup2"
ixNet commit

puts "Setting BGP Remote Router ID as DUT IP of BGP Peer"
ixNet setAttr [ixNet getAttr $bgpEpePeerList -bgpRemoteRouterId]/singleValue -value "20.20.20.1"
ixNet commit

puts "Setting EPE Peer Links Peer-Adj-SID to True"
ixNet setAttr [ixNet getAttr $bgpEpePeerLinkList -enablePeerAdjSid]/singleValue -value "True"
ixNet commit

puts "Setting EPE Peer Links Remote IPv4 Link Address"
ixNet setAttr [ixNet getAttr $bgpEpePeerLinkList -remoteIpv4LinkAddress]/singleValue -value "20.20.20.1"
ixNet commit

set bgpLocalIp [ixNet getAttr $bgp1 -localIpv4Ver2]

puts "Setting EPE Peer Links Local IPv4 Link Address"
ixNet setAttr [ixNet getAttr $bgpEpePeerLinkList -localIpv4LinkAddress]/singleValue -value $bgpLocalIp
ixNet commit


puts "Adding OSPFv2 over IP4 stack"
set ospf1 [ixNet add $ip1 ospfv2]
set ospf2 [ixNet add $ip2 ospfv2]
ixNet commit

puts "Changing OSPFv2 Network Type"
set networkTypeMultiValue1 [ixNet getAttr $ospf1 -networkType]
ixNet setAttr $networkTypeMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue1/singleValue -value pointtopoint

set networkTypeMultiValue2 [ixNet getAttr $ospf2 -networkType]
ixNet setAttr $networkTypeMultiValue2 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue2/singleValue -value pointtopoint

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "BGP Topology 1"
ixNet setAttr $topo2  -name "BGP Topology 2"

ixNet setAttr $t1dev1 -name "BGP Topology 1 Router"
ixNet setAttr $t2dev1 -name "BGP Topology 2 Router"
ixNet commit

################################################################################
# Start protocol and check statistics                                          #
################################################################################
puts "Starting protocols and waiting for 45 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000
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

puts "Verifying BGP Peer related stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"BGP Peer Per Port"/page}
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

###############################################################################
# print learned info                                                          #
###############################################################################
ixNet exec getLinkStateLearnedInfo $bgp2 1
after 5000

puts "Print BGP-LS EPE Learned Info"
set learnedInfoList [ixNet getList $bgp2 learnedInfo]
set learnedInfo [lindex $learnedInfoList end]
set table [lindex [ixNet getList $learnedInfo table] 3]
set learnedInfoColumnsList [ixNet getAttr $table -columns]
set learnedInfoValuesList [ixNet getAttr $table -values]
set row2 [lindex $learnedInfoValuesList 1]

puts "***************************************************"
foreach v $learnedInfoColumnsList {
    puts $v
}
puts "***************************************************"

puts "***************************************************"
foreach v $row2 {
    puts $v
}
puts "***************************************************"

puts "Stopping all protocols"
ixNet exec stopAllProtocols
puts "*********************************************************************END*************************************************************************"
