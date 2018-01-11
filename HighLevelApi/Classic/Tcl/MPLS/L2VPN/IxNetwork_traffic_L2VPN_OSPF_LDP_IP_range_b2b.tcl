################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    03-11-2008 LRaicea - created sample
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
#    This sample creates the following L2VPN configuration:                    #
#  ____                                                                        #
# | CE |_____                                                 ____             #
# +____+     \                                            ___| CE |            #
#             \                                          /   +____+            #
#  ____        \  _____      ____     ____     _____    /     ____             #
# | CE |---------| PE  |----|  P |___| P  |___| PE  |__/_____| CE |            #
# +____+       / +_____+    +____+   +____+   +_____+  \     +____+            #
#             /                                         \     ____             #
#  ____      /                                           \___| CE |            #
# | CE |____/                                                +____+            #
# +____+                                                                       #
#                                                                              #
#                                                                              #
#    In this figure we have:                                                   #
#        CE - customer edge                                                    #
#        PE - provider edge                                                    #
#        P  - provider                                                         #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#                                                                              #
################################################################################
package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 2/1 2/2]

################################################################################
# Connect to the chassis, reset to factory defaults
################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                           \
        -reset                                                                \
        -ixnetwork_tcl_server   localhost                                     \
        -device                 $chassisIP                                    \
        -port_list              $port_list                                    \
        -username               ixiaApiUser                                   \
        -break_locks            1                                             \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
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

################################################################################
# Variables initialization
################################################################################
set p_ip_addr_list             [list 20.20.20.1 20.20.20.2]
set p_gw_addr_list             [list 20.20.20.2 20.20.20.1]
set p_prefix_len_list          [list 24         24]
set pe_ip_addr_list            [list 1.1.1.1    2.2.2.2]
set pe_gw_addr_list            [list 2.2.2.2    1.1.1.1]
set pe_prefix_len_list         [list 32         32]
set p_label_list               [list 111        122]
set pe_label_list              [list 211        222]
set fec_vc_id_start            311
set vc_range_per_pe_list       [list 3          3]
set ip_range_count_list        [list 5          5]
set ip_range_addr_list         [list 11.11.11.1 22.22.22.1]
################################################################################
# Set L1 configuration
################################################################################
set interface_status [::ixia::interface_config                                \
        -port_handle     [list $port_0 $port_1]                               \
        -autonegotiation [list 1       1      ]                               \
        -duplex          [list auto    auto   ]                               \
        -speed           [list auto    auto   ]                               \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}
