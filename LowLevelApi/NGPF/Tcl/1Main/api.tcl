proc Connect {apiServerIp ixNetworkVersion {apiKey None}} {
    # apiServerIp: The IxNetwork API server
    # ixNetworkVersion: The IxNetwork version
    # apiKey: For connecting to Linux API server only.

    puts "\nConnecting to $apiServerIp"
    if {$apiKey == "None"} {
	set connectStatus [ixNet connect $apiServerIp -version $ixNetworkVersion]
    } else {
	set connectStatus [ixNet connect $apiServerIp -version $ixNetworkVersion -apiKey $apiKey]
    }
    puts "\nconnectStatus: $connectStatus"
    if {$connectStatus != "::ixNet::OK"} {
	puts "\nConnect failed $apiServerIp"
	return 1
    }
    return 0
}

proc ConnectToIxChassis {ixChassisIp} {
    puts "\nAdding a chassis"
    set chassisObj [ixNet add [ixNet getRoot]/availableHardware "chassis"]
    set chassisObj [ixNet remapIds $chassisObj]
    puts "Chassis object: $chassisObj"

    puts "\nConnectToIxChassis: $ixChassisIp"
    set status [ixNet setAttribute $chassisObj -hostname $ixChassisIp]
    puts "Connecting to chassis status: $status"
    ixNet commit

    puts "\nGet chassis info"
    set status [ixNet getList [ixNet getRoot]/availableHardware chassis]
    puts "Chassis: $status"
}

proc GetApiKey {apiServerIp {username admin} {password admin} {apiKeyFilePath ./apiKeyFile}} {
    # apiServerIp: The IxNetwork API server IP
    # username: The Linux API server login username
    # password: The Linux API server login password
    # apiKeyFilePath: The file path to store the api-key.

    if {[catch {set apiKey [ixNet getApiKey $apiServerIp -username $username -password $password -apiKeyFile .$apiKeyFilePath]} errMsg]} {
	puts "\nError: Login to Linux API server $apiServerIp failed as $username/$password"
	return 1
    }
    return $apiKey
}

proc LoadConfigFile {configFile} {
    # configFile: The confile file to load

    puts "\nLoading config file: $configFile"
    set result [ixNet execute loadConfig [ixNet readFrom $configFile]]
    puts "\nresult: $result"
    if {$result != "::ixNet::OK"} {
	puts "\nError: Loading config file: $configFile"
	return 1
    }
    after 8000
    return 0
}

proc GetVportPhyPort {vport {returnValue addSlash}} {
    # vport: ::ixNet::OBJ-/vport:1
    # returnValue: 
    #    addSlash: Return port format 1/2
    #    noSlash:  Return port format "1 1"

    set connectedTo [ixNet getAttribute $vport -connectedTo]
    set card [lindex [split [lindex [split $connectedTo /] 3] :] end]
    set portNum [lindex [split [lindex [split $connectedTo /] 4] :] end]
    if {$returnValue == "addSlash"} {
	set port $card/$portNum
    } else {
	set port "$card $portNum"
    }
    return $port
}

proc GetPortsAndAssignPorts {ixChassisIp} {
    set portList {}
    set vportList [ixNet getList [ixNet getRoot] vport]
    foreach vport $vportList {
	set port [GetVportPhyPort $vport noSlash]
	lappend portList [list $ixChassisIp [lindex $port 0] [lindex $port 1]]
    }
    puts "\nGetPortsAndAssignPorts"
    puts "\t[list $portList]"
    puts "\t[list $vportList]" 
    ixTclNet::AssignPorts $portList {} $vportList true
}

proc ClearPortOwnership {portList} {
    # portList: [list "$ixChassisIp $cardNum $portNum" ...]

    foreach port $portList {
	set ixChassisIp [lindex $port 0]
	set cardId [lindex $port 1]
	set portId [lindex $port 2]
    
	puts "\nClearPortOwnership: $ixChassisIp/$cardId/$portId"
	set chassisObj [lindex [ixNet getList [ixNet getRoot]/availableHardware chassis] end]
	puts "\n--- chassisObj: $chassisObj"
	if {[catch {ixNet exec clearOwnership [ixNet getRoot]/availableHardware/chassis:"$ixChassisIp"/card:$cardId/port:$portId} errMsg]} {
	    puts $errMsg
	}
    }
}

proc ReleaseAllPorts {} {
    puts "\nReleaseAllPorts"
    set status [ixNet exec releaseAllPorts]
    puts $status
}

