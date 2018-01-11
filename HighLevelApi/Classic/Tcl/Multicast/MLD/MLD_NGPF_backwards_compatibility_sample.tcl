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
# each of the 2 ports, then adds                                               #
# (and later modifies) Group Ranges and Source Ranges to some of them,         #
# after which some control actions are executed.                               #
# Module:                                                                      #
#    The sample was tested on a LSM XMVDC16 module.                            #
#                                                                              #
################################################################################
set test_name [info script]
if {[catch {package require Ixia} retCode]} {
    puts "FAIL - $test_name - $retCode"
    return 0
}

set chassis_ip            ixro-hlt-xm2-06
set port_list             [list 2/1 2/2]
set ixnetwork_tcl_server  localhost


########################################################################################
# Connect to the chassis, reset to factory defaults and take ownership                 #
########################################################################################
set connect_status [::ixiangpf::connect                   \
        -reset                                        \
        -device                         $chassis_ip   \
        -port_list                      $port_list    \
        -ixnetwork_tcl_server           $ixnetwork_tcl_server \
        -interactive 1\
        ]

if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}
ixNet setSessionParameter setAttribute loose
set port_1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]


######################################## Configure MLD on port 1 ################################################################

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

set intf_ip_addr                2022::1                                        ;# IPV6
set intf_ip_addr_step           ::10                                         ;# IPV6 DEFAULT 0::1
set intf_prefix_len             64                                          ;# RANGE   1-128  DEFAULT 64
set neighbor_intf_ip_addr       2022::10:1                      ;# IPV6  DEFAULT 0::0
set neighbor_intf_ip_addr_step  0:0:0:0:0:0:1:1                             ;# IPV6  DEFAULT 0::1

##################################################
# MLD - PROTOCOL INTERFACE Ethernet              #
##################################################

set mac_address_init            00:aa:bb:cc:00:00                              ;# MAC
set mac_address_step            00aa.1000.00a0                                 ;# MAC DEFAULT 0000.0000.0001
set vlan                        1                                              ;# CHOICES 0 1
set vlan_id                     1,2,3,4,5,6                                             ;# RANGE   0-4095
set vlan_id_mode                increment                                      ;# CHOICES fixed increment  DEFAULT increment
set vlan_id_step                2,3,4,5,6,7                                              ;# RANGE   0-4095 DEFAULT 1
set vlan_user_priority          2,2,3,3,4,4                                              ;# RANGE   0-7 DEFAULT 0

##################################################
# MLD - PROTOCOL CONFIG                          #
##################################################
set enable_packing              1                                              ;# CHOICES 0 1  DEFAULT 0
set general_query               1                                              ;# CHOICES 0 1 DEFAULT 1
set group_query                 1                                              ;# CHOICES 0 1 DEFAULT 1
set ip_router_alert             1                                              ;# CHOICES 0 1 DEFAULT 1
set mldv2_report_type           206                                            ;# CHOICES 143 206 DEFAULT 143
set mld_version                 v2                                             ;# CHOICES v1 v2 DEFAULT v2
set msg_count_per_interval      1000                                            ;# RANGE   0-999999999  DEFAULT 0
set msg_interval                8899                                            ;# RANGE   0-999999999 DEFAULT 0
set robustness                  99                                              ;# RANGE 1-65535 DEFAULT 2
set suppress_report             0                                              ;# CHOICES 0 1 DEFAULT 0
set unsolicited_report_interval 1111                                             ;# RANGE   0-999999

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


######################################## Configure MLD on port 2 ################################################################

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

set intf_ip_addr                2022::10:1                                        ;# IPV6
set intf_ip_addr_step           ::1:1                                         ;# IPV6 DEFAULT 0::1
set intf_prefix_len             64                                          ;# RANGE   1-128  DEFAULT 64
set neighbor_intf_ip_addr       2022::1                                     ;# IPV6  DEFAULT 0::0
set neighbor_intf_ip_addr_step  ::10                             ;# IPV6  DEFAULT 0::1

##################################################
# MLD - PROTOCOL INTERFACE Ethernet              #
##################################################

set mac_address_init            aa:00:00:00:00:fe                              ;# MAC
set mac_address_step            00:00:00:01:00:00                              ;# MAC DEFAULT 0000.0000.0001
set vlan                        1                                              ;# CHOICES 0 1
set vlan_id                     1,2,3,4,5,6                                             ;# RANGE   0-4095
set vlan_id_mode                increment                                      ;# CHOICES fixed increment  DEFAULT increment
set vlan_id_step                2,3,4,5,6,7                                              ;# RANGE   0-4095 DEFAULT 1
set vlan_user_priority          2,2,3,3,4,4                                              ;# RANGE   0-7 DEFAULT 0

