#################################################################################
# Version 1    $Revision: 3 $
# $Author: Dkhandelwal $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    08-15-2013 Dhiraj Khandelwal - created sample
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
#   This sample configures BFD standalone and performs following               #
#           - Start All BFD Interfaces                                         #
#           - Fetch Stats and Learned Info                                     #
#           - Set Admin down and Set admin Up                                  #
#           - Change attributes OTF                                            #
#           - Disable/Enable BFD Interfaces                                    #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
# General script variables
################################################################################
set test_name                                   [info script]


proc setup_topology {name port_handle} {
    set topology_status [::ixiangpf::topology_config \
        -topology_name      $name             \
        -port_handle        $port_handle      \
    ]
    if {[keylget topology_status status] != $::SUCCESS} {
        error $topology_status
    }
    return [keylget topology_status topology_handle]
}

################################################################################
# START - Connect to the chassis
################################################################################
puts "Starting - $test_name - [clock format [clock seconds]]"
puts "Start connecting to chassis ..."
set chassis_ip              10.216.108.130
set port_list               [list 12/1 12/2]
set break_locks             1
set tcl_server              10.216.108.130
set ixnetwork_tcl_server    10.216.108.86:8237
set port_count              2
set cfgErrors               0

set rval [ixia::connect                             \
    -reset                                          \
    -device                 $chassis_ip             \
    -port_list              $port_list              \
    -ixnetwork_tcl_server   $ixnetwork_tcl_server   \
    -tcl_server             $tcl_server             \
]
if {[keylget rval status] != $::SUCCESS} {
    error "connect failed: [keylget rval log]"
}

set port_1 [keylget rval port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget rval port_handle.$chassis_ip.[lindex $port_list 1]]


set otf [ixNet getRoot]/globals/topology

puts "-------- >yo > $port_1"
set port_list [list $port_1 $port_2]

puts "Connect to the chassis complete."

#########################################################################################################################
##                                                     Topology 1 Config                                               ##
#########################################################################################################################

set topology_1_handle [setup_topology "Topology 1" $port_1]

#########################################################################################################################
##                                                     Device Group 1 Config                                           ##
#########################################################################################################################

set device_group_1_status [::ixiangpf::topology_config      \
    -topology_handle              $topology_1_handle        \
    -device_group_name            {D1}                      \
    -device_group_multiplier      2                         \
    -device_group_enabled         1                         \
]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    error $device_group_1_status
}

set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

############################################
## Ethernet Config
############################################

set multivalue_1_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.11.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_1_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_1_status"
}
set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]

set ethernet_1_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 1}               \
    -protocol_handle              $deviceGroup_1_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_1_handle       \
    -vlan                         1                          \
    -vlan_id                      101                        \
    -vlan_id_step                 1                          \
    -vlan_id_count                1                          \
    -vlan_tpid                    0x8100                     \
    -vlan_user_priority           0                          \
    -vlan_user_priority_step      0                          \
    -use_vpn_parameters           0                          \
    -site_id                      0                          \
]
if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "[info script] $ethernet_1_status"
}
set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

############################################
## IPv4 Config
############################################

set multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          20.20.20.1              \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_2_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_2_status"
}
set multivalue_2_handle [keylget multivalue_2_status multivalue_handle]

set gw_multivalue_1_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          20.20.20.3              \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget gw_multivalue_1_status status] != $::SUCCESS} {
    puts "[info script] $gw_multivalue_1_status"
}
set gw_multivalue_1_handle [keylget gw_multivalue_1_status multivalue_handle]

set ipv4_1_status [::ixiangpf::interface_config \
    -protocol_name                {IPv4 1}                  \
    -protocol_handle              $ethernet_1_handle        \
    -ipv4_resolve_gateway         1                         \
    -ipv4_manual_gateway_mac      00.00.00.00.00.01         \
    -gateway                      $gw_multivalue_1_handle   \
    -intf_ip_addr                 $multivalue_2_handle      \
    -netmask                      255.255.255.0             \
]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
    puts "[info script] $ipv4_1_status"
}
set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]

