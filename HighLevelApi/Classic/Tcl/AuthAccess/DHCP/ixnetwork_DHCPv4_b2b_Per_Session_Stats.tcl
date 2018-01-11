################################################################################
# Version 1.0    $Revision: 1 $
# $Author: $
#
#    Copyright © 1997 - 2010 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#
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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 10.205.16.65
set port_list [list 3/1 3/2]


# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassisIP      \
        -port_list              $port_list      \
        -username               cnicutar        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_array [keylget connect_status port_handle.$chassisIP]

set port0 [keylget port_array [lindex $port_list 0]]
set port1 [keylget port_array [lindex $port_list 1]]

set interface_status [::ixia::interface_config                           \
        -mode                                       config               \
        -port_handle                                $port0               \
        -data_integrity                             1                    \
        -intf_mode                                  ethernet             \
        -speed                                      auto                 \
        -transmit_mode                              advanced             \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure DHCP client session
################################################################################

set dhcp_portHandle_status [::ixia::emulation_dhcp_config                \
        -version                                    ixnetwork            \
        -reset                                                           \
        -mode                                       create               \
        -port_handle                                $port0               \
        -lease_time                                 300                  \
        -max_dhcp_msg_size                          1000                 \
]
if {[keylget dhcp_portHandle_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dhcp_portHandle_status log]"
}
set dhcp_client_session_handle [keylget dhcp_portHandle_status handle]


################################################################################
# Configure DHCP client group
################################################################################
set dhcp_group_status [::ixia::emulation_dhcp_group_config          \
        -version                ixnetwork                           \
        -mode                   create                              \
        -handle                 $dhcp_client_session_handle         \
        -num_sessions           10                                  \
        -encap                  ethernet_ii_qinq                    \
        -vlan_id_outer          100                                 \
        -vlan_id_outer_count    1                                   \
        -vlan_id                10                                  \
        -vlan_id_count          1                                   \
        ]
if {[keylget dhcp_group_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dhcp_group_status log]"
}

set dhcp_client_group_handle [keylget dhcp_group_status handle]

################################################################################
# DHCP Server configuration
################################################################################
set dhcp_server_config_status [::ixia::emulation_dhcp_server_config            \
        -count                                       3                         \
        -encapsulation                               ETHERNET_II               \
        -handle                                      $dhcp_client_group_handle \
        -ip_address                                  10.10.0.1                 \
        -ip_gateway                                  10.10.0.2                 \
        -ip_prefix_length                            16                        \
        -ip_prefix_step                              0.0.1.0                   \
        -ip_repeat                                   1                         \
        -ip_step                                     0.1.0.0                   \
        -ipaddress_count                             100                       \
        -ipaddress_pool                              10.10.1.1                 \
        -lease_time                                  86400                     \
        -local_mac                                   0000.0001.0001            \
        -mode                                        create                    \
        -port_handle                                 $port1                    \
        -vlan_id                                     100                       \
        -ipaddress_pool_step                         0.1.0.0                   \
        -ip_dns1                                     10.10.0.2                 \
        -ip_dns1_step                                0.1.0.0                   \
        -ip_dns2                                     10.10.0.3                 \
        -ip_dns2_step                                0.1.0.0                   \
        -ip_gateway_step                             0.1.0.0                   \
        -ip_version                                  4                         \
        -lease_time_max                              864000                    \
        -local_mac_step                              0000.0000.0001            \
        -local_mac_outer_step                        0000.0001.0000            \
        -local_mtu                                   1500                      \
        -pvc_incr_mode                               both                      \
        -qinq_incr_mode                              both                      \
        -ping_check                                  0                         \
        -ping_timeout                                1                         \
        -single_address_pool                         0                         \
        -vlan_id_count                               1                         \
        -vlan_id_count_inner                         1                         \
        -vlan_id_inner                               10                        \
        -vlan_id_repeat                              1                         \
        -vlan_id_repeat_inner                        1                         \
        -vlan_id_step                                1                         \
        -vlan_id_inter_device_step                   100                       \
        -vlan_id_step_inner                          1                         \
        -vlan_id_inner_inter_device_step             10                        \
        -vlan_user_priority                          0                         \
        -vlan_user_priority_inner                    0                         \
        -vci                                         32                        \
        -vci_count                                   4063                      \
        -vci_repeat                                  1                         \
        -vci_step                                    1                         \
        -vpi                                         0                         \
        -vpi_count                                   1                         \
        -vpi_repeat                                  1                         \
        -vpi_step                                    1                         \
]
if {[keylget dhcp_server_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dhcp_server_config_status log]"
    return
}
set dhcp_server_handles [keylget dhcp_server_config_status handle.dhcp_handle]

################################################################################
# START DHCP
################################################################################
set control_status_1 [::ixia::emulation_dhcp_server_control \
        -port_handle      $port1                            \
        -action           collect                           \
        ]
if {[keylget control_status_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status_1 log]"
    return 0
}

set control_status_0 [::ixia::emulation_dhcp_control \
        -port_handle      $port0                     \
        -action           bind                       \
        ]
if {[keylget control_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status_0 log]"
    return 0
}

after 30000

##################################################
#             GET DHCP STATISTICS                #
##################################################
set dhcp_stats_0 [::ixia::emulation_dhcp_stats        \
        -port_handle $port0                           \
        -version     ixnetwork                        \
        ]
if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name -[keylget dhcp_stats_0 log]"
    return 0
}

