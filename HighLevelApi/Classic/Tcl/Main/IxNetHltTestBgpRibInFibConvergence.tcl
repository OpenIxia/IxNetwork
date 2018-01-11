#!/opt/ActiveTcl-8.5/bin/tclsh

# Written by: Hubert Gee
# hgee@ixiacom.com

package req IxTclNetwork
package req Ixia ; #Loading the Ixia package to use Tclx keylist command

# Description
#
#     This script loads an existing ixcfg file and 
#     map ports to the loaded configuration.
#
#     By default, this script will loop through each vport to get
#     the physical port and create a port list.
# 
#     Optionally:
#         In case the configuration is saved with logical ports, meaning no
#         physical port assigned, users can uncomment out the variable portList
#         to state the physical ports used.
#
#     - This script will test BGP RIB-IN convergence benchmarking.
#     - On the Traffic Item Options in the IxNetwork GUI, 
#       enable the following CP/DP Convergence:
#              - Control Plane Events
#                    To capture the BGP route advertisement time.
#
#              - Data Plane Events - Rate monitoring
#                    To measure incoming traffic to capture the timestamp
# 
#              - Set Data Plane Threshold (%) = 85
#                     Trigger the timestamp when the incoming throughput rate is over 85%.
#
#              - Set Data Plane Jitter Window = 10ms
#                     Ixia port will collect all arriving packets to determine the 
#                     throughput and frame rate.
#
#                ixNet setMultiAttribute $::IxScriptgen::_objRefs(1)/traffic/statistics/cpdpConvergence \
#                     -enabled true \
#                     -dataPlaneThreshold 85 \
#                     -enableDataPlaneEventsRateMonitor true \
#                     -enableControlPlaneEvents true
#
#     - Traffic Item configruations:
#              - Rate = 10%
#              - Framesize = 256
#              - Flow Tracking = Traffic Item and Dest Endpoint
#
#  Steps taken to test the RIB-IN/FIB convergence test
#
#     - Load the config
#     1> Make sure we have a stabilized test setup.
#         - Start BGP protocl and verify BGP session.
#         - Start/stop traffic and verify traffic is received.
#     
#     2> If step #1 passes, then get ready for testing ...
#         - Start continuous traffic
#         - Disable BGP routes
#         - Clear CP/DP stat counter
#         - Enable BGP routes
#         - Verify BGP session is up
#         - Wait for traffic to get received.
#         - Once traffic is received, get the RIB-IN/FIB convergence time
#       
# Optional: Uncomment the below line and provide your ports for this config file.
# set portList {{1 1} {1 2}}

# User's must change the following variables accordingly
set ixNetworkVersion 7.12
# This is Dean Lee's Ixia Chassis. His ports are connected to a DUT with BGP
set ixChassisIp 10.200.134.44 
#set ixChassisIp 10.205.4.172
set ixNetworkTclServer 10.205.1.42
set userName hgee
set ixNetPort 8009
set portList [list 1/1 1/2]
set cePort   1/1/2
set bgpPort  1/1/1

set intConfig(connectedInt,$cePort,intf_ip_addr) 20.3.2.2
set intConfig(connectedInt,$cePort,gateway)      20.3.2.1
set intConfig(connectedInt,$cePort,src_mac_addr) 00:01:01:02:00:01
set intConfig(connectedInt,$cePort,netmask)      255.255.255.0

set bgpConfig(connectedInt,$bgpPort,intf_ip_addr) 20.3.1.2
set bgpConfig(connectedInt,$bgpPort,gateway)      20.3.1.1
set bgpConfig(connectedInt,$bgpPort,src_mac_addr) 00:01:01:01:00:01
set bgpConfig(connectedInt,$bgpPort,netmask)      255.255.255.0


