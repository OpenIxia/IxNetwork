################################################################################
# Version 1.0    $Revision: 2 $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-24-2007: MHasegan - created sample
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
#    This sample configures a PPPoEoA tunnel with 5 sessions.                  #
#    Then it connects to the DUT(Cisco7206) and retrieves a few statistics.    #
#    Traffic is sent over the tunnel and the DUT sends                         #
#    it to the DST port. After that a few statistics are being retrieved.      #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a ATM/POS622-MultiRate-256Mb module.             #
#                                                                              #
################################################################################

################################################################################
# DUT configuration:
#
# configure terminal
# vpdn enable
#
# interface Loopback213
#  ip address 11.0.0.1 255.255.0.0
#
# ip local pool mhaseganPPPoEoA 11.0.0.2 11.0.255.254
#
# interface Virtual-Template 213
#  ip unnumbered Loopback213
#  no logging event link-status
#  no snmp trap link-status
#  peer default ip address pool mhaseganPPPoEoA
#  no keepalive
#  ppp max-bad-auth 20
#  ppp mtu adaptive
#  ppp bridge ip
#  ppp ipcp address accept
#  ppp timeout retry 10
#
#
# bba-group pppoe mhasegan
#  virtual-template 213
#
#
# interface ATM1/0
#  no ip address
#  no ip route-cache
#  no ip mroute-cache
#  no atm ilmi-keepalive
#  no shut
#  range pvc 1/32 1/36
#  encapsulation aal5snap
#  protocol pppoe group mhasegan
#
# interface ATM2/0
#  ip address 14.0.0.1 255.255.0.0
#  no ip route-cache
#  no ip mroute-cache
#  no atm ilmi-keepalive
#  no shut
#
#  pvc 1/32
#   protocol ip 14.0.0.100 broadcast
#   encapsulation aal5snap
#
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 4/1 4/2]
set session_count 5

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassisIP      \
        -port_list              $port_list      \
        -username               ixiaApiUser     ]
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

set port_src_handle [lindex $port_handle 0]
set port_dst_handle [lindex $port_handle 1]

puts "Ixia port handles are $port_handle "

