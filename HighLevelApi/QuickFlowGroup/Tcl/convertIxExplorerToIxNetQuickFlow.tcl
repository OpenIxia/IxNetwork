#!/usr/bin/tclsh

# Description
#
#    Customers who has legacy IxExplorer-FT HL API scripts and need to
#    convert scripts to IxNetwork.
#
#    Mainly because the IxExplorer-FT scripts are not supported in IxNetwork
#    after version 6.80.
#
#    The solution is to use IxNetwork Quick Flow Group, which is designed for
#    IxExplorer usage in IxNetwork.
#
#    This script is a sample to show how to use customer's existing HL API parameters/values
#    and automatically ...
#        - Create one Traffic Item and circuit_type = Quick Flow
#        - Get all the configured vports (excluding the TxPort) and 
#          add all vports to the HLAPI parameter -port_handle2 as receiving ports.
#        - Enable traffic item Ingress tracking.
#        - Regenerate Traffic Item.
#        - Start traffic
#        - Get Flow Statistics stats.
#        - Look for all the ports that received traffic.

package req Ixia

set ixnetworkTclServer 192.168.70.3
set chassisIp 192.168.70.11
set userName hgee
set portList {1/1 2/1}
set port_1 1/1/1
set port_2 1/2/1

proc ResumeHlt { connectParams } {
    # Usage:
    #   set connect(-tcl_server) "10.219.117.101"'
    #   set connect(-ixnetwork_tcl_server) "10.219.117.103"'
    #   set connect(-username) "hgee"'
    #   set connect(-session_resume_keys) 1'
    #   ResumeHlt ::connect

    upvar $connectParams params

    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "Resume..."
    set status [eval ::ixia::connect $paramList]
    return $status
}

proc GetVportConnectedToPort {vport} {
    set connectedTo [lrange [split [ixNet getAttribute $vport -connectedTo] /] 3 end]
    set card [lindex [split [lindex $connectedTo 0] :] 1]
    set port [lindex [split [lindex $connectedTo 1] :] 1]
    return 1/$card/$port
}

proc ConfigQuickFlowGroup {portHandle trafficParam} {
    # Description
    #    Using IxExplorer-FT HL APIs to configure IxNetwork Quick Flow Group.
    #    For Quick Flow Group, only one Traffic Item is allowed and required.
    #    If you have multiple streams (QFG), they all fall under this Traffic Item.
    
    upvar $trafficParam params
    
    # Create just ONE Traffic Item for Quick Flow Group. Cannot and should not create more than one Traffic Item.
    # After creating one Traffic Item, you could add multiple Quick Flow Groups.
    puts "\nExisting Traffic Item: [ixNet getList [ixNet getRoot]/traffic trafficItem]"
    if {[ixNet getList [ixNet getRoot]/traffic trafficItem] == ""} {
	puts "\nCreating new traffic item for Quick Flow Group"
	set quickFlowGroupObj [ixNet add [ixNet getRoot]/traffic trafficItem]
	ixNet setMultiAttribute $quickFlowGroupObj \
	    -trafficItemType quick \
	    -trafficType raw
	ixNet commit
	set quickFlowGroupObj [lindex [ixNet remapIds $quickFlowGroupObj] 0]
	puts "QuickFlowGroupObj: $quickFlowGroupObj"
    }
    
    # Create a list of receiving ports and exclude the transmitting port
    puts "ConfigQuickFlowGroup: [array get params name]"
    set portList {}
    foreach vport [ixNet getList [ixNet getRoot] vport] {
	set port [GetVportConnectedToPort $vport]
	# Don't append the Tx Port in the recieving port list.
	if {$portHandle != $port} {
	    lappend portList $port
	}
    }
    puts "\nAll vport list for Rx ports: $portList"
    
    # Add the receiving port(s) and make the Traffic Item type as quick_flows
    #params.update({'port_handle': portHandle, 'port_handle2': ' '.join(portList), 'circuit_type':'quick_flows'})
    set params(-port_handle) $portHandle
    set params(-port_handle2) [list $portList]
    set params(-circuit_type) quick_flows
    
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }
    
    puts "\nConfiguring HLT params: $paramList"
    set status [eval ::ixia::traffic_config $paramList]
    if {[keylget status status] != $::SUCCESS} {
	puts "\nError: traffic_config failed: $status\n"
    }
    puts "\nconfig_traffic status: $status"
    
    # Enable ingress tracking
    puts "\nEnabling Quick Flow Group statistics tracking"
    set quickFlowGroupObj [lindex [ixNet getList [ixNet getRoot]/traffic trafficItem] 0]
    if {[catch {ixNet setAttribute $quickFlowGroupObj/tracking -trackBy [list trackingenabled0]} errMsg]} {
	puts "\nError: Enabling ingress tracking: $errMsg"
    }
    ixNet commit
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

