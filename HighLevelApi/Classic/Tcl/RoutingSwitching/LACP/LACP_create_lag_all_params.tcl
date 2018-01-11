################################################################################
# Version 1.1    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    12-05-2008 LRaicea - created sample
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
#    This sample creates one LAG using two Ixia ports.                         #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET42.                                      #
#                                                                              #
################################################################################
################################################################################
# DUT (cisco 3750) configuration layer 2:
#
# conf t
# default interface range GigabitEthernet 1/0/3-10
# no interface Port-channel 3
# no interface Port-channel 5
# no interface Port-channel 7
# no interface Port-channel 9
# 
# #LACP aggregator interface configuration
# interface Port-channel3
#  switchport
#  no ip address
# !
# #LACP port 1
# interface GigabitEthernet1/0/3
#  switchport
#  no ip address
#  channel-group 3 mode active
#  channel-protocol lacp
# !
# 
# #LACP port 2
# interface GigabitEthernet1/0/4
#  switchport
#  no ip address
#  channel-group 3 mode active
#  channel-protocol lacp
#
################################################################################

set env(IXIA_VERSION) HLTSET42
package require Ixia

################################################################################
# General script variables
################################################################################
set test_name               [info script]

################################################################################
# START - Connect to the chassis
################################################################################
puts "Start connecting to chassis ..."
update idletasks

set chassis_ip              sylvester
set port_list               [list 1/1 1/2]
set break_locks             1
set username                ixiaApiUser

set connect_status [::ixia::connect                                        \
        -reset                                                             \
        -device               $chassis_ip                                  \
        -port_list            $port_list                                   \
        -break_locks          $break_locks                                 \
        -username             $username                                    \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
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
    
    # Initialize per port variables
    set interface_handles_$port ""
    
    incr i
}

puts "End connecting to chassis ..."
update idletasks
################################################################################
# END - Connect to the chassis
################################################################################

################################################################################
# START - Interface configuration - L1
################################################################################
puts "Start L1 interface configuration ..."
update idletasks


set qos_stats                   1                                              ;# CHOICES 0 1
set qos_byte_offset             14                                             ;# RANGE 0-63 DEFAULT 14
set qos_pattern_offset          12                                             ;# RANGE 0-65535 DEFAULT 12
set qos_pattern_match           0800                                           ;# DEFAULT 0800
set qos_pattern_mask            0000                                           ;# DEFAULT 0000
set qos_packet_type             ethernet                                       ;# CHOICES ethernet ip_snap vlan custom ip_ppp ip_cisco_hdlc ip_atm]


set interface_status [::ixia::interface_config                         \
        -port_handle                 $port_handle                      \
        -mode                        config                            \
        -intf_mode                   ethernet                          \
        -autonegotiation             1                                 \
        -speed                       auto                              \
        -duplex                      auto                              \
        -phy_mode                    copper                            \
        -transmit_mode               advanced                          \
        -port_rx_mode                wide_packet_group                 \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

puts "End L1 interface configuration ..."
update idletasks
################################################################################
# END - Interface configuration - L1
################################################################################################################################################################
################################################################################
# START - LACP configuration
################################################################################
puts "Start LACP configuration ..."
update idletasks

set lacp_link_config_status [::ixia::emulation_lacp_link_config                \
        -mode                                  create                          \
        -reset                                                                 \
        -lag_count                             1                               \
        -port_handle                           $port_handle                    \
        -actor_key                             3                               \
        -actor_key_step                        1                               \
        -actor_port_num                        1                               \
        -actor_port_num_step                   1                               \
        -actor_port_pri                        1                               \
        -actor_port_pri_step                   1                               \
        -actor_system_id                       0013.0101.0284                  \
        -actor_system_id_step                  0000.0002.0000                  \
        -actor_system_pri                      1                               \
        -actor_system_pri_step                 1                               \
        -aggregation_flag                      auto                            \
        -auto_pick_port_mac                    1                               \
        -collecting_flag                       1                               \
        -collector_max_delay                   0                               \
        -distributing_flag                     1                               \
        -inter_marker_pdu_delay                6                               \
        -lacp_activity                         active                          \
        -lacp_timeout                          auto                            \
        -lacpdu_periodic_time_interval         auto                            \
        -marker_req_mode                       fixed                           \
        -marker_res_wait_time                  5                               \
        -port_mac                              0013.0101.0284                  \
        -port_mac_step                         0000.0002.0000                  \
        -send_marker_req_on_lag_change         1                               \
        -send_periodic_marker_req              0                               \
        -support_responding_to_marker          1                               \
        -sync_flag                             auto                            \
        ]
if {[keylget lacp_link_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp_link_config_status log]"
    return
}
set lacp_link_handles [keylget lacp_link_config_status handle]
puts "Ixia LACP handles are: "
update idletasks
foreach lacp_link_handle $lacp_link_handles {
    puts $lacp_link_handle
    update idletasks
}

################################################################################
# END - LACP configuration
################################################################################
################################################################################
# LACP - Protocol start
################################################################################
set lacp_control_status [::ixia::emulation_lacp_control                        \
        -mode            start                                                 \
        -port_handle     $port_handle                                          \
        ]
if {[keylget lacp_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp_control_status log]"
    return
}
puts "Starting LACP protocol ..."
update idletasks
# Wait for links to be aggregated
after 30000

################################################################################
# LACP - Gather learned info
################################################################################
set lacp_agg_links 0
set retries        20
puts "Retrieving LACP learned info ..."
update idletasks
while {($lacp_agg_links < [llength $port_handle]) && $retries} {
    set lacp_info_status [::ixia::emulation_lacp_info                          \
            -mode            learned_info                                      \
            -port_handle     $port_handle                                      \
            ]
    if {[keylget lacp_info_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget lacp_info_status log]"
        return
    }
    set lacp_agg_links 0
    foreach port $port_handle {
        if {![catch {keylget lacp_info_status $port.actor_link_aggregation_status} retStat]} {
            if {$retStat == 1} {
                incr lacp_agg_links
            }
        }
    }
    incr retries -1
    puts "LACP aggregated links - $lacp_agg_links ..."
}
if {$lacp_agg_links < [llength $port_handle]} {
    puts "FAIL - $test_name - Not all LACP links have been aggregated."
    return
}

################################################################################
# Display learned info
################################################################################
foreach port $port_handle {
    puts "\n\nPort $port learned info:"
    foreach key [keylkeys lacp_info_status $port] {
        puts [format "%30s %s" $key [keylget lacp_info_status $port.$key]]
    }
}
################################################################################
# LACP - Protocol stop
################################################################################
set lacp_control_status [::ixia::emulation_lacp_control                        \
        -mode            stop                                                  \
        -port_handle     $port_handle                                          \
        ]
if {[keylget lacp_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp_control_status log]"
    return
}
puts "Stopping LACP protocol ..."
update idletasks

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return
