################################################################################
# Version 1.0    $Revision: 2 $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-24-2007: MHasegan
#    04-09-2008: LRaicea  - updated statistics list
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
#    This sample configures a PPPoA tunnel with 20 sessions between the        #
#    SRC port and the DST port.                                                #
#    Traffic is sent over the tunnels and statistics.                          #
#    After that a few statistics are being retrieved.                          #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a ATM/POS622-MultiRate-256Mb module.             #
#                                                                              #
################################################################################
package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 4/1 4/2]
set sess_count 20
################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassisIP      \
        -port_list              $port_list      \
        -break_locks            1              ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set port_0 [lindex $port_handle 0]
set port_1 [lindex $port_handle 1]

puts "Ixia port handles are $port_handle "
################################################################################
# Configure SRC interface in the test
################################################################################
set interface_status [::ixia::interface_config \
        -port_handle      $port_0              \
        -speed            oc3                  \
        -intf_mode        atm                  \
        -tx_c2            13                   \
        -rx_c2            13                   \
        ]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
################################################################################
# Configure DST interface  in the test
################################################################################
set interface_status [::ixia::interface_config \
        -port_handle      $port_1              \
        -speed            oc3                  \
        -intf_mode        atm                  \
        -tx_c2            13                   \
        -rx_c2            13                   \
        ]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
################################################################################
# Configure sessions
################################################################################
set config_status [::ixia::pppox_config      \
        -mode             add                \
        -port_handle      $port_0            \
        -protocol         pppoa              \
        -encap            vc_mux             \
        -num_sessions     $sess_count        \
        -port_role        access             \
        -disconnect_rate  10                 \
        -redial           1                  \
        -redial_max       10                 \
        -redial_timeout   20                 \
        -ip_cp            ipv4_cp            \
        -vci              32                 \
        -vci_step         1                  \
        -vci_count        $sess_count        \
        -pvc_incr_mode    vci                \
        -vpi              1                  \
        -vpi_step         1                  \
        -vpi_count        1                  \
        ]
if {[keylget config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget config_status log]"
}
set pppox_handle [keylget config_status handle]
puts "Ixia pppox_handle is $pppox_handle "

set config_status2 [::ixia::pppox_config     \
        -mode             add                \
        -port_handle      $port_1            \
        -protocol         pppoa              \
        -encap            vc_mux             \
        -num_sessions     $sess_count        \
        -port_role        network            \
        -ip_cp            ipv4_cp            \
        -vci              32                 \
        -vci_step         1                  \
        -vci_count        $sess_count        \
        -pvc_incr_mode    vci                \
        -vpi              1                  \
        -vpi_step         1                  \
        -vpi_count        1                  \
        -ppp_local_ip     25.10.10.1         \
        -ppp_peer_ip      25.10.10.2         \
        -ppp_peer_ip_step 0.0.0.1            \
        ]
if {[keylget config_status2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget config_status2 log]"
}
set pppox_handle2 [keylget config_status2 handle]
puts "Ixia pppox_handle2 is $pppox_handle2 "
################################################################################
# Connect sessions
################################################################################
set control_status2 [::ixia::pppox_control \
        -handle     $pppox_handle2         \
        -action     connect                ]
if {[keylget control_status2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status2 log]"
}

set control_status [::ixia::pppox_control  \
        -handle     $pppox_handle          \
        -action     connect                ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}
################################################################################
# Retrieve aggregate session stats
################################################################################
set aggr_status [::ixia::pppox_stats \
        -port_handle $port_handle    \
        -mode        aggregate       ]

if {[keylget aggr_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggr_status log]"
}

set sess_num       [keylget aggr_status ${port_0}.aggregate.num_sessions]
set sess_count_up  [keylget aggr_status ${port_0}.aggregate.connected]
set sess_min_setup [keylget aggr_status ${port_0}.aggregate.min_setup_time]
set sess_max_setup [keylget aggr_status ${port_0}.aggregate.max_setup_time]
set sess_avg_setup [keylget aggr_status ${port_0}.aggregate.avg_setup_time]
puts "Ixia Test Results ... "
puts "        Number of sessions           = $sess_num "
puts "        Number of connected sessions = $sess_count_up "
puts "        Minimum Setup Time (ms)      = $sess_min_setup "
puts "        Maximum Setup Time (ms)      = $sess_max_setup "
puts "        Average Setup Time (ms)      = $sess_avg_setup "
################################################################################
# Delete all the streams first
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action             reset                                           \
        -traffic_generator  ixnetwork                                       \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}
################################################################################
# Configure traffic 
################################################################################
set traffic_status [::ixia::traffic_config      \
        -mode                 create            \
        -traffic_generator    ixnetwork         \
        -bidirectional        1                 \
        -emulation_dst_handle $pppox_handle2    \
        -emulation_src_handle $pppox_handle     \
        -track_by             endpoint_pair     ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}
################################################################################
# Start the traffic 
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}
################################################################################
# The traffic must flow! 
################################################################################
after 5000

################################################################################
# Stop the traffic 
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}
################################################################################
# Wait for the traffic to stop 
################################################################################
after 20000

################################################################################
# Gather and display traffic statistics  
################################################################################
set aggregated_traffic_status [::ixia::traffic_stats                        \
        -mode                   aggregate                                   \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget aggregated_traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggregated_traffic_status log]"
}
set aggregated_traffic_results {
    "AAL5 Frames Rx."              aggregate.rx.rx_aal5_frames_count
    "ATM Cells Rx."                aggregate.rx.rx_atm_cells_count
    "AAL5 Payload Bytes Tx."       aggregate.tx.tx_aal5_bytes_count
    "AAL5 Frames Tx."              aggregate.tx.tx_aal5_frames_count
    "Scheduled Cells Tx."          aggregate.tx.tx_aal5_scheduled_cells_count
    "Scheduled Frames Tx."         aggregate.tx.tx_aal5_scheduled_frames_count  
    "ATM Cells Tx."                aggregate.tx.tx_atm_cells_count
    "AAL5 Frames Rx. Rate"         aggregate.rx.rx_aal5_frames_rate
    "ATM Cells Rx. Rate"           aggregate.rx.rx_atm_cells_rate
    "AAL5 Payload Bytes Tx. Rate"  aggregate.tx.tx_aal5_bytes_rate              
    "AAL5 Frames Tx. Rate"         aggregate.tx.tx_aal5_frames_rate
    "Scheduled Cells Tx. Rate"     aggregate.tx.tx_aal5_scheduled_cells_rate
    "Scheduled Frames Tx. Rate"    aggregate.tx.tx_aal5_scheduled_frames_rate
    "ATM Cells Tx. Rate"           aggregate.tx.tx_atm_cells_rate
    }
foreach port $port_handle {
    puts "Port $port:"
    puts "\tAggregated statistics:"
    foreach {name key} $aggregated_traffic_results {
        puts "\t\t$name: [keylget aggregated_traffic_status\
                $port.$key]"
    }
}
################################################################################
# Disconnect sessions
################################################################################
set control_status [::ixia::pppox_control \
        -handle     $pppox_handle         \
        -action     disconnect            ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}
set control_status [::ixia::pppox_control \
        -handle     $pppox_handle2        \
        -action     disconnect            ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

set cleanup_status [::ixia::cleanup_session -port_handle $port_handle]
if {[keylget cleanup_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget cleanup_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
