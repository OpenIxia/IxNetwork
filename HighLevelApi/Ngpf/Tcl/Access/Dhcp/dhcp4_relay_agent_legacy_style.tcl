################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Adrian Enache $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-29-2013 Adrian Enache
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
#    This sample configures a scenario with a dhcpv4 server and a dhcpv4       #
#    client behind a dhcpv4 relay agent                                        #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10GE LSM XM3 module.                           #
#                                                                              #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}
set test_name                   [info script]
set chassis_ip                  ixro-hlt-xm2-03
set tcl_server                  ixro-hlt-xm2-03
set ixnetwork_tcl_server        127.0.0.1:8009
set port_list                   [list 1/1 1/2]

set connect_status [::ixiangpf::connect             \
    -reset                                          \
    -device                 $chassis_ip             \
    -port_list              $port_list              \
    -ixnetwork_tcl_server   $ixnetwork_tcl_server   \
    -tcl_server             $tcl_server             \
]

if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]
set port_handle [list $port_1 $port_2] 

puts "Connected..."

proc keylprint {var_ref} {
    upvar 1 $var_ref var
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
        set indent [string repeat "    " $level]
        puts -nonewline $indent 
        if {[catch {keylkeys var $key} catch_rval] || [llength $catch_rval] == 0} {
            puts "$key: [keylget var $key]"
            continue
        } else {
            puts $key
            puts "$indent[string repeat "-" [string length $key]]"
        }
        set rec_key [keylget var $key]
        keylprint rec_key
        puts ""
    }
}
proc errorHandler {module status} {
    set msg "FAIL - $module - [keylget status log]"
    puts $msg
    return -code error $msg
}

