################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Daria Badea
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    04-01-2014 
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
#	 The script configures 2 PTP stacks, master and slave.					   #
#	 Dynamics: Start/stop protocols and get stats.     						   #
#																			   #
# Module:                                                                      #
#    The sample was tested on a LSM XM8S module.	                   		   #
#                                                                              #
################################################################################

set port1 						9/1
set port2 						9/9
set test_name                   [info script]
set chassis_ip                  10.205.15.184
set ixnetwork_tcl_server        localhost
set port_list                   [list $port1 $port2]
set username                    user1

set PASSED 0
set FAILED 1

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - $retCode"
    return $FAILED
}

set connect_status [::ixiangpf::connect \
        -reset                  1 \
        -device                 $chassis_ip \
        -username               $username \
        -port_list              $port_list \
        -ixnetwork_tcl_server   $ixnetwork_tcl_server \
        -tcl_server             $chassis_ip \
        -break_locks            1 \
        -connect_timeout        180 \
    ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - [keylget connect_status log]"
    return $FAILED
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
    set interface_handles_$port ""
    incr i
}

proc show_stats var {
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
            if {$key == "status"} {continue}
            set indent [string repeat "    " $level] 
            puts -nonewline $indent 
            if {[catch {keylkeys var $key}]} {
                puts "$key: [keylget var $key]"
                continue
            } else {
                puts $key
                puts "$indent[string repeat "-" [string length $key]]"
            }
            show_stats [keylget var $key]
    }
}

# #############################################################################
# 								PTP MASTER CONFIG
# #############################################################################

# TOPOLOGY 1 CONFIG

puts "\n\nConfiguring PTP Master...\n\n"

set topology_1_status [::ixiangpf::topology_config					\
        -topology_name      {PTP Master}                            \
        -port_handle        $port_0								    \
    ]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_1_status log]"
    return $FAILED
}

set topology_1_handle [keylget topology_1_status topology_handle]


# CREATE DEVICE GROUP 1

set device_group_1_status [::ixiangpf::topology_config      \
		-topology_handle              $topology_1_handle        \
		-device_group_multiplier      1                         \
		-device_group_enabled         1                         \
]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_1_status log]"
    return $FAILED
}

set device_1_handle	[keylget device_group_1_status device_group_handle]

# CREATE ETHERNET+IPv6 STACKs 1

set multivalue_1_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.22.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_1_status status] != $::SUCCESS} {
    puts "FAIL - $multivalue_1_status"
	return $FAILED
}
set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]

set ipv6_1_status [::ixiangpf::interface_config \
    -protocol_handle              $device_1_handle           \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_1_handle       \
	-ipv6_intf_addr				  aaaa::1					 \
	-ipv6_gateway				  aaaa::2					 \
	-ipv6_resolve_gateway			0						 \
]
if {[keylget ipv6_1_status status] != $::SUCCESS} {
    puts "FAIL - $ipv6_1_status"
	return $FAILED
}

set ethernet_1_handle [keylget ipv6_1_status ethernet_handle]
set ipv6_1_handle [keylget ipv6_1_status ipv6_handle]

# PTP 1 STACK CONFIG MASTER

set ptp_1_status [::ixiangpf::ptp_over_ip_config                    \
		-mode                                create					\
		-parent_handle                       $ipv6_1_handle   		\
		-slave_ipv6_address                  aaaa::2     			\
		-slave_ipv6_increment_by             ::1					\
	    -slave_count                         1						\
		-name                                {PTP IPv6 1}			\
		-port_number                         6323					\
		-communication_mode                  unicast				\
		-domain                              123					\
		-priority1                           10						\
		-priority2                           100					\
		-profile                             ieee1588				\
		-role                                master					\
		-ip_type       						 ipv6					\
		-intf_ipv6_addr                      aaaa::1				\
		-intf_ipv6_addr_step                 ::1000					\
		-intf_prefixv6_length                60						\
		-neighbor_intf_ipv6_addr             aaaa::2				\
		-neighbor_intf_ipv6_addr_step        ::1000					\
	]
if {[keylget ptp_1_status status] != $::SUCCESS} {
    puts "FAIL - [keylget ptp_1_status log]"
    return $FAILED
}

set ptp_master_handle [keylget ptp_1_status ptp_handle]

# #############################################################################
# 								PTP SLAVE CONFIG
# #############################################################################

# TOPOLOGY 2 CONFIG

puts "\n\nConfiguring PTP Slave...\n\n"

set topology_2_status [::ixiangpf::topology_config					\
        -topology_name      {PTP Slave}                            \
        -port_handle        $port_1								    \
    ]
if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_2_status log]"
    return $FAILED
}

set topology_2_handle [keylget topology_2_status topology_handle]

# CREATE DEVICE GROUP 2

set device_group_2_status [::ixiangpf::topology_config      \
		-topology_handle              $topology_2_handle        \
		-device_group_multiplier      1                         \
		-device_group_enabled         1                         \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_status log]"
    return $FAILED
}

set device_2_handle	[keylget device_group_2_status device_group_handle]

# CREATE ETHERNET+IPv6 STACKs 2

set multivalue_3_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.32.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_3_status status] != $::SUCCESS} {
    puts "FAIL - $multivalue_3_status"
	return $FAILED
}
set multivalue_3_handle [keylget multivalue_3_status multivalue_handle]

