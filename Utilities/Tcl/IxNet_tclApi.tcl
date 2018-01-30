#!/usr/bin/tclsh8.5
# By: Hubert Gee
# hgee@ixiacom.com

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

proc ConnectToIxiaNgpfHlt { connectParams } {
    # How to use from a script:
    #    set connect(-reset) 1
    #    set connect(-device) $ixiaChassisIp
    #    set connect(-port_list) $portList
    #    set connect(-ixnetwork_tcl_server) $ixNetworkTclServerIp
    #    set connect(-tcl_server) $ixiaChassisIp
    #    set connect(-username) $userName
    #    set connectStatus [ConnectToIxiaNgpfHlt ::connect]

    upvar $connectParams params
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "ConnectToIxiaNgpfHlt: Resetting Ixia ports. Please wait 40 seconds ..."
    set connectStatus [eval ::ixiangpf::connect $paramList]

    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "\nError: ConnectToIxiaNgpfHlt failed: $connectStatus\n"
	return 1
    } else {
	return $connectStatus
    }
}

proc ConnectToIxiaResumeHlt { args } {
    set sessionResumeFlag 1
    set paramList {}

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -ixnetwork_tcl_server {
		set ixNetworkTclServer [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
		append paramList " -ixnetwork_tcl_server $ixNetworkTclServer"
	    }
	    -tcl_server {
		set tclServer [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
		append paramList " -tcl_server $tclServer"
	    }
	    -username {
		set username [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
		append paramList " -username $username"
	    }
	    -session_resume_keys {
		set sessionResumeFlag [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "ConnectToIxiaResume: No such parameter: $currentArg"
		return 1
	    }
	}
    }

    append paramList " -session_resume_keys $sessionResumeFlag"

    puts "ConnectToIxiaResumeHlt ..."
    set connectStatus [eval ::ixia::connect $paramList]

    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "\nError ConnectToIxiaResumeHlt: $connectStatus\n"
	return 1
    } else {
        return $connectStatus
    } 
}

proc ResumeHHlt { connectParams } {
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

    puts "Resume..."
    set status [eval ::ixia::connect $paramList]
    return $status
}

proc ConnectToIxiaResumeNgpfHlt { args } {
    set sessionResumeFlag 1
    set paramList {}

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg { 
	    -ixnetwork_tcl_server {
		set ixNetworkTclServer [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
		append paramList " -ixnetwork_tcl_server $ixNetworkTclServer"
	    }
	    -tcl_server {
		set tclServer [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
		append paramList " -tcl_server $tclServer"
	    }
	    -username {
		set username [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
		append paramList " -username $username"
	    }
	    -session_resume_keys {
		set sessionResumeFlag [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "No such parameter: $currentArg"
		return 1
	    }
	}
    }

    append paramList " -session_resume_keys $sessionResumeFlag"

    puts "ConnectToIxiaResumeNgpfHlt ..."
    set connectStatus [eval ::ixiangpf::connect $paramList]
    
    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "ConnectToIxiaNgpfResume: $connectStatus\n"
	return 1
    } else {
        return $connectStatus
    } 
}

proc GetTime {} {
    return [clock format [clock seconds] -format "%H:%M:%S"]
}

proc EnableHltDebugHlt { {filename ""} } {
    # Creating a HLT debug log file in case debugging is needed

    set ::ixia::logHltapiCommandsFlag 1
    if {$filename == ""} {
	set ::ixia::logHltapiCommandsFileName ixiaHltDebug_[GetTime].txt
    } else {
	set ::ixia::logHltapiCommandsFileName $filename
    }
}

proc PortConfigProtocolIntHlt { portConfigParams } {
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
    #    set endpoint($port) [PortConfigProtocolIntHlt $port ::portConfig]
    #
    # For scaling:
    #    You have to create a list like below and the list must align 
    #    with each list's index accordlingly.
    # 
    #       ports       = {1/1/1    1/1/1    1/1/1}
#   #       ipList      = {1.1.1.1  1.1.1.2  1.1.1.3}
#   #       gatewayList = {1.1.1.4  1.1.1.5  1.1.1.6}
#   #       vlanList    = {1001     1002     1003}
#   #       macList     = {same as above}

    upvar $portConfigParams params
    
    puts "\nPortConfigProtocolIntHlt: $port"
    foreach {properties values} [array get params $port,*] {
	set property [lindex [split $properties ,] end]
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

proc PortConfigProtocolIntNgpfHlt { portConfigParams } {
    # How to use this from a script:
    #    set portConfig1(-mode)                    config
    #    set portConfig1(-mtu)                     1500
    #    set portConfig1(-protocol_handle)         $deviceGroup1(topo1,groupHandle)
    #    set portConfig1(-ipv4_resolve_gateway)    1
    #    set portConfig1(-ipv4_manual_gateway_mac) 00.00.00.00.00.01
    #    set portConfig1(-gateway)                 1.1.1.11
    #    set portConfig1(-gateway_step)            0.0.0.0
    #    set portConfig1(-intf_ip_addr)            1.1.1.1
    #    set portConfig1(-intf_ip_addr_step)       0.0.0.1
    #    set portConfig1(-netmask)                 255.255.255.0
    #    set portConfig1(-src_mac_addr)            00:01:01:01:00:01
    #    set portConfig1(-src_mac_addr_step)       00:00:00:00:00:01
    #    set portConfig1(-vlan)                    1
    #    set portConfig1(-vlan_id)                 100
    #    set portConfig1(-vlan_user_priority)      3
    #    set portConfig1(-vlan_id_count)           5
    #    set portConfig1(-vlan_id_step)            1
    #    set portConfig1(-vlan_user_priority_step) 0
    # 
    #    set deviceGroup1Topo1 [PortConfigProtocolIntNgpfHlt ::portConfig1]

    upvar $portConfigParams params

    puts "\nPortConfigProtocolIntNgpfHlt ..."
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    set interfaceConfigStatus [eval ::ixiangpf::interface_config $paramList]
    
    if {[keylget interfaceConfigStatus status] != $::SUCCESS} {
	puts "\nError PortConfigProtocolIntNgpfHlt:\n$interfaceConfigStatus\n"
	return 1
    }

    # keylget interfaceConfigStatus:
    #    ethernet_handle: /topology:2/deviceGroup:2/ethernet:1
    #    ipv4_handle: /topology:2/deviceGroup:2/ethernet:1/ipv4:1
    #    interface_handle: /topology:2/deviceGroup:2/ethernet:1/ipv4:1/item:1
    # interface object = ::ixNet::OBJ-/vport:1/interface:1

    return $interfaceConfigStatus
}

proc PortConfigStaticIpHlt { port portConfigParams } {
    # This API is for scaling L3 without Protocol Interface config.
    # No protocol configurations on the host.
    # Calling this API requires you to also call StartAllProtocols
    # to start StaticIpAuth for ARPing.

    upvar $portConfigParams params

    foreach {properties values} [array get params $port,*] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "\nPortConfigStaticIpHlt: $port"
    set interfaceConfigStatus [eval ::ixia::interface_config $paramList]

    if {[keylget interfaceConfigStatus status] != $::SUCCESS} {
	puts "\nError PortConfigStaticIp:\n$interfaceConfigStatus\n"
	return 1
    }

    # Need to enable global ARP for each IP address
    EnableGlobalArpForEachIp
    
    # We want to parse out and return ::ixNet::OBJ-/vport:1/protocolStack.
    # For Traffic Item endpoint usage.
    set interfaceHandle [keylget interfaceConfigStatus interface_handle]
    return $interfaceHandle
}

proc PortConfigStaticLanHlt { port portConfigParams } {
    # This API is for scaling L2 only and without Protocol Interface config.
    # No protocol configurations on the host.

    upvar $portConfigParams params

    # Starting with HLT version 4.81, it requires this new parameter
    #set paramList {-lan_range_count 1 }

    foreach {properties values} [array get params $port,*] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "\nPortConfigStaticLanHlt: $port"
    set interfaceConfigStatus [eval ::ixia::interface_config $paramList]
    
    if {[keylget interfaceConfigStatus status] != $::SUCCESS} {
	puts "\nError PortConfigStaticLan:\n$interfaceConfigStatus\n"
	return 1
    }
    
    # ::ixNet::OBJ-/vport:1/protocols/static/lan:1
    set interfaceHandle [keylget interfaceConfigStatus interface_handle]
    return $interfaceHandle
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

proc EnableTrafficItemHlt { trafficItem } {
    # Note: HLT returns Traffic Item keys like this:
    #       ::ixNet::OBJ-/traffic/trafficItem:7/configElement:1
    #       Need to parse out ::ixNet::OBJ-/traffic/trafficItem:7 only.
    #       
    regexp "(.*trafficItem:\[0-9]+)" $trafficItem - trafficItemId

    puts "\nEnableTrafficItemHlt: $trafficItem\n"
    set trafficItemStatus [::ixia::traffic_config -mode enable -stream_id $trafficItemId]
    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError EnableTrafficItemHlt: $status\n"
	return 1
    }
    return 0
}

proc DisableTrafficItemHlt { trafficItem } {
    regexp "(.*trafficItem:\[0-9]+)" $trafficItem - trafficItemId

    puts "\nDisableTrafficItemHlt: $trafficItem\n"
    set trafficItemstatus [::ixia::traffic_config -mode disable -stream_id $trafficItemId]
    if {[keylget trafficItemstatus status] != $::SUCCESS} {
	puts "\nError DisableTrafficItemHlt: $status\n"
	return 1
    }
    return 0
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

proc StartAllProtocolsHlt { {platform legacy} } {
    # platform: legacy or ngpf

    if {$platform == "legacy"} {
	set params "::ixia::test_control -action start_all_protocols"
    } 

    if {$platform == "ngpf"} {
	set params "::ixiangpf::test_control -action start_all_protocols"
    } 

    puts "\nStartAllProtocolsHlt: $platform"
    set startProtocolStatus [eval $params]
    if {[keylget startProtocolStatus status] != $::SUCCESS} {
	puts "\nError StartAllProtocolsHlt:  $startProtocolStatus\n"
	return 1
    }

    return 0
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

proc StartAllProtocols {} {
    puts "\nStartAllProtocols ..."
    catch {ixNet exec startAllProtocols} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "\nStartAllProtocols failed: $errMsg\n"
	return 1
    }
    ixNet commit
    Sleep 5000
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

proc StartTraffic { {includeApplyTraffic apply} } {
    # Need to make apply traffic an optional parameter because
    # not every situation can except apply traffic prior to 
    # starting traffic such as packet capture.  
    # If apply traffic for packet capture, it will stop the packet
    # capture. This is a HLT bug as of HLT 4.90

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
    
    VerifyTrafficState
    
    return 0
}

proc StartTrafficHlt {} {
    puts "\nStartTrafficHlt"
    set startTrafficStatus [::ixia::traffic_control -action run]
    if {[keylget startTrafficStatus status] != $::SUCCESS} {
	puts "\nError StartTrafficHlt: $startTrafficStatus\n"
	return 1
    } 

    # By including VerifyTrafficState, it will wait up to 15 seconds until
    # traffic is started before returning.
    VerifyTrafficState
    return 0
}

proc StartTrafficNgpfHlt {} {
    puts "\nStartTrafficNgpfHlt"
    set startTrafficStatus [::ixiangpf::traffic_control -action run]
    if {[keylget startTrafficStatus status] != $::SUCCESS} {
	puts "\nError StartTrafficHlt: $startTrafficStatus\n"
	return 1
    } 

    # By including VerifyTrafficState, it will wait up to 15 seconds until
    # traffic is started before returning.
    VerifyTrafficState
    return 0
}

proc StopTrafficHlt {} {
    puts "\nStopTrafficHlt ..."
    set stopTrafficStatus [::ixia::traffic_control -action stop]
    if {[keylget stopTrafficStatus status] != $::SUCCESS} {
	puts "\nError StopTrafficHlt: $stopTrafficStatus\n"
	return 1
    } 
    after 5000
    return 0
}

proc StopTrafficNgpfHlt {} {
    puts "\nStopTrafficNgpfHlt ..."
    set stopTrafficStatus [::ixiangpf::traffic_control -action stop]
    if {[keylget stopTrafficStatus status] != $::SUCCESS} {
	puts "\nError StopTrafficNgpfHlt: $stopTrafficStatus\n"
	return 1
    } 
    after 5000
    return 0
}

proc StopSpecifiedTrafficHlt { {trafficItemList ""} } {
    # Only stop spesific Traffic Items, if a list is provided

    if {$trafficItemList != "" } {
	foreach item [::ixTclNet::GetTrafficItemList] {
	    if { [lsearch $trafficItemList [ixNet getAttribute $item -name]] != -1 } {
		puts "\n$stopTraffic: $item"
		ixNet exec stopStatelessTraffic $item
	    }
	}
    } else {
	puts "\nStopSpecifiedTrafficHlt ..."
	set stopTrafficStatus [::ixia::traffic_control \
				   -action stop \
				  ]
	if {[keylget stopTrafficStatus status] != $::SUCCESS} {
	    puts "\nError StopTraffic: $stopTrafficStatus\n"
	    return 1
	}
	puts "\n$stopTrafficStatus"
    }
    wait 5000
    return 0
}

proc GetStatViewOnCsv { csvFileName {typeOfStats "Flow Statistics"}} {
    # This API will create and overwrite the existing
    # $csvFileName.
    # 
    # All Statistics will be written to $csvFileName
    # in csv format.
    #
    # typeOfStats options:
    #    "Flow Statistics"  (Default)
    #    "Port Statistics"
    #    "Tx-Rx Frame Rate Statistics"
    #    "Port CPU Statistics"
    #    "Global Protocol Statistics"
    #    "L2-L3 Test Summary Statistics"
    #    "Flow Detective"
    #    "Data Plane Port Statistics"
    #    "User Defined Statistics"
    #    "Traffic Item Statistics"
    # 

    exec echo "" > $csvFileName

    set viewList [ixNet getList [ixNet getRoot]/statistics view]
    puts "$viewList"
    set statViewSelection $typeOfStats

    set flowStatsViewIndex [lsearch -regexp $viewList $statViewSelection]
    if {$flowStatsViewIndex == -1} {
	puts "GetStatViewOnCsv: No \"$statViewSelection\" found"
	return 1
    }

    # $view: ::ixNet::OBJ-/statistics/view:"Flow Statistics"
    set view [lindex $viewList $flowStatsViewIndex]

    ixNet setAttribute $view -enabled true
    ixNet commit

    set columnList [ixNet getAttribute ${view}/page -columnCaptions]

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
    #puts "\n$newColumnList"
    exec echo $newColumnList >> $csvFileName

    set startTime 1
    set stopTime 30
    while {$startTime < $stopTime} {
	set totalPages [ixNet getAttribute $view/page -totalPages]
	if {[regexp -nocase "null" $totalPages]} {
	    puts "\nGetStatViewOnCsv: Getting total pages for $view is not ready. $startTime/$stopTime"
	    after 2000
	} else {
	    break
	}
    }
    
    # Iterrate through each page 
    for {set currPage 1} {$currPage <= $totalPages} {incr currPage} {
	puts "\nGetStatViewOnCsv: Getting statistics on page: $currPage/$totalPages"

	catch {ixNet setAttribute $view/page -currentPage $currPage} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nGetStatViewOnCsv: Failed to get statistic for current page."
	    return 1
	}
	ixNet commit
	
	# Wait for statistics to populate on current page
	set whileLoopStopCounter 0
	while {[ixNet getAttribute $view/page -isReady] != "true"} {
	    if {$whileLoopStopCounter == "5"} {
		puts "\nGetStatViewOnCsv: Could not get stats"
		return 1
	    }
	    if {$whileLoopStopCounter < 5} {
		puts "GetStatViewOnCsv: Not ready yet.  Waiting $whileLoopStopCounter/5 seconds ..."
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
		# cellList: 1/1/1 1/1/2 TI0-Flow_1 1.1.1.1-1.1.2.1 4000 4000 0 0 0 0 256000 0 0 0 0 0 0 0 0 0 0 0 00:00:00.684 00:00:00.700
		set cellList [lindex $rowList $rowIndex]
		
		regsub -all " " $cellList "," newCellList
		exec echo $newCellList >> $csvFileName
	    }
	}
    }
}

proc GetStats {{viewName "Flow Statistics"}} {
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

proc GetStatView { {getStatsBy trafficItem} } {
    set viewList [ixNet getList [ixNet getRoot]/statistics view]
    #puts "\nviewList: $viewList\n"

    set statViewSelection "Flow Statistics"

    set flowStatsViewIndex [lsearch -regexp $viewList $statViewSelection]
    if {$flowStatsViewIndex == -1} {
	puts "\nGetStatView: No \"$statViewSelection\" found"
	return 1
    }

    # $view: ::ixNet::OBJ-/statistics/view:"Flow Statistics"
    set view [lindex $viewList $flowStatsViewIndex]

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
    
    # Iterrate through each page 
    set row 0
    for {set currPage 1} {$currPage <= $totalPages} {incr currPage} {
	puts "\nGetStatView: Getting statistics on page: $currPage/$totalPages"

	catch {ixNet setAttribute $view/page -currentPage $currPage} errMsg
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
		
		puts "\n--- cellList $pageListIndex: $cellList ---\n"

		# Get the Traffic Item name
		set trafficItemIndex [lsearch $columnList "Traffic Item"]
		if {$trafficItemIndex == -1} {
		    set trafficItem "UnknownTrafficItem $pageListIndex"
		} else {
		    set trafficItem [lindex $cellList $trafficItemIndex]
		}

		set rxPortIndex [lsearch $columnList "Rx Port"]
		set rxPort [lindex $cellList $rxPortIndex]
		
		foreach column $columnList item $cellList {
		    if {[regexp "VLAN:VLAN Priority" $column]} {
			set column "Vlan_Priority"
		    }
		    if {[regexp "VLAN:VLAN-ID.*1" $column]} {
			set column "Inner_Vlan_ID"
		    }
		    if {[regexp "VLAN:VLAN-ID" $column]} {
			# This is also Outer VlanID
			set column "Vlan_ID"
		    }
		    if {[regexp "IPv4 :Source Address" $column]} {
			set column "IPv4_Src_Address"
		    }
		    if {[regexp "IPv4 :Destination Address" $column]} {
			set column "IPv4_Dst_Address"
		    }
		    if {[regexp "Ethernet II:Destination MAC Address" $column]} {
			set column "Dest_Mac_Address"
		    }
		    if {[regexp "Ethernet II:Source MAC Address" $column]} {
			set column "Src_Mac_Address"
		    }
		    if {$getStatsBy == "trafficItem"} {
			if {[regexp "Traffic Item" $column] == 0} {
			    keylset getStats trafficItem.[join $trafficItem _].flow.$row.[join $column _] $item
			}
		    }
		    if {$getStatsBy == "port"} {
			if {[regexp "Rx Port" $column] == 0} {
			    keylset getStats rxPort.$rxPort.trafficItem.[join $trafficItem _].[join $column _] $item
			}
		    }
		    keylset getStats totalFlows $row
		}
	    }
	}
    }

    return $getStats
}

# I have not validated this yet
proc GetFlowStats {sList} {
    if $::debug {puts "GetFlowStats at [clock format [clock seconds] -format {%H:%M:%S}]"}
    set returnValue {}
    set statList $sList
    set root [ixNet getRoot]
    foreach row [ixNet getList $root/statistics/statViewBrowser:\"Traffic\ Item\ Statistics\" row] {
        regsub {row:} [lindex [split $row "/"] end] {} trafficItem
        set flowStats [join $trafficItem]
        foreach stat $statList {
            lappend flowStats [list [join $stat] [ixNet getAttribute $row/cell:$stat -statValue]]
        }
        lappend returnValue $flowStats
    }
    return $returnValue
}

proc CreateQinQStackAndTrackHlt { packetStack } {
    foreach stack $packetStack {
	if {[regexp "vlan" $stack]} {
	    puts "\nCreateQinQStackAndTrackHlt: $stack" 
	    set streamResult [::ixia::traffic_config  \
				  -mode modify \
				  -stream_id $stack \
				  -vlan enable \
				  -vlan_id_tracking 1 \
				 ]
	    if {[keylget streamResult status] != $::SUCCESS} {
		puts "\nError CreateQinQStackAndTrackHlt: $stack\n"
		return 1
	    }
	}
    }
    return 0
}

proc ModifyStreamLineRateHlt { streamId ratePercentage } {
    # streamId format could be any of the followings:
    #      ::ixNet::OBJ-/traffic/trafficItem:1
    #      ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1

    puts "\nModifyStreamLineRateHlt: $streamId : $ratePercentage\%"
    set trafficItemStatus [eval ::ixia::traffic_config \
			       -mode modify \
			       -stream_id $streamId \
			       -rate_percent $ratePercentage \
			      ]
    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError ModifyStreamLineRateHlt: $trafficItemStatus\n"
	return 1
    }
    return 0
}

proc ModifyFlowLineRateHlt { trafficItemName endpointSetName rate } {
    # trafficItemName = The Traffic Item Name in exact spelling
    # endpointSetName = The endpointSet name
    # rate            = The percentage number

    set trafficItem [GetTrafficItemByName $trafficItemName]
    puts "\ntrafficItem: $trafficItem\n"

    if {$trafficItem == "" || $trafficItem == "0"} {
	puts "\nError ModifyFlowLineRateHlt: No such Traffic Item name: $trafficItemName"
	return 1
    }
    
    set highLevelStreamId [GetEndpointSetHandle $trafficItem $endpointSetName]
    if {$highLevelStreamId == 0} {
	puts "\nGetEndpointSetHandle: No such name found in flow group in Traffic Item $trafficItemName: $endpointSetName\n"
	return 1
    }

    puts "\nModifyFlowLineRateHlt: $highLevelStreamId : rate = $rate"
    set status [::ixia::traffic_config \
		    -mode modify \
		    -stream_id $highLevelStreamId \
		    -rate_percent $rate \
		   ]
    
    if {[keylget status status] != $::SUCCESS} {
	puts "\nError ModifyFlowLineRateHlt: $status\n"
	return 1
    }

    return 0
}

proc ModifyStreamTransmitModeHlt { trafficItemName transmitMode {totalPackets 10000} } {
    # This API will modify the given Traffic Item's transmit mode
    # 
    # trafficItemName = The Traffic Item name in exact spelling.
    # transmitMode = continuous or packetsPerBurst
    # totalPackets = Optional and for transmitMode only.
    #                Pass in the total packet count to burst.

    set trafficItem [GetTrafficItemByName $trafficItemName]
    if {$trafficItem == "" || $trafficItem == "0"} {
	puts "\nError ModifyStreamTransmitModeHlt: No such Traffic Item name: $trafficItemName"
	return 1
    }

    set params {-mode modify -stream_id $trafficItem}

    if {$transmitMode == "packetsPerBurst"} {
	append params " -transmit_mode single_burst -pkts_per_burst $totalPackets"
    }

    if {$transmitMode == "continuous"} {
	append params " -transmit_mode continuous"
    }

    puts "\nModifyStreamTransmitModeHlt: $params"
    set trafficItemStatus [eval ::ixia::traffic_config $params]

    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError ModifyStreamTransmitModeHlt: $trafficItemStatus\n"
	return 1
    }
    return 0
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

proc ModifyStreamIpPrecedenceHlt { streamId ipPrecedenceValue } {
    # streamId format = ::ixNet::OBJ-/traffic/trafficItem:1
    # ipPrecedenceValue = 0-7

    puts "\nModifyStreamIpPrecedenceHlt: $streamId : $ipPrecedenceValue"
    set trafficItemStatus [eval ::ixia::traffic_config \
			       -mode modify \
			       -stream_id $streamId \
			       -ip_precedence $ipPrecedenceValue \
			      ]
    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError ModifyStreamIpPrecedenceHlt: $trafficItemStatus\n"
	return 1
    }
    return 0
}

proc RegenerateTrafficItems { {trafficItemList all} } {
    # trafficItemList == one or more traffic item names in a list
    #                    DEFAULT is all

    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set trafficItemName [ixNet getAttribute $trafficItem -name]

	if {$trafficItemList != "all" && [lsearch $trafficItemList $trafficItemName] != -1} {
	    puts "\nRegenerateTrafficitem: $trafficItemName"
	    catch {ixNet exec generate $trafficItem} errMsg
	}
	if {$trafficItemList == "all"} {
	    puts "\nRegenerateTrafficItem: $trafficItemName"
	    catch {ixNet exec generate $trafficItem} errMsg
	}
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError RegenerateTrafficItem failed on $trafficItem : $errMsg\n"
	    return 1
	}
    }
    after 3000
    return 0
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
	set card [lindex [split [lindex [split $connectedTo /] 3] :] end]
	set portNum [lindex [split [lindex [split $connectedTo /] 4] :] end]
	set port $card/$portNum
	if {$port == $Port} {
	    return $vport
	}
    }
    return 0
}

