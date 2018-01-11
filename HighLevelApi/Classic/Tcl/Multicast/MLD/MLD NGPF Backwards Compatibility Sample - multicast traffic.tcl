#################################################################################
# Version 1.0    $Revision: 2 $
# $Author: alupu $
#
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#
#################################################################################

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
#    This sample uses NGPF Bacwardsc Compatibility to create 5 MLD hosts on    #
# one port, 3 on the other, then adds Group Ranges, starts protocols,          #
# configures multicast traffic, runs traffic and retrieves stats.              #
# Module:                                                                      #
#    The sample was tested on a LSM XMVDC16 module.                            #
#                                                                              #
################################################################################

set test_name [info script]

namespace eval ::cfg {}

set ::cfg::hltapi_p2no_hltset HLTSET174
set env(IXIA_VERSION) $::cfg::hltapi_p2no_hltset 


set cfgErrors 0

global cfgErrors

set chassis_ip            ixro-hlt-xm2-06
set port_list             [list 2/1 2/2]
set ixnetwork_tcl_server  localhost
set username              Pythar

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - $test_name - $retCode"
    return 0
}

########################################################################################
# Connect to the chassis, reset to factory defaults and take ownership                 #
########################################################################################
set connect_status [::ixiangpf::connect                   \
        -reset                                        \
        -device                         $chassis_ip   \
        -port_list                      $port_list    \
        -username                       $username     \
        -ixnetwork_tcl_server           $ixnetwork_tcl_server \
        -interactive 1                                         \
        ]

if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

ixNet setSessionParameter setAttribute loose


set port_1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]

puts "Configuring MLD on Port 1"

############################################################# Configure MLD on port 1 ########################################################################

########################################
# GENERAL                              #
########################################
set count                       5                                              ;# RANGE   1-1000 DEFAULT 1
set mode                        create                                         ;# CHOICES create modify delete disable enable enable_all disable_all
set no_write                    0                                              ;# FLAG
set reset                       1                                              ;# FLAG

##################################################
# MLD - PROTOCOL INTERFACE IPv6                  #
##################################################

set intf_ip_addr                20AB:0:0:1:0:0:0:2                          ;# IPV6
set intf_ip_addr_step           ::1                                         ;# IPV6 DEFAULT 0::1
set intf_prefix_len             64                                          ;# RANGE   1-128  DEFAULT 64
set neighbor_intf_ip_addr       20AB:0:0:1:0:0:0:1                      ;# IPV6  DEFAULT 0::0
set neighbor_intf_ip_addr_step  0:0:0:0:0:0:0:0                             ;# IPV6  DEFAULT 0::1

##################################################
# MLD - PROTOCOL INTERFACE Ethernet              #
##################################################

set mac_address_init            00:00:aa:00:00:00                              ;# MAC
set mac_address_step            0000.0000.00a0                                 ;# MAC DEFAULT 0000.0000.0001
set vlan                        0                                              ;# CHOICES 0 1
set vlan_id                     50                                             ;# RANGE   0-4095
set vlan_id_mode                increment                                      ;# CHOICES fixed increment  DEFAULT increment
set vlan_id_step                3                                              ;# RANGE   0-4095 DEFAULT 1
set vlan_user_priority          2                                              ;# RANGE   0-7 DEFAULT 0

##################################################
# MLD - PROTOCOL CONFIG                          #
##################################################
set enable_packing              1                                              ;# CHOICES 0 1  DEFAULT 0
set general_query               0                                              ;# CHOICES 0 1 DEFAULT 1
set group_query                 0                                              ;# CHOICES 0 1 DEFAULT 1
set ip_router_alert             1                                              ;# CHOICES 0 1 DEFAULT 1
set mldv2_report_type           206                                            ;# CHOICES 143 206 DEFAULT 143
set mld_version                 v1                                             ;# CHOICES v1 v2 DEFAULT v2
set msg_count_per_interval      300                                            ;# RANGE   0-999999999  DEFAULT 0
set msg_interval                400                                            ;# RANGE   0-999999999 DEFAULT 0
set robustness                  1                                              ;# RANGE 1-65535 DEFAULT 2
set suppress_report             1                                              ;# CHOICES 0 1 DEFAULT 0
set unsolicited_report_interval 500                                            ;# RANGE   0-999999

