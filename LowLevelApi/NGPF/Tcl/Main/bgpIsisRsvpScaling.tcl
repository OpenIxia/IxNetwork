#!/usr/bin/tclsh

package req IxTclNetwork

set ixiaChassisIp 10.219.117.102
set ixNetworkTclServer 10.219.117.103
set ixNetworkVersion 7.51

set portList(10.219.117.102) "1/1 1/2"

proc AddChassis { ixiaChassisIp } {
    set chassisObj [ixNet add [ixNet getRoot]/availableHardware "chassis"]
    ixNet setMultiAttribute $chassisObj \
	-masterChassis {} \
	-chainTopology daisy \
	-sequenceId 1 \
	-cableLength 0 \
	-hostname $ixiaChassisIp
    ixNet commit
    return[lindex [ixNet remapIds $chassisObj] 0]
}

proc VerifyPortState { {portList all} {expectedPortState up} } {
    # portList format = 1/2.  Not 1/1/2

    puts "\nVerifyPortState ...\n"
    #after 5000
    set allVports [ixNet getList [ixNet getRoot] vport]

    if {$portList == "all"} {
	set vPortList $allVports
    }

    if {$portList != "all"} {
	# Search out the user defined $portList
	set vPortList {}
	foreach vport $allVports {
	    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
	    set connectedTo [ixNet getAttribute $vport -connectedTo]
	    set connectedTo [lrange [split $connectedTo /] 3 4]
	    set card [lindex [split [lindex $connectedTo 0] :] end]
	    set port [lindex [split [lindex $connectedTo 1] :] end]
	    set port $card/$port

	    if {[lsearch $portList $port] != -1} { 
		lappend vPortList $vport
	    }
	}
    }

    set portsAllUpFlag 0

    foreach vport $vPortList {
	for {set timer 0} {$timer <= 60} {incr timer 2} {
	    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
	    set connectedTo [ixNet getAttribute $vport -connectedTo]
	    set connectedTo [lrange [split $connectedTo /] 3 4]
	    set card [lindex [split [lindex $connectedTo 0] :] end]
	    set port [lindex [split [lindex $connectedTo 1] :] end]
	    set port $card/$port
	    
	    set portState [ixNet getAttribute $vport -state]

	    # Expecting port state = UP
	    if {$expectedPortState == "up"} {
		if {$portState != "up" && $timer != "60"} {
		    puts "VerifyPortState: $port is still $portState. Expecting port up. $timer/60 seconds."
		    after 2000
		    continue
		}
		
		if {$portState != "up" && $timer == "60"} {
		    puts "\nError VerifyPortState: $port seem to be stuck on $portState state. Expecting port up.\n"
		    set portsAllUpFlag 1
		}
		
		if {$portState == "up"} {
		    puts "\nVerifyPortState: $port state is $portState"
		    break
		}
	    }

	    # Expecting port state = Down
	    if {$expectedPortState == "down"} {
		if {$portState != "down" && $timer != "60"} {
		    puts "\nVerifyPortState: $port is still $portState. Expecting port down. $timer/60 seconds."
		    after 2000
		    continue
		}
		
		if {$portState == "up" && $timer == "60"} {
		    puts "\nError VerifyPortState: $port seem to be stuck on the $portState state. Expecting port down."
		    set portsAllUpFlag 1
		}
		
		if {$portState == "down"} {
		    puts "\nVerifyPortState: $port state is $portState as expected"
		    break
		}
	    }
	}
    }

    if {$portsAllUpFlag == 1} {
	return 1
    } else {
	after 3000
	return 0
    }
}

proc GetVportMapping { Port } {
    # Search all vport for the port number.
    # Port format = 1/1.  Not 1/1/1.

    set vportList [ixNet getList [ixNet getRoot] vport]
    if {$vportList == ""} {
	return 0
    }
    
    foreach vport $vportList {
	set connectedTo [ixNet getAttribute $vport -connectedTo]
	set card [lindex [split [lindex [split $connectedTo /] 3] :] end]
	set portNum [lindex [split [lindex [split $connectedTo /] 4] :] end]
	set port $card/$portNum
	if {$port == $Port} {
	    return $vport
	}
    }
    return 0
}

proc CreateTopologyNgpf { topologyName vPorts } {
    puts "\nCreateTopologyNgpf: $topologyName : $vPorts"
    set topologyObj [ixNet add [ixNet getRoot] "topology"]
    ixNet setMultiAttribute $topologyObj \
	-name $topologyName \
	-vports [list $vPorts]

    ixNet commit
    return [lindex [ixNet remapIds $topologyObj] 0]
}

