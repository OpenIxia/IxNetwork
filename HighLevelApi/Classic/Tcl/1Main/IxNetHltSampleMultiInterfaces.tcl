#!/usr/bin/tclsh

# This sample script shows how to create multiple interfaces per port.
# You have to create a list of ports aligning to the rest of the list
# of parameters. For example:
#
#   -port_handle "1/1/1 1/1/1" 
#   -intf_ip_addr "1.1.1.1 1.1.1.2"
#   -gateway "1.1.1.3 1.1.1.4" 
#   -netmask "255.255.255.0 255.255.255.0" 
#   -src_mac_addr "00:01:01:01:00:01 00:01:01:01:00:02" 
#
# This example shows 2 interfaces per port.
# You have to create a list of -port_handle, -netmask and everything else.
# I suggest using a for loop.


package req Ixia

if 0 { 
set ixiaChassisIp 10.205.4.172
set ixNetworkTclServerIp 10.205.1.42
set userName hgee
set portList "1/1 1/2"
set port1 1/1/1
set port2 1/1/2
}
set ixiaChassisIp 10.10.10.2
set ixNetworkTclServerIp 10.10.10.2
set userName hgee
set portList "1/1 2/1"
set port1 1/1/1
set port2 1/2/1

#source /home/hgee/IxiaScripts/IxNet/HLT/NGPF/ixiaHltLib.tcl

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
		       -device               $ixiaChassisIp \
		       -ixnetwork_tcl_server $ixNetworkTclServerIp \
		       -tcl_server           $ixiaChassisIp \
		       -port_list            $portList \
		       -username             $userName
		  ]
if {[keylget connectStatus status] != $::SUCCESS} {
    puts "Connecting to ixNetwork Tcl server failed\n\n$connectStatus\n"
    exit
} 

puts "\nconnectStatus: $connectStatus"
# connectStatus: {port_handle {{10 {{205 {{4 {{172 {{1/1 1/1/1} {1/2 1/1/2}}}}}}}}}}} {connection {{using_tcl_proxy 0} {server_version 7.12.850.46} {port 8009} {username IxNetwork/hgee-winPc2/hgee} {hostname hgee-winPc2}}} {vport_list {1/1/1 1/1/2}} {vport_protocols_handle {::ixNet::OBJ-/vport:1/protocols ::ixNet::OBJ-/vport:2/protocols}} {status 1}


set port1Status [::ixia::interface_config \
		     -mode config \
		     -port_handle "$port1 $port1" \
		     -intf_ip_addr "1.1.1.1 1.1.1.2" \
		     -gateway "1.1.1.3 1.1.1.4" \
		     -netmask "255.255.255.0 255.255.255.0" \
		     -src_mac_addr "00:01:01:01:00:01 00:01:01:01:00:02" \
		    ]

set port1Interface [keylget port1Status interface_handle]
puts "\nport1Interface: $port1Interface"
# port1Interface = ::ixNet::OBJ-/vport:1/interface:1 ::ixNet::OBJ-/vport:1/interface:2


set port2Status [::ixia::interface_config \
		     -mode config \
		     -port_handle "$port2 $port2" \
		     -intf_ip_addr "1.1.1.3 1.1.1.4"\
		     -gateway "1.1.1.1 1.1.1.2" \
		     -netmask "255.255.255.0 255.255.255.0" \
		     -src_mac_addr "00:01:01:02:00:01 00:01:01:02:00:02" \
		    ]
set port2Interface [keylget port2Status interface_handle]
puts "\nport2Interfaces: $port2Interface\n"

# port2Interface = ::ixNet::OBJ-/vport:2/interface:1 ::ixNet::OBJ-/vport:2/interface:2

#		      -src_dest_mesh fully \
#		      -track_by  "sourceDestEndpointPair0 vlanVlanId0"\ 
# transmit_mode options: single_burst or continuous
set trafficItem1 [::ixia::traffic_config \
		      -mode create \
		      -name "TrafficItem_1" \
		      -emulation_src_handle $port1Interface \
		      -emulation_dst_handle $port2Interface \
		      -track_by  "flowGroup0 sourceDestEndpointPair0" \
		      -bidirectional 0 \
		      -src_dest_mesh one_to_one \
		      -rate_percent 10 \
		      -pkts_per_burst 10000 \
		      -transmit_mode single_burst \
		      -frame_size 100 \
		      -ip_precedence 2 \
		      -vlan enable \
		      -vlan_id 2 \
		      -vlan_user_priority 7 \
		      -l3_protocol ipv4 \
		      -l4_protocol udp \
		      -udp_src_port 1050 \
		      -udp_dst_port 1004 \
		     ]

puts "\n[KeylPrint trafficItem1]"

puts "\nStarting IxNetwork traffic ..."
set trafficControlStatus [ixia::traffic_control \
			      -action run \
			     ]
if {[keylget trafficControlStatus status] != $::SUCCESS} {
    puts "\nIxia traffic failed to start on port $portList"
} else {
    puts "\nTraffic started on port $portList"
}

puts "Wait 5 seconds ..."
after 5000

if 0 {
set trafficControlStatus [ixia::traffic_control \
			      -action stop
			 ]
if {[keylget trafficControlStatus status] != $::SUCCESS} {
    puts "\nFailed to stop Ixia traffic on $portList"
} else {
    puts "\nIxia traffic stopped on $portList"
}

after 3000
}

puts "\nGetting flow statistics ..."
# -mode options: flow or traffic_item
set flowStats [::ixia::traffic_stats \
			     -mode flow \
			    ]
if {[keylget flowStats status] != $::SUCCESS} {
    puts "Failed to get statistics"
    exit
}

puts "\n[KeylPrint flowStats]"

puts "\nPort: [keylget flowStats flow.1.rx.port]"
puts "Rx: [keylget flowStats flow.1.rx.total_pkts]"

