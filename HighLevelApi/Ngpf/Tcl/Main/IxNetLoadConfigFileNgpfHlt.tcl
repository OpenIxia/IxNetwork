#!/opt/ActiveTcl-8.5/bin/tclsh

# This script has two different methods to load a preconfigured
# IxNetwork file, in which one of them is commented out.
#
#    1> Loads the config file, but use different ports.
#          Connect remapPorts
#    2> Loads the config file and use the saved config ports.
#          Connect useConfigFilePorts
#
# Included APIs:
#
#   DebugHlt
#       Call this API to create a log file of HLT commands executed for debugging.
#
#   Connect <remapPorts | useConfigFilePorts> 
#       remapPorts         = Use different ports other than the saved config ports.
#       useConfigFilePorts = Use the Ixia chassis and ports in the saved config file.
#
#   VerifyPortState
#   RegenerateAllTrafficItems
#   DisableTrafficItem "<Traffic Item name>"
#   EnableTrafficItem  "<Traffic Item name>"
#   StartAllProtocolsHlt
#   StopAllProtocolsHlt
#
#   SendArpOnAllActiveIntNgpf  
#   VerifyArpNgpf
#   StartTrafficHlt
#   GetStatsHlt

package req Ixia

set ixiaChassisIp 10.219.117.101
set ixNetworkTclServerIp 10.219.16.219
set userName hgee
set portList "1/1 1/2"
set port1 1/1/1
set port2 1/1/2

set ixncfgFile /home/hgee/Dropbox/MyIxiaWork/Temp/ospf_ngpf_7.40.ixncfg


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

proc ApplyTraffic {} {
    puts "\nApplyTraffic ..."
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
	    puts "\nError ApplyTraffic: $errMsg\n"
	    return 1
	}
	if {$errMsg == "::ixNet::OK" && $startCounter < $stopCounter} {
	    puts "ApplyTraffic: Successfully applied traffic to hardware."
	    break
	}
    }
    after 2000
    return 0
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
    after 5000
    return 0
}

proc GetTopologyPorts { topologyName } {
    # Gets all the ports associated with the Topology

    foreach topology [ixNet getList [ixNet getRoot] topology] {
	set currentName [ixNet getAttribute $topology -name]
	if {$currentName == $topologyName} {
	    set topologyVports [ixNet getAttribute $topology -vports]
	    set portList {}
	    foreach vport $topologyVports {
		lappend portList [GetVportConnectedToPort $vport]
	    }
	}
    }
    if {[info exists portList]} {
	return $portList
    } else {
	return
    }
}

proc SendArpNgpf { deviceGroup } {
    puts "\nSendArpNgpf: $deviceGroup ..."
    ixNet exec sendArp $deviceGroup
}

proc SendArpOnAllActiveIntNgpf {} {
    # Send ARP on all active NGPF Device Groups.

    puts "\nSendArpOnAllActiveIntNgpf"
    foreach topology [ixNet getList [ixNet getRoot] topology] {
	foreach deviceGroup [ixNet getList $topology deviceGroup] {
	    if {[ixNet getAttribute $deviceGroup -status] == "started"} {
		foreach ethernet [ixNet getList $deviceGroup ethernet] {
		    foreach ipv4 [ixNet getList $ethernet ipv4] {
			SendArpNgpf $ipv4
		    }
		}
	    }
	}
    }
    after 3000
}