########################################
# Start MLD Call                       #
########################################
set mld_router_config_status_1 [::ixiangpf::emulation_mld_config                   \
        -count                          $count                                 \
        -mode                           $mode                                  \
        -no_write                       $no_write                              \
        -port_handle                    $port_1                                \
        -reset                          $reset                                 \
        -enable_packing                 $enable_packing                        \
        -general_query                  $general_query                         \
        -group_query                    $group_query                           \
        -ip_router_alert                $ip_router_alert                       \
        -mldv2_report_type              $mldv2_report_type                     \
        -mld_version                    $mld_version                           \
        -msg_count_per_interval         $msg_count_per_interval                \
        -msg_interval                   $msg_interval                          \
        -robustness                     $robustness                            \
        -suppress_report                $suppress_report                       \
        -unsolicited_report_interval    $unsolicited_report_interval           \
        -intf_ip_addr                   $intf_ip_addr                          \
        -intf_ip_addr_step              $intf_ip_addr_step                     \
        -intf_prefix_len                $intf_prefix_len                       \
        -neighbor_intf_ip_addr          $neighbor_intf_ip_addr                 \
        -neighbor_intf_ip_addr_step     $neighbor_intf_ip_addr_step            \
        -mac_address_init               $mac_address_init                      \
        -mac_address_step               $mac_address_step                      \
        -override_existence_check       0                                      \
        -override_tracking              0                                      \
        -vlan                           $vlan                                  \
        -vlan_id                        $vlan_id                               \
        -vlan_id_mode                   $vlan_id_mode                          \
        -vlan_id_step                   $vlan_id_step                          \
        -vlan_user_priority             $vlan_user_priority                    \
        ]

if {[keylget mld_router_config_status_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget mld_router_config_status_1 log]"
    return 0
}

set mld_router_handles_h1_3 [keylget mld_router_config_status_1 handle]


################################################################################
# Configure MLD groups on hosts from port 1                                    #
################################################################################
set multicast_group_handles_1 [list ]
set mld_dest_list_handle_1 [list ]

for {set i 0} {$i < [llength $mld_router_handles_h1_3]} {incr i} {
    
    set mode                          create
    set num_groups                    [expr 10+$i]
    set ip_addr_start                 FF1[expr 5+$i]::1
    set ip_addr_step                  0::1
    set ip_prefix_len                 128

    set multicast_group_status [::ixiangpf::emulation_multicast_group_config                     \
            -mode                           $mode                                            \
            -num_groups                     $num_groups                                      \
            -ip_addr_start                  $ip_addr_start                                   \
            -ip_addr_step                   $ip_addr_step                                    \
            -ip_prefix_len                  $ip_prefix_len                                   \
            ]

    if {[keylget multicast_group_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget multicast_group_status log]"
        return 0
    }

    set multicast_group_handle [keylget multicast_group_status handle]
    lappend multicast_group_handles_1 $multicast_group_handle


    set single_mld_group_status [::ixiangpf::emulation_mld_group_config                       \
                -mode                       $mode                                         \
                -session_handle             [lindex $mld_router_handles_h1_3 $i]            \
                -group_pool_handle          $multicast_group_handle       ]


    if {[keylget single_mld_group_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget single_mld_group_status log]"
        return 0
        }

    lappend mld_dest_list_handle_1 [keylget single_mld_group_status handle]
   
}

# Get interface handle

set mld_handle_1 [ixNet getP [lindex $mld_router_handles_h1_3 0]]
set protocols_handle_1 [ixNet getP $mld_handle_1] 
#set port_handle_1 [ixNet getP $protocols_handle_1]
set interface_handle_1 [ixNet getL $protocols_handle_1 item]

################################################################## Configure MLD on port 2 ###################################################################


########################################
# GENERAL                              #
########################################
set count                       3                                              ;# RANGE   1-1000 DEFAULT 1
set mode                        create                                         ;# CHOICES create modify delete disable enable enable_all disable_all
set no_write                    0                                              ;# FLAG
set reset                       1                                              ;# FLAG

