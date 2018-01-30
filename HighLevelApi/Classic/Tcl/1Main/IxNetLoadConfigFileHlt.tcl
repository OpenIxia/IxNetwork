#!/opt/ActiveTcl-8.5/bin/tclsh

# This script has two different methods to load a preconfigured
# IxNetwork file.
#
#    1> Loads the config file and use the saved config ports.
#    2> Loads the config file, but use different ports.
#       NOTE:  If the saved config file uses 3 ports, then user
#              must provide a list with 3 ports. 
#            
# Included APIs:
#
#   DebugHlt
#       Call this API to create a log file of HLT commands executed for debugging.
#
#   VerifyPortState
#   RegenerateAllTrafficItems
#   DisableTrafficItem <Traffic Item name>
#   EnableTrafficItem  <Traffic Item name>
#   StartAllProtocols
#   StopAllProtocols
#   SendArpHlt  
#   VerifyArpDiscoveries
#   StartTrafficHlt
#   GetStatsHlt


package req Ixia

set ixiaChassisIp 10.219.117.101
set ixNetworkTclServerIp 10.219.117.103
set userName hgee
set portList "1/1 1/2"
set port1 1/1/1
set port2 1/1/2
set ixncfgFile /home/hgee/Dropbox/MyIxiaWork/Temp/basicIpv4.ixncfg
#set ixncfgFile c:\\ScriptGen\\l2l3.ixncfg


if {[file exists $ixncfgFile] == 0} {
    puts "\n\n** ixNet config file does not exists: $ixncfgFile\n\n"
    exit
} else {
    puts "\nFile exists: $ixncfgFile\n"
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

proc VerifyArpDiscoveries { {ExitTest doNotExitTest} } {
    # This API is for Protocol Interface arp discovery. Not for NGPF.

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

    puts "\nVerifyArpDiscoveries: Expected ARPs to be resolved:\n"
    foreach arp $allIpGateways {
	puts "\t$arp"
    }
    puts \n

    foreach vP [ixNet getList [ixNet getRoot] vport] {
	# Get all the discovered ARPs for the current vPort
	set vPortInterfaceList [ixNet getList $vP discoveredNeighbor]
	
	if {$vPortInterfaceList != ""} {
	    set currentPort [GetVportConnectedToPort $vP]

	    # vPortInt = ::ixNet::OBJ-/vport:1/discoveredNeighbor:1
	    foreach vPortInt $vPortInterfaceList {
		set currentVp [join [lrange [split $vPortInt /] 0 1] /]
		
		set discoveredIp [ixNet getAttribute $vPortInt -neighborIp]
		set discoveredMac [ixNet getAttribute $vPortInt -neighborMac]
		
		puts "VerifyArpDiscoveries: Discovered arp on $currentPort: $discoveredIp : $discoveredMac"
		
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
	puts "\nVerifyArpDiscoveriesArp: Unresolved Arps:"
	foreach unresolvedArp $allIpGateways {
	    puts "\t$unresolvedArp"
	}

	puts \n
	puts "VerifyArpDiscoveries: Unresolved arps: $allIpGateways"
	return 1
    } else {
	puts "\nVerifyArpDiscoveries: All arps are resolved"
	return 0
    }
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
	return 1
    }
    after 3000
    return 0
}

proc RegenerateAllTrafficItems {} {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	catch {ixNet exec generate $trafficItem} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "RegenerateAllTrafficItem: Failed on $trafficItem"
	    return 1
	}
	puts "RegenerateAllTrafficItem: $trafficItem"
    }
    puts "RegenerateAllTrafficItem: Done"
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

proc StartTrafficHlt {} {
    puts "\nStarting IxNetwork traffic ..."
    set status [ixia::traffic_control -action run]
    
    if {[keylget status status] != $::SUCCESS} {
	puts "\nIxia traffic failed to start: $status"
    } else {
	puts "\nTraffic started ..."
    }

    after 10000
}

proc GetStatsHlt { {type flow} } {
    puts "\nGetStatsHlt"
    set flowStats [::ixia::traffic_stats -mode $type]
    
    if {[keylget flowStats status] != $::SUCCESS} {
	puts "GetStatsHlt failed: $status"
	return 0
    }
    return $flowStats
}

proc GetTrafficItemByName { trafficItemName } {
    # Search for the exact Traffic Item name and return the Traffic Item object"

    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set currentTiName [ixNet getAttribute $trafficItem -name]

	if {[regexp "(TI\[0-9]+)?$trafficItemName$" $currentTiName]} {
	    return $trafficItem
	}
    }
    # Retuning 0 if not found
    return 0
}

