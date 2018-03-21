#!/usr/bin/tclsh

# Description
#    Load a saved .ixncfg config file
#    Verify port state
#    Start all protocols
#    TODO: Verify protocol sessions
#    Start traffic
#    Get stats

package req IxTclNetwork
package req Tclx

set apiServerIp 192.168.70.3
set ixChassisIp 192.168.70.11
set ixNetworkVersion 8.40
set configFile /home/hgee/Dropbox/MyIxiaWork/OpenIxiaGit/IxNetwork/RestApi/Python/SampleScripts/bgp_ngpf_8.30.ixncfg

proc Connect {apiServerIp ixNetworkVersion} {
    puts "\nConnecting to $apiServerIp"
    set connectStatus [ixNet connect $apiServerIp -version $ixNetworkVersion]
    puts "\nconnectStatus: $connectStatus"
    if {$connectStatus != "::ixNet::OK"} {
	puts "\nConnect failed $apiServerIp"
	exit
    }
}

proc LoadConfigFile {configFile} {
    puts "Loading config file: $configFile"
    set result [ixNet execute loadConfig [ixNet readFrom $configFile]]
    puts "\nresult: $result"
    if {$result != "::ixNet::OK"} {
	puts "\nError: Loading config file: $configFile"
	exit
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

proc ApplyTraffic {} {
    puts "\nApplying configuration to hardware ..."
    set traffic [ixNet getRoot]traffic

    set stopCounter 10
    for {set startCounter 1} {$startCounter <= $stopCounter} {incr startCounter} {
	catch {ixNet exec apply $traffic} errMsg
	if {$errMsg != "::ixNet::OK" && $startCounter < $stopCounter} {
	        puts "ApplyTraffic warning: Attempting to apply traffic: $startCounter/$stopCounter tries"
	        after 1000
	        continue
	}
	if {$errMsg != "::ixNet::OK" && $startCounter == $stopCounter} {
	        puts "ApplyTraffic error: $errMsg"
	        exit
	}
	if {$errMsg == "::ixNet::OK" && $startCounter < $stopCounter} {
	        puts "Successfully applied traffic to hardware"
	        break
	}
    }
    after 2000
}

proc VerifyPortState { {StopTimer 60} } {
    set portDownList {}
    set stopTime $StopTimer
    puts \n
    foreach vPort [ixNet getList [ixNet getRoot] vport] {
	set port [GetVportConnectedToPort $vPort]
	for {set timer 1} {$timer <= $stopTime} {incr timer} {
	    if {$timer == $stopTime} {
		lappend portDownList $port
	    }

	    if {[ixNet getAttribute $vPort -state] == "up"} {
		puts "Info: VerifyPortState: $port is up"
		break
	    } else {
		puts "VerifyPortState: $port is still not up. Waited $timer/$stopTime seconds"
		after 1000
		continue
	    }
	}
    }

    if {$portDownList != ""} {
	puts "VerifyPortState: Ports can't come up: $portDownList\n"
	exit
    }
    puts "VerifyPortState: All ports are up"
}


proc GetVportConnectedToPort { vport } {
    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
    set connectedTo [ixNet getAttribute $vport -connectedTo]
    set connectedTo [lrange [split $connectedTo /] 3 4]
    set card [lindex [split [lindex $connectedTo 0] :] end]
    set port [lindex [split [lindex $connectedTo 1] :] end]
    return $card/$port    
}

proc StartAllProtocols {} {
    puts "\nStartAllProtocols ..."
    catch {ixNet exec startAllProtocols} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "\nStartAllProtocols failed: $errMsg\n"
	return 1
    }
    ixNet commit
    after 5000
    return 0
}

proc VerifyProtocolSessions {} {
    set startTimer 0
    set stopTimer 180 ;# User must set maximum overall time.
    set maxProtocolRetry 40 ;# User must set time to allow per port/protocol to come up.
    set retryProtocolAttempts 0
    set protocolFailures {}

    # All protocols: arp bfd bgp cfm eigrp elmi igmp isis lacp ldp linkOam lisp mld mplsOam mplsTp ospf ospfV3 pimsm ping rip ripng rsvp static stp
    
    # $viewList = {::ixNet::OBJ-/statistics/view:"Port Statistics"} {::ixNet::OBJ-/statistics/view:"Tx-Rx Frame Rate Statistics"} {::ixNet::OBJ-/statistics/view:"Port CPU Statistics"} {::ixNet::OBJ-/statistics/view:"Global Protocol Statistics"} {::ixNet::OBJ-/statistics/view:"BGP Aggregated Statistics"} {::ixNet::OBJ-/statistics/view:"BGP Aggregated State Counts"} {::ixNet::OBJ-/statistics/view:"LDP Aggregated Statistics"} {::ixNet::OBJ-/statistics/view:"LDP Aggregated State Counts"} {::ixNet::OBJ-/statistics/view:"OSPF Aggregated Statistics"} {::ixNet::OBJ-/statistics/view:"OSPF Aggregated State Counts"}

    set viewList [ixNet getList [ixNet getRoot]/statistics view]

    # Suck out all the "protocol aggregated statistics" only
    # FYI: The alignment of each stat row/column is exactly the same as IxNetwork GUI
    set protocolList {}
    foreach item $viewList {
	if {[regexp -nocase "statistics/view:\"(\[^ ]+) aggregated statistics" $item - theProtocol]} {
	        lappend protocolList $theProtocol
	}
    }

    foreach protocol $protocolList {
	set flowStatsViewIndex [lsearch -regexp $viewList "$protocol aggregated statistics"]
	if {$flowStatsViewIndex != -1} {
	    set view [lindex $viewList $flowStatsViewIndex]
	        
	        ixNet setAttribute $view -enabled true
	        ixNet commit

	        set loopProtocol 0
	        set retryProtocolAttempts 0

	    while {$startTimer < $stopTimer} {
		set pageList [ixNet getAttribute $view/page -rowValues]
		
		puts "\nVerifying Protocol status: $protocol"
		
		foreach stats $pageList {
		    set stats [lindex $stats 0]
		    set cardAndPortNumber [string map {" " /} [lrange [split [lindex $stats 0] /] 1 2]]

		        # BGP  session UP stat = column 3 on gui
		        # LDP  session UP stat = column 2 on gui
		        # OSPF session UP stat = column 3 on gui
		        
		    if {[regexp -nocase "bgp" $protocol]} {
			set sessionStatus [lindex $stats 2]
		    }
		    if {[regexp -nocase "ldp" $protocol]} {
			set sessionStatus [lindex $stats 1]
		    }
		    if {[regexp -nocase "ospf" $protocol]} {
			set sessionStatus [lindex $stats 2]
		    }
		        
		    if {$sessionStatus > 0} {
			set protocolStatus up
		    } else {
			set protocolStatus down
			set loopProtocol 1
			incr retryProtocolAttempts
		    }    
		        puts"\t$cardAndPortNumber $protocol status=$protocolStatus"
		}

		if {$loopProtocol == 1} {
		        after 2000
		        incr startTimer 2
		        puts "\t\tTotal wait time for all protocols to come up:  $startTimer/$stopTimer seconds ..."
		        puts "\t\tAllowing $protocol $maxProtocolRetry seconds to come up. $retryProtocolAttempts/$maxProtocolRetry"
		        set currentTimer $startTimer
		        set loopProtocol 0
		    if {$retryProtocolAttempts == $maxProtocolRetry} {
			set retryProtocolAttempts 0
			lappend protocolFailures "Protocol $protocol on $cardAndPortNumber did not come up"
			puts "\t\tProtocol $protocol failed to come up"
			break
		    }
		    if {$retryProtocolAttempts < $maxProtocolRetry && $startTimer == [expr $stopTimer - 2]} {
			lappend protocolFailures "Protocol $protocol on $cardAndPortNumber did not come up"
			puts "\t\tProtocol $protocol failed to come up"
		    }
		} else {
		        after 2000
		        incr startTimer 2
		        break
		}

		set startTimer $currentTimer
	    }
	}
    }

    if {$protocolFailures == ""} {
	puts "\nVerifyProtocolSessions: All protocol sessions on all ports came up"
    } else {
	puts " \nVerifyProtocolSessions: ERROR: Protocols not up: $protocolFailures"
	exit
    }
}

proc VerifyAllProtocolSessionsNgpf {} {
    # This API will loop through each created Topology Group and verify
    # all the created protocols for session up for up to 90 seconds total.
    # 
    # Returns 0 if all sessions are UP.
    # Returns 1 if any session remains DOWN after 90 seconds.
    
    set protocolList [list ancp \
			bfdv4Interface \
			    bgpIpv4Peer \
			    dhcpv4relayAgent \
			    dhcpv4server \
			    geneve \
			    greoipv4 \
			    igmpHost \
			    igmpQuerier \
			    lac \
			    ldpBasicRouter \
			    ldpConnectedInterface \
			    ldpTargetedRouter \
			    lns \
			    openFlowController \
			    openFlowSwitch \
			    ospfv2 \
			    ovsdbcontroller \
			    ovsdbserver \
			    pcc \
			    pce \
			    pcepBackupPCEs \
			    pimV4Interface \
			    ptp \
			    rsvpteIf \
			    rsvpteLsps \
			    tag \
			    vxlan \
			   ]
    
    set sessionDownList [list down notStarted]
    set startCounter 1
    set timeEnd 120

    foreach protocol $protocolList {
        foreach topology [ixNet getList [ixNet getRoot] topology] {
            foreach deviceGroup [ixNet getList $topology deviceGroup] {
                foreach ethernet [ixNet getList $deviceGroup ethernet] {
                    foreach ipv4 [ixNet getList $ethernet ipv4] {   
                        foreach currentProtocol [ixNet getList $ipv4 $protocol] {

                            for {set timer $startCounter} {$timer <= $timeEnd} {incr timer} {
                                set currentStatus [ixNet getAttribute $currentProtocol -sessionStatus]
                                puts "\n$currentProtocol"
				puts "\tCurrent status: $currentStatus"
                                puts "\tTotal sessions: [llength $currentStatus)]"

                                set totalDownSessions 0
                                foreach eachStatus $currentStatus {
                                    if {$eachStatus != "up"} {
                                        incr totalDownSessions
				    }
				}
				puts "\tTotal sessions Down: $totalDownSessions"

				if {$timer < $timeEnd} {
				    foreach element $sessionDownList {
					puts "\n--- $element: [lsearch $currentStatus $element]"
					if {[lsearch $currentStatus $element] == -1}  {
					    puts "\tProtocol sessions are all up"
					    set startCounter $timer
					    break
					}
				    }
				}

				if {$timer < $timeEnd} {
				    foreach element $sessionDownList {
					if {[lsearch $currentStatus $element] != -1} {
					    puts "\tWait $timer/$timeEnd seconds"
					    after 1000
					}
				    }
				}

				if {$timer == $timeEnd} {
				    foreach element $sessionDownList {
					if {[lsearch $currentStatus $element] != -1} {
					    puts "\tProtocol session failed to come up:"
					    return 1
					}
				    }
				}
			    }
			}
		    }
		}
	    }
	}
    }
    return 0
}


proc StartTraffic { {includeApplyTraffic apply} } {
    # Need to make apply traffic an optional parameter because
    # not every situation can except apply traffic prior to 
    # starting traffic such as packet capture.  
    # If apply traffic for packet capture, it will stop the packet
    # capture. This is a HLT bug as of HLT 4.90

    set traffic [ixNet getRoot]traffic

    if {$includeApplyTraffic == "apply"} {
	if {[ApplyTraffic] == 1} {
	        return 1
	} 
    }

    puts "StartTraffic ..."
    for {set retry 1} {$retry <= 10} {incr retry} {
	catch {ixNet exec start $traffic} errMsg
	if {$retry < 10 && $errMsg != "::ixNet::OK"} {
	        puts "\nStartTraffic: Not ready yet. Retry $retry/10: $errMsg"
	        after 1000
	}
	if {$retry == 10 && $errMsg != "::ixNet::OK"} {
	        puts "\nStartTraffic: Failed: $errMsg\n"
	        return 1
	}
	if {$retry < 10 && $errMsg == "::ixNet::OK"} {
	        puts "\nStartTraffic: Traffic started\n"
	        break
	}
    }
    
    VerifyTrafficState
    
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
    puts "\n$columnList\n"
    
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
    puts "\ntotal Pages: $totalPages"

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
		
		#puts "\n--- cellList $pageListIndex: $cellList ---\n"
		puts "  $row:"
		for {set index 0} {$index <[llength $cellList]} {incr index} {
		    keylset getStats flow.$row.[join [lindex $columnList $index] _] [lindex $cellList $index] 
		    puts "\t[lindex $columnList $index]: [lindex $cellList $index]"
		}
	    }
	}
    }  
    ixNet setAttribute $view -enabled false
    ixNet commit

    return $getStats
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

Connect $apiServerIp $ixNetworkVersion
#VerifyProtocolSessions

LoadConfigFile $configFile
VerifyPortState
StartAllProtocols
#VerifyAllProtocolSessionsNgpf
after 30000
RegenerateAllTrafficItems
StartTraffic

set stats [GetStats]
puts [KeylPrint stats]

ixNet disconnect


