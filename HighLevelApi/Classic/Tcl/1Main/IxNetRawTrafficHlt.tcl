#!/usr/bin/tclsh

# Author: Hubert Gee
# 
# Sample script on how to use HLT to create a raw Traffic Items
# and customize the sequential order of the packet header.

package req Ixia 

set ixiaChassisIp 10.219.117.101
set ixNetworkTclServerIp 10.219.117.103
set portList "1/1 1/2"
set port1 1/1/1
set port2 1/1/2
set userName hgee

proc VerifyPortState { {portList all} {expectedPortState up} } {
    # portList format = 1/2.  Not 1/1/2

    puts "\nVerifyPortState ...\n"
    #after 5000
    set allVports [ixNet getList [ixNet getRoot] vport]

    if {$portList == "all"} {
	set vPortList $allVports
    }

    if {$portList != "all"} {
	# Search out the user defined $portList
	set vPortList {}
	foreach vport $allVports {
	    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
	    set connectedTo [ixNet getAttribute $vport -connectedTo]
	    set connectedTo [lrange [split $connectedTo /] 3 4]
	    set card [lindex [split [lindex $connectedTo 0] :] end]
	    set port [lindex [split [lindex $connectedTo 1] :] end]
	    set port $card/$port

	    if {[lsearch $portList $port] != -1} { 
		lappend vPortList $vport
	    }
	}
    }

    set portsAllUpFlag 0

    foreach vport $vPortList {
	for {set timer 0} {$timer <= 60} {incr timer 2} {
	    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
	    set connectedTo [ixNet getAttribute $vport -connectedTo]
	    set connectedTo [lrange [split $connectedTo /] 3 4]
	    set card [lindex [split [lindex $connectedTo 0] :] end]
	    set port [lindex [split [lindex $connectedTo 1] :] end]
	    set port $card/$port
	    
	    set portState [ixNet getAttribute $vport -state]

	    # Expecting port state = UP
	    if {$expectedPortState == "up"} {
		if {$portState != "up" && $timer != "60"} {
		    puts "VerifyPortState: $port is still $portState. Expecting port up. $timer/60 seconds."
		    after 2000
		    continue
		}
		
		if {$portState != "up" && $timer == "60"} {
		    puts "\nError VerifyPortState: $port seem to be stuck on $portState state. Expecting port up.\n"
		    set portsAllUpFlag 1
		}
		
		if {$portState == "up"} {
		    puts "\nVerifyPortState: $port state is $portState"
		    break
		}
	    }

	    # Expecting port state = Down
	    if {$expectedPortState == "down"} {
		if {$portState != "down" && $timer != "60"} {
		    puts "\nVerifyPortState: $port is still $portState. Expecting port down. $timer/60 seconds."
		    after 2000
		    continue
		}
		
		if {$portState == "up" && $timer == "60"} {
		    puts "\nError VerifyPortState: $port seem to be stuck on the $portState state. Expecting port down."
		    set portsAllUpFlag 1
		}
		
		if {$portState == "down"} {
		    puts "\nVerifyPortState: $port state is $portState as expected"
		    break
		}
	    }
	}
    }

    if {$portsAllUpFlag == 1} {
	return 1
    } else {
	after 3000
	return 0
    }
}

proc RegenerateAllTrafficItems {} {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	catch {ixNet exec generate $trafficItem} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError RegenerateAllTrafficItems: Failed on $trafficItem"
	    return 1
	}
	puts "\nRegenerateAllTrafficItems: $trafficItem"
    }
    puts "RegenerateAllTrafficItems: Done"
    return 0
}

proc KeylPrint {keylist {space ""}} {
    upvar $keylist kl
    set result ""
    foreach key [keylkeys kl] {
	set value [keylget kl $key]
	if {[catch {keylkeys value}]} {
	    append result "$space$key: $value\n"
	} else {
	    set newspace "$space "
	    append result "$space$key:\n[KeylPrint value $newspace]"
	}
    }
    return $result
}

