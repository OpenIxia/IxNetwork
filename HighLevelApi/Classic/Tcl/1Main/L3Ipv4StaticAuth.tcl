#!/opt/ActiveTcl-8.5/bin/tclsh

# Example script by Hubert Gee
#  
# Insieme wants a way to scale 1000 hosts.
#    Incrementing srcIp, vlanId, srcMac.
# 
# This script will use Static IP w/Auth instead of Protocol Interface
# because this script doesn't involve protocols and scaling host
# through Protocol Interface takes a lot of resource.
#
# 
#
package req Ixia

set ixiaChassisIp 10.205.4.155
set ixNetworkTclServerIp 10.205.1.42
set userName hgee
set portList "1/1 1/2"

exec echo "" > ixiaHltDebug.txt
set ::ixia::logHltapiCommandsFlag 1
set ::ixia::logHltapiCommandsFileName ixiaHltDebug.txt

# -vlan_id outter,inner
set port1Config {
    -port_handle 1/1/1 
    -mode config -connected_count 10 
    -intf_ip_addr 1.1.1.1 
    -intf_ip_addr_step 0.0.0.1 
    -gateway 1.1.1.11 
    -gateway_step 0.0.0.0 
    -netmask 255.255.255.0 
    -l23_config_type static_endpoint 
    -qinq_incr_mode both 
    -vlan_id 301,101 
    -vlan_id_step 1,1 
    -vlan_id_count 10,10 
    -addresses_per_vlan 1,1 
    -vlan_user_priority 1,1 
    -vlan 1 -mtu 1500 
    -src_mac_addr 0001.0101.0001 
    -src_mac_addr_step 0000.0000.0001
}

set port2Config {
    -port_handle 1/1/2 
    -mode config 
    -connected_count 10 
    -intf_ip_addr 1.1.1.11 
    -intf_ip_addr_step 0.0.0.1 
    -gateway 1.1.1.1 
    -gateway_step 0.0.0.0 
    -netmask 255.255.255.0 
    -l23_config_type 
    static_endpoint 
    -qinq_incr_mode both 
    -vlan_id 301,101 
    -vlan_id_step 1,1 
    -vlan_id_count 10,10 
    -addresses_per_vlan 1,1 
    -vlan_user_priority 1,1 
    -vlan 1 
    -mtu 1500 
    -src_mac_addr 0001.0102.0001 
    -src_mac_addr_step 0000.0000.0001
}

proc ConnectToIxia { connectParams } {
    set connectStatus [eval ::ixia::connect $connectParams]

    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "\nError: ConnectToIxia failed: $connectStatus\n"
	exit
    } else {
	puts "\n$connectStatus\n"
	return 0
    }
}

proc ConfigInterfaceConfig { portConfigParams } {
    global portConfig

    set interfaceConfigStatus [eval ::ixia::interface_config $portConfigParams]
    
    if {[keylget interfaceConfigStatus status] != $::SUCCESS} {
	puts "\nError: interfaceConfigStatus failed:\n$interfaceConfigStatus\n"
    }

    # {interface_handle ::ixNet::OBJ-/vport:1/protocolStack/ethernet:\"a9bb5610-f95e-4a0f-9de7-19f12f8e5b34\"/ipEndpoint:\"036b9de0-5072-47cd-81c1-ec63932f4264\"/range:\"0e3ee6fa-3a1b-402c-956f-a67e73804de3\"} {status 1}
    # We want to parse out and return ::ixNet::OBJ-/vport:1/protocolStack.
    # For Traffic Item endpoint usage.
    set interfaceHandle [keylget interfaceConfigStatus interface_handle]
    if {[regexp "(::ixNet::OBJ-/vport:\[0-9]+/protocolStack)" $interfaceHandle - handle]} {
	return $handle
    }
}

proc CreateTrafficItem { trafficItemParams } {
    # For non-full-mesh: -src_dest_mesh one_to_one
    # for full-mesh:     -src_dest_mesh fully
    # -transmit_mode:    continuous | single_burst -number_of_packets-per_stream 50000
    set trafficItemStatus [eval ::ixia::traffic_config $trafficItemParams]

    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError: Traffic Item config failed: $trafficItemStatus\n"
	exit
    }
    return $trafficItemStatus
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

