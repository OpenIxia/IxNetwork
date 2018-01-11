################################################################################
# Version 1.0    $Revision: 1 $
# $Author: MHasegan $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    11-22-2008 Mircea Hasegan
#
# Description:
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
#    Back2Back configuration. Both ports acting as both Ingress and Egress.    #
#    P2MP LSPs and Sub-LSPs are established. RSVP statistics are returned.     #
#    Bidirectional RAW traffic is configured. Traffic statistics are returned. #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a STXS4 module.                                  #
#                                                                              #
################################################################################



package require Ixia

set test_name               [info script]

################################################################################
# START - Connect to the chassis
################################################################################
set chassis_ip              sylvester
set ixnetwork_tcl_server    localhost
set port_list               [list 2/3 2/4]

# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                        \
        -reset                                                             \
        -device               $chassis_ip                                  \
        -port_list            $port_list                                   \
        -ixnetwork_tcl_server $ixnetwork_tcl_server                        \
        -break_locks          1                                            \
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

set i 0
puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port
    incr i
}

################################################################################
# END - Connect to the chassis
################################################################################

set interface_status [::ixia::interface_config                             \
        -port_handle      $port_0                                          \
        -mode             config                                           \
        -intf_mode        ethernet                                         \
        -autonegotiation  1                                                \
        -speed            ether100                                         \
        -duplex           auto                                             \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set interface_status [::ixia::interface_config                             \
        -port_handle      $port_1                                          \
        -mode             config                                           \
        -intf_mode        ethernet                                         \
        -autonegotiation  1                                                \
        -speed            ether100                                         \
        -duplex           auto                                             \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# START - RSVP configuration
################################################################################
puts "\nRSVP configuration $port_0 - Ingress..."

################################################################################
# RSVP Call - port_0 - Ingress
################################################################################

set rsvp_config_status [::ixia::emulation_rsvp_config  \
        -mode                            create        \
        -count                           1             \
        -intf_ip_addr                    1.1.1.1       \
        -intf_prefix_length              24            \
        -ip_version                      4             \
        -neighbor_intf_ip_addr           1.1.1.2       \
        -port_handle                     $port_0       \
        -reset                                         \
    ]
if {[keylget rsvp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_config_status log]"
}

set rsvpHandleList_ingress [keylget rsvp_config_status handles]


################################################################################
# RSVP configuration $port_1 - Egress
################################################################################
puts "\nRSVP configuration $port_1 - Egress..."

set rsvp_config_status [::ixia::emulation_rsvp_config                           \
        -mode                            create        \
        -count                           1             \
        -intf_ip_addr                    1.1.1.2       \
        -intf_prefix_length              24            \
        -ip_version                      4             \
        -neighbor_intf_ip_addr           1.1.1.1       \
        -port_handle                     $port_1       \
        -reset                                         \
    ]
if {[keylget rsvp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_config_status log]"
}

set rsvpHandleList_egress [keylget rsvp_config_status handles]

################################################################################
# RSVP Tunnel configuration - Ingress
################################################################################
puts "\nRSVP Tunnel configuration - Ingress"

set rsvp_tunnel_config_status [::ixia::emulation_rsvp_tunnel_config        \
        -count                                    1                        \
        -emulation_type                           rsvptep2mp               \
        -handle                                   $rsvpHandleList_ingress  \
        -mode                                     create                   \
        -port_handle                              $port_0                  \
        -rsvp_behavior                            rsvpIngress              \
        -egress_ip_addr                           5.5.5.1                  \
        -egress_ip_step                           0.0.1.0                  \
        -egress_leaf_ip_count                     10                       \
        -egress_leaf_range_count                  10                       \
        -egress_leaf_range_step                   0.0.1.0                  \
        -p2mp_id                                  1                        \
        -ingress_ip_addr                          4.4.4.1                  \
        -lsp_id_start                             0                        \
        -tunnel_id_start                          1                        \
        -head_traffic_start_ip                    100.100.100.100          \
        -tail_traffic_start_ip                    224.0.0.20               \
    ]

if {[keylget rsvp_tunnel_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tunnel_config_status log]"
}

set rsvp_ingress_handle_0 [keylget rsvp_tunnel_config_status tunnel_handle]

################################################################################
# RSVP Tunnel configuration - Egress
################################################################################
puts "\nRSVP Tunnel configuration - Egress"

set rsvp_tunnel_config_status [::ixia::emulation_rsvp_tunnel_config        \
        -count                                    1                        \
        -emulation_type                           rsvptep2mp               \
        -handle                                   $rsvpHandleList_ingress  \
        -mode                                     create                   \
        -port_handle                              $port_0                  \
        -rsvp_behavior                            rsvpEgress               \
        -egress_ip_addr                           50.50.50.1               \
        -egress_ip_step                           0.0.1.0                  \
        -egress_leaf_ip_count                     10                       \
        -egress_leaf_range_count                  10                       \
        -egress_leaf_range_step                   0.0.1.0                  \
        -p2mp_id                                  2                        \
        -tail_traffic_start_ip                    225.0.0.20               \
    ]

if {[keylget rsvp_tunnel_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tunnel_config_status log]"
}

set rsvp_egress_handle_0 [keylget rsvp_tunnel_config_status tunnel_handle]

################################################################################
# RSVP Tunnel configuration - Ingress
################################################################################
puts "\nRSVP Tunnel configuration - Ingress"

set rsvp_tunnel_config_status [::ixia::emulation_rsvp_tunnel_config        \
        -count                                    1                        \
        -emulation_type                           rsvptep2mp               \
        -handle                                   $rsvpHandleList_egress  \
        -mode                                     create                   \
        -port_handle                              $port_1                  \
        -rsvp_behavior                            rsvpIngress              \
        -egress_ip_addr                           50.50.50.1               \
        -egress_ip_step                           0.0.1.0                  \
        -egress_leaf_ip_count                     10                       \
        -egress_leaf_range_count                  10                       \
        -egress_leaf_range_step                   0.0.1.0                  \
        -p2mp_id                                  2                        \
        -ingress_ip_addr                          7.7.7.1                  \
        -lsp_id_start                             7                        \
        -tunnel_id_start                          8                        \
        -head_traffic_start_ip                    101.101.101.101          \
        -tail_traffic_start_ip                    225.0.0.20               \
    ]

if {[keylget rsvp_tunnel_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tunnel_config_status log]"
}

set rsvp_ingress_handle_1 [keylget rsvp_tunnel_config_status tunnel_handle]

################################################################################
# RSVP Tunnel configuration - Egress
################################################################################
puts "\nRSVP Tunnel configuration - Egress"

set rsvp_tunnel_config_status [::ixia::emulation_rsvp_tunnel_config      \
        -count                                    1                      \
        -emulation_type                           rsvptep2mp             \
        -handle                                   $rsvpHandleList_egress \
        -mode                                     create                 \
        -port_handle                              $port_1                \
        -rsvp_behavior                            rsvpEgress             \
        -egress_ip_addr                           5.5.5.1                \
        -egress_ip_step                           0.0.1.0                \
        -egress_leaf_ip_count                     10                     \
        -egress_leaf_range_count                  10                     \
        -egress_leaf_range_step                   0.0.1.0                \
        -p2mp_id                                  1                      \
        -tail_traffic_start_ip                    224.0.0.20             \
    ]
if {[keylget rsvp_tunnel_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tunnel_config_status log]"
}

set rsvpTunnelHandleList [keylget rsvp_tunnel_config_status tunnel_handle]
set rsvp_egress_handle_1 $rsvpTunnelHandleList

################################################################################
# Traffic configuration
################################################################################
puts "Raw traffic configure"

set traffic_status [::ixia::traffic_config         \
        -mode                        create        \
        -traffic_generator           ixnetwork     \
        -bidirectional               1             \
        -emulation_dst_handle        $port_1       \
        -emulation_src_handle        $port_0       \
        -circuit_endpoint_type       ethernet_vlan \
        -circuit_type                raw           \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Start - RSVP emulation - Egress
################################################################################
puts "\nStart - RSVP emulation - Egress - 0"
set rsvp_control_status [::ixia::emulation_rsvp_control\
        -mode           start                    \
        -handle         $rsvp_egress_handle_0    \
        ]

if {[keylget rsvp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_control_status log]"
}

puts "\nStart - RSVP emulation - Egress - 1"
set rsvp_control_status [::ixia::emulation_rsvp_control\
        -mode           start                    \
        -handle         $rsvp_egress_handle_1    \
        ]

if {[keylget rsvp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_control_status log]"
}

################################################################################
# Start - RSVP emulation - Ingress
################################################################################
puts "\nStart - RSVP emulation - Ingress - 0"
set rsvp_control_status [::ixia::emulation_rsvp_control\
        -mode           start                    \
        -handle         $rsvp_ingress_handle_0   \
        ]

if {[keylget rsvp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_control_status log]"
}

puts "\nStart - RSVP emulation - Ingress - 1"
set rsvp_control_status [::ixia::emulation_rsvp_control\
        -mode           start                    \
        -handle         $rsvp_ingress_handle_1   \
        ]

if {[keylget rsvp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_control_status log]"
}

# exit 1

################################################################################
# RSVP Tunnel info - Ingress - received_info
################################################################################
puts "\nRSVP Tunnel info - Ingress - received_info - port_0"

after 10000

set retry_count 10
for {set retry 0} {$retry < $retry_count} {incr retry} {
    
    set rsvp_tun_info_status [::ixia::emulation_rsvp_tunnel_info                        \
            -handle $rsvp_ingress_handle_0                                              \
            -info_type received_info                                                    \
        ]
    if {[keylget rsvp_tun_info_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rsvp_tun_info_status log]"
    }
    
    set leaf_count_up [llength [keylget rsvp_tun_info_status leaf_ip.$rsvp_ingress_handle_0]]
    
    puts "retry $retry ; Port - $port_0 ; Ingress - Leaf count up $leaf_count_up"
    if {$leaf_count_up >= 100} {
        break
    }
    after 10000
}

puts "Port - $port_0 - Ingress - received_info"
foreach stat [keylkeys rsvp_tun_info_status] {
    if {$stat == "status"} {
        continue
    }
    puts [format {%-10s%-40s%s} "" $stat [keylget rsvp_tun_info_status $stat]]
}

if {[llength [keylget rsvp_tun_info_status leaf_ip.$rsvp_ingress_handle_0]] < 100} {
    return "FAIL - $test_name - RSVP P2MP leaf count failure port $port_0, handle \
            $rsvp_ingress_handle_0, info_type received_info . Expected: 100; \
            Actual: [llength [keylget rsvp_tun_info_status leaf_ip.$rsvp_ingress_handle_0]]."
}
################################################################################
# RSVP Tunnel info - Egress - assigned_info
################################################################################
# after 10000
puts "\nRSVP Tunnel info - Egress - assigned_info - port_0"
set rsvp_tun_info_status [::ixia::emulation_rsvp_tunnel_info                       \
        -handle $rsvp_egress_handle_0                                              \
        -info_type assigned_info                                                   \
    ]
if {[keylget rsvp_tun_info_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tun_info_status log]"
}

puts "Port - $port_0 - Egress - assigned_info"
foreach stat [keylkeys rsvp_tun_info_status] {
    if {$stat == "status"} {
        continue
    }
    puts [format {%-10s%-40s%s} "" $stat [keylget rsvp_tun_info_status $stat]]
}

if {[llength [keylget rsvp_tun_info_status leaf_ip.$rsvp_egress_handle_0]] != 100} {
    return "FAIL - $test_name - RSVP P2MP leaf count failure port $port_0, handle \
            $rsvp_egress_handle_0, info_type assigned_info . Expected: 100; \
            Actual: [llength [keylget rsvp_tun_info_status leaf_ip.$rsvp_egress_handle_0]]."
}

################################################################################
# RSVP Tunnel info - Ingress - received_info
################################################################################
# after 10000
puts "\nRSVP Tunnel info - Ingress - received_info - port_1"
set rsvp_tun_info_status [::ixia::emulation_rsvp_tunnel_info                        \
        -handle $rsvp_ingress_handle_1                                              \
        -info_type received_info                                                    \
    ]
if {[keylget rsvp_tun_info_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tun_info_status log]"
}

puts "Port - $port_1 - Ingress - received_info"
foreach stat [keylkeys rsvp_tun_info_status] {
    if {$stat == "status"} {
        continue
    }
    puts [format {%-10s%-40s%s} "" $stat [keylget rsvp_tun_info_status $stat]]
}

if {[llength [keylget rsvp_tun_info_status leaf_ip.$rsvp_ingress_handle_1]] != 100} {
    return "FAIL - $test_name - RSVP P2MP leaf count failure port $port_1, handle \
            $rsvp_ingress_handle_1, info_type received_info . Expected: 100; \
            Actual: [llength [keylget rsvp_tun_info_status leaf_ip.$rsvp_ingress_handle_1]]."
}

################################################################################
# RSVP Tunnel info - Egress - assigned_info
################################################################################
# after 10000
puts "\nRSVP Tunnel info - Egress - assigned_info - port_1"
set rsvp_tun_info_status [::ixia::emulation_rsvp_tunnel_info                       \
        -handle $rsvp_egress_handle_1                                              \
        -info_type assigned_info                                                   \
    ]
if {[keylget rsvp_tun_info_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tun_info_status log]"
}

puts "Port - $port_1 - Egress - assigned_info"
foreach stat [keylkeys rsvp_tun_info_status] {
    if {$stat == "status"} {
        continue
    }
    puts [format {%-10s%-40s%s} "" $stat [keylget rsvp_tun_info_status $stat]]
}

if {[llength [keylget rsvp_tun_info_status leaf_ip.$rsvp_egress_handle_1]] != 100} {
    return "FAIL - $test_name - RSVP P2MP leaf count failure port $port_1, handle \
            $rsvp_egress_handle_1, info_type assigned_info . Expected: 100; \
            Actual: [llength [keylget rsvp_tun_info_status leaf_ip.$rsvp_egress_handle_1]]."
}

################################################################################
# Start the traffic                                                            #
################################################################################
puts "\nStart RAW Traffic"
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

puts "\nStop RAW Traffic"
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
# Wait for the traffic to stop 
################################################################################
after 20000

################################################################################
# Gather and display traffic statistics                                        #
################################################################################
puts "\nTraffic Aggregated Statistics:"
set aggregated_traffic_status [::ixia::traffic_stats                        \
        -mode                   aggregate                                   \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget aggregated_traffic_status status] != $SUCCESS} {
    return "FAIL - $test_name - [keylget aggregated_traffic_status log]"
}

set pkt_tx_p0 [keylget aggregated_traffic_status $port_0.aggregate.tx.pkt_count]
set pkt_rx_p0 [keylget aggregated_traffic_status $port_0.aggregate.rx.pkt_count]
set pkt_tx_p1 [keylget aggregated_traffic_status $port_1.aggregate.tx.pkt_count]
set pkt_rx_p1 [keylget aggregated_traffic_status $port_1.aggregate.rx.pkt_count]

puts [format "%-16s%-16s%-16s" ""   $port_0 $port_1]
puts [format "%-16s%-16s%-16s" "TX" $pkt_tx_p0 $pkt_tx_p1]
puts [format "%-16s%-16s%-16s" "RX" $pkt_rx_p0 $pkt_rx_p1]

if {[abs [mpexpr $pkt_tx_p0 -  $pkt_rx_p1]] > [mpexpr $pkt_tx_p0 / 10]} {
    return "FAIL - $test_name - Frame loss detected on port $port_1"
}

if {[abs [mpexpr $pkt_tx_p1 -  $pkt_rx_p0]] > [mpexpr $pkt_tx_p1 / 10]} {
    return "FAIL - $test_name - Frame loss detected on port $port_0"
}


################################################################################
# Stop - RSVP emulation - Ingress
################################################################################
puts "\nStop - RSVP emulation - Ingress"
set rsvp_control_status [::ixia::emulation_rsvp_control\
        -mode           stop                           \
        -handle         $rsvp_ingress_handle_0         \
        ]

if {[keylget rsvp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_control_status log]"
}

set rsvp_control_status [::ixia::emulation_rsvp_control\
        -mode           stop                           \
        -handle         $rsvp_ingress_handle_1         \
        ]

if {[keylget rsvp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_control_status log]"
}


################################################################################
# Stop - RSVP emulation - Egress
################################################################################
puts "\nStop - RSVP emulation - Egress"
set rsvp_control_status [::ixia::emulation_rsvp_control\
        -mode           stop                    \
        -handle         $rsvp_egress_handle_0      \
        ]

if {[keylget rsvp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_control_status log]"
}

set rsvp_control_status [::ixia::emulation_rsvp_control\
        -mode           stop                    \
        -handle         $rsvp_egress_handle_1      \
        ]

if {[keylget rsvp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_control_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