proc GetVportPhyPort { vport } {
    # Based on the $vport, return the physical port number.
    # Port format is: 1/1.  Not 1/1/1

    set connectedTo [ixNet getAttribute $vport -connectedTo]
    set card [lindex [split [lindex [split $connectedTo /] 3] :] end]
    set portNum [lindex [split [lindex [split $connectedTo /] 4] :] end]
    set port $card/$portNum
    return $port
}

proc GetStatViewArp {} {
    # This API will look at the "Global Protocol Statistics" tablet
    # on the IxNetwork GUI for ARP request replies.
    # Mainly for Static IP w/Auth configuration.  When this protocol
    # is enabled, it will generate ARPs out of each IP host.
    # This API will retrieve the total number of ARP request replies.

    set viewList [ixNet getList [ixNet getRoot]/statistics view]
    puts "\nGetStatViewArp: viewList: $viewList\n"

    set statViewSelection "Global Protocol Statistics"
    set flowStatsViewIndex [lsearch -regexp $viewList $statViewSelection]
    if {$flowStatsViewIndex == -1} {
	puts "\nGetStatViewArp: ViewStats: No \"$statViewSelection\" found"
	return ""
    }

    set view [lindex $viewList $flowStatsViewIndex]

    ixNet setAttribute $view -enabled true
    ixNet commit

    # $columnList:
    # {Stat Name} {Port Name} {Control Packet Tx.} {Control Packet Rx.} {Ping Reply Tx.} {Ping Request Tx.} {Ping Reply Rx.} {Ping Request Rx.} {Arp Reply Tx.} {Arp Request Tx.} {Arp Request Rx.} {Arp Reply Rx.} {Neighbor Solicitation Tx.} {Neighbor Advertisement Tx.} {Neighbor Solicitation Rx.} {Neighbor Advertisement Rx.}

    set columnList [ixNet getAttribute ${view}/page -columnCaptions]
    #puts "\n$columnList\n"

    set startTime 1
    set stopTime 30
    while {$startTime < $stopTime} {
	set totalPages [ixNet getAttribute $view/page -totalPages]
	if {[regexp -nocase "null" $totalPages]} {
	    puts "\nGetStatViewArp: Getting total pages for $view is not ready. $startTime/$stopTime"
	    after 2000
	} else {
	    break
	}
    }

    # Iterrate through each page 
    for {set currPage 1} {$currPage <= $totalPages} {incr currPage} {
	catch {ixNet setAttribute $view/page -currentPage $currPage} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nGetResults: Failed to get statistic for current page."
	    return 1
	}
	ixNet commit
	
	set pageList [ixNet getAttribute $view/page -rowValues] ;# first list of all rows in the page
	set totalFlowStatistics [llength $pageList]

	# totalPageList == The total amount of flow statistics
	for {set pageListIndex 0} {$pageListIndex <= $totalFlowStatistics} {incr pageListIndex} {
	    set rowList [lindex $pageList $pageListIndex] ;# second list of 1 ingress and x egress rows

	    for {set rowIndex 0} {$rowIndex < [llength $rowList]} {incr rowIndex} {
		# cellList: 10.205.4.155/Card01/Port01 1/1/1 249 249 0 0 0 0 249 0 249 0 0 0 0 0
		set cellList [lindex $rowList $rowIndex] ;# third list of cell values

		# 10.205.4.155/Card01/Port02
		set port [lindex $cellList 0]
		regexp "\[0-9]+\.\[0-9]+\.\[0-9]+\.\[0-9]+/Card(\[0-9]+)/Port(\[0-9]+)" $port - cardNumber portNumber
		regsub "^\[0]" $cardNumber "" card
		regsub "^\[0]" $portNumber "" port
		
		foreach column $columnList item $cellList {
		    if {[regexp "Arp Request Rx" $column]} {
			set column "Arp_Request_Rx"
			keylset getStats $card/$port.$column $item
		    }
		}
	    }
	}
    }

    if {[info exists getStats] == 0} {
	return 1
    } else {
	return $getStats
    }
}

