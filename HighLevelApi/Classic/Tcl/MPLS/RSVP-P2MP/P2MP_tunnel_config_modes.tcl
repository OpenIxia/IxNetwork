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
#    This sample uses all modes accepted by -mode argument for                 #
#    ::ixia::emulation_rsvp_tunnel_config procedure.                           #
#        -create 2 RSVP Ingres tunnels                                         #
#        -modify tunnels                                                       #
#        -delete first RSVP tunnel                                             #
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
set port_list               [list 2/3]

# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                        \
        -reset                                                             \
        -device               $chassis_ip                                  \
        -port_list            $port_list                                   \
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

################################################################################
# Create RSVP router
################################################################################
puts "\nCreate RSVP router"

set rsvp_config_status [::ixia::emulation_rsvp_config                \
        -mode                            create                      \
        -count                           1                           \
        -intf_ip_addr                    1.1.1.1                     \
        -intf_prefix_length              24                          \
        -ip_version                      4                           \
        -mac_address_init                1101.2233.0001              \
        -neighbor_intf_ip_addr           111.111.111.1               \
        -port_handle                     $port_0                     \
        -reset                                                       \
    ]

if {[keylget rsvp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_config_status log]"
}

set rsvp_handle [keylget rsvp_config_status handles]

################################################################################
# START - RSVP Tunnel configuration Ingress
################################################################################
puts "\nRSVP Tunnel configuration Ingress..."

set ero_list_as_num                         {33 44}
set ero_list_ipv4                           {33.0.0.1 44.0.0.1}
set ero_list_loose                          {1  0}
set ero_list_pfxlen                         {1  1}
set rro_list_ctype                          [list 1 2 3 4]
set rro_list_flags                          [list 2 4 16 32]
set rro_list_ipv4                           [list 5.5.5.5 6.6.6.6               \
                                                  7.7.7.7 8.8.8.8]
set rro_list_label                          [list 11 22 33 44]
set avoid_node_id                           [list 1.2.3.4 5.6.7.8]
set plr_id                                  [list 1.2.3.4 5.6.7.8]
set h2l_info_dut_hop_type                   [list strict loose]
set h2l_info_dut_prefix_length              [list 24  32]
set h2l_info_enable_append_tunnel_leaf      [list 0  1]
set h2l_info_enable_prepend_dut             [list 1  1]
set h2l_info_enable_send_as_ero             [list 1  0]
set h2l_info_enable_send_as_sero            [list 0  1]
set h2l_info_ero_sero_list                  [list                             \
                            "ip,0.0.1.0/32,l:ip,0.0.1.0/32,l:ip,1.1.1.1/24,s" \
                            "as,15,l:as,16,l:as,17,s"                         ]
set h2l_info_tunnel_leaf_hop_type           [list strict    loose       ]
set h2l_info_tunnel_leaf_ip_start           [list 6.6.6.6   7.7.7.7     ]
set h2l_info_tunnel_leaf_prefix_length      [list 32        16          ]