################################################################################
# OSPF configuration
################################################################################
set index 0
set p_ospf_router_list [list]
foreach port [list $port_0 $port_1] {
    set ospf_neighbor_status [::ixia::emulation_ospf_config                    \
            -port_handle                $port                                  \
            -reset                                                             \
            -session_type               ospfv2                                 \
            -mode                       create                                 \
            -count                      1                                      \
            -intf_ip_addr               [lindex $p_ip_addr_list     $index]    \
            -intf_prefix_length         [lindex $p_prefix_len_list  $index]    \
            -neighbor_intf_ip_addr      [lindex $p_gw_addr_list     $index]    \
            -loopback_ip_addr           [lindex $pe_ip_addr_list    $index]    \
            -router_id                  [lindex $p_ip_addr_list     $index]    \
            -area_id                    0.0.0.0                                \
            -area_id_step               0.0.0.0                                \
            -area_type                  external-capable                       \
            -authentication_mode        null                                   \
            -network_type               ptop                                   \
            -lsa_discard_mode           0                                      \
            ]
    if {[keylget ospf_neighbor_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ospf_neighbor_status log]"
        return
    }
    lappend p_ospf_router_list [keylget ospf_neighbor_status handle]
    incr index
}
################################################################################
# LDP configuration
################################################################################
set index 0
set p_ldp_router_list [list]
foreach port [list $port_0 $port_1] {
    # Provider
    set ldp_router_status [::ixia::emulation_ldp_config                        \
            -reset                                                             \
            -mode                           create                             \
            -port_handle                    $port                              \
            -count                          1                                  \
            -intf_ip_addr                   [lindex $p_ip_addr_list    $index] \
            -intf_prefix_length             [lindex $p_prefix_len_list $index] \
            -gateway_ip_addr                [lindex $p_gw_addr_list    $index] \
            -lsr_id                         [lindex $p_ip_addr_list    $index] \
            -label_space                    0                                  \
            -label_adv                      unsolicited                        \
            -peer_discovery                 link                               \
            -hello_interval                 5                                  \
            -hello_hold_time                15                                 \
            -keepalive_interval             10                                 \
            -keepalive_holdtime             30                                 \
            -discard_self_adv_fecs          0                                  \
            -enable_l2vpn_vc_fecs           1                                  \
            -enable_explicit_include_ip_fec 0                                  \
            -enable_remote_connect          1                                  \
            -enable_vc_group_matching       0                                  \
            -targeted_hello_hold_time       45                                 \
            -targeted_hello_interval        15                                 \
            ]
    
    if {[keylget ldp_router_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ldp_router_status log]"
        return
    }
    set p_ldp_router          [keylget ldp_router_status handle]
    lappend p_ldp_router_list [keylget ldp_router_status handle]
    
    # Provider advertised FECs
    set ldp_route_status [::ixia::emulation_ldp_route_config                   \
            -mode                   create                                     \
            -handle                 $p_ldp_router                              \
            -fec_type               ipv4_prefix                                \
            -label_msg_type         mapping                                    \
            -egress_label_mode      nextlabel                                  \
            -num_lsps               1                                          \
            -fec_ip_prefix_start    [lindex $pe_ip_addr_list     $index]       \
            -fec_ip_prefix_length   [lindex $pe_prefix_len_list  $index]       \
            -packing_enable         0                                          \
            -label_value_start      [lindex $p_label_list        $index]       \
            -provisioning_model     manual_configuration                       \
            ]
    if {[keylget ldp_route_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ldp_routers_status log]"
        return
    }
    # PE
    set ldp_routers_status [::ixia::emulation_ldp_config                       \
            -mode                           create                             \
            -port_handle                    $port                              \
            -count                          1                                  \
            -intf_ip_addr                   [lindex $p_ip_addr_list    $index] \
            -intf_prefix_length             [lindex $p_prefix_len_list $index] \
            -gateway_ip_addr                [lindex $p_gw_addr_list    $index] \
            -loopback_ip_addr               [lindex $pe_ip_addr_list   $index] \
            -lsr_id                         [lindex $pe_ip_addr_list   $index] \
            -remote_ip_addr                 [lindex $pe_gw_addr_list   $index] \
            -label_space                    0                                  \
            -peer_discovery                 targeted_martini                   \
            -hello_interval                 5                                  \
            -hello_hold_time                15                                 \
            -keepalive_interval             10                                 \
            -keepalive_holdtime             30                                 \
            -discard_self_adv_fecs          0                                  \
            -enable_l2vpn_vc_fecs           1                                  \
            -enable_explicit_include_ip_fec 0                                  \
            -enable_remote_connect          1                                  \
            -enable_vc_group_matching       0                                  \
            -targeted_hello_hold_time       45                                 \
            -targeted_hello_interval        15                                 \
            ]
    if {[keylget ldp_routers_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ldp_routers_status log]"
        return
    }
    set pe_ldp_router [keylget ldp_routers_status handle]
    lappend pe_ldp_router_list [keylget ldp_routers_status handle]
    
    
    # PE L2 VC
    set ldp_route_status [::ixia::emulation_ldp_route_config                   \
            -mode                         create                               \
            -handle                       $pe_ldp_router                       \
            -fec_type                     vc                                   \
            -fec_vc_type                  eth_vpls                             \
            -fec_vc_count                 [lindex $vc_range_per_pe_list $index]\
            -fec_vc_group_id              1                                    \
            -fec_vc_group_count           1                                    \
            -fec_vc_cbit                  0                                    \
            -fec_vc_id_start              $fec_vc_id_start                     \
            -fec_vc_id_step               1                                    \
            -fec_vc_id_count              1                                    \
            -fec_vc_intf_mtu_enable       1                                    \
            -fec_vc_intf_mtu              1500                                 \
            -fec_vc_intf_desc             "ixia_ldp_vc"                        \
            -packing_enable               0                                    \
            -fec_vc_label_mode            increment_label                      \
            -fec_vc_label_value_start     [lindex $pe_label_list     $index]   \
            -fec_vc_label_value_step      1                                    \
            -fec_vc_peer_address          [lindex $pe_gw_addr_list   $index]   \
            -fec_vc_ce_ip_addr            [lindex $pe_ip_addr_list   $index]   \
            -fec_vc_ip_range_enable       1                                    \
            -fec_vc_ip_range_addr_count   [lindex $ip_range_count_list $index] \
            -fec_vc_ip_range_addr_start   [lindex $ip_range_addr_list  $index] \
            -fec_vc_ip_range_addr_inner_step   0.0.0.1                         \
            -fec_vc_ip_range_addr_outer_step   0.0.1.0                         \
            -fec_vc_ip_range_prefix_len        24                              \
            -provisioning_model            manual_configuration                \
            ]
    if {[keylget ldp_route_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ldp_route_status log]"
        return
    }
    set lsp_vc_range_handles_$port [keylget ldp_route_status lsp_vc_range_handles]
    incr index
}
################################################################################
# Configure traffic
################################################################################
set traffic_status [::ixia::traffic_control                                    \
        -action             reset                                              \
        -traffic_generator  ixnetwork                                          \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}
