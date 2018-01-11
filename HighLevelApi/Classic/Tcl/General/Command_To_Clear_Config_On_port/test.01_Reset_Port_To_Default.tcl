#################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    02-20-2013 Mchakravarthy - created sample
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
#    This sample configures Port Interfaces, OSPF protocol and traffic on the  #
#    port and reset the entire port to factory default                         #
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

################################################################################
# START - Connect to the chassis
################################################################################
puts "Starting - $test_name - [clock format [clock seconds]]"
puts "Start connecting to chassis ..."

set chassis_ip                  10.205.16.54
set port_list                   [list 2/5 2/6]
set break_locks                 1
set tcl_server                  127.0.0.1
set ixnetwork_tcl_server        127.0.0.1
set port_count                  2

set connect_status [::ixia::connect                                            \
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

set interface_status_0 [::ixia::interface_config         \
        -port_handle                $port_0              \
        -l23_config_type            protocol_interface   \
        -intf_ip_addr               11.1.1.1             \
        -gateway                    11.1.1.2             \
        -netmask                    255.255.255.0        \
        -arp_on_linkup              1                    \
        -ns_on_linkup               1                    \
        -single_arp_per_gateway     1                    \
        -single_ns_per_gateway      1                    \
        -autonegotiation            1                    \
        -duplex                     auto                 \
        -speed                      auto                 \
        -intf_mode                  ethernet             ]
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

set interface_status_1 [::ixia::interface_config      \
        -port_handle            $port_1               \
        -l23_config_type        protocol_interface    \
        -intf_ip_addr           11.1.1.2              \
        -gateway                11.1.1.1              \
        -netmask                255.255.255.0         \
        -arp_on_linkup          1                     \
        -ns_on_linkup           1                     \
        -single_arp_per_gateway 1                     \
        -single_ns_per_gateway  1                     \
        -autonegotiation        1                     \
        -duplex                 auto                  \
        -speed                  auto                  \
        -intf_mode              ethernet              ]
if {[keylget interface_status_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status_1 log]"
    return 0
}

set interface_handle_1 [keylget interface_status_1 interface_handle]
puts "Interface Handle: $interface_handle_1"
puts "End interface configuration for Port:$port_1"

################################################################################
# OSPF Configuration - Port 0
################################################################################

set _result_ [::ixia::emulation_ospf_config              \
        -mode                        create              \
        -port_handle                 $port_0             \
        -lsa_discard_mode            1                   \
        -session_type                ospfv2              \
        -area_id                     0.0.0.0             \
        -area_type                   external-capable    \
        -dead_interval               40                  \
        -hello_interval              10                  \
        -interface_cost              10                  \
        -authentication_mode         null                \
        -mtu                         1500                \
        -neighbor_router_id          0.0.0.0             \
        -network_type                ptop                \
        -option_bits                 2                   \
        -router_priority             2                   \
        -te_enable                   0                   \
        -bfd_registration            0                   \
        -intf_ip_addr                11.1.1.1            \
        -intf_prefix_length          24                  \
        -neighbor_intf_ip_addr       11.1.1.2            \
        -vlan                        0                   \
        -vlan_id                     1                   \
        -vlan_user_priority          0                   \
        -graceful_restart_enable     0                   \
        -router_id                   83.90.0.1           ]
        
#Check status
if {[keylget _result_ status] != $::SUCCESS}     {
    puts "FAIL - $test_name - [keylget _result_ log]"
}

set ixnHLT(HANDLES,$port_0,emulation_ospf_config) ""
# Collate handles on per-vport basis for use in control cmds
foreach _handle_ [keylget _result_ handle] {
    puts "Handle: $_handle_"
    set ixnHLT(HANDLE,$port_0) $_handle_
    lappend ixnHLT(HANDLES,$port_0,emulation_ospf_config) \
    $ixnHLT(HANDLE,$port_0)
}

puts "COMPLETED: emulation_ospf_config - port_0"

################################################################################
# OSPF Configuration - Port 1
################################################################################

set _result_ [::ixia::emulation_ospf_config              \
        -mode                        create              \
        -port_handle                 $port_1             \
        -lsa_discard_mode            1                   \
        -session_type                ospfv2              \
        -area_id                     0.0.0.0             \
        -area_type                   external-capable    \
        -dead_interval               40                  \
        -hello_interval              10                  \
        -interface_cost              10                  \
        -authentication_mode         null                \
        -mtu                         1500                \
        -neighbor_router_id          0.0.0.0             \
        -network_type                ptop                \
        -option_bits                 2                   \
        -router_priority             2                   \
        -te_enable                   0                   \
        -bfd_registration            0                   \
        -intf_ip_addr                11.1.1.2            \
        -intf_prefix_length          24                  \
        -neighbor_intf_ip_addr       11.1.1.1            \
        -vlan                        0                   \
        -vlan_id                     1                   \
        -vlan_user_priority          0                   \
        -graceful_restart_enable     0                   \
        -router_id                   83.91.0.1           ]
        
#Check status
if {[keylget _result_ status] != $::SUCCESS}     {
    puts "FAIL - $test_name - [keylget _result_ log]"
}

set ixnHLT(HANDLES,$port_1,emulation_ospf_config) ""
# Collate handles on per-vport basis for use in control cmds
foreach _handle_ [keylget _result_ handle] {
    puts "Handle: $_handle_"
    set ixnHLT(HANDLE,$port_1) $_handle_
    lappend ixnHLT(HANDLES,$port_1,emulation_ospf_config) \
    $ixnHLT(HANDLE,$port_1)
}

puts "COMPLETED: emulation_ospf_config - port_1"

################################################################################
# OSPF  Route Range Configuration - Port 0
################################################################################

set _result_ [::ixia::emulation_ospf_topology_route_config  \
        -mode                       create                  \
        -handle                     $ixnHLT(HANDLE,$port_0) \
        -count                      2                       \
        -summary_prefix_length      24                      \
        -summary_prefix_metric      0                       \
        -summary_prefix_start       12.1.1.0                \
        -summary_number_of_prefix   1                       \
        -type                       summary_routes          ]
        
#Check status
if {[keylget _result_ status] != $::SUCCESS}     {
    puts "FAIL - $test_name - [keylget _result_ log]"
}

set route_range_handle_port0 [keylget _result_ elem_handle]
puts $route_range_handle_port0

puts "COMPLETED: emulation_ospf_topology_route_config - $port_0" 
################################################################################
# OSPF  Route Range Configuration - Port 1
################################################################################

set _result_ [::ixia::emulation_ospf_topology_route_config  \
        -mode                       create                  \
        -handle                     $ixnHLT(HANDLE,$port_1) \
        -count                      2                       \
        -summary_prefix_length      24                      \
        -summary_prefix_metric      0                       \
        -summary_prefix_start       13.1.1.0                \
        -summary_number_of_prefix   1                       \
        -type                       summary_routes          ]
        
#Check status
if {[keylget _result_ status] != $::SUCCESS}     {
    puts "FAIL - $test_name - [keylget _result_ log]"
}
set route_range_handle_port1 [keylget _result_ elem_handle]

puts $route_range_handle_port1

puts "COMPLETED: emulation_ospf_topology_route_config - $port_1" 
################################################################################
# OSPF START
################################################################################

set _result_ [::ixia::test_control -action start_all_protocols]
if {[keylget _result_ status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
}

puts "Starting emulation_ospf_config configuration elements for $port_1"

puts "emulation_ospf_config start sequence complete"


################################################################################
# Delete all the streams first
################################################################################
set traffic_status [::ixia::traffic_config \
        -mode        reset                 \
        -port_handle $port_handle          \
        -traffic_generator ixnetwork_540   ]
        
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

################################################################################
# Configure the IPv4 Traffic
################################################################################

set rate_start_value        30
set frame_size_start        512

set ti_srcs(EndpointSet-1)  $route_range_handle_port0
set ti_dsts(EndpointSet-1)  $route_range_handle_port1

set traffic_status [::ixia::traffic_config                                              \
        -traffic_generator                          ixnetwork_540                       \
        -mode                                       create                              \
        -circuit_endpoint_type                      ipv4                                \
        -track_by                                   endpoint_pair                       \
        -name                                       "IPV4_Traffic"                      \
        -endpointset_count                          1                                   \
        -emulation_src_handle                       $ti_srcs(EndpointSet-1)             \
        -emulation_dst_handle                       $ti_dsts(EndpointSet-1)             \
        -rate_percent                               $rate_start_value                   \
        -frame_size                                 $frame_size_start                   \
        -duration                                   10                                  \
        -l2_encap                                   ethernet_ii                         \
        -l3_protocol                                ipv4                                \
        -frame_sequencing                           enable                              \
        -frame_sequencing_mode                      rx_threshold                        ]
        
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}
################################################################################
# Port Set Factory Defaults
################################################################################

set reset_result [::ixia::reset_port                    \
        -mode              set_factory_defaults         \
        -port_handle       [list $port_0 $port_1]       ]

if {[keylget reset_result status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget reset_result log]"
    return 0
}

############################### SUCCESS or FAILURE #############################

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1

################################################################################