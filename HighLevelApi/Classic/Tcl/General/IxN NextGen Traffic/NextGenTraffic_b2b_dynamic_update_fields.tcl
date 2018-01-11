################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Eduard Tutescu $
#
#    Copyright © 1997 - 2012 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    12-05-2012 Eduard Tutescu
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
# This script creates a traffic item and configurest the dynamic_field_updates #
# Module:                                                                      #
#    The sample was tested on an STXS4 module.                                 #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassis_ip  10.205.16.98
set port_list [list 7/1 7/2]
set sess_count 20
set ixnetwork_tcl_server localhost
# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect                 \
        -reset                                      \
        -device    $chassis_ip                      \
        -port_list $port_list                       \
        -username  ixiaApiUser                      \
        -ixnetwork_tcl_server $ixnetwork_tcl_server \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set port_src_handle [lindex $port_handle 0]
set port_dst_handle [lindex $port_handle 1]

puts "Ixia port handles are $port_handle "

########################################
# Configure SRC interface in the test  #
########################################
set interface_status [::ixia::interface_config \
        -port_handle      $port_src_handle     \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

########################################
# Configure DST interface  in the test #
########################################
set interface_status [::ixia::interface_config \
        -port_handle      $port_dst_handle     \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

#########################################
#  Configure sessions                   #
#########################################
set config_status [::ixia::pppox_config      \
        -port_handle      $port_src_handle   \
        -protocol         pppoe              \
        -encap            ethernet_ii    \
        -num_sessions     $sess_count        \
        -port_role           access                \
        -disconnect_rate  10                 \
        -redial                 1                        \
        -redial_max          10                    \
        -redial_timeout      20                    \
        -ip_cp            ipv4_cp            \
        -ppp_local_mode   peer_only ]
if {[keylget config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget config_status log]"
}
set pppox_handle [keylget config_status handle]
puts "Ixia pppox_handle is $pppox_handle "

set config_status2 [::ixia::pppox_config     \
        -port_handle      $port_dst_handle   \
        -protocol         pppoe              \
        -encap            ethernet_ii        \
        -num_sessions     $sess_count        \
        -port_role           network                  \
        -ip_cp            ipv4_cp            \
        -ppp_local_mode   local_only         \
        -ppp_local_ip     25.10.10.1         \
        -ppp_peer_mode    local_only          \
        -ppp_peer_ip      25.10.10.2         \
        -ppp_peer_ip_step 0.0.0.1            ]
if {[keylget config_status2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget config_status2 log]"
}
set pppox_handle2 [keylget config_status2 handle]
puts "Ixia pppox_handle2 is $pppox_handle2 "
#########################################
#  Connect sessions                     #
#########################################
set control_status [::ixia::pppox_control \
        -handle     $pppox_handle         \
        -action     connect               ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}
set control_status2 [::ixia::pppox_control \
        -handle     $pppox_handle2         \
        -action     connect               ]
if {[keylget control_status2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status2 log]"
}
puts "Sessions..."

after 60000
################################################################################
# Get PPPoE session aggregate statistics
################################################################################
 set pppoe_attempts  0
 set pppoe_sessions_up 0
 while {($pppoe_attempts < 20) && ($pppoe_sessions_up < $sess_count)} {
     after 10000
     set pppox_status [::ixia::pppox_stats \
             -handle   $pppox_handle       \
             -mode     aggregate           ]
     
     if {[keylget pppox_status status] != $::SUCCESS} {
         return "FAIL - $test_name - [keylget pppox_status log]"
     }
     set  aggregate_stats   [keylget pppox_status aggregate]
     set  pppoe_sessions_up [keylget aggregate_stats sessions_up]
     puts "pppoe_sessions_up=$pppoe_sessions_up"
     incr pppoe_attempts
 }
 
if {$pppoe_sessions_up < $sess_count} {
     return "FAIL - $test_name - Not all sessions are up."
}
set traffic_status [::ixia::traffic_config         \
        -mode                 reset                \
        -port_handle          $port_src_handle     \
        -emulation_src_handle $pppox_handle        \
        -ip_src_mode          emulation            ]

if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}
set traffic_status [::ixia::traffic_config          \
        -mode                 reset                 \
        -port_handle          $port_dst_handle      \
        -emulation_src_handle $pppox_handle2        \
        -ip_src_mode          emulation             ]

if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

# #########################################
#  Configure traffic                    #
#########################################
set traffic_status [::ixia::traffic_config      \
        -mode                 create            \
        -bidirectional        1                 \
        -port_handle          $port_src_handle  \
        -port_handle2         $port_dst_handle  \
        -l3_protocol          ipv4              \
        -ip_src_mode          emulation         \
        -ip_src_count         $sess_count       \
        -emulation_src_handle $pppox_handle     \
        -emulation_dst_handle $pppox_handle2     \
        -ip_dst_mode          emulation          \
        -l3_length            100              \
        -rate_percent         5                 \
        -transmit_mode        continuous        \
        -mac_dst_mode         discovery         \
        -dynamic_update_fields ppp \
        ]
# Check dynamic update fields

if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

set current_config_element [keylget traffic_status traffic_item]
set stack_handle [lindex [keylget traffic_result $current_config_element.headers] 0]

set traffic_result [::ixia::traffic_config                  \
    -mode                           modify                  \
    -traffic_generator              ixnetwork_540           \
    -stream_id                      $current_config_element \
    -dynamic_update_fields          mpls_label_value        \

]

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1