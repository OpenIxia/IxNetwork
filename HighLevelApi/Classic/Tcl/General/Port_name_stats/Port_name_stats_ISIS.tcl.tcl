#################################################################################
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
#   This sample configures portname and IPv4 traffic items                     #
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
set ::cfg::l1_intf_mode  ethernet                  ;# CHOICES atm 
                                                   ;# CHOICES ethernet (for 10/100/1000 Ethernet cards and 10GE cards)
                                                   ;# CHOICES pos_hdlc pos_ppp frame_relay1490 frame_relay2427 frame_relay_cisco srp srp_cisco rpr gfp (for POS cards)

set ::cfg::l1_speed      auto                      ;# CHOICES ether10 ether100 ether1000 auto DEFAULT ether100 (for 10/100/1000 Ethernet cards)

set ::ixia::debug 0

################################################################################
# START - Connect to the chassis
################################################################################
puts "Start connecting to chassis ..."
update idletasks
set var_list [list chassis_ip port_list break_locks tcl_server ixnetwork_tcl_server]

################################################################################
# START - Connect to the chassis
################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect

puts "Starting - $test_name - [clock format [clock seconds]]"
puts "Start connecting to chassis ..."
set chassis_ip				10.205.16.54
set port_list				[list 2/5 2/6]
set break_locks             1
set tcl_server				10.205.16.54
set ixnetwork_tcl_server	127.0.0.1
set port_count				2
set port_names				[list test_port_1 test_port_2]
set start_time				[clock clicks -milliseconds]
set ixn_time				0
set item_start_time			0
global cfgErrors

set connect_status [::ixia::connect                                        	   \
            -reset                                                             \
            -device               $chassis_ip                                  \
            -port_list            $port_list                                   \
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
    
    # Initialize per port variables
    set interface_handles_$port ""
    
    incr i
}
set vport_info_status	[::ixia::vport_info					\
		-mode				set_info						\
		-port_list			$port_handle					\
		-port_name_list		$port_names						]
		
if {[keylget vport_info_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget vport_info_status log]"
}
foreach item $var_list {catch {unset $item}}
################################################################################
# END - Connect to the chassis
################################################################################

puts "Connect to the chassis complete."

################################################################################
# START - Interface configuration - L1
################################################################################
puts "Start interface configuration L1 ..."
update idletasks
set var_list [list intf_cfg_port_handle intf_mode speed autonegotiation duplex  \
                   phy_mode clocksource]

set intf_cfg_port_handle      $port_handle
set intf_mode                 $::cfg::l1_intf_mode ;# CHOICES atm 
                                                   ;# CHOICES ethernet (for 10/100/1000 Ethernet cards and 10GE cards)
                                                   ;# CHOICES pos_hdlc pos_ppp frame_relay1490 frame_relay2427 frame_relay_cisco srp srp_cisco rpr gfp (for POS cards)
set speed                     $::cfg::l1_speed     ;# CHOICES ether10 ether100 ether1000 auto DEFAULT ether100 (for 10/100/1000 Ethernet cards)
                                                   ;# CHOICES ether10000lan ether10000wan (for 10GE cards)
                                                   ;# CHOICES oc3 oc12 oc48 oc192 DEFAULT oc12 (for ATM and POS cards)