proc VerifyArpNgpf { {ipType ipv4} {maxRetry 3} } {
    # ipType:  ipv4 or ipv6

    # This API will verify for ARP session resolvement on 
    # every TopologyGroup/DeviceGroup and/or
    #       TopologyGroup/DeviceGroup/DeviceGroup that has protocol "enabled".
    # 
    # How it works?
    #    Each device group has a list of $sessionStatus: up or notStarted.
    #    If the deviceGroup has sessionStatus as "up", then ARP will be verified.
    #    It also has a list of $resolvedGatewayMac: MacAddress or removePacket[Unresolved]
    #    These two lists are aligned.
    #    If lindex 0 on $sessionSatus is up, then the API expects lindex 0 on $resolvedGatewayMac 
    #    to have a mac address.
    #    If not, then arp is not resolved.
    #    This script will wait up to the $maxRetry before it declares failed.
    #
    # Return 0 if ARP passes.

    # This Proc is only for VerifyArpNgpf to use internally.
    # It's created because each deviceGroup has IPv4/IPv6 and
    # a deviceGroup can create an inner deviceGroup that has IPv4/IPv6.
    proc deviceGroupProtocolStacks { deviceGroup ipType maxRetry } {
	set unresolvedArpList {}
	foreach ethernet [ixNet getList $deviceGroup ethernet] {
	    foreach ipProtocol [ixNet getList $ethernet $ipType] {
		puts "\nVerifyArpNgpf: Protocol is started: $ipProtocol"
		set flag 0
		
		set sessionStatus [ixNet getAttribute $ipProtocol -sessionStatus]
		set resolvedGatewayMac [ixNet getAttribute $ipProtocol -resolvedGatewayMac]

		# Only care for unresolved ARPs.
		for {set index 0} {$index <= [llength $resolvedGatewayMac]} {incr index} {
		    for {set timer 1} {$timer <= $maxRetry} {incr timer} {
			if {[regexp "Unresolved" [lindex $resolvedGatewayMac $index]] == 1 && \
				[lindex $sessionStatus $index] != "notStarted" && $timer < $maxRetry} {
			    # Getting in here means the interface should be up
			    set multiValueNumber [ixNet getAttribute $ipProtocol -address]
			    set ipAddrNotResolved [lindex [ixNet getAttribute [ixNet getRoot]$multiValueNumber -values] $index]

			    # /topology:2/deviceGroup:1/ethernet:1/ipv4:1 -address
			    set topologyDeviceGroupSource [ixNet getAttribute [ixNet getRoot]$multiValueNumber -source]
			    regexp "(topology:\[0-9]+)/deviceGroup:(\[0-9]+).*" $topologyDeviceGroupSource - topologyNum deviceGroupNum
			    set vport [ixNet getAttribute [ixNet getRoot]$topologyNum -vports]
			    set realPortNumber [GetVportConnectedToPort $vport]				    
			    puts "\t$topologyNum $realPortNumber $ipAddrNotResolved did not resolve ARP yet. Verifying $timer/$maxRetry tries ..."
			    
			    after 250
			}
			
			if {[regexp "Unresolved" [lindex $resolvedGatewayMac $index]] == 1 && \
				[lindex $sessionStatus $index] != "notStarted" && $timer == $maxRetry} {
			    puts "\t$topologyNum $realPortNumber $ipAddrNotResolved cannot resolve ARP after $timer/$maxRetry retries"
			    lappend unresolvedArpList "$topologyNum Port:$realPortNumber IP:$ipAddrNotResolved"
			}
		    }
		}
		
		if {$unresolvedArpList == ""} {
		    puts "\n\tARP is resolved"
		    return ""
		} else {
		    return $unresolvedArpList
		}
	    }
	}
    }
    

    set unresolvedArpList {}
    foreach topology [ixNet getList [ixNet getRoot] topology] {
	set currentTopologyName [ixNet getAttribute $topology -name]
	set topologyPorts [GetTopologyPorts $currentTopologyName]
	
	foreach deviceGroup [ixNet getList $topology deviceGroup] {
	    if {[ixNet getAttribute $deviceGroup -status] == "started"} {
		set arpResult [deviceGroupProtocolStacks $deviceGroup $ipType $maxRetry]
		if {$arpResult != ""} {
		    set unresolvedArpList [concat $unresolvedArpList $arpResult]
		}

		if {[ixNet getList $deviceGroup deviceGroup] != ""} {
		    foreach innerDeviceGroup [ixNet getList $deviceGroup deviceGroup] {
			set arpResult [deviceGroupProtocolStacks $innerDeviceGroup $ipType $maxRetry]
			if {$arpResult != ""} {
			    set unresolvedArpList [concat $unresolvedArpList $arpResult]
			}
		    }
		}
	    } else {
		puts "\nVerifyArpNgpf: Protocol not started on:\n\t$deviceGroup"
	    }
	}
    }

    if {$unresolvedArpList == ""} {
	return 0
    }

    if {$unresolvedArpList != ""} {
	puts \n
	foreach unresolvedArp $unresolvedArpList {
	    puts "VerifyArpNgpf: UnresolvedArps: $unresolvedArp"
	}
	puts \n
	return unresolvedArpList
    }
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

proc StartAllProtocolsHlt {} {
    puts "\nStartAllProtocolsHlt"
    set startProtocolStatus [::ixiangpf::test_control -action start_all_protocols]
    if {[keylget startProtocolStatus status] != $::SUCCESS} {
	puts "\nError: StartAllProtocolsHlt failed:  $startProtocolStatus\n"
	return 1
    }

    after 3000
    return 0
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

    if {$type != "useConfigFilePorts"} {
	puts "Using saved config file ports"
	set connectStatus [::ixiangpf::connect \
			       -device $::ixiaChassisIp \
			       -port_list $::portList \
			       -ixnetwork_tcl_server $::ixNetworkTclServerIp \
			       -tcl_server $::ixiaChassisIp \
			       -username $::userName \
			       -config_file $::ixncfgFile \
			       -break_locks 1 \
			       -session_resume_keys 1 \
			       -connect_timeout 120 \
			      ]
    }

    if {$type == "useConfigFilePorts"} {
	puts "Remapping ports: $::portList"
	set connectStatus [::ixiangpf::connect \
			       -config_file $::ixncfgFile \
			       -ixnetwork_tcl_server $::ixNetworkTclServerIp \
			       -tcl_server $::ixiaChassisIp \
			       -session_resume_keys 1 \
			       -connect_timeout 120 \
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

# Uncomment this to enable HLT debugging
# DebugHlt

Connect remapPorts ;# Uncomment this to use different ports
#Connect ;# Use this to use the configuration file's ports

if {[VerifyPortState]} {
    exit
}

StartAllProtocolsHlt

puts "\nSleeping 10 seconds for protocols to come up ..."
after 10000

SendArpOnAllActiveIntNgpf

if {[VerifyArpNgpf] != 0} {
    exit
}

# --> Verify protocols on the DUT before continuing  <--

RegenerateAllTrafficItems

# Example on how to disable/enable Traffic Items
#DisableTrafficItem "Traffic Item 1"
#after 3000
#EnableTrafficItem "Traffic Item 1"

StartTrafficHlt
set flowStats [GetStatsHlt flow]

# Example on how to get certain statistics.
puts "\n[KeylPrint flowStats]\n"

puts \n
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
