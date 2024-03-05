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
# The script is not a standard commercial product offered by Ixia Keysight and #
# have     																	   #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia Keysight and/or by the user and/or by a third party)] shall at  #
# all times 																   #
# remain the property of Ixia Keysight.                                        #
#                                                                              #
# Ixia Keysight does not warrant (i) that the functions contained in the script#
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND Ixia Keysight#
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL Ixia Keysight BE LIABLE FOR ANY DAMAGES RESULTING FROM OR  #
# ARISING   																   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF Ixia Keysight HAS BEEN ADVISED OF THE          #
# POSSIBILITY OF  SUCH DAMAGES IN ADVANCE.                                     #
# Ixia Keysight will not be required to provide any software maintenance or    #
# support services of any kind (e.g. any error corrections) in connection with #
# script or any part thereof. The user acknowledges that although Ixia Keysight# 
# may     																	   #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia Keysight to  #
# provide any additional maintenance or support services.                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    Script  will create following:                                            #
#    1. Adding ports to configuration                                          #
#    2. Create VxLanV6 with IPv4 hosts                                         #
#    3.	Enable unicast info                                                    #
#    4. Start all protocols                           						   #
#  	 5. Check stats and learned info										   #
#    6. Stop all protocols	   					  							   #
#                                                                              #
################################################################################


#edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.65.1
    set ixTclPort   9863
    set ports       {{10.39.64.117 2 7} {10.39.64.117 2 8}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 9.00

puts "Creating a new config"
ixNet exec newConfig

puts "Adding 2 vports"
ixNet add 				[ixNet getRoot] vport
ixNet add 				[ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 				[lindex $vPorts 0]
set vport2 				[lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

after 5000

################################################################################
# 1. Adding ports to configuration
################################################################################

puts "Adding ports to configuration"
set root [ixNet getRoot]
ixNet commit
set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 [lindex $vPorts 0]
set vport2 [lindex $vPorts 1]

################################################################################
# 2. Adding VXLANv6 Protocol
################################################################################
puts "Add topologies"
ixNet add [ixNet getRoot] topology
ixNet add [ixNet getRoot] topology
ixNet commit

set topo1 [lindex [ixNet getList [ixNet getRoot] topology] 0]
set topo2 [lindex [ixNet getList [ixNet getRoot] topology] 1]

puts "Add ports to topologies"
ixNet setA $topo1 -vports $vport1
ixNet setA $topo2 -vports $vport2
ixNet commit

puts "Add device groups to topologies"
ixNet add $topo1 deviceGroup
ixNet add $topo2 deviceGroup
ixNet commit

set dg1 [ixNet getList $topo1 deviceGroup]
set dg2 [ixNet getList $topo2 deviceGroup]

puts "Add Ethernet stacks to device groups"
ixNet add $dg1 ethernet
ixNet add $dg2 ethernet
ixNet commit

set mac1 [ixNet getList $dg1 ethernet]
set mac2 [ixNet getList $dg2 ethernet]

puts "Add ipv6 stacks to Ethernets"
ixNet add $mac1 ipv6
ixNet add $mac2 ipv6
ixNet commit

set ipv6_1 [ixNet getList $mac1 ipv6]
set ipv6_2 [ixNet getList $mac2 ipv6]

#Setting ipv6 address and ipv6 gateway address
puts "Setting multi values for ipv6 addresses"
ixNet setMultiAttribute [ixNet getAttribute $ipv6_1 -address]/counter -start 2000:0:0:1:0:0:0:2 -step 0:0:0:1:0:0:0:0
ixNet setMultiAttribute [ixNet getAttribute $ipv6_1 -gatewayIp]/counter -start 2000:0:0:1:0:0:0:1 -step 0:0:0:1:0:0:0:0
ixNet setMultiAttribute [ixNet getAttribute $ipv6_1 -resolveGateway]/singleValue -value true
ixNet setMultiAttribute [ixNet getAttribute $ipv6_2 -address]/counter -start 2000:0:0:1:0:0:0:1 -step 0:0:0:1:0:0:0:0
ixNet setMultiAttribute [ixNet getAttribute $ipv6_2 -gatewayIp]/counter -start 2000:0:0:1:0:0:0:2 -step 0:0:0:1:0:0:0:0
ixNet setMultiAttribute [ixNet getAttribute $ipv6_2 -resolveGateway]/singleValue -value true
ixNet commit

puts "Add VXLANV6 stacks to IPv6"
ixNet add $ipv6_1 vxlanv6
ixNet add $ipv6_2 vxlanv6
ixNet commit

set vxlanv6_1 [lindex [ixNet getList $ipv6_1 vxlanv6] 0]
set vxlanv6_2 [lindex [ixNet getList $ipv6_2 vxlanv6] 0]

ixNet setMultiAttribute [ixNet getAttribute $vxlanv6_1 -vni]/counter -start 1100 -step 1
ixNet setMultiAttribute [ixNet getAttribute $vxlanv6_1 -ipv6_multicast]/counter -start ff03:0:0:0:0:0:0:1 -step 0:0:0:0:0:0:0:1
ixNet setMultiAttribute [ixNet getAttribute $vxlanv6_2 -vni]/counter -start 1100 -step 1
ixNet setMultiAttribute [ixNet getAttribute $vxlanv6_2 -ipv6_multicast]/counter -start ff03:0:0:0:0:0:0:1 -step 0:0:0:0:0:0:0:1

ixNet setMultiAttribute $vxlanv6_1 \
		-enableStaticInfo true \
		-staticInfoCount 1 \
		-stackedLayers [list ] \
		-name "VXLAN\ 1"
ixNet commit

#Adding IPv4 Hosts behind VxLANv6 device group
puts "Add IPv4 hosts to VXLANv6 device group "
ixNet add $dg1 deviceGroup
ixNet add $dg2 deviceGroup
ixNet commit

set dg3 [lindex [ixNet getList $dg1 deviceGroup] 0]
set dg4 [lindex [ixNet getList $dg2 deviceGroup] 0]

puts "Add Ethernet stacks to IPv4 hosts"
ixNet add $dg3 ethernet
ixNet add $dg4 ethernet
ixNet commit

set mac3 [lindex [ixNet getList $dg3 ethernet] 0]
set mac4 [lindex [ixNet getList $dg4 ethernet] 0]

puts "Add IPv4 stacks to IPv4 hosts"
ixNet add $mac3 ipv4
ixNet add $mac4 ipv4
ixNet commit

set ipv4_3 [lindex [ixNet getList $mac3 ipv4] 0]
set ipv4_4 [lindex [ixNet getList $mac4 ipv4] 0]

puts "Setting multi values for IPv4 hosts"
ixNet setMultiAttribute [ixNet getAttribute $ipv4_3 -address]/counter -start 5.1.1.1 -step 0.0.1.0
ixNet setMultiAttribute [ixNet getAttribute $ipv4_3 -gatewayIp]/counter -start 5.1.1.2 -step 0.0.1.0
ixNet setMultiAttribute [ixNet getAttribute $ipv4_3 -resolveGateway]/singleValue -value true
ixNet setMultiAttribute [ixNet getAttribute $ipv4_4 -address]/counter -start 5.1.1.2 -step 0.0.1.0
ixNet setMultiAttribute [ixNet getAttribute $ipv4_4 -gatewayIp]/counter -start 5.1.1.1 -step 0.0.1.0
ixNet setMultiAttribute [ixNet getAttribute $ipv4_4 -resolveGateway]/singleValue -value true
ixNet commit


################################################################################
# 3. Start protocol 
################################################################################
puts "Starting protocols and waiting for 30 seconds for protocols to come up"
ixNet exec startAllProtocols
after 30000

################################################################################
# 4. Retrieve protocol statistics.
################################################################################

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

puts "Verifying VXLANv6  per port stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"VXLANv6 Per Port"/page}
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


###############################################################################
# 5. Retrieve protocol learned info
###############################################################################
ixNet exec getVXLANLearnedInfo $vxlanv6_1 1
after 5000
puts "Getting VxLanV6 Learned info!!!!!!!"
set learnedInfoList [ixNet getL $vxlanv6_1 learnedInfo]
set learnedInfo [lindex $learnedInfoList end]
set table [lindex [ixNet getList $learnedInfo table] 0]
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
################################################################################
# 6. Stop protocol 
################################################################################
ixNet exec stopAllProtocols
after 5000

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