################################################################################
# Start RSVP Tunnel Call
################################################################################
set rsvp_tunnel_config_status [::ixia::emulation_rsvp_tunnel_config \
        -count                                    2                 \
        -emulation_type                           rsvptep2mp        \
        -handle                                   $rsvp_handle      \
        -mode                                     create            \
        -port_handle                              $port_0           \
        -rsvp_behavior                            rsvpIngress       \
        -egress_ip_addr                           55.55.55.1        \
        -egress_ip_step                           0.1.0.0           \
        -egress_leaf_ip_count                     5                 \
        -egress_leaf_range_count                  3                 \
        -egress_leaf_range_step                   0.0.1.0           \
        -p2mp_id                                  1                 \
        -p2mp_id_step                             1                 \
        -ingress_ip_addr                          66.66.66.1        \
        -ingress_ip_step                          0.0.1.0           \
        -lsp_id_count                             10                \
        -lsp_id_start                             0                 \
        -lsp_id_step                              1                 \
        -tunnel_id_count                          15                \
        -tunnel_id_start                          0                 \
        -tunnel_id_step                           1                 \
        -ero                                      1                 \
        -ero_dut_pfxlen                           16                \
        -ero_list_as_num                          $ero_list_as_num  \
        -ero_list_ipv4                            $ero_list_ipv4    \
        -ero_list_loose                           $ero_list_loose   \
        -ero_list_pfxlen                          $ero_list_pfxlen  \
        -ero_list_type                            ipv4              \
        -ero_mode                                 loose             \
        -enable_append_connected_ip               1                 \
        -enable_prepend_tunnel_head_ip            1                 \
        -rro                                      1                 \
        -rro_list_ctype                           $rro_list_ctype   \
        -rro_list_flags                           $rro_list_flags   \
        -rro_list_ipv4                            $rro_list_ipv4    \
        -rro_list_label                           $rro_list_label   \
        -rro_list_type                            label             \
        -reservation_error_tlv                    22,1,aa:22,2,bb   \
        -ingress_bandwidth                        60                \
        -session_attr                             1                 \
        -session_attr_bw_protect                  1                 \
        -session_attr_flags                       50                \
        -session_attr_hold_priority               7                 \
        -session_attr_label_record                1                 \
        -session_attr_local_protect               1                 \
        -session_attr_node_protect                1                 \
        -session_attr_se_style                    1                 \
        -session_attr_setup_priority              7                 \
        -session_attr_ra_exclude_any              {11 22 33 44}     \
        -session_attr_ra_include_all              {0a bb cc dd}     \
        -session_attr_ra_include_any              1                 \
        -session_attr_resource_affinities         1                 \
        -sender_tspec_max_pkt_size                50                \
        -sender_tspec_min_policed_size            60                \
        -sender_tspec_peak_data_rate              70                \
        -sender_tspec_token_bkt_rate              80                \
        -sender_tspec_token_bkt_size              90                \
        -avoid_node_id                            $avoid_node_id    \
        -facility_backup                          1                 \
        -fast_reroute                             1                 \
        -fast_reroute_bandwidth                   80                \
        -fast_reroute_exclude_any                 1f                \
        -fast_reroute_holding_priority            5                 \
        -fast_reroute_hop_limit                   50                \
        -fast_reroute_include_all                 {0a bb cc dd}     \
        -fast_reroute_include_any                 {01 f2 e3 d4}     \
        -fast_reroute_setup_priority              2                 \
        -one_to_one_backup                        1                 \
        -plr_id                                   $plr_id           \
        -session_attr_reroute                     1                 \
        -path_tlv                                 22,1,aa:22,2,bb   \
        -path_tear_tlv                            22,1,aa:22,2,bb   \
        -h2l_info_dut_hop_type                    $h2l_info_dut_hop_type              \
        -h2l_info_dut_prefix_length               $h2l_info_dut_prefix_length         \
        -h2l_info_enable_append_tunnel_leaf       $h2l_info_enable_append_tunnel_leaf \
        -h2l_info_enable_prepend_dut              $h2l_info_enable_prepend_dut        \
        -h2l_info_enable_send_as_ero              $h2l_info_enable_send_as_ero        \
        -h2l_info_enable_send_as_sero             $h2l_info_enable_send_as_sero       \
        -h2l_info_ero_sero_list                   $h2l_info_ero_sero_list             \
        -h2l_info_tunnel_leaf_count               2                                   \
        -h2l_info_tunnel_leaf_hop_type            $h2l_info_tunnel_leaf_hop_type      \
        -h2l_info_tunnel_leaf_ip_start            $h2l_info_tunnel_leaf_ip_start      \
        -h2l_info_tunnel_leaf_prefix_length       $h2l_info_tunnel_leaf_prefix_length \
        -head_traffic_inter_tunnel_ip_step        0.0.1.0           \
        -head_traffic_ip_count                    2                 \
        -head_traffic_ip_type                     ipv4              \
        -head_traffic_start_ip                    100.100.100.100   \
        -tail_traffic_inter_tunnel_ip_step        0.1.0.1           \
        -tail_traffic_ip_count                    2                 \
        -tail_traffic_ip_type                     ipv4              \
        -tail_traffic_start_ip                    224.0.0.1         \
    ]
    
if {[keylget rsvp_tunnel_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tunnel_config_status log]"
}

set rsvpTunnelHandleList [keylget rsvp_tunnel_config_status tunnel_handle]
foreach tunnelHandle $rsvpTunnelHandleList {
    puts "\nRSVP Tunnel $tunnelHandle"
    puts "\tTunnel Leaf Handles:"
    foreach tunLeaf [keylget rsvp_tunnel_config_status tunnel_leaves_handle.$tunnelHandle] {
        puts "\t\t$tunLeaf"
    }
    puts "\tIngress Tunnel Interface Handles:"
    foreach intHandle [keylget rsvp_tunnel_config_status routed_interfaces.$tunnelHandle] {
        puts "\t\t$intHandle"
    }
}

################################################################################
# START - RSVP Tunnel configuration Ingress - modify
################################################################################
puts "\nModify RSVP Tunnels"

set h2l_info_dut_hop_type                   [list strict loose]
set h2l_info_dut_prefix_length              [list 24  32]
set h2l_info_enable_append_tunnel_leaf      [list 0  1]
set h2l_info_enable_prepend_dut             [list 1  1]
set h2l_info_enable_send_as_ero             [list 1  0]
set h2l_info_enable_send_as_sero            [list 0  1]
set h2l_info_ero_sero_list                  [list                             \
                            "ip,0.0.1.0/32,l:ip,0.0.1.0/32,l:ip,1.1.1.1/24,s" \
                            "as,15,l:as,16,l:as,17,s"                         ]
