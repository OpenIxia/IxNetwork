################################################################################
# Version 1.0    $Revision: 1 $
# $Author: L.Raicea $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    18/8-2005 L.Raicea
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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample creates the following L2VPN configuration on two pairs of     #
#    ports (1/1,1/2) and (1/3,1/4):                                            #
#  ____                                                                        #
# | CE |_____                                                        ____      #
# +____+     \                                                   ___| CE |     #
#             \                                                 /   +____+     #
#  ____        \  __________        ______            _____    /     ____      #
# | CE |---------| DUT (PE) |------|  P   |__________| PE  |__/_____| CE |     #
# +____+       / +__________+      +______+          +_____+  \     +____+     #
#             /                                                \     ____      #
#  ____      /                                                  \___| CE |     #
# | CE |____/                                                       +____+     #
# +____+                                                                       #
#                                                                              #
#                                                                              #
#    In this figure we have:                                                   #
#        CE - customer edge                                                    #
#        PE - provider edge                                                    #
#        P  - provider                                                         #
#    The following DUT(Cisco 6509) configuration was used:                     #
#                                                                              #
#        ip multicast-routing                                                  #
#        mpls label protocol ldp                                               #
#        mpls traffic-eng tunnels                                              #
#        tag-switching tdp router-id Loopback100 force                         #
#                                                                              #
#        interface Loopback100                                                 #
#            ip address 100.0.0.1 255.255.255.255                              #
#                                                                              #
#        router ospf 41                                                        #
#            log-adjacency-changes                                             #
#            network 170.1.1.0 0.0.0.255 area 0                                #
#        router ospf 42                                                        #
#            log-adjacency-changes                                             #
#            network 170.1.2.0 0.0.0.255 area 0                                #
#                                                                              #
#    Interface connected to TX port1(1/1):                                     #
#        interface GigabitEthernet4/30                                         #
#            no ip address                                                     #
#        interface GigabitEthernet4/30.41                                      #
#            encapsulation dot1Q 41                                            #
#            mpls l2transport route 41.41.41.41 41                             #
#        interface GigabitEthernet4/30.42                                      #
#            encapsulation dot1Q 42                                            #
#            mpls l2transport route 41.41.41.41 42                             #
#        interface GigabitEthernet4/30.43                                      #
#            encapsulation dot1Q 43                                            #
#            mpls l2transport route 41.41.41.41 43                             #
#                                                                              #
#    Interface connected to RX port1(1/2):                                     #
#        interface GigabitEthernet4/32                                         #
#            ip address 170.1.1.1 255.255.255.0                                #
#            ip ospf network broadcast                                         #
#            mpls label protocol ldp                                           #
#            tag-switching ip                                                  #
#                                                                              #
#    Interface connected to TX port2(1/3):                                     #
#        interface GigabitEthernet4/40                                         #
#            no ip address                                                     #
#        interface GigabitEthernet4/40.44                                      #
#            encapsulation dot1Q 44                                            #
#            mpls l2transport route 41.41.41.42 44                             #
#        interface GigabitEthernet4/40.45                                      #
#            encapsulation dot1Q 45                                            #
#            mpls l2transport route 41.41.41.42 45                             #
#        interface GigabitEthernet4/40.46                                      #
#            encapsulation dot1Q 46                                            #
#            mpls l2transport route 41.41.41.42 46                             #
#                                                                              #
#    Interface connected to RX port2(1/4):                                     #
#        interface GigabitEthernet4/46                                         #
#            ip address 170.1.2.1 255.255.255.0                                #
#            ip ospf network broadcast                                         #
#            mpls label protocol ldp                                           #
#            tag-switching ip                                                  #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM100TXS8 module.                              #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester

# Set transmit and receive ports
set port_tx_list [list 1/1 1/3]
set port_rx_list [list 1/2 1/4]

# Set mac addresses for the interfaces on the RX ports
set rx_mac_init_list     [list 0000.0000.0001    0000.0000.0002   ]

# Set CE parameters (used to configure the stream)
set ce_tx_mac_init_list  [list ea.00.00.00.00.00 fa.00.00.00.00.00]
set ce_tx_mac_step_list  [list 00.00.00.00.00.01 00.00.00.00.00.01]
set ce_tx_mac_count_list [list 3                 3                ]
set ce_tx_ip_init_list   [list 196.16.1.100      198.18.1.100]
set ce_tx_ip_step_list   [list 0.0.0.1           0.0.0.1     ]
set ce_tx_ip_count_list  [list 3                 3           ]

