proc ConnectToIxiaHlt { connectParams } {
    # How to use this from a script:
    #    set connect(-reset) 1
    #    set connect(-device) $ixiaChassisIp
    #    set connect(-port_list) $portList
    #    set connect(-ixnetwork_tcl_server) $ixNetworkTclServerIp
    #    set connect(-tcl_server) $ixiaChassisIp
    #    set connect(-username) $userName
    #    set connectStatus [ConnectToIxiaHlt ::connect]

    upvar $connectParams params
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "ConnectToIxiaHlt: Please wait 40 seconds ..."
    set connectStatus [eval ::ixia::connect $paramList]

    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "\nEror ConnectToIxia: $connectStatus\n"
	return 1
    } else {
	return $connectStatus
    }
}

proc ResumeHlt { connectParams } {
    # Usage:
    #   set connect(-tcl_server) "10.219.117.101"'
    #   set connect(-ixnetwork_tcl_server) "10.219.117.103"'
    #   set connect(-username) "hgee"'
    #   set connect(-session_resume_keys) 1'
    #   Resume ::connect

    upvar $connectParams params

    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "ConnectToIxiaHlt: Please wait 40 seconds ..."
    set status [eval ::ixia::connect $paramList]

    #set status [::ixia::connect \
    #		    -ixnetwork_tcl_server $ixNetworkTclServerIp \
    #		    -tcl_server $ixiaChassisIp \
    #		    -username $userName \
    #		    -session_resume_keys 1 \
    #		    ]
    return $status
}

proc LoadConfigFile { {type useConfigFilePorts} } {
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
	return 1
    } else {
	puts "Successfully connected to IxNetwork Tcl server"
    }
    
    puts "\n[KeylPrint connectStatus]\n"
    return $connectStatus
}

proc GetVportConnectedToPort { vport } {
    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
    set connectedTo [ixNet getAttribute $vport -connectedTo]
    set connectedTo [lrange [split $connectedTo /] 3 4]
    set card [lindex [split [lindex $connectedTo 0] :] end]
    set port [lindex [split [lindex $connectedTo 1] :] end]
    return $card/$port    
}