set h2l_info_tunnel_leaf_hop_type           [list strict    loose       ]
set h2l_info_tunnel_leaf_ip_start           [list 6.6.6.6   7.7.7.7     ]
set h2l_info_tunnel_leaf_prefix_length      [list 32        16          ]

set rsvp_tunnel_config_status [::ixia::emulation_rsvp_tunnel_config     \
        -mode                                     modify                \
        -ingress_ip_addr                          22.23.24.1            \
        -ingress_ip_step                          0.0.1.0               \
        -lsp_id_count                             10                    \
        -lsp_id_start                             0                     \
        -lsp_id_step                              1                     \
        -tunnel_id_count                          15                    \
        -tunnel_id_start                          77                    \
        -tunnel_id_step                           1                     \
        -tunnel_pool_handle                       $rsvpTunnelHandleList \
        -reservation_error_tlv                    22,1,aa:22,2,bb       \
        -ingress_bandwidth                        10                    \
        -session_attr                             1                     \
        -session_attr_bw_protect                  0                     \
        -session_attr_flags                       128                   \
        -session_attr_hold_priority               3                     \
        -session_attr_label_record                0                     \
        -session_attr_local_protect               0                     \
        -session_attr_name                        "modified_tunnel"     \
        -session_attr_node_protect                0                     \
        -session_attr_se_style                    1                     \
        -session_attr_setup_priority              7                     \
        -session_attr_ra_exclude_any              {00 11 22 00}         \
        -session_attr_ra_include_all              {00 aa bb 00}         \
        -session_attr_ra_include_any              0                     \
        -session_attr_resource_affinities         0                     \
        -sender_tspec_max_pkt_size                20                    \
        -sender_tspec_min_policed_size            21                    \
        -sender_tspec_peak_data_rate              22                    \
        -sender_tspec_token_bkt_rate              23                    \
        -sender_tspec_token_bkt_size              24                    \
        -facility_backup                          1                     \
        -fast_reroute                             1                     \
        -fast_reroute_bandwidth                   80                    \
        -fast_reroute_exclude_any                 1f                    \
        -fast_reroute_holding_priority            5                     \
        -fast_reroute_hop_limit                   50                    \
        -fast_reroute_include_all                 {00 00 11 22}         \
        -fast_reroute_include_any                 {00 00 aa bb}         \
        -fast_reroute_setup_priority              7                     \
        -one_to_one_backup                        0                     \
        -session_attr_reroute                     1                     \
        -path_tlv                                 12,10,bb:23,3,cc      \
        -path_tear_tlv                            12,10,bb:23,3,cc      \
        -h2l_info_dut_hop_type                    $h2l_info_dut_hop_type\
        -h2l_info_dut_prefix_length               $h2l_info_dut_prefix_length             \
        -h2l_info_enable_append_tunnel_leaf       $h2l_info_enable_append_tunnel_leaf     \
        -h2l_info_enable_prepend_dut              $h2l_info_enable_prepend_dut            \
        -h2l_info_enable_send_as_ero              $h2l_info_enable_send_as_ero            \
        -h2l_info_enable_send_as_sero             $h2l_info_enable_send_as_sero           \
        -h2l_info_ero_sero_list                   $h2l_info_ero_sero_list                 \
        -h2l_info_tunnel_leaf_count               2                                       \
        -h2l_info_tunnel_leaf_hop_type            $h2l_info_tunnel_leaf_hop_type          \
        -h2l_info_tunnel_leaf_ip_start            $h2l_info_tunnel_leaf_ip_start          \
        -h2l_info_tunnel_leaf_prefix_length       $h2l_info_tunnel_leaf_prefix_length     \
        -head_traffic_inter_tunnel_ip_step        0.0.1.0               \
        -head_traffic_ip_count                    2                     \
        -head_traffic_ip_type                     ipv4                  \
        -head_traffic_start_ip                    105.105.105.105       \
        -tail_traffic_inter_tunnel_ip_step        0.1.0.1               \
        -tail_traffic_ip_count                    2                     \
        -tail_traffic_ip_type                     ipv4                  \
        -tail_traffic_start_ip                    225.0.0.1             \
    ]
if {[keylget rsvp_tunnel_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tunnel_config_status log]"
}

################################################################################
# Delete First RSVP Tunnel
################################################################################
puts "\nDelete First RSVP Tunnel"

set rsvp_tunnel_config_status [::ixia::emulation_rsvp_tunnel_config     \
        -mode                  delete                                   \
        -tunnel_pool_handle    [lindex $rsvpTunnelHandleList 0]         \
    ]
if {[keylget rsvp_tunnel_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tunnel_config_status log]"
}


return "SUCCESS - $test_name - [clock format [clock seconds]]"
