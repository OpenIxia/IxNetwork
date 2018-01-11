################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LBose $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-26-2013 LBose - Initial Version
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
#    This sample script creates the IGMP V1/V2/V3 queriers using two ports     #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#                                                                              #
################################################################################

package require Ixia

## Declare the Chassis IP address and the Ports that will be used
set test_name                   [info script]
set chassis_ip                  10.206.27.55
set tcl_server                  10.206.27.55
set ixnetwork_tcl_server        192.168.4.6
set port_list                   [list 10/1 10/2]

# Connect to the chassis, and load the configuration on ports using the 
# given IxNetwork configuration file. Also instruct not to load the 
# session resumes keys during connect.
set connect_status [::ixia::connect                      \
        -reset                                           \
        -device                 $chassis_ip              \
        -port_list              $port_list               \
        -ixnetwork_tcl_server   $ixnetwork_tcl_server    \
        -tcl_server             $tcl_server              \
]

if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_1 [keylget connect_status  \
    port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget connect_status  \
    port_handle.$chassis_ip.[lindex $port_list 1]]
set port_handle [list $port_1 $port_2] 

#################################################################################
#  Configure interfaces and create IGMP sessions                                # 
#################################################################################
puts "Configure IGMP v2 hosts"

set ip_router_alert         1
set host                    90.34.1.1
set query                   90.34.1.2
set vlan_id                 10
set vlan_id_step            1
set vlan_user_priority      4

set igmp_status [::ixia::emulation_igmp_config          \
        -port_handle           $port_1                  \
        -reset                                          \
        -mode                  create                   \
        -msg_interval          167                      \
        -igmp_version          v2                       \
        -ip_router_alert       $ip_router_alert         \
        -general_query         0                        \
        -group_query           0                        \
        -filter_mode           exclude                  \
        -count                 1                        \
        -intf_ip_addr          $host                    \
        -neighbor_intf_ip_addr $query                   \
        -intf_prefix_len       24                       \
        -vlan_id_mode          increment                \
        -vlan_id               $vlan_id                 \
        -vlan_id_step          $vlan_id_step            \
        -vlan_user_priority    $vlan_user_priority      \
        ]
if {[keylget igmp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status log]"
    return 0
}
set host_handle_v2 [keylget igmp_status handle]

puts "Create v2 IGMP group"
set session_handle      90.34.1.1
set mgroup_params       [list 226.0.2.1/0.0.0.1/5   226.0.2.6/0.0.0.2/4]
set msource_params      [list 100.0.2.2/0.0.0.2/2,110.0.2.2/0.0.0.1/3   \
             120.0.2.2/0.0.0.1/5,130.0.2.2/0.0.0.1/5,140.0.2.2/0.0.0.1/5]

set group_status_0 [::ixia::emulation_igmp_group_config \
        -mode                 create                    \
        -session_handle       $session_handle           \
        -group_pool_handle    $mgroup_params            \
        -source_pool_handle   $msource_params           \
        ]
if {[keylget group_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_status_0 log]"
    return 0
}
set group1_handle [keylget group_status_0 group_pool_handle]

#################################################################################
#                        IGMP v3 hosts                                          #
#################################################################################
puts "Configure IGMP v3 hosts"
set ip_router_alert         1
set host                    100.0.1.2
set query                   100.0.1.1
set vlan_id                 10
set vlan_id_step            1
set vlan_user_priority      4

set igmp_status [::ixia::emulation_igmp_config          \
        -port_handle           $port_1                  \
        -mode                  create                   \
        -msg_interval          167                      \
        -igmp_version          v3                       \
        -ip_router_alert       $ip_router_alert         \
        -general_query         0                        \
        -group_query           0                        \
        -filter_mode           exclude                  \
        -count                 1                        \
        -intf_ip_addr          $host                    \
        -neighbor_intf_ip_addr $query                   \
        -intf_prefix_len       20                       \
        -vlan_id_mode          increment                \
        -vlan_id               $vlan_id                 \
        -vlan_id_step          $vlan_id_step            \
        -vlan_user_priority    $vlan_user_priority      \
        ]
if {[keylget igmp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status log]"
    return 0
}
set host_handle_v3 [keylget igmp_status handle]

puts "Create IGMP v3 group"
set session_handle  100.0.1.2
set mgroup_params   [list 226.0.1.1/0.0.0.1/5   226.0.1.6/0.0.0.2/4]
set msource_params  [list 100.0.1.2/0.0.0.2/2,110.0.1.2/0.0.0.1/3   \
        120.0.1.2/0.0.0.1/5,130.0.1.2/0.0.0.1/5,140.0.1.2/0.0.0.1/5]