set ce_rx_mac_init_list  [list eb.00.00.00.00.00 fb.00.00.00.00.00]
set ce_rx_mac_step_list  [list 00.00.00.00.00.01 00.00.00.00.00.01]
set ce_rx_mac_count_list [list 3                 3                ]
set ce_rx_ip_init_list   [list 197.17.1.100      199.19.1.100]
set ce_rx_ip_step_list   [list 0.0.0.1           0.0.0.1     ]
set ce_rx_ip_count_list  [list 3                 3           ]

# Set DUT parameters (used to configure OSPF and LDP routers)
set dut_ldp_intf         100.0.0.1
set dut_intf_list        [list 170.1.1.1         170.1.2.1   ]

# Set Provider parameters (used to configure OSPF and LDP routers)
set provider_ip_list     [list 170.1.1.100       170.1.2.100 ]
set provider_prefix_list [list 24                24          ]

# Set PE parameters (used to configure OSPF and LDP routers)
set pe_ip_list           [list 41.41.41.41       41.41.41.42 ]
set pe_prefix_list       [list 32                32          ]
set pe_vcid_init_list    [list 41                44          ]
set pe_vcid_step_list    [list 1                 1           ]
set pe_vcid_count_list   [list 3                 3           ]

# Set stream signature in order to provide data integrity check and
# packet group signature for latency stats
set stream_tx_signature_list        [list 11223344  55667788   ]
set stream_tx_signature_offset_list [list 48          48       ]

set stream_tx_pgid_value_list       [list 10          20       ]
set stream_tx_pgid_offset_list      [list 52          52       ]

# Connect to the chassis,reset to factory defaults and
# take ownership of tx ports
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_tx_list    \
        -username  ixiaApiUser      ]

if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_tx_handle [list]
foreach port $port_tx_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
            temp_port]} {
        lappend port_tx_handle $temp_port
    }
}

# Connect to the chassis,reset to factory defaults and
# take ownership of rx ports
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_rx_list    \
        -username  ixiaApiUser      ]

if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_rx_handle [list]
foreach port $port_rx_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
                temp_port]} {
        lappend port_rx_handle $temp_port
    }
}

