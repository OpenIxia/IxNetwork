################################################################################
# Version 1.0    $Revision: 1 $
# $Author: L.Raicea $
#
#    Copyright © 1997 - 2006 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    09/29/2006 L.Raicea
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
#    ports (4/1,4/2) and (4/3,4/4):                                            #
#                                                                              #
# (Port 4/3)                                                                   #
#  ____                                                                        #
# | CE1|_____                                                        ____      #
# +____+     \                                                   ___| CE |     #
#             \                     (Port 4/1)                  /   +____+     #
#  ____        \  __________        ______            _____    /     ____      #
# | CE2|---------| DUT (PE) |------|  P   |__________| PE  |__/_____| CE |     #
# +____+       / +__________+   |  +______+   |      +_____+  \     +____+     #
#             /  |              |             |                \     ____      #
#  ____      /   |              |             |                 \___| CE |     #
# | CE3|____/    |              |             |                     +____+     #
# +____+         |              |             |                                #
#                |              |             |                                #
#                |              |             |                      ____      #
#                |              |             |                  ___| CE |     #
#                |              |             |                 /   +____+     #
#                |              |             |       _____    /     ____      #
#                |              |             |______| PE  |__/_____| CE |     #
#                |              |             |      +_____+  \     +____+     #
#                |              |             |                \     ____      #
#                |              |             |                 \___| CE |     #
#                |              |             |                     +____+     #
#                |              |             |                                #
#                |              |             |                      ____      #
#                |              |             |                  ___| CE |     #
#                |              |             |                 /   +____+     #
#                |              |             |       _____    /     ____      #
#                |              |             |______| PE  |__/_____| CE |     #
#                |              |                    +_____+  \     +____+     #
#                |              |                              \     ____      #
#                |              |                               \___| CE |     #
#                |              |                                   +____+     #
# (Port 4/4)     |              |                                              #
#  ____          |              |                                              #
# | CE4|_____    |              |                                    ____      #
# +____+     \   |              |                                ___| CE |     #
#             \  |              |   (Port 4/2)                  /   +____+     #
#  ____        \ |              |   ______            _____    /     ____      #
# | CE5|---------|              ---|  P   |__________| PE  |__/_____| CE |     #
# +____+       /                   +______+   |      +_____+  \     +____+     #
#             /                               |                \     ____      #
#  ____      /                                |                 \___| CE |     #
# | CE6|____/                                 |                     +____+     #
# +____+                                      |                                #
#                                             |                                #
#                                             |                      ____      #
#                                             |                  ___| CE |     #
#                                             |                 /   +____+     #
#                                             |       _____    /     ____      #
#                                             |______| PE  |__/_____| CE |     #
#                                             |      +_____+  \     +____+     #
#                                             |                \     ____      #
#                                             |                 \___| CE |     #
#                                             |                     +____+     #
#                                             |                                #
#                                             |                      ____      #
#                                             |                  ___| CE |     #
#                                             |                 /   +____+     #
#                                             |       _____    /     ____      #
#                                             |______| PE  |__/_____| CE |     #
#                                                    +_____+  \     +____+     #
#                                                              \     ____      #
#                                                               \___| CE |     #
#                                                                   +____+     #
#                                                                              #
#    CE - customer edge                                                        #
#    PE - provider edge                                                        #
#    P  - provider                                                             #
#    Provider Side IGP                - OSPF                                   #
#    Provider Side MPLS Protocol      - LDP                                    #
#    DUT: Cisco 6509                                                           #
#    IOS: s72033-ipservicesk9-mz.122-18.SXF.bin                                #
#                                                                              #
# DUT configuration:                                                           #
# 
#    ip multicast-routing
#    mpls label protocol ldp
#    mpls traffic-eng tunnels
#    tag-switching tdp router-id Loopback100 force
#    
#    interface Loopback100
#    ip address 100.0.0.1 255.255.255.255
#    
#    router ospf 1
#    log-adjacency-changes
#    network 170.1.1.0 0.0.0.255 area 0
#    network 170.1.2.0 0.0.0.255 area 0
#    
#    interface GigabitEthernet9/41
#    no ip address
#    no shutdown
#    
#    interface GigabitEthernet9/41.41
#    description ToCE1
#    encapsulation dot1Q 41
#    mpls l2transport route 41.41.41.41 41
#    
#    interface GigabitEthernet9/41.42
#    description ToCE2
#    encapsulation dot1Q 42
#    mpls l2transport route 41.41.41.42 42
#    
#    interface GigabitEthernet9/41.43
#    description ToCE3
#    encapsulation dot1Q 43
#    mpls l2transport route 41.41.41.43 43
#    
#    interface GigabitEthernet9/42
#    no ip address
#    no shutdown
#    
#    interface GigabitEthernet9/42.51
#    description ToCE4
#    encapsulation dot1Q 51
#    mpls l2transport route 51.51.51.51 51
#    
#    interface GigabitEthernet9/42.52
#    description ToCE5
#    encapsulation dot1Q 52
#    mpls l2transport route 51.51.51.52 52
#    
#    interface GigabitEthernet9/42.53
#    description ToCE6
#    encapsulation dot1Q 53
#    mpls l2transport route 51.51.51.53 53
#    
#    interface GigabitEthernet9/39
#    description ToProvider1
#    ip address 170.1.1.1 255.255.255.0
#    ip ospf network broadcast
#    mpls label protocol ldp
#    tag-switching ip
#    no shutdown
#    
#    interface GigabitEthernet9/40
#    description ToProvider2
#    ip address 170.1.2.1 255.255.255.0
#    ip ospf network broadcast
#    mpls label protocol ldp
#    tag-switching ip
#    no shutdown
#
# Erase DUT config:
#
#    no ip multicast-routing
#    no mpls label protocol ldp
#    no mpls traffic-eng tunnels
#    no tag-switching tdp router-id Loopback100 force
#    
#    no interface Loopback100
#    
#    no router ospf 1
#
#    default interface GigabitEthernet9/41
#    no interface GigabitEthernet9/41.41
#    no interface GigabitEthernet9/41.42
#    no interface GigabitEthernet9/41.43
#
#    default interface GigabitEthernet9/42
#    no interface GigabitEthernet9/42.51
#    no interface GigabitEthernet9/42.52
#    no interface GigabitEthernet9/42.53
#
#    default interface GigabitEthernet9/39
#    default interface GigabitEthernet9/40
#                                                                                 #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#                                                                              #
################################################################################

