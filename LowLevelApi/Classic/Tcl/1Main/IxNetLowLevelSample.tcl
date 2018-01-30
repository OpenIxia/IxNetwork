#!/usr/bin/tclsh

package req IxTclNetwork

set ixChassisIp 10.219.117.101
set ixNetworkTclServer 10.219.117.103
set ixNetworkVersion 8.0
set ixNetworkPort 8009
set portList {{1 1} {1 2} {1 5} {1 6}}
set port1 1/1
set port2 1/2
set port3 1/5
set port4 1/6

#             Port      IP   Gateway     SrcMac
set portConfig(1/1) "1.1.1.1 1.1.1.2 00:01:01:01:00:01"
set portConfig(1/2) "1.1.1.2 1.1.1.1 00:01:01:02:00:01"
set portConfig(1/5) "1.1.1.3 1.1.1.4 00:01:01:03:00:01"
set portConfig(1/6) "1.1.1.4 1.1.1.3 00:01:01:04:00:01"

proc VerifyPortState { {StopTimer 60} } {
    set portDownList {}
    set stopTime $StopTimer
    puts \n
    foreach vPort [ixNet getList [ixNet getRoot] vport] {
	set port $::getPort($vPort)
	for {set timer 1} {$timer <= $stopTime} {incr timer} {
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
    }

    if {$portDownList != ""} {
	puts "VerifyPortState: Ports can't come up: $portDownList\n"
	exit
    }
}

proc SendArp {} {
    foreach vPort [ixNet getList [ixNet getRoot] vport] {
	set port $::getPort($vPort)
	foreach interface [ixNet getList $vPort interface] {
	    # Don't send arps on Unconnected (Routed) and GRE interfaces
	    set interfaceType [ixNet getAttribute $interface -type]
	    
	    if {[regexp "default" $interfaceType]} {
		set isIntEnabled [ixNet getAttribute $interface -enabled]
		if {$isIntEnabled == "true" || $isIntEnabled == "True"} {
		    puts "Sendt ARP on $interface"
		    
		    ixNet exec sendArp $interface
		    ixNet exec sendNs $interface
		    #if {$ipv4ErrMsg != "::ixNet::OK" || $ipv6ErrMsg2 != "::ixNet::OK" } {
		    #	puts "On port $port"
		    #}
		}
	    }
	}
    }
}

proc VerifyArpDiscoveries { {ExitTest doNotExitTest} } {
    # First, get a list of all the expected Gateway IP addresses for this vPort.
    # Get only if the interface is enabled. We don't care about gateways if the
    # interface isn't enable.
    # Then get a list of all the discovered arps.
    # At the end, compare the two list. Any left overs are unresolved arps.
    
    set resolvedArp {}
    set allIpGateways {}

    foreach vP [ixNet getList [ixNet getRoot] vport] {
	# Refresh the arp table on this vport first
	ixNet execute refreshUnresolvedNeighbors $vP

	set currentVportInterfaceList [ixNet getList $vP interface]

	foreach int $currentVportInterfaceList {

	    # Ignore the Unconnected (Routed), and GRE interfaces
	    set interfaceType [ixNet getAttribute $int -type]

	    if {[regexp "default" $interfaceType]} {
		# Only lappend the Gateway if the Interface is enabled.
		set isIntEnabled [ixNet getAttribute $int -enabled]
		if {$isIntEnabled == "true" || $isIntEnabled == "True"} {
		    catch {ixNet getAttribute $int/ipv4 -gateway} ipv4GatewayReturn
		    
		    if {[regexp "null" $ipv4GatewayReturn] != 1} {
			if {[lsearch $allIpGateways $ipv4GatewayReturn] == -1} {
			    lappend allIpGateways $ipv4GatewayReturn
			}
		    }
		    
		    catch {ixNet getList $int ipv6} ipv6GatewayList
		    if {$ipv6GatewayList != ""} {
			foreach ipv6Gateway $ipv6GatewayList {
			    set ipv6 [ixNet getAttribute $ipv6Gateway -gateway]
			    
			    if {$ipv6 != "0:0:0:0:0:0:0:0"} {
				if {[lsearch $allIpGateways $ipv6] == -1} {
				    lappend allIpGateways $ipv6
				}
			    }
			}
		    }
		}
	    }
	}
    }

    puts "Expected ARPs to be resolved:\n"
    foreach arp $allIpGateways {
	puts "\t$arp"
    }
    puts \n

    foreach vP [ixNet getList [ixNet getRoot] vport] {
	# Get all the discovered ARPs for the current vPort
	set vPortInterfaceList [ixNet getList $vP discoveredNeighbor]
	
	if {$vPortInterfaceList != ""} {
	    set currentPort $::getPort($vP)

	    # vPortInt = ::ixNet::OBJ-/vport:1/discoveredNeighbor:1
	    foreach vPortInt $vPortInterfaceList {
		set currentVp [join [lrange [split $vPortInt /] 0 1] /]
		
		set discoveredIp [ixNet getAttribute $vPortInt -neighborIp]
		set discoveredMac [ixNet getAttribute $vPortInt -neighborMac]
		
		puts "Discovered arp on $currentPort: $discoveredIp : $discoveredMac"
		
		if {$discoveredMac != "" || $discoveredMac != "00:00:00:00:00:00"} {
		    if {[lsearch $allIpGateways $discoveredIp] != -1} {
			lappend resolvedArp $discoveredIp
		    }
		}
	    }
	}
    }

    # Now compare the expected list of arps with what is resolved.
    # Any left overs are unresovled arps.
    foreach resolvedGateway $resolvedArp {
	if {[lsearch $allIpGateways $resolvedGateway] != -1} {
	    set index [lsearch $allIpGateways $resolvedGateway]
	    set allIpGateways [lreplace $allIpGateways $index $index]
	}
    }

    if {$allIpGateways != ""} {
	puts "Error: Unresolved Arps:"
	foreach unresolvedArp $allIpGateways {
	    puts  "\t$unresolvedArp"
	}
	exit
    } else {
	puts "All arps are resolved"
    }
}

proc StartAllProtocols {} {
    catch {ixNet exec startAllProtocols} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "\nStartAllProtocols: Failed to start all protocols\n$errMsg"
	exit
    }
    puts "Started all protocols"
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

proc AddProtocolStack { protocol trafficItem configElementObject insertAfterIndex } {
    set index [lsearch -regexp [ixNet getList [ixNet getRoot]/traffic protocolTemplate] $protocol]
    if {$index == -1} {
	puts "No such protocol found: $protocol"
    }

    # protocolTemplate = ::ixNet::OBJ-/traffic/protocolTemplate:"udp"
    set protocolTemplate [lindex [ixNet getList [ixNet getRoot]/traffic protocolTemplate] $index]

    # ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1 
    #set configElementList [ixNet getList $trafficItem highLevelStream]

    # Example on how the protocol stack looks like for configElement:1
    # 
    # 0 = trafficItem:1/configElement:1/stack:\"ethernet-1\"
    # 1 = trafficItem:1/configElement:1/stack:\"ipv4-2\"
    # 2 = trafficItem:1/configElement:1/stack:\"udp-3\"
    # 3 = trafficItem:1/configElement:1/stack:\"fcs-4\"
    # 
    # If $insertAfterIndex = 1 (zero based indexing), then add after the ipv4 layer.
    # $addToStackLevel is ...
    #  ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ipv4-2"

    # Append after this stack -> $addToStackLevel
    set addToStackLevel [lindex [ixNet getList $configElementObject stack] $insertAfterIndex]

    puts "\tAdding [string toupper $protocol] protocol to stack layer $insertAfterIndex"
    ixNet exec append $addToStackLevel $protocolTemplate
}

proc RegenerateAllTrafficItems {} {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	catch {ixNet exec generate $trafficItem} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "RegenerateAllTrafficItem: Failed on $trafficItem"
	    exit
	}
        puts "RegenerateAllTrafficItem: $trafficItem"
    }
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
	    puts "ApplyTraffic Error: $errMsg"
	    exit
	}
	if {$errMsg == "::ixNet::OK" && $startCounter < $stopCounter} {
	    puts "Successfully applied traffic to hardware"
	    break
	}
    }
    after 2000
}