##################################################
# MLD - PROTOCOL CONFIG                          #
##################################################
set enable_packing              0                                              ;# CHOICES 0 1  DEFAULT 0
set general_query               1                                              ;# CHOICES 0 1 DEFAULT 1
set group_query                 1                                              ;# CHOICES 0 1 DEFAULT 1
set ip_router_alert             1                                              ;# CHOICES 0 1 DEFAULT 1
set mldv2_report_type           206                                            ;# CHOICES 143 206 DEFAULT 143
set mld_version                 v2                                             ;# CHOICES v1 v2 DEFAULT v2
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
# Creating several multicast groups in a for loop                              #
################################################################################
set g_list [list ]
for {set i 0} {$i < 20} {incr i} {
    set addr "FF99::23:[expr $i + 1]"
    lappend g_addr $addr
    set group_add [::ixiangpf::emulation_multicast_group_config        \
            -mode                           create  \
            -ip_addr_start                  $addr   \
            -ip_addr_step                   0::1:0   \
            -ip_prefix_len                  48      \
            -num_groups                     3       \
            ]
    if {[keylget group_add status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget group_add log]"
        return 0
    }
    set g [keylget group_add handle]
    lappend g_list $g
}

################################################################################
# Creating several multicast sources with step ::1 in a for loop               #
################################################################################
set s_list_1 [list ]
for {set i 0} {$i < 10} {incr i} {
    set addr "2015::44:[expr $i + 1]"
    lappend s_addr_1 $addr
    set source_add [::ixiangpf::emulation_multicast_source_config        \
            -mode                           create  \
            -ip_addr_start                  $addr   \
            -ip_addr_step                   0::1   \
            -ip_prefix_len                  64      \
            -num_sources                     100       \
            ]
    if {[keylget source_add status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget source_add log]"
        return 0
    }
    set s [keylget source_add handle]
    lappend s_list_1 $s
}

################################################################################
# Creating several multicast sources with step ::1:1 in a for loop             # 
################################################################################
set s_list_2 [list ]
for {set i 0} {$i < 10} {incr i} {
    set addr "2020::44:[expr $i + 1]"
    set source_add [::ixiangpf::emulation_multicast_source_config        \
            -mode                           create  \
            -ip_addr_start                  $addr   \
            -ip_addr_step                   0::1:1   \
            -ip_prefix_len                  64      \
            -num_sources                    5       \
            ]
    if {[keylget source_add status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget source_add log]"
        return 0
    }
    set s [keylget source_add handle]
    lappend s_list_2 $s
}

#############################################################################################
# Adding one group and one source from the first pool to the first MLD host on port_1       #
#############################################################################################

set group_list_handle_0_0 [list ]

set group_config [::ixiangpf::emulation_mld_group_config \
    -mode                   create                                  \
    -session_handle         [lindex $mld_router_handles_h1_3 0]     \
    -group_pool_handle      [lindex $g_list 0 ]                     \
    -source_pool_handle     [lindex $s_list_1 0]                      \
    -g_enable_packing       1                                       \
    -g_filter_mode          exclude                                 \
    -g_max_groups_per_pkts  333                                      \
    -g_max_sources_per_group 444                                     \
]
if {[keylget group_config status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_config log]"
    return 0
}
set g_handle [keylget group_config handle]
set group_pool_handle [keylget group_config group_pool_handle]
set source_pool_handle [keylget group_config source_pool_handles]
lappend group_list_handle_0_0 $g_handle


#############################################################################################
# Adding one group and one source from the second pool to the first MLD host on port_2      #
#############################################################################################

set group_list_handle_1_0 [list ]

set group_config [::ixiangpf::emulation_mld_group_config \
    -mode                   create                                  \
    -session_handle         [lindex $mld_router_handles_h2 0]     \
    -group_pool_handle      [lindex $g_list 1]                     \
    -source_pool_handle     [lindex $s_list_2 0]                      \
    -g_enable_packing       0                                       \
    -g_filter_mode          include                                 \
    -g_max_groups_per_pkts  11                                      \
    -g_max_sources_per_group 33                                     \
]
if {[keylget group_config status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_config log]"
    return 0
}
set g_handle [keylget group_config handle]
set group_pool_handle [keylget group_config group_pool_handle]
set source_pool_handle [keylget group_config source_pool_handles]
lappend group_list_handle_1_0 $g_handle


#############################################################################################
# Adding 2 groups, each with 2 sources from the first pool to the first MLD host on port_1  #
#############################################################################################