proc script_increment_ipv4_address {prefix intf_ip_addr_step} {
    
    set temp_route_ip_addr_step [split $intf_ip_addr_step .]
    set step_index 3
    set octet_number 4
    while {$octet_number >= 1} {
        set single_octet_step [lindex $temp_route_ip_addr_step\
                $step_index]
        set one   0
        if {[scan $prefix "%d.%d.%d.%d" a b c d] == 4} {
            set one   [format %u [expr ($a<<24)|($b<<16)|($c<<8)|$d]]
        }
        set two [expr {$single_octet_step<<(8*(4-$octet_number))}]
        set value [expr {$one + $two}]
        if [catch {set prefix [format "%s.%s.%s.%s" \
                    [expr {(($value >> 24) & 0xff)}] \
                    [expr {(($value >> 16) & 0xff)}] \
                    [expr {(($value >> 8 ) & 0xff)}] \
                    [expr {$value & 0xff}]]} prefix] {
            set prefix 0.0.0.0
        }
        
        incr octet_number -1
        incr step_index -1
    }
    return $prefix
}

proc script_increment_mac_address { macAdd amount } {
    # Replace all colons, periods, and spaces with null.
    regsub -all {\.} $macAdd "" tempMac
    regsub -all {:} $tempMac "" tempMac
    regsub -all { } $tempMac "" tempMac
    set macAdd "0x$tempMac"
    
    regsub -all {\.} $amount "" tempMac
    regsub -all {:} $tempMac "" tempMac
    regsub -all { } $tempMac "" tempMac
    set amount "0x$tempMac"
    
    set result [mpexpr $macAdd + $amount]
    for {set i 0} {$i < 6} {incr i} {
        set b$i [format "%02X" [mpexpr $result & 0xFF]]
        set result [mpexpr $result >> 8]
    }
    return "$b5.$b4.$b3.$b2.$b1.$b0"
}

package require Ixia

set test_name [info script]

set chassisIP sylvester

# Set transmit and receive ports
set port_pe_list [list 4/1 4/2]
set port_ce_list [list 4/3 4/4]

# Set Provider parameters (used to configure OSPF and LDP routers)
set p_count              2
set p_ip_addr_start      170.1.1.100
set p_ip_addr_step       0.0.1.0
set p_gw_addr_start      170.1.1.1
set p_gw_addr_step       0.0.1.0
set p_ip_prefix_len      24
set dut_ip_addr          100.0.0.1

