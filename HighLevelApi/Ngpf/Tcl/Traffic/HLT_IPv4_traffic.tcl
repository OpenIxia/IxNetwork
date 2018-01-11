################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Theresa Kong $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-06-2014 Anca Lupu
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
#    This sample configures 100 NGPF IPv4 sessions on each of the two ports    #
#    configures two traffic items, starts traffic and collects stats           #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10/100/1000 LSM XMVDC16NG module.              #
#                                                                              #
################################################################################


################################################################################
# Logging and error handling procs
################################################################################
if {![info exists ::ixnHLT_log]} {
    proc ::my_ixnhlt_logger {s} {
        puts stderr $s; flush stderr; update; update idletasks
    }
    set ::ixnHLT_log ::my_ixnhlt_logger
}
if {![info exists ::ixnHLT_errorHandler]} {
    proc ::my_ixnhlt_errorhandler {module status} {
        set msg "FAIL - $module - [keylget status log]"
        $::ixnHLT_log $msg
        return -code error $msg
    }
    set ::ixnHLT_errorHandler ::my_ixnhlt_errorhandler
}

################################################################################
# Package require Ixia
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}
      
################################################################################
#  chassis, card, port configuration										   #
################################################################################
set chassis ixro-hlt-xm12-2
set ixnetwork_tcl_server localhost
set tcl_server localhost
set port_list {1/1 1/2}
set vport_name_list {{{{Ethernet - 001}} {{Ethernet - 002}}}}
set guard_rail statistics
set test_name                   [info script]
################################################################################
# START - Connect to the chassis											   #
# Connect to the IxNetwork Tcl Server & chassis, reset to factory defaults and take ownership		   #
################################################################################

set connect_status [::ixiangpf::connect  \
    -reset 1 \
    -device $chassis \
    -port_list $port_list \
    -ixnetwork_tcl_server $ixnetwork_tcl_server \
    -tcl_server $tcl_server \
    -guard_rail $guard_rail \
]
puts "End connecting to chassis ..."

set port1 [keylget connect_status port_handle.$chassis.[lindex $port_list 0]]
set port2 [keylget connect_status port_handle.$chassis.[lindex $port_list 1]]
set port_handle [list $port1 $port2] 