for {set i 0} {$i < 2} {incr i} {
    set group_config [::ixiangpf::emulation_mld_group_config \
        -mode                   create                                  \
        -session_handle         [lindex $mld_router_handles_h1_3 0]     \
        -group_pool_handle      [lindex $g_list [expr $i + 1] ]                     \
        -source_pool_handle     [lrange $s_list_1 1 2]                      \
    ]
    if {[keylget group_config status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget group_config log]"
        return 0
    }
    set g_handle [keylget group_config handle]
    set group_pool_handle [keylget group_config group_pool_handle]
    set source_pool_handle [keylget group_config source_pool_handles]
    lappend group_list_handle_0_0 $g_handle
}

#############################################################################################
# Adding one group and 3 sources from the first pool to the second MLD host on port_1       #
#############################################################################################

set group_list_handle_0_1 [list ]
set group_config [::ixiangpf::emulation_mld_group_config \
    -mode                   create                                  \
    -session_handle         [lindex $mld_router_handles_h1_3 1]     \
    -group_pool_handle      [lindex $g_list 5]                     \
    -source_pool_handle     [lrange $s_list_1 end-2 end]                      \
    -g_enable_packing       1                                       \
    -g_filter_mode          exclude                                 \
    -g_max_groups_per_pkts  1001                                      \
    -g_max_sources_per_group 1500                                     \
]
if {[keylget group_config status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_config log]"
    return 0
}
set g_handle [keylget group_config handle]
set group_pool_handle [keylget group_config group_pool_handle]
set source_pool_handle [keylget group_config source_pool_handles]
lappend group_list_handle_0_1 $g_handle


#######################################################################################################
# Adding one group (same as above) and 4 sources from the first pool to the third MLD host on port_1  #
#######################################################################################################
set group_list_handle_0_2 [list ]
set group_config [::ixiangpf::emulation_mld_group_config \
    -mode                   create                                 \
    -session_handle         [lindex $mld_router_handles_h1_3 2]    \
    -group_pool_handle      [lindex $g_list 5]                     \
    -source_pool_handle     [lrange $s_list_1 4 7]                 \
    -g_enable_packing       1                                      \
    -g_filter_mode          include                                \
    -g_max_groups_per_pkts  222                                    \
    -g_max_sources_per_group 11                                    \
]
if {[keylget group_config status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_config log]"
    return 0
}
set g_handle [keylget group_config handle]
set group_pool_handle [keylget group_config group_pool_handle]
set source_pool_handle [keylget group_config source_pool_handles]
lappend group_list_handle_0_2 $g_handle

#############################################################################################
# Adding another group + 2 sources to the third MLD host from port_1                        #
#############################################################################################

set group_config [::ixiangpf::emulation_mld_group_config \
    -mode                   create                                 \
    -session_handle         [lindex $mld_router_handles_h1_3 2]    \
    -group_pool_handle      [lindex $g_list 6]                     \
    -source_pool_handle     [lrange $s_list_1 8 9]                 \
]
if {[keylget group_config status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_config log]"
    return 0
}
set g_handle [keylget group_config handle]
set group_pool_handle [keylget group_config group_pool_handle]
set source_pool_handle [keylget group_config source_pool_handles]
lappend group_list_handle_0_2 $g_handle


################################################################################################
# Adding 4 groups (with 1, 2, 3, and, respectively, 4 sources) to the 4th MLD host on port_1   #
################################################################################################

set group_list_handle_0_3 [list ]
set source_list [list ]
for {set i 0} {$i < 4} {incr i} {
    set group_config [::ixiangpf::emulation_mld_group_config \
        -mode                   create                                 \
        -session_handle         [lindex $mld_router_handles_h1_3 3]    \
        -group_pool_handle      [lindex $g_list $i]                    \
        -source_pool_handle     [lrange $s_list_1 0 $i]                \
        -g_enable_packing       1                                      \
        -g_filter_mode          include                                \
        -g_max_groups_per_pkts  [expr [expr $i + 3] * 3]               \
        -g_max_sources_per_group [expr [expr $i + 4] * 4]              \
    ]
    if {[keylget group_config status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget group_config log]"
        return 0
    }
    set g_handle [keylget group_config handle]
    set group_pool_handle [keylget group_config group_pool_handle]
    set source_pool_handle [keylget group_config source_pool_handles]
    lappend group_list_handle_0_3 $g_handle
    set source_list [concat $source_list [lrange $s_addr_1 0 $i]]
}

