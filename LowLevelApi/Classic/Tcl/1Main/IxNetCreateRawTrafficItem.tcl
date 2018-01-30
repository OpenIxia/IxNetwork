#!/opt/ActiveTcl-8.5/bin/tclsh
#!/usr/bin/tclsh

# Description:
# 
#    - Loads a preconfigured IxNetwork file.
#
#    - Create a Raw Traffic Item.
#
#    - Includes an API to remove a Traffic Item by
#      the name.
#
#    - Includes an API to return the Traffic Item 
#      by the Mac Address and VlanId.
#    

package req Ixia

set ixiaChassisIp 10.205.4.172
set ixNetworkTclServerIp 10.205.1.42
set ixNetworkVersion 7.30
set ixNetworkCfgFile ~/MyIxiaWork/Temp/basicIpv4_7.30_172.ixncfg

proc GetVportMapping { userPort } {
    foreach vport [ixNet getList [ixNet getRoot] vport] {
	set connectedTo [ixNet getAttribute $vport -connectedTo]
	set card [lindex [split [lindex [split $connectedTo /] 3] :] end]
	set portNum [lindex [split [lindex [split $connectedTo /] 4] :] end]
	set port $card/$portNum

	if {$port == $userPort} {
	    return $vport
	}
    }
    return 0
}

proc RemoveTrafficItem { trafficItemName } {
    set flag 0
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set currentTiName [ixNet getAttr $trafficItem -name]
	if {[regexp -nocase "(TI\[0-9]+)?$trafficItemName$" $currentTiName]} {
	    puts "\nRemoveTrafficItem: $trafficItemName"
	    catch {ixNet remove [ixNet getRoot]traffic $trafficItem} errMsg
	    if {$errMsg != "::ixNet::OK"} {
		puts "\nRemoveTrafficItem error: $errMsg"
		return 1
	    }
	    ixNet commit
	    set flag 1
	}
    }
    if {$flag == 0} {
	puts "\nRemoveTrafficItem error: No such Traffic Item name: $trafficItemName"
	return 1
    }
    return 0
}