proc StartTrafficNgpfHlt {} {
    puts "\nStartTrafficNgpfHlt"
    set startTrafficStatus [::ixiangpf::traffic_control -action run]
    if {[keylget startTrafficStatus status] != $::SUCCESS} {
	puts "\nError StartTrafficHlt: $startTrafficStatus\n"
	return 1
    } 

    # By including VerifyTrafficState, it will wait up to 15 seconds until
    # traffic is started before returning.
    VerifyTrafficState
    return 0
}

proc StopTrafficNgpfHlt {} {
    puts "\nStopTrafficNgpfHlt ..."
    set stopTrafficStatus [::ixiangpf::traffic_control -action stop]
    if {[keylget stopTrafficStatus status] != $::SUCCESS} {
	puts "\nError StopTrafficNgpfHlt: $stopTrafficStatus\n"
	return 1
    } 
    after 5000
    return 0
}

proc VerifyTrafficState {} {
    set startCounter 1
    set stopCounter 15
    for {set start $startCounter} {$start <= $stopCounter} {incr start} {
	set trafficState [CheckTrafficState]

	# Basically, if traffic state is unapplied or lock, then failed.
	if {$start == $stopCounter} {
	    if {$trafficState != "started" || $trafficState != "startedWaitingForStats" \
		    || $trafficState != "stoppedWaitingForStats" || $trafficState != "stopped"} {
		puts "VerifyTrafficState Error: Traffic failed to start"
		return 1
	    }
	}
	
	if {$trafficState == "started"} {
	    puts "VerifyTrafficState: Traffic Started"
	    break
	}

	if {$trafficState == "stopped"} {
	    puts "VerifyTrafficState: Traffic stopped"
	    break
	}

	if {$trafficState == "startedWaitingForStats" || $trafficState == "stoppedWaitingForStats"} {
	    puts "VerifyTrafficState: Traffic started. Waiting for stats to complete"
	    break
	}

	if {$start < $stopCounter} {
	    if {$trafficState != "started" || $trafficState != "startedWaitingForStats" \
		    || $trafficState != "stoppedWaitingForStats" || $trafficStats != "stopped"} {
		puts "VerifyTrafficState: Current state = $trafficState. Waiting $start/$stopCounter ..."
		after 1000
	    }
	}
    }
}

proc CheckTrafficState {} {
    # This API is mainly used by VerifyTrafficState.
    # Users can also use this in their scripts to check traffic state.

    # startedWaitingForStats, startedWaitingForStreams, started, stopped, stoppedWaitingForStats, txStopWatchExpected, locked, unapplied

    set currentTrafficState [ixNet getAttribute [ixNet getRoot]/traffic -state]

    switch -exact -- $currentTrafficState {
	::ixNet::OK {
	    return notRunning
	}
	stopped {
	    return stopped
	}
	started {
	    return started
	}
	locked {
	    return locked
	}
	unapplied {
	    return unapplied
	}
	startedWaitingForStreams {
	    return startedWaitingForStreams
	}
	startedWaitingForStats {
	    return startedWaitingForStats
	}
	stoppedWaitingForStats {
	    return stoppedWaitingForStats
	}
	default {
	    return $currentTrafficState
	    puts "\nError CheckTrafficState: Traffic state is currently: $currentTrafficState\n"
	    return 1
	}
    }
}