puts "\nConnecting to $ixNetworkTclServerIp ..."
puts "Rebooting ports $portList ..."
set connectStatus [::ixia::connect \
		       -reset \
		       -device $ixiaChassisIp \
		       -ixnetwork_tcl_server $ixNetworkTclServerIp \
		       -tcl_server $ixiaChassisIp \
		       -port_list $portList \
		       -break_locks 1 \
		       -username $userName
		  ]
if {[keylget connectStatus status] != $::SUCCESS} {
    puts "Connecting to ixNetwork Tcl server failed\n\n$connectStatus\n"
    exit
} 

puts [KeylPrint connectStatus]

set port1Int [lindex [keylget connectStatus vport_protocols_handle] 0]
set port2Int [lindex [keylget connectStatus vport_protocols_handle] 1]

if {[VerifyPortState]} {
    exit
}

set port1Status [::ixia::interface_config  \
		  -mode config \
		  -port_handle $port1 \
		  -phy_mode copper \
		 ]
puts [KeylPrint port1Status]

set port2Status [::ixia::interface_config  \
		  -mode config \
		  -port_handle $port2 \
		  -phy_mode copper \
		 ]

set trafficItemStatus [::ixia::traffic_config  \
			   -mode create \
			   -circuit_type raw \
			   -name Traffic_Item_1 \
			   -endpointset_count 1 \
			   -emulation_src_handle [list [list $port1Int]] \
			   -emulation_dst_handle [list [list $port2Int]] \
			   -src_dest_mesh one_to_one \
			   -route_mesh one_to_one \
			   -bidirectional 0 \
			   -rate_percent 100 \
			   -pkts_per_burst 1000 \
			   -transmit_mode single_burst \
			   -frame_size 100 \
			  ]

# ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1
set configElement [keylget trafficItemStatus traffic_item]

# ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ethernet-1"
set ethernetHeaderObj [lindex [keylget trafficItemStatus $configElement.headers] 0]

set trafficStatus2 [::ixia::traffic_config  \
		  -mode modify \
		  -stream_id $ethernetHeaderObj \
		  -l2_encap ethernet_ii \
		  -mac_dst_mode fixed \
		  -mac_dst_tracking 0 \
		  -mac_dst 00:22:22:22:22:22 \
		  -mac_src_mode fixed \
		  -mac_src_tracking 0 \
		  -mac_src 00:11:11:11:11:11 \
		 ]

puts [KeylPrint trafficStatus2]

# headers: ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ethernet-1"
#          ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"fcs-2"
set ethernetHeaderObj [lindex [keylget trafficStatus2 $configElement.headers] 0]

# Insert the Vlan header after the ethernetHeaderObj (ethernet header)
set trafficStatus3 [::ixia::traffic_config  \
			-mode append_header \
			-stream_id $ethernetHeaderObj \
			-vlan enable \
			-vlan_user_priority_mode fixed \
			-vlan_user_priority 7 \
			-vlan_user_priority_tracking 0 \
			-vlan_id 107 \
			-vlan_id_tracking 0 \
		       ]

# headers: ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ethernet-1"
#          ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"vlan-2"
#          ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"fcs-3"
puts [KeylPrint trafficStatus3]

# Get the Vlan header object and insert IPv4 after the Vlan header.
set vlanHeaderObj [lindex [keylget trafficStatus3 $configElement.headers] 1]

set trafficStatus4 [::ixia::traffic_config  \
		  -mode append_header \
		  -stream_id $vlanHeaderObj \
		  -l3_protocol ipv4 \
		  -qos_type_ixn tos \
		  -ip_precedence_mode fixed \
		  -ip_precedence 0 \
		  -ip_src_mode fixed \
		  -ip_src_addr 10.10.10.1 \
		  -ip_src_tracking 0 \
		  -ip_dst_mode fixed \
		  -ip_dst_addr 10.10.10.2 \
		  -ip_dst_tracking 0 \
		  -track_by {flowGroup0 trackingenabled0} \
		  -egress_tracking none \
		 ]

# headers: ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ethernet-1"
#          ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"vlan-2"
#          ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ipv4-3"
#          ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"fcs-4"
puts [KeylPrint trafficStatus4]

# Get the IPv4 header object and insert it after the Vlan header.
set ipv4Obj [lindex [keylget trafficStatus4 $configElement.headers] 2]