proc GetVportMapping { Port } {
    # Search all vport for the port number.
    # Port format = 1/1.  Not 1/1/1.

    regexp "\[0-9]+/(\[0-9]+/\[0-9]+)" $Port - Port
 
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

proc PortConfigProtocolIntHlt { port portConfigParams } {
    # Call this API if you are configuring protocols on the port.
    # You could also use this for scaling, but using this API
    # will take up a lot of resource.
    # For scaling, it is better to use PortConfigStaticIp.
    
    # How to use this from a script:
    #    set port 1/1/3
    #    set portConfig($port1,-mode) config
    #    set portConfig($port1,-intf_ip_addr) 1.1.1.1
    #    set portConfig($port1,-connected_count) 1
    #    set portConfig($port1,-gateway) 1.1.1.2
    #    set portConfig($port1,-gateway_step) 0.0.0.0
    #    set portConfig($port1,-netmask) 255.255.255.0
    #    set portConfig($port1,-src_mac_addr) "0001.0101.0001"
    #    set portConfig($port1,-src_mac_addr_step) 0000.0000.0001
    #    set portConfig($port1,-l23_config_type) static_endpoint
    #    set portConfig($port1,-mtu) 1500
    #    set portConfig($port1,-vlan_id) 300
    #    set portConfig($port1,-vlan_id_count) 1
    #    set portConfig($port1,-vlan) 0
    #    set portConfig($port1,-vlan_id_step) 1
    #    set endpoint($port) [PortConfigProtocolIntHlt ::portConfig]

    upvar $portConfigParams params
    
    puts "\nPortConfigProtocolIntHlt: $port"
    foreach {properties values} [array get params $port,*] {
	set property [lindex [split $properties ,] end]
	puts "$property: $values"
	append paramList "$property $values "
    }

    set interfaceConfigStatus [eval ::ixia::interface_config $paramList]

    if {[keylget interfaceConfigStatus status] != $::SUCCESS} {
	puts "\nError PortConfigProtocolInt:\n$interfaceConfigStatus\n"
	return 1
    }

    # interface object = ::ixNet::OBJ-/vport:1/interface:1
    set interfaceHandle [keylget interfaceConfigStatus interface_handle]

    return $interfaceHandle
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

proc ModifyProtocolInterfaces { args } {
    # This API allows you to modify any or all configured Protocol Interfaces.
    # It is mandatory that you include the -port parameter with the port value
    # format of 1/1/1.
    #
    # This API requires calling GetProtocolIntObjects.
    # 
    # Usage:
    #   
    #    Two ways to use this.  
    # 
    #    1> Enter a starting address for any of the followings:
    #           -ippv4, -gatewayIpv4, -mac ...
    # 
    #    2> Provide a custom list: -ipv4List, -ipv4GatewayList, -vlanIdList, -macList ... 
    #
    #       -ipv4              = Single value
    #       -ipv4Step          = Ex: 0.0.0.1 = increment the 4th octect by 1 step
    #       -                  = Ex: 0.0.3.0 = increment the 3rd octect by 3 steps
    #       -ipv4List          = A list of list  with interfaceNumber|description and IP.
    #                            Ex: {{1 10.10.10.1} {"descName" 10.10.10.2}}
    #       -gatewayIpv4       = Single value
    #       -gatewayIpv4Step   = Same as ipv4Step
    #       -ipv4GatewayList   = Same as ipv4List
    #       -mac               = Single value
    #       -macStep           = 00:00:00:00:00:01 = increment the 6th byte by 1 step
    #       -macStep           = 00:00:00:02:00:00 = increment the 4th byte by 2 steps
    #       -macList           = Same method as ipv4List
    #       -ipv4MaskWidth     = In digits: 24.  Fixed value for all interfaces.
    #       -ipv4MaskWidthList = A list of list with interfaceNumber|description and the maskWidth.
    #                            Ex:  -ipv4MaskWidthList {{1 24} {2 23} {"descName" 22}}
    #       -name              = Provide a list of list with interface number and description.
    #                            Ex: -name {{1 "int1_description"} {2 "int2_descriptION"} {5 "int5_description}}
    #       -enable            = "all" or a list of interface numbers to enable.
    #                            Ex: -enable all
    #                            Ex: -enable {1 3 5}  This will enable only interface 1, 3, and 5
    #       -disable           = Same as enable
    #       -vlanId            = The vlan ID for all interfaces.
    #                          = Ex: For QinQ, -vlanId {88,103}.
    #       -vlanIdList        = A list of list with interfaceNumber|description and vlanId.
    #                            Ex: -vlanIdList {{1 103} {"descName" 110}}
    #                            Ex: QinQ: -vlanidList {{1 78,103} {"desc name" 78,103}}.
    #                                1 and 3 are interface numbers followed by outer,inner vlanId.
    #       -vlanPriority      = The vlan priority for all interfaces.
    #                          = Ex: QinQ: Same as vlanId
    #       -vlanPriorityList  = A list of list with interface number and vlan priority number.
    #                          = Ex: QinQ: Same as vlanIdList
    #       -vlanEnable        = True or False, for all interfaces.
    #       -vlanEnableList    = A list of interface numbers to enable.
    #                            Ex: -vlanEnableList {1 3 5 7}
    #       -vlanDisableList   = Same as above.
    #       -vlanTpId          = 0x8100 for all interfaces.
    #       -vlanCount         = The number of vlan to create for each interface.
    #       -delete            = "all" or a list of interface numbers to delete.
    #                            Ex: -delete all
    #                            Ex: -delete {1 2 5} will delete only interface 1, 2 and 5
    
    if {[lsearch $args -port] == -1} {
	puts "\nModifyProtocolInterfaces Error: Must include -port"
	return 1
    }

    # TODO: Handle interface description for a list of names also:
    # -delete {11 12 13 14 15 16 17 18 19 20 21}

    # This Proc is only used internally to avoid rewriting same codes
    proc lsearchList { interfaceObj param theList currentInterfaceNumber} {
	# obj = interface or interface/vlan ...
	# param = -vlanId, macAddress, etc
	# theList = The list to search
	# currentInterfaceNumber = The for loop current interface number
	# {1 1.1.1.1} and/or {"interface name" 1.1.1.1}

	# If the user provided list is not an interface number, then it's a name.	
	# Convert the interface name to interface number.
	set theList [eval list $theList]
	set theList2 {}

	foreach item $theList {
	    set interfaceNameOrNumber [lindex $item 0]
	    set theValue [lindex $item 1]
	    if {[regexp "^\[0-9]+$" $interfaceNameOrNumber] == 0} {
		# The user provided a name.  Get the interface number.
		# ::ixNet::OBJ-/vport:1/interface:1
		foreach eachInterface $::interfaceList {
		    set currentIntName [ixNet getAttribute $eachInterface -description]
		    if {[regexp -nocase $interfaceNameOrNumber $currentIntName]} {
			set convertNameToIntNumber [lindex [split $eachInterface ":"] end]
			lappend theList2 "$convertNameToIntNumber $theValue"
		    } else {
			lappend theList2 "$interfaceNameOrNumber $theValue"
		    }
		}
	    }
	}

	set currentValue [lsearch -index 0 -all -inline $theList2 $currentInterfaceNumber]
	if {$currentValue != ""} {
	    set value [lindex [lindex $currentValue 0] 1]
	    puts "\t$param $value"
	    ixNet setAttribute $interfaceObj $param $value
	}

	if 0 {
	    set currentIndex [lsearch -index 0 -all -inline $theList $currentInterfaceNumber]
	    if {$currentIndex != ""} {
		set currentIndex [lindex [lindex $currentIndex 0] 1]
		puts "\t$param $currentIndex"
		ixNet setAttribute $interfaceObj $param $currentIndex
	    }
	}
    }

    set ipv4Step 0
    set maskWidth 24
    set gatewayIpv4Step 0
    set macStep 00:00:00:00:00:00
    
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg { 
	    -port {
		set port [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ipv4 {
		set startingIpv4 [lindex $args [expr $argIndex + 1]]
		incr argIndex 2V
	    }
	    -ipv4MaskWidth {
		set ipv4MaskWidth [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ipv4Step {
		set ipv4Step [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -gatewayIpv4 {
		set startingGatewayIpv4 [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -gatewayIpv4Step {
		set gatewayIpv4Step [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -name {
		# -name {{interfaceNumber1 "the name1"} {interfaceNumber2 "the name2"}}
		set name [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -enable {
		# -enable all or {intNumbers in a list}
		set enableList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -disable {
		# -disable all or  {intNumbers in a list}
		set disableList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ipv4List {
		# -ipv4List {{1 $ip} {2 $ip}}
		set ipv4List [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ipv4GatewayList {
		# -ipv4GatewayList {{1 $gatewayIp} {2 $gatewayIp}}
		set ipv4GatewayList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ipv4MaskWidthList {
		# -ipv4MaskWidthList {{1 $maskWidth} {2 $maskWidth}}
		set ipv4MaskWidthList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -mac {
		set mac [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -macStep {
		set macStep [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -macList {
		set macList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -mtu {
		set mtu [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -vlanId {
		set vlanId [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -vlanPriority {
		set vlanPriority [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -vlanEnable {
		set vlanEnable [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -vlanTpId {
		set vlanTpId [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -vlanCount {
		set vlanCount [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -vlanIdList {
		set vlanIdList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -vlanPriorityList {
		set vlanPriorityList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -vlanEnableList {
		set vlanEnableList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -vlanDisableList {
		set vlanDisableList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -delete {
		set delete [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "\nModifyProtocolInterface: No such parameter: $currentArg"
		return 1
	    }
	}    
    }

    global interfaceList
    set interfaceList [GetProtocolIntObjects -port $port] 
    
    if {[info exists mac]} {
	# Default the incr steps to 0 in case regexp didn't find any match
	set incr1stIpOctect 0
	set incr2ndIpOctect 0
	set incr3rdIpOctect 0
	set incr4thIpOctect 0
	
	regexp "(\[0-9a-fA-F]+):(\[0-9a-fA-F]+):(\[0-9a-fA-F]+):(\[0-9a-fA-F]+):(\[0-9a-fA-F]+):(\[0-9a-fA-F]+)" $macStep - \
	    macStepByte1 macStepByte2 macStepByte3 macStepByte4 macStepByte5 macStepByte6

	scan $macStepByte1 %x incr1stMac
	scan $macStepByte2 %x incr2ndMac   
	scan $macStepByte3 %x incr3rdMac 
	scan $macStepByte4 %x incr4thMac 
	scan $macStepByte5 %x incr5thMac 
	scan $macStepByte6 %x incr6thMac

	set macByte1 [lindex [split $mac :] 0]
	set macByte2 [lindex [split $mac :] 1]
	set macByte3 [lindex [split $mac :] 2]
	set macByte4 [lindex [split $mac :] 3]
	set macByte5 [lindex [split $mac :] 4]
	set macByte6 [lindex [split $mac :] 5]
	set currentMac $mac
    }

    if {$ipv4Step != "0"} {
	# Default the incr steps to 0 in case regexp didn't find any match
	set incr1stIpOctect 0
	set incr2ndIpOctect 0
	set incr3rdIpOctect 0
	set incr4thIpOctect 0
	
	regexp "(\[0-9]+)\.(\[0-9]+)\.(\[0-9]+)\.(\[0-9]+)" $ipv4Step - \
	    incr1stIpOctect incr2ndIpOctect incr3rdIpOctect incr4thIpOctect

	set byte1 [lindex [split $startingIpv4 .] 0]
	set byte2 [lindex [split $startingIpv4 .] 1]
	set byte3 [lindex [split $startingIpv4 .] 2]
	set byte4 [lindex [split $startingIpv4 .] 3]
	set currentIpv4 $startingIpv4
    }

    if {$gatewayIpv4Step != "0"} {
	# Default the incr steps to 0 in case regexp didn't find any match
	set incr1stGatewayOctect 0
	set incr2ndGatewayOctect 0
	set incr3rdGatewayOctect 0
	set incr4thGatewayOctect 0
	
	regexp "(\[0-9]+)\.(\[0-9]+)\.(\[0-9]+)\.(\[0-9]+)" $gatewayIpv4Step - \
	    incr1stGatewayOctect incr2ndGatewayOctect incr3rdGatewayOctect incr4thGatewayOctect
	
	set gatewayByte1 [lindex [split $startingGatewayIpv4 .] 0]
	set gatewayByte2 [lindex [split $startingGatewayIpv4 .] 1]
	set gatewayByte3 [lindex [split $startingGatewayIpv4 .] 2]
	set gatewayByte4 [lindex [split $startingGatewayIpv4 .] 3]
	set currentGatewayIpv4 $startingGatewayIpv4
    }

    set oneTimeOnly 0
    set currentInterfaceNumber 0
    foreach interface $interfaceList {
	puts "\nModifyProtocolInterface: $interface"
	incr currentInterfaceNumber

	if {[info exists vlanId]} {
	    puts "\t-vlanId $vlanId"
	    ixNet setAttribute $interface/vlan -vlanId $vlanId
	}
	if {[info exists vlanPriority]} {
	    puts "\t-vlanPriority $vlanPriority"
	    ixNet setAttribute $interface/vlan -vlanPriority $vlanPriority
	}
	if {[info exists vlanEnable]} {
	    puts "\t-vlanEnable $vlanEnable"
	    ixNet setAttribute $interface/vlan -vlanEnable $vlanEnable
	}
	if {[info exists vlanTpId]} {
	    puts "\t-tpid $vlanTpId"
	    ixNet setAttribute $interface/vlan -tpid $vlanTpId
	}
	if {[info exists vlanCount]} {
	    puts "\t-vlanCount $vlanCount"
	    ixNet setAttribute $interface/vlan -vlanCount $vlanCount
	}
	if {[info exists vlanIdList]} {
	    lsearchList $interface/vlan -vlanId $vlanIdList $currentInterfaceNumber
	}
	if {[info exists vlanPriorityList]} {
	    lsearchList $interface/vlan -vlanPriority $vlanPriorityList $currentInterfaceNumber
	}
	if {[info exists vlanEnableList]} {
	    if {[regexp "A|all" $vlanEnableList]} {
		puts "\tvlan: -enable True"
		ixNet setAttribute $interface/vlan -vlanEnable True
	    } else {
		if {[lsearch $vlanEnableList $currentInterfaceNumber] != -1} {
		    puts "\tvlan: -enable True"
		    ixNet setAttribute $interface/vlan -vlanEnable True 
		}
	    }
	}

	if {[info exists vlanDisableList]} {
	    if {[regexp "A|all" $vlanDisableList]} {
		puts "\tvlan: -enable False"
		ixNet setAttribute $interface/vlan -vlanEnable False
	    } else {
		if {[lsearch $vlanDisableList $currentInterfaceNumber] != -1} {
		    puts "\tvlan: -enable False"
		    ixNet setAttribute $interface/vlan -vlanEnable False 
		}
	    }
	}

	if {[info exists mac]} {
	    # Generate Mac address
	    if {$oneTimeOnly == 1} {
		if {$incr6thMac > 0 && $macByte6 >= "254"} {
		    set macByte6 1
		    incr macByte5
		}
		if {$incr6thMac > 0 && $macByte6 < "254"} {
		    incr macByte6 $incr6thMac
		}

		if {$incr5thMac > 0 && $macByte5 >= "254"} {
		    set macByte5 1
		    incr macByte4
		}
		if {$incr5thMac > 0 && $macByte5 < "254"} {
		    incr macByte5 $incr5thMac
		}
 
		if {$incr4thMac > 0 && $macByte4 >= "254"} {
		    set macByte4 1
		    incr macByte3
		}
		if {$incr4thMac > 0 && $macByte4 < "254"} {
		    incr macByte4 $incr4thMac
		}

		if {$incr3rdMac > 0 && $macByte3 >= "254"} {
		    set macByte3 1
		    incr macByte2
		}
		if {$incr3rdMac > 0 && $macByte3 < "254"} {
		    incr macByte3 $incr3rdMac
		}

		if {$incr2ndMac > 0 && $macByte2 >= "254"} {
		    set macByte2 1
		    incr macByte1
		}
		if {$incr2ndMac > 0 && $macByte2 < "254"} {
		    incr macByte2 $incr2ndMac
		}
	    }
	    set currentMac [format %2.2x $macByte1]:[format %2.2x $macByte2]:[format %2.2x $macByte3]:[format %2.2x $macByte4]:[format %2.2x $macByte5]:[format %2.2x $macByte6]
	    puts "\t-mac $currentMac"
	    ixNet setAttribute $interface/ethernet -macAddress $currentMac
	}

	if {[info exists startingIpv4]} {
	    # Generate IP address
	    if {$oneTimeOnly == 1} {
		if {$incr4thIpOctect > 0 && $byte4 >= "254"} {
		    set byte4 1
		    incr byte3
		}
		if {$incr4thIpOctect > 0 && $byte4 < "254"} {
		    incr byte4 $incr4thIpOctect
		}
		
		if {$incr3rdIpOctect > 0 && $byte3 >= "254"} {
		    set byte3 1
		    incr byte2
		}
		if {$incr3rdIpOctect > 0 && $byte3 < "254"} {
		    incr byte3 $incr3rdIpOctect
		}
		
		if {$incr2ndIpOctect > 0 && $byte2 >= "254"} {
		    set byte2 1
		    incr byte1
		}
		if {$incr2ndIpOctect > 0 && $byte2 < "254"} {
		    incr byte1 $incr2ndIpOctect
		}
	    }	    
	    set currentIpv4 $byte1.$byte2.$byte3.$byte4
	    puts "\t-ip $currentIpv4"
	    ixNet setAttribute $interface/ipv4 -ip $currentIpv4
	}
	
	if {[info exists startingGatewayIpv4]} {
	    # Generate IP Gateway address
	    if {$oneTimeOnly == 1} {
		if {$incr4thGatewayOctect > 0 && $gatewayByte4 >= "254"} {
		    set gatewayByte4 1
		    incr gatewayByte3 
		}
		if {$incr4thGatewayOctect > 0 && $gatewayByte4 < "254"} {
		    incr gatewayByte4 $incr4thGatewayOctect
		}
		
		if {$incr3rdGatewayOctect > 0 && $gatewayByte3 >= "254"} {
		    set gatewayByte3 1
		    incr gatewayByte2 
		}
		if {$incr3rdGatewayOctect > 0 && $gatewayByte3 < "254"} {
		    incr gatewayByte3 $incr3rdGatewayOctect
		}
		
		if {$incr2ndGatewayOctect > 0 && $gatewayByte2 >= "254"} {
		    set gatewayByte2 1
		    incr gatewayByte1
		}
		if {$incr2ndGatewayOctect > 0 && $gatewayByte2 < "254"} {
		    incr gatewayByte2 $incr2ndGatewayOctect
		}
	    }	    
	    set currentGatewayIpv4 $gatewayByte1.$gatewayByte2.$gatewayByte3.$gatewayByte4
	    puts "\t-gateway $currentGatewayIpv4"
	    ixNet setAttribute $interface/ipv4 -gateway $currentGatewayIpv4
	}
	
	if {[info exists macList]} {
	    # -ipv4List {{1 00:01:02:03:00:01} {2 00:02:02:03:00:01} {3 00:03:02:03:00:01}}
	    # lindex 0 = 2 00:02:02:03:00:01
	    lsearchList $interface/ethernet -macAddress $macList $currentInterfaceNumber
	}
	
	if {[info exists ipv4List]} {
	    # -ipv4List {{1 1.1.1.1} {2 2.2.2.1} {3 3.3.3.1}}
	    # lindex 0 = 2 2.2.2.1
	    lsearchList $interface/ipv4 -ip $ipv4List $currentInterfaceNumber
	}
	
	if {[info exists ipv4GatewayList]} {
	    lsearchList $interface/ipv4 -gateway $ipv4GatewayList $currentInterfaceNumber
	}
	
	if {[info exists ipv4MaskWidthList]} {
	    lsearchList $interface/ipv4 -maskWidth $ipv4MaskWidthList $currentInterfaceNumber
	}
	
	if {[info exists ipv4MaskWidth]} {
	    puts "\t-maskWidth $ipv4MaskWidth"
	    ixNet setAttribute $interface/ipv4 -maskWidth $ipv4MaskWidth
	}
	
	if {[info exists name]} {
	    lsearchList $interface -description $name $currentInterfaceNumber
	}
	
	if {[info exists enableList]} {
	    if {[regexp "A|all" $enableList]} {
		puts "\t-enable True"
		ixNet setAttribute $interface -enabled True
	    } else {
		if {[lsearch $enableList $currentInterfaceNumber] != -1} {
		    puts "\t-enable True"
		    ixNet setAttribute $interface -enabled True 
		}
	    }
	}
	
	if {[info exists disableList]} {
	    if {[regexp "A|all" $disableList]} {
		puts "\t-enable False"
		ixNet setAttribute $interface -enabled False
	    } else {
		if {[lsearch $disableList $currentInterfaceNumber] != -1} {
		    puts "\t-enable False"
		    ixNet setAttribute $interface -enabled False
		}
	    }
	}
	
	if {[info exists delete]} {
	    if {[regexp "A|all" $delete]} {
		puts "\tDelete interface: $currentInterfaceNumber"
		ixNet remove $interface
	    } else {
		if {[lsearch $delete $currentInterfaceNumber] != -1} {
		    puts "\tDelete interface: $currentInterfaceNumber"
		    ixNet remove $interface
		}
	    }
	}
	set oneTimeOnly 1
    }
    ixNet commit
}

proc CreateTrafficItemHlt { trafficItemParams } {
    upvar $trafficItemParams params

    # For non-full-mesh:        -src_dest_mesh one_to_one
    # For full-mesh:            -src_dest_mesh fully
    # For continuous traffic:   -transmit_mode continuous
    # For single burst traffic: -transmit single_burst -number_of_packets-per_stream 50000

    # How to use this from a script:
    #     set trafficItem1(-mode) create 
    #     set trafficItem1(-endpointset_count) 1
    #     set trafficItem1(-emulation_src_handle) $topology1(portHandle)
    #     set trafficItem1(-emulation_dst_handle) $topology2(portHandle)
    #     set trafficItem1(-src_dest_mesh) one_to_one
    #     set trafficItem1(-route_mesh) one_to_one
    #     set trafficItem1(-bidirectional) 0
    #     set trafficItem1(-allow_self_destined) 0
    #     set trafficItem1(-name) Traffic_Item_1
    #     set trafficItem1(-circuit_endpoint_type) ipv4
    #     set trafficItem1(-track_by) {trackingenabled0 sourceDestValuePair0}
    #     set trafficItem1(-l3_protocol) ipv4
    #
    #     set trafficItem1Objects [CreateTrafficItemHlt ::trafficItem1]

    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "\nCreateTrafficItemHlt: $paramList\n"
    set trafficItemStatus [eval ::ixia::traffic_config $paramList]

    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError CreateTrafficItem: $trafficItemStatus\n"
	return 1
    }

    return $trafficItemStatus
}

proc SendArpOnProtocolIntHlt { ports } {
    # This API will send ARP out of all the ports in -port_handle.
    # For Protocol Interface configuration.
    # Returns the Arp results.
    #
    # Success: {1/1/1 {{arp_request_success 1}}} {status 1}
    # Failed: 
    #
    # 1/1/1:
    #   arp_ipv4_interfaces_failed: ::ixNet::OBJ-/vport:2/interface:1
    #   arp_request_success: 0

    set arpStatus [::ixia::interface_config -mode modify -port_handle $ports -arp_send_req 1 -arp_req_retries 3]
    puts "\nSendArpOnProtocolInt: $arpStatus"

    return $arpStatus
}

proc StopAllProtocolsHlt { {platform legacy} } {
    # platform: legacy or ngpf

    if {$platform == "legacy"} {
	set params "::ixia::test_control -action stop_all_protocols"
    } 
    if {$platform == "ngpf"} {
	set params "::ixiangpf::test_control -action stop_all_protocols"
    } 
    
    puts "\nStopAllProtocolsHlt: $platform"
    set stopProtocolStatus [eval $params]
    if {[keylget stopProtocolStatus status] != $::SUCCESS} {
	puts "\nError StopAllProtocolsHlt failed:  $stopProtocolStatus\n"
	return 1
    }
    wait 5000
    return 0
}

proc ConfigIgmpHostHlt { igmpParams } {
    # Usage Example:
    #    set igmpHost($port1,-mode) create
    #    set igmpHost($port1,-port_handle) $port1
    #    set igmpHost($port1,-reset) 1
    #    set igmpHost($port1,-msg_interval) 0
    #    set igmpHost($port1,-igmp_version) v2
    #    set igmpHost($port1,-ip_router_alert) 0
    #    set igmpHost($port1,-general_query) 0
    #    set igmpHost($port1,-group_query) 0
    #    set igmpHost($port1,-count) 1
    #    set igmpHost($port1,-intf_ip_addr) 1.0.101.8
    #    set igmpHost($port1,-neighbor_intf_ip_addr) 1.0.101.254
    #    set igmpHost($port1,-intf_prefix_len) 24
    #    set igmpHost($port1,-vlan) 1
    #    set igmpHost($port1,-vlan_id) 101
    #    set igmpHostHandle($port1) [ConfigIgmpHostHlt ::igmpHost]    

    upvar $igmpParams params

    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "\nConfigIgmpHostHlt: $paramList\n"
    set status [eval ::ixia::emulation_igmp_config $paramList]

    if {[keylget status status] != $::SUCCESS} {
	puts "Error: igmp emulation config:\n[keylget status log]"
	return 1
    }
    # ::ixNet::OBJ-/vport:1/protocols/igmp/host:3
    return [keylget status handle]
}

proc CreateIgmpGroupHlt { igmpGroupParams } {
    # Usage Examples:
    #    set igmpGroup(-mode) create
    #    set igmpGroup(-num_groups) 10
    #    set igmpGroup(-ip_addr_start) 235.0.0.1
    #    set igmpGroup(-ip_addr_step) 0.0.0.1
    #    set igmpGroup(-ip_prefix_len) 24
    #    set igmpGroupHandle($port1) [ConfigIgmpGroupHlt ::igmpGroup]

    upvar $igmpGroupParams params

    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "\nCreateIgmpGroupHlt: $paramList\n"
    set status [eval ::ixia::emulation_multicast_group_config $paramList]

    if {[keylget status status] != $::SUCCESS} {
	puts "Create Error: igmp emulation group config:\n[keylget status log]"
	return 1
    }
    # group2
    return [keylget status handle]
}

proc ConfigIgmpGroupHlt { igmpParams } {
    # Usage Examples:
    #    set igmpHostToGroup(-mode) create
    #    set igmpHostToGroup(-session_handle) ::ixNet::OBJ-/vport:1/protocols/igmp/host:3
    #    set igmpHostToGroup(-group_pool_handle) ::ixNet::OBJ-/vport:1/protocols/igmp/host:3/group:3
    #    set igmpHostToGroupHandle($port1) [ConfigIgmpHostToGroupHlt ::igmpHostToGroup]

   upvar $igmpParams params

    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "\nConfigIgmpGroupHlt: $paramList\n"
    set status [eval ::ixia::emulation_igmp_group_config $paramList]

    if {[keylget status status] != $::SUCCESS} {
	puts "ConfigIgmpGroupHlt Error:\n[keylget status log]"
	return 1
    }
    # ::ixNet::OBJ-/vport:1/protocols/igmp/host:3/group:1
    return [keylget status handle]
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

proc ConfigIgmpSourceHlt { igmpParams } {
    upvar $igmpParams params
    
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }
    
    puts "\nConfigIgmpSourceHlt: $paramList\n"
    set status [eval ::ixia::emulation_multicast_source_config $paramList]
    
    if {[keylget status status] != $::SUCCESS} {
	puts "ConfigIgmpSourceHlt Error:\n[keylget status log]"
	return 1
    }
    # ::ixNet::OBJ-/vport:1/protocols/igmp/host:3/group:1
    return [keylget status handle]

}

proc ModifyIgmpGroup { args } {
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg { 
	    -port {
		set port [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -igmpGroup {
		set igmpGroup [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -count {
		set count [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -step {
		set step [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -sourceMode {
		set sourceMode [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -default {
		puts "\nModifyIgmpGroup: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    set vport [GetVportMapping $port]
    set igmpObj $vport/protocols/igmp

    foreach igmpHostNumObj [ixNet getList $igmpObj host] {	
	foreach igmpGroupObj [ixNet getList $igmpHostNumObj group] {
	    # TODO:  Incomplete. Need to know what to modify and how it is based on.
	}
    }
    ixNet commit
    
}

proc EnableIgmpGroup { port igmpGroupList } {
    # This API requires GetVportMapping API
    # port = 1/1/1 format
    # igmpGroupList = One or more IP addresses in a list.
    
    set vport [GetVportMapping $port]
    set igmpObj $vport/protocols/igmp

    foreach igmpHostNumObj [ixNet getList $igmpObj host] {	
	foreach igmpGroupObj [ixNet getList $igmpHostNumObj group] {
	    set currentIgmpGroup [ixNet getAttribute $igmpGroupObj -groupFrom]
	    if {[lsearch $igmpGroupList $currentIgmpGroup] != -1} {
		puts "\nEnableIgmpGroup: $igmpGroupObj $currentIgmpGroup"
		ixNet setAttribute $igmpGroupObj -enabled True
	    }
	}
    }
    ixNet commit
}

proc DisableIgmpGroup { port igmpGroupList } {
    # This API requires GetVportMapping API
    # port = 1/1/1 format
    # igmpGroupList = One or more IP addresses in a list.
    
    set vport [GetVportMapping $port]
    set igmpObj $vport/protocols/igmp

    foreach igmpHostNumObj [ixNet getList $igmpObj host] {	
	foreach igmpGroupObj [ixNet getList $igmpHostNumObj group] {
	    set currentIgmpGroup [ixNet getAttribute $igmpGroupObj -groupFrom]
	    if {[lsearch $igmpGroupList $currentIgmpGroup] != -1} {
		puts "\nDisableIgmpGroup: $igmpGroupObj $currentIgmpGroup"
		ixNet setAttribute $igmpGroupObj -enabled False
	    }
	}
    }
    ixNet commit
}

proc DeleteIgmpGroup { port igmpGroupList } {
    # This API requires GetVportMapping API
    # port = 1/1/1 format
    # igmpGroupList = One or more IP addresses in a list.
    
    set vport [GetVportMapping $port]
    set igmpObj $vport/protocols/igmp

    foreach igmpHostNumObj [ixNet getList $igmpObj host] {	
	foreach igmpGroupObj [ixNet getList $igmpHostNumObj group] {
	    set currentIgmpGroup [ixNet getAttribute $igmpGroupObj -groupFrom]
	    if {[lsearch $igmpGroupList $currentIgmpGroup] != -1} {
		puts "\nDeleteIgmpGroup: $igmpGroupObj $currentIgmpGroup"
		ixNet remove $igmpGroupObj
	    }
	}
    }
    ixNet commit
}

proc StartTrafficHlt {} {
    puts "\nStartTrafficHlt ..."
    set startTrafficStatus [::ixia::traffic_control \
				-action run \
				]
    if {[keylget startTrafficStatus status] != $::SUCCESS} {
	puts "\nError StartTrafficHlt: $startTrafficStatus\n"
	return 1
    } 

    # By including VerifyTrafficState, it will wait up to 15 seconds until
    # traffic is started before returning.
    VerifyTrafficState
    return 0
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

