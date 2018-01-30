#!/usr/bin/tclsh

# Description
#
#    Version 1.0 - Aug-7-2013 By Hubert Gee: hgee@ixiacom.com
#        - destIp list
#        - incr 2nd octet network address
# 
#    Version 2.0 - Sep-18-2013
#        - added srcIp list
#        - incr 2nd octet network addresses and 4th octet host ip addresses.
#
#    Traffic Items are all configured on the IxNet gui.
#    Has to be RAW type in order to set the ipList on the srcIp/dstIp header.
#    This script will create a list of unique srcIp/dstIp network octets and host addresses.
#    on the dstIp packet header.
#

package req IxTclNetwork

# User must change all of these values accordingly
set ixChassisIp 10.205.4.35
set ixNetworkTclServer 10.205.1.42
set ixNetworkVersion 7.12
set ixNetPort 8009

#TrafficItemName,FlowNumber,TotalUniqueNetworks,TotalUniqueIpHosts
#----------------------------------------------------------------
# Example:
#    "My Traffic Item 1",1,250,100 = TrafficItem1 Flow1
#    "My Traffic Item 1",2,250,100 = TrafficItem1 Flow2
#    "My Traffic Item 1",3,250,100 = TrafficItem1 Flow3
#
#    "My Traffic Item 1" = The name of the Traffic Item in double quotes.
#    1 = The flow number
#    250 = Total number of unique network IP address on the 2nd octet.
#    100 = Total number of unique IP hosts on the 4th octet.
#

set trafficItem1Name "To BGP Raw 2"

set trafficItemList($trafficItem1Name,dstIp,1,250,100) "1.1.1.1 2.1.1.1 3.1.1.1"
set trafficItemList($trafficItem1Name,srcIp,1,250,100) "10.1.1.1 20.1.1.1 30.1.1.1"

# Connect to the IxNetwork Tcl server
ixNet connect $ixNetworkTclServer -port $ixNetPort -version $ixNetworkVersion
set root [ixNet getRoot]

foreach {properties ip} [array get trafficItemList *] {
    # To BGP Raw,destIp,2,1,3,5 : ip: 1.1.1.1 2.1.1.1 3.1.1.1
    # To BGP Raw,srcIp,2,1,3,5 : ip: 1.1.1.1 2.1.1.1 3.1.1.1
    set definedTiName  [lindex [split $properties ,] 0]
    set ipHeader       [lindex [split $properties ,] 1]
    set flowNumber     [lindex [split $properties ,] 2]
    set totalNetworkIp [lindex [split $properties ,] 3]
    set totalHostIp    [lindex [split $properties ,] end]

    # Using foreach to loop through every Traffic Item to get the user defined name
    foreach trafficItem [ixNet getList $root/traffic trafficItem] {
	set currentTrafficItemName [ixNet getAttribute $trafficItem -name]

	if {$currentTrafficItemName == $definedTiName} {
	    set currentFlowNumber 0

	    puts "\nConfiguring TrafficItemName: \"$currentTrafficItemName\" : $ipHeader\n"
	    
	    # Each Traffic Item can have man Flows.
	    # Using foreach to loop through each Flow in the same Traffic Item
	    foreach highLevelStream [ixNet getList $trafficItem highLevelStream] {
		set ipList {}
		incr currentFlowNumber

		# Build the list of IP addresses.
		# Customer provides the starting point for each IP address, 
		# and this piece of code will increment the 2nd octet up the the total
		# amount specified by the user:  Example: trafficItem(1,2,250) <-- 250 is total
		if {$currentFlowNumber == $flowNumber} {
		    foreach ipAddress $ip {
			set 1stOctet [lindex [split $ipAddress .] 0]
			set 2ndOctet [lindex [split $ipAddress .] 1]
			set 3rdOctet [lindex [split $ipAddress .] 2]
			set 4thOctet [lindex [split $ipAddress .] 3]
			set totalNetworkIpFromPrefix [expr $2ndOctet + $totalNetworkIp]
			set startHostIp              $4thOctet
			set endHostIp                [expr $4thOctet + [expr $totalHostIp - 1]]
			
			# set trafficItemList($trafficItem1Name,2,1,5,3) "1.1.1.1 2.1.1.1 3.1.1.1"
			set hostIp $startHostIp

			for {set ipNum $2ndOctet} {$ipNum < $totalNetworkIpFromPrefix} {incr ipNum} {
			    # Increment the 2nd octet network address and increment
			    # the last octet host ip address.
			    
			    set flag 0
			    lappend ipList $1stOctet.$ipNum.$3rdOctet.$hostIp
			    
			    if {$hostIp == $endHostIp} {
				set hostIp $startHostIp
				set flag 1
			    }
			    
			    if {$flag == 0} {
				incr hostIp
			    }
			}
		    }

		    # Parsing out the IPv4 header from the current Flow
		    set ipv4Index [lsearch -regexp [ixNet getList $highLevelStream stack] ipv4]
		    set ipv4Stack [lindex [ixNet getList $highLevelStream stack] $ipv4Index]
		    # ipHeader == dstIp or srcIp
		    set ipv4StackFieldIndex [lsearch -regexp [ixNet getList $ipv4Stack field] $ipHeader]
		    
		    # This is the complete API object to configure this current Flow
		    # ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"ipv4-2"/field:"ipv4.header.dstIp-28"
		    set ipv4StackIpField [lindex [ixNet getList $ipv4Stack field] $ipv4StackFieldIndex]
		    
		    puts "\tFlow: $ipv4StackIpField"
		    ixNet setMultiAttribute $ipv4StackIpField \
			-fieldValue 0.0.0.0 \
			-fixedBits 0.0.0.0 \
			-optionalEnabled true \
			-randomMask 0.0.0.0 \
			-seed 1 \
			-singleValue 0.0.0.0 \
			-startValue 0.0.0.0 \
			-stepValue 0.0.0.0 \
			-valueList "$ipList" \
			-valueType valueList
		}
	    }
	    # Write the configuration to hardware
	    ixNet commit
	    after 1000
	}
    }
}