proc GetStats {{viewName "Traffic Item Statistics"}} {
    # This will get the stats based on the $viewName stat that you want to retrieve.
    # Stats will be returned in a keyed list.
    #
    # viewName options (Not case sensitive):
    #    NOTE: Not all statistics are listed here.
    #          You could get the statistic viewName directly from the IxNetwork GUI in the statistics.
    #
    #    'Port Statistics'
    #    'Tx-Rx Frame Rate Statistics'
    #    'Port CPU Statistics'
    #    'Global Protocol Statistics'
    #    'Protocols Summary'
    #    'Port Summary'
    #    'OSPFv2-RTR Drill Down'
    #    'OSPFv2-RTR Per Port'
    #    'IPv4 Drill Down'
    #    'L2-L3 Test Summary Statistics'
    #    'Flow Statistics'
    #    'Traffic Item Statistics'
    #    'IGMP Host Drill Down'
    #    'IGMP Host Per Port'
    #    'IPv6 Drill Down'
    #    'MLD Host Drill Down'
    #    'MLD Host Per Port'
    #    'PIMv6 IF Drill Down'
    #    'PIMv6 IF Per Port'

    set root [ixNet getRoot]
    set viewList [ixNet getList $root/statistics view]    
    set statViewIndex [lsearch -nocase -regexp $viewList $viewName]
    set view [lindex $viewList $statViewIndex]
    puts "\nview: $view"
    # Flow Statistics
    set caption [ixNet getAttribute $view -caption]

    ixNet setAttribute $view -enabled true
    ixNet commit

    set columnList [ixNet getAttribute ${view}/page -columnCaptions]
    #puts "\n$columnList\n"
    
    set startTime 1
    set stopTime 30
    while {$startTime < $stopTime} {
	set totalPages [ixNet getAttribute $view/page -totalPages]
	if {[regexp -nocase "null" $totalPages]} {
	            puts "\nGetStatView: Getting total pages for $view is not ready. $startTime/$stopTime"
	            after 2000
	} else {
	            break
	}
    }
    #puts "\ntotal Pages: $totalPages"

    # Iterrate through each page 
    set row 0
    for {set currentPage 1} {$currentPage <= $totalPages} {incr currentPage} {
	puts "\nGetStatView: Getting statistics on page: $currentPage/$totalPages. Please wait ..."

	catch {ixNet setAttribute $view/page -currentPage $currentPage} errMsg
	if {$errMsg != "::ixNet::OK"} {
	            puts "\nGetStatView: Failed to get statistic for current page.\n"
	            return 1
	}
	ixNet commit
	
	# Wait for statistics to populate on current page
	set whileLoopStopCounter 0
	while {[ixNet getAttribute $view/page -isReady] != "true"} {
	    if {$whileLoopStopCounter == "5"} {
		puts "\nGetStatView: Could not get stats"
		return 1
	    }
	    if {$whileLoopStopCounter < 5} {
		puts "\nGetStatView: Not ready yet.  Waiting $whileLoopStopCounter/5 seconds ..."
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
		# Increment the row number
		incr row

		# cellList: 1/1/1 1/1/2 TI0-Flow_1 1.1.1.1-1.1.2.1 4000 4000 0 0 0 0 256000 0 0 0 0 0 0 0 0 0 0 0 00:00:00.684 00:00:00.700
		set cellList [lindex $rowList $rowIndex] ;# third list of cell values
		
		puts "\n  $row:"
		for {set index 0} {$index <[llength $cellList]} {incr index} {
		    keylset getStats flow.$row.[join [lindex $columnList $index] _] [lindex $cellList $index]
		    puts "\t[join [lindex $columnList $index] _]: [lindex $cellList $index]"
		}
	    }
	}
    }  
    ixNet setAttribute $view -enabled false
    ixNet commit

    return $getStats
}