set traffic_status [::ixia::traffic_config                                     \
        -mode                   create                                         \
        -traffic_generator      ixnetwork                                      \
        -transmit_mode          continuous                                     \
        -name                   "VC_Range_Traffic"                             \
        -src_dest_mesh          one_to_one                                     \
        -route_mesh             one_to_one                                     \
        -circuit_type           l2vpn                                          \
        -circuit_endpoint_type  ethernet_vlan                                  \
        -emulation_src_handle   [set lsp_vc_range_handles_${port_0}]           \
        -emulation_dst_handle   [set lsp_vc_range_handles_${port_1}]           \
        -track_by               mpls_label                                     \
        -stream_packing         one_stream_per_endpoint_pair                   \
        -rate_percent           2                                              \
        -length_mode            fixed                                          \
        -frame_size             512                                            \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}
################################################################################
# Start protocols
################################################################################
set ospf_control_status [::ixia::emulation_ospf_control                        \
        -port_handle           [list $port_0 $port_1]                          \
        -mode                  start                                           \
        ]
if {[keylget ospf_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospf_control_status log]"
    return
}
set ldp_control_status  [::ixia::emulation_ldp_control                         \
        -port_handle           [list $port_0 $port_1]                          \
        -mode                  start                                           \
        ]
if {[keylget ldp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_control_status log]"
}

# Wait 60 seconds for the OSPF and LDP to learn routes and labels
after 60000

################################################################################
# Start traffic
################################################################################
set traffic_status [::ixia::traffic_control                                    \
        -action             run                                                \
        -port_handle        $port_0                                            \
        -traffic_generator  ixnetwork       ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}
after 10000
################################################################################
# Stop traffic
################################################################################
set traffic_status [::ixia::traffic_control                                    \
        -action             stop                                               \
        -port_handle        $port_0                                            \
        -traffic_generator  ixnetwork                                          \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

# Procedure to print stats
proc post_stats {port_handle label key_list stat_key {stream ""}} {
    puts -nonewline [format "%-30s" $label]
    
    foreach port $port_handle {
        if {$stream != ""} {
            set key $port.stream.$stream.$stat_key
        } else {
            set key $port.$stat_key
        }
        
        if {[llength [keylget key_list $key]] > 1} {
            puts -nonewline "[format "%-16s" N/A]"
        } else  {
            puts -nonewline "[format "%-16s" [keylget key_list $key]]"
        }
    }
    puts ""
}
################################################################################
# Retrieve stats 
################################################################################
set aggregate_stats [::ixia::traffic_stats                                     \
        -port_handle       $port_handle                                        \
        -traffic_generator ixnetwork                                           \
        -mode              aggregate                                           \
        ]
if {[keylget aggregate_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget aggregate_stats log]"
    return
}

puts -nonewline "[format "%-30s" " "]"
foreach port $port_handle {
    puts -nonewline "[format "%-16s" $port]"
}
puts ""
puts -nonewline "[format "%-30s" " "]"
foreach port $port_handle {
    puts -nonewline "[format "%-16s" "-----"]"
}
puts ""

post_stats $port_handle "Packets Tx"     $aggregate_stats \
        aggregate.tx.pkt_count

post_stats $port_handle "Packets Rx"     $aggregate_stats \
        aggregate.rx.pkt_count

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return

