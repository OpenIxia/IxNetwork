proc ConnectToIxia { connectParams } {
    puts "\nConnectToIxia: $connectParams"

    puts "Resetting Ixia ports. Please wait 40 seconds ..."
    set connectStatus [eval ::ixia::connect $connectParams]

    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "\nError: ConnectToIxia failed: $connectStatus\n"
	return 1
    } else {
	return $connectStatus
    }
}

proc PortConfigProtocolInt { portConfigParams } {
    set interfaceConfigStatus [eval ::ixia::interface_config $portConfigParams]
    
    if {[keylget interfaceConfigStatus status] != $::SUCCESS} {
	puts "\nError: PortConfigProtocolList failed:\n$interfaceConfigStatus\n"
    }

    # interface object = ::ixNet::OBJ-/vport:1/interface:1
    set interfaceHandle [keylget interfaceConfigStatus interface_handle]
    return $interfaceHandle
}

proc CreateTrafficItem { trafficItemParams } {
    # For non-full-mesh:        -src_dest_mesh one_to_one
    # For full-mesh:            -src_dest_mesh fully
    # For continuous traffic:   -transmit_mode continuous
    # For single burst traffic: -transmit single_burst -number_of_packets-per_stream 50000

    puts "\nCreating new Traffic Item ..."
    set trafficItemStatus [eval ::ixia::traffic_config $trafficItemParams]

    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError: Traffic Item config failed: $trafficItemStatus\n"
	return 1
    }

    return $trafficItemStatus
}

proc StartTrafficHlt {} {
    puts "\nStarting all traffic"
    set startTrafficStatus [::ixia::traffic_control \
				-action run \
			       ]
    if {[keylget startTrafficStatus status] != $::SUCCESS} {
	puts "\nError: Failed to start traffic: $startTrafficStatus\n"
	return 1
    } 
    puts "\n$startTrafficStatus"

    # By including VerifyTrafficState, it will wait up to 15 seconds until
    # traffic is started before returning.
    VerifyTrafficState
    return 0
}

proc CheckTrafficState {} {
    # This API is mainly used by VerifyTrafficState.
    # Users can also use this in their scripts to check traffic state.

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
	    puts "CheckTrafficState: Traffic state is currently: $currentTrafficState"
	}
    }
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
	    puts "Traffic Started"
	    break
	}

	if {$trafficState == "stopped"} {
	    puts "Traffic stopped"
	    break
	}

	if {$trafficState == "startedWaitingForStats" || $trafficState == "stoppedWaitingForStats"} {
	    puts "Traffic started. Waiting for stats to complete"
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
}

proc GetStatsHlt { {type flow} } {
    set flowStats [::ixia::traffic_stats \
		       -mode $type \
		      ]
    if {[keylget flowStats status] != $::SUCCESS} {
	puts "Failed to get statistics"
	exit
    }
    return $flowStats
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