proc CreateTrafficItem { args } {
    set trafficItemName My_Traffic_Item

    # Options: random or the framesize value
    set frameSize random

    set totalFrames 1000

    # oneWay or biDirection
    set biDirection oneWay

    # oneToOne, manyToMany, fullMesh
    set trafficType oneToOne

    set trackBy flowGroup0
    set srcMacTotalIncr 1
    set dstMacTotalIncr 1
    set vlanIdTotalIncr 1
    set vlanIdPriorityTotalIncr 1
    set srcIpTotalIncr 1
    set dstIpTotalIncr 1

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg { 
	    -name {
		set trafficItemName [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -trafficType {
		# oneToOne, manyToMany, fullMesh
		set trafficType [lindex $args [expr $argIndex + 1]]
		incr argIndex
	    }
	    -frameCount {
		set totalFrames [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -frameSize {
		# Options: random or the framesize value
		set frameSize [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -lineRate {
		set lineRatePercent [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -packetRate {
		set packetRate [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -trafficTransmission {
		# continuour or packetBurst
		set trafficTransmission [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -trackBy {
		set trackBy [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -srcPorts {
		set srcPorts [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -dstPorts {
		set dstPorts [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -vlanId {
		set vlanId [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -vlanIdTotalIncr {
		set vlanIdTotalIncr [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -vlanIdPriority {
		set vlanIdPriority [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -vlanIdPriorityTotalIncr {
		set vlanIdPriorityTotalIncr [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -srcMac {
		set srcMac [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -dstMac {
		set dstMac [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -srcMacTotalIncr {
		set srcMacTotalIncr [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -dstMacTotalIncr {
		set dstMacTotalIncr [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -srcIp {
		set srcIp [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -dstIp {
		set dstIp [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -srcIpTotalIncr {
		set srcIpTotalIncr [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -dstIp {
		set dstIp [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    -dstIpTotalIncr {
		set dstIpTotalIncr [lindex $args [expr $argIndex + 1]]
		incr argIndex 2		
	    }
	    default {
		puts "\nError: CreateTrafficItem: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    set mandatories "srcMac dstMac srcPorts dstPorts"
    foreach mandatoryItem $mandatories {
	if {[info exists $mandatoryItem] == 0} {
	    puts "CreateTrafficItem Error: Requires parameter -$mandatoryItem"
	    return
	}
    }
    
    # Set some defaults
    if {[info exists trafficTransmission] == 0} {
	# continuous or packetBurst
	set trafficTransmission packetBurst
    }
    
    if {[info exists lineRatePercent] == 0 && [info exists packetRate] == 0} {
	set lineRatePercent 100
    }
    
    puts "\nCreating new Traffic Item ..."
    set trafficItemObj [ixNet add [ixNet getRoot]traffic trafficItem]
    
    catch {ixNet setMultAttr $trafficItemObj \
	       -enabled True \
	       -trafficType raw \
	       -name $trafficItemName \
	       -routeMesh oneToOne \
	       -srcDestMesh $trafficType \
	       -transmitMode interleaved \
	       -biDirectional $biDirection
    } errMsg
    
    if {$errMsg != "::ixNet::OK"} {
	puts "\nError: $errMsg"
    } else {
	puts "\nCreateTrafficItem: Successfully created new Traffic Item"
    }
    
    set trafficItemObj [lindex [ixNet remapIds $trafficItemObj] 0]
     
    set endpoints [ixNet add $trafficItemObj endpointSet]
    puts "\nAdded endpoints: $endpoints"
    
    set srcPortList {}
    foreach sourcePort $srcPorts {
	# Like this:    /vport:1/protocols.  
	# Not like this ::ixNet::OBJ-/vport:1/protocols
	set vport [GetVportMapping $sourcePort]
	regexp "::ixNet::OBJ-(/vport:\[0-9]+)" $vport - vport
	lappend srcPortList $vport/protocols
    }
    
    set dstPortList {}
    foreach destPort $dstPorts {
	set vport [GetVportMapping $destPort]
	regexp "::ixNet::OBJ-(/vport:\[0-9]+)" $vport - vport
	lappend dstPortList $vport/protocols
    }
    
    puts "Src Endpoints: $srcPortList"
    puts "Dst Endpoints: $dstPortList"
    catch {ixNet setMultiAttr $endpoints \
	       -sources [list $srcPortList]  \
	       -destinations [list $dstPortList]
    } errMsg
    
    if {$errMsg != "::ixNet::OK"} {
	puts "\nError: CreateTrafficItem: Failed to create endpoints"
	return 1
    }
    ixNet commit
    
    # Fixed frame count Traffic Item
    if {$trafficTransmission == "packetBurst"} {
	catch {ixNet setMultiAttr $trafficItemObj/configElement:1/transmissionControl \
		   -type fixedFrameCount \
		   -burstPacketCount 1 \
		   -frameCount $totalFrames
	} errMsg
	
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError:CreateTrafficItem: $errMsg"
	}
    }
    
    if {$trafficTransmission == "continuous"} {
	catch {ixNet setMultiAttr $trafficItemObj/configElement:1/transmissionControl \
		   -type continuous \
		   -burstPacketCount 1
	} errMsg

	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError:CreateTrafficItem: $errMsg"
	}
    }
    
    if {[info exists lineRatePercent]} {
	catch {ixNet setAttr $trafficItemObj/configElement:1/frameRate -rate $lineRatePercent} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError:CreateTrafficItem: $errMsg"
	}
    }
    
    if {[info exists packetRate]} {
	catch {ixNet setAttr $trafficItemObj/configElement:1/frameRate -type framesPerSecond -rate $packetRate} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError:CreateTrafficItem: $errMsg"
	}
    }
    
    if {$frameSize == "random"} {
	catch {ixNet setMultiAttribute $trafficItemObj/configElement:1/frameSize \
		   -weightedPairs [list ] \
		   -incrementFrom 64 \
		   -randomMax 1500 \
		   -weightedRangePairs [list ] \
		   -type random \
		   -presetDistribution cisco \
		   -incrementTo 1500
	} errMsg

	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError:CreateTrafficItem: $errMsg"
	}
    }

    if {$frameSize != "random"} {
	catch {ixNet setAttr $trafficItemObj/configElement:1/frameSize -fixedSize $frameSize} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError:CreateTrafficItem: $errMsg"
	}
    }

    catch {ixNet setAttr $trafficItemObj/tracking -trackBy $trackBy} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "\nError:CreateTrafficItem: $errMsg"
    }
    
    catch {ixNet setMultiAttr $trafficItemObj/configElement:1/stack:"ethernet-1"/field:"ethernet.header.destinationAddress-1" \
	       -singleValue 00:00:00:00:00:00 \
	       -seed 1 \
	       -optionalEnabled true \
	       -valueList [list 00:00:00:00:00:00] \
	       -stepValue 00:00:00:00:00:01 \
	       -fixedBits 00:00:00:00:00:00 \
	       -fieldValue 00:00:00:00:00:00 \
	       -randomMask 00:00:00:00:00:00 \
	       -valueType increment \
	       -startValue $dstMac \
	       -countValue $dstMacTotalIncr
    } errMsg

    if {$errMsg != "::ixNet::OK"} {
	puts "\nError:CreateTrafficItem: $errMsg"
    }
    
    catch {ixNet setMultiAttribute $trafficItemObj/configElement:1/stack:"ethernet-1"/field:"ethernet.header.sourceAddress-2" \
	       -singleValue 00:00:00:00:00:00 \
	       -seed 1 \
	       -optionalEnabled true \
	       -valueList [list 00:00:00:00:00:00] \
	       -stepValue 00:00:00:00:00:01 \
	       -fixedBits 00:00:00:00:00:00 \
	       -fieldValue 00:00:00:00:00:00 \
	       -randomMask 00:00:00:00:00:00 \
	       -valueType increment \
	       -startValue $srcMac \
	       -countValue $srcMacTotalIncr
    } errMsg

    if {$errMsg != "::ixNet::OK"} {
	puts "\nError:CreateTrafficItem: $errMsg"
    }
	
    if {[info exists vlanIdPriority]} {
	catch {ixNet setMultiAttribute $trafficItemObj/configElement:1/stack:"vlan-2"/field:"vlan.header.vlanTag.vlanUserPriority-1" \
		   -singleValue 0 \
		   -seed 1 \
		   -optionalEnabled true \
		   -valueList [list 0] \
		   -stepValue 1 \
		   -fixedBits 0 \
		   -fieldValue 0 \
		   -randomMask 0 \
		   -valueType increment \
		   -startValue $vlanIdPriority \
		   -countValue $vlanIdPriorityTotalIncr
	} errMsg
	
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError:CreateTrafficItem: $errMsg"
	}
    }

    if {[info exists vlanId]} {
	catch {ixNet setMultiAttribute $trafficItemObj/configElement:1/stack:"vlan-2"/field:"vlan.header.vlanTag.vlanID-3" \
		   -singleValue 0 \
		   -seed 1 \
		   -optionalEnabled true \
		   -valueList [list 0] \
		   -stepValue 1 \
		   -fixedBits 0 \
		   -fieldValue 0 \
		   -randomMask 0 \
		   -valueType increment \
		   -startValue $vlanId \
		   -countValue $vlanIdTotalIncr
	} errMsg

	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError:CreateTrafficItem: $errMsg"
	}
    }
    
    if {[info exists srcIp]} {
	catch {ixNet setMultiAttribute $trafficItemObj/configElement:1/stack:"ipv4-3"/field:"ipv4.header.srcIp-27" \
		   -singleValue 0.0.0.0 \
		   -seed 1 \
		   -optionalEnabled true \
		   -valueList [list 0.0.0.0] \
		   -stepValue 0.0.0.1 \
		   -fixedBits 0.0.0.0 \
		   -fieldValue 0.0.0.0 \
		   -randomMask 0.0.0.0 \
		   -valueType increment \
		   -startValue $srcIp \
		   -countValue $srcIpTotalIncr
	} errMsg
	
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError:CreateTrafficItem: $errMsg"
	}
    }

    if {[info exists dstIp]} {
	catch {ixNet setMultiAttribute $trafficItemObj/configElement:1/stack:"ipv4-3"/field:"ipv4.header.dstIp-28" \
		   -singleValue 0.0.0.0 \
		   -seed 1 \
		   -optionalEnabled true \
		   -valueList [list 0.0.0.0] \
		   -stepValue 0.0.0.1 \
		   -fixedBits 0.0.0.0 \
		   -fieldValue 0.0.0.0 \
		   -randomMask 0.0.0.0 \
		   -valueType increment \
		   -startValue $dstIp \
		   -countValue $dstIpTotalIncr
	} errMsg

	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError:CreateTrafficItem: $errMsg"
	}
    }

    ixNet commit

    catch {ixNet exec generate $trafficItemObj} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "\nError:CreateTrafficItem Regenerate: $errMsg"
    }
    after 1000
}

proc GetMacAndVlanTrafficItem { mac vlanId } {
    # Based on the given mac address and vlanId, return the 
    # Traffic Item.

    set trafficItemList {}

    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set macFlag 0
	set vlanIdFlag 0

	foreach highLevelStream [ixNet getList $trafficItem highLevelStream] {
	    foreach stack [ixNet getList $highLevelStream stack] {
		# ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"ethernet-1" 
		# ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"vlan-2" 
		# ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"ipv4-3" 
		# ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"fcs-4"
		if {[regexp "ethernet" $stack] == 1 || [regexp "vlan" $stack] == 1} {
		    foreach field [ixNet getList $stack field] {
			# ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"ethernet-1"/field:"ethernet.header.sourceAddress-2"
			# ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"vlan-2"/field:"vlan.header.vlanTag.vlanID-3"
			if {[regexp -nocase "ethernet\.header\.sourceAddress-" $field]} {
			    set currentSrcMac [ixNet getAttribute $field -startValue]
			    if {$currentSrcMac == $mac} {
				set macFlag 1
			    }
			}
			
			if {[regexp -nocase "vlanTag\.vlanID-" $field]} {
			    set currentVlanId [ixNet getAttribute $field -startValue]
			    if {$currentVlanId == $vlanId} {
				set vlanIdFlag 1
			    }
			}		    

			if {$macFlag == 1 && $vlanIdFlag == 1} {
			    set macFlag 0
			    set vlanIdFlag 0
			    lappend trafficItemList $trafficItem
			}
		    }
		}
	    }
	}
    }

    return $trafficItemList
}

proc VerifyPortState { {portList all} {expectedPortState up} } {
    # portList format = 1/2.  Not 1/1/2

    puts "\nVerifying port state ...\n"
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
		    puts "$port is still $portState. Expecting port up. $timer/60 seconds."
		    after 2000
		    continue
		}
		
		if {$portState != "up" && $timer == "60"} {
		    puts "Failed: $port seem to be stuck on $portState state. Expecting port up."
		    set portsAllUpFlag 1
		}
		
		if {$portState == "up"} {
		    puts "$port state is $portState"
		    break
		}
	    }

	    # Expecting port state = Down
	    if {$expectedPortState == "down"} {
		if {$portState != "down" && $timer != "60"} {
		    puts "$port is still $portState. Expecting port down. $timer/60 seconds."
		    after 2000
		    continue
		}
		
		if {$portState == "up" && $timer == "60"} {
		    puts "Error: $port seem to be stuck on the $portState state. Expecting port down."
		    set portsAllUpFlag 1
		}
		
		if {$portState == "down"} {
		    puts "$port state is $portState"
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

puts "\nConnecting to $ixNetworkTclServerIp ..."
ixNet connect $ixNetworkTclServerIp -version $ixNetworkVersion

ixNet rollback
ixNet execute newConfig

if {[file exists $ixNetworkCfgFile] == 0} {
    puts "\n\n** ixNet config file does not exists: $ixNetworkCfgFile\n\n"
}

puts "\nLoading ixncfg file ..."
if {[ixNet exec loadConfig [ixNet readFrom $ixNetworkCfgFile]] != "::ixNet::OK"} {
    puts "\n\n*** Failed to load IxNetwork config file: $ixNetworkCfgFile"
    exit
} else {
    puts "\n\n*** Successfully loaded IxNetworkCfg file: $ixNetworkCfgFile\n"
    puts "Please wait 40 seconds while your ports are getting rebooted ..."
    if {[VerifyPortState] == 1} {
	exit
    }
}


# -trafficTransmission options: packetBurst or continuous
# -lineRate 75  or -packetRate 10000

CreateTrafficItem \
    -name My_Traffic_Item \
    -srcPorts 1/1 \
    -dstPorts 1/2 \
    -srcMac 00:01:01:01:00:01 \
    -dstMac 00:01:01:02:00:01 \
    -srcMacTotalIncr 5 \
    -dstMacTotalIncr 5 \
    -srcIp 1.1.1.1 \
    -dstIp 1.1.1.2 \
    -srcIpTotalIncr 5 \
    -dstIpTotalIncr 5 \
    -vlanId 3 \
    -vlanIdTotalIncr 5 \
    -vlanIdPriority 7 \
    -vlanIdPriorityTotalIncr 8 \
    -trafficTransmission continuous \
    -packetRate 1008

set trafficItemList [GetMacAndVlanTrafficItem 00:01:01:01:00:01 3]
puts "\n--- got back: $trafficItemList ----"

RemoveTrafficItem My_Traffic_Item

ixNet disconnect