proc GetStatsHlt { {typeOfStats flow} } {
    puts "\nGetStatsHlt: $typeOfStats"
    set flowStats [::ixia::traffic_stats -mode flow]
    if {[keylget flowStats status] != $::SUCCESS} {
	puts "GetStatsHlt: Failed to get statistics: $flowStats"
	return
    }
    return $flowStats
}

proc VerifyArpStatCounter { portList totalExpectedArps } {
    # This API will call GetStatViewArp
    # and wait up to 5 minutes for the total expected
    # number of ARPs replied from the DUT.

    set stats [GetStatViewArp]
    puts "\n[KeylPrint stats]\n"
    set failedArpList ""
    
    foreach port $portList {
	for {set timer 0} {$timer <= 300} {incr timer} {
	    set rxArps [keylget stats $port.Arp_Request_Rx]
	    if {$rxArps != $totalExpectedArps && $timer != "300"} {
		puts "\nVerifyArpStatCounter: $port learned $rxArps/$totalExpectedArps arps. Retrying $timer/300"
		after 1000
	    }
	    if {$rxArps != $totalExpectedArps && $timer == "300"} {
		lappend failedArpList $port
	    }
	}
    }
    
    if {$failedArpList == ""} {
	puts "VerifyArpStatCounter: All ports received Arp replies."
	return 0
    } else {
	puts "\nError VerifyArpStatCounter: Ports did not receive $totalExpectedArps arps: $failedArpList"
	return 1
    }
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


proc RestartStaticIpAuthProtocol { portList } {
    # This API will restart all protocols.
    # Mainly for re-arping
    
    puts "\nRestartStaticIpAuthProtocol ,,,"
    StopStaticAuthProtocol $portList
    StartStaticAuthProtocol $portList
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

proc GetAssignedPort { name } {
    # By default, IxNetwork assigns ports in the format of "1/1/1".
    # This would be the name passed in as the parameter.

    foreach vport [ixNet getList [ixNet getRoot] vport] {
	set currentName [ixNet getAttribute $vport -name]

	if {$currentName == $name} {
	    set assignedPort [ixNet getAttribute $vport -assignedTo]
	    set assignedPort [split $assignedPort :]
	    set chassis [lindex $assignedPort 0]
	    set card    [lindex $assignedPort 1]
	    set port    [lindex $assignedPort 2]
	    return $card/$port
	}
    }
    return unknownPort
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

proc CreateNewTopologyNgpfHlt { topologyParams } {
    # How to use this from a script:
    #     set port1 1/1/3
    #     set topology1(-topology_name)  "IPv4 Topology Tx-1"
    #     set topology1(-port_handle) [  list [list $port1]]
    #     set topology1Keys [CreateNewTopologyNgpfHlt ::topology1]
    #     set topology1(portHandle) [keylget topology1Keys topology_handle]

    upvar $topologyParams params

    puts "\nCreateNewTopologyNgpfHlt ..."
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "\nCreateNewTopologyNgpfHlt paramList: $paramList"
    set topologyStatus [eval ::ixiangpf::topology_config $paramList]

    if {[keylget topologyStatus status] != $::SUCCESS} {
	puts "\nError CreateNewTopologyNgpfHlt: $topologyStatus"
	return 1
    }
    
    return $topologyStatus
}

proc CreateNewDeviceGroupNgpfHlt { deviceGroupParams } {
    # How to use this from a script:
    #     set deviceGroup1(topo1,-topology_handle) $topology1(portHandle)
    #     set deviceGroup1(topo1,-device_group_multiplier) 5
    #     set deviceGroup1(topo1,-device_group_name) "Ipv4 Tx-1"
    #     set deviceGroup1(topo1,-device_group_enabled) 1
    #     set deviceGroup1(topo1,protocolName) "Ethernet"
    #     set topo1DeviceGroup1Keys [CreateNewDeviceGroupNgpfHlt ::deviceGroup1]
    #     set deviceGroup1(topo1,groupHandle) [keylget topo1DeviceGroup1Keys device_group_handle]

    upvar $deviceGroupParams params

    puts "\nCreateNewDeviceGroupNgpfHlt"
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	
	# Using regexp to parse out $property with a dash because only dashes 
	# in front of a parameter is a hlt parameter.
	if {[regexp -- "-" $property]} {
	    append paramList "$property $values "
	}
    }
    
    set topoDeviceGroupStatus [eval ::ixiangpf::topology_config $paramList]

    if {[keylget topoDeviceGroupStatus status] != $::SUCCESS} {
	puts "\nError CreateNewDeviceGroupNgpfHlt: $topoDeviceGroupStatus"
	return 1
    } 

    return $topoDeviceGroupStatus
}

proc ClearStatsHlt {} {
    puts "\nClearStatsHlt ..."
    ::ixia::traffic_control -action clear_stats
}

proc ClearStatsNgpfHlt {} {
    puts "\nClearStatsNgpfHlt ..."
    ::ixiangpf::traffic_control -action clear_stats
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
    # Usage example:
    #    set igmpSource2(-mode) create
    #    set igmpSource2(-num_sources) 3
    #    set igmpSource2(-ip_addr_start) 10.1.1.11
    #    set igmpSource2(-ip_addr_step) 0.0.0.1
    #    set igmpSource2(-ip_prefix_len) 24
    #    set igmpSourceHandle2($port1) [ConfigIgmpSourceHlt ::igmpSource2]
    
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

proc CreateIgmpHostNgpfHlt { igmpHostParams } {
    upvar $igmpHostParams params

    puts "\nCreateIgmpHostNgpfHlt ...\n"
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    set igmpHostStatus [eval ::ixiangpf::emulation_igmp_config $paramList]
    
    if {[keylget igmpHostStatus status] != $::SUCCESS} {
	puts "\nError CreateIgmpHostNgpfHlt:\n$igmpHostStatus"
    }

    return $igmpHostStatus
}

proc CreateIgmpGroupEmulationNgpfHlt { igmpGroupParams } {
    upvar $igmpGroupParams params

    puts "\nCreateIgmpGroupEmulation ...\n"
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    set igmpGroupStatus [eval ::ixiangpf::emulation_igmp_group_config $paramList]
    if {[keylget igmpGroupStatus status] != $::SUCCESS} {
	puts "\nError CreateImgpGroupEmulation: $igmpGroupStatus"
    }
    return $igmpGroupStatus

}
 
proc CreateIgmpQuerierNgpfHlt { igmpQuerierParams } {
    upvar $igmpQuerierParams params

    puts "\nCreateIgmpQuerierNgpfHlt ..."
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }
    
    set igmpQuerierStatus [eval ::ixiangpf::emulation_igmp_querier_config $paramList]
    if {[keylget igmpQuerierStatus status] != $::SUCCESS} {
	puts "\nError CreateIgmpQuerierNgpfHlt: $igmpQuerierStatus"
	return 1
    }
    return $igmpQuerierStatus
}


proc StartIgmpEmulationNgpfHlt { igmpHandle } {
    # igmpHandle could be IGMP host or IGMP Querier

    foreach handle $igmpHandle {
	puts "\nStartIgmpEmulationNgpfHlt: $handle"
	set igmpStatus [::ixiangpf::emulation_igmp_control \
			    -mode   start \
			    -handle $handle \
			   ]
	
	if {[keylget igmpStatus status] != $::SUCCESS} {
	    puts "\nError StartIgmpEmulationNgpfHlt: $igmpStatus\n"
	    return 1
	}
    }
    after 10000
    return 0
}


proc StopIgmpEmulationNgpfHlt { igmpHandle } {
    # igmpHandle could be IGMP host or IGMP Querier
    foreach handle $igmpHandle {
	puts "\nStopIgmpEmulationNgpfHlt: $handle"
	set igmpStatus [::ixiangpf::emulation_igmp_control \
			    -mode   stop \
			    -handle $igmpHandle \
			   ]
	
	if {[keylget igmpStatus status] != $::SUCCESS} {
	    puts "\nError StopIgmpEmulationNgpfHlt: $igmpStatus\n"
	    return 1
	}
    }
    after 10000
    return 0
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

proc GetIgmpQuerierAggregatedStatsNgpfHlt { igmpQuerierHandle } {
    # Querier Aggregated Stats: /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1 = {aggregate {{status started} {sessions_total 1} {sessions_up 1} {sessions_down 0} {sessions_notstarted 0}}}

    puts "\nGetIgmpQuerierAggregatedStatsNgpfHlt ..."
    set igmpQuerierStatus [::ixiangpf::emulation_igmp_info \
			       -mode        aggregate \
			       -handle      $igmpQuerierHandle \
			       -type        querier \
			      ]
    
    if {[keylget igmpQuerierStatus status] != $::SUCCESS} {
	puts "\nError GetIgmpQuerierAggregatedStatsNgpfHlt: $igmpQuerierStatus\n"
	return 1
    }
    return $igmpQuerierStatus
}


proc GetIgmpQuerierLearnedInfoNgpfHlt { igmpQuerierHandle } {
    #Querier Learned Info: /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:1 = {learned_info {{{"IGMP Querier" "1/1/2" "Interface-IP - 100.1.0.1"} {{id {"IGMP Querier" "1/1/2" "Interface-IP - 100.1.0.1"}} {{Querier Working Version} {v2 v2 v2 v2 v2}} {{Elected Querier Address} {100.1.0.1 100.1.0.1 100.1.0.1 100.1.0.1 100.1.0.1}} {{Group Address} {228.0.0.2 228.0.0.1 228.0.0.4 228.0.0.3 228.0.0.5}} {{Group Timer (sec)} {259 259 259 259 259}} {{Filter Mode} {N/A N/A N/A N/A N/A}} {{Compatibility Mode} {v2 v2 v2 v2 v2}} {{Compatibility Timer (sec)} {0 0 0 0 0}} {{Source Address} {removePacket[N/A] removePacket[N/A] removePacket[N/A] removePacket[N/A] removePacket[N/A]}} {{Source Timer (sec)} {0 0 0 0 0}}}}}}	

    puts "\nGetIgmpQuerierLearnedInfoHlt: Retrieving IGMP Querier learned information"
    set igmpQuerierStatus [::ixiangpf::emulation_igmp_info \
			       -mode        learned_info \
			       -handle      $igmpQuerierHandle \
			       -type        querier \
			      ]
    
    if {[keylget igmpQuerierStatus status] != $::SUCCESS} {
	puts "\nError GetIgmpQuerierLearnedInfoHlt: $igmpQuerierStatus\n"
	return 1
    }
    return $igmpQuerierStatus
}


proc CreateIgmpGroupAddrNgpfHlt { igmpGroupParams } {
    # Creating IGMP IP group addresses

    upvar $igmpGroupParams params
    
    puts "\nCreateIgmpGroupAddr ..."
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }
    
    set igmpGroupIpStatus [eval ::ixiangpf::emulation_multicast_group_config $paramList]
    
    if {[keylget igmpGroupIpStatus status] != $::SUCCESS} {
	puts "\nError CreateIgmpGroupAddr: $igmpGroupIpStatus\n"
	return 1
    }
    return $igmpGroupIpStatus
}

proc CreateIgmpSourceGroupAddrNgpfHlt { igmpSrcGroupAddrParams } {
    upvar $igmpSrcGroupAddrParams params

    puts "\nCreateIgmpSourceGroupAddr ..."
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    set igmpSourceAddrStatus [eval ::ixiangpf::emulation_multicast_source_config $paramList]
    
    if {[keylget igmpSourceAddrStatus status] != $::SUCCESS} {
	puts "\nError CreateIgmpSourceGroupAddr: $igmpSourceAddrStatus\n"
	return 1
    }
    return $igmpSourceAddrStatus
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

proc GetNgpfHltHandles { {deviceGroup ""} {deviceGroupStack ""} } {

    # deviceGroup = Device Group Handle
    #
    # If no parameter values are given, then return all Topology Group handles.
    #
    # If $deviceGroup == "all" && deviceGroupStack == "":
    #     Return all top level Device Group handles.
    #
    # If $deviceGroup != "all" (User needs to provide the Device Group Handle)
    #     && $deviceGroupStack == "ethernet|vlan|ipv4/ipv6" (User needs to select one)
    #        Return all the specific handles: ethernet|vlan|ipv4|ipv6
    # 
    # 
    
    # Default to returning all Topology Groups only
    if {$deviceGroup == "" && $deviceGroupStack == ""} {
	# Topology Group handles: ::ixNet::OBJ-/topology:1
	set topologyHandleList {}
	foreach topology [ixNet getList [ixNet getRoot] topology] {
	    if {[regexp "::ixNet::OBJ-(/topology:\[0-9]+)" $topology - handle]} {
		lappend topologyHandleList $handle
	    }
	}
	return $topologyHandleList
    }
    
    if {$deviceGroup == "all" && $deviceGroupStack == ""} {
	# Top level Device Group handles: /topology:1/deviceGroup:1
	set deviceGroupHandles {}
	foreach topology [ixNet getList [ixNet getRoot] topology] {
	    foreach deviceGroup [ixNet getList $topology deviceGroup] {
		if {[regexp "::ixNet::OBJ-(/topology:\[0-9]+/deviceGroup:\[0-9]+)" $deviceGroup - deviceGroupHandle]} {
		    lappend deviceGroupHandles $deviceGroupHandle
		}
	    }
	}
	return $deviceGroupHandles
    }

    if {$deviceGroup != "all" && $deviceGroupStack != ""} {
	# User needs to provide the device Group handle and
	# provide which device group stack to get; ethernet/vlan/ipv4/ipv6
	
	# Device Group handle needs to look like one of the following two:
	# ::ixNet::OBJ-/topology:1/deviceGroup:1
	# /topology:1/deviceGroup:1
	# /topology:1/deviceGroup:1/ethernet:1
	if {[regexp "^/topology:\[0-9]+/deviceGroup:\[0-9]+.*" $deviceGroup]} {
	    # Need to prepend ::ixNet::OBJ- in front if it isn't there
	    set deviceGroup "::ixNet::OBJ-$deviceGroup"
	}
	
	# It is assuming user is providing a handle that looks like this: /topology:1/deviceGroup:1
	if {[regexp -nocase "ethernet" $deviceGroupStack]} {
	    set ethernetStackList {}
	    foreach ethernetStack [ixNet getList $deviceGroup ethernet] {
		lappend ethernetStackList $ethernetStack
	    }
	    return $ethernetStackList
	}
	
	# If user wants the vlan handle, user can provide two different Device Group handles:
	# /topology:1/deviceGroup:1/
	# /topology:1/deviceGroup:1/ethernet:1
	if {[regexp -nocase "vlan" $deviceGroupStack]} {
	    set vlanStackList {}
	    if {[regexp "ethernet:\[0-9]+" $deviceGroupStack] == 0} {
		foreach ethernetStack [ixNet getList $deviceGroup ethernet] {
		    foreach vlanStack [ixNet getList $ethernetStack vlan] {
			lappend vlanStackList $vlanStack
		    }
		}
		return $vlanStackList
	    }
	    
	    # See if user passed in a Device Group handle with ethernet or not
	    if {[regexp "ethernet:\[0-9]+" $deviceGroupStack] == 1} {
		foreach vlanStack [ixNet getList $ethernetStack vlan] {
		    lappend vlanStackList $vlanStack
		}
		return $vlanStackList
	    }
	}
	
	if {[regexp -nocase "ipv4" $deviceGroupStack]} {
	    # Returning: /topology:1/deviceGroup:1/ethernet:1/ipv4:1
	    set ipv4StackList {}
	    if {[regexp "ethernet:\[0-9]+" $deviceGroupStack] == 0} {
		foreach ethernetStack [ixNet getList $deviceGroup ethernet] {
		    foreach ipv4Stack [ixNet getList $ethernetStack ipv4] {
			lappend ipv4StackList $ipv4Stack
		    }
		}
		return $ipv4StackList
	    }
	    
	    # See if user passed in a Device Group handle with ethernet or not
	    if {[regexp "ethernet:\[0-9]+" $deviceGroupStack] == 1} {
		foreach ipv4Stack [ixNet getList $ethernetStack ipv4] {
		    lappend ipv4StackList $ipv4Stack
		}
		return $ipv4StackList
	    }
	}
	
	if {[regexp -nocase "ipv6" $deviceGroupStack]} {
	    # /topology:1/deviceGroup:1/ethernet:1/ipv6:1
	    set ipv6StackList {}
	    if {[regexp "ethernet:\[0-9]+" $deviceGroupStack] == 0} {
		foreach ethernetStack [ixNet getList $deviceGroup ethernet] {
		    foreach ipv6Stack [ixNet getList $ethernetStack ipv6] {
			lappend ipv6StackList $ipv6Stack
		    }
		}
		return $ipv6StackList
	    }
	    
	    # See if user passed in a Device Group handle with ethernet or not
	    if {[regexp "ethernet:\[0-9]+" $deviceGroupStack] == 1} {
		foreach ipv6Stack [ixNet getList $ethernetStack ipv6] {
		    lappend ipv6StackList $ipv6Stack
		}
		return $ipv6StackList
	    }
	}
    }
}

proc GetTopologyGroupHandle { topologyGroupNumber } {
    foreach topologyHandle [ixNet getList [ixNet getRoot] topology] {
	if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber" $topologyHandle]} {
	    return $topoHandle
	}
    }
    return 0
}

proc GetDeviceGroupHandle { args } {
    # -topologyGroupNumber <number>
    # -deviceGroupNumber <number>

    if {[lsearch $args "-topologyGroupNumber"] == -1} {
	puts "\nGetDeviceGroupHandle: Requires parameter -topologyGroupNumber"
	exit
    }
    if {[lsearch $args "-deviceGroupNumber"] == -1} {
	puts "\nGetDeviceGroupHandle: Requires parameter -deviceGroupNumber"
	exit
    }

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -topologyGroupNumber {
		set topologyGroupNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -deviceGroupNumber {
		set deviceGroupNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "\nNo such parameter: $currentArg"
	    }
	}
    }

    foreach topologyGroup [ixNet getList [ixNet getRoot] topology] {
	if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber" $topologyGroup]} {
	    foreach deviceGroup [ixNet getList $topologyGroup deviceGroup] {
		if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber" $deviceGroup]} {
		    return $deviceGroup
		}
	    }
	}
    }
    return 0
}