##########################################
# Configure interface in the test (IPv4) #
##########################################
set interface_status [ixia::interface_config            \
        -port_handle     $intf_cfg_port_handle	 		\
        -autonegotiation 1                          	\
        -speed           $speed		               		\
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

#########################################
# Configure the first IS-IS L1L2 router #
#########################################
set isis_router_status [ixia::emulation_isis_config     \
        -mode                           create          \
        -reset                                          \
        -port_handle                    $port_0         \
        -intf_ip_addr                   22.1.1.2        \
        -gateway_ip_addr                22.1.1.1        \
        -intf_ip_prefix_length          24              \
        -mac_address_init               0000.0000.0011  \
        -count                          1               \
        -wide_metrics                   1               \
        -discard_lsp                    1               \
        -attach_bit                     1               \
        -partition_repair               1               \
        -overloaded                     1               \
        -lsp_refresh_interval           888             \
        -lsp_life_time                  777             \
        -max_packet_size                1492            \
        -intf_metric                    0               \
        -routing_level                  L1L2            \
        -te_enable                      1               \
        -te_max_bw                      10              \
        -te_max_resv_bw                 20              \
        -te_unresv_bw_priority0         10              \
        -te_unresv_bw_priority2         20              \
        -te_unresv_bw_priority3         30              \
        -te_unresv_bw_priority4         40              \
        -te_unresv_bw_priority5         50              \
        -te_unresv_bw_priority6         60              \
        -te_unresv_bw_priority7         70              \
        -te_metric                      10              \
        ]
if {[keylget isis_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_router_status log]"
    return
}

set router_handle1 [keylget isis_router_status handle]

#####################################################
# Add a stub route range for the first IS-IS router #
#####################################################
set route_config_status [ixia::emulation_isis_topology_route_config \
        -mode                   create                              \
        -handle                 $router_handle1                     \
        -type                   stub                                \
        -ip_version             4                                   \
        -stub_ip_start          44.0.0.1                            \
        -stub_ip_pfx_len        20                                  \
        -stub_count             5                                   \
        -stub_metric            22                                  \
        -stub_up_down_bit       1                                   \
        ]
if {[keylget route_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget route_config_status log]"
    return
}

##########################################
# Configure the second IS-IS L1L2 router #
##########################################
set isis_router_status [ixia::emulation_isis_config     \
        -mode                           create          \
        -reset                                          \
        -port_handle                    $port_1         \
        -intf_ip_addr                   22.1.1.1        \
        -gateway_ip_addr                22.1.1.2        \
        -intf_ip_prefix_length          24              \
        -mac_address_init               0000.0000.0022  \
        -count                          1               \
        -wide_metrics                   1               \
        -discard_lsp                    1               \
        -attach_bit                     1               \
        -partition_repair               1               \
        -overloaded                     1               \
        -lsp_refresh_interval           888             \
        -lsp_life_time                  777             \
        -max_packet_size                1492            \
        -intf_metric                    0               \
        -routing_level                  L1L2            \
        -te_enable                      1               \
        -te_max_bw                      10              \
        -te_max_resv_bw                 20              \
        -te_unresv_bw_priority0         10              \
        -te_unresv_bw_priority2         20              \
        -te_unresv_bw_priority3         30              \
        -te_unresv_bw_priority4         40              \
        -te_unresv_bw_priority5         50              \
        -te_unresv_bw_priority6         60              \
        -te_unresv_bw_priority7         70              \
        -te_metric                      10              \
        ]
if {[keylget isis_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_router_status log]"
    return
}

set router_handle2 [keylget isis_router_status handle]

######################################################
# Add a stub route range for the second IS-IS router #
######################################################
set route_config_status [ixia::emulation_isis_topology_route_config \
        -mode                   create                              \
        -handle                 $router_handle2                     \
        -type                   stub                                \
        -ip_version             4                                   \
        -stub_ip_start          55.0.0.3                            \
        -stub_ip_pfx_len        14                                  \
        -stub_count             3                                   \
        -stub_metric            20                                  \
        -stub_up_down_bit       1                                   \
        ]
if {[keylget route_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget route_config_status log]"
    return
}

######################################
# Start the IS-IS protocol emulation #
######################################
set isis_emulation_status [ixia::emulation_isis_control \
        -port_handle $port_0                            \
        -mode        start                              ]
if {[keylget isis_emulation_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_emulation_status log]"
    return
}

set isis_emulation_status [ixia::emulation_isis_control \
        -port_handle $port_1                            \
        -mode        start                              ]
if {[keylget isis_emulation_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_emulation_status log]"
    return
}

######################################
# Gather statistics IS-IS statistics #
######################################
after 10000
set isis_routers_info [ixia::emulation_isis_info    \
        -handle $router_handle1                     \
        -mode   stats                               \
        ]
if {[keylget isis_routers_info status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_routers_info log]"
    return
}

set all_the_problems 0

puts "========== ISIS Stats =========="

puts "========== Port $port_0 =========="

######################################
# Verifying port_name 				 #
######################################

if { [catch {set port_name [keylget isis_routers_info $port_0.port_name]} error] } {
	puts "! No port_name stats available - Get stats failed."
	puts "Error: $error"
	incr all_the_problems
} else {
	puts "port_name Stats Available."
	if {$port_name != "test_port_1"} {
		puts "port_name value is incorrect. $port_name != test_port_1"
		incr all_the_problems
	} else {
		puts "port_name value is correct. $port_name == test_port_1"
	}
}

######################################
# Gather statistics IS-IS statistics #
######################################

set isis_routers_info [ixia::emulation_isis_info    \
        -handle $router_handle2                     \
        -mode   stats                               \
        ]
if {[keylget isis_routers_info status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_routers_info log]"
    return
}

######################################
# Verifying port_name 				 #
######################################

puts "========== Port $port_1 =========="

if { [catch {set port_name [keylget isis_routers_info $port_1.port_name]} error] } {
	puts "! No port_name stats available - Get stats failed."
	puts "Error: $error"
	incr all_the_problems
} else {
	puts "port_name Stats Available."
	if {$port_name != "test_port_2"} {
		puts "port_name value is incorrect. $port_name != test_port_2"
		incr all_the_problems
	} else {
		puts "port_name value is correct. $port_name == test_port_2"
	}
}

if {$all_the_problems > 0} {
    puts "***** $all_the_problems Errors encountered *****"
    return 0
}

set total_time [expr [clock clicks -milliseconds] - $start_time]
puts "Total Time: $total_time" 
puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1