set multivalue_4_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          192.0.0.1               \
        -counter_step           0.0.0.1                 \
        -counter_direction      increment               \
        -nest_step              0.1.0.0                 \
        -nest_owner             $topology_1_handle      \
        -nest_enabled           1                       \
    ]
    if {[keylget multivalue_4_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $multivalue_4_status
    }
    set multivalue_4_handle [keylget multivalue_4_status multivalue_handle]
###############################
##BFDv4 Config
###############################

set bfdv4_interface_1_status [::ixiangpf::emulation_bfd_config \
        -count                           1                         \
        -echo_rx_interval                0                         \
        -echo_timeout                    1500                      \
        -echo_tx_interval                0                         \
        -control_plane_independent       0                         \
        -enable_demand_mode              0                         \
        -flap_tx_interval                0                         \
        -handle                          $ipv4_1_handle            \
        -min_rx_interval                 1000                      \
        -mode                            create                    \
        -detect_multiplier               3                         \
        -poll_interval                   0                         \
        -router_id                       $multivalue_4_handle      \
        -tx_interval                     1000                      \
        -configure_echo_source_ip        0                         \
        -echo_source_ip4                 0.0.0.0                   \
        -ip_diff_serv                    0                         \
        -interface_active                1                         \
        -interface_name                  {BFDv4 IF 1}              \
        -router_active                   1                         \
        -router_name                     {BfdRouter 1}             \
        -session_count                   1                         \
        -enable_auto_choose_source       1                         \
        -enable_learned_remote_disc      1                         \
        -ip_version                      4                         \
        -session_discriminator           1                         \
        -session_discriminator_step      0                         \
        -remote_discriminator            1                         \
        -remote_discriminator_step       0                         \
        -source_ip_addr                  0.0.0.0                   \
        -remote_ip_addr                  20.20.20.3                \
        -remote_ip_addr_step             0.0.0.1                   \
        -hop_mode                        singlehop                 \
        -session_active                  1                         \
        -session_name                    {BFDv4 Session 1}         \
    ]
    if {[keylget bfdv4_interface_1_status status] != $::SUCCESS} {
        puts "[info script] $bfdv4_interface_1_status"
    }
    set bfdv4Interface_1_handle [keylget bfdv4_interface_1_status bfd_v4_interface_handle]


#########################################################################################################################
##                                                     Topology 2 Config                                               ##
#########################################################################################################################

set topology_2_handle [setup_topology "Topology 2" $port_2]

#########################################################################################################################
##                                                     Device Group 2 Config                                           ##
#########################################################################################################################

set device_group_2_status [::ixiangpf::topology_config      \
    -topology_handle              $topology_2_handle        \
    -device_group_name            {D2}                      \
    -device_group_multiplier      2                         \
    -device_group_enabled         1                         \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    error $device_group_2_status
}

set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]

############################################
## Ethernet Config
############################################

set multivalue_3_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.11.01.00.00.02       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_3_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_1_status"
}
set multivalue_3_handle [keylget multivalue_3_status multivalue_handle]

set ethernet_2_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 2}               \
    -protocol_handle              $deviceGroup_2_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_3_handle       \
    -vlan                         1                          \
    -vlan_id                      101                        \
    -vlan_id_step                 1                          \
    -vlan_id_count                1                          \
    -vlan_tpid                    0x8100                     \
    -vlan_user_priority           0                          \
    -vlan_user_priority_step      0                          \
    -use_vpn_parameters           0                          \
    -site_id                      0                          \
]
if {[keylget ethernet_2_status status] != $::SUCCESS} {
    puts "[info script] $ethernet_2_status"
}
set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]

############################################
## IPv4 Config
############################################

set multivalue_4_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          192.0.0.1               \
        -counter_step           0.0.0.1                 \
        -counter_direction      increment               \
        -nest_step              0.1.0.0                 \
        -nest_owner             $topology_1_handle      \
        -nest_enabled           1                       \
    ]
if {[keylget multivalue_4_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $multivalue_4_status
}
set multivalue_4_handle [keylget multivalue_4_status multivalue_handle]

set multivalue_5_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          20.20.20.3              \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]

