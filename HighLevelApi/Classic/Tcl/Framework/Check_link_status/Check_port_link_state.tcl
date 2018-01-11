################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-20-2007 Mchakravarthy - created sample
#
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################
################################################################################
#                                                                              #
# Description:                                                                 #
#   This sample configures checks port link state							   #
#  	 and validates it												           #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
# General script variables
################################################################################
set test_name                                   [info script]
set cfgError									0
set chassis_ip									10.205.16.54
set port_list									[list 2/5 2/6]
set break_locks									1
set tcl_server									127.0.0.1
set ixnetwork_tcl_server						127.0.0.1
set port_count									2
################################################################################
# START - Connect to the chassis
################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect

puts "Starting - $test_name - [clock format [clock seconds]]"
puts "Start connecting to chassis ..."

set connect_status [::ixia::connect                                        	   \
            -reset                                                             \
            -break_locks          $break_locks                                 \
			-vport_count		  $port_count								   \
            -tcl_server           $tcl_server                                  \
            -ixnetwork_tcl_server $ixnetwork_tcl_server                        \
            -interactive          1                                            \
            ]
			
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_handle [list]
set port_handle [keylget connect_status vport_list]

set i 0

puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port    
    incr i
}
puts "End connecting to chassis ..."

################################################################################
# END - Connect to the chassis
################################################################################

################################################################################
# LINK STATUS - Check port link status - unassigned
################################################################################

puts "check port link state desired status - unassigned"
set port_link_status [::ixia::test_control -action check_link_state -port_handle $port_handle -desired_status unassigned]

if {[keylget port_link_status status] != $::SUCCESS} {
	puts "FAIL - $test_name - [keylget port_link_status log]"
	return 0
}

foreach port $port_handle {
	set port_status [keylget port_link_status $port.state]
	if {$port_status != "unassigned"} {
		puts "Error: Port $port doesnt have desired state set"
		incr cfgError
	} else {
		puts "Port $port State : $port_status"
	}
}
	
################################################################################
# RESET - Reset and connect to the chassis
################################################################################

set connect_status [::ixia::connect                                        	   \
            -reset                                                             \
            -port_list            $port_list                                   \
            -device               $chassis_ip                                  \
            -break_locks          $break_locks                                 \
            -tcl_server           $tcl_server                                  \
            -ixnetwork_tcl_server $ixnetwork_tcl_server                        \
            -interactive          1                                            \
            ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set i 0
puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port    
    incr i
}
puts "End connecting to chassis ..."

################################################################################
# END - Connect to the chassis
################################################################################

################################################################################
# START - Interface configuration - Port 0
################################################################################
puts "Start interface configuration for Port:$port_0"

set interface_status_0 [::ixia::interface_config 		\
        -port_handle        		$port_0        		\
		-l23_config_type 			protocol_interface	\
        -intf_ip_addr       		11.1.1.1      		\
        -gateway            		11.1.1.2     		\
        -netmask            		255.255.255.0		\
		-arp_on_linkup 				1					\
        -ns_on_linkup 				1					\
        -single_arp_per_gateway 	1					\
        -single_ns_per_gateway		1					\
		-autonegotiation			1              		\
        -duplex             		auto           		\
        -speed              		auto           		\
        -intf_mode          		ethernet         	]
if {[keylget interface_status_0 status] != $::SUCCESS} {
	puts "FAIL - $test_name - [keylget interface_status_0 log]"
	return 0
}

set interface_handle_0 [keylget interface_status_0 interface_handle]

puts "Interface Handle: $interface_handle_0"
puts "End interface configuration for Port:$port_0"

################################################################################
# START - Interface configuration - Port 1
################################################################################

puts "Start interface configuration for Port:$port_1"