#############################################################################################
# Adding 5 groups, each with 2 sources to the 5th host on port_1                            #
#############################################################################################
set group_list_handle_0_4 [list ]
for {set i 0} {$i < 5} {incr i} {
    set group_config [::ixiangpf::emulation_mld_group_config \
        -mode                   create                                 \
        -session_handle         [lindex $mld_router_handles_h1_3 4]    \
        -group_pool_handle      [lindex $g_list $i]                    \
        -source_pool_handle     [lrange $s_list_1 $i [expr $i + 1]]    \
        -g_enable_packing       0                                      \
        -g_filter_mode          exclude                                \
        -g_max_groups_per_pkts  [expr [expr $i + 3] * 3]               \
        -g_max_sources_per_group [expr [expr $i + 4] * 4]              \
    ]
    if {[keylget group_config status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget group_config log]"
        return 0
    }
    set g_handle [keylget group_config handle]
    set group_pool_handle [keylget group_config group_pool_handle]
    set source_pool_handle [keylget group_config source_pool_handles]
    lappend group_list_handle_0_4 $g_handle
}


#############################################################################################
# Modifying group#2 from host1 on port_1 and replacing it with the 10th group created       #
#############################################################################################

set group_config [::ixiangpf::emulation_mld_group_config \
    -mode               modify                          \
    -handle  [lindex $group_list_handle_0_0 1]           \
    -group_pool_handle [lindex $g_list end]             \
]
if {[keylget group_config status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_config log]"
    return 0
}
set handle [keylget group_config handle]

#############################################################################################
# Modifying source#1 and #2 from group#3 from host1 on port_1                               #
#############################################################################################

set group_config [::ixiangpf::emulation_mld_group_config \
    -mode               modify                          \
    -handle  [lindex $group_list_handle_0_0 2]          \
    -group_pool_handle [lindex $g_list end]             \
    -source_pool_handle [lrange $s_list_1 end-1 end]    \
]
if {[keylget group_config status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_config log]"
    return 0
}
set handle [keylget group_config handle]


#############################################################################################
# Modifying the group + source#2 from host2 from port_1                                     #
#############################################################################################

set group_config [::ixiangpf::emulation_mld_group_config \
    -mode               modify                          \
    -handle             $group_list_handle_0_1          \
    -group_pool_handle [lindex $g_list end-2]             \
    -source_pool_handle [list [lindex $s_list_1 end-2] [lindex $s_list_1 0] [lindex $s_list_1 end]]   \
    -g_enable_packing       0                                      \
    -g_filter_mode          exclude                                \
    -g_max_groups_per_pkts  10               \
    -g_max_sources_per_group 30              \
]
if {[keylget group_config status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_config log]"
    return 0
}


############################################################################################# 
# Modifying the group and source#1 from host2 from port_1                                   #
#############################################################################################

set group_config [::ixiangpf::emulation_mld_group_config \
    -mode               modify                          \
    -handle             $group_list_handle_0_1          \
    -group_pool_handle [lindex $g_list end]             \
    -source_pool_handle [list [lindex $s_list_1 0] [lindex $s_list_1 0] [lindex $s_list_1 end]]   \
]
if {[keylget group_config status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_config log]"
    return 0
}


#############################################################################################
# Modifying all the groups and sources from host3 on port_1                                 #
#############################################################################################

for {set i 0} {$i <[llength $group_list_handle_0_2]} {incr i} {
    set group_config [::ixiangpf::emulation_mld_group_config \
        -mode               modify                          \
        -handle             [lindex $group_list_handle_0_2 $i]         \
        -group_pool_handle [lindex $g_list $i]             \
        -source_pool_handle [lrange $s_list_1 0 [expr $i + 2]]   \
    ]
    if {[keylget group_config status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget group_config log]"
        return 0
    }
    set handle [keylget group_config handle]
}


#############################################################################################
# Modifying 2 of the groups and 5 of the sources from host4 on port_1                       #
#############################################################################################

for {set i 1} {$i <3} {incr i} {
    set group_config [::ixiangpf::emulation_mld_group_config \
        -mode               modify                          \
        -handle             [lindex $group_list_handle_0_3 $i]         \
        -group_pool_handle  [lindex $g_list end-$i]             \
        -source_pool_handle [lrange $s_list_1 0 [expr 5 - $i]]   \
    ]
    if {[keylget group_config status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget group_config log]"
        return 0
    }
    set handle [keylget group_config handle]
}

#########################################################################################################################
# Modifying the first source from the first 3 groups from host5 and the last source from the last 2 groups from host5   #
#########################################################################################################################