# Set PE parameters (used to configure OSPF and LDP routers)
set pe_count              3
set pe_ip_addr_start      41.41.41.41
set pe_ip_addr_step1      0.0.0.1
set pe_ip_addr_step2      10.10.10.10
set pe_ip_prefix_len      32
set pe_intf_addr_start    11.11.11.11
set pe_intf_addr_step1    0.0.0.1
set pe_intf_addr_step2    10.10.10.10
set pe_intf_prefix_len    24
set pe_intf_mask          255.255.255.0
set pe_ospf_type          route

# Set CE parameters (used to configure the stream)
set ce_tx_count          3
set ce_tx_mac_start      ea.00.00.00.00.00
set ce_tx_mac_step1      00.00.00.00.00.01
set ce_tx_mac_step2      10.00.00.00.00.00
set ce_tx_ip_addr_start  196.16.1.100
set ce_tx_ip_addr_step1  0.0.0.1
set ce_tx_ip_addr_step2  2.2.0.0

set ce_rx_count          3
set ce_rx_mac_start      eb.00.00.00.00.00
set ce_rx_mac_step1      00.00.00.00.00.01
set ce_rx_mac_step2      10.00.00.00.00.00
set ce_rx_ip_addr_start  197.17.1.100
set ce_rx_ip_addr_step1  0.0.0.1
set ce_rx_ip_addr_step2  2.2.0.0

set vcid_count            3
set vcid_start            41
set vcid_step1            1
set vcid_step2            10

set vlan_count            3
set vlan_start            41
set vlan_step1            1
set vlan_step2            10

# Set stream signature in order to provide data integrity check and
# packet group signature for latency stats
set stream_tx_sgn_start       0x11223344
set stream_tx_sgn_step        0x44444444
set stream_tx_sgn_offset      48

set stream_tx_pgid_start            10
set stream_tx_pgid_step1            1
set stream_tx_pgid_step2            10
set stream_tx_pgid_offset           52

# Connect to the chassis, reset to factory defaults and take ownership
# of CE ports
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_ce_list    \
        -username  ixiaApiUser      ]

if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_ce_handle [list]
foreach port $port_ce_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
            temp_port]} {
        lappend port_ce_handle $temp_port
    }
}

# Connect to the chassis, reset to factory defaults and take ownership
# of PE ports
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_pe_list    \
        -username  ixiaApiUser      ]

if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_pe_handle [list ]
foreach port $port_pe_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
                temp_port]} {
        lappend port_pe_handle $temp_port
    }
}