proc setup_topology {name port_handle} {
    set topology_status [::ixiangpf::topology_config \
        -topology_name      $name             \
        -port_handle        $port_handle      \
    ]
    if {[keylget topology_status status] != $::SUCCESS} {
        errorHandler [info script] $topology_status
    }
    return [keylget topology_status topology_handle]
}
proc setup_dhcp_client_and_relay_agent {topology_1_handle} {
    ############################################
    ## dhcpv4 relay agent + client (and lower stacks)
    ############################################

    set dhcpv4_status [::ixiangpf::emulation_dhcp_group_config \
        -dhcp_range_ip_type                 ipv4                    \
        -handle                             $topology_1_handle      \
        -protocol_name                      {DHCPv4 Client 1}       \
        -num_sessions                       3                       \
        -dhcp_range_renew_timer             0                       \
        -dhcp_range_server_address          10.10.0.1               \
        -dhcp_range_use_first_server        1                       \
        -use_rapid_commit                   0                       \
        -dhcp4_broadcast                    0                       \
        -mac_addr                           00.11.01.00.00.01       \
        -mac_addr_step                      00.00.00.00.00.01       \
        -mac_mtu                            1500                    \
        -dhcp_range_use_relay_agent         1                       \
        -dhcp_range_relay_count             1                       \
        -dhcp_range_relay_destination       100.0.0.1               \
        -dhcp_range_relay_first_address     150.0.0.1               \
        -dhcp_range_relay_address_increment 0.1.0.0                 \
    ]
    if {[keylget dhcpv4_status status] != $::SUCCESS} {
        errorHandler [info script] $dhcpv4_status
    }
    set dhcpv4relayAgent_handle [keylget dhcpv4_status dhcpv4relayagent_handle]
    set dhcpv4client_handle [keylget dhcpv4_status dhcpv4client_handle]

    ############################################
    ## dhcp client global options
    ############################################
    set mv_outstanding_releases_count_status [::ixiangpf::multivalue_config \
        -pattern                distributed      \
        -distributed_value      400              \
    ]
    if {[keylget mv_outstanding_releases_count_status status] != $::SUCCESS} {
        errorHandler [info script] $mv_outstanding_releases_count_status
    }
    set mv_outstanding_releases_count_handle [keylget mv_outstanding_releases_count_status multivalue_handle]

    set mv_release_rate_status [::ixiangpf::multivalue_config \
        -pattern                distributed      \
        -distributed_value      200              \
    ]
    if {[keylget mv_release_rate_status status] != $::SUCCESS} {
        errorHandler [info script] $mv_release_rate_status
    }
    set mv_release_rate_handle [keylget mv_release_rate_status multivalue_handle]

    set mv_outstanding_session_count_status [::ixiangpf::multivalue_config \
        -pattern                distributed      \
        -distributed_value      400              \
    ]
    if {[keylget mv_outstanding_session_count_status status] != $::SUCCESS} {
        errorHandler [info script] $mv_outstanding_session_count_status
    }
    set mv_outstanding_session_count_handle [keylget mv_outstanding_session_count_status multivalue_handle]

    set mv_request_rate_status [::ixiangpf::multivalue_config \
        -pattern                distributed      \
        -distributed_value      200              \
    ]
    if {[keylget mv_request_rate_status status] != $::SUCCESS} {
        errorHandler [info script] $mv_request_rate_status
    }
    set mv_request_rate_handle [keylget mv_request_rate_status multivalue_handle]

    set mv_min_lifetime_status [::ixiangpf::multivalue_config \
        -pattern                distributed      \
        -distributed_value      1                \
    ]
    if {[keylget mv_min_lifetime_status status] != $::SUCCESS} {
        errorHandler [info script] $mv_min_lifetime_status
    }
    set mv_min_lifetime_handle [keylget mv_min_lifetime_status multivalue_handle]

    set mv_max_restarts_status [::ixiangpf::multivalue_config \
        -pattern                distributed      \
        -distributed_value      10               \
    ]
    if {[keylget mv_max_restarts_status status] != $::SUCCESS} {
        errorHandler [info script] $mv_max_restarts_status
    }
    set mv_max_restarts_handle [keylget mv_max_restarts_status multivalue_handle]

    set mv_max_lifetime_status [::ixiangpf::multivalue_config \
        -pattern                distributed      \
        -distributed_value      10               \
    ]
    if {[keylget mv_max_lifetime_status status] != $::SUCCESS} {
        errorHandler [info script] $mv_max_lifetime_status
    }
    set mv_max_lifetime_handle [keylget mv_max_lifetime_status multivalue_handle]

    set dhcpv4client_2_status [::ixiangpf::emulation_dhcp_config \
        -handle                             /globals                                \
        -mode                               create                                  \
        -msg_timeout                        4                                       \
        -outstanding_releases_count         $mv_outstanding_releases_count_handle   \
        -outstanding_session_count          $mv_outstanding_session_count_handle    \
        -release_rate                       $mv_release_rate_handle                 \
        -request_rate                       $mv_request_rate_handle                 \
        -retry_count                        3                                       \
        -client_port                        68                                      \
        -start_scale_mode                   port                                    \
        -stop_scale_mode                    port                                    \
        -interval_stop                      1000                                    \
        -interval_start                     1000                                    \
        -min_lifetime                       $mv_min_lifetime_handle                 \
        -max_restarts                       $mv_max_restarts_handle                 \
        -max_lifetime                       $mv_max_lifetime_handle                 \
        -enable_restart                     0                                       \
        -enable_lifetime                    0                                       \
        -unlimited_restarts                 0                                       \
        -server_port                        67                                      \
        -msg_timeout_factor                 2                                       \
        -override_global_setup_rate         1                                       \
        -override_global_teardown_rate      1                                       \
        -skip_release_on_stop               0                                       \
        -renew_on_link_up                   0                                       \
        -ip_version                         4                                       \
    ]
    if {[keylget dhcpv4client_2_status status] != $::SUCCESS} {
        errorHandler [info script] $dhcpv4client_2_status
    }

    return [list \
        $dhcpv4relayAgent_handle    \
        $dhcpv4client_handle        \
    ]
}
proc setup_dhcp_server {topology_2_handle} {
    ############################################
    ## dhcpv4 server device group
    ############################################
    set device_group_status [::ixiangpf::topology_config \
        -topology_handle              $topology_2_handle      \
        -device_group_name            {Device Group 3}        \
        -device_group_multiplier      1                       \
        -device_group_enabled         1                       \
    ]
    if {[keylget device_group_status status] != $::SUCCESS} {
        errorHandler [info script] $device_group_status
    }
    set deviceGroup_handle [keylget device_group_status device_group_handle]

    ############################################
    ## ethernet
    ############################################
    set mv_src_mac_addr_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          00.13.01.00.00.01       \
        -counter_step           00.00.00.00.00.01       \
        -counter_direction      increment               \
        -nest_step              00.00.01.00.00.00       \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
    if {[keylget mv_src_mac_addr_status status] != $::SUCCESS} {
        errorHandler [info script] $mv_src_mac_addr_status
    }
    set mv_src_mac_addr_handle [keylget mv_src_mac_addr_status multivalue_handle]

    set ethernet_status [::ixiangpf::interface_config \
        -protocol_name                {Ethernet 3}               \
        -protocol_handle              $deviceGroup_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 $mv_src_mac_addr_handle    \
        -vlan                         0                          \
        -vlan_id                      1                          \
        -vlan_id_step                 0                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
    ]
    # n Node: vpnParameter is not supported for scriptgen.
    if {[keylget ethernet_status status] != $::SUCCESS} {
        errorHandler [info script] $ethernet_status
    }
    set ethernet_handle [keylget ethernet_status ethernet_handle]

    ############################################
    ## ipv4
    ############################################

    set ipv4_status [::ixiangpf::interface_config \
        -protocol_name                {IPv4 2}                  \
        -protocol_handle              $ethernet_handle          \
        -ipv4_resolve_gateway         1                         \
        -ipv4_manual_gateway_mac      00.00.00.00.00.01         \
        -gateway                      100.0.0.2                 \
        -gateway_step                 0.0.0.1                   \
        -intf_ip_addr                 100.0.0.1                 \
        -netmask                      255.255.255.0             \
    ]
    if {[keylget ipv4_status status] != $::SUCCESS} {
        errorHandler [info script] $ipv4_status
    }
    set ipv4_handle [keylget ipv4_status ipv4_handle]

    ############################################
    ## dhcpv4 server
    ############################################
    set mv_ipaddress_pool_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          150.0.0.5               \
        -counter_step           0.1.0.0                 \
        -counter_direction      increment               \
        -nest_step              0.1.0.0                 \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
    if {[keylget mv_ipaddress_pool_status status] != $::SUCCESS} {
        errorHandler [info script] $mv_ipaddress_pool_status
    }
    set mv_ipaddress_pool_handle [keylget mv_ipaddress_pool_status multivalue_handle]

    set dhcpv4server_status [::ixiangpf::emulation_dhcp_server_config \
        -dhcp_offer_router_address         0.0.0.0                   \
        -handle                            $ipv4_handle              \
        -ip_dns1                           0.0.0.0                   \
        -ip_dns2                           0.0.0.0                   \
        -ip_version                        4                         \
        -ipaddress_count                   50                        \
        -ipaddress_pool                    $mv_ipaddress_pool_handle \
        -ipaddress_pool_prefix_length      16                        \
        -lease_time                        86400                     \
        -mode                              create                    \
        -protocol_name                     {DHCPv4 Server 1}         \
        -use_rapid_commit                  0                         \
        -echo_relay_info                   1                         \
        -pool_address_increment            0.0.0.1                   \
    ]
    if {[keylget dhcpv4server_status status] != $::SUCCESS} {
        errorHandler [info script] $dhcpv4server_status
    }
    set dhcpv4server_handle [keylget dhcpv4server_status dhcpv4server_handle]

    ############################################
    ## dhcpv4 server global options
    ############################################
    set dhcpv4server_status [::ixiangpf::emulation_dhcp_server_config \
        -handle            /globals      \
        -ip_version        4             \
        -mode              create        \
        -ping_check        0             \
        -ping_timeout      1             \
    ]
    if {[keylget dhcpv4server_status status] != $::SUCCESS} {
        errorHandler [info script] $dhcpv4server_status
    }

    return [list \
        $deviceGroup_handle     \
        $ethernet_handle        \
        $ipv4_handle            \
        $dhcpv4server_handle    \
    ]
}