for {set i 0} {$i < 3} {incr i} {
    set group_config [::ixiangpf::emulation_mld_group_config \
        -mode                   modify                                 \
        -handle                 [lindex $group_list_handle_0_4 $i]    \
        -group_pool_handle      [lindex $g_list end-$i]                    \
        -source_pool_handle     [list [lindex $s_list_1 end-$i] [lindex $s_list_1 [expr $i + 1]]]    \
    ]
    if {[keylget group_config status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget group_config log]"
        return 0
    }
    set g_handle [keylget group_config handle]
}


for {set i 3} {$i < 5} {incr i} {
    set group_config [::ixiangpf::emulation_mld_group_config \
        -mode                   modify                                 \
        -handle                 [lindex $group_list_handle_0_4 $i]    \
        -group_pool_handle      [lindex $g_list end-$i]                    \
        -source_pool_handle     [list [lindex $s_list_1 $i] [lindex $s_list_1 [expr 6-$i]]]    \
    ]
    if {[keylget group_config status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget group_config log]"
        return 0
    }
    set g_handle [keylget group_config handle]
}


################################
# Starting MLD on both ports   #
################################

set group_control [::ixiangpf::emulation_mld_control \
    -mode start                 \
    -port_handle [list $port_1 $port_2] \
]
if {[keylget group_control status] != $::SUCCESS} {
    puts "FAIL - $test_name -  [keylget group_control log]"
    return 0
}

after 30000

##########################################################################
# Performing ::emulation_mld_control with -mode leave & 3 group ranges   #
##########################################################################

set group_control [::ixiangpf::emulation_mld_control \
    -mode leave                 \
    -handle [list [lindex $mld_router_handles_h1_3 4] [lindex $mld_router_handles_h1_3 3] [lindex $mld_router_handles_h1_3 1]] \
]
if {[keylget group_control status] != $::SUCCESS} {
    puts "FAIL - $test_name -  [keylget group_control log]"
    return 0
}
after 5000

##########################################################################################################################
# Performing ::emulation_mld_control with -mode join on the 3 groups for which leave was issued in the previous command  #
##########################################################################################################################

set group_control [::ixiangpf::emulation_mld_control \
    -mode join                 \
    -handle [list [lindex $mld_router_handles_h1_3 4] [lindex $mld_router_handles_h1_3 3] [lindex $mld_router_handles_h1_3 1]] \
]
if {[keylget group_control status] != $::SUCCESS} {
    puts "FAIL - $test_name -  [keylget group_control log]"
    return 0
}

#########################################################################################################################
# Performing ::emulation_mld_control with mode -restart and 2 MLD hosts                                                 #
#########################################################################################################################

set group_control [::ixiangpf::emulation_mld_control \
    -mode restart                 \
    -handle [lrange $mld_router_handles_h1_3 1 2] \
]
if {[keylget group_control status] != $::SUCCESS} {
    puts "FAIL - $test_name -  [keylget group_control log]"
    return 0
}
after 30000


#########################################################################################################################
# Performing ::emulation_mld_control command with -mode stop and an MLD host handle                                     #
#########################################################################################################################
set group_control [::ixiangpf::emulation_mld_control \
    -mode stop                 \
    -handle [lindex $mld_router_handles_h1_3 4] \
]
if {[keylget group_control status] != $::SUCCESS} {
    puts "FAIL - $test_name -  [keylget group_control log]"
    return 0
}
after 60000

##########################################################################################################################
# Performing ::emulation_mld_control command with -mode start and an MLD host handle                                     #
##########################################################################################################################
set group_control [::ixiangpf::emulation_mld_control \
    -mode start                 \
    -handle [lindex $mld_router_handles_h1_3 4] \
]
if {[keylget group_control status] != $::SUCCESS} {
    puts "FAIL - $test_name -  [keylget group_control log]"
    return 0
}
after 60000

##########################################################################################################################
# Performing ::emulation_mld_control command with -mode stop and port_handle                                             #
##########################################################################################################################
set group_control [::ixiangpf::emulation_mld_control \
    -mode stop                 \
    -port_handle $port_1 \
]
if {[keylget group_control status] != $::SUCCESS} {
    puts "FAIL - $test_name -  [keylget group_control log]"
    return 0
}
after 60000


##########################################################################################################################
# Performing ::emulation_mld_control command with -mode start and port_handle                                            #
##########################################################################################################################
set group_control [::ixiangpf::emulation_mld_control \
    -mode start                 \
    -port_handle [list $port_1 $port_2] \
]
if {[keylget group_control status] != $::SUCCESS} {
    puts "FAIL - $test_name -  [keylget group_control log]"
    return 0
}
after 60000

##########################################################################################################################


puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1