if {[keylget multivalue_5_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_2_status"
}
set multivalue_5_handle [keylget multivalue_5_status multivalue_handle]
set gw_multivalue_1_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          20.20.20.1              \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget gw_multivalue_1_status status] != $::SUCCESS} {
    puts "[info script] $gw_multivalue_1_status"
}
set gw_multivalue_1_handle [keylget gw_multivalue_1_status multivalue_handle]

set ipv4_2_status [::ixiangpf::interface_config \
    -protocol_name                {IPv4 2}                  \
    -protocol_handle              $ethernet_2_handle        \
    -ipv4_resolve_gateway         1                         \
    -ipv4_manual_gateway_mac      00.00.00.00.00.01         \
    -gateway                      $gw_multivalue_1_handle   \
    -intf_ip_addr                 $multivalue_5_handle      \
    -netmask                      255.255.255.0             \
]
if {[keylget ipv4_2_status status] != $::SUCCESS} {
    puts "[info script] $ipv4_1_status"
}
set ipv4_2_handle [keylget ipv4_2_status ipv4_handle]

set multivalue_5_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          20.20.20.1              \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_5_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_2_status"
}
set multivalue_5_handle [keylget multivalue_5_status multivalue_handle]
############################
###BFDv4 Config
############################

set bfdv4_interface_2_status [::ixiangpf::emulation_bfd_config \
        -count                           1                         \
        -echo_rx_interval                0                         \
        -echo_timeout                    1500                      \
        -echo_tx_interval                0                         \
        -control_plane_independent       0                         \
        -enable_demand_mode              0                         \
        -flap_tx_interval                0                         \
        -handle                          $ipv4_2_handle            \
        -min_rx_interval                 1000                      \
        -mode                            create                    \
        -detect_multiplier               3                         \
        -poll_interval                   0                         \
        -router_id                       $multivalue_4_handle      \
        -tx_interval                     1000                      \
        -configure_echo_source_ip        0                         \
        -echo_source_ip4                 0.0.0.0                   \
        -ip_diff_serv                    0                         \
        -interface_active                1                         \
        -interface_name                  {BFDv4 IF 2}              \
        -router_active                   1                         \
        -router_name                     {BfdRouter 2}             \
        -session_count                   1                         \
        -enable_auto_choose_source       1                         \
        -enable_learned_remote_disc      1                         \
        -ip_version                      4                         \
        -session_discriminator           1                         \
        -session_discriminator_step      0                         \
        -remote_discriminator            1                         \
        -remote_discriminator_step       0                         \
        -source_ip_addr                  0.0.0.0                   \
        -remote_ip_addr                  20.20.20.1                   \
        -remote_ip_addr_step             0.0.0.1                   \
        -hop_mode                        singlehop                 \
        -session_active                  1                         \
        -session_name                    {BFDv4 Session 2}         \
    ]
    if {[keylget bfdv4_interface_2_status status] != $::SUCCESS} {
        puts "[info script] $bfdv4_interface_2_status"
    }
    set bfdv4Interface_2_handle [keylget bfdv4_interface_2_status bfd_v4_interface_handle]

######################################
##Starting BFD Interfaces
######################################
set start_status1 [::ixiangpf::emulation_bfd_control    \
            -mode start                         \
            -handle $bfdv4Interface_1_handle]

if {[keylget start_status1 status] != $::SUCCESS} {
        puts "[info script] $start_status1"
    }       

set start_status2 [::ixiangpf::emulation_bfd_control    \
            -mode start                         \
            -handle $bfdv4Interface_2_handle]

if {[keylget start_status2 status] != $::SUCCESS} {
        puts "[info script] $start_status2"
    }       

puts "BFD interfaces started, wait 60 seconds "
after 60000
#########################################
##Fetching the stats
#########################################

set agg_stats [::ixiangpf::emulation_bfd_info   \
                -mode aggregate                 \
                -handle $bfdv4Interface_1_handle]

if {[keylget agg_stats status] != $::SUCCESS} {
        puts "[info script] $agg_stats"
    }       

puts "The stats are $agg_stats"