############################################
## config 2 device groups in Topology 1
## one dhcp relay agent and one dhcp client
############################################
set topology_1_handle [setup_topology "Topology 1" $port_1]
set ret [setup_dhcp_client_and_relay_agent $topology_1_handle]
set dhcpv4relayAgent_1_handle   [lindex $ret 0]
set dhcpv4client_1_handle       [lindex $ret 1]

############################################
## config 1 device group in Topology 2
## the dhcp server
############################################
set topology_2_handle [setup_topology "Topology 2" $port_2]
set ret [setup_dhcp_server $topology_2_handle]
set deviceGroup_3_handle    [lindex $ret 0]
set ethernet_3_handle       [lindex $ret 1]
set ipv4_2_handle           [lindex $ret 2]
set dhcpv4server_1_handle   [lindex $ret 3]

############################################
## start all protocols
############################################
set ret [::ixiangpf::test_control -action start_all_protocols]
if {[keylget ret status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ret log]"
    return 0
}
after 30000

############################################
## get aggregate stats for dhcp relay agent
############################################
set ret [::ixiangpf::emulation_dhcp_stats   \
    -mode aggregate_stats_relay_agent       \
    -handle $dhcpv4relayAgent_1_handle      \
]
if {[keylget ret status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ret log]"
    return 0
}
puts "Dhcp relay agent aggregate stats for $dhcpv4relayAgent_1_handle"
keylprint ret

############################################
## stop all protocols
############################################
set ret [::ixiangpf::test_control -action stop_all_protocols]
if {[keylget ret status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ret log]"
    return 0
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"