set ipv6_2_status [::ixiangpf::interface_config \
    -protocol_handle              $device_2_handle           \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_3_handle       \
	-ipv6_intf_addr				  aaaa::2					 \
	-ipv6_gateway				  aaaa::1					 \
	-ipv6_resolve_gateway		  0							 \
]
if {[keylget ipv6_2_status status] != $::SUCCESS} {
    puts "FAIL - $ipv6_2_status"
	return $FAILED
}

set ethernet_2_handle [keylget ipv6_2_status ethernet_handle]
set ipv6_2_handle [keylget ipv6_2_status ipv6_handle]

# PTP 2 STACK CONFIG SLAVE

set ptp_2_status [::ixiangpf::ptp_over_ip_config                    \
		-mode                                create					\
		-parent_handle                       $ipv6_2_handle  		\
		-name                                {PTP IPv6 2}			\
		-offset_scaled_log_variance          1						\
		-one_way                             1						\
		-p_delay_follow_up_residence_time    120					\
		-port_number                         6323					\
		-communication_mode                  unicast				\
		-master_ipv6_address                 aaaa::1				\
		-master_ipv6_increment_by            ::1					\
		-master_count						 1						\
		-domain                              123					\
		-profile                             ieee1588				\
		-role                                slave					\
		-ip_type       						 ipv6					\
		-intf_ipv6_addr                      aaaa::2				\
		-intf_ipv6_addr_step                 ::1000					\
		-intf_prefixv6_length                60						\
		-neighbor_intf_ipv6_addr             aaaa::1				\
		-neighbor_intf_ipv6_addr_step        ::1000					\
	]
if {[keylget ptp_2_status status] != $::SUCCESS} {
    puts "FAIL - [keylget ptp_2_status log]"
    return $FAILED
}

set ptp_slave_handle [keylget ptp_2_status ptp_handle]

# #############################################################################
# 								START PTP
# #############################################################################

puts "\n\nStarting PTP Master...\n\n"

set control_status [::ixiangpf::ptp_over_ip_control  \
	-handle 			 	$ptp_master_handle                       \
	-action 				start					             \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - [keylget control_status log]"
    return $FAILED
}

puts "\n\nStarting PTP Slave...\n\n"

set control_status [::ixiangpf::ptp_over_ip_control  \
	-handle 			 	$ptp_slave_handle                       \
	-action 				start					             \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - [keylget control_status log]"
    return $FAILED
}

while {[lindex [ixNet getA $ptp_slave_handle -stateCounts] 3]!="1" || [lindex [ixNet getA $ptp_master_handle -stateCounts] 3]!="1"} {
	after 1000
	puts "Waiting for PTP to be up..."
}
puts "PTP stacks are up!"

after 10000

# #############################################################################
# 								COLLECT PTP STATS
# #############################################################################

puts "\n\nCollecting PTP aggregate stats...\n\n"

set ptp_1_stats [::ixiangpf::ptp_over_ip_stats				\
		-port_handle			$port_0				\
		-mode					aggregate		    \
	]
if {[keylget ptp_1_stats status] != $::SUCCESS} {
    puts "FAIL - [keylget ptp_1_stats log]"
    return $FAILED
}

set ptp_2_stats [::ixiangpf::ptp_over_ip_stats				\
		-port_handle			$port_1				\
		-mode					aggregate		    \
	]
if {[keylget ptp_2_stats status] != $::SUCCESS} {
    puts "FAIL - [keylget ptp_2_stats log]"
    return $FAILED
}

puts "\n\nPTP Master statistics\n\n"
show_stats $ptp_1_stats
puts "\n\nPTP Slave statistics\n\n"
show_stats $ptp_2_stats

if {[keylget ptp_1_stats $port_0.gen.sessions_active] != "1" || [keylget ptp_2_stats $port_1.gen.sessions_active] != "1"} {
	puts "FAIL - PTP sessions not active as expected!"
	return $FAILED
}

if {[keylget ptp_1_stats $port_0.gen.followup_messages_sent] < 1 || [keylget ptp_2_stats $port_1.gen.followup_messages_received] < 1} {
	puts "FAIL - PTP not negociated as expected!"
	return $FAILED
}

after 3000

# #############################################################################
# 								STOP PTP
# #############################################################################

puts "\n\nStopping PTP Slave...\n\n"

set control_status [::ixiangpf::ptp_over_ip_control  \
	-handle 			 	$ptp_slave_handle                       \
	-action 				stop					             \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - [keylget control_status log]"
    return $FAILED
}

puts "\n\nStopping PTP Master...\n\n"

set control_status [::ixiangpf::ptp_over_ip_control  \
	-handle 			 	$ptp_master_handle                       \
	-action 				stop					             \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - [keylget control_status log]"
    return $FAILED
}

while {[lindex [ixNet getA $ptp_slave_handle -stateCounts] 1]!="1" || [lindex [ixNet getA $ptp_master_handle -stateCounts] 1]!="1"} {
	after 1000
	puts "Waiting for PTP to stop..."
}
puts "PTP stacks are not started!"

after 3000

# #############################################################################
# 								CLEANUP
# #############################################################################

set cleanup [::ixia::cleanup_session -reset]
if {[keylget cleanup status] != $::SUCCESS} {
	puts "FAIL - [keylget cleanup log]"
	return $FAILED
}

puts "Done... IxNetwork session is closed..."
puts ""
puts "!!! PASSED !!!"
return $PASSED