########################################
# Configure SRC interface in the test  #
########################################
set interface_status [::ixia::interface_config \
        -port_handle      $port_src_handle     \
        -speed            oc3                  \
        -intf_mode        atm                  \
        -tx_c2            13                   \
        -rx_c2            13                   ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

########################################
# Configure DST interface  in the test #
########################################

set interface_status [::ixia::interface_config \
        -port_handle      $port_dst_handle     \
        -mode             config               \
        -speed            oc3                  \
        -intf_mode        atm                  \
        -tx_c2            13                   \
        -rx_c2            13                   \
        -atm_encapsulation LLCRoutedCLIP       \
        -vpi              1                    \
        -vci              32                   \
        -intf_ip_addr     14.0.0.100           \
        -gateway          14.0.0.1             \
        -netmask          255.255.0.0          \
        ]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set int_handle [keylget interface_status interface_handle]

###############################################
# Configure session                           #
###############################################

set pppox_config_status [::ixia::pppox_config          \
        -mode                        add               \
        -port_handle                 $port_src_handle  \
        -protocol                    pppoeoa           \
        -encap                       llcsnap           \
        -num_sessions                $session_count    \
        -vci                         32                \
        -vci_step                    1                 \
        -vci_count                   $session_count    \
        -pvc_incr_mode               vci               \
        -vpi                         1                 \
        -vpi_step                    1                 \
        -vpi_count                   1                 \
        -ppp_local_ip                11.0.0.2          \
        -ppp_local_ip_step           0.0.0.1           \
        ]

if {[keylget pppox_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pppox_config_status log]"
}

set pppox_handle [keylget pppox_config_status handle]

################################################
#  Setup session                               #
################################################
set pppox_control_status [::ixia::pppox_control  \
        -handle                 $pppox_handle  \
        -action                 connect        \
        ]

if {[keylget pppox_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pppox_control_status log]"
}

################################################
#  Stats      
################################################
set aggr_status [::ixia::pppox_stats \
        -port_handle $port_src_handle\
        -mode   aggregate            ]
if {[keylget aggr_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggr_status log]"
}

set sess_num       [keylget aggr_status $port_src_handle.aggregate.num_sessions]
set sess_count_up  [keylget aggr_status $port_src_handle.aggregate.connected]
set sess_min_setup [keylget aggr_status $port_src_handle.aggregate.min_setup_time]
set sess_max_setup [keylget aggr_status $port_src_handle.aggregate.max_setup_time]
set sess_avg_setup [keylget aggr_status $port_src_handle.aggregate.avg_setup_time]

puts "Ixia Session Setup Test Results ... "
puts "        Number of sessions           = $sess_num "
puts "        Number of connected sessions = $sess_count_up "
puts "        Minimum Setup Time (ms)      = $sess_min_setup "
puts "        Maximum Setup Time (ms)      = $sess_max_setup "
puts "        Average Setup Time (ms)      = $sess_avg_setup "

################################################################################
# Delete all the streams first                                                 #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action             reset                                           \
        -traffic_generator  ixnetwork                                       \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

#########################################
#  Configure traffic                    #
#########################################
set traffic_status [::ixia::traffic_config                  \
        -mode                 create                        \
        -traffic_generator    ixnetwork                     \
        -bidirectional        1                             \
        -emulation_dst_handle $int_handle                   \
        -emulation_src_handle $pppox_handle                 \
        -track_by             endpoint_pair                 \
        -circuit_endpoint_type ipv4                         \
        -transmit_mode        return_to_id_for_count        \
        -loop_count           10                            \
        -stream_packing       one_stream_per_endpoint_pair  \
        -length_mode          increment                     \
        -frame_size_step      1                             \
        -frame_size_min       800                           \
        -frame_size_max       1500                          \
        -pkts_per_burst       2                             \
        -rate_percent         4.5                           \
        -enforce_min_gap      9                             \
        -tx_delay             10                            \
        -inter_frame_gap      8                             \
        -inter_burst_gap      11                            \
        -inter_stream_gap     12                            \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Start the traffic                                                            #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# The traffic must flow!                                                       #
################################################################################
after 5000

################################################################################
# Stop the traffic                                                             #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Wait for the traffic to stop                                                 #
################################################################################
after 15000

################################################################################
# Gather and display traffic statistics                                        #
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

set stream_traffic_status [::ixia::traffic_stats                            \
        -mode                   stream                                      \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget stream_traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget stream_traffic_status log]"
}
set stream_tx_results [list                                                 \
        "Tx Frames"                     total_pkts                          \
        "Tx Frame Rate"                 total_pkt_rate                      \
        ]
set stream_rx_results [list                                                 \
        "Rx Frames"                     total_pkts                          \
        "Frames Delta"                  loss_pkts                           \
        "Rx Frame Rate"                 total_pkt_rate                      \
        "Loss %"                        loss_percent                        \
        "Rx Bytes"                      total_pkts_bytes                    \
        "Rx Rate (Bps)"                 total_pkt_byte_rate                 \
        "Rx Rate (bps)"                 total_pkt_bit_rate                  \
        "Rx Rate (Kbps)"                total_pkt_kbit_rate                 \
        "Rx Rate (Mbps)"                total_pkt_mbit_rate                 \
        "Avg Latency (ns)"              avg_delay                           \
        "Min Latency (ns)"              min_delay                           \
        "Max Latency (ns)"              max_delay                           \
        "First Timestamp"               first_tstamp                        \
        "Last Timestamp"                last_tstamp                         \
        ]
foreach port $port_handle {
    puts "Port $port:"
    set streams [keylget stream_traffic_status \
            $port.stream]
    foreach stream [keylkeys streams] {
        set stream_key [keylget stream_traffic_status \
                $port.stream.$stream]
        foreach dir [keylkeys stream_key] {
            puts "\tStream $stream - $dir:"
            foreach {name key} [subst $[subst stream_${dir}_results]] {
                puts "\t\t$name: [keylget stream_traffic_status\
                        $port.stream.$stream.$dir.$key]"
            }
        }
    }
}

#########################################
#  Disconnect sessions                  #
#########################################
puts "Disconnecting $sess_count_up sessions. "
set control_status [::ixia::pppox_control \
        -handle     $pppox_handle         \
        -action     disconnect            ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

set cleanup_status [::ixia::cleanup_session -port_handle $port_handle]
if {[keylget cleanup_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget cleanup_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