set group_status_0 [::ixia::emulation_igmp_group_config \
        -mode                 create                    \
        -session_handle       $session_handle           \
        -group_pool_handle    $mgroup_params            \
        -source_pool_handle   $msource_params           \
        ]
if {[keylget group_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_status_0 log]"
    return 0
}
set group2_handle [keylget group_status_0 group_pool_handle]
#################################################################################
#                   IGMP v1 hosts                                               #
#################################################################################
puts "Configure IGMP v1 hosts"
set ip_router_alert         1
set host                    40.0.1.2
set query                   40.0.1.1
set vlan_id                 20
set vlan_id_step            1
set vlan_user_priority      5

set igmp_status [::ixia::emulation_igmp_config          \
        -port_handle           $port_1                  \
        -mode                  create                   \
        -msg_interval          167                      \
        -igmp_version          v1                       \
        -ip_router_alert       $ip_router_alert         \
        -general_query         0                        \
        -group_query           0                        \
        -filter_mode           exclude                  \
        -count                 1                        \
        -intf_ip_addr          $host                    \
        -neighbor_intf_ip_addr $query                   \
        -intf_prefix_len       20                       \
        -vlan_id_mode          increment                \
        -vlan_id               $vlan_id                 \
        -vlan_id_step          $vlan_id_step            \
        -vlan_user_priority    $vlan_user_priority      \
        ]
if {[keylget igmp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status log]"
    return 0
}
set host_handle_v1 [keylget igmp_status handle]

puts "Configure IGMP v1 group"
set session_handle  40.0.1.2
set mgroup_params   [list 226.0.3.1/0.0.0.1/5   226.0.3.6/0.0.0.2/4]
set msource_params  [list 100.0.3.2/0.0.0.2/2,110.0.3.2/0.0.0.1/3   \
         120.0.3.2/0.0.0.1/5,130.0.3.2/0.0.0.1/5,140.0.3.2/0.0.0.1/5]

set group_status_0 [::ixia::emulation_igmp_group_config \
        -mode                 create                    \
        -session_handle       $session_handle           \
        -group_pool_handle    $mgroup_params            \
        -source_pool_handle   $msource_params           \
        ]
if {[keylget group_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_status_0 log]"
    return 0
}
set group3_handle [keylget group_status_0 group_pool_handle]

##############################################################################
#                       Create IGMP queriers                                 #
##############################################################################
puts "Configure IGMP v2 querier..."
set ip_router_alert         1
set host                    90.34.1.1
set query                   90.34.1.2
set vlan_id                 10
set vlan_id_step            1
set vlan_user_priority      4

set igmp_status [::ixia::emulation_igmp_querier_config              \
        -port_handle                            $port_2             \
        -mode                                   create              \
        -reset                                                      \
        -specific_query_response_interval       300                 \
        -robustness_variable                    2                   \
        -support_older_version_host             1                   \
        -support_older_version_querier          1                   \
        -support_election                       1                   \
        -specific_query_transmission_count      2                   \
        -startup_query_count                    2                   \
        -igmp_version                           v2                  \
        -discard_learned_info                   0                   \
        -general_query_response_interval        600                 \
        -msg_count_per_interval                 0                   \
        -msg_interval                           0                   \
        -count                                  1                   \
        -intf_ip_addr                           $query              \
        -neighbor_intf_ip_addr                  $host               \
        -intf_prefix_len                        20                  \
        -vlan_id_mode                           increment           \
        -vlan_id                                $vlan_id            \
        -vlan_id_step                           0                   \
        -vlan_user_priority                     $vlan_user_priority \
        -ip_router_alert                        1                   \
        -mac_address_init                       0002.c1cc.ddd0      \
        -mac_address_step                       0000.0000.0001      \
        -override_existence_check               1                   \
        -override_tracking                      1                   \
        -vci                                    3400                \
        -vci_step                               535                 \
        -vpi                                    100                 \
        -vpi_step                               90                  \
        -query_interval                         450                 \
        ]
if {[keylget igmp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status log]"
    return 0
}
set query_handle_v2 [keylget igmp_status handle]
##############################################################################
#        IGMPv3 queriers                                                     #
##############################################################################

puts "Configure IGMP v3 querier..."
set ip_router_alert         1
set host                    100.0.1.2
set query                   100.0.1.1
set vlan_id                 10
set vlan_id_step            1
set vlan_user_priority      4