##################################################
# MLD - PROTOCOL INTERFACE IPv6                  #
##################################################

set intf_ip_addr                20AB:0:0:2:0:0:0:2                                        ;# IPV6
set intf_ip_addr_step           ::1                                         ;# IPV6 DEFAULT 0::1
set intf_prefix_len             64                                          ;# RANGE   1-128  DEFAULT 64
set neighbor_intf_ip_addr       20AB:0:0:2:0:0:0:1                     ;# IPV6  DEFAULT 0::0
set neighbor_intf_ip_addr_step  0:0:0:0:0:0:0:0                             ;# IPV6  DEFAULT 0::1

##################################################
# MLD - PROTOCOL INTERFACE Ethernet              #
##################################################

set mac_address_init            aa:00:00:00:00:00                              ;# MAC
set mac_address_step            00:00:00:01:00:00                              ;# MAC DEFAULT 0000.0000.0001
set vlan                        0                                              ;# CHOICES 0 1
set vlan_id                     50                                             ;# RANGE   0-4095
set vlan_id_mode                increment                                      ;# CHOICES fixed increment  DEFAULT increment
set vlan_id_step                3                                              ;# RANGE   0-4095 DEFAULT 1
set vlan_user_priority          2                                              ;# RANGE   0-7 DEFAULT 0

##################################################
# MLD - PROTOCOL CONFIG                          #
##################################################
set enable_packing              0                                              ;# CHOICES 0 1  DEFAULT 0
set general_query               1                                              ;# CHOICES 0 1 DEFAULT 1
set group_query                 1                                              ;# CHOICES 0 1 DEFAULT 1
set ip_router_alert             1                                              ;# CHOICES 0 1 DEFAULT 1
set mldv2_report_type           143                                            ;# CHOICES 143 206 DEFAULT 143
set mld_version                 v1                                             ;# CHOICES v1 v2 DEFAULT v2
set msg_count_per_interval      300                                            ;# RANGE   0-999999999  DEFAULT 0
set msg_interval                400                                            ;# RANGE   0-999999999 DEFAULT 0
set robustness                  1                                              ;# RANGE 1-65535 DEFAULT 2
set suppress_report             0                                              ;# CHOICES 0 1 DEFAULT 0
set unsolicited_report_interval 500                                            ;# RANGE   0-999999

########################################
# Start MLD Call                       #
########################################
set mld_router_config_status_2 [::ixiangpf::emulation_mld_config                   \
        -count                          $count                                 \
        -mode                           $mode                                  \
        -no_write                       $no_write                              \
        -port_handle                    $port_2                                \
        -reset                          $reset                                 \
        -enable_packing                 $enable_packing                        \
        -general_query                  $general_query                         \
        -group_query                    $group_query                           \
        -ip_router_alert                $ip_router_alert                       \
        -mldv2_report_type              $mldv2_report_type                     \
        -mld_version                    $mld_version                           \
        -msg_count_per_interval         $msg_count_per_interval                \
        -msg_interval                   $msg_interval                          \
        -robustness                     $robustness                            \
        -suppress_report                $suppress_report                       \
        -unsolicited_report_interval    $unsolicited_report_interval           \
        -intf_ip_addr                   $intf_ip_addr                          \
        -intf_ip_addr_step              $intf_ip_addr_step                     \
        -intf_prefix_len                $intf_prefix_len                       \
        -neighbor_intf_ip_addr          $neighbor_intf_ip_addr                 \
        -neighbor_intf_ip_addr_step     $neighbor_intf_ip_addr_step            \
        -mac_address_init               $mac_address_init                      \
        -mac_address_step               $mac_address_step                      \
        -override_existence_check       0                                      \
        -override_tracking              0                                      \
        -vlan                           $vlan                                  \
        -vlan_id                        $vlan_id                               \
        -vlan_id_mode                   $vlan_id_mode                          \
        -vlan_id_step                   $vlan_id_step                          \
        -vlan_user_priority             $vlan_user_priority                    \
        ]

if {[keylget mld_router_config_status_2 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget mld_router_config_status_2 log]"
    return 0
}

set mld_router_handles_h2 [keylget mld_router_config_status_2 handle]