set interface_status_1 [::ixia::interface_config    \
        -port_handle        	$port_1       		\
		-l23_config_type 		protocol_interface	\
        -intf_ip_addr       	11.1.1.2      		\
        -gateway            	11.1.1.1     		\
        -netmask            	255.255.255.0		\
		-arp_on_linkup 			1					\
        -ns_on_linkup 			1					\
        -single_arp_per_gateway 1					\
        -single_ns_per_gateway	1					\
		-autonegotiation		1              		\
        -duplex             	auto           		\
        -speed              	auto           		\
        -intf_mode          	ethernet            ]
if {[keylget interface_status_1 status] != $::SUCCESS} {
	puts "FAIL - $test_name - [keylget interface_status_1 log]"
	return 0
}

set interface_handle_1 [keylget interface_status_1 interface_handle]

puts "Interface Handle: $interface_handle_1"
puts "End interface configuration for Port:$port_1"

################################################################################
# LINK STATUS - Check port link status - up
################################################################################

# Default value for desired status = up

puts "check port link state desired status - up"

set port_link_status [::ixia::test_control -action check_link_state -port_handle $port_handle]

if {[keylget port_link_status status] != $::SUCCESS} {
	puts "FAIL - $test_name - [keylget port_link_status log]"
	return 0
}

foreach port $port_handle {
	set port_status [keylget port_link_status $port.state]
	if {$port_status != "up"} {
		puts "Error: Port $port doesnt have desired state set"
		incr cfgError
	} else {
		puts "Port $port State : $port_status"
	}
}	

################################################################################
# START - Modify Interface configuration - Port 0
################################################################################
puts "Start interface configuration for Port:$port_0"

set interface_status_0 [::ixia::interface_config 		\
        -port_handle        		$port_0        		\
		-mode						modify				\
		-autonegotiation			0              		\
        -speed              		ether100      		\
        -intf_mode          		ethernet         	]
if {[keylget interface_status_0 status] != $::SUCCESS} {
	puts "FAIL - $test_name - [keylget interface_status_0 log]"
	return 0
}


################################################################################
# START - Modify Interface configuration - Port 1
################################################################################

puts "Start interface configuration for Port:$port_1"

set interface_status_1 [::ixia::interface_config 	\
        -port_handle        	$port_1       		\
		-mode					modify				\
		-autonegotiation		0              		\
        -speed              	ether1000      		\
        -intf_mode          	ethernet         	]
if {[keylget interface_status_1 status] != $::SUCCESS} {
	puts "FAIL - $test_name - [keylget interface_status_1 log]"
	return 0
}

################################################################################
# LINK STATUS - Check port link status - down
################################################################################

puts "check port link state desired status - down"
set port_link_status [::ixia::test_control -action check_link_state -port_handle $port_handle -desired_status down]

if {[keylget port_link_status status] != $::SUCCESS} {
	puts "FAIL - $test_name - [keylget port_link_status log]"
	return 0
}

foreach port $port_handle {
	set port_status [keylget port_link_status $port.state]
	if {$port_status != "down"} {
		puts "Error: Port $port doesnt have desired state set"
		incr cfgError
	} else {
		puts "Port $port State : $port_status"
	}
}

################################################################################
# LINK STATUS - Check port link status - timeout
################################################################################

puts "Polling for desired status - timeout 60s - [clock format [clock seconds]]"


set port_link_status [::ixia::test_control -action check_link_state -port_handle $port_handle -desired_status up]

puts "Polled for desired status - timeout 60s - [clock format [clock seconds]]"

if {[keylget port_link_status status] != $::FAILURE} {
	puts "FAIL - $test_name - Return value should be $::FAILURE if ports are not in desired state"
	return 0
}

foreach port $port_handle {
	set port_status [keylget port_link_status $port.state]
	if {$port_status != "down"} {
		puts "Error: Port $port doesnt have desired state set"
		incr cfgError
	} else {
		puts "Port $port State : $port_status"
	}
}	

############################### SUCCESS or FAILURE #############################

if {$cfgError == 0} {
	puts "SUCCESS - $test_name - [clock format [clock seconds]]"
	return 1
} else {
	puts "FAILURE - $test_name - [clock format [clock seconds]]"
	return 0
}

################################################################################

