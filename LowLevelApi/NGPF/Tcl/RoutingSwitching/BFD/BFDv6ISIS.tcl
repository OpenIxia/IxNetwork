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
#    This script intends to demonstrate how to use NGPF BFDv6  API             #
#    It will create 2 BFDv6  topologies, it will start the emulation and       #
#    than it will retrieve and display few statistics                          #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.216.22.27
    set ixTclPort   8229
    set ports       {{10.216.108.99 11 3} { 10.216.108.99 11 4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.00\
    �setAttribute strict

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

puts "Add ipv6"
ixNet add $mac1 ipv6
ixNet add $mac2 ipv6
ixNet commit

set ip1 [ixNet getList $mac1 ipv6]
set ip2 [ixNet getList $mac2 ipv6]

set mvAdd1 [ixNet getAttr $ip1 -address]
set mvAdd2 [ixNet getAttr $ip2 -address]
set mvGw1  [ixNet getAttr $ip1 -gatewayIp]
set mvGw2  [ixNet getAttr $ip2 -gatewayIp]

puts "configuring ipv6 addresses"
ixNet setAttr $mvAdd1/singleValue -value "11:0:0:0:0:0:0:1"
ixNet setAttr $mvAdd2/singleValue -value "11:0:0:0:0:0:0:2"
ixNet setAttr $mvGw1/singleValue  -value "11:0:0:0:0:0:0:2"
ixNet setAttr $mvGw2/singleValue  -value "11:0:0:0:0:0:0:1"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 64
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 64
ixNet commit

#######################################################################
#Adding and Configuring ISIS L3 Router                                
#######################################################################
puts "Adding and Configuring ISIS-L3"
ixNet add $mac1 isisL3
ixNet add $mac2 isisL3
ixNet commit

set isisL31 [ixNet getList $mac1 isisL3]
set isisL32 [ixNet getList $mac2 isisL3]

set networkType1 [ixNet getAttr $isisL31 -networkType]
set networkType2 [ixNet getAttr $isisL32 -networkType]
set enableBFD1 [ixNet getAttr $isisL31 -enableBfdRegistration]
set enableBFD2 [ixNet getAttr $isisL32 -enableBfdRegistration]

ixNet setAttr $networkType1/singleValue -value pointpoint
ixNet setAttr $networkType2/singleValue -value pointpoint
ixNet setAttr $enableBFD1/singleValue -value true
ixNet setAttr $enableBFD2/singleValue -value true
ixNet commit

###########################################################################
#Add and Configure BFDv6 Interface 
###########################################################################
puts "Add BFDv6 Interface"
ixNet add $ip1 bfdv6Interface
ixNet add $ip2 bfdv6Interface
ixNet commit

set bfdv61 [ixNet getList $ip1 bfdv6Interface]
set bfdv62 [ixNet getList $ip2 bfdv6Interface]

set txInterval1 [ixNet getAttr $bfdv61 -txInterval]
set txInterval2 [ixNet getAttr $bfdv62 -txInterval]
set minRxInterval1 [ixNet getAttr $bfdv61 -minRxInterval]
set minRxInterval2 [ixNet getAttr $bfdv62 -minRxInterval]

puts "Configuring Tx Interval and Min Rx Interval on BFD Interface"
ixNet setAttr $txInterval1/singleValue -value 2000
ixNet setAttr $txInterval2/singleValue -value 2000
ixNet setAttr $minRxInterval1/singleValue -value 2000
ixNet setAttr $minRxInterval2/singleValue -value 2000
ixNet commit

#############################################################################
#Starting Protocols and Dispalying Statistics
#############################################################################
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

############################################################################
##On The Fly Section
############################################################################
puts "Deactivating and Then Activating BFD Interfaces"

set activation [ixNet getAttr $bfdv61 -active]

ixNet setAttr $activation/singleValue -value false
ixNet commit
set topology [ixNet getRoot]/globals/topology
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
	puts "$::errorInfo"
}
after 10000

ixNet setAttr $activation/singleValue -value true
ixNet commit
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
	puts "$::errorInfo"
}
after 10000

############################################################################
#Fetching and Displaying Learned Information on BFDv4 Interface
############################################################################
ixNet exec getLearnedInfo $bfdv61 1
after 5000
set linfo [ixNet getList $bfdv61 learnedInfo]
set values [ixNet getAttribute $linfo -values]
puts "BFD learned info"
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"

puts " "
puts "For more info please refer to the user manual or the built-in help"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6/bfdv6Interface"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6/bfdv6Interface]"

puts "Stopping all protocols"
ixNet exec stopAllProtocols
puts "*********************************************************************END*************************************************************************"