################################################################################
# Configure MLD groups on hosts from port 2                                    #
################################################################################
set multicast_group_handles_2 [list ]
set mld_dest_list_handle_2 [list ]

for {set i 0} {$i < [llength $mld_router_handles_h2]} {incr i} {
    
    set mode                          create
    set num_groups                    [expr 10+$i]
    set ip_addr_start                 FF2[expr 5+$i]::1
    set ip_addr_step                  0::1
    set ip_prefix_len                 128

    set multicast_group_status [::ixiangpf::emulation_multicast_group_config                     \
            -mode                           $mode                                            \
            -num_groups                     $num_groups                                      \
            -ip_addr_start                  $ip_addr_start                                   \
            -ip_addr_step                   $ip_addr_step                                    \
            -ip_prefix_len                  $ip_prefix_len                                   \
            ]

    if {[keylget multicast_group_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget multicast_group_status log]"
        return 0
    }

    set multicast_group_handle [keylget multicast_group_status handle]
    lappend multicast_group_handles_2 $multicast_group_handle


    set single_mld_group_status [::ixiangpf::emulation_mld_group_config                       \
                -mode                       $mode                                         \
                -session_handle             [lindex $mld_router_handles_h2 $i]            \
                -group_pool_handle          $multicast_group_handle       ]


    if {[keylget single_mld_group_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget single_mld_group_status log]"
        return 0
        }

    lappend mld_dest_list_handle_2 [keylget single_mld_group_status handle]
}

# Get interface handle

set mld_handle_2 [ixNet getP [lindex $mld_router_handles_h2 0]]
set protocols_handle_2 [ixNet getP $mld_handle_2] 
#set port_handle_2 [ixNet getP $protocols_handle_2]
set interface_handle_2 [ixNet getL $protocols_handle_2 item]

###############################################################
################### Start MLD #################################
###############################################################

puts "Starting MLD hosts"

set mode start

set mld_router_control_status [::ixiangpf::emulation_mld_control                   \
        -mode                           $mode                                  \
        -port_handle                    [list $port_1 $port_2]                                \
        ]

if {[keylget mld_router_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget mld_router_control_status log]"
    return 0
}

after 15000

####################################################################
################### Create Traffic #################################
####################################################################

puts "Creating taffic item 1..."

set ti_dsts(EndpointSet-1) [list]

set ti_mcast_rcvr_handle(EndpointSet-1) [lrepeat 3 [ixNet getP [lindex $mld_dest_list_handle_2 0]]]

set ti_mcast_rcvr_port_index(EndpointSet-1) [list 0 0 0]
set ti_mcast_rcvr_host_index(EndpointSet-1) [list 0 1 2]
set ti_mcast_rcvr_mcast_index(EndpointSet-1) [list 0 0 0]

set traffic_status_1 [::ixiangpf::traffic_config      \
        -mode                        create            \
        -traffic_generator           ixnetwork_540     \
        -bidirectional               0                 \
        -emulation_src_handle        /topology:1       \
        -emulation_dst_handle        [list]       \
        -emulation_multicast_dst_handle [list "ff25:0:0:0:0:0:0:1/0:0:0:0:0:0:0:1/10" "ff26:0:0:0:0:0:0:1/0:0:0:0:0:0:0:1/12" "ff27:0:0:0:0:0:0:1/0:0:0:0:0:0:0:1/14"] \
        -emulation_multicast_dst_handle_type [list [list none none none]] \
        -emulation_multicast_rcvr_handle [list $ti_mcast_rcvr_handle(EndpointSet-1)] \
        -emulation_multicast_rcvr_port_index [list $ti_mcast_rcvr_port_index(EndpointSet-1)] \
        -emulation_multicast_rcvr_host_index [list $ti_mcast_rcvr_host_index(EndpointSet-1)] \
        -emulation_multicast_rcvr_mcast_index [list $ti_mcast_rcvr_mcast_index(EndpointSet-1)] \
        -circuit_endpoint_type       ipv6      \
        -rate_percent                8               \
        -track_by                    ipv6_dest_ip     ]


if {[keylget traffic_status_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status_1 log]"
    return 0
}