proc ConfigInterfaceIp {} {
    # This Proc will dynamically create each port interface configurations based
    # on what the user created for the array variable of ::intConfig.
    # The parameters used in ::intConfig must be the same HLT parameter.

    if {[info exists ::portList] == 0} {
	puts "Error: You must create a variable \"portList\" with all your ports"
	exit
    }

    foreach port $::portList {
	set port 1/$port

	if {[array get ::intConfig connectedInt,$port,*] != ""} {
	    set portConfigProperties {-mode config }
	    append portConfigProperties "-port_handle $port "
	    
	    puts "\nInterface Config:\n\t-port_handle $port\n\t-mode config"
	    
	    foreach {properties values} [array get ::intConfig connectedInt,$port,*] {
		set property [lindex [split $properties ,] end]
		append portConfigProperties "-$property $values "
		puts "\t-$property $values"
	    }
	    
	    set portStatus [eval ::ixia::interface_config $portConfigProperties]
	    
	    if {[keylget portStatus status] != $::SUCCESS} {
		puts "\nERROR: ConfigInterfaceIp: Failed on $port: $portStatus"
		exit
	    } else {
		puts "Successfully configured IP interface on $port"
	    }
	    
	    set interfaceHandle [keylget portStatus interface_handle]
	    
	    # Build a list of all the src/dst emulation handles for Traffic Item
	    # interfaceHandles: ::ixNet::OBJ-/vport:1/interface:1
	    set ::trafficConfig($port,interfaceHandle) $interfaceHandle
	}
    }
}

proc ConfigTrafficItem {} {
    # This Proc will create Traffic Items "dynamically".
    # This configures only what the user create for the 
    # array trafficConfig.
    # All the parameters must be the same as the HLT parameters.

    # Get a list of all the Traffic Items first in order to know exactly 
    # how many Traffic Items to create.
    set totalTrafficItem {}
    foreach {properties values} [array get ::trafficConfig *] {
	set number [lindex [split $properties ,] 1]
	if {[lsearch $totalTrafficItem $number] == -1} {
	    lappend totalTrafficItem $number
	}
    }

    for {set traffItemNum 1} {$traffItemNum <= $totalTrafficItem} {incr traffItemNum} {
	puts "\nTrafficItem $traffItemNum:\n\t-mode create"

	set trafficItemProperties {-mode create }
	
	foreach {properties value} [array get ::trafficConfig trafficItem,$traffItemNum,*] {	    
	    set property [lindex [split $properties ,] end]

	    if {$property == "endpoints"} {
		# [lindex $values 0] = list_of_all_src_endpoints
		# [lindex $values 1] = list_of_all_dst_endpoints
		set endpoints $value

		foreach srcEp [lindex $endpoints 0] {
		    lappend srcEndpointHandles $srcEp
		}

		append trafficItemProperties "-emulation_src_handle $srcEndpointHandles "
		puts "\t-emulation_src_handle $srcEndpointHandles"

		foreach dstEp [lindex $endpoints 1] {
		    lappend dstEndpointHandles $dstEp
		}
		append trafficItemProperties "-emulation_dst_handle $dstEndpointHandles "
		puts "\t-emulation_dst_handle $dstEndpointHandles"

	    } else {
		append trafficItemProperties "-$property $value "
		puts "\t-$property $value"
	    }

	}

	set trafficItemStatus [eval ::ixia::traffic_config $trafficItemProperties]
	
	if {[keylget trafficItemStatus status] != $::SUCCESS} {
	    puts "\nERROR: Ixia traffic item $traffItemNum failed: $trafficItemStatus"
	    exit
	} else {
	    puts "Successfully created Traffic Item $traffItemNum"
	}
    }
}

proc VerifyPortState {} {
    puts "\nVerifying port state ...\n"

    foreach vport [ixNet getList [ixNet getRoot] vport] {
	for {set timer 0} {$timer <= 60} {incr timer 2} {
	    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
	    set connectedTo [ixNet getAttribute $vport -connectedTo]
	    set connectedTo [lrange [split $connectedTo /] 3 4]
	    set card [lindex [split [lindex $connectedTo 0] :] end]
	    set port [lindex [split [lindex $connectedTo 1] :] end]
	    set port $card/$port
	    
	    set portState [ixNet getAttribute $vport -state]
	    if {$portState != "up" && $timer != "60"} {
		puts "$port is still rebooting. PortState = $portState.  $timer/60 seconds."
		after 2000
		continue
	    }
	    
	    if {$portState != "up" && $timer == "60"} {
		puts "$port seem to be stuck on rebooting"
		exit
	    }
	    
	    if {$portState == "up"} {
		puts "$port state is $portState"
		break
	    }
	}
    }
    after 3000
}

proc StartAllProtocols {} {
    puts "\nStarting BGP protocol ..."
    catch {ixNet exec startAllProtocols} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "\nError: Failed to start all protocols\n$errMsg"
	return 1
    }
    ixNet commit
    return 0
}