set dhcp_stats_1 [::ixia::emulation_dhcp_server_stats  \
        -port_handle $port1                            \
        -action      collect                           \
        ]
if {[keylget dhcp_stats_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name -[keylget dhcp_stats_1 log]"
    return 0
}
##################################################
#            PRINT DHCP STATISTICS               #
##################################################
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

################################################################################
# Retrieve per session stats
################################################################################

after 10000

array set stats_array_per_session {
    session_name
        "Session Name"
    port_handle
        "Port"
    dhcp_group
        "DHCP Group"
    discovers_sent
        "Discovers sent"
    offers_received
        "Offers received"
    requests_sent
        "Requests sent"
    acks_received
        "Acks received"
    nacks_received
        "Nacks received"
    releases_sent
        "Releases sent"
    declines_sent
        "Declines sent"
    ip_address
        "IP Address"
    gateway_address
        "Gateway address"
    lease_time
        "Lease time"
}
puts [string repeat "#" 80]
puts "Per session stats:"
puts [string repeat "#" 80]
puts ""
set sess_status [::ixia::emulation_dhcp_stats       \
        -port_handle $port0                         \
        -mode        session                        \
        -version     ixnetwork                      \
        ]
if {[keylget sess_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget sess_status log]"
    return 0
}
############################ CHECKING PER SESSION STATS ########################
set all_ok 1
set ok_log [list]
foreach key_1 [keylkeys sess_status session] {
    puts "Session $key_1"
    puts [string repeat "#" 40]
    set target_statistics [keylget sess_status session.$key_1]
    foreach key_2 [keylkeys target_statistics] {
        set current_value [keylget target_statistics $key_2]
        puts "[format %-40s $key_2]: $current_value"
        if {[string first "ip_addr" $key_2] >= 0} {
            # Validate ip addresses...
            set matched [regexp {([0-9]+).([0-9]+).([0-9]+).([0-9]+)$} $current_value matched_str ip1 ip2 ip3 ip4]
            if {$matched} {
                lappend ok_log $current_value
            } else {
                set all_ok 0
                set ok_log "IP address not matched: $current_value !"
            }
        }
    }
}

################################################################################

puts [string repeat "#" 80]
puts "Per session stats:"
puts [string repeat "#" 80]
puts ""
set sess_status [::ixia::emulation_dhcp_stats       \
        -handle      $dhcp_client_group_handle     \
        -mode        session                        \
        -version     ixnetwork                      \
        ]
if {[keylget sess_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget sess_status log]"
    return 0
}

############################ CHECKING PER SESSION STATS ########################
foreach key_1 [keylkeys sess_status session] {
    puts "Session $key_1"
    puts [string repeat "#" 40]
    set target_statistics [keylget sess_status session.$key_1]
    foreach key_2 [keylkeys target_statistics] {
        set current_value [keylget target_statistics $key_2]
        puts "[format %-40s $key_2]: $current_value"
        if {[string first "ip_addr" $key_2] >= 0} {
            # Validate ip addresses...
            set matched [regexp {([0-9]+).([0-9]+).([0-9]+).([0-9]+)$} $current_value matched_str ip1 ip2 ip3 ip4]
            if {$matched} {
                lappend ok_log $current_value
            } else {
                set all_ok 0
                set ok_log "IP address not matched: $current_value !"
            }
        }
    }
}

return 0
################################################################################