set ospf_router_list ""
set index -1
foreach {port_tx} $port_tx_handle {port_rx} $port_rx_handle {
    incr index
    ########################################
    # Configure TX interface in the test   #
    ########################################
    set interface_status [::ixia::interface_config        \
            -port_handle     $port_tx                     \
            -autonegotiation 1                            \
            -duplex          full                         \
            -speed           ether100                     \
            -transmit_mode   stream                       \
            -qos_stats       0                            \
            -port_rx_mode    capture                      \
            ]
    if {[keylget interface_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget interface_status log]"
    }
    
    ########################################
    # Configure RX interface in the test   #
    ########################################
    # When the stream is received on RX port, it is mpls encapsulated
    # So if the data signature offset on transmition is $offset then
    # 14 bytes for the mac header and 4 bytes for the mpls label must
    # be added on receive port.
    set interface_status [::ixia::interface_config      \
            -port_handle                $port_rx        \
            -autonegotiation            1               \
            -duplex                     full            \
            -speed                      ether100        \
            -port_rx_mode               packet_group    \
            -data_integrity             1               \
            -integrity_signature                                         \
            [lindex $stream_tx_signature_list $index]                    \
            -integrity_signature_offset                                  \
            [expr [lindex $stream_tx_signature_offset_list $index] + 18] \
            -signature                                                   \
            [lindex $stream_tx_signature_list $index]                    \
            -signature_offset                                            \
            [expr [lindex $stream_tx_signature_offset_list $index] + 18] \
            -pgid_offset                                                 \
            [expr [lindex $stream_tx_pgid_offset_list      $index] + 18] \
            -transmit_mode              stream                           ]
    
    if {[keylget interface_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget interface_status log]"
    }
    
    #################################################
    #  Configure OSPFv2 Provider and Provider Edge  #
    #                                               #
    #################################################
    set ospf_neighbor_status [::ixia::emulation_ospf_config \
            -port_handle                $port_rx          \
            -reset                                        \
            -session_type               ospfv2            \
            -mode                       create            \
            -count                      1                 \
            -mac_address_init           [lindex $rx_mac_init_list     $index] \
            -intf_ip_addr               [lindex $provider_ip_list     $index] \
            -intf_prefix_length         [lindex $provider_prefix_list $index] \
            -neighbor_intf_ip_addr      [lindex $dut_intf_list        $index] \
            -loopback_ip_addr           [lindex $pe_ip_list           $index] \
            -router_id                  [string map {/ "."} $port_rx].1       \
            -area_id                    0.0.0.0           \
            -area_id_step               0.0.0.0           \
            -area_type                  external-capable  \
            -authentication_mode        null              \
            -dead_interval              40                \
            -hello_interval             10                \
            -interface_cost             10                \
            -network_type               broadcast         \
            -option_bits                "0x02"            ]
    
    if {[keylget ospf_neighbor_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget ospf_neighbor_status log]"
    }
    
    lappend ospf_router_list [keylget ospf_neighbor_status handle]
    
    #################################################
    #  Configure LDP Provider Router                #
    #################################################
    set ldp_routers_status [::ixia::emulation_ldp_config          \
            -reset                                              \
            -mode                           create              \
            -port_handle                    $port_rx            \
            -count                          1                   \
            -intf_ip_addr           [lindex $provider_ip_list     $index] \
            -intf_prefix_length     [lindex $provider_prefix_list $index] \
            -gateway_ip_addr        [lindex $dut_intf_list        $index] \
            -mac_address_init       [lindex $rx_mac_init_list     $index] \
            -lsr_id                 [string map {/ "."} $port_rx].1       \
            -label_space                    0                   \
            -label_adv                      unsolicited         \
            -peer_discovery                 link                \
            -hello_interval                 5                   \
            -hello_hold_time                15                  \
            -keepalive_interval             10                  \
            -keepalive_holdtime             30                  \
            -discard_self_adv_fecs          0                   \
            -enable_l2vpn_vc_fecs           0                   \
            -enable_explicit_include_ip_fec 0                   \
            -enable_remote_connect          1                   \
            -enable_vc_group_matching       0                   \
            -targeted_hello_hold_time       45                  \
            -targeted_hello_interval        15                  ]
    
    if {[keylget ldp_routers_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget ldp_routers_status log]"
    }
    
    set router_handle_list [keylget ldp_routers_status handle]
    set router_handle [lindex $router_handle_list 0]
    
    #################################################
    #  Configure ipv4_prefix fec type routes        #
    #################################################
    set ldp_routers_status [::ixia::emulation_ldp_route_config \
            -mode                   create              \
            -handle                 $router_handle      \
            -fec_type               ipv4_prefix         \
            -label_msg_type         mapping             \
            -egress_label_mode      nextlabel           \
            -num_lsps               1                   \
            -fec_ip_prefix_start    [lindex $pe_ip_list     $index] \
            -fec_ip_prefix_length   [lindex $pe_prefix_list $index] \
            -packing_enable         0                   \
            -label_value_start      3                   \
            ]
    
    #################################################
    #  Configure LDP Provider Edge Router           #
    #################################################
    set ldp_routers_status [::ixia::emulation_ldp_config          \
            -mode                           create              \
            -port_handle                    $port_rx            \
            -count                          1                   \
            -intf_ip_addr           [lindex $provider_ip_list     $index] \
            -intf_prefix_length     [lindex $provider_prefix_list $index] \
            -gateway_ip_addr        [lindex $dut_intf_list        $index] \
            -loopback_ip_addr       [lindex $pe_ip_list           $index] \
            -mac_address_init       [lindex $rx_mac_init_list     $index] \
            -lsr_id                 [lindex $pe_ip_list           $index] \
            -remote_ip_addr                 $dut_ldp_intf       \
            -label_space                    0                   \
            -peer_discovery                 targeted_martini    \
            -hello_interval                 5                   \
            -hello_hold_time                15                  \
            -keepalive_interval             10                  \
            -keepalive_holdtime             30                  \
            -discard_self_adv_fecs          0                   \
            -enable_l2vpn_vc_fecs           1                   \
            -enable_explicit_include_ip_fec 0                   \
            -enable_remote_connect          1                   \
            -enable_vc_group_matching       0                   \
            -targeted_hello_hold_time       45                  \
            -targeted_hello_interval        15                  ]
    
    if {[keylget ldp_routers_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget ldp_routers_status log]"
    }
    
    set router_handle_list [keylget ldp_routers_status handle]
    set router_handle [lindex $router_handle_list 0]
    #################################################
    #  Configure vc ranges for LDP                  #
    #################################################
    set ldp_routers_status [::ixia::emulation_ldp_route_config \
            -mode                      create                \
            -handle                    $router_handle        \
            -fec_type                  vc                    \
            -fec_vc_type               eth_vlan              \
            -fec_vc_group_id           1                     \
            -fec_vc_group_count        1                     \
            -fec_vc_cbit               0                     \
            -fec_vc_id_start           [lindex $pe_vcid_init_list  $index] \
            -fec_vc_id_step            [lindex $pe_vcid_step_list  $index] \
            -fec_vc_id_count           [lindex $pe_vcid_count_list $index] \
            -fec_vc_intf_mtu_enable    1                     \
            -fec_vc_intf_mtu           1500                  \
            -fec_vc_intf_desc          "ixia_ldp_vc"         \
            -packing_enable            0                     \
            -fec_vc_label_mode         increment_label       \
            -fec_vc_label_value_start  16                    \
            -fec_vc_peer_address       $dut_ldp_intf         \
            ]
    
    if {[keylget ldp_routers_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget ldp_routers_status log]"
    }
    
    # Delete all the streams first
    set traffic_status [::ixia::traffic_config \
            -mode        reset               \
            -port_handle $port_tx            ]
    if {[keylget traffic_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget traffic_status log]"
    }
    
    set traffic_status [::ixia::traffic_config                   \
            -mode                       create                 \
            -port_handle                $port_tx               \
            -length_mode                imix                   \
            -l3_imix1_size              128                    \
            -l3_imix1_ratio             1                      \
            -l3_imix2_size              256                    \
            -l3_imix2_ratio             1                      \
            -l3_imix3_size              512                    \
            -l3_imix3_ratio             1                      \
            -l3_imix4_size              1024                   \
            -l3_imix4_ratio             1                      \
            -rate_percent               100                    \
            -mac_src                    [lindex $ce_tx_mac_init_list  $index] \
            -mac_src_mode               increment              \
            -mac_src_step               [lindex $ce_tx_mac_step_list  $index] \
            -mac_src_count              [lindex $ce_tx_mac_count_list $index] \
            -mac_dst                    [lindex $ce_rx_mac_init_list  $index] \
            -mac_dst_mode               increment              \
            -mac_dst_step               [lindex $ce_rx_mac_step_list  $index] \
            -mac_dst_count              [lindex $ce_rx_mac_count_list $index] \
            -l3_protocol                ipv4                   \
            -ip_src_addr                [lindex $ce_tx_ip_init_list   $index] \
            -ip_src_mode                increment              \
            -ip_src_count               [lindex $ce_tx_ip_count_list  $index] \
            -ip_src_step                [lindex $ce_tx_ip_step_list   $index] \
            -ip_dst_addr                [lindex $ce_rx_ip_init_list   $index] \
            -ip_dst_mode                increment              \
            -ip_dst_count               [lindex $ce_rx_ip_count_list  $index] \
            -ip_dst_step                [lindex $ce_rx_ip_step_list   $index] \
            -vlan_id_mode               increment              \
            -vlan_id                    [lindex $pe_vcid_init_list    $index] \
            -vlan_id_step               [lindex $pe_vcid_step_list    $index] \
            -vlan_id_count              [lindex $pe_vcid_count_list   $index] \
            -enable_data_integrity      1                      \
            -integrity_signature                               \
            [lindex $stream_tx_signature_list        $index]   \
            -integrity_signature_offset                        \
            [lindex $stream_tx_signature_offset_list $index]   \
            -signature                                         \
            [lindex $stream_tx_signature_list        $index]   \
            -signature_offset                                  \
            [lindex $stream_tx_signature_offset_list $index]   \
            -pgid_value                                        \
            [lindex $stream_tx_pgid_value_list       $index]   \
            ]
    
    if {[keylget traffic_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget traffic_status log]"
    }
}