proc StartTraffic { } {
    set traffic [ixNet getRoot]traffic

    puts "Starting traffic ..."

    catch {ixNet exec start $traffic} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "Start traffic error: $errMsg"
	exit
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
		puts "Failed: Traffic failed to start"
		exit
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

proc StopTraffic {} {
    set traffic [ixNet getRoot]traffic

    catch {ixNet exec stop $traffic} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "Stop traffic error: $errMsg"
    }
    puts "Stopping traffic ..."
    after 2000
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
	    puts "CheckTrafficState: Traffic state is currently: $currentTrafficState"
	    exit
	}
    }
}

catch {ixNet connect $ixNetworkTclServer -port $ixNetworkPort -version $ixNetworkVersion} errMsg
if {$errMsg != "::ixNet::OK"} {
    puts "\nError: $errMsg"
    exit
}

catch {ixNet execute newConfig} errMsg

set ixChassis [ixNet add [ixNet getRoot]/availableHardware chassis]
ixNet setAttribue $ixChassis -hostname $ixChassisIp
set ixChassis [lindex [ixNet remapIds $ixChassis] 0]

foreach port $portList {
    set cardNumber [lindex $port 0]
    set portNumber [lindex $port 1]
    puts "Clearning port state on $cardNumber/$portNumber ..."

    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:2
    catch {ixNet execute clearOwnership "::ixNet::OBJ-/availableHardware/chassis:\"$ixChassisIp\"/card:$cardNumber/port:$portNumber"} errMsg
    if {[regexp "Unable" $errMsg]} {
	puts "Failed to clear port ownership"
	exit
    }

    set vPort [ixNet add [ixNet getRoot] vport]
    ixNet commit
    set vPort [lindex [ixNet remapIds $vPort] 0]
    lappend vPortList $vPort
    
    ixNet setAttribute $vPort \
	-connectedTo $ixChassisIp/card:$cardNumber/port:$portNumber
    #ixNet commit

    set getVport($cardNumber/$portNumber) $vPort
    set getPort($vPort) $cardNumber/$portNumber
}

