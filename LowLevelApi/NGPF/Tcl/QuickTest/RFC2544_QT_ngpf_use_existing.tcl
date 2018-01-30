################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Daniel Iordache $
#
#    Copyright © 1997 - 2015 by IXIA
#    All Rights Reserved.
#
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              														  #
# Description:                                                                													  #
#    This sample script configures a RFC2544 Tput/Latency Use-Existing QT over NGPF     	  #						     
#                                                                            															  #
# Steps:   1 -> Cleaning up IxNetwork                                         											  #
#	   			2 -> Add virtual port                                               												  #
#	  			3  -> Add topologies                                               											  #
#	   			4  -> Add device groups                                             											  #
#	   			5 -> Add values for deviceGroup and Topologies                     								  #
#	   			6 -> Add mac to device group                                      									      #
#	   			7  -> Add ipv4 to device group                                      										  #
#	   			8 -> Add virtual ports to topology                                  										  #
#	   			9 -> Setting multiple values for ipv4 addresse                     									  #
#	   			10 -> Creating Traffic Item                                        											  #
#	   			11  -> Creating QT                                                 											  #
#	   			12 -> Assigning ports to virtual ports                              										  #                
#	   			13 -> Starting All Protocols                                        											  #
#	   			14 -> Apply QT                                                      											  #
#	   			15 -> Starting QT                                                   											  #
#	   			16 -> Test run status                                 										  #
#     			17 -> Cleaning up the client                                        										  #
# 									      																								  #
################################################################################


namespace eval ::py {
    #client domain name or ip address
    set ixTclServer PC-name 
    #client Tcl port
    set ixTclPort   8009    
    #chassis ip address/domain name ; card number ; port number	
    set ports       {{192.168.1.1 1 1} {192.168.1.1 1 2}} 
}

################################################################################
# Source the IxNet library
################################################################################
package req IxTclNetwork

################################################################################
# Connect to IxNet client
################################################################################
ixNet connect $::py::ixTclServer -port $::py::ixTclPort -version 7.50

################################################################################
# Cleaning up IxNetwork
################################################################################
puts "Step 1 -> Cleaning up IxNetwork..."
ixNet exec newConfig

################################################################################
# TEST BODY START
################################################################################
set FAILED 1
set PASSED 0

puts "Step 2 -> Add virtual port"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] topology
ixNet add [ixNet getRoot] topology
ixNet commit

puts "Step 3  -> Add topologies"
set topo1 [lindex [ixNet getList [ixNet getRoot] topology] 0]
set topo2 [lindex [ixNet getList [ixNet getRoot] topology] 1]
set vPorts [ixNet getList [ixNet getRoot] vport]

set vport1 [lindex $vPorts 0]
set vport2 [lindex $vPorts 1]

puts "Step 4  -> Add device groups"
ixNet add $topo1 deviceGroup
ixNet add $topo2 deviceGroup
ixNet commit

set dev1 [ixNet getList $topo1 deviceGroup]
set dev2 [ixNet getList $topo2 deviceGroup]

puts "Step 5 -> Add values for deviceGroup and Topologies"
ixNet setA $dev1 -multiplier 5
ixNet setA $dev2 -multiplier 5
ixNet setAttr $topo1 -name "ipv4_topo1"
ixNet setAttr $topo2 -name "ipv4_topo2"
ixNet commit

puts "Step 6 -> Add mac to device group"
ixNet add $dev1 ethernet
ixNet add $dev2 ethernet
ixNet commit

set mac1 [ixNet getList $dev1 ethernet]
set mac2 [ixNet getList $dev2 ethernet]

puts "Step 7  -> Add ipv4 to device group"
ixNet add $mac1 ipv4
ixNet add $mac2 ipv4
ixNet commit

set ip1 [ixNet getList $mac1 ipv4]
set ip2 [ixNet getList $mac2 ipv4]

puts "Step 8 -> Add virtual ports to topology"
set tPort1 [lindex [ixNet getList $topo1 port] 0]
set tPort2 [lindex [ixNet getList $topo2 port] 0]

ixNet setAttr $topo1 -vports $vport1
ixNet setAttr $topo2 -vports $vport2
ixNet commit

puts "Step 9 -> Setting multiple values for ipv4 addresse"
ixNet  setMultiAttr [ixNet getAttr $ip1 -address]/counter -start 192.168.1.2 -step 0.0.0.1 -direction increment
ixNet  setMultiAttr [ixNet getAttr $ip2 -address]/counter -start 192.168.2.2 -step 0.0.0.1 -direction increment
ixNet  setMultiAttr [ixNet getAttr $ip1 -gatewayIp]/counter -start 192.168.2.2 -step 0.0.0.1 -direction increment
ixNet  setMultiAttr [ixNet getAttr $ip2 -gatewayIp]/counter -start 192.168.1.2 -step 0.0.0.1 -direction increment
ixNet  setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet  setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

puts "Wait 5 sec"
after 5000

puts "Step 10 -> Creating Traffic Item"
set trafficItem [ixNet add /traffic trafficItem]
ixNet setMultiAttribute $trafficItem \-name "RFC2544Traffic" \-roundRobinPacketOrdering false \-routeMesh oneToOne \-trafficType ipv4\

set endpointSet [ixNet add $trafficItem endpointSet]
ixNet setMultiAttribute $endpointSet \-sources $topo1 \-destinations $topo2
ixNet setMultiAttribute $trafficItem /tracking \-trackBy [list flowGroup0 trackingenabled0] 
ixNet commit

puts "Step 11  -> Creating QT"
set test [ixNet add /quickTest "rfc2544throughput"]
ixNet commit

set test [lindex [ixNet remapIds $test] 0]
ixNet setMultiAttribute $test/testConfig \-frameSizeMode fixed \-loadType unchanged \-imixTrafficType UNCHANGED 
	
set trafficSelection [ixNet add $test "trafficSelection"]
ixNet setMultiAttribute $trafficSelection \-id $trafficItem \-isGenerated false
ixNet commit

################################################################################
# Assign ports 
################################################################################
set vPorts [ixNet getList [ixNet getRoot] vport]
puts "Step 12 -> Assigning ports to $vPorts"
::ixTclNet::AssignPorts $py::ports {} $vPorts force
puts "Done"

################################################################################
# Start All Protocols
################################################################################
puts "Step 13 -> Starting All Protocols"
ixNet exec startAllProtocols
puts "Wait 10sec for protocols to start"
after 10000

################################################################################
# Apply QT
################################################################################
puts "Step 14 -> Apply QT"
ixNet execute apply $test

################################################################################
# Run QT and Run Progress
################################################################################
puts "Step 15 -> Starting QT"
if {[catch {ixNet exec start $test} errMsg ]} {
    error "start QT failed : $errMsg"
    return $FAILED
}
while {true} {

	set progress [ixNet getA $test/results -progress]
	if { [string length $progress ] > 3 } {
	    puts $progress  
	}
	after 5000
	if {[ixNet getA $test/results -isRunning] == "false"} {
	    break
	}
    }
puts "Test Finished"

################################################################################
#Test run status 
################################################################################
puts "Step 16 -> Test run status"

if {[ixNet getA $test/results -result] == "fail"} {
    puts "The test has failed !"
    return $FAILED
    } else {
	puts "The test has passed"
	}


################################################################################
#Cleaning up the client 
################################################################################
puts "Step 17 -> Cleaning up the client: "
puts " -> Stopping protocols"
ixNet exec stop $test

after 5000

puts "->Performing New Config"
ixNet exec newConfig
    
################################################################################
# TEST END
################################################################################