set session_conf_up [keylget agg_stats $port_1.aggregate.sessions_configured_up]
set session_auto_created [keylget agg_stats $port_1.aggregate.sessions_auto_created]

puts "Sessions Configured up : $session_conf_up \
        \nSessions Auto Created : $session_auto_created"

######################################
##Fetching Learned_info
######################################

set learned_information [::ixiangpf::emulation_bfd_info \
                            -mode learned_info \
                            -handle $bfdv4Interface_1_handle]

if {[keylget learned_information status] != $::SUCCESS} {
        puts "[info script] $learned_information"
    }       

puts "Learned Information : $learned_information"

#####################################
#Perform set_admin_down and then set_admin_up
#####################################

puts "Setting admin down, followed by set admin up"
set set_admin_down [::ixiangpf::emulation_bfd_control \
                    -mode set_admin_down \
                    -handle $bfdv4Interface_1_handle\
                    -protocol_name bfd]

if {[keylget set_admin_down status] != $::SUCCESS} {
        puts "[info script] $set_admin_down"
    }       

after 10000

set agg_stats [::ixiangpf::emulation_bfd_info   \
                -mode aggregate                 \
                -handle $bfdv4Interface_1_handle]

if {[keylget agg_stats status] != $::SUCCESS} {
        puts "[info script] $agg_stats"
    }       

puts "The stats are $agg_stats"

set session_conf_up [keylget agg_stats $port_1.aggregate.sessions_configured_up]

puts "Session configured up : $session_conf_up"

after 2000

set set_admin_up [::ixiangpf::emulation_bfd_control \
                    -mode set_admin_up \
                    -handle $bfdv4Interface_1_handle\
                    -protocol_name bfd]

if {[keylget set_admin_up status] != $::SUCCESS} {
        puts "[info script] $set_admin_up"
    }       

after 10000

set agg_stats [::ixiangpf::emulation_bfd_info   \
                -mode aggregate                 \
                -handle $bfdv4Interface_1_handle]

if {[keylget agg_stats status] != $::SUCCESS} {
        puts "[info script] $agg_stats"
    }       

puts "The stats are $agg_stats"

set session_conf_up [keylget agg_stats $port_1.aggregate.sessions_configured_up]

puts "Session configured up : $session_conf_up"

after 2000

###############################
##performin OTF changes
###############################

puts "Modifying tx_interval and min_rx_interval OTF"
set otf1 [::ixiangpf::emulation_bfd_config   \
            -mode modify                     \
            -handle $bfdv4Interface_1_handle \
            -ip_version 4                    \
            -tx_interval 2000                \
            -min_rx_interval 2000           ]

set otf2 [::ixiangpf::emulation_bfd_config   \
            -mode modify                     \
            -handle $bfdv4Interface_2_handle \
            -ip_version 4                    \
            -tx_interval 2000                \
            -min_rx_interval 2000           ]            

ixNet commit
ixNet exec applyOnTheFly $otf

#################################################
##Performing Enable/Disable of BFD interface
#################################################

set disable [::ixiangpf::emulation_bfd_config \
                -mode disable \
                -handle $bfdv4Interface_1_handle \
                -ip_version 4]

if {[keylget disable status] != $::SUCCESS} {
        puts "[info script] $disable"
    }       
ixNet commit
ixNet exec applyOnTheFly $otf

after 10000

set agg_stats [::ixiangpf::emulation_bfd_info   \
                -mode aggregate                 \
                -handle $bfdv4Interface_2_handle]

if {[keylget agg_stats status] != $::SUCCESS} {
        puts "[info script] $agg_stats"
    }       

puts "The stats are $agg_stats"

set session_conf_up [keylget agg_stats $port_2.aggregate.sessions_configured_up]
set flap [keylget agg_stats $port_2.aggregate.session_flap_cnt]

puts "Session configured up : $session_conf_up \
        \nFlap : $flap"

after 2000        

set enable [::ixiangpf::emulation_bfd_config \
                -mode enable \
                -handle $bfdv4Interface_1_handle \
                -ip_version 4]

if {[keylget enable status] != $::SUCCESS} {
        puts "[info script] $enable"
    }       

after 10000
puts "TEST COMPLETED"