set igmp_status [::ixia::emulation_igmp_querier_config          \
        -port_handle                        $port_2             \
        -mode                               create              \
        -specific_query_response_interval   300                 \
        -robustness_variable                4                   \
        -support_older_version_host         1                   \
        -support_older_version_querier      1                   \
        -support_election                   1                   \
        -specific_query_transmission_count  4                   \
        -startup_query_count                1                   \
        -igmp_version                       v3                  \
        -discard_learned_info               0                   \
        -general_query_response_interval    4200                \
        -msg_count_per_interval             9                   \
        -msg_interval                       4                   \
        -count                              1                   \
        -intf_ip_addr                       $query              \
        -neighbor_intf_ip_addr              $host               \
        -intf_prefix_len                    24                  \
        -vlan_id_mode                       increment           \
        -vlan_id                            $vlan_id            \
        -vlan_id_step                       $vlan_id_step       \
        -vlan_user_priority                 $vlan_user_priority \
        -ip_router_alert                    1                   \
        -mac_address_init                   00ab.cccc.ddd0      \
        -mac_address_step                   0000.0000.0001      \
        -override_existence_check           1                   \
        -override_tracking                  1                   \
        -vci                                3400                \
        -vci_step                           535                 \
        -vpi                                100                 \
        -vpi_step                           90                  \
        -query_interval                     30                  \
]

if {[keylget igmp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status log]"
    return 0
}
set query_handle_v3 [keylget igmp_status handle]
##############################################################################
#   IGMPv1 queriers                                                          #
##############################################################################
puts "Configure IGMP v1 querier..."
set ip_router_alert         1
set host                    40.0.1.2
set query                   40.0.1.1
set vlan_id                 20
set vlan_id_step            1
set vlan_user_priority      5

set igmp_status [::ixia::emulation_igmp_querier_config          \
        -port_handle                        $port_2             \
        -mode                               create              \
        -specific_query_response_interval   100                 \
        -robustness_variable                1                   \
        -support_older_version_host         1                   \
        -support_older_version_querier      1                   \
        -support_election                   1                   \
        -specific_query_transmission_count  4                   \
        -startup_query_count                1                   \
        -igmp_version                       v1                  \
        -discard_learned_info               0                   \
        -general_query_response_interval    4200                \
        -msg_count_per_interval             7                   \
        -msg_interval                       3                   \
        -count                              1                   \
        -intf_ip_addr                       $query              \
        -neighbor_intf_ip_addr              $host               \
        -intf_prefix_len                    24                  \
        -vlan_id_mode                       increment           \
        -vlan_id                            $vlan_id            \
        -vlan_id_step                       $vlan_id_step       \
        -vlan_user_priority                 $vlan_user_priority \
        -ip_router_alert                    1                   \
        -mac_address_init                   00ab.0ccc.ddd0      \
        -mac_address_step                   0000.0000.0001      \
        -override_existence_check           1                   \
        -override_tracking                  1                   \
        -vci                                3400                \
        -vci_step                           335                 \
        -vpi                                200                 \
        -vpi_step                           40                  \
        -query_interval                     20                  \
]

if {[keylget igmp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status log]"
    return 0
}
set query_handle_v1 [keylget igmp_status handle]

##############################################################################
#                             Start IGMP                                     #
##############################################################################
puts "Start protocol..."
set  query_handle [list $query_handle_v1 $query_handle_v2 $query_handle_v3]

set igmp_status [::ixia::emulation_igmp_control     \
        -mode       start                           \
        -handle     $query_handle                   \
]

if {[keylget igmp_status status] != $::SUCCESS} {
    puts "Error - Starting querier"        
}

set host_handle [list $host_handle_v3 $host_handle_v2 $host_handle_v1]

after 10000

##############################################################################
#                           Restart IGMP queriers                            #
##############################################################################
puts "Restart IGMP querier"
set igmp_status [::ixia::emulation_igmp_control \
        -mode   restart                         \
        -handle	$query_handle                   \
]

if {[keylget igmp_status status] != $::SUCCESS} {
    puts "Error - Starting querier"    
}

##############################################################################
#                           Join/Leave IGMP host                             #
##############################################################################
puts "Leave IGMP host"
set igmp_status [::ixia::emulation_igmp_control \
        -mode   leave                           \
        -handle	$host_handle                    \
]

if {[keylget igmp_status status] != $::SUCCESS} {
    puts "Error - starting hosts"    
}

after 5000
puts "Join IGMP host"

set igmp_status [::ixia::emulation_igmp_control \
        -mode       join                        \
        -handle     $host_handle                \
]

if {[keylget igmp_status status] != $::SUCCESS} {
    puts "Error - starting hosts"    
}

##############################################################################
#                           Stop IGMP                                        #
##############################################################################

after 5000
puts "Stop IGMP"

set igmp_status [::ixia::emulation_igmp_control \
        -mode       stop                        \
        -handle     $query_handle               \
]

if {[keylget igmp_status status] != $::SUCCESS} {
    puts "Error - Stopping querier"    
}

set igmp_status [::ixia::emulation_igmp_control \
        -mode       stop                        \
        -handle     $host_handle                \
]

if {[keylget igmp_status status] != $::SUCCESS} {
    puts "Error - Stopping hosts"
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1