set traffic_item_1_handle [keylget traffic_status_1 traffic_item]

puts "Creating taffic item 2..."

set ti_dsts(EndpointSet-1) [list]
set ti_mcast_rcvr_handle(EndpointSet-1) [lrepeat 5 [ixNet getP [lindex $mld_dest_list_handle_1 0]]]
set ti_mcast_rcvr_port_index(EndpointSet-1) [list 0 0 0 0 0]
set ti_mcast_rcvr_host_index(EndpointSet-1) [list 0 1 2 3 4]
set ti_mcast_rcvr_mcast_index(EndpointSet-1) [list 0 0 0 0 0]

set traffic_status_1 [::ixiangpf::traffic_config      \
        -mode                        create            \
        -traffic_generator           ixnetwork_540     \
        -bidirectional               0                 \
        -emulation_src_handle        /topology:2       \
        -emulation_dst_handle        [list]       \
        -emulation_multicast_dst_handle [list "ff15:0:0:0:0:0:0:1/0:0:0:0:0:0:0:1/10" "ff16:0:0:0:0:0:0:1/0:0:0:0:0:0:0:1/12" "ff17:0:0:0:0:0:0:1/0:0:0:0:0:0:0:1/14" "ff18:0:0:0:0:0:0:1/0:0:0:0:0:0:0:1/14" "ff19:0:0:0:0:0:0:1/0:0:0:0:0:0:0:1/14"] \
        -emulation_multicast_dst_handle_type [list [list none none none]] \
        -emulation_multicast_rcvr_handle [list $ti_mcast_rcvr_handle(EndpointSet-1)] \
        -emulation_multicast_rcvr_port_index [list $ti_mcast_rcvr_port_index(EndpointSet-1)] \
        -emulation_multicast_rcvr_host_index [list $ti_mcast_rcvr_host_index(EndpointSet-1)] \
        -emulation_multicast_rcvr_mcast_index [list $ti_mcast_rcvr_mcast_index(EndpointSet-1)] \
        -circuit_endpoint_type       ipv6      \
        -rate_percent                8               \
        -track_by                    ipv6_dest_ip     ]


if {[keylget traffic_status_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status_1 log]"
    return 0
}

set traffic_item_2_handle [keylget traffic_status_1 traffic_item]

puts "Starting Traffic..."

set traffic_control [::ixia::traffic_control                            \
        -action                        run ]  

 if {[keylget traffic_control status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_control log]"
    return 0
}

after 20000

puts "Stop Traffic..."

set traffic_control [::ixia::traffic_control                            \
        -action                        stop ]  

 if {[keylget traffic_control status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_control log]"
    return 0
} 

after 15000

puts "Collecting stats"
puts "Analyze Loss per Group"

set traffic_stats [::ixia::traffic_stats                            \
        -mode                        flow ]  

 if {[keylget traffic_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_stats log]"
    return 0
}

puts [::ixia::keylprint traffic_stats]
set stats_keys [keylkeys traffic_stats flow]

set expected_tracking [list "ff27:0:0:0:0:0:0:c" "ff19:0:0:0:0:0:0:c" "ff27:0:0:0:0:0:0:7" "ff19:0:0:0:0:0:0:7" "ff27:0:0:0:0:0:0:2" \
                            "ff19:0:0:0:0:0:0:2" "ff26:0:0:0:0:0:0:8" "ff18:0:0:0:0:0:0:a" "ff26:0:0:0:0:0:0:3" "ff18:0:0:0:0:0:0:5" \
                            "ff25:0:0:0:0:0:0:8" "ff17:0:0:0:0:0:0:c" "ff25:0:0:0:0:0:0:3" "ff17:0:0:0:0:0:0:7" "ff17:0:0:0:0:0:0:2" \
                            ]

for {set i 0} {$i < 15 } {incr i} {
    if {[keylget traffic_stats flow.[expr 5*$i+1].tracking.2.tracking_value] != [lindex $expected_tracking [expr $i]]} {
        puts "Not all the groups are present in the configuration"
        incr cfgErrors
    }
}


if {$cfgErrors} {
    puts "FAILED - There were $cfgErrors configuration errors."
    return 0
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