proc GetStatView { {getStatsBy trafficItem} } {
    set viewList [ixNet getList [ixNet getRoot]/statistics view]
    #puts "\nviewList: $viewList\n"

    set statViewSelection "Flow Statistics"

    set flowStatsViewIndex [lsearch -regexp $viewList $statViewSelection]
    if {$flowStatsViewIndex == -1} {
	puts "ViewStats: No \"$statViewSelection\" found"
	exit
    }

    # $view: ::ixNet::OBJ-/statistics/view:"Flow Statistics"
    set view [lindex $viewList $flowStatsViewIndex]

    ixNet setAttribute $view -enabled true
    ixNet commit

    set columnList [ixNet getAttribute ${view}/page -columnCaptions]
    puts "\n$columnList\n"

    set startTime 1
    set stopTime 30
    while {$startTime < $stopTime} {
	set totalPages [ixNet getAttribute $view/page -totalPages]
	if {[regexp -nocase "null" $totalPages]} {
	    puts "Getting total pages for $view is not ready. $startTime/$stopTime"
	    after 2000
	} else {
	    break
	}
    }
    
    # Iterrate through each page 
    for {set currPage 1} {$currPage <= $totalPages} {incr currPage} {
	catch {ixNet setAttribute $view/page -currentPage $currPage} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "GetResults: Failed to get statistic for current page."
	    exit
	}
	ixNet commit
	
	# Wait for statistics to populate on current page
	set whileLoopStopCounter 0
	while {[ixNet getAttribute $view/page -isReady] != "true"} {
	    if {$whileLoopStopCounter == "5"} {
		puts "ViewStats: Could not get stats"
		exit
	    }
	    if {$whileLoopStopCounter < 5} {
		puts "\nViewStats: Not ready yet.  Waiting $whileLoopStopCounter/5 seconds ..."
		after 1000
	    }
	    incr whileLoopStopCounter
	}
	
	set pageList [ixNet getAttribute $view/page -rowValues] ;# first list of all rows in the page
	set totalFlowStatistics [llength $pageList]

	# totalPageList == The total amount of flow statistics
	for {set pageListIndex 0} {$pageListIndex <= $totalFlowStatistics} {incr pageListIndex} {
	    set rowList [lindex $pageList $pageListIndex] ;# second list of 1 ingress and x egress rows

	    for {set rowIndex 0} {$rowIndex < [llength $rowList]} {incr rowIndex} {
		# cellList: 1/1/1 1/1/2 TI0-Flow_1 1.1.1.1-1.1.2.1 4000 4000 0 0 0 0 256000 0 0 0 0 0 0 0 0 0 0 0 00:00:00.684 00:00:00.700
		set cellList [lindex $rowList $rowIndex] ;# third list of cell values
		
		#puts "\n--- cellList $pageListIndex: $cellList ---\n"

		# Get the Traffic Item name
		set trafficItemIndex [lsearch $columnList "Traffic Item"]
		if {$trafficItemIndex == -1} {
		    set trafficItem "UnknownTrafficItem $pageListIndex"
		} else {
		    set trafficItem [lindex $cellList $trafficItemIndex]
		}

		set rxPortIndex [lsearch $columnList "Rx Port"]
		set rxPort [lindex $cellList $rxPortIndex]
		
		foreach column $columnList item $cellList {
		    if {[regexp "VLAN:VLAN Priority" $column]} {
			set column "Vlan_Priority"
		    }
		    if {[regexp "VLAN:VLAN-ID.*1" $column]} {
			set column "Outter_Vlan_ID"
		    }
		    if {[regexp "VLAN:VLAN-ID" $column]} {
			set column "Inner_Vlan_ID"
		    }
		    if {[regexp "IPv4 :Source Address" $column]} {
			set column "IPv4_Src_Address"
		    }
		    if {[regexp "IPv4 :Destination Address" $column]} {
			set column "IPv4_Dst_Address"
		    }
		    if {[regexp "Ethernet II:Destination MAC Address" $column]} {
			set column "Dest_Mac_Address"
		    }
		    if {[regexp "Ethernet II:Source MAC Address" $column]} {
			set column "Src_Mac_Address"
		    }
		    if {$getStatsBy == "trafficItem"} {
			if {[regexp "Traffic Item" $column] == 0} {
			    keylset getStats trafficItem.[join $trafficItem _].flow.$pageListIndex.[join $column _] $item
			}
		    }
		    if {$getStatsBy == "port"} {
			if {[regexp "Rx Port" $column] == 0} {
			    keylset getStats rxPort.$rxPort.trafficItem.[join $trafficItem _].[join $column _] $item
			}
		    }
		}
	    }
	}
    }

    return $getStats
}

puts "\nConnecting to $ixNetworkTclServerIp ..."
puts "Rebooting ports $portList ..."

ConnectToIxia "-reset -device $ixiaChassisIp -port_list $portList -ixnetwork_tcl_server $ixNetworkTclServerIp -tcl_server $ixiaChassisIp -username $userName -connect_timeout 120"

# port1Endpoint: ::ixNet::OBJ-/vport:1/protocolStack
# port2Endpoint: ::ixNet::OBJ-/vport:2/protocolStack
set port1Endpoint [ConfigInterfaceConfig $port1Config]
set port2Endpoint [ConfigInterfaceConfig $port2Config]

# Start Static IP w/Auth Protocol to generate ARPs
set startProtocolStatus [::ixia::test_control -action start_all_protocols]
if {[keylget startProtocolStatus status] != $::SUCCESS} {
    puts "\nError: Starting all protocols failed:  $startProtocolStatus\n"
    exit
}

# -mac_dst_tracking 1
# I am excluding -mac_dst_tracking ingres tracking
# because I can only track four items.
set trafficItem1 [CreateTrafficItem "-mode create -name Traffic_Item_1 -emulation_src_handle [list $port1Endpoint] -emulation_dst_handle [list $port2Endpoint] -src_dest_mesh one_to_one -route_mesh one_to_one -bidirectional 0 -circuit_endpoint_type ipv4 -rate_percent 100 -frame_size 100 -transmit_mode single_burst -pkts_per_burst 50000 -ip_dst_tracking 1 -ip_src_tracking 1 -mac_src_tracking 1 -vlan_id_tracking 1"]

# Enable Q-in-Q, the two vlan stacks for tracking
set configElement [keylget trafficItem1 traffic_item]
set packetStack [keylget trafficItem1 $configElement.headers]
foreach stack $packetStack {
    if {[regexp "vlan" $stack]} {
	puts "\nEnabling vlan packet stack for tracking:\n$stack" 
	set streamResult [::ixia::traffic_config  \
			  -mode modify \
			  -stream_id $stack \
			  -vlan enable \
			  -vlan_id_tracking 1 \
			 ]
	if {[keylget streamResult status] != $::SUCCESS} {
	    puts "Error: Failed to track vlan ID on: $stack"
	    exit
	}
    }
}

set startTrafficStatus [::ixia::traffic_control \
			    -action run \
			    -type l23 \
			   ]
if {[keylget startTrafficStatus status] != $::SUCCESS} {
    puts "\nError: Failed to start traffic: $startTrafficStatus\n"
    exit
}

after 10000

set flowStats [GetStatView]

puts \n[KeylPrint flowStats]\n