proc GetEthernetHandleNgpf { args } {
    # -topologyGroupNumber <number>
    # -deviceGroupNumber <number>
    # -ethernetNumber <number>

    if {[lsearch $args "-topologyGroupNumber"] == -1} {
	puts "\nGetEthernetHandleNgpf: Requires parameter -topologyGroupNumber"
	exit
    }
    if {[lsearch $args "-deviceGroupNumber"] == -1} {
	puts "\nGetEthernetHandleNgpf: Requires parameter -deviceGroupNumber"
	exit
    }
    if {[lsearch $args "-ethernetNumber"] == -1} {
	puts "\nGetEthernetHandleNgpf: Requires parameter -ethernetNumber"
	exit
    }

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -topologyGroupNumber {
		set topologyGroupNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -deviceGroupNumber {
		set deviceGroupNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ethernetNumber {
		set ethernetNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "\nNo such parameter: $currentArg"
	    }
	}
    }

    foreach topologyGroup [ixNet getList [ixNet getRoot] topology] {
       	if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber" $topologyHandle]} {
	    foreach deviceGroup [ixNet getList $topologyGroup deviceGroup] {
		if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber" $deviceGroup]} {
		    foreach ethernetHandle [ixNet getList $deviceGroup ethernet] {
			if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber/ethernet:$ethernetNumber" $ethernetHandle]} {
			    return $ethernetHandle
			}
		    }
		}
	    }
	}
    }
    return 0
}