proc CreateDeviceGroupNgpf { topologyObj deviceGroupName multiplier } {
    puts "\nCreateDeviceGroupNgpf: $topologyObj : $deviceGroupName"
    set deviceGroupObj [ixNet add $topologyObj "deviceGroup"]
    ixNet setMultiAttribute $deviceGroupObj \
	-name $deviceGroupName \
	-multiplier $multiplier
    
    ixNet commit
    return [lindex [ixNet remapIds $deviceGroupObj] 0]
}

proc CreateEthernetStackNgpf { deviceGroupObj ethernetStackName } {
    puts "\nCreateEthernetStackNgpf: $deviceGroupObj : $ethernetStackName"
    set ethernetStackObj [ixNet add $deviceGroupObj "ethernet"]
    ixNet setMultiAttribute $ethernetStackObj \
	-name $ethernetStackName

    ixNet commit
    return [lindex [ixNet remapIds $ethernetStackObj] 0]
}

proc CreateIpv4StackNgpf { ethernetStackObj ipv4StackName } {
    puts "\nCreateIpv4StackNgpf: $ethernetStackObj : $ipv4StackName"
    set ipv4StackObj [ixNet add $ethernetStackObj ipv4]
    ixNet setMultiAttribute $ipv4StackObj \
	-name $ipv4StackName

    ixNet commit
    return [lindex [ixNet remapIds $ipv4StackObj] 0]
}

proc ConfigIpv4AddressNgpf { ipv4StackObj start {step 0.0.0.1} {direction increment} } {
    puts "\nConfigIpv4AddressNgpf: $ipv4StackObj : start=$start step=$step direction=$direction"
    set ipv4AddressObj [ixNet getAttribute $ipv4StackObj -address]
    ixNet setMultiAttribute $ipv4AddressObj \
	-clearOverlays false \
	-pattern counter
    ixNet commit

    set ipv4AddressObj2 [ixNet add $ipv4AddressObj "counter"]
    ixNet setMultiAttribute $ipv4AddressObj2 \
	-start $start \
	-step $step \
	-direction $direction
    ixNet commit
    
    return [lindex [ixNet remapIds $ipv4AddressObj2] 0]
}

proc ConfigIpv4PrefixNgpf { ipv4StackObj prefixValue } {
    set ipv4Prefix [ixNet getAttribute $ipv4StackObj -prefix]
    set ipv4PrefixObj [ixNet add $ipv4PrefixObj "singleValue"]
    ixNet setAttribute $ipv4Prefix -value $prefixValue
    ixNet commit

    return [lindex [ixNet remapIds $ipv4PrefixObj] 0]
}

proc CreateIpv4GatewayIpObjNgpf { ipv4StackObj } {
    puts "\nCreateIpv4GatewayIpObjNgpf: $ipv4StackObj"
    set ipv4GatewayIpObj [ixNet getAttribute $ipv4StackObj -gatewayIp]
    ixNet setMultiAttribute $ipv4GatewayIpObj \
	-clearOverlays false \
	-pattern counter
    ixNet commit
    
    return [lindex [ixNet remapIds $ipv4GatewayIpObj] 0]
}

proc ConfigIpv4GatewayIpNgpf { ipv4GatwayIpObj start {step 0.0.0.0} {direction increment} } {
    puts "\nConfigIpv4GatewayIpNgpf: $ipv4GatwayIpObj : start=$start step=$step direction=$direction"
    set ipv4GatewayIpObj2 [ixNet add $ipv4GatwayIpObj "counter"]
    ixNet setMultiAttribute $ipv4GatewayIpObj2 \
	-start $start \
	-step $step \
	-direction $direction
    ixNet commit

    return [lindex [ixNet remapIds $ipv4GatewayIpObj2] 0]
}

proc ConfigIpv4GatewayIpOverlayNgpf { ipv4GatewayIpObj count index indexStep valueStep value } {
    # Example: Each of the below uses the same Ipv4 Object.
    #
    #-step 0.0.0.0
    #-start 1.1.1.4
    #-direction increment
    #
    #-count 1 
    #-index 2 
    #-indexStep 0 
    #-valueStep 1.1.1.5 
    #-value 1.1.1.5
    #
    #-count 1
    #-index 3
    #-indexStep 0
    #-valueStep 1.1.1.6
    #-value 1.1.1.6
    
    puts "\nConfigIpv4GatewayIpOverlayNgpf: $ipv4GatewayIpObj : count=$count index=$index indexStep=$indexStep value=$value valueStep=$valueStep "
    set ipv4GatewayOverlayObj [ixNet add $ipv4GatewayIpObj "overlay"]
    ixNet setMultiAttribute $ipv4GatewayOverlayObj \
	-count $count \
	-index $index \
	-indexStep $indexStep \
	-valueStep $valueStep \
	-value $value
    ixNet commit

    return [lindex [ixNet remapIds $ipv4GatewayOverlayObj] 0]
}


