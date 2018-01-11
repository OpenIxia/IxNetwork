#!/usr/bin/tclsh

package req Ixia

set ixiaChassisIp 10.219.117.101
set ixNetworkTclServerIp 10.219.117.103
set userName hgee
set portList "1/1 1/2"
set port1 1/1/1
set port2 1/1/2

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
		       -port_list $portList \
		       -ixnetwork_tcl_server $ixNetworkTclServerIp \
		       -tcl_server $ixiaChassisIp \
		       -username $userName \
		  ]

if {[keylget connectStatus status] != $::SUCCESS} {
    puts "Connecting to ixNetwork Tcl server failed\n\n$connectStatus\n"
    exit
} 

# This is just another way to build a list of IP addresses.
# Uncomment to demo. Otherwise, leave it commented out.
if 0 {
    set ip 0
    set totalInterface 1
    set startingVlandId 0
    
    for {set interface 1} {$interface <= $totalInterface} {incr interface} {
	lappend int1PortList $port1
	lappend int1IpAddressList 1.1.1.[incr ip]
	lappend int1GatewayList 1.1.1.254
	lappend int1NetMaskList 255.255.255.0
	
	set macLast2Bytes [format %04x $interface]
	set original [string index $macLast2Bytes 2]
	set macLast2Bytes [string replace $macLast2Bytes 2 2 :$original]
	
	lappend int1SrcMacList 00:01:01:01:$macLast2Bytes
	lappend int1VlanIdList [incr startingVlanId]
    }
    
    set port1Status [::ixia::interface_config \
			 -mode config \
			 -port_handle [list $int1PortList] \
			 -intf_ip_addr [list $int1IpAddressList] \
			 -gateway [list $int1GatewayList] \
			 -netmask [list $int1NetMaskList] \
			 -src_mac_addr [list $int1SrcMacList] \
			]
}

set port1Status [::ixia::interface_config \
		     -mode config \
		     -port_handle $port1 \
		     -intf_ip_addr 1.1.1.1 \
		     -intf_ip_addr_step 0.0.0.1 \
		     -connected_count 10 \
		     -gateway 1.1.1.11 \
		     -gateway_step 0.0.0.1 \
		     -netmask 255.255.255.0 \
		     -src_mac_addr 00:01:01:01:00:01 \
		     -src_mac_addr_step 0000.0000.0001 \
		     -vlan 1 \
		     -vlan_id 103 \
		     -vlan_id_step 1 \
		     -vlan_id_count 10 \
		    ]

set port1Interface [keylget port1Status interface_handle]

set port2Status [::ixia::interface_config \
		     -mode config \
		     -port_handle $port2 \
		     -intf_ip_addr 1.1.1.11 \
		     -intf_ip_addr_step 0.0.0.1 \
		     -connected_count 10 \
		     -gateway 1.1.1.1 \
		     -gateway_step 0.0.0.1 \
		     -netmask 255.255.255.0 \
		     -src_mac_addr 00:01:01:02:00:01 \
		     -src_mac_addr_step 0000.0000.0001 \
		     -vlan 1 \
		     -vlan_id 103 \
		     -vlan_id_step 1 \
		     -vlan_id_count 10 \
		    ]

set port2Interface [keylget port2Status interface_handle]

# port1Interface = ::ixNet::OBJ-/vport:1/interface:1
# port2Interfaces = ::ixNet::OBJ-/vport:2/interface:1 

puts "\nSending ARP ..."
set port1ArpStatus [::ixia::interface_config -port_handle $port1 -arp_send_req 1 -arp_req_retries 3]
set port2ArpStatus [::ixia::interface_config -port_handle $port2 -arp_send_req 1 -arp_req_retries 3]
puts "\nport1ArpStatus: $port1ArpStatus"
puts "\nport2ArpStatus: $port2ArpStatus"

# transmit_mode options: single_burst or continuous
set trafficItem1 [::ixia::traffic_config \
		      -mode create \
		      -emulation_src_handle $port1Interface \
		      -emulation_dst_handle $port2Interface \
		      -track_by  "traffic_item flowGroup0 " \
		      -name "TrafficItem_1" \
		      -bidirectional 1 \
		      -rate_percent 10 \
		      -pkts_per_burst 10000 \
		      -transmit_mode single_burst \
		      -frame_size 100 \
		      -transmit_distribution {srcDestEndpointPair0} \
		      -vlan enable \
		      -vlan_id 2 \
		      -vlan_user_priority 7 \
		      -l3_protocol ipv4 \
		      -l4_protocol udp \
		      -udp_src_port 1050 \
		      -udp_dst_port 1004 \
		     ]

puts "\nStarting IxNetwork traffic ..."
set trafficControlStatus [ixia::traffic_control \
			      -port_handle $port1 \
			      -action run \
			     ]
if {[keylget trafficControlStatus status] != $::SUCCESS} {
    puts "\nIxia traffic failed to start on port $portList"
} else {
    puts "\nTraffic started on port $portList"
}

# Wait 10 seconds and collect stats
after 10000

set flowStats [::ixia::traffic_stats \
		   -mode flow \
	      ]
if {[keylget flowStats status] != $::SUCCESS} {
    puts "Failed to get statistics"
    exit
}

puts \n
puts "[format %-10s FlowGroup][format %10s TxPort][format %10s RxPort][format %14s TxFrames][format %14s RxFrames]"
puts "------------------------------------------------------------------------"

for {set flowNumber 1} {$flowNumber <= [llength [keylget flowStats flow]]} {incr flowNumber} {
    set txPort [keylget flowStats flow.$flowNumber.tx.port]
    set rxPort [keylget flowStats flow.$flowNumber.rx.port]
    set txFrames [keylget flowStats flow.$flowNumber.tx.total_pkts]
    set rxFrames [keylget flowStats flow.$flowNumber.rx.total_pkts]
    
    # flow_name: 1/1/2 TI0-TrafficItem_1 1.1.1.6 TI0-TrafficItem_1-EndpointSet-1 - Flow Group 0001
    set flowName [keylget flowStats flow.$flowNumber.flow_name]
  
    puts "[format %5s $flowNumber][format %15s $txPort][format %10s $rxPort][format %14s $txFrames][format %14s $rxFrames]"
}

puts \n