set ospf_router_list   ""
set ldp_router_list    ""
set index -1
set p_ip_addr_temp     $p_ip_addr_start
set p_gw_addr_temp     $p_gw_addr_start
set stream_tx_sgn_temp $stream_tx_sgn_start
foreach {port_ce} $port_ce_handle {port_pe} $port_pe_handle {
    set pe_ip_addr_start_p        $pe_ip_addr_start
    set pe_intf_addr_start_p      $pe_intf_addr_start
    set vcid_start_p              $vcid_start
    set vlan_start_p              $vlan_start
    set ce_tx_mac_start_p         $ce_tx_mac_start
    set ce_rx_mac_start_p         $ce_rx_mac_start
    set ce_tx_ip_addr_start_p     $ce_tx_ip_addr_start
    set ce_rx_ip_addr_start_p     $ce_rx_ip_addr_start
    set stream_tx_pgid_p          $stream_tx_pgid_start
    
    # Incrementing variable when passing to the next port/provider
    for {set i -1} {$i < $index} {incr i} {
        set pe_ip_addr_start_p    [script_increment_ipv4_address \
                $pe_ip_addr_start_p    $pe_ip_addr_step2]
        
        set pe_intf_addr_start_p  [script_increment_ipv4_address \
                $pe_intf_addr_start_p  $pe_intf_addr_step2]
        
        incr vcid_start_p         $vcid_step2
        incr vlan_start_p         $vlan_step2
        
        set ce_tx_mac_start_p     [script_increment_mac_address  \
                $ce_tx_mac_start_p     $ce_tx_mac_step2]
        
        set ce_rx_mac_start_p     [script_increment_mac_address  \
                $ce_rx_mac_start_p     $ce_rx_mac_step2]
        
        set ce_tx_ip_addr_start_p [script_increment_ipv4_address \
                $ce_tx_ip_addr_start_p $ce_tx_ip_addr_step2]
        
        set ce_rx_ip_addr_start_p [script_increment_ipv4_address \
                $ce_rx_ip_addr_start_p $ce_rx_ip_addr_step2]
        
        incr stream_tx_pgid_p $stream_tx_pgid_step2
    }
    
    incr index
    # Configure CE interface in the test
    set interface_status [::ixia::interface_config        \
            -port_handle     $port_ce                     \
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
    
    # Configure PE interface in the test
    # When the stream is received on PE port, it is mpls encapsulated
    # So if the data signature offset on transmition is $offset then
    # 14 bytes for the mac header and 4 bytes for the mpls label must
    # be added on receive port.
    set interface_status [::ixia::interface_config                         \
            -port_handle                $port_pe                           \
            -autonegotiation            1                                  \
            -duplex                     full                               \
            -speed                      ether100                           \
            -port_rx_mode               packet_group                       \
            -data_integrity             1                                  \
            -integrity_signature        $stream_tx_sgn_temp                \
            -integrity_signature_offset $stream_tx_sgn_offset              \
            -signature                  $stream_tx_sgn_temp                \
            -signature_offset           [expr $stream_tx_sgn_offset  + 18] \
            -pgid_offset                [expr $stream_tx_pgid_offset + 18] \
            -transmit_mode              stream                             ]
    
    if {[keylget interface_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget interface_status log]"
    }
    
    # Configure OSPFv2 Provider Router
    set ospf_neighbor_status [::ixia::emulation_ospf_config \
            -reset                                        \
            -port_handle                $port_pe          \
            -session_type               ospfv2            \
            -mode                       create            \
            -count                      1                 \
            -intf_ip_addr               $p_ip_addr_temp   \
            -intf_prefix_length         $p_ip_prefix_len  \
            -neighbor_intf_ip_addr      $p_gw_addr_temp   \
            -router_id                  $p_ip_addr_temp   \
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
    
    set     ospf_router_provider [keylget ospf_neighbor_status handle]
    lappend ospf_router_list     [keylget ospf_neighbor_status handle]
    
    # Configure LDP Provider Router
    set ldp_routers_status [::ixia::emulation_ldp_config          \
            -reset                                              \
            -mode                           create              \
            -port_handle                    $port_pe            \
            -count                          1                   \
            -intf_ip_addr                   $p_ip_addr_temp     \
            -intf_prefix_length             $p_ip_prefix_len    \
            -gateway_ip_addr                $p_gw_addr_temp     \
            -lsr_id                         $p_ip_addr_temp     \
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
    
    set     ldp_router_provider [keylget ldp_routers_status handle]
    lappend ldp_router_list     [keylget ldp_routers_status handle]
    
    set pe_ip_addr_temp   $pe_ip_addr_start_p
    set pe_intf_addr_temp $pe_intf_addr_start_p
    for {set i 0} {$i < $pe_count} {incr i} {
        # Configure OSPFv2 PE
        if {$pe_ospf_type == "route"} {
            # As route
            set route_config_status [::ixia::emulation_ospf_topology_route_config\
                    -mode                     create                  \
                    -handle                   $ospf_router_provider   \
                    -type                     summary_routes          \
                    -summary_number_of_prefix 1                       \
                    -summary_prefix_start     $pe_ip_addr_temp        \
                    -summary_prefix_length    $pe_ip_prefix_len       \
                    ]
                    
            if {[keylget route_config_status status] != $::SUCCESS} {
                return "FAIL - $test_name - [keylget route_config_status log]"
            }
        } elseif {$pe_ospf_type == "grid"} {
            # As grid
            set route_config_status [::ixia::emulation_ospf_topology_route_config\
                    -mode                   create                   \
                    -handle                 $ospf_router_provider    \
                    -type                   grid                     \
                    -grid_router_id         $pe_ip_addr_temp         \
                    -grid_router_id_step    $pe_ip_addr_step1        \
                    -grid_row               1                        \
                    -grid_col               1                        \
                    -grid_link_type         ptop_numbered            \
                    -grid_prefix_start      $pe_ip_addr_temp         \
                    -grid_prefix_length     $pe_ip_prefix_len        \
                    -grid_prefix_step       $pe_ip_addr_step1        \
                    -grid_te                0                        \
                    -grid_connect           1 1                      \
                    -interface_ip_address   $pe_intf_addr_temp       \
                    -interface_ip_mask      $pe_intf_mask            \
                    -enable_advertise       1                        \
                    ]
            
            if {[keylget route_config_status status] != $::SUCCESS} {
                return "FAIL - $test_name - [keylget route_config_status log]"
            }
        }
        
        # Configure ipv4_prefix fec type routes
        set ldp_routers_status [::ixia::emulation_ldp_route_config \
                -mode                   create                   \
                -handle                 $ldp_router_provider     \
                -fec_type               ipv4_prefix              \
                -label_msg_type         mapping                  \
                -egress_label_mode      nextlabel                \
                -num_lsps               1                        \
                -fec_ip_prefix_start    $pe_ip_addr_temp         \
                -fec_ip_prefix_length   $pe_ip_prefix_len        \
                -packing_enable         0                        \
                -label_value_start      3                        \
                ]
        
        # Configure LDP PE Routers
        set ldp_routers_status [::ixia::emulation_ldp_config          \
                -mode                           create              \
                -port_handle                    $port_pe            \
                -count                          1                   \
                -intf_ip_addr                   $p_ip_addr_temp     \
                -intf_prefix_length             $p_ip_prefix_len    \
                -gateway_ip_addr                $p_gw_addr_temp     \
                -loopback_ip_addr               $pe_ip_addr_temp    \
                -lsr_id                         $pe_ip_addr_temp    \
                -remote_ip_addr                 $dut_ip_addr        \
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
        
        set     ldp_router_pe   [keylget ldp_routers_status handle]
        lappend ldp_router_list [keylget ldp_routers_status handle]
        
        # Configure vc ranges for LDP
        set ldp_routers_status [::ixia::emulation_ldp_route_config \
                -mode                      create                \
                -handle                    $ldp_router_pe        \
                -fec_type                  vc                    \
                -fec_vc_type               eth_vlan              \
                -fec_vc_group_id           1                     \
                -fec_vc_group_count        1                     \
                -fec_vc_cbit               0                     \
                -fec_vc_id_start           $vcid_start_p         \
                -fec_vc_id_step            $vcid_step1           \
                -fec_vc_id_count           $vcid_count           \
                -fec_vc_intf_mtu_enable    1                     \
                -fec_vc_intf_mtu           1500                  \
                -fec_vc_intf_desc          "ixia_ldp_vc"         \
                -packing_enable            0                     \
                -fec_vc_label_mode         increment_label       \
                -fec_vc_label_value_start  16                    \
                -fec_vc_peer_address       $dut_ip_addr          \
                ]
        
        if {[keylget ldp_routers_status status] != $::SUCCESS} {
            return "FAIL - $test_name - [keylget ldp_routers_status log]"
        }
        
        set pe_ip_addr_temp      [script_increment_ipv4_address \
                $pe_ip_addr_temp      $pe_ip_addr_step1]
        
        set pe_intf_ip_address_temp [script_increment_ipv4_address \
                $pe_intf_addr_temp    $pe_intf_addr_step1 ]
    }
    
    # Delete all the streams first
    set traffic_status [::ixia::traffic_config \
            -mode        reset               \
            -port_handle $port_ce            ]
    if {[keylget traffic_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget traffic_status log]"
    }
    
    set rate_percent        [expr 100 / ($pe_count * $p_count)]
    set vlan_temp           $vlan_start_p
    set stream_tx_pgid_temp $stream_tx_pgid_p
    for {set i 0} {$i < $pe_count} {incr i} {
        set traffic_configuration "ixia::traffic_config                \
                -mode                       create                     \
                -port_handle                $port_ce                   \
                -length_mode                fixed                      \
                -frame_size                 1024                       \
                -rate_percent               $rate_percent              \
                -mac_src                    $ce_tx_mac_start_p         \
                -mac_src_mode               increment                  \
                -mac_src_step               $ce_tx_mac_step1           \
                -mac_src_count              $ce_tx_count               \
                -mac_dst                    $ce_rx_mac_start_p         \
                -mac_dst_mode               increment                  \
                -mac_dst_step               $ce_rx_mac_step1           \
                -mac_dst_count              $ce_rx_count               \
                -l3_protocol                ipv4                       \
                -ip_src_addr                $ce_tx_ip_addr_start_p     \
                -ip_src_mode                increment                  \
                -ip_src_count               $ce_tx_count               \
                -ip_src_step                $ce_tx_ip_addr_step1       \
                -ip_dst_addr                $ce_rx_ip_addr_start_p     \
                -ip_dst_mode                increment                  \
                -ip_dst_count               $ce_rx_count               \
                -ip_dst_step                $ce_rx_ip_addr_step1       \
                -vlan_id                    $vlan_temp                 \
                -vlan_id_mode               fixed                      \
                -enable_data_integrity      1                          \
                -integrity_signature        $stream_tx_sgn_temp        \
                -integrity_signature_offset $stream_tx_sgn_offset      \
                -signature                  $stream_tx_sgn_temp        \
                -signature_offset           $stream_tx_sgn_offset      \
                -pgid_value                 $stream_tx_pgid_temp       "
        
        if {$i == $pe_count} {
            lappend traffic_configuration           \
                    "-transmit_mode" "return_to_id" \
                    "-return_to_id"  1
        }
        
        set traffic_status [eval $traffic_configuration]
        if {[keylget traffic_status status] != $::SUCCESS} {
            return "FAIL - $test_name - [keylget traffic_status log]"
        }
        set vlan_temp           [incr vlan_temp           $vlan_step1]
        set stream_tx_pgid_temp [incr stream_tx_pgid_temp $stream_tx_pgid_step1]
    }
    
    set p_ip_addr_temp [script_increment_ipv4_address \
            $p_ip_addr_temp      $p_ip_addr_step]
    
    set p_gw_addr_temp [script_increment_ipv4_address \
            $p_gw_addr_temp      $p_gw_addr_step]
    
    set stream_tx_sgn_temp [incr stream_tx_sgn_temp $stream_tx_sgn_step]
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
        -port_handle                $port_pe_handle   \
        -mode                       start             ]

if {[keylget ldp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_control_status log]"
}

# Wait 100 seconds for the OSPF and LDP to learn routes and labels
after 100000

set port_handle [concat $port_ce_handle $port_pe_handle]

# Clear all statistics on ports
set traffic_status [::ixia::traffic_control \
        -action      clear_stats          \
        -port_handle $port_handle         ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

# Start traffic on CE ports
set traffic_status [::ixia::traffic_control \
        -action      run                  \
        -port_handle $port_ce_handle      ]
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

# Wait for CE ports to send traffic
after 10000

# Stop traffic on the CE ports
set traffic_stop_status [::ixia::traffic_control \
        -port_handle $port_ce_handle           \
        -action      stop                      ]
if {[keylget traffic_stop_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_stop_status log]"
}

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

# Get PGID stats for all PE ports
puts "\n********** LATENCY STATS (latency is in nanosecondes) *********"
puts  [format "%8s  %8s  %15s  %15s  %8s  %8s  %8s" \
        Port PGID PkCount BitRate MaxLat MinLat AvgLat]

set index -1
set pgid_index $stream_tx_pgid_start
foreach {port_pe} $port_pe_handle {
    incr index
    for {set i 0} {$i < $pe_count} {incr i} {
        set pgid_statistics_list [::ixia::traffic_stats     \
                -port_handle     $port_pe                 \
                -packet_group_id $pgid_index              \
                ]
        
        puts  [format "%8s  %8d  %15.1f  %15.1f  %8.1f  %8.1f  %8d" \
                $port_pe $pgid_index                      \
                [keylget pgid_statistics_list             \
                $port_pe.pgid.rx.pkt_count.$pgid_index]   \
                [keylget pgid_statistics_list             \
                $port_pe.pgid.rx.bit_rate.$pgid_index]    \
                [keylget pgid_statistics_list             \
                $port_pe.pgid.rx.max_latency.$pgid_index] \
                [keylget pgid_statistics_list             \
                $port_pe.pgid.rx.min_latency.$pgid_index] \
                [keylget pgid_statistics_list             \
                $port_pe.pgid.rx.avg_latency.$pgid_index] ]
        
        incr pgid_index $stream_tx_pgid_step1
    }
    set pgid_index [expr $stream_tx_pgid_start + \
            $stream_tx_pgid_step2 * ($index + 1)]
}

# Clean up the connection
set cleanup_status [::ixia::cleanup_session \
        -port_handle $port_handle         ]
if {[keylget cleanup_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget cleanup_status log]"
}


return "SUCCESS - $test_name - [clock format [clock seconds]]"

