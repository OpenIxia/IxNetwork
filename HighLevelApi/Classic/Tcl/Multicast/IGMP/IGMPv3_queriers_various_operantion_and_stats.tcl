################################################################################
# Version 1.1    $Revision: 0 $
# $Author: Florin Barbuceanu $
#
#    Copyright © 1997 - 2013 by IXIA
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
#    This sample performs various operations. It creates, starts, stops,delete #
#    and retreive statistics for an IGMPv2 querier. Also it creates an IGMPv2  #
#    host and a multicast group pool that will be assigned to the host.        #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################

#Procedure used to print  statistics
proc keylprint {var_ref} {
    upvar 1 $var_ref var
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
    set indent [string repeat " " $level]
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

package require Ixia

set test_name [info script]
set chassis_ip                  10.215.180.120
set tcl_server                  10.215.180.120
set ixnetwork_tcl_server        127.0.0.1:8009
set port_list                   [list 5/1 5/2]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect 

set connect_status [::ixia::connect 				     \
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

set port_1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]
set port_handle [list $port_1 $port_2] 

##################################################
#  Configure interfaces and create IGMP sessions #
##################################################

puts "Configure IGMP host"


set ip_router_alert         1
set host                    100.0.1.2
set query                   100.0.1.1
set vlan_id                 10
set vlan_id_step            1
set vlan_user_priority      4

#Configure IGMPv2 host
set igmp_status [::ixia::emulation_igmp_config          \
        -port_handle           $port_1                  \
        -reset                                          \
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
        -intf_prefix_len       24                       \
        -vlan_id_mode          increment                \
        -vlan_id               $vlan_id                 \
        -vlan_id_step          $vlan_id_step            \
        -vlan_user_priority    $vlan_user_priority      \
        -max_response_time     0                        \
        -max_response_control  1                        \
        ]
if {[keylget igmp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status log]"
    return 0
}
set host_handle [keylget igmp_status handle]

#Configure IGMPv2 queriers
puts "Configure IGMP querier..."

set igmp_status [::ixia::emulation_igmp_querier_config          \
        -port_handle                       $port_2              \
        -mode                              create               \
        -reset                                                  \
        -specific_query_response_interval  1000                 \
        -robustness_variable               2                    \
        -support_older_version_host        1                    \
        -support_older_version_querier     1                    \
        -support_election                  1                    \
        -specific_query_transmission_count 2                    \
        -startup_query_count               2                    \
        -igmp_version                      v3                   \
        -query_interval                    125                  \
        -discard_learned_info 0                                 \
        -general_query_response_interval   10000                \
        -msg_count_per_interval            0                    \
        -msg_interval                      0                    \
        -count                             1                    \
        -intf_ip_addr                      $query               \
        -neighbor_intf_ip_addr             $host                \
        -intf_prefix_len                   24                   \
        -vlan_id_mode                      increment            \
        -vlan_id                           $vlan_id             \
        -vlan_id_step                      $vlan_id_step        \
        -vlan_user_priority                $vlan_user_priority  \
        ]

 if {[keylget igmp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status log]"
    return 0
}
set query_handle [keylget igmp_status handle]

##############################################################################
# Create IGMP group member by asociating a multicast group pool to a host    #
##############################################################################

set session_handle       100.0.1.2
set mgroup_params  [list 226.0.1.1/0.0.0.1/5                       226.0.1.6/0.0.0.2/4]
set msource_params [list 100.0.1.2/0.0.0.2/2,110.0.1.2/0.0.0.1/3   120.0.1.2/0.0.0.1/5,130.0.1.2/0.0.0.1/5,140.0.1.2/0.0.0.1/5]

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

##############################################################################
#                    Start IGMP hosts and queriers                           #
##############################################################################

puts "Starting IGMP"

#Start IGMPv2 host
set igmp_status [::ixia::emulation_igmp_control	\
        -mode   start                           \
        -handle $host_handle                    \
]

if {[keylget igmp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status log]"
    return 0
}

#Start IGMPv2 queriers
set igmp_status [::ixia::emulation_igmp_control \
        -mode   start                           \
        -handle $query_handle                   \
]

if {[keylget igmp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status log]"
    return 0
}

after 10000

##############################################################################
#                           Retrieve IGMP querier stats                      #
##############################################################################

puts "Retrieve aggregate stats"

set igmp_stats [::ixia::emulation_igmp_info         \
        -mode   aggregate                           \
        -port_handle  $port_2                       \
        -type querier                               \
]

if {[keylget igmp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_stats log]"
    return 0
}

#Display aggregate stats
keylprint igmp_stats

puts "Retrieve learn info stats"
set igmp_stats [::ixia::emulation_igmp_info         \
        -mode   learned_info                        \
        -port_handle  $port_2                       \
]

if {[keylget igmp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_stats log]"
    return 0
}

#Display learn_info stats
keylprint igmp_stats
##############################################################################
#                           Stop IGMP                                        #
##############################################################################
puts "Stop IGMP"

#Stop querier
set igmp_status [::ixia::emulation_igmp_control \
        -mode   stop                            \
        -handle	$query_handle                   \
]

if {[keylget igmp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status log]"
    return 0
}

#Stop host
set igmp_status [::ixia::emulation_igmp_control \
        -mode   stop                            \
        -handle $host_handle                    \
]

if {[keylget igmp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status log]"
    return 0
        
}
##############################################################################
#                           Delete querier                                   #
##############################################################################
set igmp_status [::ixia::emulation_igmp_querier_config          \
        -port_handle           $port_2                          \
        -mode                  delete                           \
        -handle	               $query_handle                    \
]

return "SUCCESS - $test_name - [clock format [clock seconds]]"