puts "Assigning ports to vPort"
puts "Rebooting  all ports ..."
#ixTclNet::AssignPorts {{10.205.1.36 1 1} {10.205.1.36 1 2} {10.205.1.36 1 3} {10.205.1.36 1 4}} {} $vPortList true
ixTclNet::AssignPorts [list [list $ixChassisIp [lindex [split $port1 /] 0] [lindex [split $port1 /] 1]] \
			   [list $ixChassisIp [lindex [split $port2 /] 0] [lindex [split $port2 /] 1]] \
			   [list $ixChassisIp [lindex [split $port3 /] 0] [lindex [split $port3 /] 1]] \
			   [list $ixChassisIp [lindex [split $port4 /] 0] [lindex [split $port4 /] 1]] \
			  ] {} $vPortList true

set vportList [ixNet getList [ixNet getRoot] vport]
foreach vPort $vportList {
    set portNumber $getPort($vPort)

    set vPortInterfaceObj [ixNet add $vPort interface]
    # -type: Choices: default, routed or gre
    ixNet setMultiAttrs $vPortInterfaceObj \
	-enabled True \
	-mtu 1500 \
	-type default \
	-description "Port $getPort($vPort)"
    #ixNet commit
    set vPortInterfaceObj [lindex [ixNet remapIds $vPortInterfaceObj] 0]
    
    ixNet setAttribute $vPortInterfaceObj/ethernet -macAddress [lindex $portConfig($portNumber) 2]
    #ixNet commit

    set ipv4IntObj [ixNet add $vPortInterfaceObj ipv4]
    ixNet setMultiAttrs $ipv4IntObj \
	-gateway [lindex $portConfig($portNumber) 1]  \
	-ip [lindex $portConfig($portNumber) 0] \
	-maskWidth 24
    #ixNet commit
    set ipv4IntObj [lindex [ixNet remapIds $ipv4IntObj] 0]
}