################################################################################
# Configure Topology, Device Group 
################################################################################
    set topology_1_status [::ixiangpf::topology_config \
        -topology_name      {Topology 1}                            \
        -port_handle        $port1\
    ]
    if {[keylget topology_1_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $topology_1_status
    }
    set topology_1_handle [keylget topology_1_status topology_handle]
    
    set device_group_1_status [::ixiangpf::topology_config \
        -topology_handle              $topology_1_handle      \
        -device_group_name            {Device Group 1}        \
        -device_group_multiplier      100                     \
        -device_group_enabled         1                       \
    ]
    if {[keylget device_group_1_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $device_group_1_status
    }
    set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]
    
################################################################################
# Create Ethernet Stack for the Device Group 
################################################################################
    set ethernet_1_status [::ixiangpf::interface_config \
        -protocol_name                {Ethernet 1}               \
        -protocol_handle              $deviceGroup_1_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 00.11.01.00.00.01          \
        -src_mac_addr_step            00.00.00.00.00.01          \
		-vlan						  1							 \
        -vlan_id                      1                          \
        -vlan_id_step                 1                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
    ]
    if {[keylget ethernet_1_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $ethernet_1_status
    }
    set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]
    
################################################################################
# Create IPv4 Stack on top of Ethernet Stack
################################################################################
    set ipv4_1_status [::ixiangpf::interface_config \
        -protocol_name                     {IPv4 1}                \
        -protocol_handle                   $ethernet_1_handle      \
        -ipv4_resolve_gateway              1                       \
        -ipv4_manual_gateway_mac           00.00.00.00.00.01       \
        -ipv4_manual_gateway_mac_step      00.00.00.00.00.00       \
        -gateway                           100.1.0.1               \
        -gateway_step                      0.0.1.0                 \
        -intf_ip_addr                      100.1.0.2               \
        -intf_ip_addr_step                 0.0.1.0                 \
        -netmask                           255.255.255.0           \
    ]

    if {[keylget ipv4_1_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $ipv4_1_status
    }
    set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]
    
################################################################################
# Configure 2nd Topology, Device Group 
################################################################################
    set topology_2_status [::ixiangpf::topology_config \
        -topology_name      {Topology 2}                            \
        -port_handle        $port2\
    ]
    if {[keylget topology_2_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $topology_2_status
    }
    set topology_2_handle [keylget topology_2_status topology_handle]
    set ixnHLT(HANDLE,//topology:<2>) $topology_2_handle
    
    set device_group_2_status [::ixiangpf::topology_config \
        -topology_handle              $topology_2_handle      \
        -device_group_name            {Device Group 2}        \
        -device_group_multiplier      100                      \
        -device_group_enabled         1                       \
    ]
    if {[keylget device_group_2_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $device_group_2_status
    }
    set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]
    
################################################################################
# Configure multivalue for the mac addresses
################################################################################
    set multivalue_1_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          00.12.01.00.00.01       \
        -counter_step           00.00.00.00.00.01       \
        -counter_direction      increment               \
        -nest_step              00.00.01.00.00.00       \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
    if {[keylget multivalue_1_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $multivalue_1_status
    }
    set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]
    
################################################################################
# Configure ethernet stack for the device group 
################################################################################
    set ethernet_2_status [::ixiangpf::interface_config \
        -protocol_name                {Ethernet 2}               \
        -protocol_handle              $deviceGroup_2_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 $multivalue_1_handle       \
		-vlan 						  1							 \
        -vlan_id                      1                          \
        -vlan_id_step                 1                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
    ]
    if {[keylget ethernet_2_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $ethernet_2_status
    }
    set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]
    
################################################################################
# Configure ipv4 stack on top of the ethernet stack
################################################################################
    set ipv4_2_status [::ixiangpf::interface_config \
        -protocol_name                     {IPv4 2}                \
        -protocol_handle                   $ethernet_2_handle      \
        -ipv4_resolve_gateway              1                       \
        -ipv4_manual_gateway_mac           00.00.00.00.00.01       \
        -ipv4_manual_gateway_mac_step      00.00.00.00.00.00       \
        -gateway                           100.1.0.2               \
        -gateway_step                      0.0.1.0                 \
        -intf_ip_addr                      100.1.0.1               \
        -intf_ip_addr_step                 0.0.1.0                 \
        -netmask                           255.255.255.0           \
    ]
    # n The attribute: connectedVia with the value: {} is not supported by scriptgen.
    if {[keylget ipv4_2_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $ipv4_2_status
    }
    set ipv4_2_handle [keylget ipv4_2_status ipv4_handle]
    
################################################################################
# Configure global options for ipv4 arp
################################################################################
    set ipv4_3_status [::ixiangpf::interface_config \
        -protocol_handle                    /globals      \
        -arp_on_linkup                      1             \
        -single_arp_per_gateway             1             \
        -ipv4_send_arp_rate                 200           \
        -ipv4_send_arp_interval             1000          \
        -ipv4_send_arp_max_outstanding      400           \
        -ipv4_send_arp_scale_mode           port          \
        -ipv4_attempt_enabled               0             \
        -ipv4_attempt_rate                  200           \
        -ipv4_attempt_interval              1000          \
        -ipv4_attempt_scale_mode            port          \
        -ipv4_diconnect_enabled             0             \
        -ipv4_disconnect_rate               200           \
        -ipv4_disconnect_interval           1000          \
        -ipv4_disconnect_scale_mode         port          \
    ]
    if {[keylget ipv4_3_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $ipv4_3_status
    }
    
################################################################################
# Configure global options for ethernet 
################################################################################
    set ethernet_3_status [::ixiangpf::interface_config \
        -protocol_handle                     /globals      \
        -ethernet_attempt_enabled            0             \
        -ethernet_attempt_rate               100           \
        -ethernet_attempt_interval           999          \
        -ethernet_attempt_scale_mode         port          \
        -ethernet_diconnect_enabled          0             \
        -ethernet_disconnect_rate            100           \
        -ethernet_disconnect_interval        999          \
        -ethernet_disconnect_scale_mode      port          \
    ]
    if {[keylget ethernet_3_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $ethernet_3_status
    }
    

###################################################################################
# Start All Protocols - This command also starts ethernet stack & sends out ARP REQ 
###################################################################################    
$::ixnHLT_log {Starting all protocol(s) ...}
set r [::ixia::test_control -action start_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $r
}

###################################################################################################
# Wait 30 seconds
###################################################################################################
after 30000

####################################################################################
# Send ARP request for ipv4 interfaces - sending ARP without starting other protocols
#####################################################################################    
$::ixnHLT_log "Sending ARP Request on $ipv4_1_handle ..."
set arp_status [::ixiangpf::interface_config \
		    -protocol_handle                   $ipv4_1_handle\
		    -arp_send_req                      1\
		   ]

$::ixnHLT_log "Sending ARP Request on $ipv4_2_handle ..."
set arp_status [::ixiangpf::interface_config \
		    -protocol_handle                   $ipv4_2_handle\
		    -arp_send_req                      1\
		   ]

####################################################
#  Create Traffic item from Topology 1 to Topology 2
####################################################
$::ixnHLT_log {Configuring traffic for traffic item: //traffic/trafficItem:<1>}

set _result_ [::ixia::traffic_config  \
        -mode create \
        -endpointset_count 1 \
        -emulation_src_handle $topology_1_handle\
        -emulation_dst_handle $topology_2_handle\
        -src_dest_mesh one_to_one \
        -route_mesh one_to_one \
        -bidirectional 1 \
        -name Traffic_Item_1 \
        -circuit_endpoint_type ipv4 \
		-track_by endpoint_pair\
		      ]

    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }

set traffic_item_name [keylget _result_ stream_id]
set current_config_elements [keylget _result_ traffic_item]
puts "Created $traffic_item_name.  Config Element is: $current_config_elements"

###################################################################################################
# Wait 10 seconds
###################################################################################################
after 10000

###################################################################################################
#  Create Traffic item from subset of endpoints in Topology 1 to subset of endpoints in Topology 2
###################################################################################################
$::ixnHLT_log {Configuring traffic for traffic item: //traffic/trafficItem:<1>}
set ti_scalable_srcs(EndpointSet-1) $ipv4_1_handle
set ti_scalable_srcs_port_start(EndpointSet-1) [list 1]
set ti_scalable_srcs_port_count(EndpointSet-1) [list 1]
set ti_scalable_srcs_intf_start(EndpointSet-1) [list 1]
set ti_scalable_srcs_intf_count(EndpointSet-1) [list 5]
set ti_scalable_dsts(EndpointSet-1) $ipv4_2_handle
set ti_scalable_dsts_port_start(EndpointSet-1) [list 1]
set ti_scalable_dsts_port_count(EndpointSet-1) [list 1]
set ti_scalable_dsts_intf_start(EndpointSet-1) [list 6]
set ti_scalable_dsts_intf_count(EndpointSet-1) [list 5]

set _result_ [::ixia::traffic_config  \
		  -mode create \
		  -endpointset_count 1 \
		  -emulation_src_handle {}\
		  -emulation_dst_handle {}\
		  -emulation_scalable_src_handle ti_scalable_srcs \
		  -emulation_scalable_src_port_start ti_scalable_srcs_port_start \
		  -emulation_scalable_src_port_count ti_scalable_srcs_port_count \
		  -emulation_scalable_src_intf_start ti_scalable_srcs_intf_start \
		  -emulation_scalable_src_intf_count ti_scalable_srcs_intf_count \
		  -emulation_scalable_dst_handle ti_scalable_dsts \
		  -emulation_scalable_dst_port_start ti_scalable_dsts_port_start \
		  -emulation_scalable_dst_port_count ti_scalable_dsts_port_count \
		  -emulation_scalable_dst_intf_start ti_scalable_dsts_intf_start \
		  -emulation_scalable_dst_intf_count ti_scalable_dsts_intf_count \
		  -src_dest_mesh one_to_one \
		  -route_mesh one_to_one \
		  -bidirectional 0\
		  -name Traffic_Item_1 \
		  -circuit_endpoint_type ipv4 \
		  -track_by endpoint_pair\
		 ]

if {[keylget _result_ status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $_result_
}

set traffic_item_name [keylget _result_ stream_id]
set current_config_elements [keylget _result_ traffic_item]
puts "Created $traffic_item_name.  Config Element is: $current_config_elements"

###################################################################################################
# Wait 10 seconds
###################################################################################################
after 10000

###################################################################################################
#  Start Traffic - for a large traffic config, it may take sometime to start the traffic.   
#  max_wait_timer option & return key:stopped_flag are used to ensure that the traffic is started before
#  moving on to the next step
###################################################################################################
puts "Starting Traffic..."
set retry_cnt 3
set cmd_status [::ixia::traffic_control \
		    -action run\
		    -max_wait_timer 60 \
		   ]
if {[keylget cmd_status status] == $::FAILURE} {
    puts  "Error: starting traffic"
    return 0
} else {
    set stopped_flag [keylget cmd_status stopped]
    while {$stopped_flag == 1} {
	after 3000
	incr retry_cnt -1
	set poll_status [ixia::traffic_control -action poll]
	set stopped_flag [keylget poll_status stopped]
	if {$retry_cnt == 0} break;
    }
}
if {$stopped_flag} {
    puts "Error: starting traffic after $retry_cnt attempts"
    return 0
} 

###################################################################################################
# Wait 20 seconds
###################################################################################################
after 20000

###################################################################################################
#  Collect Traffic Item Stats
###################################################################################################
puts "Collecting Traffic Item Stats"
set traffic_status [::ixia::traffic_stats \
		  -mode traffic_item\
	      ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

set traffic_items [keylget traffic_status traffic_item]
set traffic_items [keylkeys traffic_items]

foreach traffic_item $traffic_items {
    puts "***** Traffic item: $traffic_item"
    puts [format "%24s %s" "Rx Total packets: "\
    [keylget traffic_status traffic_item.$traffic_item.rx.total_pkts]]    
    puts [format "%24s %s" "Rx Lost packets: "\
    [keylget traffic_status traffic_item.$traffic_item.rx.loss_pkts]]
    puts [format "%24s %s" "Rx Total packet bytes: "\
    [keylget traffic_status traffic_item.$traffic_item.rx.total_pkt_bytes]]
}

###################################################################################################
#  Stop Traffic - for a large traffic config, it may take sometime to stop the traffic.   
#  max_wait_timer option & return key:stopped_flag are used to ensure that the traffic is started before
#  moving on to the next step
###################################################################################################
puts "Stopping Traffic"
set retry_cnt 3
set cmd_status [::ixia::traffic_control \
		    -action stop \
		    -max_wait_timer 60 \
		   ]
if {[keylget cmd_status status] == $::FAILURE} {
    puts  "Error: starting traffic"
    return 0
} else {
    set stopped_flag [keylget cmd_status stopped]
    while {$stopped_flag != 1} {
	after 3000
	incr retry_cnt -1
	set poll_status [ixia::traffic_control -action poll]
	set stopped_flag [keylget poll_status stopped]
	if {$retry_cnt == 0} break;
    }
}
if {!$stopped_flag} {
    puts "Error: stopping traffic after $retry_cnt attempts"
    return 0
} 

###################################################################################
# Stop All Protocols
###################################################################################    
$::ixnHLT_log {Stopping all protocol(s) ...}
set r [::ixia::test_control -action stop_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $r
}


return "SUCCESS - $test_name - [clock format [clock seconds]]"