proc EnableTrafficItem { Name } {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set trafficItemName [ixNet getAttribute $trafficItem -name]

	if {[regexp "(TI\[0-9]+-)?$Name" $trafficItemName]} {
	    catch {ixNet setAttribute $trafficItem -enabled True} errMsg
	    if {$errMsg != "::ixNet::OK"} {
		puts "\nEnableTrafficItemByName: $Name : Failed\n:$errMsg\n"
		return 1
	    }

	    ixNet commit
	    puts "\nEnableTrafficItemByName: $Name : Done\n"
	    return 0
	} 
    }

    puts "\nEnableTrafficItemByName: No such traffic item name: $Name\n"
    return 1
}

proc DisableTrafficItem { Name } {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set trafficItemName [ixNet getAttribute $trafficItem -name]

	if {[regexp "(TI\[0-9]+-)?$Name" $trafficItemName]} {
	    catch {ixNet setAttribute $trafficItem -enabled False} errMsg
	    if {$errMsg != "::ixNet::OK"} {
		puts "\nDisableTrafficItemByName: $Name : Failed\n$errMsg\n"
		return 1
	    }

	    ixNet commit
	    puts "\nDisableTrafficItemByName: $Name : Done\n"
	    return 0
	}
    }

    puts "\nDisableTrafficItemByName: No such traffic item name: $Name\n"
    return 1
}

proc ModifyStreamFrameSizeHlt { trafficItemName framesize } {
    # trafficItemName = The Traffic Item name in exact spelling.
    # framesize = The framesize value to modify.

    # Note: The stream_id format = ::ixNet::OBJ-/traffic/trafficItem:1

    set trafficItem [GetTrafficItemByName $trafficItemName]
    if {$trafficItem == "" || $trafficItem == "0"} {
	puts "\nError ModifyStreamTransmitModeHlt: No such Traffic Item name: $trafficItemName"
	return 1
    }

    puts "\nModifyFrameSizeHlt: $trafficItem : $framesize"
    set trafficItemStatus [::ixia::traffic_config \
			      -mode modify \
			      -stream_id $trafficItem \
			      -frame_size $framesize \
			      ]

    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError ModifyFrameSizeHlt: $trafficItemStatus\n"
	return 1
    }
    return 0
}

proc ModifyStreamLineRateHlt { trafficItemName ratePercentage } {
    # streamId format = ::ixNet::OBJ-/traffic/trafficItem:1

    set trafficItem [GetTrafficItemByName $trafficItemName]
    if {$trafficItem == "" || $trafficItem == "0"} {
	puts "\nError ModifyStreamTransmitModeHlt: No such Traffic Item name: $trafficItemName"
	return 1
    }

    puts "\nModifyStreamLineRateHlt: $streamId : $ratePercentage\%"
    set trafficItemStatus [eval ::ixia::traffic_config \
			       -mode modify \
			       -stream_id $trafficItem \
			       -rate_percent $ratePercentage \
			      ]
    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError ModifyStreamLineRateHlt: $trafficItemStatus\n"
	return 1
    }
    return 0
}

proc StartAllProtocols {} {
    puts "\nStartAllProtocols ..."
    catch {ixNet exec startAllProtocols} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "\nStartAllProtocols failed: $errMsg\n"
	return 1
    }
    ixNet commit
    after 10000
    return 0
}

proc StopAllProtocols {} {
    puts"StopAllProtocols ..."
    catch {ixNet exec stopAllProtocols} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "StopAllProtocols failed: $errMsg\n"
	return 1
    }
    ixNet commit
    after 10000
    return 0
}