set trafficItem1Obj [ixNet add [ixNet getRoot]/traffic trafficItem]
ixNet setMultAttrs $trafficItem1Obj \
    -enabled True \
    -name "My Traffic Item 1" \
    -routeMesh oneToOne \
    -srcDestMesh oneToOne \
    -trafficType ipv4 \
    -transmitMode interleaved \
    -biDirectional 1
#ixNet commit
set trafficItem1Obj [lindex [ixNet remapIds $trafficItem1Obj] 0]

ixNet setAttribute $trafficItem1Obj/tracking \
    -trackBy {trackingenabled0 flowGroup0 sourceDestEndpointPair0}
#ixNet commit

# vPortList: ::ixNet::OBJ-/vport:1 ::ixNet::OBJ-/vport:2 
#            ::ixNet::OBJ-/vport:3 ::ixNet::OBJ-/vport:4

puts "Creating Endpoint 1 ..."
set trafficItem1Endpoint1Obj [ixNet add $trafficItem1Obj endpointSet]
ixNet setMultiAttrs $trafficItem1Endpoint1Obj \
    -name EndPoint-1 \
    -sources ::ixNet::OBJ-/vport:1/protocols \
    -destinations ::ixNet::OBJ-/vport:2/protocols
#ixNet commit
set trafficItem1Endpoint1Obj [lindex [ixNet remapIds $trafficItem1Endpoint1Obj] 0]

puts "Creating Endpoint 2 ..."
set trafficItem1Endpoint2Obj [ixNet add $trafficItem1Obj endpointSet]
ixNet setMultiAttrs $trafficItem1Endpoint2Obj \
    -name EndPoint-2 \
    -sources ::ixNet::OBJ-/vport:3/protocols \
    -destinations ::ixNet::OBJ-/vport:4/protocols
#ixNet commit
set trafficItem1Endpoint2Obj [lindex [ixNet remapIds $trafficItem1Endpoint2Obj] 0]

foreach  traffic1ConfigElementObj [ixNet getList $trafficItem1Obj configElement] {
    # use highLevelStream to configure individual streams
    #    --> [ixNet getList $trafficItemObject highLevelStream]
    
    puts "Configuring: $traffic1ConfigElementObj"
    
    ixNet setAttribute $traffic1ConfigElementObj/frameSize -fixedSize 777
    #ixNet commit
    
    ixNet setAttribute $traffic1ConfigElementObj/frameRate -rate 75
    #ixNet commit
    
    ixNet setMultiAttrs $traffic1ConfigElementObj/framePayload \
	-type incrementByte \
	-customRepeat True \
	-customPattern {}
    #ixNet commit
    
    # -type: Choices fixedFrameCount or continuous
    ixNet setMultiAttrs $traffic1ConfigElementObj/transmissionControl -type fixedFrameCount -frameCount 25000
    #ixNet commit

    # AddProtocol Stack only if you want to add more protocl headers
    puts "trafficItemObj: $trafficItem1Obj"
    puts "configElementObj: $traffic1ConfigElementObj"
   # AddProtocolStack udp $trafficItem1Obj $traffic1ConfigElementObj 1
}

ixNet commit

VerifyPortState
RegenerateAllTrafficItems
ApplyTraffic
SendArp
VerifyArpDiscoveries
#StartAllProtocols
#VerifyProtocolSessions
StartTraffic
after 10000
StopTraffic