proc ReleasePorts {portList} {
    # portList: [list "$ixChassisIp $cardNum $portNum" ...]

    puts "\nReleasePorts: $portList"
    set vportList [ixNet getList [ixNet getRoot] vport]
    foreach vport $vportList {
	puts $vport
	# chassis="192.168.70.11" card="1" port="1" portip="192.168.70.12"
	set assignedTo [ixNet getAttribute $vport -assignedTo]
	puts "assignedTo: $assignedTo"
	set chassisIp [string map {\" ""}  [lindex [split $assignedTo :] 0]]
	set cardId [string map {\" ""} [lindex [split $assignedTo :] 1]]
	set portId [string map {\" ""} [lindex [split $assignedTo :] 2]]

	if {[lsearch -regexp $portList "$chassisIp $cardId $portId"] != -1} {
	    puts "\nReleasePorts: $chassisIp/$cardId/$portId"
	    set status [ixNet exec releasePort $vport]
	    puts $status
	}
    }
}

proc ConfigLicenseServer {{licenseServerIp None} {licenseMode None} {licenseTier None} } {
    # licenseServerIp: The license server IP.
    # licenseMode: subscription | perpetual| mixed
    # licenseTier: tier1 | tier2 | tier3 ...

    if {$licenseServerIp != "None"} {
	puts "\nConfiguring license server: $licenseServerIp"
	set status [ixNet setAttribute [ixNet getRoot]/globals/licensing -licensingServers $licenseServerIp]
	puts $status
    }
    if {$licenseMode != "None"} {
	puts "\nConfiguring license mode: $licenseMode"
	set licenseServer [ixNet setAttribute [ixNet getRoot]/globals/licensing -mode $licenseMode]
	puts $status
    }
    if {$licenseServerIp != "None"} {
	puts "\nConfiguring license tier: $licenseTier"
	set licenseServer [ixNet setAttribute [ixNet getRoot]/globals/licensing -tier $licenseTier]
	puts $status
    }
    ixNet commit
}

proc VerifyPortState { {StopTimer 120} } {
    set portDownList {}
    set startTimer 1
    set stopTime $StopTimer
    puts \n
    foreach vPort [ixNet getList [ixNet getRoot] vport] {
	puts "\nvPort: $vPort"
	set port [GetVportConnectedToPort $vPort]
	for {set timer $startTimer} {$timer <= $stopTime} {incr timer} {
	    if {$timer == $stopTime} {
		lappend portDownList $port
	    }
	    if {[ixNet getAttribute $vPort -state] == "up"} {
		puts "VerifyPortState: $port is up"
		break
	    } else {
		puts "VerifyPortState: $port is still not up. Waited $timer/$stopTime seconds"
		after 1000
		continue
	    }
	}
       set startTimer $timer
    }

    if {$portDownList != ""} {
	puts "VerifyPortState: Ports can't come up: $portDownList\n"
	return 1
    }
    return 0
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

proc VerifyAllProtocolSessionsNgpf {} {
    # This API will loop through each created Topology Group and verify
    # all the created protocols for session up for up to 90 seconds total.
    # 
    # Returns 0 if all sessions are UP.
    # Returns 1 if any session remains DOWN after 90 seconds.

    # TODO: Create an IPv6 protocol list to also support IPv6
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
				# up up
                                set currentStatus [ixNet getAttribute $currentProtocol -sessionStatus]
                                puts "\n$currentProtocol"
                                puts "\tTotal sessions: [llength $currentStatus)]"
				puts "\tCurrent session status: $currentStatus"

                                set totalDownSessions 0
                                foreach eachStatus $currentStatus {
                                    if {$eachStatus != "up"} {
                                        incr totalDownSessions
				    }
				}
				puts "\tTotal sessions Down: $totalDownSessions"

				if {$timer < $timeEnd} {
				    if {[lsearch $currentStatus notStarted] != -1} {
					puts "\tSession not started. Wait $timer/$timeEnd seconds"
					after 1000
					continue
				    }

				    if {[lsearch $currentStatus down] == -1}  {
					puts "\tAll sessions are all up"
					set startCounter $timer
					set breakFlag 1
					break
				    }

				    if {$timer < $timeEnd} {
					foreach element $sessionDownList {
					    if {[lsearch $currentStatus $element] != -1} {
						puts "\tSessions are started, but still down. Wait $timer/$timeEnd seconds"
						after 1000
					    }
					}
				    }
				}

				if {$timer == $timeEnd} {
				    foreach element $sessionDownList {
					if {[lsearch $currentStatus $element] != -1} {
					    puts "\tProtocol session failed to come up after $timeEnd seconds"
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



proc StartTraffic { {includeApplyTraffic apply} } {
    # Need to make apply traffic an optional parameter because
    # not every situation can except apply traffic prior to 
    # starting traffic such as packet capture.  
    # If apply traffic for packet capture, it will stop the packet
    # capture.

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
    
    if {[VerifyTrafficState]} {
	return 1
    }
    
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
	        return 0
	}

	if {$trafficState == "stopped"} {
	        puts "VerifyTrafficState: Traffic stopped"
	        return 0
	}

	if {$trafficState == "startedWaitingForStats" || $trafficState == "stoppedWaitingForStats"} {
	        puts "VerifyTrafficState: Traffic started. Waiting for stats to complete"
	        return 0
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
    # Pretty print key list

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