proc KeylPrint {keylist {space ""}} {
    # Pretty print key list

    upvar $keylist kl
    set result ""
    foreach key [keylkeys kl] {
	if {$key == ""} {
	    continue
	}
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


set trafficItem1(-name) rule1
set trafficItem1(-mode) create
set trafficItem1(-mac_dst_mode) fixed
set trafficItem1(-mac_src_mode) fixed
set trafficItem1(-mac_src) 00:0C:29:AA:86:E0
set trafficItem1(-mac_dst) 00:0C:29:84:37:16
set trafficItem1(-transmit_mode) single_burst
set trafficItem1(-rate_pps) 1000
set trafficItem1(-l3_protocol) ipv4
set trafficItem1(-ip_src_addr) 1.1.1.1
set trafficItem1(-ip_src_mode) increment
set trafficItem1(-ip_src_step) 0.0.0.1
set trafficItem1(-ip_src_count) 1
set trafficItem1(-ip_dst_addr) 1.1.1.2
set trafficItem1(-ip_dst_mode) increment
set trafficItem1(-ip_dst_step) 0.0.0.1
set trafficItem1(-ip_dst_count) 1
set trafficItem1(-rate_percent) 10
set trafficItem1(-frame_size) 1000
set trafficItem1(-number_of_packets_per_stream) 50000

set trafficItem2(-name) rule2
set trafficItem2(-mode) create
set trafficItem2(-mac_dst_mode) fixed
set trafficItem2(-mac_src_mode) fixed
set trafficItem2(-mac_src) 00:0C:29:84:37:16
set trafficItem2(-mac_dst) 00:0C:29:AA:86:E0
set trafficItem2(-transmit_mode) single_burst
set trafficItem2(-rate_pps) 1000
set trafficItem2(-l3_protocol) ipv4
set trafficItem2(-ip_src_addr) 1.1.1.2
set trafficItem2(-ip_src_mode) increment
set trafficItem2(-ip_src_step) 0.0.0.1
set trafficItem2(-ip_src_count) 1
set trafficItem2(-ip_dst_addr) 1.1.1.1
set trafficItem2(-ip_dst_mode) increment
set trafficItem2(-ip_dst_step) 0.0.0.1
set trafficItem2(-ip_dst_count) 1
set trafficItem2(-rate_percent) 10
set trafficItem2(-frame_size) 1000
set trafficItem2(-number_of_packets_per_stream) 50000

set connect(-ixnetwork_tcl_server) $ixnetworkTclServer
set connect(-username) "hgee"
set connect(-session_resume_keys) 1
#set status [ResumeHlt ::connect]

set status [::ixia::connect  \
		-reset 1 \
		-device $chassisIp \
		-port_list $portList \
		-ixnetwork_tcl_server $ixnetworkTclServer \
		-tcl_server $chassisIp \
		-username hgee \
	       ]
puts [KeylPrint status]

set port1Status [::ixia::interface_config \
		     -mode config \
		     -port_handle $port_1 \
		     -intf_ip_addr 1.1.1.1 \
		     -gateway 1.1.1.2 \
		     -netmask 255.255.255.0 \
		     -src_mac_addr 00:01:01:01:00:01 \
		    ]
set port1Interface [keylget port1Status interface_handle]

set port2Status [::ixia::interface_config \
		     -mode config \
		     -port_handle $port_2 \
		     -intf_ip_addr 1.1.1.2 \
		     -gateway 1.1.1.1 \
		     -netmask 255.255.255.0 \
		     -src_mac_addr 00:01:01:02:00:02 \
		    ]
set port2Interface [keylget port2Status interface_handle]

# port1Interface = ::ixNet::OBJ-/vport:1/interface:1
# port2Interface = ::ixNet::OBJ-/vport:2/interface:1

after 3000

set port1ArpStatus [::ixia::interface_config -port_handle $port_1 -arp_send_req 1 -arp_req_retries 3]
set port2ArpStatus [::ixia::interface_config -port_handle $port_2 -arp_send_req 1 -arp_req_retries 3]

ConfigQuickFlowGroup $port_1 trafficItem1
ConfigQuickFlowGroup $port_2 trafficItem2

RegenerateAllTrafficItems
StartTrafficNgpfHlt

after 15000
set stats [GetStats "Flow Statistics"]
puts [KeylPrint stats]