# Start OSPF protocol
foreach {ospf_router} $ospf_router_list {
    set ospf_control_status [::ixia::emulation_ospf_control \
            -handle                $ospf_router           \
            -mode                  start                  ]
    
    if {[keylget ospf_control_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget ospf_control_status log]"
    }
}

# Start LDP protocol 
set ldp_control_status  [::ixia::emulation_ldp_control  \
        -port_handle                $port_rx_handle   \
        -mode                       start             ]

if {[keylget ldp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_control_status log]"
}

# Wait 100 seconds for the OSPF and LDP to learn routes and labels
after 100000

set port_handle [concat $port_tx_handle $port_rx_handle]

# Clear all statistics on ports
set traffic_status [::ixia::traffic_control \
        -action      clear_stats          \
        -port_handle $port_handle         ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

# Start traffic on TX ports
set traffic_status [::ixia::traffic_control \
        -action      run                  \
        -port_handle $port_tx_handle      ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
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

# Wait for TX ports to send traffic
after 10000

# Stop traffic on the TX ports
set traffic_stop_status [::ixia::traffic_control \
        -port_handle $port_tx_handle           \
        -action      stop                      ]
if {[keylget traffic_stop_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_stop_status log]"
}

###############################################################################
#   Retrieve stats after stopped
###############################################################################
# Get aggregrate stats for all ports
set aggregate_stats [::ixia::traffic_stats -port_handle $port_handle]
if {[keylget aggregate_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggregate_stats log]"
}

puts "\n********************* FINAL COUNT STATS ***********************"

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


post_stats $port_handle "Elapsed Time"   $aggregate_stats \
        aggregate.tx.elapsed_time

post_stats $port_handle "Packets Tx"     $aggregate_stats \
        aggregate.tx.pkt_count

post_stats $port_handle "Bytes Tx"       $aggregate_stats \
        aggregate.tx.pkt_byte_count

post_stats $port_handle "Bits Tx"        $aggregate_stats \
        aggregate.tx.pkt_bit_count

post_stats $port_handle "Packets Rx"     $aggregate_stats \
        aggregate.rx.pkt_count

post_stats $port_handle "Collisions"     $aggregate_stats \
        aggregate.rx.collisions_count

post_stats $port_handle "Dribble Errors" $aggregate_stats \
        aggregate.rx.dribble_errors_count

post_stats $port_handle "CRCs"           $aggregate_stats \
        aggregate.rx.crc_errors_count

post_stats $port_handle "Oversizes"      $aggregate_stats \
        aggregate.rx.oversize_count

post_stats $port_handle "Undersizes"     $aggregate_stats \
        aggregate.rx.undersize_count

post_stats $port_handle "Data Integrity Frames" $aggregate_stats \
        aggregate.rx.data_int_frames_count

post_stats $port_handle "Data Integrity Error"  $aggregate_stats \
        aggregate.rx.data_int_errors_count

puts "***************************************************************\n"

############################################
# Get traffic statistics for all the PGIDs #
############################################

puts "\n********** LATENCY STATS (latency is in nanosecondes) *********"
puts  [format "%8s  %8s  %15s  %15s  %8s  %8s  %8s" \
        Port PGID PkCount BitRate MaxLat MinLat AvgLat]

set index -1
foreach {port_rx} $port_rx_handle {
    incr index
    set pgid_index [lindex $stream_tx_pgid_value_list $index]
    set pgid_statistics_list [::ixia::traffic_stats     \
            -port_handle     $port_rx                 \
            -packet_group_id $pgid_index              \
            ]
    
    #############################
    #   Format the statistics   #
    #############################
    puts  [format "%8s  %8d  %15.1f  %15.1f  %8.1f  %8.1f  %8d" \
            $port_rx $pgid_index                      \
            [keylget pgid_statistics_list             \
            $port_rx.pgid.rx.pkt_count.$pgid_index]   \
            [keylget pgid_statistics_list             \
            $port_rx.pgid.rx.bit_rate.$pgid_index]    \
            [keylget pgid_statistics_list             \
            $port_rx.pgid.rx.max_latency.$pgid_index] \
            [keylget pgid_statistics_list             \
            $port_rx.pgid.rx.min_latency.$pgid_index] \
            [keylget pgid_statistics_list             \
            $port_rx.pgid.rx.avg_latency.$pgid_index] ]

}

# Clean up the connection
set cleanup_status [::ixia::cleanup_session \
        -port_handle $port_handle         ]
if {[keylget cleanup_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget cleanup_status log]"
}


return "SUCCESS - $test_name - [clock format [clock seconds]]"

