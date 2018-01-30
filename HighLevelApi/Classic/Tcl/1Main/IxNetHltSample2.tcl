#!/usr/bin/tclsh

package req Ixia

set ixiaChassisIp 10.219.117.101
set ixNetworkTclServerIp 10.219.117.103
set portList "1/1 1/2"
set port1 1/1/1
set port2 1/1/2
set userName hgee

proc GetTime {} {
    return [clock format [clock seconds] -format "%H:%M:%S"]
}

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

if {[VerifyPortState]} {
    exit
}

set port1Status [::ixia::interface_config \
		     -mode config \
		     -port_handle $port1 \
		     -intf_ip_addr 1.1.1.1 \
		     -gateway 1.1.1.2 \
		     -netmask 255.255.255.0 \
		     -src_mac_addr 00:01:01:01:00:01 \
		    ]

puts "\nport1Status: $port1Status ---"

set port1Interface [keylget port1Status interface_handle]


set port2Status [::ixia::interface_config \
		     -mode config \
		     -port_handle $port2 \
		     -intf_ip_addr 1.1.1.2 \
		     -gateway 1.1.1.1 \
		     -netmask 255.255.255.0 \
		     -src_mac_addr 00:01:01:02:00:02 \
		    ]

set port2Interface [keylget port2Status interface_handle]

# port1Interface = ::ixNet::OBJ-/vport:1/interface:1
# port2Interface = ::ixNet::OBJ-/vport:2/interface:1

after 3000

set port1ArpStatus [::ixia::interface_config -port_handle $port1 -arp_send_req 1 -arp_req_retries 3]
set port2ArpStatus [::ixia::interface_config -port_handle $port2 -arp_send_req 1 -arp_req_retries 3]
puts "\nport1ArpStatus: $port1ArpStatus"
puts "\nport2ArpStatus: $port2ArpStatus"

# -track_by  "traffic_item flowGroup0"
# transmit_mode options: single_burst or continuous

set startTime [GetTime]

for {set number 1} {$number <= 1} {incr number} {
    puts "\nStart creating Traffic Item #$number: [GetTime]"
    set trafficItem1 [::ixia::traffic_config \
			  -mode create \
			  -emulation_src_handle $port1Interface \
			  -emulation_dst_handle $port2Interface \
			  -track_by  "traffic_item flowGroup0" \
			  -name "TrafficItem_$number" \
			  -bidirectional 0 \
			  -rate_percent 100 \
			  -pkts_per_burst 1000 \
			  -transmit_mode single_burst \
			  -frame_size 100 \
			  -ip_precedence 2 \
			  -vlan disable \
			  -vlan_id 2 \
			  -vlan_user_priority 7 \
			  -l3_protocol ipv4 \
			  -l4_protocol udp \
			  -udp_src_port 1050 \
			  -udp_dst_port 1004 \
			 ]
    puts "Done creating Traffic Item #$number: [GetTime]"
}

puts "\ntrafficItem1:\n\n[KeylPrint trafficItem1]\n\n"

puts "\nStarting IxNetwork traffic ..."
set trafficControlStatus [ixia::traffic_control \
			      -action run \
			     ]
if {[keylget trafficControlStatus status] != $::SUCCESS} {
    puts "\nIxia traffic failed to start on port $portList"
} else {
    puts "\nTraffic started on port $portList"
}

puts "\nTraffic started. Sleep 10 seconds ..."
after 10000

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

puts "\nGetting stats ..."
set flowStats [::ixia::traffic_stats \
		   -mode flow
	      ]
if {[keylget flowStats status] != $::SUCCESS} {
    puts "Failed to get statistics"
    exit
}

puts [KeylPrint flowStats]
#exit

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