# ixNet exec stopAllProtocols
proc StopAllProtocols {} {
    catch {ixNet exec stopAllProtocols} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "\nError: Failed to stop all protocols\n$errMsg"
	return 1
    }
    ixNet commit
    puts "\nStopping BGP protocol ..."
    return 0
}

proc ConfigCpDpConvergence {} {
    set cpdpStatus [::ixia::traffic_control \
			-action manual_trigger \
			-cpdp_convergence_enable 1 \
			-cpdp_ctrl_plane_events_enable 1 \
			-cpdp_data_plane_events_rate_monitor_enable 1 \
			-cpdp_data_plane_threshold 85 \
			-cpdp_data_plane_jitter 10 \
			-disable_latency_bins \
		       ]
    if {[keylget cpdpStatus status] != $::SUCCESS} {
	puts "Error: Failed to set Traffic Options CP/DP Convergence"
	puts "$cpdpStatus"
    }
    
    if 0 {
	ixNet setMultiAttribute [ixNet getRoot]/traffic/statistics/cpdpConvergence \
	    -enabled true \
	    -dataPlaneThreshold 85 \
	    -enableDataPlaneEventsRateMonitor true \
	    -enableControlPlaneEvents true
	ixNet commit
    }
}

proc ClearCpDpStatCounter {} {
    puts "\nClearing CP/DP statistic counter ..."
    ixNet exec clearCPDPStats
}

proc RegenerateAllTrafficItems {} {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	catch {ixNet exec generate $trafficItem} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "Error: Regenerate failed on $trafficItem"
	    return 1
	}
	puts "Regenerate: $trafficItem"
    }
    return 0
}


proc ApplyTraffic {} {
    puts "\nApplying configuration to hardware ..."
    set traffic [ixNet getRoot]traffic

    set stopCounter 10
    for {set startCounter 1} {$startCounter <= $stopCounter} {incr startCounter} {
	catch {ixNet exec apply $traffic} errMsg
	if {$errMsg != "::ixNet::OK" && $startCounter < $stopCounter} {
	    puts "ApplyTraffic: Attempting to apply traffic: $startCounter/$stopCounter tries"
	    after 1000
	    continue
	}
	if {$errMsg != "::ixNet::OK" && $startCounter == $stopCounter} {
	    puts "ApplyTraffic: $errMsg"
	    return 1
	}
	if {$errMsg == "::ixNet::OK" && $startCounter < $stopCounter} {
	    puts "Successfully applied traffic to hardware"
	    break
	}
    }
    after 5000
    return 0
}

proc StartTraffic { } {
    set traffic [ixNet getRoot]traffic

    puts "\nStarting traffic ..."

    catch {ixNet exec start $traffic} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "Start traffic error: $errMsg"
	return 1
    }

    after 2000

    set startCounter 1
    set stopCounter 10
    for {set start $startCounter} {$start <= $stopCounter} {incr start} {
	set trafficState [CheckTrafficState]

	# Basically, if traffic state is unapplied or lock, then failed.
	if {$start == $stopCounter} {
	    if {$trafficState != "started" || $trafficState != "startedWaitingForStats" \
		    || $trafficState != "stoppedWaitingForStats" || $trafficState != "stopped"} {
		puts "Traffic failed to start"
		return 1
	    }
	}
	
	if {$trafficState == "started"} {
	    puts "Traffic Started"
	    break
	}

	if {$trafficState == "stopped"} {
	    puts "Traffic stopped"
	    break
	}

	if {$trafficState == "startedWaitingForStats" || $trafficState == "stoppedWaitingForStats"} {
	    puts " Traffic started. Waiting for stats to complete"
	    break
	}

	if {$start < $stopCounter} {
	    if {$trafficState != "started" || $trafficState != "startedWaitingForStats" \
		    || $trafficState != "stoppedWaitingForStats" || $trafficStats != "stopped"} {
		puts "StartTraffic: Current state = $trafficState. Waiting $start/$stopCounter ..."
		after 1000
	    }
	}
    }
    after 10000
    return 0
}

proc StopTraffic {} {
    set traffic [ixNet getRoot]traffic

    catch {ixNet exec stop $traffic} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "Error: Stop traffic: $errMsg"
	return 1
    }
    puts "\nStopping traffic. Please wait ..."
    after 10000
    return 0
}

proc CheckTrafficState {} {
    # startedWaitingForStats,startedWaitingForStreams,stopped,stoppedWaitingForStats,txStopWatchExpected,unapplied
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
	    puts "CheckTrafficState Error: Traffic state is currently: $currentTrafficState"
	    return 0
	}
    }
}

