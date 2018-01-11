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
#    This sample configures a scenario with a dhcpv6 server and a dhcpv6       #
#    client behind a dhcpv6 relay agent                                        #
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

    set dhcpv6_status [::ixiangpf::emulation_dhcp_group_config \
        -dhcp_range_ip_type                 ipv6                    \
        -handle                             $topology_1_handle      \
        -protocol_name                      {DHCPv6 Client 1}       \
        -num_sessions                       3                       \
        -dhcp_range_renew_timer             0                       \
        -dhcp_range_server_address          2000:0:0:0:0:0:0:1      \
        -dhcp_range_use_first_server        1                       \
        -use_rapid_commit                   0                       \
        -dhcp4_broadcast                    0                       \
        -mac_addr                           00.11.01.00.00.01       \
        -mac_addr_step                      00.00.00.00.00.01       \
        -mac_mtu                            1500                    \
        -dhcp_range_use_relay_agent         1                       \
        -dhcp_range_relay_count             1                       \
        -dhcp_range_relay_destination       2000:0:0:0:0:0:0:1      \
        -dhcp_range_relay_first_address     3000:0:0:1:0:0:0:1      \
        -dhcp_range_relay_address_increment 0:0:0:1:0:0:0:0         \
    ]
    if {[keylget dhcpv6_status status] != $::SUCCESS} {
        errorHandler [info script] $dhcpv6_status
    }
    set dhcpv6relayAgent_handle [keylget dhcpv6_status dhcpv6relayagent_handle]
    set dhcpv6client_handle [keylget dhcpv6_status dhcpv6client_handle]


    return [list \
        $dhcpv6relayAgent_handle    \
        $dhcpv6client_handle        \
    ]
}
proc setup_dhcp_server {topology_2_handle} {
    ############################################
    ## dhcpv6 server device group
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
    ## ipv6
    ############################################

    set ipv6_status [::ixiangpf::interface_config \
        -protocol_name                {IPv6 1}                  \
        -protocol_handle              $ethernet_handle          \
        -ipv6_multiplier              1                         \
        -ipv6_resolve_gateway         1                         \
        -ipv6_manual_gateway_mac      00.00.00.00.00.01         \
        -ipv6_gateway                 2000:0:0:0:0:0:0:2        \
        -ipv6_gateway_step            0:0:0:0:0:0:0:1           \
        -ipv6_intf_addr               2000:0:0:0:0:0:0:1        \
        -ipv6_prefix_length           64                        \
    ]
    if {[keylget ipv6_status status] != $::SUCCESS} {
        errorHandler [info script] $ipv6_status
    }
    set ipv6_handle [keylget ipv6_status ipv6_handle]

    ############################################
    ## dhcpv6 server
    ############################################
    set mv_ipaddress_pool_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          a1a1:0:0:0:0:0:0:0      \
        -counter_step           0:1:0:0:0:0:0:0         \
        -counter_direction      increment               \
        -nest_step              0:1:0:0:0:0:0:0         \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
    if {[keylget mv_ipaddress_pool_status status] != $::SUCCESS} {
        errorHandler [info script] $mv_ipaddress_pool_status
    }
    set mv_ipaddress_pool_handle [keylget mv_ipaddress_pool_status multivalue_handle]

    set mv_start_pool_prefix_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          a1a1:0:0:0:0:0:0:0      \
        -counter_step           0:1:0:0:0:0:0:0         \
        -counter_direction      increment               \
        -nest_step              0:1:0:0:0:0:0:0         \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
    if {[keylget mv_start_pool_prefix_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $mv_start_pool_prefix_status
    }
    set mv_start_pool_prefix_handle [keylget mv_start_pool_prefix_status multivalue_handle]
    
    set mv_pool_prefix_size_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          3                       \
        -counter_step           0                       \
        -counter_direction      increment               \
        -nest_step              1                       \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           0                       \
    ]
    if {[keylget mv_pool_prefix_size_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $mv_pool_prefix_size_status
    }
    set mv_pool_prefix_size_handle [keylget mv_pool_prefix_size_status multivalue_handle]

    set dhcpv6server_status [::ixiangpf::emulation_dhcp_server_config \
        -dhcp6_ia_type                     iapd                         \
        -handle                            $ipv6_handle                 \
        -ip_dns1                           fffe:0:0:0:0:0:0:0           \
        -ip_dns1_step                      0:0:0:0:0:0:0:0              \
        -ip_dns2                           eeef:0:0:0:0:0:0:0           \
        -ip_dns2_step                      0:0:0:0:0:0:0:0              \
        -ip_version                        6                            \
        -ipaddress_count                   1                            \
        -ipaddress_pool                    $mv_ipaddress_pool_handle    \
        -ipaddress_pool_prefix_length      64                           \
        -lease_time                        86400                        \
        -mode                              create                       \
        -protocol_name                     {DHCPv6 Server 1}            \
        -use_rapid_commit                  0                            \
        -pool_address_increment            0:0:0:0:0:0:0:1              \
        -start_pool_prefix                 $mv_start_pool_prefix_handle \
        -pool_prefix_increment             1:0:0:0:0:0:0:0              \
        -pool_prefix_size                  $mv_pool_prefix_size_handle  \
        -prefix_length                     64                           \
        -custom_renew_time                 34560                        \
        -custom_rebind_time                55296                        \
        -use_custom_times                  0                            \
    ]
    if {[keylget dhcpv6server_status status] != $::SUCCESS} {
        errorHandler [info script] $dhcpv6server_status
    }
    set dhcpv6server_handle [keylget dhcpv6server_status dhcpv6server_handle]

    ############################################
    ## dhcpv6 server global options
    ############################################
    set dhcpv6server_status [::ixiangpf::emulation_dhcp_server_config \
        -handle            /globals      \
        -ip_version        6             \
        -mode              create        \
        -ping_check        0             \
        -ping_timeout      1             \
    ]
    if {[keylget dhcpv6server_status status] != $::SUCCESS} {
        errorHandler [info script] $dhcpv6server_status
    }

    return [list \
        $deviceGroup_handle     \
        $ethernet_handle        \
        $ipv6_handle            \
        $dhcpv6server_handle    \
    ]
}

############################################
## config 2 device groups in Topology 1
## one dhcp relay agent and one dhcp client
############################################
set topology_1_handle [setup_topology "Topology 1" $port_1]
set ret [setup_dhcp_client_and_relay_agent $topology_1_handle]
set dhcpv6relayAgent_1_handle   [lindex $ret 0]
set dhcpv6client_1_handle       [lindex $ret 1]

############################################
## config 1 device group in Topology 2
## the dhcp server
############################################
set topology_2_handle [setup_topology "Topology 2" $port_2]
set ret [setup_dhcp_server $topology_2_handle]
set deviceGroup_3_handle    [lindex $ret 0]
set ethernet_3_handle       [lindex $ret 1]
set ipv6_2_handle           [lindex $ret 2]
set dhcpv6server_1_handle   [lindex $ret 3]

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
    -handle $dhcpv6relayAgent_1_handle      \
]
if {[keylget ret status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ret log]"
    return 0
}
puts "Dhcp relay agent aggregate stats for $dhcpv6relayAgent_1_handle"
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