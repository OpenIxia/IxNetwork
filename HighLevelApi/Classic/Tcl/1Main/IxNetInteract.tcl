#!/usr/bin/tclsh

# This script is meant to be sourced inside a tclsh shell.
# Then users have knobs to control the following APIs at anytime:
# 
# API usage:
#
#    help                       = Show all API command usage   
#    starttraffic               = Start traffic on all Trafic Items
#    stoptraffic                = Stop traffic on all Traffic Items
#    getstats                   = Show current statistics
#

package req Ixia

set ixiaChassisIp 10.205.4.172
set ixNetworkTclServerIp 10.205.1.42
set userName hgee
set portList [list 1/1 1/1]
set txPort1 1/1/1
set rxPort1 1/1/1

set intConfig(connectedInt,$txPort1,intf_ip_addr) 1.1.1.1
set intConfig(connectedInt,$txPort1,gateway)      1.1.1.254
set intConfig(connectedInt,$txPort1,src_mac_addr) 00:01:01:01:00:01
set intConfig(connectedInt,$txPort1,netmask)      255.255.255.0

set intConfig(connectedInt,$rxPort1,intf_ip_addr) 1.1.1.254
set intConfig(connectedInt,$rxPort1,gateway)      1.1.1.1
set intConfig(connectedInt,$rxPort1,src_mac_addr) 00:01:01:02:00:01
set intConfig(connectedInt,$rxPort1,netmask)      255.255.255.0

# endpoints: The 1st value is a list of all srcPorts.
#            The 2nd value is a list of all dstPorts
set trafficConfig(trafficItem,1,endpoints)    "$txPort1 $rxPort1"
set trafficConfig(trafficItem,1,bidirectional)   0
set trafficConfig(trafficItem,1,rate_percent)  100
set trafficConfig(trafficItem,1,frame_size)    64
set trafficConfig(trafficItem,1,transmit_mode) continuous
set trafficConfig(trafficItem,1,l3_protocol)   ipv4
set trafficConfig(trafficItem,1,track_by)      {traffic_item flowGroup0}