proc GetStatView { {statView "Flow Statistics"} {getStatsBy trafficItem} } {
    # $viewList: 
    # {::ixNet::OBJ-/statistics/view:"Port Statistics"} 
    # {::ixNet::OBJ-/statistics/view:"Tx-Rx Frame Rate Statistics"} 
    # {::ixNet::OBJ-/statistics/view:"Port CPU Statistics"} 
    # {::ixNet::OBJ-/statistics/view:"Global Protocol Statistics"}
    # {::ixNet::OBJ-/statistics/view:"Flow Statistics"} 
    # {::ixNet::OBJ-/statistics/view:"Flow Detective"}  
    # {::ixNet::OBJ-/statistics/view:"Data Plane Port Statistics"} 
    # {::ixNet::OBJ-/statistics/view:"User Defined Statistics"} 
    # {::ixNet::OBJ-/statistics/view:"Traffic Item Statistics"}
    # {::ixNet::OBJ-/statistics/view:"BGP Aggregated Statistics"}
    set viewList [ixNet getList [ixNet getRoot]/statistics view]

    # set statViewSelection "Flow Statistics"
    set statViewSelection $statView
    
    set flowStatsViewIndex [lsearch -regexp $viewList $statViewSelection]
    if {$flowStatsViewIndex == -1} {
	puts "ViewStats: No \"$statViewSelection\" found"
	exit
    }
    
    # $view: ::ixNet::OBJ-/statistics/view:"Flow Statistics"
    set view [lindex $viewList $flowStatsViewIndex]
    
    ixNet setAttribute $view -enabled true
    ixNet commit

    # $columnList:
    # {Tx Port} {Rx Port} {Traffic Item} {Ethernet II:Destination MAC Address} {Ethernet II:Source MAC Address} {Ethernet II:Ethernet-Type} {Ethernet II:PFC Queue} {IPv4 :Precedence} {IPv4 :Source Address} {IPv4 :Destination Address} {Custom Tracking: Byte Offset 0} {Source/Dest Endpoint Pair} {Source/Dest Value Pair} {Source/Dest Port Pair} {Source Endpoint} {Source Port} {Dest Endpoint} {Frame Size} {Flow Group} {Traffic Group ID} {Tx Frames} {Rx Frames} {Frames Delta} {Loss %} {Tx Frame Rate} {Rx Frame Rate} {Rx Bytes} {Tx Rate (Bps)} {Rx Rate (Bps)} {Tx Rate (bps)} {Rx Rate (bps)} {Tx Rate (Kbps)} {Rx Rate (Kbps)} {Tx Rate (Mbps)} {Rx Rate (Mbps)} {Store-Forward Avg Latency (ns)} {Store-Forward Min Latency (ns)} {Store-Forward Max Latency (ns)} {First TimeStamp} {Last TimeStamp}
    
    set columnList [ixNet getAttribute ${view}/page -columnCaptions]
    #puts "\n$columnList\n"

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
		    if {[regexp "TI\[0-9]+-(.*)" $trafficItem - newTrafficItemName]} {
			set trafficItem $newTrafficItemName
		    }
		}

		# Get the Flow Group
		set flowGroupIndex [lsearch $columnList "Flow Group"]
		if {$flowGroupIndex == -1} {
		    set flowGroup "$pageListIndex"
		} else {
		    # Flow Group 0008
		    set flowGroup [lindex [lindex $cellList $flowGroupIndex] end]
		}
		
		set rxPortIndex [lsearch $columnList "Rx Port"]
		set rxPort [lindex $cellList $rxPortIndex]
		
		foreach column $columnList item $cellList {
		    if {[regexp "Sess\. Up" $column]} {
			set column "SessionUp"
		    }

		    if {[regexp "RIB-IN/FIB" $column]} {
			set column "RibInFibConvergence"
		    }

		    if {[regexp "DP Above Threshold Timestamp" $column]} {
			set column "DpAboveThresholdTimestamp"
		    }

		    if {[regexp "DP Below Threshold Timestamp" $column]} {
			set column "DpBelowThresholdTimestamp"
		    }

		    if {[regexp "Event Start Timestamp" $column]} {
			set column "EventStartTimestamp"
		    }
		    if {[regexp "Event End Timestamp" $column]} {
			set column "EventEndTimestamp"
		    }

		    if {$getStatsBy == "trafficItem"} {
			if {[regexp "Traffic Item" $column] == 0} {
			    keylset getStats trafficItem.[join $trafficItem _].flowGroup.Flow_Group_$flowGroup.[join $column _] $item
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

proc VerifyBgpSession {} {
    puts \n
    set endCounter 80
    for {set counter 0} {$counter <= $endCounter} {incr counter} {
	if {$counter == $endCounter} {
	    puts "BGP session cannot get established"
	    return 1
	}

	set results [GetStatView "BGP Aggregated Statistics"]
	set bgpSessionUp [keylget results trafficItem.UnknownTrafficItem_0.flowGroup.Flow_Group_0.SessionUp]
	
	if {$bgpSessionUp == 0 || $bgpSessionUp == ""} {
	    puts "BGP session is not up yet: Waiting $counter/$endCounter seconds ..."
	    after 1000
	}

	if {$bgpSessionUp > 0} {
	    puts "BGP Session is up"
	    after 3000
	    return 0
	}
    }
}

proc VerifyTxRxTraffic { {timeout 25} } {

    for {set counter 0} {$counter <= $timeout} {incr counter} {
	if {$counter == $timeout} {
	    puts "Packets are not getting transmitted. TxFrames counter remains 0"
	    return 1
	}

	set results [GetStatView]
	set txFrames [keylget results trafficItem.To_BGP.flowGroup.Flow_Group_0.Tx_Frames]
	set rxFrames [keylget results trafficItem.To_BGP.flowGroup.Flow_Group_0.Rx_Frames]

	if {$txFrames == 0 || $rxFrames == 0} {
	    puts "Waiting for packet transmittion: $counter/$timeout seconds"
	    after 1000
	}

	if {$rxFrames > 0} {
	    puts "\nPackets are transmitting ..."
	    puts "TxFrames: $txFrames"
	    puts "RxFrames: $rxFrames"
	    return 0
	}
    }
}

proc GetConvergenceStats {} {
    set results [GetStatView]
    puts "[KeylPrint results]"

    set ribInFibConverge [keylget results trafficItem.To_BGP.flowGroup.Flow_Group_0.RibInFibConvergence]
    set dpAboveThresholdTimestamp [keylget results trafficItem.To_BGP.flowGroup.Flow_Group_0.DpAboveThresholdTimestamp]
    set dpBelowThresholdTimestamp [keylget results trafficItem.To_BGP.flowGroup.Flow_Group_0.DpBelowThresholdTimestamp]
    
    set eventStartTimestamp [keylget results trafficItem.To_BGP.flowGroup.Flow_Group_0.EventStartTimestamp]
    set eventEndTimestamp [keylget results trafficItem.To_BGP.flowGroup.Flow_Group_0.EventEndTimestamp]
    
    puts \n
    puts "RibInFibConverge          : $ribInFibConverge (ms)"
    puts "DPAboveThresholdTimestamp : $dpAboveThresholdTimestamp (ns)"
    puts "DPBelowThresholdTimestamp : $dpBelowThresholdTimestamp (ns)"
    puts "EventStartTimestamp       : $eventStartTimestamp (ns)"
    puts "EventEndTimestamp         : $eventEndTimestamp (ns)"
    puts "\nRibInFibConvergence time = DPAboveThresholdTimestamp - EvenStartTimestamp"
}

# control options: enable or disable
proc ControlBgpRoutes { control portNumber } {
    if {$control == "enable"} {
	set type True
    } else {
	set type False
    }

    # ::ixNet::OBJ-/availableHardware/chassis:"10.200.134.44"/card:1/port:1
    foreach vport [ixNet getList [ixNet getRoot] vport] {
	set connectedTo [ixNet getAttribute $vport -connectedTo]
	set connectedTo [split $connectedTo /]
	set card [lindex [split [lindex $connectedTo 3] :] end]
	set port [lindex [split [lindex $connectedTo 4] :] end]
	set currentPort $card/$port
	if {$portNumber == $currentPort} {
	    puts "\nSetting port $currentPort BGP routes: $control"
	    set vportBgpRoute $vport/protocols/bgp/neighborRange:1/routeRange:1
	    ixNet setAttribute $vportBgpRoute -enabled $type
	    ixNet commit
	}
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

proc Connect { {connectionType reset} } {
    puts "\nConnecting to $::ixNetworkTclServer\n"
    if {$connectionType == "reset"} {
	set connectStatus [::ixia::connect \
			       -reset \
			       -port_list $::portList \
			       -username $::userName \
			       -ixnetwork_tcl_server $::ixNetworkTclServer \
			       -device $::ixChassisIp \
			       -tcl_server $::ixChassisIp \
			       -session_resume_keys 1
			  ]
    }
    if {$connectionType == "resume"} {
	set connectStatus [::ixia::connect \
			       -username $::userName \
			       -ixnetwork_tcl_server $::ixNetworkTclServer \
			       -tcl_server $::ixChassisIp \
			       -session_resume_keys 1 \
			  ]
    }
    
    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "Connecting to ixNetwork Tcl server failed\n\n$connectStatus\n"
	exit
    } 
}

Connect reset
ConfigInterfaceIp

set bgpConfigStatus [::ixia::emulation_bgp_config \
        -port_handle        $bgpPort \
        -mode               reset \
        -ip_version         4 \
        -local_ip_addr      20.3.1.2 \
        -remote_ip_addr     20.3.1.1 \
        -local_addr_step    0.0.1.0 \
        -remote_addr_step   0.0.1.0 \
        -count              1 \
        -neighbor_type      external \
        -local_as           200 \
        -local_as_step      1 \
        -local_as_mode      increment \
        ]
if {[keylget bgpConfigStatus status] != $::SUCCESS} {
    puts "Error: Configuring emulation_bgp_config failed:\nbgpConfigStatus"
    exit
}

# This is the handle to use in Traffic Item Endpoint
# ::ixNet::OBJ-/vport:1/proTocols/bgp/neighborRange:1
set bgpNeighborHandle [keylget bgpConfigStatus handles]
set trafficConfig($bgpPort,interfaceHandle) $bgpNeighborHandle

set bgpRouteConfigStatus [::ixia::emulation_bgp_route_config \
				 -mode                  add \
				 -handle                $bgpNeighborHandle \
				 -prefix                23.22.1.0 \
				 -prefix_step           1 \
				 -netmask               255.255.255.0 \
				 -num_routes            1000 \
				 -ip_version            4 \
				 -origin_route_enable   1 \
				 -origin                igp \
				]
if {[keylget bgpRouteConfigStatus status] != $::SUCCESS} {
    puts "Error: Configuring emulation-bgp_route_config failed:\n$bgpRouteConfigStatus"
    exit
}

# endpoints: The 1st value is a list of all srcPorts.
#            The 2nd value is a list of all dstPorts
set trafficConfig(trafficItem,1,endpoints)     "$::trafficConfig($cePort,interfaceHandle) $trafficConfig($bgpPort,interfaceHandle)"
set trafficConfig(trafficItem,1,bidirectional) 0
set trafficConfig(trafficItem,1,rate_percent)  10
set trafficConfig(trafficItem,1,frame_size)    256
set trafficConfig(trafficItem,1,transmit_mode) continuous
set trafficConfig(trafficItem,1,l3_protocol)   ipv4
set trafficConfig(trafficItem,1,track_by)      {traffic_item destEndpoint0}
set trafficConfig(trafficItem,1,name) To_BGP

ConfigTrafficItem
ConfigCpDpConvergence
VerifyPortState

if {[RegenerateAllTrafficItems]} {
    exit
}

if {[StartAllProtocols]} {
    exit
}

if {[VerifyBgpSession]} {
    exit
}

if {[ApplyTraffic]} {
    exit
}

# Start/Stop traffic and verify to 
# ensure the test setup is in a good state
if {[StartTraffic]} {
    exit
}
after 5000
StopTraffic

# If VerifyTxRxTraffic returns 0, means traffic was good.
if {[VerifyTxRxTraffic 25] == 0} {    
    puts "\nThe test setup is in a stabilized condition for convergence testing ..."

    StartTraffic
    ControlBgpRoutes disable 1/1
    puts "\nWait 10 seconds ..."
    after 10000
    ClearCpDpStatCounter
    ControlBgpRoutes enable 1/1
    puts "\nWait 10 seconds ..."
    after 10000
    VerifyBgpSession

    puts "\nVerifying traffic. As soon as traffic is getting received,"
    puts "then verify RIB-IN/FIB convergence time ..."

    VerifyTxRxTraffic 120
    GetConvergenceStats
}

StopTraffic
StopAllProtocols