proc GetIpv4HandleNgpf { args } {
    # -topologyGroupNumber <number>
    # -deviceGroupNumber <number>
    # -ethernetNumber <number>
    # -ipv4Number <number>

    if {[lsearch $args "-topologyGroupNumber"] == -1} {
	puts "\nGetIpv4HandleNgpf: Requires parameter -topologyGroupNumber"
	exit
    }
    if {[lsearch $args "-deviceGroupNumber"] == -1} {
	puts "\nGetIpv4HandleNgpf: Requires parameter -deviceGroupNumber"
	exit
    }
    if {[lsearch $args "-ethernetNumber"] == -1} {
	puts "\nGetIpv4HandleNgpf: Requires parameter -ethernetNumber"
	exit
    }
    if {[lsearch $args "-ipv4Number"] == -1} {
	puts "\nGetIpv4HandleNgpf: Requires parameter -ipv4Number"
	exit
    }

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -topologyGroupNumber {
		set topologyGroupNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -deviceGroupNumber {
		set deviceGroupNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ethernetNumber {
		set ethernetNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ipv4Number {
		set ipv4Number [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "\nNo such parameter: $currentArg"
	    }
	}
    }

    foreach topologyHandle [ixNet getList [ixNet getRoot] topology] {
       	if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber" $topologyHandle]} {
	    foreach deviceGroupHandle [ixNet getList $topologyHandle deviceGroup] {
		if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber" $deviceGroupHandle]} {
		    foreach ethernetHandle [ixNet getList $deviceGroupHandle ethernet] {
			if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber/ethernet:$ethernetNumber" $ethernetHandle]} {
			    foreach ipv4Handle [ixNet getList $ethernetHandle ipv4] {
				if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber/ethernet:$ethernetNumber/ipv4:$ipv4Number" $ipv4Handle]} {
				    return $ipv4Handle
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

proc GetOspfHandleNgpf { args } {
    # -topologyGroupNumber <number>
    # -deviceGroupNumber <number>
    # -ethernetNumber <number>
    # -ipv4Number <number>
    # -ospfNumber <number>

    if {[lsearch $args "-topologyGroupNumber"] == -1} {
	puts "\nGetOspfHandleNgpf: Requires parameter -topologyGroupNumber"
	exit
    }
    if {[lsearch $args "-deviceGroupNumber"] == -1} {
	puts "\nGetOspfHandleNgpf: Requires parameter -deviceGroupNumber"
	exit
    }
    if {[lsearch $args "-ethernetNumber"] == -1} {
	puts "\nGetOspfHandleNgpf: Requires parameter -ethernetNumber"
	exit
    }
    if {[lsearch $args "-ipv4Number"] == -1} {
	puts "\nGetOspfHandleNgpf: Requires parameter -ipv4Number"
	exit
    }
    if {[lsearch $args "-ospfNumber"] == -1} {
	puts "\nGetOspfHandleNgpf: Requires parameter -ospfNumber"
	exit
    }

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -topologyGroupNumber {
		set topologyGroupNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -deviceGroupNumber {
		set deviceGroupNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ethernetNumber {
		set ethernetNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ipv4Number {
		set ipv4Number [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ospfNumber {
		set ospfNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "\nNo such parameter: $currentArg"
	    }
	}
    }

    foreach topologyHandle [ixNet getList [ixNet getRoot] topology] {
       	if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber" $topologyHandle]} {
	    foreach deviceGroupHandle [ixNet getList $topologyHandle deviceGroup] {
		if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber" $deviceGroupHandle]} {
		    foreach ethernetHandle [ixNet getList $deviceGroupHandle ethernet] {
			if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber/ethernet:$ethernetNumber" $ethernetHandle]} {
			    foreach ipv4Handle [ixNet getList $ethernetHandle ipv4] {
				if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber/ethernet:$ethernetNumber/ipv4:$ipv4Number" $ipv4Handle]} {
				    foreach ospfHandle [ixNet getList $ipv4Handle ospfv2] {
					if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber/ethernet:$ethernetNumber/ipv4:$ipv4Number/ospfv2:$ospfNumber" $ospfHandle]} {	
					    return $ospfHandle
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

proc GetBgpHandleNgpf { args } {
    # -topologyGroupNumber <number>
    # -deviceGroupNumber <number>
    # -ethernetNumber <number>
    # -ipv4Number <number>
    # -bgpNumber <number>

    if {[lsearch $args "-topologyGroupNumber"] == -1} {
	puts "\nGetBgpHandleNgpf: Requires parameter -topologyGroupNumber"
	exit
    }
    if {[lsearch $args "-deviceGroupNumber"] == -1} {
	puts "\nGetBgpHandleNgpf: Requires parameter -deviceGroupNumber"
	exit
    }
    if {[lsearch $args "-ethernetNumber"] == -1} {
	puts "\nGetBgpHandleNgpf: Requires parameter -ethernetNumber"
	exit
    }
    if {[lsearch $args "-ipv4Number"] == -1} {
	puts "\nGetBgpHandleNgpf: Requires parameter -ipv4Number"
	exit
    }
    if {[lsearch $args "-bgpNumber"] == -1} {
	puts "\nGetBgpHandleNgpf: Requires parameter -bgpNumber"
	exit
    }

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -topologyGroupNumber {
		set topologyGroupNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -deviceGroupNumber {
		set deviceGroupNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ethernetNumber {
		set ethernetNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ipv4Number {
		set ipv4Number [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -bgpNumber {
		set bgpNumber [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		puts "\nNo such parameter: $currentArg"
	    }
	}
    }

    foreach topologyHandle [ixNet getList [ixNet getRoot] topology] {
       	if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber" $topologyHandle]} {
	    foreach deviceGroupHandle [ixNet getList $topologyHandle deviceGroup] {
		if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber" $deviceGroupHandle]} {
		    foreach ethernetHandle [ixNet getList $deviceGroupHandle ethernet] {
			if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber/ethernet:$ethernetNumber" $ethernetHandle]} {
			    foreach ipv4Handle [ixNet getList $ethernetHandle ipv4] {
				if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber/ethernet:$ethernetNumber/ipv4:$ipv4Number" $ipv4Handle]} {
				    foreach bgpHandle [ixNet getList $ipv4Handle bgpIpv4Peer] {
					if {[regexp "::ixNet::OBJ-/topology:$topologyGroupNumber/deviceGroup:$deviceGroupNumber/ethernet:$ethernetNumber/ipv4:$ipv4Number/bgpIpv4Peer:$bgpNumber" $bgpHandle]} {	
					    return $bgpHandle
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

proc CheckTrafficStateHlt {} {
    # If stopped key is 1 - means stopped
    # 0 - means started.
    
    puts "\nCheckTrafficStatHlt .."
    set pollStatus [ixia::traffic_control -action poll]
    set stoppedFlag [keylget pollStatus stopped]
    return $stoppedFlag
}

proc CheckTraffic { state {endTime 20} } {
    # startedWaitingForStats, startedWaitingForStreams, started, stopped, stoppedWaitingForStats, txStopWatchExpected, locked, unapplied

    set flag 0
    set stopTimer $endTime
    for {set timer 1} {$timer <= $stopTimer} {incr timer} {
	if {[CheckTrafficState] != $state} {
	    puts "\nCheckTraffic: Traffic state is not $state. Wait $timer/$stopTimer seconds"
	    after 1000
	}
	if {[CheckTrafficState] == $state} {
	    set flag 1
	    break
	}
    }
    if {$flag == 1} {
	return 0
    } else {
	return 1
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
	    puts "VerifyTrafficState: Traffic Started"
	    break
	}

	if {$trafficState == "stopped"} {
	    puts "VerifyTrafficState: Traffic stopped"
	    break
	}

	if {$trafficState == "startedWaitingForStats" || $trafficState == "stoppedWaitingForStats"} {
	    puts "VerifyTrafficState: Traffic started. Waiting for stats to complete"
	    break
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

proc ConfigPacketCapturePortHlt { port {dataPlane "dataPlane"} {controlPlane "noControlPlane"} } {
    # $port = 1/1/3.  Not 1/3.
    # dataPlane options:  dataPlane or noDataPlane
    # controlPlane options: controlPlane or noControlPlane

    if {$dataPlane == "dataPlane"} {
	set dataPlane 1
    } else {
	set dataPlane 0
    }

    if {$controlPlane == "controlPlane"} {
	set controlPlane 1
    } else {
	set controlPlane 0
    }
    
    puts "\nConfigPacketCapturePort"
    set status [::ixia::packet_config_buffers  \
		    -port_handle $port \
		    -data_plane_capture_enable $dataPlane \
		    -control_plane_capture_enable $controlPlane \
		    -slice_size 0 \
		    -trigger_position 1 \
		    -capture_mode trigger \
		    -after_trigger_filter filter \
		    -before_trigger_filter none \
		    -continuous_filter filter \
		   ]
    if {[keylget status status] != $::SUCCESS} {
	puts "\nError ConfigPacketCapturePort: $status\n"
	return 1
    } else {
	puts "\nConfigPacketCapturePort: Successfully configured packet capturing on port $port."
    }

    after 5000
    puts "ConfigPacketCapturePort: Applying traffic ..."
    ixNet exec apply [ixNet getRoot]/traffic
    after 2000
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


proc StartPacketCaptureHlt { port } {
    # Must use low level API to start traffic. HLT doesn't work.
    # Enhancement is filed.

    puts "StartPacketCaptureHlt ..."
    set startStatus [::ixia::packet_control \
			 -port_handle $port \
			 -action      start \
			]
    if {[keylget startStatus status] != $::SUCCESS} {
	puts "\nError StartPacketCaptureHlt: $startStatus\n"
	return 1
    }
    after 10000
    return 0
}

proc StopPacketCaptureHlt { port } {
    puts "StopPacketCaptureHlt ..."
    set stopStatus [::ixia::packet_control \
			-port_handle $port\
			-action      stop \
		       ]
    if {[keylget stopStatus status] != $::SUCCESS} {
	puts "\nError StopPacketCaptureHlt: $stopStatus\n"
	return 1
    }
    return 0
}

proc GetPacketCaptureCsvFileHlt { port localDirectory {stopTime 300} } {
    # $port = 1/1/2.  Not 1/2.
    # $directory is the local Linux path to save the csv file at. 
    # For example: /home/hgee/IxiaScripts

    # Return: The path + filename of the csv file of the packet capture.

    puts "\nGetPacketCaptureCsvFile: Generate a CSV format packet capture file..."

    set flag 0
    for {set counter 1} {$counter <= $stopTime} {incr counter} {
	if {$flag == 0 && $counter < $stopTime} {	    
	    set statStatus [::ixia::packet_stats   \
				-port_handle $port  \
				-format csv \
				-dirname $localDirectory \
			       ]
	    if {[keylget statStatus status] != $::SUCCESS} {
		puts "\nGetPacketCaptureCsvFile: IxNetwork is still processing all the buffered captured packets."
		puts "Not ready yet. Retrying $counter/$stopTime seconds"
		after 1000
		continue
	    } else {
		set flag 1
	    }
	}
	if {$flag == 1 && $counter < $stopTime} {
	    puts "\nGetPacketCaptureCsvFile: Successfully generated a csv packet capture file."
	    return $statStatus
	    break
	}
	if {$flag == 0 && $counter == $stopTime} {
	    puts "\nError GetPacketCaptureCsvFile: It has been $stopTime seconds and IxNetwork packet capture didn't have enough time to generate the csv file. Please run test again and watch the IxNetwok gui to verify the amount of time for the \"Packets\" to finish processing your traffic load."
	    return 1
	}
    }
}

proc CloseAllCapturedDatas {} {
    ixNet exec closeAllTabs
}

proc ConfigBgpEmulationHlt { portConfigParams {platform legacy} } {
    upvar $portConfigParams params
    
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    if {$platform == "ngpf"} {
	puts "\nConfigBgpEmulationHlt: ngpf ...\n"
	set bgpConfigStatus [eval ::ixiangpf::emulation_bgp_config $paramList]
    }

    if {$platform == "legacy"} {
	puts "\nConfigBgpEmulationHlt: legacy ..."
	set bgpConfigStatus [eval ::ixia::emulation_bgp_config $paramList]
    }

    if {[keylget bgpConfigStatus status] != $::SUCCESS} {
	puts "\nError: ConfigBgpEmulationHlt: [keylget bgpConfigStatus log]"
	return 1
    }

    return $bgpConfigStatus
}

proc ConfigNetworkGroupNgpfHlt { portConfigParams } {
    upvar $portConfigParams params

    puts "\nConfigNetworkGroupNgpfHlt: Configuring Network Group ..."
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    set network_group_status [eval ::ixiangpf::network_group_config $paramList]
    if {[keylget network_group_status status] != "1"} {
	puts "\nError ConfigNetworkGroupNgpfHlt: $network_group_status\n"
	return 1
    }

    return $network_group_status

}

proc ConfigIsisNetworkGroupNgpfHlt { portConfigParams } {
    upvar $portConfigParams params

    puts "\nConfigIsisNetworkGroupNgpfHlt: Configuring Network Group ..."
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    set network_group_status [eval ::ixiangpf::emulation_isis_network_group_config $paramList]
    if {[keylget network_group_status status] != "1"} {
	puts "\nError ConfigIsisNetworkGroupNgpfHlt: $network_group_status\n"
	return 1
    }

    return $network_group_status

}

proc ConfigBgpRouteEmulationNgpfHlt { portConfigParams {platform legacy} } {
    # /vport/protocols/bgp/neighborRange:#

    upvar $portConfigParams params

    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    if {$platform == "ngpf"} {
	set portHandleIndex [lsearch $paramList -handle]
	set bgpNeighborNumber [lindex $paramList [expr $portHandleIndex + 1]]
	
	puts "\nConfigBgpRouteEmulationHlt: $bgpNeighborNumber ..."
	set bgpRouteConfigStatus [eval ::ixiangpf::emulation_bgp_route_config $paramList]
	
	if {[keylget bgpRouteConfigStatus status] != $::SUCCESS} {
	    puts "\nError ConfigBgpRouteEmulationHlt: [keylget bgpRouteConfigStatus log]"
	    return 1
	}
    }

    if {$platform == "legacy"} {
	set portHandleIndex [lsearch $paramList -handle]
	set bgpNeighborNumber [lindex $paramList [expr $portHandleIndex + 1]]
	
	puts "\nConfigBgpRouteEmulationHlt: $bgpNeighborNumber ..."
	set bgpRouteConfigStatus [eval ::ixia::emulation_bgp_route_config $paramList]
	
	if {[keylget bgpRouteConfigStatus status] != $::SUCCESS} {
	    puts "\nError ConfigBgpRouteEmulationHlt: [keylget bgpRouteConfigStatus log]"
	    return 1
	}
    }

    return 0
}

proc StartBgpEmulationHlt { port } {
    # port format = 1/1/2.  Not 1/2

    puts "\nStartBgpEmulationHlt: $port ..."
    set bgpContolStatus [::ixia::emulation_bgp_control \
			     -port_handle    $port \
			     -mode           start \
			    ]
    if {[keylget bgpControlStatus status] != $::SUCCESS} {
	puts "\nError StartBgpEmulationHlt: Failed to start BGP CE emulation on $port:\n$bgpControlStatus"
	return 1
    }
    return 0
}

proc StopBgpEmulationHlt { port } {
    # port format = 1/1/2.  Not 1/2

    puts "\nStopBgpEmulationHlt: $port ..."
    set bgpContolStatus [::ixia::emulation_bgp_control \
			     -port_handle    $port \
			     -mode           start \
			    ]
    if {[keylget bgpControlStatus status] != $::SUCCESS} {
	puts "\nError StopBgpEmulationHlt: Failed to start BGP CE emulation on $port:\n[keylget bgpControlSatus log]"
	return 1
    }
    return 0
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

proc GetVportConnectedToPort { vport } {
    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
    set connectedTo [ixNet getAttribute $vport -connectedTo]
    set connectedTo [lrange [split $connectedTo /] 3 4]
    set card [lindex [split [lindex $connectedTo 0] :] end]
    set port [lindex [split [lindex $connectedTo 1] :] end]
    return $card/$port    
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

proc ApplyTrafficHlt {} {
    set cmd_status [::ixia::traffic_control -action apply]
}

proc ApplyTrafficNgpfHlt {} {
    set cmd_status [::ixiangpf::traffic_control -action apply]
}

proc ConfigMultivalueNgpfHlt { pattern topologyHandle counterDirection counterStart counterStep nestStep nestEnabled } {
    # pattern = counter
    # nest_owner = topology handle

    puts "\nConfigMultivalueNgpfHlt: $topologyHandle"
    set status [::ixiangpf::multivalue_config \
		    -pattern $pattern \
		    -nest_owner $topologyHandle \
		    -counter_direction $counterDirection \
		    -counter_start $counterStart \
		    -counter_step $counterStep \
		    -nest_step $nestStep \
		    -nest_enabled $nestEnabled \
		   ]
    return [keylget status multivalue_handle]
}

proc ConfigNgpfMultiValueHlt { multiValueParams } {
    upvar $multiValueParams param

    foreach {properties values} [array get param *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }
    
    puts "\nConfigNgpfMultiValueHlt"
    set multiValueStatus [eval ::ixiangpf::multivalue_config $paramList]

    if {[keylget multiValueStatus status] != $::SUCCESS} {
	puts "\nError ConfigNgpfMultiValueHlt: $multiValueStatus\n"
	return 1
    }

    return $multiValueStatus
}

proc ConfigOspfEmulationNgpfHlt { portConfigParams } {
    upvar $portConfigParams ospfParams

    #puts "[parray ospfParams]"
    puts "\nConfigOspfEmulationNgpf ..."
    foreach {properties values} [array get ospfParams *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    set ospfConfigStatus [eval ::ixiangpf::emulation_ospf_config $paramList]

    if {[keylget ospfConfigStatus status] != $::SUCCESS} {
	puts "\nError ConfigOspfEmulationNgpf: $ospfConfigStatus\n"
	return 1
    }
    
    return $ospfConfigStatus
}

proc StartOspfProtocolNgpfHlt { topologyHandle } {
    puts "StartOspfProtocolNgpfHlt: $topologyHandle ..."
    set status [::ixiangpf::emulation_ospf_control \
		    -handle $topologyHandle \
		    -mode start \
		   ]
    if {[keylget status status] != $::SUCCESS} {
	puts "Error StartOspfProtocolNgpfHlt: $status\n"
	return 1
    }
    return 0
}

proc StartOspfProtocolNgpf { ospfHandle } {
    puts "\nStartOspfProtocolNgpf: $ospfHandle"
    ixNet execute start $ospfHandle
}

proc StopOspfProtocolNgpfHlt { topologyHandle } {
    puts "StopOspfProtocolNgpfHlt: $topologyHandle ..."
    set status [::ixiangpf::emulation_ospf_control \
		    -handle $topologyHandle \
		    -mode stop \
		   ]
    if {[keylget status status] != $::SUCCESS} {
	puts "\nError StartOspfProtocolNgpfHlt: $status\n"
	return 1
    }
    return 0
}

proc StopOspfProtocolNgpf { ospfHandle } {
    puts "\nStopOspfProtocolNgpf: $ospfHandle"
    ixNet execute stop $ospfHandle
}

proc GetOspfAggregatedStatsNgpfHlt { ospfEmulationHandle} {
    # ospfEmulationHandle: 
    #     # $ixnHLT(HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>/ospfv2:<1>)

    puts "\nGetOspfAggregatedStatsNgpfHlt ..."
    set ospfStats [::ixiangpf::emulation_ospf_info \
		       -handle $ospfEmulationHandle \
		       -mode aggregate_stats \
		      ]
    if {[keylget ospfStats status] != $::SUCCESS} {
	puts "\nError GetOspfAggregatedStatsNgpfHlt: $ospfStats"
	return 1
    }
    
    return $ospfStats
}

proc GetOspfLearnedInfoStatsNgpfHlt { ospfEmulationHandle} {
    # ospfEmulationHandle: 
    #     # $ixnHLT(HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>/ospfv2:<1>)

    puts "\nGetOspfLearnedInfoStatsNgpfHlt ..."
    set ospfStats [::ixiangpf::emulation_ospf_info \
		       -handle $ospfEmulationHandle \
		       -mode learned_info \
		      ]
    if {[keylget ospfStats status] != $::SUCCESS} {
	puts "\nError GetOspfLearnedInfoStatsNgpfHlt: $ospfStats"
	return 1
    }
    
    return $ospfStats
}

proc ConfigOspfNetworkGroupNgpfHlt { ospfNetworkGroupParams } {
    upvar $ospfNetworkGroupParams params

    puts "\nConfigOspfNetworkGroupNgpfHlt ..."
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
	puts "ConfigOspfNetworkGroupNgpf: $properties  :  $values"
    }
    
    set ospfNetworkGroupStatus [eval ::ixiangpf::emulation_ospf_network_group_config $paramList]

    if {[keylget ospfNetworkGroupStatus status] != $::SUCCESS} {
	puts "\nError ConfigOspfNetworkGroupNgpfHlt: $ospfNetworkGroupStatus\n"
	return 1
    }
    puts "\nConfigOspfNetworkGroupNgpfHlt: $ospfNetworkGroupStatus\n"

    return $ospfNetworkGroupStatus
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

proc DeleteTrafficItemHlt { stream_id } {

    puts "\nDeleteTrafficItemHlt ..."
    set trafficItemStatus [::ixia::traffic_config -mode remove -stream_id $stream_id]

    # Check status of delete process
    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError DeleteTrafficItemHlt: $trafficItemStatus\n"
	return 1
    }

    return $trafficItemStatus
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

# BuildEgressView
# Builds a statitics view in IxNetwork, which displays all egress stats
# @Example:
#	Tcl: 	BuildEgressView
#			BuildEgressView "My View Stats"
# @PARAMS:
#	viewName		-	[optional] The name of the view that will be created
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

proc LinkUpDownHlt {port state} {

    puts "\nLinkUpDown: Set port($port) status to $state"

    set vport [::ixia::convert_porthandle_to_vport $port]
    set output [ixNet exec linkUpDn $vport $state]

    after 2000
    #TODO: Add error handling to check state of port after it has been changed

    if {$output == "::ixNet::OK"} {
	puts "\tPort($port) is $state"
	return 0
    } else {
	puts "\tError LinkUpDown: Port's status did no change"
	return 1
    }
}


proc getTrafficWarnings { {trafficItems ""} } {
    # Return the list of traffic item warnings

    set warningList {}

    if {$trafficItems == ""} {
	set trafficItems [::ixTclNet::GetTrafficItemList]
    }

    foreach item $trafficItems {
	if {[ixNet getAttribute $item -warnings] != ""} {
	    set warningList "$warningList\n\tWarning: [ixNet getAttribute $item -name] - [ixNet getAttribute $item -warnings]"
	}
    }

    if {$warningList != ""} {
	return $warningList
    }
}


proc getTrafficErrors { {trafficItems ""} } {
    # Return the list of traffic item errors
    set errorList {}

    if {$trafficItems == ""} {
	set trafficItems [::ixTclNet::GetTrafficItemList]
    }

    foreach item $trafficItems {
	if {[ixNet getAttribute $item -errors] != ""} {
	    set errorList "$errorList\n\tError: [ixNet getAttribute $item -name] - [ixNet getAttribute $item -errors]"
	}
    }

    if {$errorList != ""} {
	return $errorList
    } else {
	return 0
    }
}

# Modifying multi-value 
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

proc ConfigVxlanEmulationNgpfHlt { port portConfigParams} {
    upvar $portConfigParams params

    puts "\nPortVxlanEmulation: $port"
    foreach {properties values} [array get params $port,*] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    set status [eval ::ixiangpf::emulation_vxlan_config $paramList]

    if {[keylget status status] != $::SUCCESS} {
	puts "\nError ConfigVxlanEmulation:\n$status\n"
	return 1
    }

    # /topology:1/deviceGroup:1/ethernet:1/ipv4:1/vxlan:1
    set vxlanHandle [keylget status vxlan_handle]

    return $vxlanHandle
}

proc GetVxLanProtocolStatsNgpfHlt { port } {
    # port format = 1/8/3 (Not 8/3)
    # Returns:
    #
    # status: 1
    # 1/8/4:
    #   aggregate:
    #    port_name: 1/8/4
    #    bytes_tx: 378
    #    bytes_rx: 420
    #    packets_tx: 9
    #    packets_rx: 10
    #    sessions_up: 2
    #    sessions_down: 0
    #    sessions_not_started: 0
    #    sessions_total: 2
    
    puts "\nGetVxLanProtocolStatsHlt: $port"
    set vxlanStats [::ixiangpf::emulation_vxlan_stats \
			-port_handle $port \
			-mode aggregate_stats \
			-execution_timeout  30 \
		       ]
    if {[keylget vxlanStats status] != $::SUCCESS} {
	puts "\nGetVxLanProtocolStatsHlt failed: [keylget vxlanStats log]\n"
    }
    return $vxlanStats
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

proc disconnectHlt {} {
    ixia::cleanup_session
}

proc disconnectNgpfHlt {} {
    ixia_ngpf::cleanup_session
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

proc ConfigLacpNgpfHlt { ethernetHandle } {
    # ethernetHandle: /topology:2/deviceGroup:1/ethernet:1
    set lacpStatus [::ixiangpf::emulation_lacp_link_config \
			-mode create \
			-handle $ethernetHandle \
			-active 1 \
			-session_type lacp \
			-actor_key 1 \
			-actor_port_num 1 \
			-actor_key_step 0 \
			-actor_port_num_step 0 \
			-actor_port_pri 1 \
			-actor_port_pri_step 0 \
			-actor_system_id 00:00:00:00:00:01 \
			-administrative_key 1 \
			-actor_system_id_step 00:00:00:00:00:00 \
			-collecting_flag 1 \
			-distributing_flag 1 \
			-collector_max_delay 0 \
			-inter_marker_pdu_delay  6 \
			-lacp_activity active \
			-lacp_timeout 0 \
			-lacpdu_periodic_time_interval 0 \
			-marker_req_mode fixed \
			-marker_res_wait_time 5 \
			-send_marker_req_on_lag_change 1 \
			-inter_marker_pdu_delay_random_min 1 \
			-inter_marker_pdu_delay_random_max 6 \
			-send_periodic_marker_req 0 \
			-support_responding_to_marker 1 \
			-sync_flag 1 \
			-aggregation_flag 1 \
		       ]
    if {[keylget lacpStatus status] != $::SUCCESS} {
	puts "\nConfigLacpNgpfHlt: Error: $lappStatus"
	return 1
    }
    return [keylget lacpStatus lacp_handle]
}

proc ConfigIsIsNgpfHlt { isisParams } {
    upvar $isisParams params

    puts "\nConfigIsIsNgpfHlt"
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    set isisStatus [eval ::ixiangpf::emulation_isis_config $paramList]

    if {[keylget isisStatus status] != $::SUCCESS} {
	puts "\nError ConfigIsIsNgpfHlt:\n$isisStatus\n"
	return 1
    }
    return [keylget isisStatus isis_l3_handle]
}

proc VerifyProtocolSessionStatusUpNgpfHlt { protocolHandle {totalTime 60}} {
    # protocolHandle: Ethernet handle, IPv4 handle, OSPF handle, etc
    #    IPv4 handle sample: /topology:1/deviceGroup:1/ethernet:1/ipv4:1
    #    OSPF handle sample: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1
   
    for {set timer 1} {$timer <= $totalTime} {incr timer} {
	set sessionStatus [ixiangpf::protocol_info \
			       -handle $protocolHandle \
			       -mode "aggregate" \
			      ]
	set currentSessionUp [keylget sessionStatus $protocolHandle.aggregate.sessions_up]
	set totalSessions    [keylget sessionStatus $protocolHandle.aggregate.sessions_total]
	
	puts "\n$protocolHandle"
	puts "\t$timer/$totalTime\secs: CurrentSessionUp:$currentSessionUp   TotalSessions:$totalSessions"
	
	if {$timer < $totalTime && $currentSessionUp != $totalSessions} {
	    after 1000
	    continue
	}
	if {$timer < $totalTime && $currentSessionUp == $totalSessions} {
	    return 0
	}
	if {$timer == $totalTime && $currentSessionUp != $totalSessions} {
	    puts "\nError: It has been $timer seconds and total sessions are not all UP"
	    return 1
	}
    }
}

proc ModifyTopologyName { topologyHandle topologyName } {
    # topologyHandle example:  ::ixNet::OBJ-/topology:1

    puts "\nModifyTopologyName: $topologyHandle : $topologyName"
    ixNet setAttribute $topologyHandle -name $topologyName
    ixNet commit
}

proc ModifyDeviceGroupName { deviceGroupHandle deviceGroupName } {
    # deviceGroupHandle example:  ::ixNet::OBJ-/topology:1/deviceGroup:1

    puts "\nModifyDeviceGroupName: $deviceGroupHandle : $deviceGroupName"
    ixNet setAttribute $deviceGroupHandle -name $deviceGroupName
    ixNet commit
}

proc RebootCardId { cardId } {
    ixNet execute hwRebootCardByIDs $cardId
}

proc PlaceHolder {} {
}
