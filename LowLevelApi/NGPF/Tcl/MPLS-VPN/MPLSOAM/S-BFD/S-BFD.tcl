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
#   This script intends to demonstrate how to use NGPF S-BFD using             #
#   Low Level TCL API #               					                       #        
#                                                                              #
#    1. Configuration of protocols as described in topology.                   #
#    2. Start all protocols.                                                   #
#    3. Retrieve protocol statistics and check Learned Information.            #
#    4. Deactivate the first initiator OTF                                     #
#    5. Retrieve protocol statistics and check Learned Information again.      #
#    6. Deactivate the first initiator OTF                                     #
#    7. Retrieve protocol statistics again                                     #
#    8. Change the discrminator of the first responder OTF                     #
#    9. Retrieve protocol statistics again.                                    #
#   10. Stop all protocols.                                                    #                                                                                
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.50.134
    set ixTclPort   8998
    set ports       {{10.39.50.126 1 9} { 10.39.50.126 1 13}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.60\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. 
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
        -start      {00:11:01:00:00:01}              \
        -step       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
        -value      {00:12:01:00:00:01}
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
ixNet setAttr $mvAdd1/singleValue -value "20.20.20.1"
ixNet setAttr $mvAdd2/singleValue -value "20.20.20.2"
ixNet setAttr $mvGw1/singleValue  -value "20.20.20.2"
ixNet setAttr $mvGw2/singleValue  -value "20.20.20.1"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit


puts "Adding ISIS over Ethernet stacks"
ixNet add $mac1 isisL3
ixNet add $mac2 isisL3
ixNet commit


set isis1 [ixNet getList $mac1 isisL3]
set isis2 [ixNet getList $mac2 isisL3]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "S-BFD Inititator Topology'"
ixNet setAttr $topo2  -name "S-BFD Responder Topology'"

ixNet commit

puts "Adding NetworkGroup behind the DG"

ixNet add $t1dev1 networkGroup
ixNet add $t2dev1 networkGroup
ixNet commit


set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

ixNet setAttr $networkGroup1 -multiplier "1"
ixNet setAttr $networkGroup2 -multiplier "1"
ixNet commit



puts "Configuring Network Topology in Network Groups"
ixNet add $networkGroup1 networkTopology
ixNet add $networkGroup2 networkTopology
ixNet commit

set nt1 [ixNet getList $networkGroup1 networkTopology]
set nt2 [ixNet getList $networkGroup2 networkTopology]


ixNet add $nt1 netTopologyLinear
ixNet add $nt2 netTopologyLinear
ixNet commit

set nt11 [ixNet getList $nt1 netTopologyLinear]
set nt12 [ixNet getList $nt2 netTopologyLinear]
ixNet commit

ixNet setAttr $nt11 -nodes "150"
ixNet setAttr $nt12 -nodes "150"
ixNet commit

ixNet add $nt1 simRouter
ixNet add $nt2 simRouter
ixNet commit

set simRouter1 [ixNet getList $nt1 simRouter]
set simRouter2 [ixNet getList $nt2 simRouter]
ixNet commit

ixNet add $simRouter1 isisL3PseudoRouter
ixNet add $simRouter2 isisL3PseudoRouter
ixNet commit

set Router1 [ixNet getList $simRouter1 isisL3PseudoRouter]
set Router2 [ixNet getList $simRouter2 isisL3PseudoRouter]
ixNet commit



puts "Configuring SR on ISIS Router"

ixNet setAttr $Router2 -enableSR "true"

set nodePrefix [ixNet getAttribute $Router2 -nodePrefix]
ixNet setMultiAttribute $nodePrefix\
    -clearOverlays false\
    -pattern counter
ixNet commit

set counter [ixNet add $nodePrefix "counter"]
ixNet setMultiAttribute $counter\
    -step 0.0.0.1\
    -start 2.2.2.2\
    -direction increment
ixNet commit

set sIDIndexLabel1 [ixNet getAttribute $Router2 -sIDIndexLabel]
ixNet setMultiAttribute $sIDIndexLabel1\
    -clearOverlays false\
    -pattern counter
ixNet commit

set counter2 [ixNet add $sIDIndexLabel1 "counter"]
ixNet setMultiAttribute $counter2\
    -step 1\
    -start 1\
    -direction increment
ixNet commit




puts "Adding Device Group behind Network Groups"
ixNet add $networkGroup1 deviceGroup
ixNet add $networkGroup2 deviceGroup
ixNet commit


set t1dev2 [lindex [ixNet getList $networkGroup1 deviceGroup] 0]
set t2dev2 [lindex [ixNet getList $networkGroup2 deviceGroup] 0]

puts "Configuring the multipliers"
ixNet setAttr $t1dev2 -multiplier 150
ixNet setAttr $t2dev2 -multiplier 150
ixNet commit

ixNet setAttr $t1dev2 -name "Initiator"
ixNet setAttr $t2dev2 -name "Responder"
ixNet commit

puts "Adding loopback in second device group of both topologies"
ixNet add $t1dev2 ipv4Loopback
ixNet add $t2dev2 ipv4Loopback
ixNet commit

set ipv4Loopback1 [ixNet getList $t1dev2 ipv4Loopback]
set ipv4Loopback2 [ixNet getList $t2dev2 ipv4Loopback]

puts "Adding MPLSOAM over these loopbacks"
ixNet add $ipv4Loopback1 mplsOam
ixNet add $ipv4Loopback2 mplsOam
ixNet commit

puts "Assigning ipv4 address on Loop Back Interface"
set addressSet1 [ixNet getAttribute $ipv4Loopback1 -address]
ixNet setMultiAttribute $addressSet1\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet1 [ixNet add $addressSet1 "counter"]
ixNet setMultiAttribute $addressSet1\
    -step 0.0.0.1\
    -start 1.1.1.1\
    -direction increment
ixNet commit

set addressSet2 [ixNet getAttribute $ipv4Loopback2 -address]
ixNet setMultiAttribute $addressSet2\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet2 [ixNet add $addressSet2 "counter"]
ixNet setMultiAttribute $addressSet2\
    -step 0.0.0.1\
    -start 2.2.2.2\
    -direction increment
ixNet commit

set mplsoam1 [ixNet getList $ipv4Loopback1 mplsOam]
set mplsoam2 [ixNet getList $ipv4Loopback2 mplsOam]

ixNet setAttr $mplsoam2 -enableSBfdResponder "true"
ixNet setAttr $mplsoam1 -initiatorSBFDSessionCount "1"
ixNet commit

ixNet add $mplsoam1 sbfdInitiator
ixNet add $mplsoam2 sbfdResponder


set sbfdinit [lindex [ixNet getList $mplsoam1 sbfdInitiator] 0]
set sbfdresp [lindex [ixNet getList $mplsoam2 sbfdResponder] 0]
ixNet commit

set peerDisc [ixNet getAttribute $sbfdinit -peerDiscriminator]
set respDisc [ixNet getAttribute $sbfdresp -sBFDDiscriminator]
ixNet setMultiAttribute $peerDisc\
    -clearOverlays false\
    -pattern counter
ixNet commit

set counter3 [ixNet add $peerDisc "counter"]
ixNet setMultiAttribute $counter3\
    -step 1\
    -start 1\
    -direction increment
ixNet commit

ixNet add $sbfdinit mplsLabelList
ixNet commit

set sbflabel [lindex [ixNet getList $sbfdinit mplsLabelList] 0]
set label [ixNet getAttribute $sbflabel -mplsLabel]

ixNet setMultiAttribute $label\
    -clearOverlays false\
    -pattern counter
ixNet commit
set counter4 [ixNet add $label "counter"]
ixNet setMultiAttribute $counter4\
    -step 1\
    -start 16001\
    -direction increment
ixNet commit


################################################################################
# 2. Start all  protocol and wait for 60 seconds
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

#################################################################################
# Retrieve protocol learned info                                                #
#################################################################################
puts "Fetching MPLSOAM Basic Learned Info"
ixNet exec getAllLearnedInfo $mplsoam1 1 
after 5000
set linfo [ixNet getList $mplsoam1 learnedInfo]
ixNet getAttr $linfo -columns
set values [ixNet getAttribute $linfo -values]

puts "***************************************************"
foreach v $values {
        puts $v
}
puts "***************************************************"


################################################################################
# Deactivate the First initiator                                               #
################################################################################
puts "Deactivating the first initiator"
set root [ixNet getRoot]
set active_1 [ixNet getAttribute $sbfdinit -active]
set overlay1 [ixNet add $active_1 "overlay"]
ixNet setMulA $overlay1 -index 1 -value false

ixNet commit
if {[catch {ixNet exec applyOnTheFly $root/globals/topology}]} {
        puts "Could not apply changes on the fly: $::errorInfo"
        return $FAILED
}
after 30000


################################################################################
# Applying changes on the fly                                                  #
################################################################################
puts "Applying changes on the fly"
set globals [ixNet getRoot]/globals
set topology $globals/topology
ixNet exec applyOnTheFly $topology
after 10000


################################################################################
# 3. Retrieve protocol statistics again after deactivating
################################################################################
puts "Fetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"MPLSOAM IF Per Port"/page}
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

#################################################################################
# Retrieve protocol learned info again afetr deactivating                       #
#################################################################################
puts "Fetching MPLSOAM Basic Learned Info"
ixNet exec getAllLearnedInfo $mplsoam1 1 
after 5000
set linfo [ixNet getList $mplsoam1 learnedInfo]
ixNet getAttr $linfo -columns
set values [ixNet getAttribute $linfo -values]

puts "***************************************************"
foreach v $values {
        puts $v
}
puts "***************************************************"

################################################################################
# Activate the First initiator                                                 #
################################################################################

puts "Activating the first  initiator"
set root [ixNet getRoot]
set active_1 [ixNet getAttribute $sbfdinit -active]
set overlay1 [ixNet add $active_1 "overlay"]
ixNet setMulA $overlay1 -index 1 -value true

ixNet commit
if {[catch {ixNet exec applyOnTheFly $root/globals/topology}]} {
        puts "Could not apply changes on the fly: $::errorInfo"
        return $FAILED
}
after 30000


################################################################################
# Applying changes on the fly                                                  #
################################################################################
puts "Applying changes on the fly"
set globals [ixNet getRoot]/globals
set topology $globals/topology
ixNet exec applyOnTheFly $topology
after 10000


################################################################################
# 3. Retrieve protocol statistics again after deactivating
################################################################################
puts "Fetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"MPLSOAM IF Per Port"/page}
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
# OTF changing the discriminator the the 1st responder                         #
################################################################################

puts "OTF changing the peer discriminator the the 1st initiator "
set overlay5 [ixNet add $respDisc "overlay"]
ixNet setMulA $overlay5 -index 1 -value 100

ixNet commit
if {[catch {ixNet exec applyOnTheFly $root/globals/topology}]} {
        puts "Could not apply changes on the fly: $::errorInfo"
        return $FAILED
}
after 30000


################################################################################
# Applying changes on the fly                                                  #
################################################################################
puts "Applying changes on the fly"
set globals [ixNet getRoot]/globals
set topology $globals/topology
ixNet exec applyOnTheFly $topology
after 10000


################################################################################
# 3. Retrieve protocol statistics again after changing the Peer Disc
################################################################################
puts "Fetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"MPLSOAM IF Per Port"/page}
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
# Stop all protocols                                                          #
################################################################################
puts "Stopping all protocols"
ixNet exec stopAllProtocols

puts "!!! Test Script Ends !!!"