catch {ixNet connect $ixNetworkTclServer -version $ixNetworkVersion} errMsg
if {$errMsg != "::ixNet::OK"} {
    puts "\nFailed to connect to the IxNetwork Tcl server. Exiting.\n"
    exit
}

set root [ixNet getRoot]
ixNet execute newConfig

foreach {ixChassisIp ports} [array get portList *] {
    set ixChassis [ixNet add [ixNet getRoot]/availableHardware chassis]
    ixNet setAttribue $ixChassis -hostname $ixChassisIp
    set ixChassis [lindex [ixNet remapIds $ixChassis] 0]

    foreach port $ports {
	set port [split $port /]
	set cardNumber [lindex $port 0]
	set portNumber [lindex $port 1]
	puts "Clearing port state on $ixChassisIp: $cardNumber/$portNumber ..."
	
	# ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:2
	catch {ixNet execute clearOwnership "::ixNet::OBJ-/availableHardware/chassis:\"$ixChassisIp\"/card:$cardNumber/port:$portNumber"} errMsg
	if {[regexp "Unable" $errMsg]} {
	    puts "Failed to clear port ownership"
	    exit
	}
	
	set vPort [ixNet add [ixNet getRoot] vport]
	ixNet commit
	set vPort [lindex [ixNet remapIds $vPort] 0]
	
	ixNet setMultiAttribute $vPort \
	    -connectedTo $ixChassis/card:$cardNumber/port:$portNumber \
	    -name 1/$cardNumber/$portNumber

	lappend vPortList $vPort
	
	set getVport($ixChassisIp:$cardNumber/$portNumber) $vPort
	set getPort($vPort) $ixChassisIp:$cardNumber/$portNumber
    }

    ixNet commit
}

if {[VerifyPortState] == 1} {
    exit
}

set topology1 [CreateTopologyNgpf Hgee-Topo-1 $getVport($ixiaChassisIp:1/1)]
set topology2 [CreateTopologyNgpf Hgee-Topo-2 $getVport($ixiaChassisIp:1/2)]

set topo1Dg1 [CreateDeviceGroupNgpf $topology1 Hgee-DG-1 3]
set topo2Dg1 [CreateDeviceGroupNgpf $topology2 Hgee-DG-2 3]

set topo1Dg1EthernetObj [CreateEthernetStackNgpf $topo1Dg1 Hgee-Eth1]
set topo2Dg1EthernetObj [CreateEthernetStackNgpf $topo2Dg1 Hgee-Eth2]

# Creating multivalue
set topo1Dg1Ipv4Obj [CreateIpv4StackNgpf $topo1Dg1EthernetObj Hgee-Ipv4-1]
set topo2Dg1Ipv4Obj [CreateIpv4StackNgpf $topo2Dg1EthernetObj Hgee-Ipv4-2]

set topo1Dg1Ipv4AddrObj [ConfigIpv4AddressNgpf $topo1Dg1Ipv4Obj 1.1.1.1]
set topo2Dg1Ipv4AddrObj [ConfigIpv4AddressNgpf $topo2Dg1Ipv4Obj 1.1.1.4]

set topo1Dg1Ipv4GatewayObj [CreateIpv4GatewayIpObjNgpf $topo1Dg1Ipv4Obj]
set topo2Dg1Ipv4GatewayObj [CreateIpv4GatewayIpObjNgpf $topo2Dg1Ipv4Obj]

ConfigIpv4GatewayIpNgpf        $topo1Dg1Ipv4GatewayObj 1.1.1.4 0.0.0.0 increment
ConfigIpv4GatewayIpOverlayNgpf $topo1Dg1Ipv4GatewayObj 1 2 0 1.1.1.5 1.1.1.5
ConfigIpv4GatewayIpOverlayNgpf $topo1Dg1Ipv4GatewayObj 1 3 0 1.1.1.6 1.1.1.6

ConfigIpv4GatewayIpNgpf        $topo2Dg1Ipv4GatewayObj 1.1.1.1 0.0.0.0 increment
ConfigIpv4GatewayIpOverlayNgpf $topo2Dg1Ipv4GatewayObj 1 2 0 1.1.1.2 1.1.1.2
ConfigIpv4GatewayIpOverlayNgpf $topo2Dg1Ipv4GatewayObj 1 3 0 1.1.1.3 1.1.1.3


ixNet disconnect
