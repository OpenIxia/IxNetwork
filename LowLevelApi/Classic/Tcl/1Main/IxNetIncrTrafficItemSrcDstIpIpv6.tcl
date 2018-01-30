#!/usr/bin/tclsh

# Description
#    Use ixncfg config file: 131018_TME_DT_Terastream_buffer_HubertEdited01.ixncfg
#
#    Add a header to an existing traffic item

package req IxTclNetwork

# User must change all of these values accordingly
set ixChassisIp 10.205.4.172
set ixNetworkTclServer 10.205.1.42
set ixNetworkVersion 7.12
set ixNetPort 8009

# hex to decimal = expr 0x$hex
# decimal to hex = format "%x" $decimal
#
# 1> expr 225 / 50 = 4
# 2> expr fmod(225,50) = 25.0  <- remainders

# Create a list of all the Traffic Items to configure
set trafficItemList { {50pkt_6250bytes_PG Raw (1)} }
set currentIpv6Addr 2003:1408:120:200:0:0:0:0

set totalSubnetsOn3rdOctet 20
set totalSubnetsOn4thOctet 250 ;# increment by 100 starting at 200
set totalHostIp 50
set totalTxHostPackets 625

set 1stOctet [lindex [split $currentIpv6Addr :] 0]
set 2ndOctet [lindex [split $currentIpv6Addr :] 1]
set 3rdOctet [lindex [split $currentIpv6Addr :] 2]

set 4thOctet [lindex [split $currentIpv6Addr :] 3]
set 4thOctet1stByte [string index $4thOctet 0]
set 4thOctet2ndByte [string range $4thOctet 1 end]

set 5thOctet [lindex [split $currentIpv6Addr :] 4]
set 6thOctet [lindex [split $currentIpv6Addr :] 5]
set 7thOctet [lindex [split $currentIpv6Addr :] 6]
set 8thOctet [lindex [split $currentIpv6Addr :] 7]

set 3rdSub $3rdOctet
set 4thSub $4thOctet1stByte

set totalLoops [expr [expr $totalTxHostPackets / $totalHostIp] - 1]
set totalHosts $totalTxHostPackets

set ipList {}
for {set 3rdNum 1} {$3rdNum <= $totalSubnetsOn3rdOctet} {incr 3rdNum} {
    for {set 4thNum 1} {$4thNum <= $totalSubnetsOn4thOctet} {incr 4thNum} {

	set flag 0
	for {set hostIp 1} {$hostIp <= $totalHosts} {incr hostIp} {
	    # totalTxHostPackets / totalHostIp
	    #    1> expr 225 / 50 = 4
	    #
	    # totalTxHostPackets,$totalHostIp
	    #    2> expr fmod(225,50) = 25.0  <- remainders

	    if {$flag == 0} {
		set ipAddr $1stOctet:$2ndOctet:$3rdSub:$4thSub$4thOctet2ndByte:$5thOctet:$6thOctet:$7thOctet:$hostIp
		puts "Appending IP: $ipAddr"
		lappend ipList $ipAddr
	    }

	    if {$hostIp == $totalHostIp && $totalLoops != 0} {
		incr totalLoops -1
		set hostIp 0
	    }

	    if {$hostIp == $totalHostIp && $totalLoops == 0} {
		set totalHosts2 [expr fmod($totalTxHostPackets,$totalHostIp)]
		set totalHosts2 [format %.0f $totalHosts2]

		# Add the remainding hosts from fmod
		for {set hostIp2 1} {$hostIp2 <= $totalHosts2} {incr hostIp2} {
		    set ipAddr $1stOctet:$2ndOctet:$3rdSub:$4thSub$4thOctet2ndByte:$5thOctet:$6thOctet:$7thOctet:$hostIp2
		    puts "Appending IP: $ipAddr"
		    lappend ipList $ipAddr
		}
		set totalHosts $totalTxHostPackets
		set totalLoops [expr [expr $totalTxHostPackets / $totalHostIp] - 1]
		set flag 1
	    }
	}

	set decimal [expr 0x$4thSub] ;# Convert hex to decimal
	incr decimal
	set hex [format "%x" $decimal] ;# Convert decimal to hex
	set 4thSub $hex

	if {$4thNum == $totalSubnetsOn4thOctet} {
	    set 4thSub $4thOctet1stByte
	}
    }

    set 3rdSub [expr 0x$3rdSub]
    incr 3rdSub
    set 3rdSub [format "%x" $3rdSub]
}

# Connect to the IxNetwork Tcl server
ixNet connect $ixNetworkTclServer -port $ixNetPort -version $ixNetworkVersion
set root [ixNet getRoot]

foreach trafficItem [ixNet getList $root/traffic trafficItem] {
    set currentTrafficItemName [ixNet getAttribute $trafficItem -name]
    if {[lsearch $trafficItemList $currentTrafficItemName] != -1} {

	puts "\nConfiguring TrafficItemName: \"$currentTrafficItemName\"\n"

	# Each Traffic Item can have many Flows.
	# Using foreach to loop through each Flow in the same Traffic Item
	set configElement $trafficItem/configElement:1

	# Parsing out the IPv6 header from the current Flow
	set ipv6Index [lsearch -regexp [ixNet getList $configElement stack] ipv6]
	
	# ipv6Stack: ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ipv6-2"
	set ipv6Stack [lindex [ixNet getList $configElement stack] $ipv6Index]
	
	# ipHeader == dstIP or srcIP
	# ipv6StackFieldIndex: 7
	set ipv6StackFieldIndex [lsearch -regexp [ixNet getList $ipv6Stack field] dstIP]
	
	# This is the complete API object to configure this current Flow
	# ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ipv6-2"/field:"ipv6.header.dstIP-8"
	set ipv6StackIpField [lindex [ixNet getList $ipv6Stack field] $ipv6StackFieldIndex]

	puts "\tFlow: $ipv6StackIpField"
	ixNet setMultiAttribute $ipv6StackIpField \
	    -fieldValue 0::0 \
	    -fixedBits 0::0 \
	    -optionalEnabled true \
	    -randomMask 0::0 \
	    -seed 1 \
	    -singleValue 0::0 \
	    -startValue 0::0 \
	    -stepValue 0::0 \
	    -valueList $ipList \
	    -valueType valueList
	
	# Write the configuration to hardware
	ixNet commit

	ixNet exec generate $trafficItem

	}
    }
}

