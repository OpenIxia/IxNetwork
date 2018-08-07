proc NewBlankConfig {} {
    if {[catch {ixNet execute newConfig} errMsg]} {
	puts "\nError: Failed to start new blank config: $errMsg"
	return 1
    }
    return 0
}

proc Connect {args} {
    # osPlatform:  The Ixia chassis OS.  windows|linux.  Defaults to windows
    # apiServerIp: The IxNetwork API server
    # ixNetworkVersion: The IxNetwork version
    # username: Linux API server. login. Defaults = admin
    # password: Linux API server login passwoed. Default = admin
    # apiKey:   Linux API server user login account API-key.
    #           The Proc will automatically get the API-key when login is authenticated.
    #           Optionally, you could pass it in.
    # closeServerOnDisconnect: True|False

    # Set the Linux API server admin login default credentials
    set username None
    set password None
    set apiKey None
    set osPlatform windows

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -osPlatform {
		set osPlatform [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -apiServerIp {
		set apiServerIp [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
		append paramList " $apiServerIp"
	    }
	    -ixNetworkVersion {
		set ixNetworkVersion [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
		append paramList " -version $ixNetworkVersion"
	    }
	    -apiKey {
		set apiKey [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
		append paramList " -apiKey $apiKey"
	    }
	    -username {
		set username [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
		append paramList " -username $username"
	    }
	    -password {
		set password [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
		append paramList " -username $password"
	    }
	    -closeServerOnDisconnect {
		set closeServerOnDisconnect [lindex $args [expr $argIndex + 1]]
		append paramList " -closeServerOnDisconnect $closeServerOnDisconnect"
		incr argIndex 2
	    }
	    default {
		puts "Connect: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    # For Linux API server login to get the API key
    if {$osPlatform == "linux"} {
	if {$username == "None"} {
	    set username admin
	    set password admin
	    append paramList " -username $password -password $password"
	}
	if {$apiKey == "None"} {
	    set apiKey [GetApiKey $apiServerIp $username $password]
	    if {$apiKey == 1} {
		return 1
	    }
	}
	
	append paramList " -apiKey $apiKey"
    }

    puts "\nConnecting to API server: $paramList"
    if {[catch {set connectStatus [eval ixNet connect $paramList]} errMsg]} {
	puts "\nConnect failed $paramList"
	return 1
    }

    puts "connectStatus: $connectStatus"
    return 0
}

proc ConnectToIxChassis {ixChassisIpList} {
    foreach ixChassisIp $ixChassisIpList {
	if {[catch {set chassisObj [ixNet add [ixNet getRoot]/availableHardware "chassis"]} errMsg]} {
	    puts "Error: ConnectToIxChassis: $errMsg"
	    return 1
	}
	
	puts "\nConnectToIxChassis: $ixChassisIp"
	if {[catch {set status [ixNet setAttribute $chassisObj -hostname $ixChassisIp]} errMsg]} {
	    puts "\nError: ConnectToIxChassis: $errMsg"
	    return 1
	}
	ixNet commit

	set chassisObj [ixNet remapIds $chassisObj]
	#set status [ixNet getList [ixNet getRoot]/availableHardware chassis]
	#puts "ConnectToIxChassis: Connected: $status"
	for {set counter 1} {$counter <= 60} {incr counter} {
	    set currentState [ixNet getAttribute $chassisObj -state]
	    if {$counter < 60 && $currentState != "ready"} {
		puts "Chassis $ixChassisIp is not ready yet. Wait $counter/60 seconds"
		after 1000
	    }
	    if {$counter == 60 && $currentState != "ready"} {
		puts "\nError: Chassis $ixChassisIp failed to connect"
	    }
	    if {$counter < 60 && $currentState == "ready"} {
		puts "Chassis $ixChassisIp is up"
		break
	    }
	}
    }
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

    if {[file exists $configFile] == 0} {
	puts "\nError: LoadConfigFile: No such file found: $configFile"
	return 1
    }

    puts "\nLoadConfigFile: $configFile"
    if {[ixNet exec loadConfig [ixNet readFrom $configFile]] != "::ixNet::OK"} {
	puts "\nError: LoadConfigFile failed: $configFile"
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

proc GetPorts {{ixChassisIp None}} {
    # Get all the ports from $ixChassisIp

    set chassisObjList [ixNet getList [ixNet getRoot]/availableHardware chassis]
    if {$chassisObjList == ""} {
	puts "\nError: GetPorts: No chassis is connected"
	return 1
    }
    foreach chassisObj $chassisObjList {
	set chassisIp [ixNet getAttribute $chassisObj -hostname]
	if {$ixChassisIp == "None"} {
	    set ixChassisIp $chassisIp
	    break
	}
	if {$ixChassisIp != "None"} {
	    if {$ixChassisIp == $chassisIp} {
		set ixChassisIp $chassisIp
		break
	    } else {
		continue
	    }
	}
    }

    set portList {}
    set cardList [ixNet getList $chassisObj card]
    foreach cardObj $cardList {
	set portObjList [ixNet getList $cardObj port]
	foreach port $portObjList {
	    # ::ixNet::OBJ-/availableHardware/chassis:"192.168.70.11"/card:2/port:1
	    set cardId [lindex [split [lindex [split $port /] 3] :] end]
	    set portId [lindex [split [lindex [split $port /] end] :] end]
	    lappend portList [list $ixChassisIp $cardId $portId]
	} 
    }
    return $portList
}

proc GetPortsAssignedToVports {} {
    # Dynamically get all the ports assigned to the vports
    # Returns a list of all the configured ports and a list of all the associated vports.
    # Returns: {{192.168.70.11 1 1} {192.168.70.11 2 1}} {::ixNet::OBJ-/vport:1 ::ixNet::OBJ-/vport:2}

    set chassisObj [ixNet getList [ixNet getRoot]/availableHardware chassis]
    if {$chassisObj == ""} {
	puts "\nError: GetPortsAssignedToVports: No chassis is connected"
	return 1
    }
    set ixChassisIp [ixNet getAttribute $chassisObj -hostname]
    set portList {}
    set vportList [ixNet getList [ixNet getRoot] vport]

    if {$vportList == ""} {
	puts "\nError: GetPortsAssignedToVports: The configuration has no vport created."
	return 1
    }

    foreach vport $vportList {
	set port [GetVportPhyPort $vport noSlash]
	set cardId [lindex $port 0]
	set portId [lindex $port 1]
	if {$cardId == ""} {
	    puts "\nError: GetPortsAssignedToVports: No cardId is assigned to vport: $vport."
	    return 1
	}
	if {$portId == ""} {
	    puts "\nError: GetPortsAssignedToVports: No portId is assigned to cardId:$cardId"
	    return 1
	}
	lappend portList [list $ixChassisIp $cardId $portId]
    }
    return [list $portList $vportList]
}


proc AssignPorts {ixChassisIp {portList None}} {
    # This Proc assigns physical ports to vpors.
    #
    # With the ixChassis IP, this proc discover all the ports or
    # you could pass in a portList.
    #
    # If there is no vports discovered in your configuration, this Proc
    # expected you to pass in a portList.
    #
    # portList: A list of ports in a list format: [list "$ixChassisIp $card $port" ...]

    set vportList [ixNet getList [ixNet getRoot] vport]
    if {$vportList == "" && $portList == "None"} {
	puts "\nError: AssignPorts: The configuration has no vports created and you did not pass"
	puts "\tin a portList. Don't know how to assign ports. If it's a blank config, you need"
	puts "\tto pass in a portList"
	return 1
    }

    puts "\nAssignPorts"
    if {$vportList == ""} {
	# vports will be automatically created by ixTclNet::AssignPorts
	set vportList {}
    }

    puts "\tPortList: [list $portList]"
    puts "\tVportList: [list $vportList]" 
    if {[catch {ixTclNet::AssignPorts $portList {} $vportList true} errMsg]} {
	puts "\nError: AssignPorts: Port assigning to vport failed or ports not booting up."
	return 1
    }
    
    return 0
}

proc getRawTrafficVports {} {
    # Ordinary vports looks like this: ::ixNet::OBJ-/vport:1
    # For raw traffic items, vports needs to be like this: ::ixNet::OBJ-/vport:1/protocols

    set vportList [ixNet getList [ixNet getRoot] vport]
    set protocolList {}
    # Raw traffic vport format: /vport:1/protocols.  
    # Not like this ::ixNet::OBJ-/vport:1/protocols
    foreach vport $vportList {
	regexp ".*(/vport.*)" $vport - protocolVport
	lappend protocolList $protocolVport/protocols
    }
    return $protocolList
}

proc ClearPortOwnership {{portList None}} {
    # This Proc could get all the ports dynamically or you could pass in 
    # a list of ports.
    #
    # WARNING: If you don't pass in a list of $portList, then this function
    #          will clear port ownership on ALL the ports connected to your chassis.
    # 
    # portList: The format is:  [list "$ixChassisIp $cardNum $portNum" ...]

    if {$portList == "None"} {
	set configuredPorts [GetPortsAssignedToVports]
	set portList [lindex $configuredPorts 0]
    }

    puts \n
    foreach port $portList {
	set ixChassisIp [lindex $port 0]
	set cardId [lindex $port 1]
	set portId [lindex $port 2]
    
	set isPortOwned [ixNet getAttribute [ixNet getRoot]/availableHardware/chassis:"$ixChassisIp"/card:$cardId/port:$portId -owner]

	if {$isPortOwned != ""} {
	    puts "ClearPortOwnership: $ixChassisIp/$cardId/$portId"
	    set chassisObj [lindex [ixNet getList [ixNet getRoot]/availableHardware chassis] end]
	    if {[catch {ixNet exec clearOwnership [ixNet getRoot]/availableHardware/chassis:"$ixChassisIp"/card:$cardId/port:$portId} errMsg]} {
		puts "\nError: ClearPortOwnership: $errMsg"
		return 1
	    }
	} else {
	    puts "ClearPortOwnership: $ixChassisIp/$cardId/$portId is not currently owned"
	}
    }
    return 0
}

proc ReleaseAllPorts {} {
    puts "\nReleaseAllPorts"
    set status [ixNet exec releaseAllPorts]
    puts $status
}

proc ReleasePorts {{portList None}} {
    # This Proc could either get all the configured ports dynamically or you
    # could pass in a list of ports.
    # 
    # portList: The format is:  [list "$ixChassisIp $cardNum $portNum" ...]

    # If user did not include $portList, then get ports from the loaded configuration.
    # WARNING: This will release ALL the ports that is connected to your chassis.
    if {$portList == "None"} {
	set configuredPorts [GetPortsAssignedToVports]
	set portList [lindex $configuredPorts 0]
	set vportList [lindex $configuredPorts 1]
    }

    if {$portList != "None"} {
	set vportList [GetVportMappingToPhyPort $portList]
    }
    if {$vportList == 0 || $vportList == ""} {
	return 0
    }
    puts "releasePorts vportList: $vportList"
    
    foreach vport $vportList {
	# chassis="192.168.70.11" card="1" port="1" portip="192.168.70.12"
	set assignedTo [ixNet getAttribute $vport -assignedTo]
	set chassisIp [string map {\" ""}  [lindex [split $assignedTo :] 0]]
	set cardId [string map {\" ""} [lindex [split $assignedTo :] 1]]
	set portId [string map {\" ""} [lindex [split $assignedTo :] 2]]

	if {[lsearch -regexp $portList "$chassisIp $cardId $portId"] != -1} {
	    puts "ReleasePorts: $chassisIp/$cardId/$portId"
	    if {[catch {ixNet exec releasePort $vport} errMsg]} {
		puts "\nError: ReleasePorts: $errMsg"
		return 1
	    }
	}
    }
    return 0
}


proc ConfigLicenseServer {{licenseServerIp None} {licenseMode None} {licenseTier None} } {
    # licenseServerIp: The license server IP.
    # licenseMode: subscription | perpetual| mixed
    # licenseTier: tier1 | tier2 | tier3 ...

    if {$licenseServerIp != "None"} {
	puts "\nConfiguring license server: $licenseServerIp"
	if {[catch {set status [ixNet setAttribute [ixNet getRoot]/globals/licensing -licensingServers $licenseServerIp]} errMsg]} {
	    puts "Error: ConfigLicenseServerIp: $errMsg"
	    return 1
	}
    }
    if {$licenseMode != "None"} {
	puts "Configuring license mode: $licenseMode"
	if {[catch {set licenseServer [ixNet setAttribute [ixNet getRoot]/globals/licensing -mode $licenseMode]} errMsg]} {
	    puts "Error: ConfigLicenseMode: $errMsg"
	    return 1
	}
    }
    if {$licenseTier != "None"} {
	puts "Configuring license tier: $licenseTier"
	if {[catch {set licenseServer [ixNet setAttribute [ixNet getRoot]/globals/licensing -tier $licenseTier]} errMsg]} {
	    puts "Error: ConfigLicenseServerIp: $errMsg"
	    return 1
	}
    }
    ixNet commit
    return 0
}

proc VerifyPortState { {StopTimer 120} } {
    set portDownList {}
    set startTimer 1
    set stopTime $StopTimer
    puts \n
    foreach vPort [ixNet getList [ixNet getRoot] vport] {
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

# ixNet exec stopAllProtocols
proc StopAllProtocols {} {
    puts"StopAllProtocols ..."
    catch {ixNet exec stopAllProtocols} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "StopAllProtocols failed: $errMsg\n"
	return 1
    }
    ixNet commit
    Sleep 10000
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

proc GetTrafficItemNames {} {
    # Return a list of the configured Traffic Item names

    set trafficItemNames {}
    set trafficItemObjList [ixNet getList [ixNet getRoot]/traffic trafficItem]
    foreach trafficItemObj $trafficItemObjList {
	set trafficItemName [ixNet getAttribute $trafficItemObj -name]
	lappend trafficItemNames $trafficItemName
    }
    return $trafficItemNames
}

proc GetTrafficItemObjects {{trafficItemName None}} {
    # Get the Traffic Item objects: trafficItemObj, configElementObj and endpointSetObj
    #    - trafficItemObj: Configures bi-directional traffic, tracking, one-to-one meshing.
    #    - configElement:  Configures frameSizes, lineRate
    #    - endpointSetObj: The source/dest endpoints and name
    #
    # Parameter
    #    trafficItemName: Provide a traffic item name to look for. This is optional.
    #                     If no traffic item name is specified, then return the 
    #                     first trafficItemObj, configElementObj and endpointSetObj.

    set trafficItemObjList [ixNet getList [ixNet getRoot]/traffic trafficItem]
    foreach trafficItemObj $trafficItemObjList {
	set trafficItemObjName [ixNet getAttribute $trafficItemObj -name]
	set configElementObj [ixNet getList $trafficItemObj configElement]
	set endpointSetObj [ixNet getList $trafficItemObj endpointSet]

	if {$trafficItemName != "None" && $trafficItemName == $trafficItemObjName} {
	    return [list $trafficItemObj $configElementObj $endpointSetObj]
	}
	if {$trafficItemName == "None"} {
	    # If user did not specify which Traffic Item object to get by a name, 
	    # return the first objects
	    return [list $trafficItemObj $configElementObj $endpointSetObj]
	}
    }
    puts "\nError: GetTrafficItemObjects: No traffic item name found in configuration: $trafficItemName"
    return 0
}

proc GetConfigElementObj {trafficItemObj} {
    return [ixNet getList $trafficItemObj configElement]
}

proc ConfigFrameSize {args} {
    set params {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg { 
	    -configElementObj {
		set configElementObj [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -type {
		# auto, fixed, increment, presetDistribution, quadGaussian, random, weightedPairs
		set type [lindex $args [expr $argIndex + 1]]
		append params " -type $type"
		incr argIndex 2
	    }
	    -frameSize {
		set frameSize [lindex $args [expr $argIndex + 1]]
		append params " -fixedSize $frameSize"
		incr argIndex 2
	    }
	    -randomMin {
		set randomMin [lindex $args [expr $argIndex + 1]]
		append params " -randomMin $randomMin"
		incr argIndex 2
	    }
	    -randomMax {
		set randomMax [lindex $args [expr $argIndex + 1]]
		append params " -randomMax $randomMax"
		incr argIndex 2
	    }
	    -incrementFrom {
		set incrementFrom [lindex $args [expr $argIndex + 1]]
		append params " -incrementFrom $incrementFrom"
		incr argIndex 2
	    }
	    -incrementTo {
		set incrementTo [lindex $args [expr $argIndex + 1]]
		append params " -incrementTo $incrementTo"
		incr argIndex 2
	    }
	    -incrementStep {
		set incrementStep [lindex $args [expr $argIndex + 1]]
		append params " -incrementStep $incrementStep"
		incr argIndex 2
	    }
	    default {
		puts "\nError ConfigFrameSize: No such parameter: $currentArg"
	    }
	}
    }

    puts "\nConfigFrameSize: $params"
    if {[catch {eval ixNet setMultiAttribute $configElementObj/frameSize $params} errMsg]} {
	puts "Error: ConfigFrameSize: $params"
	return 1
    }
    ixNet commit
    return 0
}

proc ConfigFrameRate {args} {
    set params {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg { 
	    -configElementObj {
		set configElementObj [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -type {
		# percentLineRate, framesPerSecond, bitsPerSecond, interPacketGap
		set type [lindex $args [expr $argIndex + 1]]
		append params " -type $type"
		incr argIndex 2
	    }
	    -rate {
		set rate [lindex $args [expr $argIndex + 1]]
		append params " -rate $rate"
		incr argIndex 2
	    }
	    -interPacketGapUnitsType {
		set interPacketGapUnitsType [lindex $args [expr $argIndex + 1]]
		append params " -interPacketGapUnitsTyhpe $interPacketGapUnitsType"
		incr argIndex 2
	    }
	    -enforceMinimumInterPacketGap {
		set enforceMinimumInterPacketGap [lindex $args [expr $argIndex + 1]]
		append params " -enforceMinimumInterPacketGap $enforceMinimumInterPacketGap"
		incr argIndex 2
	    }
	    -bitRateUnitsType {
		set bitRateUnitsType [lindex $args [expr $argIndex + 1]]
		append params " -bitRateUnitsType $bitRateUnitsType"
		incr argIndex 2
	    }
	    default {
		puts "\nError ConfigFrameRate: No such parameter: $currentArg"
	    }
	}
    }

    puts "\nConfigFrameRate: $params"
    if {[catch {eval ixNet setMultiAttribute $configElementObj/frameRate $params} errMsg]} {
	puts "Error: ConfigFrameRate: $params"
	return 1
    }
    ixNet commit
    return 0
}

proc ConfigFramePayload {args} {
    set params {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg { 
	    -configElementObj {
		set configElementObj [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -type {
		# custom, decrementByte, decrementWord, incrementByte, incrementWord, random
		set type [lindex $args [expr $argIndex + 1]]
		append params " -type $type"
		incr argIndex 2
	    }
	    -customPattern {
		set customPattern [lindex $args [expr $argIndex + 1]]
		append params " -customPattern $customPattern"
		incr argIndex 2
	    }
	    # True|False
	    -customRepeat {
		set customRepeat [lindex $args [expr $argIndex + 1]]
		append params " -customRepeat $customRepeat"
		incr argIndex 2
	    }
	    default {
		puts "\nError ConfigFrameRate: No such parameter: $currentArg"
	    }
	}
    }

    puts "\nConfigFramePayload: $params"
    if {[catch {eval ixNet setMultiAttribute $configElementObj/framePayload $params} errMsg]} {
	puts "Error: ConfigFramePayload: $params"
	return 1
    }
    ixNet commit
    return 0
}

proc ConfigPortSpeed {args} {
    # Parameters:
    #    -port "$ixChassisIp 1 2"
    #    -portList [list "$ixChassisIp 1 2" "$ixChassisIp 1 3"]
    #
    #    -cardType: ethernet, ethernetvm, hubndredGigLan, novusHundredGigLan, novusTenGigLan
    #		    fc, fortyGigLan, OAM, pos, tenFourtyHundredGigLan, tenGigLan, tenGigWan
    #    -speed
    #        For -cardType ethernet
    #           -autoNegotiate: True|False
    #           -speed: auto, speed1000, speed100fd, speed100hd, speed10fd, speed10hd
    #
    #        For -cardType ethernetvm
    #            -speed speed100, speed1000, speed10g, speed2000, speed20g, speed25g, speed3000, speed30g, 
    #                   speed4000, speed5000, speed50g, speed6000, speed7000, speed9000
    #
    #        For -cardType hundredGigLan
    #            -speed speed100g, speed40g   
    #
    #        For -cardType novusHundredGigLan
    #           -enableAutoNegotiation: True|False
    #           -speed: speed100g, speed10g, speed25g, speed40g, speed50g
    #
    #        For -cardType novusTenGigLan
    #           -autoNegotiate: True|False
    #           -speed: speed1000, speed100fd, speed10g, speed2.5g, speed5g
    # 
    # Look below under -speed for parameter inputs.
    # Note: Some port speed doesn't have autonegotation.

    set params {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg { 
	    -port {
		set port [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -portList {
		set portList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -cardType {
		# ethernet, ethernetvm, hubndredGigLan, novusHundredGigLan, novusTenGigLan
		# fc, fortyGigLan, OAM, pos, tenFourtyHundredGigLan, tenGigLan, tenGigWan
		set cardType [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -speed {
		set speed [lindex $args [expr $argIndex + 1]]
		append params " -speed $speed"
		incr argIndex 2
	    }
	    -autonegotiate {
		# True|False
		set autonegotiate [lindex $args [expr $argIndex + 1]]
		append params " -autonegotiate $autonegotiate"
		incr argIndex 2
	    }
	    default {
		puts "\nError ConfigPortSpeed: No such parameter: $currentArg"
	    }
	}
    }

    set vportList {}
    if {[info exists portList]} {
	set vportList [GetVportMappingToPhyPort [list $portList]]
    }

    if {[info exists port]} {
	set vportList [GetVportMappingToPhyPort [list $port]]
    }

    puts "\nConfigPortSpeed: vports: $vportList"
    foreach vportObj $vportList {
	puts "\nConfigPortSpeed: $vportObj $params"
	set result [eval ixNet setAttribute $vportObj/l1Config/$cardType $params]
	puts "\tresult: $result"
	if {$result != "::ixNet::OK"} {
	    puts "\nError ConfigPortSpeed"
	    return 1
	}
    }
    ixNet commit
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

proc StopTraffic { {includeApplyTraffic apply} } {
    set traffic [ixNet getRoot]traffic
    puts "StopTraffic ..."
    catch {ixNet exec stop $traffic} errMsg
    if {$errMsg != "::ixNet::OK"} {
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
    #puts "\n$columnList\n"
    
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
    #puts "\ntotal Pages: $totalPages"

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
		
		puts "\n  $row:"
		for {set index 0} {$index <[llength $cellList]} {incr index} {
		    keylset getStats flow.$row.[join [lindex $columnList $index] _] [lindex $cellList $index]
		    puts "\t[join [lindex $columnList $index] _]: [lindex $cellList $index]"
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
	if {$key == ""} {
	    continue
	}
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

proc RemoveTrafficItemByName { trafficItemName } {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set currentTiName [ixNet getAttribute $trafficItem -name]

	if {[regexp $trafficItemName $currentTiName]} {
	    puts "\nRemoveTrafficItemByName: $currentTiName"
	    ixNet remove $trafficItem
	    ixNet commit
	    return 0
	}
    }
    puts "\nError RemoveTrafficItemByName: No Traffic Item Name found: $trafficItemName"
    return 0
}

proc GetEndpointSetHandle { trafficItemHandle endpointSetName } {
    # Each Traffic Item can configure many EndpointSets.
    # Each EndpointSet handle looks like this:
    #     ::ixNet::OBJ-/traffic/trafficItem:4/highLevelStream:1
    #
    # Return the EndpointSet handle that matches the $flowGroupName.
    
    set highLevelStreamId ""
    foreach endpointSet [ixNet getList $trafficItemHandle highLevelStream] {
	set currentName [ixNet getAttrib $endpointSet -name]
	if {[regexp ".*$endpointSetName.*" $currentName]} {
	    set highLevelStreamId $endpointSet
	    break
	}
    }
    
    if {$highLevelStreamId == ""} {
	return 0
    }
    return $highLevelStreamId
}

proc EnableTrafficItem { trafficItemName {disable true} } {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set currentTiName [ixNet getAttribute $trafficItem -name]

	if {$trafficItemName == $currentTiName} {
	    puts "\nEnableTrafficItem: $trafficItemName\n"
	    puts "[ixNet getAttribute $trafficItem -enabled]"
	    ixNet setAttribute $trafficItem -enabled $disable
	    ixNet commit

	    return
	}
    }
    # Return 0 if Traffic Item is not found
    return 0
}

proc DisableAllTrafficItems {} {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	puts "\nDisableAllTrafficItems: $trafficItem"
	ixNet setAttribute $trafficItem -enabled false
    }
    ixNet commit
}

proc EnableAllTrafficItems {} {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	puts "\nEnableAllTrafficItems: $trafficItem"
	ixNet setAttribute $trafficItem -enabled true
    }
    ixNet commit
}

proc ConfigFlowGroupName { streamId name } {
    # This is the Flow Group (EndpointSet)
    # You can pass in either the configElement or highLevelStream API
    
    after 5000
    puts "\nConfigFlowGroupName: $streamId: $name"
    ixNet setAttribute $streamId -name $name
    ixNet commit
}

proc EnableFlowGroup { streamId } {
    puts "\nEnableFlowGroup: $streamId"
    ixNet setAttribute $streamId -suspend False
    ixNet commit
}

proc SuspendFlowGroup { streamId } {
    puts "\nSuspendFlowGroup: $streamId"
    ixNet setAttribute $streamId -suspend True
    ixNet commit
}

proc EnableGlobalArpForEachIp { {args ""} } {
    # For Static IP w/Auth
    # Need to enable this at:
    # Traffic Options -> Protocol Options -> IP

    set enable true ;# true|false
    set arpRate 300
    set maxOutstanding 300
    set sendOneArpFromEachGateway false ;# true|false
    
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg { 
	    -enable {
		set enable [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -arpRate {
		set arpRate [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -maxOutstanding {
		set maxOutstanding [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -sendOneArpFromEachGateway {
		set sendOneArpFromEachGateway [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "\nError EnableGlobalArpForEachIp: No such parameter"
	    }
	}
    }

    foreach global [ixNet getList [ixNet getRoot]globals/protocolStack ipGlobals] {
	puts "\nEnableGlobalArpForEachIp"
	ixNet setMultiAttribute $global \
	    -enableGatewayArp $enable \
	    -gatewayArpRequestRate $arpRate \
	    -maxOutstandingGatewayArpRequests $maxOutstanding \
	    -sendOneArpFromEachInterface $sendOneArpFromEachGateway
	ixNet commit
    }
}

proc StartProtocol { protocol } {
    # Start a protocol on all the ports that has the protocol enabled

    set root [ixNet getRoot]

    foreach vport [ixNet getList $root vport] {
	set port [ixNet getAttribute $vport -assignedTo]
	puts "$vport : $port"
	puts "Enabled = [ixNet getAttribute $vport/protocols/[string tolower $protocol] -enabled]"

	if {[ixNet getAttribute $vport/protocols/[string tolower $protocol] -enabled] == "true"} {
	    puts "Starting $protocol on $port"
	    catch {ixNet exec start $vport/protocols/[string tolower $protocol]} errMsg
	    if {$errMsg != "::ixNet::OK"} {
		puts "Error: Failed to start $protocol on port $port"
	    } else {
		puts "Started $protocol on port $port"
	    }
	}
    }
}

proc StopProtocol { protocol } {
    # Stop a protocol on all the ports that has the protocol enabled
    set root [ixNet getRoot]

    foreach vport [ixNet getList $root vport] {
	set port [ixNet getAttribute $vport -assignedTo]
	if {[ixNet getAttribute $vport/protocols/[string tolower $protocol] -enabled] == "true"} {
	    catch {ixNet exec stop $vport/protocols/[string tolower $protocol]} errMsg
	    if {$errMsg != "::ixNet::OK"} {
		puts "Error: Failed to stop $protocol on port $port"
	    } else {
		puts "Stopped $protocol on port $port"
	    }
	}
    }
}

proc StartProtocolOnPortList { portList protocolList } {
    # You can pass in a list of ports and a list of protocols
    # portList format = 1/1
    
    foreach protocol $protocolList {
	foreach port $portList {
	    set vport [GetVportMapping $port]
	    puts "StartProtocol: $port"
	    catch {ixNet exec start $vport/protocols/[string tolower $protocol]} errMsg
	    if {$errMsg != "::ixNet::OK"} {
		puts "\nError StartProtocol: $port: $errMsg\n"
		return 1
	    }
	}
    }
    after 5000
    return 0
}

proc StopProtocolOnPortList { portList protocolList } {
    # You can pass in a list of ports and a list of protocols
    # portList format = 1/1

    foreach protocol $protocolList {
	foreach port $portList {
	    set vport [GetVportMapping $port]
	    puts "StopProtocol: $port"
	    catch {ixNet exec stop $vport/protocols/[string tolower $protocol]} errMsg
	    if {$errMsg != "::ixNet::OK"} {
		puts "\nStopProtocol: $port: $errMsg\n"
		return 1
	    }
	}
    }
    after 5000
    return 0
}

proc StartStopPortProtocolNgpf { portList action protocol } {
    # NOTE: 
    #     This API will start/stop a protocol on all Device Groups 
    #     that the port belongs to.
    #
    #     If you want to start/stop a specific Device Group, then
    #     call StartStopDeviceGroupProtocolNgpf.
    #
    # portList = One or more ports in a list. Port format = 1/1.  Not 1/1/1.
    # action   = start or stop
    # protocol = Only one protocol

    # ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1
    # ixNet execute igmpStartHost|igmpStopHost $igmp
    #
    # protocol:
    #    ethernet, ipv4, ipv6, bgpIpv4Peer, dhcpv4relayAgent, dhcpv4server, greoipv4, igmpHost, igmpQuerier
    #    lac, ldpBasicRouter, ldpConnectedInterface, lns, ospfv2, pimV4Interface, port
    #    ptp, rsvpteIf, vsvpteLsps, staticMPLS, tag, vxlan

    set supportedProtocols "ethernet, ipv4, ipv6, bgpIpv4Peer, dhcpv4relayAgent, dhcpv4server, greoipv4, igmpHost, igmpQuerier lac, ldpBasicRouter, ldpConnectedInterface, lns, ospfv2, pimV4Interface, port, ptp, rsvpteIf, vsvpteLsps, staticMPLS, tag, vxlan"

    if {$action == "start" && $protocol == "igmpHost"} {
	set action igmpStartHost
    }
    if {$action == "stop" && $protocol == "igmpHost"} {
	set action igmpStopHost
    }
    
    set root [ixNet getRoot]

    foreach port $portList {
	set portDiscoveredFlag 0
	foreach topology [ixNet getList $root topology] {
	    foreach portObj [ixNet getList $topology port] {
		set vport [ixNet getAttribute $portObj -vport]
		
		# ::ixNet::OBJ-/availableHardware/chassis:"10.10.10.2"/card:1/port:1
		set connectedTo [ixNet getAttribute $vport -connectedTo]
		set chassis [lindex [split $connectedTo /] 3]
		set cardNum [lindex [split [lindex [split $connectedTo /] 3] :] end]
		set portNum [lindex [split [lindex [split $connectedTo /] 4] :] end]
		
		if {$port == "$cardNum/$portNum"} {
		    set portDiscoveredFlag 1
		    if {$protocol == "ethernet"} {
			foreach deviceGroup [ixNet getList $topology deviceGroup] {
			    foreach ethernet [ixNet getList $deviceGroup ethernet] {
				catch {ixNet execute $action $ethernet} errMsg
				if {$errMsg != "::ixNet::OK"} {
				    puts "\nError StartStopPortProtocolNgpf: Failed to $action $protocol NGPF protocol on port $port\n"
				    return 1
				} else {
				    puts "\nStartStopPortProtocolNgpf: Successfully $action NGPF $protocol protocol on port $port\n"
				    puts "\tOn $ethernet"
				}
			    }
			}
		    }

		    if {$protocol == "ipv4" || $protocol == "ipv6"} {
			foreach deviceGroup [ixNet getList $topology deviceGroup] {
			    foreach ethernet [ixNet getList $deviceGroup ethernet] {
				foreach ipVersion [ixNet getList $ethernet $protocol] {
				    catch {ixNet execute $action $ipVersion} errMsg
				    if {$errMsg != "::ixNet::OK"} {
					puts "\nError StartStopPortProtocolNgpf: Failed to $action $protocol NGPF protocol on port $port\n"
					return 1
				    } else {
					puts "\nStartStopPortProtocolNgpf: Successfully $action NGPF $protocol protocol on port $port"
					puts "\tOn $ipVersion"
				    }
				}
			    }
			}
		    }
		    
		    if {$protocol != "ethernet" && $protocol != "ipv4" && $protocol != "ipv6"} {
			foreach deviceGroup [ixNet getList $topology deviceGroup] {
			    foreach ethernet [ixNet getList $deviceGroup ethernet] {
				foreach ipv4 [ixNet getList $ethernet ipv4] {
				    set protocolObjDiscovered [ixNet getList $ipv4 $protocol]
				    if {$protocolObjDiscovered != ""} {
					foreach protocolObj $protocolObjDiscovered {
					    catch {ixNet execute $action $protocolObj} errMsg
					    if {$errMsg != "::ixNet::OK"} {
						puts "\nError StartStopPortProtocolNgpf: Failed to $action NGPF $port $protocol\n"
						return 1
					    } else {
						puts "\nStartStopPortProtocolNgpf: Successfully $action NGPF $protocol protocol on port $port"
						puts "\tOn $protocolObj"
					    }
					}
				    } else {
					puts "Error StartStopPortProtocolNgpf: $protocol is not configured on $port. If $protocol is configured on $port, verify correct protocol spelling:\n\n$supportedProtocols\n"
					return 1
				    }
				}
			    }
			}
		    }
		}
	    }
	}

	if {$portDiscoveredFlag == 0} {
	    puts "Error StartStopPortProtocolNgpf: No such port configured: $port"
	    return 1
	}
    }
    return 0
}

proc StartStopDeviceGroupProtocolNgpf { deviceGroupList action protocol } {
    # Description: 
    #     Only start|stop a protocol for specific device group.
    #     Every other protocol on the device group will not be touched.

    # deviceGroup = One or more device group in a list.
    #               Handle should be provided by HLT or user must know
    #               how to retrieve the device group handle somehow.
    #               Handle style: /topology:1/deviceGroup:1
    # action   = start or stop
    # protocol = Only one protocol

    # protocol:
    #    bgpIpv4Peer, dhcpv4relayAgent, dhcpv4server, greoipv4, igmpHost, igmpQuerier
    #    lac, ldpBasicRouter, ldpConnectedInterface, lns, ospfv2, pimV4Interface, port
    #    ptp, rsvpteIf, vsvpteLsps, staticMPLS, tag, vxlan

    set supportedProtocols "bgpIpv4Peer, dhcpv4relayAgent, dhcpv4server, greoipv4, igmpHost, igmpQuerier lac, ldpBasicRouter, ldpConnectedInterface, lns, ospfv2, pimV4Interface, port, ptp, rsvpteIf, vsvpteLsps, staticMPLS, tag, vxlan"

    if {$action == "start"} {
	set action startIGMP
    }
    if {$action == "stop"} {
	set action stopIGMP
    }

    set root [ixNet getRoot]

    foreach deviceGroup $deviceGroupList {
	foreach topology [ixNet getList $root topology] {
	    foreach deviceGroupObj [ixNet getList $topology deviceGroup] {
		# HLT returns handles like this: /topology:1/deviceGroup:1
		# But full path is like this: ::ixNet::OBJ-/topology:1/deviceGroup:1
		if {[lsearch -regexp $deviceGroupObj $deviceGroup] != -1} {
		    foreach ethernet [ixNet getList $deviceGroupObj ethernet] {
			foreach ipv4 [ixNet getList $ethernet ipv4] {
			    # protocolObjDiscovered: ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1
			    set protocolObjDiscovered [ixNet getList $ipv4 $protocol]
			    if {$protocolObjDiscovered != ""} {
				catch {ixNet execute $action $protocolObjDiscovered} errMsg
				if {$errMsg != "::ixNet::OK"} {
				    puts "\nError StartStopDeviceGroupProtocolNgpf: Failed to start NGPF $protocol on $deviceGroupObj\n"
				    return 1
				} else {
				    puts "\nStartStopDeviceGroupProtocolNgpf Success: $action NGPF on $deviceGroupObj\n"
				}
			    } else {
				puts "\nError StartStopDeviceGroupProtocolNgpf: $protocol is not configured on $deviceGroup. If $protocol is configured on $deviceGroup, verify correct protocol spelling:\n\n$supportedProtocols\n"
			    }
			}
		    }
		}
	    }
	}
    }
    return 0
}

proc StartStaticAuthProtocol { portList } {
    foreach port $portList {
	set vport [GetVportMapping $port]
	set etherObj [lindex [ixNet getList $vport/protocolStack ethernet] 0]
	catch {ixNet exec start $etherObj} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError StartStaticAuthProtocol: Starting Static IP/Auth on $port: $errMsg\n"
	    return 1
	} else {
	    puts "\nStartStaticAuthProtocol: Successfully started Static IP/Auth on $port: $errMsg"
	}
    }
}

proc StopStaticAuthProtocol { portList } {
    foreach port $portList {
	set vport [GetVportMapping $port]	
	set etherObj [lindex [ixNet getList $vport/protocolStack ethernet] 0]
	catch {ixNet exec stop $etherObj} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError StopStaticAuthProtocol: Stopping Static IP/Auth on $port: $errMsg"
	    return 1
	} else {
	    puts "\nStartStaticAuthProtocol: Successfully stopped Static IP/Auth on $port: $errMsg"
	}
    }
    return 0
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
	set chassis [lindex [split [lindex [split $connectedTo /] 2] :] end]
	set card [lindex [split [lindex [split $connectedTo /] 3] :] end]
	set portNum [lindex [split [lindex [split $connectedTo /] 4] :] end]
	set port $card/$portNum
	if {$port == $Port} {
	    return $vport
	}

    }
    return 0
}

proc GetVportMappingToPhyPort { portList} {
    # Search all vport for the port number.
    # Port format = [list [$ixChassisIp $card $port] ...]

    set vportList [ixNet getList [ixNet getRoot] vport]
    if {$vportList == ""} {
	return 0
    }

    set vportPhyPortList {}
    foreach vport $vportList {
	set connectedTo [ixNet getAttribute $vport -connectedTo]
	set chassis [lindex [lindex [split [lindex [split $connectedTo /] 2] :] end] 0]
	set card [lindex [split [lindex [split $connectedTo /] 3] :] end]
	set portNum [lindex [split [lindex [split $connectedTo /] 4] :] end]
	set port "$chassis $card $portNum"
	puts "GetVportMapping: $portList    $port"
	#if {$portList == $port} {
	#    append vportPhyPortList "$vport "
	#}

	if {[lsearch -regexp $portList $port] != -1} {
	        append vportPhyPortList "$vport "
	}
    }
    return $vportPhyPortList
}

proc RestartStaticIpAuthProtocol { portList } {
    # This API will restart all protocols.
    # Mainly for re-arping
    
    puts "\nRestartStaticIpAuthProtocol ,,,"
    StopStaticAuthProtocol $portList
    StartStaticAuthProtocol $portList
}

proc TakeSnapShot { copyToLocalPathAndFileName {view "Flow Statistics"} {getEgress 0} } {
    # This API will create a "Results" folder on the IxNetwork Tcl Server
    # C: drive if it doesn't exist.
    
    # Important note:
    #     Users must verify if traffic started successfully.  If not, don't call 
    #     TakeSnapShot.  Or else you will get the previous stats left behind on the GUI.
    #
    #     If traffic started successfully and taking a snapshot failed, this API
    #     will return 0.
    #     If snapshot is ok, it will return the $$copyToLocalPathAndFileName.

    # $copyToLocalPathAndFileName
    #    
    #    If using the HLT command to take snapshot:
    #        TakeSnapShot will put the csv result file to the path of your
    #        current destination.  For example:
    # 
    #        If you executed TaksSnapShot from /home/hgee, and you stated the destination
    #        as /home/hgee/results, then the csv snapshot result file will be in:
    #         /home/hgee/home/hgee/results/snapshot.csv.
    # 
    #    If using low level command to take snapshot:
    #         Then the csv snapshot result file will be in:
    #         /home/hgee/snapshot.csv.
    #
    # $view
    #    This parameter defaults to get statistics from Flow Statistics.
    #    Users could also select which statistics they want to collect.
    #    In the case of getting egress tracking stats, the GetEgressStats
    #    API creates a "EgressStats" statistic view.
    #    Users would need to call this API and pass in EgressStats.

    set csvWindowsPath "C:\\Results"

    # You can also add to the list "Traffic Item Statistics"
    #set listOfTrafficStats [list "Flow Statistics"]
    set listOfTrafficStats [list $view]
    set csvFileName  "[string map {" " "_"} [lindex $listOfTrafficStats 0]]"

    set root [ixNet getRoot]
    set stats $root/statistics
    
    # This is csv logging
    ixNet setAttr $stats -enableCsvLogging "true"
    ixNet setAttr $stats -csvFilePath $csvWindowsPath
    
    #"C:\Users\hgee\AppData\Local\Ixia\IxNetwork\data\logs"
    ixNet setAttr $stats -pollInterval 1
    ixNet commit

    puts "TakeSnapshot: listOfTrafficStats: $listOfTrafficStats ---"
    set opts [::ixTclNet::GetDefaultSnapshotSettings]
    #puts "\n$opts\n"

    lset opts [lsearch $opts *Location*] [subst {Snapshot.View.Csv.Location: $csvWindowsPath}]
    #lset opts [lsearch $opts *GeneratingMode*] {Snapshot.View.Csv.GeneratingMode: kAppendCSVFile}
    lset opts [lsearch $opts *GeneratingMode*] {Snapshot.View.Csv.GeneratingMode: "kOverwriteCSVFile"}
    lset opts [lsearch $opts *Settings.Name*] [subst {Snapshot.Settings.Name: $csvFileName}]
    #lset opts [lsearch $opts *Contents*] {Snapshot.View.Contents: "currentPage"}
    lset opts [lsearch $opts *Contents*] {Snapshot.View.Contents: "allPages"}
    lset opts [lsearch $opts *StringQuotes*] {Snapshot.View.Csv.StringQuotes: "False"}
    lappend opts [subst {Snapshot.View.Csv.Name: $csvFileName}]

    # opts: {Snapshot.View.Contents: "allPages"} {Snapshot.View.Csv.Location: C:\Results} {Snapshot.View.Csv.GeneratingMode: "kOverwriteCSVFile"} {Snapshot.View.Csv.StringQuotes: "False"} {Snapshot.View.Csv.SupportsCSVSorting: "False"} {Snapshot.View.Csv.FormatTimestamp: "True"} {Snapshot.View.Csv.DumpTxPortLabelMap: "False"} {Snapshot.View.Csv.DecimalPrecision: "3"} {Snapshot.Settings.Name: Flow_Statistics} {Snapshot.View.Csv.Name: Flow_Statistics}

    catch {ixTclNet::TakeViewCSVSnapshot $listOfTrafficStats $opts} errMsg

    ixNet setAttr $stats -enableCsvLogging "false"
    ixNet commit

    # HLT
    # set resultStatus [::ixia::copy_csv_fileName "$csvWindowsPath\\$csvFileName.csv" $copyToLocalPathAndFileName]

    # Original low level
    #catch {ixNet exec copyFile [ixNet readFrom "$csvWindowsPath\\tmp.[file tail [info script]]...Flow_Statistics.csv" -ixNetRelative] [ixNet writeTo $copyToLocalPathAndFileName -overwrite]} errMsg

    catch {ixNet exec copyFile [ixNet readFrom "$csvWindowsPath\\$csvFileName.csv" -ixNetRelative] [ixNet writeTo $copyToLocalPathAndFileName -overwrite]} errMsg

    puts "\nTakeSnapshot result: $errMsg\n"
    if {$errMsg != "::ixNet::OK"} {
	return 0
    } else {
	return $copyToLocalPathAndFileName
    }
}

proc ConfigStaticIpAuthVlan { args } {
    set portObjectIndex [lsearch $args -portObject]
    set portObject      [lindex $args [expr $portObjectIndex + 1]]

    # $portObject could be a list of Protocol Stack interfaces
    # So, use foreach to loop every interface even though if it is only one interface. 
    foreach intObject $portObject {
	set params {}
	set argIndex 0
	while {$argIndex < [llength $args]} {
	    set currentArg [lindex $args $argIndex]
	    switch -exact -- $currentArg { 
		-portObject {
		    incr argIndex 2
		}
		-vlanId {
		    set vlanId [lindex $args [expr $argIndex + 1]]
		    append params "-firstId $vlanId "
		    incr argIndex 2
		}
		-innerVlanId {
		    set innerVlanId [lindex $args [expr $argIndex + 1]]
		    append params "-innerFirstId $innerVlanId "
		    incr argIndex 2
		}
		-priority {
		    set priority [lindex $args [expr $argIndex + 1]]
		    append params "-priority $priority "
		    incr argIndex 2
		}
		-innerPriority {
		    set innerPriority [lindex $args [expr $argIndex + 1]]
		    append params "-innerPriority $innerPriority "
		    incr argIndex 2
		}
		-incrementBy {
		    set increment [lindex $args [expr $argIndex + 1]]
		    append params "-increment $increment "
		    incr argIndex 2
		}
		-innerIncrementBy {
		    set innerIncrement [lindex $args [expr $argIndex + 1]]
		    append params "-innerIncrement $innerIncrement "
		    incr argIndex 2
		}		
		-incrementStep {
		    set incrementStep [lindex $args [expr $argIndex + 1]]
		    append params "-incrementStep $incrementStep "
		    incr argIndex 2
		}
		-innterIncrementStep {
		    set innerIncrementStep [lindex $args [expr $argIndex + 1]]
		    append params "-innerIncrementStep $innerIncrementStep "
		    incr argIndex 2
		}
		-enable {
		    # True or False
		    set enable [lindex $args [expr $argIndex + 1]]
		    append params "-enable $enable "
		    incr argIndex 2
		}
		-innerEnable {
		    # True or False
		    set innerEnable [lindex $args [expr $argIndex + 1]]
		    append params "-innerEnable $innerEnable "
		    incr argIndex 2
		}
		-name {
		    set name [lindex $args [expr $argIndex + 1]]
		    append params "-name $name "
		    incr argIndex 2
		}
		-tpid {
		    # 0x8100
		    set tpid [lindex $args [expr $argIndex + 1]]
		    append params "-tpid $tpdi "
		    incr argIndex 2
		}
		-innerTpid {
		    # 0x8100
		    set innerTpid [lindex $args [expr $argIndex + 1]]
		    append params "-innerTpid $innerTpdi "
		    incr argIndex 2
		}
		-tpid {
		    # 0x8100
		    set tpid [lindex $args [expr $argIndex + 1]]
		    append params "-tpid $tpdi "
		    incr argIndex 2
		}
		-count {
		    # 4094
		    set uniqueCount [lindex $args [expr $argIndex + 1]]
		    append params "-uniqueCount $uniqueCount "
		    incr argIndex 2
		}		
		-innerCount {
		    # 4094
		    set innerUniqueCount [lindex $args [expr $argIndex + 1]]
		    append params "-innerUniqueCount $innerUniqueCount "
		    incr argIndex 2
		}		
		default {
		    puts "\nConfigStaticIpAuthVlan ERROR: No such parameter: $currentArg"
		    return
		}
	    }
	}

	# Default 
	if {[lsearch $args -enabled] == -1} {
	    append params "-enabled True "
	}
	if {[lsearch $args $innerVlanId] != -1 && [lsearch $args -innerEnable] == -1} {
	    append params "-innerEnable True "
	}

	puts "\nConfigStaticIpAuthVlan: $intObject/vlanRange\n\t$params"
	foreach {param value} $params {
	    ixNet setAttribute $intObject/vlanRange $param $value
	}
	ixNet commit
    }
}

proc GetProtocolIntObjects { args } {
    # This API supports single chassis ports and diasy chained chassis ports.
    # 
    # This API will return you all the Protocol Interface objects
    # based on the $port and/or $vlanId
    # 
    # -port format = 1/1/3 or $ixiaChassisIp/1/3
    #       -You could pass in a list of ports also:
    #           "1/1/1 1/1/2" or "$ixiaChassisIp/1/1  $ixiaChassisIp/1/2"

    # For a single chassis, port format can be 1/1/1 or $ixiaChassisIp/1/1
    # For a daisy chained chassis, port format must be $ixiaChassisIp1/1

    # For -vlanId parameter:
    #     Currently, you can only pass in one vlan ID for a single port or for 
    #     the list of ports.

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg { 
	    -port {
		# For a single chassis, port format can be 1/1/1 or $ixiaChassisIp/1/1
		# For a daisy chained chassis, port format must be $ixiaChassisIp/1/1
		set port [lindex $args [expr $argIndex + 1]]
		set portList {}
		foreach p $port {
		    set port [join [lrange [split $p /] 1 end] /]
		    lappend portList $port
		}
		incr argIndex 2
	    }
	    -vlanId {
		set vlanId [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "\nError GetProtocolIntObjects: No such parameter: $currentArg"
		return 1
	    }
	}	    
    }

    set interfaceObjList {}
    foreach vport [ixNet getList [ixNet getRoot] vport] {
	set currentPort [ixNet getAttribute $vport -assignedTo]
	set chassis    [lindex [split $currentPort :] 0]
	set card       [lindex [split $currentPort :] 1]
	set portNumber [lindex [split $currentPort :] 2]

	if {[lsearch $portList "$card/$portNumber"] != -1 || [lsearch $portList "$chassis/$card/$portNumber"] != -1} {
	    # Get all the interface objects for the current $card/$portNumber.
	    # Because a port can have a large scale of interfaces.
	    foreach interface [ixNet getList $vport interface] {
		if {[info exists vlanId] == 0} {
		    lappend interfaceObjList $interface
		}
		
		# User can bind a vlanID to a port.
		if {[info exists vlanId] == 1} {
		    set currentVlanId [ixNet getAttribute $interface/vlan -vlanId]
		    if {$vlanId == $currentVlanId} {
			lappend interfaceObjList $interface
		    }
		}
	    }
	}
    }

    if {$interfaceObjList != ""} {
	return $interfaceObjList
    } else {
	return 0
    }
}

proc GetStaticIpAuthObjects { args } {
    # This API will return you all the Protocol Interface objects
    # based on the $port and/or $vlanId
    
    # port format = 1/1/3
    # not 1/3
    
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg { 
	    -port {
		set port [lindex $args [expr $argIndex + 1]]
		set port [join [lrange [split $port /] 1 end] /]
		incr argIndex 2
	    }
	    -vlanId {
		set vlanId [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "GetStaticIpAuthObjects: No such parameter: $currentArg"
		return 0
	    }
	}	    
    }
    
    foreach vport [ixNet getList [ixNet getRoot] vport] {
	set currentPort [ixNet getAttribute $vport -assignedTo]
	set chassis    [lindex [split $currentPort :] 0]
	set card       [lindex [split $currentPort :] 1]
	set portNumber [lindex [split $currentPort :] 2]

	if {$port == "$card/$portNumber"} {
	    set interfaceObjList {}
	    foreach ethernet [ixNet getList $vport/protocolStack ethernet] {
		foreach endpoint [ixNet getList $ethernet ipEndpoint] {
		    foreach range [ixNet getList $endpoint range] {
			
			if {[info exists port] == 1 && [info exists vlanId] == 0} {
			    #set currentIp [ixNet getAttribute $range/ipRange -ipAddress]
			    lappend interfaceObjList $range
			}

			if {[info exists port] && [info exists vlanId]} {
			    foreach vlanRange [ixNet getList $range/vlanRange vlanIdInfo] {
				set currentVlan [ixNet getAttribute $vlanRange -firstId]
				if {$currentVlan == $vlanId} {
				    lappend interfaceObjList $range
				}
			    }
			}
		    }
		}
	    }
	}
    }

    if {$interfaceObjList != ""} {
	return $interfaceObjList
    } else {
	return 0
    }
}

proc GetEgressStats { args } {
    # Remove all existing TCL Views first.
    ixNet execute removeAllTclViews

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg { 
	    -trafficItemName {
		set trafficItemName [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -port {
		set port [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -offset {
		set customOffset [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -bits {
		set bits [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -field {
		set field [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -csvFileName {
		set csvFileName [lindex $args [expr $argIndex + 1]]
		exec echo "" > $csvFileName
		incr argIndex 2
	    }
	    default {
		puts "\nError GetEgressStats: No such parameter: $currentArg"
		return 1
	    }
	}
    }
    
    set offset "Custom: ($bits bits at offset $customOffset)"

    set view [ixNet add [ixNet getRoot]statistics "view"]
    
    ixNet setMultiAttribute $view -caption "EgressView" -treeViewNodeName "Egress\\Custom\ Views" -type layer23TrafficFlow -visible true
    #ixNet setMultiAttribute $view -caption "$trafficItemName\View" -type layer23TrafficFlow -visible true
    ixNet setMultiAttribute $view -caption "EgressStats" -type layer23TrafficFlow -visible true
    ixNet commit
    set view [lindex [ixNet remapIds $view] 0]
    
    set trafficFlowFilter [ixNet add $view "layer23TrafficFlowFilter"]
    ixNet setMultiAttribute $trafficFlowFilter -egressLatencyBinDisplayOption showEgressRows
    ixNet commit
    set trafficFlowFilter [lindex [ixNet remapIds $trafficFlowFilter] 0]
    
    # ::ixNet::OBJ-/statistics/view:"EgressView"/layer23TrafficFlowFilter/enumerationFilter:L81
    set enumerationFilter2 [ixNet add $trafficFlowFilter "enumerationFilter"]
    ixNet setMultiAttribute $enumerationFilter2 -sortDirection ascending
    ixNet commit
    set enumerationFilter2 [lindex [ixNet remapIds $enumerationFilter2] 0]
    
    # ::ixNet::OBJ-/statistics/view:"EgressView"/layer23TrafficFlowFilter/enumerationFilter:L81
    set enumerationFilter3 [ixNet add $trafficFlowFilter "enumerationFilter"]
    ixNet setMultiAttribute $enumerationFilter3 -sortDirection ascending
    ixNet commit
    set enumerationFilter3 [lindex [ixNet remapIds $enumerationFilter3] 0]
    
    puts "\n-portFilterIds: [list $view/availablePortFilter:"$port"]"
    # The -portFilterIds needs to be in this format:
    # ::ixNet::OBJ-/statistics/view:"EgressStats"/availablePortFilter:"10.205.4.155/Card1/Port2"
    # layer23TrafficFlowFilter will use the -portFilterIds port handles to retrieve egress stats from.
    ixNet setMultiAttribute $trafficFlowFilter -portFilterIds [list $view/availablePortFilter:"$port"]
    ixNet setMultiAttribute $trafficFlowFilter -trafficItemFilterIds [list $view/availableTrafficItemFilter:"$trafficItemName"]
    ixNet setMultiAttribute $enumerationFilter2 -trackingFilterId $view/availableTrackingFilter:"$offset"
    ixNet setMultiAttribute $enumerationFilter3 -trackingFilterId $view/availableTrackingFilter:"$field"
    
    catch {ixNet commit} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "\nError GetEgressStats: $field must be selected in Flow Tracking for tracking:\n$errMsg\n"
	return 1
    }
    
    # Enable all the statistic counters
    foreach {statistic} [ixNet getList $view statistic] {
	ixNet setAttribute $statistic -enabled true
    }
    ixNet commit 
    
    puts "\nGetEgressStats: Created and enabling: $view"
    puts "\nRetrieving egress stats is intense processing."
    puts "Please wait ~1.5 minutes ..."
    
    catch {ixNet setMultiAttribute $view -enabled true} errMsg
    puts "\nGetEgressStats: Enabling statView $view : $errMsg"
    catch {ixNet commit} errMsg
    
    # These are all the stat counters on the page
    set columnList [ixNet getAttribute ${view}/page -columnCaptions]

    if {[info exists csvFileName]} {
	# Using a foreach loop to add a comma in between each item for csv.
	set newColumnList {}
	set needComma false
	foreach item $columnList {
	    if {$needComma} {
		# Don't put a comma in front.
		# And don't put a comma at the end.
		append newColumnList ,
	    } else {
		set needComma true
	    }
	    append newColumnList $item
	}
	exec echo $newColumnList >> $csvFileName
    }

    set totalPages [ixNet getAttribute $view/page -totalPages]
    
    for {set currPage 1} {$currPage <= $totalPages} {incr currPage} {
	ixNet setAttribute $view/page -currentPage $currPage
	ixNet commit
	
	set rowValues [ixNet getAttribute ${view}/page -rowValues]
	set totalRowsOfStatistics [llength $rowValues]
	
	#puts "\n---- rowValues: $rowValues ----\n"
	
	for {set pageListIndex 0} {$pageListIndex <= $totalRowsOfStatistics} {incr pageListIndex} {
	    set rowList [lindex $rowValues $pageListIndex]
	    
	    for {set rowIndex 0} {$rowIndex < [llength $rowList]} {incr rowIndex} {
		set cellLineFlag 0
		set getOneTimeOnlyFlag 0
		foreach row $rowList {
		    if {[info exists csvFileName]} {
			exec echo $row >> $csvFileName
		    }

		    #puts "\n---- foreach row: $row ----\n"
		    foreach column $columnList item $row {
			# Using cellLineFlag to control only getting stats on the 
			# first line. Ignore the second line.
			# Already parsed out the egress tracking.
			if {$cellLineFlag == 0} {
			    if {$getOneTimeOnlyFlag == 0} {
				set ingressTracking [lindex $row 1]
				#puts "\nIngressTracking: $ingressTracking"
				
				if {$column == "Rx Port"} {
				    set port [GetAssignedPort $item]
				}
				set getOneTimeOnlyFlag 1
			    }
			    
			    set column [join $column _]
			    set item   [join $item _]
			    
			    #puts "--- $column : $item ----"
			    keylset egressStats rxPort.$port.$trafficItemName.ingress.$ingressTracking.$column $item
			}			
		    }
		    
		    # We just want the egressing value. That is it.
		    if {$cellLineFlag == 1} {
			set egressTrackingIndex [lsearch $columnList "Egress Tracking"]
			set egressTracking      [lindex $row $egressTrackingIndex]
			keylset egressStats rxPort.$port.$trafficItemName.ingress.$ingressTracking.Egressing-As $egressTracking
		    }
		    set cellLineFlag 1
		}
	    }
	}
    }
    
    if {[info exists ::removeTclViewStats] == 1 && $::removeTclViewStats == 1} {
	ixNet remove $view
	ixNet commit
    }

    return $egressStats
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

proc DeviceGroupProtocolStacksNgpf { deviceGroup ipType} {
    # This Proc is an internal API for VerifyArpNgpf.
    # It's created because each deviceGroup has IPv4/IPv6 and
    # a deviceGroup could have inner deviceGroup that has IPv4/IPv6.
    # Therefore, you can loop device groups.
    set unresolvedArpList {}
    foreach ethernet [ixNet getList $deviceGroup ethernet] {
	foreach ipProtocol [ixNet getList $ethernet $ipType] {
	    # sessionStatus could be: down, up, notStarted
	    set sessionStatus [ixNet getAttribute $ipProtocol -sessionStatus]
	    set resolvedGatewayMac [ixNet getAttribute $ipProtocol -resolvedGatewayMac]
	    #puts "resolvedGatewayMac: $resolvedGatewayMac"
	    #puts "sessionStatus: $sessionStatus"
	    # Only care for unresolved ARPs.
	    # resolvedGatewayMac: 00:01:01:01:00:01 00:01:01:01:00:02 removePacket[Unresolved]
	    # Search each mac to see if they're resolved or not.
	    for {set index 0} {$index < [llength $resolvedGatewayMac]} {incr index} {
		if {[regexp ".*Unresolved.*" [lindex $resolvedGatewayMac $index]] == 1} {
		    # Getting in here means the interface should be up
		    set multiValueNumber [ixNet getAttribute $ipProtocol -address]
		    set srcIpAddrNotResolved [lindex [ixNet getAttribute [ixNet getRoot]$multiValueNumber -values] $index]
		    puts "\tFailed to resolve ARP: $srcIpAddrNotResolved"
		    lappend unresolvedArpList "$srcIpAddrNotResolved"
		    
		}
	    }
	}
    }
    
    if {$unresolvedArpList == ""} {
	puts "\tARP is resolved"
	return ""
    } else {
	return $unresolvedArpList
    }
}

proc VerifyArpNgpf { {ipType ipv4} } {
    # This Proc requires:
    #    1> DeviceGroupProtocolStacksNgpf
    #
    # ipType:  ipv4 or ipv6
    #
    # This API will verify for ARP session resolvement on 
    # every Device Group including inner Device Groups.
    # 
    # How it works?
    #    Each device group has a list of $sessionStatus: up, down or notStarted.
    #    If the deviceGroup has sessionStatus as "up", then ARP will be verified.
    #    It also has a list of $resolvedGatewayMac: MacAddress or removePacket[Unresolved]
    #    These two $sessionStatus and $resolvedGatewayMac lists are aligned.
    #    If lindex 0 on $sessionSatus is up, then $resolvedGatewayMac on index 0 expects 
    #    to have a mac address.  Not removePacket[Unresolved].
    #    If not, then arp is not resolved.
    #
    # Return 0 if ARP passes.
    # Return 1 if device group is not started
    # Returns a list of unresolved ARPs (src ip)

    set startFlag 0
    set unresolvedArpList {}
    foreach topology [ixNet getList [ixNet getRoot] topology] {
	foreach deviceGroup [ixNet getList $topology deviceGroup] {
	    puts "\n$deviceGroup"
	    set deviceGroupStatus [ixNet getAttribute $deviceGroup -status]
	    puts "\tdeviceGroup Status: $deviceGroupStatus"
	    if {$deviceGroupStatus == "started"} {
		set startFlag 1
		set arpResult [DeviceGroupProtocolStacksNgpf $deviceGroup $ipType]
		if {$arpResult != ""} {
		    set unresolvedArpList [concat $unresolvedArpList $arpResult]
		}
		
		if {[ixNet getList $deviceGroup deviceGroup] != ""} {
		    foreach innerDeviceGroup [ixNet getList $deviceGroup deviceGroup] {
			puts "\n$innerDeviceGroup"
			set deviceGroupStatus1 [ixNet getAttribute $innerDeviceGroup -status]
			puts "\tInner deviceGroup Status: $deviceGroupStatus1"
			if {$deviceGroupStatus == "started"} {
			    set arpResult [DeviceGroupProtocolStacksNgpf $innerDeviceGroup $ipType]
			    if {$arpResult != ""} {
				set unresolvedArpList [concat $unresolvedArpList $arpResult]
			    }
			}
		    }
		}
	    } elseif {[ixNet getAttribute $deviceGroup -status] == "mixed"} {
		set startFlag 1
		puts "\tWarning: Ethernet stack is started, but layer3 is not started"
		set arpResult [DeviceGroupProtocolStacksNgpf $deviceGroup $ipType]
		if {$arpResult != ""} {
		    set unresolvedArpList [concat $unresolvedArpList $arpResult]
		}
		
		if {[ixNet getList $deviceGroup deviceGroup] != ""} {
		    foreach innerDeviceGroup [ixNet getList $deviceGroup deviceGroup] {
			puts "\n$innerDeviceGroup"
			set deviceGroupStatus2 [ixNet getAttribute $innerDeviceGroup -status]
			puts "\tInner deviceGroup Status: $deviceGroupStatus2"
			if {$deviceGroupStatus2 == "started"} {
			    set arpResult [DeviceGroupProtocolStacksNgpf $innerDeviceGroup $ipType]
			    if {$arpResult != ""} {
				set unresolvedArpList [concat $unresolvedArpList $arpResult]
			    }
			}
		    }
		}		
	    } else {
		puts "\nVerifyArpNgpf: Protocol not started successfuly on:\n\t$deviceGroup"
	    }
	}
    }

    if {$unresolvedArpList == "" && $startFlag == 1} {
	return 0
    }
    if {$unresolvedArpList == "" && $startFlag == 0} {
	return 1
    }
    if {$unresolvedArpList != "" && $startFlag == 1} {
	puts \n
	foreach unresolvedArp $unresolvedArpList {
	    puts "VerifyArpNgpf: UnresolvedArps: $unresolvedArp"
	}
	puts \n
	return $unresolvedArpList
    }
}

proc ConfigIgmpSourceMode { igmpSessionHandle mode } {
    # igmpSessionHandle: ::ixNet::OBJ-/vport:1/protocols/igmp/host:3/group:3
    # mode: include or exclude

    # Usage example:
    #    -mode create
    #    -session_handle ::ixNet::OBJ-/vport:1/protocols/igmp/host:3
    #    -source_pool_handle [list source1 source2] 
    #    -group_pool_handle group3 

    puts  "\nConfigIgmpSourceMode: $igmpSessionHandle"
    ixNet setAttribute $igmpSessionHandle -sourceMode $mode
    ixNet commit
}

proc IgmpJoinLeaveNgpf { port igmpGroupAddrList action } {
    # This API allows you to specify port(s) to either join or leave an igmp group address.

    # port = The port to join or leave the igmp group address.
    # igmpGroupAddrList = One or more igmp group address in a list to join or leave.
    # action = igmpJoinGroup or igmpLeaveGroup

    set root [ixNet getRoot]

    set portDiscoveredFlag 0
    foreach topology [ixNet getList $root topology] {
	foreach portObj [ixNet getList $topology port] {
	    set vport [ixNet getAttribute $portObj -vport]
	    
	    # ::ixNet::OBJ-/availableHardware/chassis:"10.10.10.2"/card:1/port:1
	    set connectedTo [ixNet getAttribute $vport -connectedTo]
	    set chassis [lindex [split $connectedTo /] 3]
	    set cardNum [lindex [split [lindex [split $connectedTo /] 3] :] end]
	    set portNum [lindex [split [lindex [split $connectedTo /] 4] :] end]
	    
	    if {$port == "$cardNum/$portNum"} {
		set portDiscoveredFlag 1
		foreach deviceGroup [ixNet getList $topology deviceGroup] {
		    foreach ethernet [ixNet getList $deviceGroup ethernet] {
			foreach ipv4 [ixNet getList $ethernet ipv4] {
			    set protocolObjDiscovered [ixNet getList $ipv4 igmpHost]
			    if {$protocolObjDiscovered != ""} {
				foreach igmpGroupRangeObj [ixNet getList $protocolObjDiscovered igmpMcastIPv4GroupList] {
				    
				    foreach igmpPortObj [ixNet getList $igmpGroupRangeObj port] {
					# igmpPortObj = ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList/port:1
					foreach rangeObj [ixNet getList $igmpPortObj item] {
					    #rangeObj = ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1/ipv4:1/igmpHost:1/igmpMcastIPv4GroupList/port:1/item:1
					    set igmpHostGroupAddr [ixNet getAttribute $rangeObj -startMcastAddr]
					    if {[lsearch $igmpGroupAddrList $igmpHostGroupAddr] != -1} {
						catch {ixNet execute $action $rangeObj} errMsg
						if {$errMsg != "::ixNet::OK"} {
						    puts "\nError IgmpJoinLeaveNgpf: Faied to $action NGPF on $port"
						    return 1
						} else {
						    puts "\nIgmpJoinLeaveNgpf Success: $action $port NGPF"
						}
					    }
					}
				    }
				}
			    } else {
				puts "\nError IgmpJoinLeaveNgpf: $protocol is not configured on $port. If $protocol is configured on $port, verify correct protocol spelling:\n\n$supportedProtocols\n"
				return 1
			    }
			}
		    }
		}
	    }
	}
    }
    if {$portDiscoveredFlag == 0} {
	puts "\nError IgmpJoinLeaveNgpf: No such port configured: $port"
	return 1
    }
}

proc ModifyIgmpGroupRanges { portList igmpGroupCount } {
    # portList = One port or a list of ports in format of: "1/2 1/3 1/5"
    # igmpGroupCount = A list of group counts for each port: "100 200 300"

    # For example:
    #    If modifying one port, then: 1/1 200
    #    If modifying two ports, then: "1/1 1/2" "100 200"

    if {[llength $portList] != [llength $igmpGroupCount]} {
	puts "\nError: ModifyIgmpGroupRanges: The number of portList and igmpGroupCount are not the same"
	return 1
    }

    for {set index 0} {$index < [llength $portList]} {incr index} {
	set port [lindex $portList $index]
	set vport [GetVportMapping $port]

	foreach igmpHostNumber [ixNet getList $vport/protocols/igmp host] {
	    foreach igmpHostGroupNumber [ixNet getList $igmpHostNumber group] {
		puts "\nModifyIgmpGroupRanges: $port igmpGroupCount=$igmpGroupCount"
		ixNet setAttribute $igmpHostGroupNumber -groupCount [lindex $igmpGroupCount $index]
		ixNet commit		
	    }
	}
    }
    return 0
}

proc IsPortInCaptureState { port } {
    # port format: 1/3
    #
    # If port is in capture state, will return "ready"
    # If port is not in capture state, will return:
    #     "::ixNet::ERROR-Data  capture is not selected on the specified port."

    set vport [GetVportMapping $port]
    if {[ixNet getAttribute $vport/capture -dataCaptureState] == "ready"} {
	return 1
    }
    if {[ixNet getAttribute $vport/capture -controlCaptureState] == "ready"} {
	return 1
    }
    return 0
}

proc CloseAllCapturedDatas {} {
    ixNet exec closeAllTabs
}

proc StartBgpProtocolNgpf { bgpHandle } {
    puts "\nStartBgpProtocolNgpf: $bgpHandle"
    ixNet execute start $bgpHandle
}

proc StopBgpProtocolNgpf { bgpHandle } {
    puts "\nStopBgpProtocolNgpf: $bgpHandle"
    ixNet execute stop $bgpHandle
}

proc EnableTrafficItemByName { Name } {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set trafficItemName [ixNet getAttribute $trafficItem -name]

	if {[regexp $Name $trafficItemName]} {
	    catch {ixNet setAttribute $trafficItem -enabled True} errMsg
	    if {$errMsg != "::ixNet::OK"} {
		puts "\nEnableTrafficItemByName Error: $Name : Failed\n:$errMsg\n"
		return 1
	    }

	    ixNet commit
	    puts "\nEnableTrafficItemByName: $Name : Done\n"
	    return 0
	} 
    }

    puts "\nEnableTrafficItemByName Error: No such traffic item name: $Name\n"
    return 1
}

proc DisableTrafficItemByName { Name } {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set trafficItemName [ixNet getAttribute $trafficItem -name]

	if {[regexp $Name $trafficItemName]} {
	    catch {ixNet setAttribute $trafficItem -enabled False} errMsg
	    if {$errMsg != "::ixNet::OK"} {
		puts "\nError DisableTrafficItemByName: $Name : $errMsg\n"
		return 1
	    }

	    ixNet commit
	    puts "\nDisableTrafficItemByName: $Name"
	    return 0
	}
    }
    puts "\nError DisableTrafficItemByName: No such traffic item name: $Name\n"
    return 1
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

proc StartOspfProtocolNgpf { ospfHandle } {
    puts "\nStartOspfProtocolNgpf: $ospfHandle"
    ixNet execute start $ospfHandle
}

proc StopOspfProtocolNgpf { ospfHandle } {
    puts "\nStopOspfProtocolNgpf: $ospfHandle"
    ixNet execute stop $ospfHandle
}

proc ModifyOspfRouteRanges { portList ospfRouteRanges } {
    # portList = One port or a list of ports in format of: "1/2 1/3 1/5"
    # ospfRouteRanges = A list of group counts for each port: "100 200 300"

    # For example:
    #    If modifying one port, then: 1/1 200
    #    If modifying two ports, then: "1/1 1/2" "100 200"

    if {[llength $portList] != [llength $ospfRouteRanges]} {
	puts "\nError: ModifyOspfRouteRanges: The number of portList and ospfRouteRanges are not the same"
	return 1
    }

    for {set index 0} {$index < [llength $portList]} {incr index} {
	set port [lindex $portList $index]
	set vport [GetVportMapping $port]

	foreach ospfRouteNumber [ixNet getList $vport/protocols/ospf router] {
	    puts "\nindex=$index ospfRouterNumber= $ospfRouteNumber  $vport"
	    foreach ospfRouteRangeNumber [ixNet getList $ospfRouteNumber routeRange] {
		puts "\nModifyOspfRouteRanges: $port ospfRouteRanges=[lindex $ospfRouteRanges $index]"
		ixNet setAttribute $ospfRouteRangeNumber -numberOfRoutes [lindex $ospfRouteRanges $index]
		ixNet commit		
	    }
	}
    }
    return 0
}

proc DeleteTrafficItem { trafficItemName } {
    set flag 0
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set currentTiName [ixNet getAttr $trafficItem -name]
	if {[regexp -nocase "(TI\[0-9]+)?$trafficItemName$" $currentTiName]} {
	    puts "\nDeleteTrafficItem: $trafficItemName"
	    catch {ixNet remove [ixNet getRoot]traffic $trafficItem} errMsg
	    if {$errMsg != "::ixNet::OK"} {
		puts "\nError DeleteTrafficItem: $errMsg"
		return 1
	    }
	    ixNet commit
	    set flag 1
	}
    }
    if {$flag == 0} {
	puts "\nError DeleteTrafficItem: No such Traffic Item name: $trafficItemName"
	return 1
    }
    return 0
}

proc DeleteAllTrafficItems {} {
    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set trafficItemName [ixNet getAttr $trafficItem -name]
	puts "\nDeleteAllTrafficItems: $trafficItemName"
	catch {ixNet remove [ixNet getRoot]traffic $trafficItem} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nDeleteAllTrafficItems: $errMsg\n"
	    return 1
	}
	ixNet commit
    }

    return 0
}

proc GetEnabledTrafficItems {} {
    set enabledTrafficItems {}

    foreach item [ixNet getList [ixNet getRoot]/traffic trafficItem] {
	if {[ixNet getAttenabenabribute $item -enabled] == "true"} {
	    lappend enabledTrafficItems $item
	}
    }

    return $enabledTrafficItems
}

proc BuildEgressView {{viewName "Egress"}} {

    puts "\nBuildEgressView - Name:$viewName"

    if { [catch {
	set egress_by_flow_view [ixNet add ::ixNet::OBJ-/statistics view]
	ixNet setMultiAttrs $egress_by_flow_view -type layer23TrafficFlow -visible true -caption $viewName
	ixNet commit

	set egress_by_flow_view [ixNet remapIds $egress_by_flow_view]
	set available_ti_filter [ixNet getL $egress_by_flow_view availableTrafficItemFilter]
	set layer23_traffic_flow_filter [ixNet getL $egress_by_flow_view layer23TrafficFlowFilter]

	ixNet setMultiAttrs $layer23_traffic_flow_filter -egressLatencyBinDisplayOption showEgressRows -trafficItemFilterIds $available_ti_filter
	ixNet commit

	set available_tracking_filter [ixNet getL $egress_by_flow_view availableTrackingFilter]
	set stat_keys [ixNet getL $egress_by_flow_view statistic]

	#Select the keys that you want to use in the view
	foreach key [lrange $stat_keys 0 end] {
	    ixNet setA $key -enabled true
	}

	set enum_filter_1 [ixNet add $layer23_traffic_flow_filter enumerationFilter]
	ixNet setMultiAttrs $enum_filter_1 -trackingFilterId [lindex $available_tracking_filter 1]

	set view_page [ixNet getList $egress_by_flow_view page]
	ixNet setAttr $view_page -egressMode conditional
	ixNet commit

	ixNet setA $egress_by_flow_view -enabled true

	ixNet commit

    } e] } {
	puts "\nError BuildEgressView: - $e"
    } else {
	puts "\nBuildEgressView: Egress view created ($egress_by_flow_view)"
    }
}

proc LinkUpDown { portNumber {action down} } {
    # action = down or up

    foreach vport [ixNet getList [ixNet getRoot] vport] {
	# ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
	set connectedTo [ixNet getAttribute $vport -connectedTo]
	set connectedTo [lrange [split $connectedTo /] 3 4]
	set card [lindex [split [lindex $connectedTo 0] :] end]
	set port [lindex [split [lindex $connectedTo 1] :] end]
	set port $card/$port

	if {$portNumber == $port} {
	    LogMessage -info "Bringing port $port: $action"
	    ixNet exec linkUpDn $vport $action
	}
    }
}

proc EnableDisableSuppressArp { ports action } {
    # Description:
    #    This API will disable or enable
    #    suppress ARP for duplicate gateway on one  
    #    port or a list of ports with ipv4.
    #

    # port = 1/1 format. Not 1/1/1
    #        You can pass in a list of ports also.
    # action = true or false or enable or disable

    # This API will take the port number and do a lookup
    # for its vport -name because suppressArp API goes
    # by the name of the port rather than the physical port.

    if {$action == "enable"} {
	set action true
    } else {
	set action false
    }

    set root [ixNet getRoot]
    set globals $root\globals
    set globalTopology $globals/topology
    set globalTopologyIpv4 $globalTopology/ipv4
    
    foreach port $ports {
	set vport [GetVportMapping $port]
	set portName [ixNet getAttribute $vport -name]

	# This is a list of all the ports and its name description
	set portNameList [ixNet getAttribute $globalTopologyIpv4 -rowNames]	
	
	# Get the multi-value number
	set multiValue [ixNet getAttribute $globalTopologyIpv4 -suppressArpForDuplicateGateway]
	
	# The portIndex is not zero-based. Begins with 1.
	set portIndex [expr [lsearch $portNameList $portName] + 1]
	
	puts "\nEnableDisableSuppressArp: Set to $action"
	if {[SetNgpfCounterMultiValue $multiValue $portIndex $action]} {
	    return 1
	}
	
    }
    return 0
}

proc EnableDisableSuppressArpAllPorts { action } {
    # Description:
    #    This API will automatically disable or enable
    #    suppress ARP for duplicate gateway on all the 
    #    ports with ipv4.

    # action = true or false or enable or disable

    if {$action == "enable"} {
	set action true
    } else {
	set action false
    }

    set root [ixNet getRoot]
    set globals $root\globals
    set globalTopology $globals/topology
    set globalTopologyIpv4 $globalTopology/ipv4
        
    set portNameList [ixNet getAttribute $globalTopologyIpv4 -rowNames]	

    foreach portName $portNameList {
	set multiValue [ixNet getAttribute $globalTopologyIpv4 -suppressArpForDuplicateGateway]
	set portIndex [expr [lsearch $portNameList $portName] + 1]

	puts "\nEnableDisableSuppressArpAllPorts: Set to $action"
	if {[SetNgpfCounterMultiValue $multiValue $portIndex $action]} {
	    return 1
	}

    }
    return 0
}

proc ModifyIgmpReportsPerSecond { portList rate } {
    # Description:
    #    This API will automatically disable or enable
    #    suppress ARP for duplicate gateway on all the 
    #    ports with ipv4.

    # action = true or false or enable or disable

    set root [ixNet getRoot]
    set globals $root\globals
    set globalTopology $globals/topology
    set globalTopologyIgmpHost $globalTopology/igmpHost
        
    set multiValue [ixNet getAttribute $globalTopologyIgmpHost -ratePerInterval]	
    set igmpHostPortList [ixNet getAttribute $globalTopologyIgmpHost -rowNames]

    foreach port $portList {
	set portIndex [expr [lsearch $igmpHostPortList $port] + 1]
	if {$portIndex == -1} {
	    puts "\nError ModifyIgmpReportPerSecond: No such port found for igmpHost: $port"
	    return 1
	}

	puts "\nModifyIgmpReportsPerSecond: $port -> $rate"
	if {[SetNgpfCounterMultiValue $multiValue $portIndex $rate]} {
	    return 1
	}
    }
    return 0
}

proc DisableDeviceGroupNgpf { deviceGroupName } {
    foreach topology [ixNet getList [ixNet getRoot] topology] {
	foreach deviceGroup [ixNet getList $topology deviceGroup] {
	    set currentDgName [ixNet getAttribute $deviceGroup -name]
	    if {[regexp -nocase $deviceGroupName $currentDgName]} {
		puts "\nDisableDeviceGroup: $currentDgName"
		set multiValue [ixNet getAttribute $deviceGroup -enabled]
		ixNet setAttribute $multiValue/singleValue -value false
		ixNet commit
	    }
	}
    }
}

proc EnableDeviceGroupNgpf { deviceGroupName } {
    foreach topology [ixNet getList [ixNet getRoot] topology] {
	foreach deviceGroup [ixNet getList $topology deviceGroup] {
	    set currentDgName [ixNet getAttribute $deviceGroup -name]
	    if {[regexp -nocase $deviceGroupName $currentDgName]} {
		puts "\nEnableDeviceGroup: $currentDgName"
		set multiValue [ixNet getAttribute $deviceGroup -enabled]
		ixNet setAttribute $multiValue/singleValue -value true
		ixNet commit
	    }
	}
    }
}

proc StopDeviceGroupNgpf { deviceGroupName } {
    foreach topology [ixNet getList [ixNet getRoot] topology] {
	foreach deviceGroup [ixNet getList $topology deviceGroup] {
	    set currentDgName [ixNet getAttribute $deviceGroup -name]
	    if {[regexp -nocase $deviceGroupName $currentDgName]} {
		puts "\nStopDeviceGroup: $currentDgName"
		ixNet exec stop $deviceGroup
		ixNet commit
	    }
	}
    }
}

proc StartDeviceGroupNgpf { deviceGroupName } {
    foreach topology [ixNet getList [ixNet getRoot] topology] {
	foreach deviceGroup [ixNet getList $topology deviceGroup] {
	    set currentDgName [ixNet getAttribute $deviceGroup -name]
	    if {[regexp -nocase $deviceGroupName $currentDgName]} {
		puts "\nStartDeviceGroup: $currentDgName"
		ixNet exec start $deviceGroup
		ixNet commit
	    }
	}
    }
}

proc RemoveDeviceGroupNgpf { deviceGroupName } {
    foreach topology [ixNet getList [ixNet getRoot] topology] {
	foreach deviceGroup [ixNet getList $topology deviceGroup] {
	    set currentDgName [ixNet getAttribute $deviceGroup -name]
	    if {[regexp -nocase $deviceGroupName $currentDgName]} {
		puts "\nRemoveDeviceGroup: $deviceGroup : $currentDgName"
		ixNet remove $deviceGroup
		ixNet commit
	    }
	}
    }
}

proc StartEthernetProtocolNgpf { ethernetGroupHandle } {
    puts "\nStartEthernetProtocol: $ethernetGroupHandle"
    ixNet exec start $ethernetGroupHandle
}

proc StopEthernetProtocolNgpf { ethernetGroupHandle } {
    puts "\nStopEthernetProtocolNgpf: $ethernetGroupHandle"
    ixNet exec stop $ethernetGroupHandle
}


proc StartIpv4ProtocolNgpf { ipv4Handle } {
    puts "\nStartIpv4ProtocolNgpf"
    ixNet exec start $ipv4Handle
}

proc StopIpv4ProtocolNgpf { ipv4Handle } {
    puts "\nStopIpv4ProtocolNgpf"
    ixNet exec stop $ipv4Handle
}

proc SaveConfigToFile { configName } {
    # To save the current IxNetwork configuration to a file in Linux.
    # Users need to include .ixncfg to the end of the name.
    
    puts "\nSaveConfigToFile: $configName"
    ixNet exec saveConfig [ixNet writeTo $configName -overwrite]
}

proc EnableDisablePimRouterIdNgpf { routerId action } {
    # NOTE: Don't get this API confused with PIM "Interface"
    #       This API enables/disables PIMv4 router ID.
    #
    # action = enable or disable
    
    if {$action == "enable"} {
	set action true
    } else {
	set action false
    }
    
    foreach topology [ixNet getList [ixNet getRoot] topology] {
	foreach deviceGroup [ixNet getList $topology deviceGroup] {
	    foreach pimRouter [ixNet getList $deviceGroup pimRouter] {
		set listOfRouterIds [ixNet getAttribute $pimRouter -localRouterId]
		
		if {[lsearch $listOfRouterIds $routerId] != -1} {
		    set routerIdIndex [expr [lsearch $listOfRouterIds $routerId] + 1]		    
		    set activeMultiValue [ixNet getAttribute $pimRouter -active]
		    
		    puts "\nEnableDisablePimRouterIdNgpf: Setting PIM routerID $routerId to $action"
		    if {[SetNgpfCounterMultiValue $activeMultiValue $routerIdIndex $action]} {
			return 1
		    }
		}
	    }
	}
    }
    return 0
}

proc EnableDisablePimInterfaceNgpf { routerId action } {
    # NOTE: Don't get this API confused with PIM "router ID"
    #       This API enables/disables PIMv4 interfaaces 
    #       based on the router ID address.
    #
    # action = enable or disable

    if {$action == "enable"} {
	set action true
    } else {
	set action false
    }

    foreach topology [ixNet getList [ixNet getRoot] topology] {
	foreach deviceGroup [ixNet getList $topology deviceGroup] {
	    foreach ethernet [ixNet getList $deviceGroup ethernet] {
		foreach ipv4 [ixNet getList $ethernet ipv4] {
		    foreach pimInterface [ixNet getList $ipv4 pimV4Interface] {
			set listOfRouterIds [ixNet getAttribute $pimInterface -localRouterId]
			if {[lsearch $listOfRouterIds $routerId] != -1} {
			    set routerIdIndex [expr [lsearch $listOfRouterIds $routerId] + 1]		    
			    set activeMultiValue [ixNet getAttribute $pimInterface -active]

			    puts "\nEnableDisablePimInterfaceNgpf: Setting PIM routerID $routerId to $action"
			    if {[SetNgpfCounterMultiValue $activeMultiValue $routerIdIndex $action]} {
				return 1
			    }
			}
		    }
		}
	    }
	}
    }
    return 0
}

proc ModifyIgmpHostVersionNgpf { deviceGroupName igmpVersion } {
    # Modifies all the igmp hosts in the given Device Group to 
    # the given $igmpVersion.
    #
    # deviceGroupName: The exact spelling of the Device Group (Case sensitive)
    # igmpVersion: version1, version2, or version3 (Case sensitive)

    foreach topology [ixNet getList [ixNet getRoot] topology] {
	foreach deviceGroup [ixNet getList $topology deviceGroup] {
	    set currentDgName [ixNet getAttribute $deviceGroup -name]

	    if {$deviceGroupName == $currentDgName} {
		foreach ethernet [ixNet getList $deviceGroup ethernet] {
		    foreach ipv4 [ixNet getList $ethernet ipv4] {
			foreach igmpHost [ixNet getList $ipv4 igmpHost] {
			    set multiValue [ixNet getAttribute $igmpHost -versionType]

			    puts "\nModifyIgmpHostVersionNgpf: $deviceGroup: igmpVersion:$igmpVersion"   
			    catch {ixNet setAttribute $multiValue/singleValue -value $igmpVersion} errMsg
			    if {$errMsg != "::ixNet::OK"} {
				puts "\nError ModifyIgmpHostVersionNgpf: $errMsg"
				return 1
			    }
			    ixNet commit
			}
		    }
		}
	    }
	}
    }
    return 0
}

proc EnablePktLossDuration {} {
    puts "\nEnablePktLossDuration"
    catch {ixNet setAttribute [ixNet getRoot]traffic/statistics/packetLossDuration -enabled true} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "\nError EnablePktLossDuration: $errMsg"
	return 1
    }
    ixNet commit
    return 0
}

proc SetCounterMultiValueNgpf { multiValue propertyIndex action } {
    # This API is for setting NGPF multivalue "property index" to true or false.
    # It checks to see if there is an overlay for the $propertyIndex.
    # If none, then create an overlay for the $propertyIndex.
    # If exists, verify if the overlay is for the $propertyIndex.
    # If it's not for the $propertyIndex, then create an overlay for it.

    # Example usage: EnableDisableSuppressArp calls this to 
    #                create, enable or disable a property index
    #                in which a property can have multiple indexes.

    set multiValueCurrentPattern [ixNet getAttribute $multiValue -pattern]
    if {$multiValueCurrentPattern != "counter"} {
	ixNet setAttribute $multiValue -pattern counter
	ixNet commit
	ixNet setAttribute $multiValue/counter -start $action
	ixNet commit
    }
    
    set overlayList [ixNet getList $multiValue overlay]
    
    set overlayDiscoveredFlag 0
    
    if {$overlayList != ""} {
	foreach overlay $overlayList {
	    set currentIndex [ixNet getAttribute $overlay -index]
	    
	    if {$currentIndex == $propertyIndex} {
		set overlayDiscoveredFlag 1
		puts "\nSetNgpfCounterMultiValue: Action = $action : propertyIndex = $propertyIndex"
		puts "\t$overlay"
		catch {ixNet setMultiAttr $overlay -value $action -valueStep $action -count 1 -index $propertyIndex} errMsg
		if {$errMsg != "::ixNet::OK"} {
		    puts "\nError SetNgpfCounterMultiValue: Set action to $action for overlay $currentOverlay: $errMsg"
		    return 1
		}
		ixNet commit
	    }
	}
	
	if {$overlayDiscoveredFlag == 0} {
	    # Getting here means no overlay found for the property Index.
	    # Have to create an overlay with the proper -index number.
	    puts "\nSetNgpfCounterMultiValue: No NGPF overlay for propertyIndex: $propertyIndex"
	    puts "Creating new overlay"
	    set currentOverlay [ixNet add $multiValue overlay]

	    puts "\nSetNgpfCounterMultiValue: Action = $action : propertyIndex = $propertyIndex"
	    puts "\t$overlay"
	    catch {ixNet setMultiAttr $currentOverlay -value $action -valueStep $action -count 1 -index $propertyIndex} errMsg
	    if {$errMsg != "::ixNet::OK"} {
		puts "\nError SetNgpfCounterMultiValue: Set action to $action for overlay $currentOverlay: $errMsg\n"
		return 1
	    }
	    
	    ixNet commit
	}
    }
    
    if {$overlayList == ""} {
	# Getting here means there are no overlays
	
	# Create Overlays with proper index number based on the portIndex
	# in $root/globals/topology/ipv4 -rowNames indexes
	puts "\nSetNgpfCounterMultiValue: No overlay exists"
	set currentOverlay [ixNet add $multiValue overlay]
	puts "Creating overlay: $currentOverlay"
	catch {ixNet setMultiAttr $currentOverlay -value $action -valueStep $action -count 1 -index $propertyIndex} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError SetNgpfCounterMultiValue: Set action to $action for overlay $currentOverlay: $errMsg\n"
	    return 1
	}
	ixNet commit
    }
    return 0
}

proc GetIgmpQuerierLearnedInfo { deviceGroup } {
    # ::ixNet::OBJ-/topology:1/deviceGroup:1

    # This API will group all common info by ID numbers like below:
    #7: Querier_Working_Version : v2
    #7: Elected_Querier_Address : 10.10.10.6
    #7: Group_Address : 229.0.0.1
    #7: Group_Timer_(sec) : 136
    #7: Filter_Mode : N/A
    #7: Compatibility_Mode : v2
    #7: Compatibility_Timer_(sec) : 0
    #7: Source_Address : removePacket[N/A]
    #7: Source_Timer_(sec) : 0
    #
    # On your script, you can do a foreach to view all :
    #    foreach {property value} $learnedInfo {}
    #
    # Or use for loop to get a set of IDs using regexp.

    regexp "(::ixNet::OBJ-)?(/topology:\[0-9]+/deviceGroup:\[0-9]+)" $deviceGroup - parsedDeviceGroup

    set id 0

    if {[info exists parsedDeviceGroup]} {
	# /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1
	foreach ethernet [ixNet getList ::ixNet::OBJ-$deviceGroup ethernet] {
	    foreach ipv4 [ixNet getList $ethernet ipv4] {
		foreach igmpQuerier [ixNet getList $ipv4 igmpQuerier] {
		    foreach learnedInfo [ixNet getList $igmpQuerier learnedInfo] {
			set currentValues [ixNet getAttribute $learnedInfo -values]
			set columnNames   [ixNet getAttribute $learnedInfo -columns]
			#puts "\ncurrentValues: $currentValues\n"
			#puts "\ncurrentNames: $columnNames\n"

			foreach valueList $currentValues {
			    incr id 
			    foreach name $columnNames value $valueList {
				set igmpLearnedInfo($id,[join $name _]) $value
				#puts "$id: [join $name _] : $value"
			    }
			}
		    }
		}
	    }
	}
    } else {
	puts "\nError GetIgmpQuerierLearnedInfo: No such device group exists: $deviceGroup\n"
	return 0
    }
    array get igmpLearnedInfo
}

proc ModifyMldGroupRanges { portList mldGroupRanges } {
    # portList = One port or a list of ports in format of: "1/2 1/3 1/5"
    # mldGroupCount = A list of group counts for each port: "100 200 300"

    # For example:
    #    If modifying one port, then: 1/1 200
    #    If modifying two ports, then: "1/1 1/2" "100 200"

    if {[llength $portList] != [llength $mldGroupRanges]} {
	puts "\nError: ModifyMldGroupRanges: The number of portList and mldGroupRanges are not the same"
	return 1
    }

    for {set index 0} {$index < [llength $portList]} {incr index} {
	set port [lindex $portList $index]
	set vport [GetVportMapping $port]

	foreach mldHostNumber [ixNet getList $vport/protocols/mld host] {
	    puts "\nindex=$index mldHostNumber= $mldHostNumber  $vport"
	    foreach mldHostGroupNumber [ixNet getList $mldHostNumber groupRange] {
		puts "\nModifyMldGroupRanges: $port mldGroupRanges=[lindex $mldGroupRanges $index]"
		ixNet setAttribute $mldHostGroupNumber -groupCount [lindex $mldGroupRanges $index]
		ixNet commit		
	    }
	}
    }
    return 0
}

proc ApplyChangesOnTheFly {{timeout 90}} {
    set count 0
    set status [ixNet getAttr /globals/topology -applyOnTheFlyState]
    puts "Aplying changes on the fly -> $status"
    while {$status == "notAllowed"} {
        puts "      $count: /globals/topology -applyOnTheFlyState --> $status"
        set status [ixNet getAttr /globals/topology -applyOnTheFlyState]
        after 1000
        incr count
        if {$count > $timeout } {
            error "Waited for $count sec, '/globals/topology -applyOnTheFlyState' still not in 'allowed' status... "
        }
    }

    set status [ixNet getAttr /globals/topology -applyOnTheFlyState]
    if {$status == "allowed"} {
        ixNet exec applyOnTheFly /globals/topology
        return 0
    } elseif {$status == "nothingToApply"} {
        ixNet exec applyOnTheFly /globals/topology
        return 0
    } else {
        error "Status unknown '$status'"
	return 1
    }
}

proc SendPing { port srcIp destIp } {
    # port format = 1/3.  Not 1/1/3
    # srcIp = The srcIp address of the port to ping from.
    # destIp = The destIp address to ping to.
    #
    # Passed (return 0) = ::ixNet::OK-{kString,Response received from 1.1.1.3. Sequence Number 3}
    # Failed (return 1) = ::ixNet::OK-{kString,Ping request to 1.1.1.6 failed: Ping request timed out}

    # Verify for proper port format. If incorrect, fix it.
    if {[regexp "\[0-9]+/(\[0-9]+/\[0-9]+)" $port - port2]} {
	set port $port2
    }

    set vport [GetVportMapping $port]

    foreach vportInterface [ixNet getList $vport interface] {
	set currentIpv4 [ixNet getAttribute $vportInterface/ipv4 -ip]
	if {$currentIpv4 == $srcIp} {
	    set interfaceObj $vportInterface
	}
    }

    set result [ixNet exec sendPing $interfaceObj $destIp]

    if {[regexp "Ping request timed out" $result]} {
	return 1
    } else {
	return 0
    }
}

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

proc CreateTopology { args } {
    # Example: set topology1Obj [CreateTopologyNgpf -name Topo-1 -portList [list "$ixChassisIp 1 1"]]

    set paramList {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -name {
		set name [lindex $args [expr $argIndex + 1]]
		append paramList " -name $name"
		incr argIndex 2
	    }
	    -portList {
		set portList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "Connect: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    if {[info exists portList] == 0} {
	puts "\nError: CreateToplogy: Requires portList"
	return 1
    }

    puts "\nCreate Topology: Getting vport for: $portList"
    set vportList [GetVportMappingToPhyPort $portList]
    puts "Create Topology: Vport: $vportList"
    append paramList " -vports [list $vportList]"

    puts "\nCreateTopology: $paramList"
    set topologyObj [ixNet add [ixNet getRoot] "topology"]

    if {[catch {eval ixNet setMultiAttribute $topologyObj $paramList} errMsg]} {
	puts "\nConnect failed $paramList"
	return 1
    }
    ixNet commit
    return [lindex [ixNet remapIds $topologyObj] 0]
}

proc CreateDeviceGroup { args } {

    set paramList {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -topologyObj {
		set topologyObj [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -name {
		set name [lindex $args [expr $argIndex + 1]]
		append paramList " -name $name"
		incr argIndex 2
	    }
	    -multiplier {
		set multiplier [lindex $args [expr $argIndex + 1]]
		append paramList " -multiplier $multiplier"
		incr argIndex 2
	    }
	    default {
		puts "Connect: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    puts "\nCreateDeviceGroupNgpf: $paramList"
    set deviceGroupObj [ixNet add $topologyObj "deviceGroup"]
    if {[catch {eval ixNet setMultiAttribute $deviceGroupObj $paramList} errMsg]} {
	puts "\nCreateDeviceGroup failed: $paramList"
	return 1
    }
    ixNet commit
    return [lindex [ixNet remapIds $deviceGroupObj] 0]
}

proc CreateEthernetNgpf {args} {
    set direction increment
    set step 00:00:00:00:00:00
    set enableVlan false

    set paramList {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -deviceGroupObj {
		set deviceGroupObj [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -name {
		set name [lindex $args [expr $argIndex + 1]]
		append paramList " -name $name"
		incr argIndex 2
	    }
	    -macAddress {
		set macAddress [lindex $args [expr $argIndex + 1]]
		append paramList " -start $macAddress"
		incr argIndex 2
	    }
	    -direction {
		set direction [lindex $args [expr $argIndex + 1]]
		append paramList " -direction $direction"
		incr argIndex 2
	    }
	    -step {
		set step [lindex $args [expr $argIndex + 1]]
		append paramList " -step $step"
		incr argIndex 2
	    }
	    -macAddressPortStep {
		set macAddressPortStep [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -enableVlan {
		set enableVlan [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "Connect: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    puts "\nCreateEthernetNgpf: Adding new Ethernet stack"
    set ethernetObj [ixNet add $deviceGroupObj ethernet]
    ixNet commit

    set ethernetMultivalue [ixNet getAttribute $ethernetObj -mac]
    puts "\t$paramList"
    if {[catch {eval ixNet setMultiAttribute $ethernetMultivalue/counter  $paramList} errMsg]} {
	puts "\nCreateEthernetNgpf failed: $paramList"
	return 1
    }
    ixNet commit

    set ethernetObj [lindex [ixNet remapIds $ethernetObj] 0]

    if {[info exists macAddressPortStep]} {
	ixNet setAttribute $ethernetMultivalue/nest:1 -step $macAddressPortStep
	ixNet commit
    }
    
    if {$enableVlan == "true"} {
	puts "\nEnabling vlan for: $ethernetObj"
	set enableVlanMultivalue [ixNet getAttribute $ethernetObj -enableVlans]
	if {[catch {ixNet setAttribute $enableVlanMultivalue/singleValue -value true} errMsg]} {
	    puts "\nEnabling vlan failed for $ethernetObj"
	    return 1
	}
	ixNet commit
    }

    #return [lindex [ixNet remapIds $ethernetObj] 0]
    return $ethernetObj
}

proc ConfigVlanIdNgpf {args} {
    set direction increment
    set step 0

    set paramList {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -ethernetObj {
		set ethernetObj [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -start {
		set vlanId [lindex $args [expr $argIndex + 1]]
		append paramList " -start $vlanId"
		incr argIndex 2
	    }
	    -step {
		set step [lindex $args [expr $argIndex + 1]]
		append paramList " -step $step"
		incr argIndex 2
	    }
	    -direction {
		set direction [lindex $args [expr $argIndex + 1]]
		append paramList " -direction $direction"
		incr argIndex 2
	    }
	    default {
		puts "Connect: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    puts "\nConfigVlanIdNgpf: start:$vlanId step:$step direction:$direction"
    set vlanMultivalue [ixNet getAttribute $ethernetObj/vlan:1 -vlanId]
    if {[catch {eval ixNet setMultiAttribute $vlanMultivalue/counter $paramList} errMsg]} {
	puts "\nConfigVlanIdNgpf failed: start:$vlanId step:$step direction:$direction"
	return 1
    }
    ixNet commit
} 

proc CreateIpv4Ngpf {args} {
    set direction increment
    set step 0.0.0.0

    set paramList {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -ethernetObj {
		set ethernetObj [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -name {
		set name [lindex $args [expr $argIndex + 1]]
		append paramList " -name $name"
		incr argIndex 2
	    }
	    -ipAddress  {
		set ipAddress [lindex $args [expr $argIndex + 1]]
		append paramList " -start $ipAddress"
		incr argIndex 2
	    }
	    -direction {
		set direction [lindex $args [expr $argIndex + 1]]
		append paramList " -direction $direction"
		incr argIndex 2
	    }
	    -step {
 		set step [lindex $args [expr $argIndex + 1]]
		append paramList " -step $step"
		incr argIndex 2
	    }
	    -ipv4PortStep {
 		set ipv4PortStep [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "Connect: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    puts "\nCreateIpv4Ngpf: Adding new IPv4 stack"
    set ipv4Obj [ixNet add $ethernetObj ipv4]
    ixNet commit

    set ipv4Multivalue [ixNet getAttribute $ipv4Obj -address]

    puts "\t$paramList"
    if {[catch {eval ixNet setMultiAttribute $ipv4Multivalue/counter  $paramList} errMsg]} {
	puts "\nCreateIpv4Ngpf failed: $paramList"
	return 1
    }
    ixNet commit

    if {[info exists ipv4PortStep]} {
	puts "\nConfiguring ipv4PortStep: $ipv4Multivalue/nest:1 $ipv4PortStep"
	ixNet setAttribute $ipv4Multivalue/nest:1 -step $ipv4PortStep
	ixNet commit
    }

    return [lindex [ixNet remapIds $ipv4Obj] 0]
}

proc ConfigIpv4GatewayIpNgpf {args} {
    set direction increment
    set step 0.0.0.0

    set paramList {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -ipv4Obj {
		set ipv4Obj [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -gatewayIp  {
		set gatewayIp [lindex $args [expr $argIndex + 1]]
		append paramList " -start $gatewayIp"
		incr argIndex 2
	    }
	    -direction {
		set direction [lindex $args [expr $argIndex + 1]]
		append paramList " -direction $direction"
		incr argIndex 2
	    }
	    -step {
		set step [lindex $args [expr $argIndex + 1]]
		append paramList " -step $step"
		incr argIndex 2
	    }
	    -ipv4GatewayPortStep {
		set ipv4GatewayPortStep [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "Connect: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    set gatewayMultivalue [ixNet getAttribute $ipv4Obj -gatewayIp]

    puts "\t$paramList"
    if {[catch {eval ixNet setMultiAttribute $gatewayMultivalue/counter $paramList} errMsg]} {
	puts "\nConfigGatewayIpNgpf failed: $paramList"
	return 1
    }
    ixNet commit

    if {[info exists ipv4GatewayPortStep]} {
	puts "\nConfiguring ConfigIpv4GatewayIpNgpf port step: $gatewayMultivalue/nest:1 $ipv4GatewayPortStep"
	ixNet setAttribute $gatewayMultivalue/nest:1 -step $ipv4GatewayPortStep
	ixNet commit
    }
}

proc ConfigBgpNgpf {args} {
    set direction increment
    set step 0.0.0.0

    set paramList {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -ipv4Obj {
		set ipv4Obj [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -dutIp  {
		set dutIp [lindex $args [expr $argIndex + 1]]
		append paramList " -start $dutIp"
		incr argIndex 2
	    }
	    -direction {
		set direction [lindex $args [expr $argIndex + 1]]
		append paramList " -direction $direction"
		incr argIndex 2
	    }
	    -step {
		set step [lindex $args [expr $argIndex + 1]]
		append paramList " -step $step"
		incr argIndex 2
	    }
	    default {
		puts "Connect: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    puts "\nCreateBgpNgpf: Adding new BGP V4 stack"
    set bgpObj [ixNet add $ipv4Obj bgpIpv4Peer]
    ixNet commit

    set bgpMultivalue [ixNet getAttribute $bgpObj -dutIp]

    puts "\t$paramList"
    if {[catch {eval ixNet setMultiAttribute $bgpMultivalue/counter $paramList} errMsg]} {
	puts "\nConfigBgpNgpf failed: $paramList"
	return 1
    }
    ixNet commit
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

proc ConfigIpv4GatewayIpNgpf_backup { ipv4GatwayIpObj start {step 0.0.0.0} {direction increment} } {
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

proc RebootCardId { cardId } {
    ixNet execute hwRebootCardByIDs $cardId
}

proc CreateTrafficItem {args} {
    # raw, ipv4, ipv6, ethernetVlan

    set paramList {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	puts "currentArg: $currentArg"
	switch -exact -- $currentArg {
	    -name {
		set name [lindex $args [expr $argIndex + 1]]
		append paramList " -name $name"
		incr argIndex 2
	    }
	    -trafficType {
		set trafficType [lindex $args [expr $argIndex + 1]]
		append paramList " -trafficType $trafficType"
		incr argIndex 2
	    }
	    -trafficItemType {
		set trafficItemType [lindex $args [expr $argIndex + 1]]
		append paramList " -trafficItemType $trafficItemType"
		incr argIndex 2
	    }
	    # true|false
	    -biDirection {
		set biDirection [lindex $args [expr $argIndex + 1]]
		append paramList " -biDirectional $biDirection"
		incr argIndex 2
	    }
	    -trackBy {
		set trackBy [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -srcEndpoint {
		set srcEndpoint [lindex $args [expr $argIndex + 1]]
		append paramList " -srcEndpoint $srcEndpoint"
		incr argIndex 2
	    }	    
	    -dstEndpoint {
		set dstEndpoint [lindex $args [expr $argIndex + 1]]
		append paramList " -dstEndpoint $dstEndpoint"
		incr argIndex 2
	    }	    
	    default {
		puts "Connect: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    puts "\nCreateTrafficItem: $paramList"
    set trafficItemObj [ixNet add [ixNet getRoot]/traffic trafficItem]
    ixNet commit
    if {[catch {eval ixNet setMultiAttribute $trafficItemObj $paramList} errMsg]} {
	puts "Error: CreateTrafficItem: $errMsg"
	return 1
    }
    ixNet commit

    # Must set trafficType after creating a new Traffic Item or else it will default to raw.
    ixNet setAttribute $trafficItemObj -trafficType $trafficType
    ixNet commit

    set trafficItemObj [lindex [ixNet remapIds $trafficItemObj] 0]
    if {[info exists trackBy]} {
	puts "Configuring tracking: $trackBy"
	if {[catch {ixNet setMultiAttribute $trafficItemObj/tracking -trackBy $trackBy} errMsg]} {
	    puts "\nError CreateTrafficItem: $errMsg"
	}
	ixNet commit
    }
    return $trafficItemObj
}

proc CreateEndpoints {args} {
    set paramList {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -trafficItemObj {
		set trafficItemObj [lindex $args [expr $argIndex + 1]]
		#append paramList " -trafficItemObj $trafficItemObj"
		incr argIndex 2
	    }
	    -name {
		set name [lindex $args [expr $argIndex + 1]]
		append paramList " -name $name"
		incr argIndex 2
	    }
	    -srcEndpoint {
		set srcEndpoint [lindex $args [expr $argIndex + 1]]
		append paramList " -sources $srcEndpoint"
		incr argIndex 2
	    }	    
	    -dstEndpoint {
		set dstEndpoint [lindex $args [expr $argIndex + 1]]
		append paramList " -destinations $dstEndpoint"
		incr argIndex 2
	    }	    
	    default {
		puts "Connect: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    if {[catch {set endpointSetObj [ixNet add $trafficItemObj endpointSet]} errMsg]} {
	puts "Error: Creating new endpoints"
	return 1
    }
    ixNet commit
    puts "CreateEndpoints: $paramList"
    if {[catch {eval ixNet setMultiAttribute $endpointSetObj $paramList} errMsg]} {
	puts "\nError: CreateEndpoints: $errMsg"
	return 1
    }
    ixNet commit
    set endpointSetObj [lindex [ixNet remapIds $endpointSetObj] 0]
}

proc ConfigTrafficTransmissionControl {args} {
    set paramList {}
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -configElementObj {
		set configElementObj [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -type {
		# continuous, fixedFrameCount, fixedDuration, fixedIterationCount, custom, auto
		set type [lindex $args [expr $argIndex + 1]]
		append paramList " -type $type"
		incr argIndex 2
	    }
	    -frameCount {
		set frameCount [lindex $args [expr $argIndex + 1]]
		append paramList " -frameCount $frameCount"
		incr argIndex 2
	    }
	    default {
		puts "Connect: No such parameter: $currentArg"
		return 1
	    }
	}
    }
    
    puts "\nConfigTrafficTransmissionControl: $paramList"
    if {[catch {eval ixNet setMultiAttribute $configElementObj/transmissionControl $paramList} errMsg]} {
	puts "Error: ConfigTrafficTransmissionControl: $errMsg"
	return 1
    }
    ixNet commit
}

proc addTrafficItemPacketStack {configElementObj protocolStackNameToAdd stackNumber action} {
    # Example:
    #    addTrafficItemPacketStack $configElementObj udp 3 append
    # 
    # Parameters
    #    configElementObj: The configElementObj object handle
    #    protocolStackNameToAdd: mpls, ipv4, etc.
    #    stackNumber: The stack number to insert before or append after.
    #    action: append or insert.
    #            append goes after $stackNumber, insert goes before $stackNumber
    
    set index [lsearch -regexp [ixNet getList [ixNet getRoot]/traffic protocolTemplate] $protocolStackNameToAdd]
    set stack [lindex [ixNet getList [ixNet getRoot]/traffic protocolTemplate] $index]
    
    puts "\tAdding stack: $stack"
    set addToStackLevel [lindex [ixNet getList $configElementObj stack] $stackNumber]
    ixNet exec append $addToStackLevel $stack
    ixNet commit
}

proc configPacketHeaderField {stackObj args} {
    # Example:
    #ixNet setMultiAttribute $configElementObj/stack:\"mpls-2\"/field:\"mpls.label.value-1\" \
    #	-valueType increment \
    #	-startValue 1001 \
    #	-stepValue 1 \
    #	-countValue 1

    puts "\nconfigPacketHeaderField: $stackObj\n\t$args"
    eval ixNet setMultiAttribute $stackObj $args
    ixNet commit
}