proc SendArpHlt { ports } {
    # This API will send ARP out of all the ports in -port_handle.
    # Only for Protocol Interface configuration.
    # Returns the Arp results.

    puts "\nSendArpHlt: $ports"
    set arpStatus [::ixia::interface_config -mode modify -port_handle $ports -arp_send_req 1 -arp_req_retries 3]
    puts "\n[KeylPrint arpStatus]\n"
    return $arpStatus
}

proc DebugHlt { {debugFileName ixiaHltDebug.log} } {
    # Uncomment these lines for debugging.
    # This will create a log file for Ixia support to help you debug.
    #set ::ixia::debug 1
    #set ::ixia::debug_file_name $debugFileName

    file delete $debugFileName
    set ::ixia::logHltapiCommandsFlag 1
    set ::ixia::logHltapiCommandsFileName $debugFileName
}

proc Connect { {type useConfigFilePorts} } {
    # Options:
    #    type = useConfigFilePorts | remapPorts
    #   
    #    Defaults to using ports in the saved config file

    if {[file exists $::ixncfgFile] == 0} {
	puts "\n\n** ixNet config file does not exists: $::ixncfgFile\n\n"
	exit
    }

    puts "\nLoading config file: $::ixncfgFile ..."

    # BUG on IxOS 6.70/IxNet 7.30.  You must include -tcl_server.
    #     If IxNet Windows isn't running IxOS tcl server, it won't
    #     default to the Ixia chassis's IxOS tcl server.
    if {$type != "useConfigFilePorts"} {
	puts "Remapping ports"
	set connectStatus [::ixia::connect \
			       -device $::ixiaChassisIp \
			       -tcl_server $::ixiaChassisIp \
			       -port_list $::portList \
			       -ixnetwork_tcl_server $::ixNetworkTclServerIp \
			       -username $::userName \
			       -config_file $::ixncfgFile \
			       -break_locks 1 \
			       -session_resume_keys 1 \
			      ]
    }

    # NOTE: This requires -tcl_server <ip address> if the ixNet 
    #       Tcl server is not running IxOS Tcl Server.
    if {$type == "useConfigFilePorts"} {
	puts "Loading saved config ports: $::portList"
	set connectStatus [::ixia::connect \
			       -tcl_server $::ixiaChassisIp \
			       -config_file $::ixncfgFile \
			       -ixnetwork_tcl_server $::ixNetworkTclServerIp \
			       -session_resume_keys 1 \
			       -connect_timeout 30 \
			       -break_locks 1 
			  ]
    }

    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "Connecting to IxNetwork Tcl server failed\n\n$connectStatus\n"
	exit
    } else {
	puts "Successfully connected to IxNetwork Tcl server"
    }
    
    puts "\n[KeylPrint connectStatus]\n"
    return $connectStatus
}

#DebugHlt

Connect

if {[VerifyPortState]} {
    exit
}

SendArpHlt "$port1 $port2"

if {[VerifyArpDiscoveries]} {
    exit
}

RegenerateAllTrafficItems

DisableTrafficItem "TrafficItem_1"
after 3000
EnableTrafficItem "TrafficItem_1"

# StartAllProtocols

StartTrafficHlt
set flowStats [GetStatsHlt flow]
puts "\n[KeylPrint flowStats]\n"

puts "[format %-10s FlowGroup][format %10s TxPort][format %10s RxPort][format %14s TxFrames][format %14s RxFrames]"
puts "------------------------------------------------------------------------"

for {set flowNumber 1} {$flowNumber <= [llength [keylget flowStats flow]]} {incr flowNumber} {
    set txPort [keylget flowStats flow.$flowNumber.tx.port]
    set rxPort [keylget flowStats flow.$flowNumber.rx.port]
    set txFrames [keylget flowStats flow.$flowNumber.tx.total_pkts]
    set rxFrames [keylget flowStats flow.$flowNumber.rx.total_pkts]
    
    set flowName [keylget flowStats flow.$flowNumber.flow_name]
  
    puts "[format %5s $flowNumber][format %15s $txPort][format %10s $rxPort][format %14s $txFrames][format %14s $rxFrames]"
}