set trafficStatus5 [::ixia::traffic_config  \
		  -mode append_header \
		  -stream_id $ipv4Obj \
		  -l3_protocol ipv6 \
		  -ipv6_flow_version_mode fixed \
		  -ipv6_flow_version 6 \
		  -ipv6_flow_version_tracking 0 \
		  -ipv6_traffic_class_mode fixed \
		  -ipv6_traffic_class 0 \
		  -ipv6_traffic_class_tracking 0 \
		  -ipv6_flow_label_mode fixed \
		  -ipv6_flow_label 0 \
		  -ipv6_flow_label_tracking 0 \
		  -ipv6_hop_limit_mode fixed \
		  -ipv6_hop_limit 64 \
		  -ipv6_hop_limit_tracking 0 \
		  -ipv6_src_mode fixed \
		  -ipv6_src_addr 0:0:0:0:0:0:0:0 \
		  -ipv6_src_tracking 0 \
		  -ipv6_dst_mode fixed \
		  -ipv6_dst_addr 0:0:0:0:0:0:0:0 \
		  -ipv6_dst_tracking 0 \
		 ]

puts [KeylPrint trafficStatus5]

# Get the IPv6 header object and insert it after the ipv4 header.
set ipv6Obj [lindex [keylget trafficStatus5 $configElement.headers] 3]

set trafficStatus6 [::ixia::traffic_config  \
			-mode append_header \
			-stream_id $ipv6Obj \
			-l4_protocol tcp \
			-tcp_src_port_mode fixed \
			-tcp_src_port 1005 \
			-tcp_src_port_tracking 0 \
			-tcp_dst_port_mode fixed \
			-tcp_dst_port 1006 \
			-track_by {flowGroup0 trackingenabled0} \
		       ]

# Get the ipv6 header object and insert it after the tcp header.
set tcpObj [lindex [keylget trafficStatus6 $configElement.headers] 4]

set trafficStatus7 [::ixia::traffic_config  \
			-mode append_header \
			-stream_id $tcpObj \
			-l4_protocol udp \
			-udp_src_port_mode fixed \
			-udp_src_port 1003 \
			-udp_src_port_tracking 0 \
			-udp_dst_port_mode fixed \
			-udp_dst_port 1004 \
			-udp_dst_port_tracking 0 \
		       ]

puts [KeylPrint trafficStatus7]
#  headers: ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ethernet-1"
#           ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"vlan-2"
#           ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ipv4-3"
#           ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ipv6-4"
#           ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"tcp-5"
#           ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"udp-6"
#           ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"fcs-7"

RegenerateAllTrafficItems

puts "\nStarting IxNetwork traffic ..."
set trafficControlStatus [ixia::traffic_control \
			      -action run \
			     ]
if {[keylget trafficControlStatus status] != $::SUCCESS} {
    puts "\nIxia traffic failed to start on port $portList"
} else {
    puts "\nTraffic started on port $portList"
}

puts "\nTraffic started. Sleep 5 seconds ..."
after 5000

puts "\nGetting stats ..."
set flowStats [::ixia::traffic_stats \
		   -mode flow
	      ]
if {[keylget flowStats status] != $::SUCCESS} {
    puts "Failed to get statistics"
    exit
}

puts [KeylPrint flowStats]

# The below code shows how to retreive statistics that matters
# to you for passed/failed criteria.
for {set flowNumber 1} {$flowNumber <= [llength [keylget flowStats flow]]} {incr flowNumber} {
    set txPort [keylget flowStats flow.$flowNumber.tx.port]
    set rxPort [keylget flowStats flow.$flowNumber.rx.port]
    set txFrames [keylget flowStats flow.$flowNumber.tx.total_pkts]
    set rxFrames [keylget flowStats flow.$flowNumber.rx.total_pkts]
    set flowName [keylget flowStats flow.$flowNumber.flow_name]

    puts "\nFlow Group $flowNumber\:"
    puts "\t[format %8s TxPort][format %8s RxPort][format %12s TxFrames][format %12s RxFrames]"
    puts "\t--------------------------------------------"
    puts "\t[format %8s $txPort][format %8s $rxPort][format %12s $txFrames][format %12s $rxFrames]"
}