proc help {} {
    puts \n
    puts "starttraffic  = Start all ports"
    puts "stoptraffic   = Same format as starttraffic"
    puts "getstats      = Show current stats"
    puts \n
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
	set portConfigProperties {-mode config }
	append portConfigProperties "-port_handle $port "

	puts "\nInterface Config:\n\t-port_handle $port\n\t-mode config"

	foreach {properties values} [array get ::intConfig connectedInt,$port,*] {
	    set property [lindex [split $properties ,] end]
	    append portConfigProperties "-$property $values "
	    puts "\t-$property $values"
	}

	append portConfigProperties "-arp_send_req 1"

	set portStatus [eval ::ixia::interface_config $portConfigProperties]

	if {[keylget portStatus status] != $::SUCCESS} {
	    puts "\nERROR: ConfigInterfaceIp: Failed on $port: $portStatus"
	    exit
	} else {
	    puts "Successfully configured IP interface on $port:\n\n$portStatus\n"
	}
	
	set interfaceHandle [keylget portStatus interface_handle]
	
	# Build a list of all the src/dst emulation handles for Traffic Item
	# interfaceHandles: ::ixNet::OBJ-/vport:1/interface:1
	set ::trafficConfig($port,interfaceHandle) $interfaceHandle
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

		# Get and build the src port handles from the physical port number
		foreach port [lindex $endpoints 0] {
		    lappend srcEndpointHandles $::trafficConfig($port,interfaceHandle)
		}
		append trafficItemProperties "-emulation_src_handle $srcEndpointHandles "
		puts "\t-emulation_src_handle $srcEndpointHandles"

		foreach port [lindex $endpoints 1] {
		    lappend dstEndpointHandles $::trafficConfig($port,interfaceHandle)
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

proc ApplyTraffic {} {
    # This Proc is used when calling StartTrafficPort only
    # because if using HLT, HLT will apply traffic.

    puts "\nApplying configuration to hardware ..."
    set traffic [ixNet getRoot]traffic

    set stopCounter 10
    for {set startCounter 1} {$startCounter <= $stopCounter} {incr startCounter} {
	catch {ixNet exec apply $traffic} errMsg
	after 1000

	if {$errMsg != "::ixNet::OK" && $startCounter == $stopCounter} {
	    puts "ApplyTraffic ERROR: $errMsg"
	    exit
	}

	if {$errMsg == "::ixNet::OK" && $startCounter < $stopCounter} {
	    puts "Successfully applied traffic to hardware"
	    break
	}
    }
}

proc starttraffic {} {
    # Call this Proc to start all traffic.

    set traffic [ixNet getRoot]traffic

    ixNet exec start $traffic
    after 2000

    set startCounter 1
    set stopCounter 10
    for {set start $startCounter} {$start <= $stopCounter} {incr start} {
	set trafficState [CheckTrafficState]

	# Basically, if traffic state is unapplied or lock, then failed.
	if {$start == $stopCounter} {
	    if {$trafficState != "started" || $trafficState != "startedWaitingForStats" \
		    || $trafficState != "stoppedWaitingForStats" || $trafficState != "stopped"} {
		puts "ERROR: Traffic failed to start"
		exit
	    }
	}
	
	if {$trafficState == "started"} {
	    puts "Traffic Started"
	    break
	}

	if {$trafficState == "startedWaitingForStats" || $trafficState == "stoppedWaitingForStats"} {
	    puts "Traffic started"
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

proc stoptraffic {} {
    # Stop traffic on all ports

    set traffic [ixNet getRoot]traffic
    catch {ixNet exec stop $traffic} errMsg
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
	    puts "CheckTrafficState ERROR: Traffic state is currently: $currentTrafficState"
	    exit
	}
    }
}

proc ConnectToIxia { ixiaChassisIp ixNetworkTclServerIp portList userName} {
    puts "\nConnecting to $ixNetworkTclServerIp ..."
    
    puts "Wait 40 seconds. Rebooting ports $portList ..."
    set connectStatus [::ixia::connect \
			   -reset \
			   -device $ixiaChassisIp \
			   -tcl_server $ixiaChassisIp \
			   -ixnetwork_tcl_server $ixNetworkTclServerIp \
			   -port_list $portList \
			   -username $userName \
			  ]

    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "Error: Connecting to ixNetwork Tcl server failed\n\n$connectStatus\n"
	exit
    } 

    set trafficControlStatus [::ixia::traffic_control -action reset -packet_loss_duration_enable 1]
    if {[keylget trafficControlStatus status] != $::SUCCESS} {
	puts "Error: Enabling Packet Loss Duration failed: $trafficControlStatus"
	exit
    }
}

proc getstats {} {
    set flowStats [::ixia::traffic_stats \
		       -mode flow \
		      ]
    if {[keylget flowStats status] != $::SUCCESS} {
	puts "Failed to get statistics"
	exit
    }
    
    #puts [KeylPrint flowStats]
     
    for {set flowNumber 1} {$flowNumber <= [llength [keylget flowStats flow]]} {incr flowNumber} {
	set txPort [keylget flowStats flow.$flowNumber.tx.port]
	set rxPort [keylget flowStats flow.$flowNumber.rx.port]
	set txFrames [keylget flowStats flow.$flowNumber.tx.total_pkts]
	set rxFrames [keylget flowStats flow.$flowNumber.rx.total_pkts]
	set flowName [keylget flowStats flow.$flowNumber.flow_name]
	set pktLossDuration [keylget flowStats flow.$flowNumber.rx.pkt_loss_duration]
	
	puts "\nFlow Group $flowNumber\:"
	puts "\t[format %8s TxPort][format %8s RxPort][format %12s TxFrames][format %15s RxFrames][format %22s PktLossDuration(ms)]"
	puts "\t-----------------------------------------------------------------"
	puts "\t[format %8s $txPort][format %8s $rxPort][format %12s $txFrames][format %15s $rxFrames][format %22s $pktLossDuration]"
    }
}

# Using this mechanism to control whether to reconfigure ports or not
if {[info exists resumeNoConfig] == 0} {
    set resumeNoConfig 0
} else {
    set resumeNoConfig 1
}


# Uncomment these lines for debugging
#set ::ixia::debug 1
#set ::ixia::debug_file_name ixiaHltDebugLog.txt
#set ::ixia::logHltapiCommandsFlag 1
#set ::ixia::logHltapiCommandsFileName ixiaHltCommandsLog.txt

set connectStatus [ConnectToIxia $ixiaChassisIp $ixNetworkTclServerIp $portList $userName]

if {$resumeNoConfig == 0} {
    ConfigInterfaceIp
    ConfigTrafficItem
    ApplyTraffic
    starttraffic
}

# Set this variable at the bottom to let the script know that
# the configuration is done. Do not reconfigure again.
set resumeNoConfig 1

getstats


