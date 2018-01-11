################################################################################
# Version 1.0    $Revision: 1 $
#
#    Copyright © 1997 - 2006 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    09/25/2006 LRaicea
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
#    This sample creates a L3VPN setup. It uses two Ixia ports.                #
#    One port is used for PEs and P router configuration. The other port is    #
#    used for CE routers configuration.                                        #
#    Streams are generated on both ports and then started.                     #
#                                                                              #
#         ------        -----           -----          ------                  #
#        |  PEs  |-----|  P  |---------| DUT |--------|  CEs |                 #
#         ------        -----     |     -----     |    ------                  #
#                                 |               |                            #
#               Ixia port 1       |  Cisco 6500   |    Ixia port 2             #
#                                                                              #
#    PE runs mBGP                                                              #
#    P  runs LDP and OSPF                                                      #
#    CE runs OSPF                                                              #
#    DUT: Cisco 6500
#    IOS: s72033-ipservicesk9-mz.122-18.SXF.bin
# 
# DUT configuration:
#
#    conf t
#    
#    ip cef distributed
#    ip vrf vpn801
#    description vpn801
#    rd 801:1
#    route-target export 801:1
#    route-target import 801:1
#
#    ip vrf vpn802
#    description vpn802
#    rd 802:1
#    route-target export 802:1
#    route-target import 802:1
#
#    ip vrf vpn803
#    description vpn803
#    rd 803:1
#    route-target export 803:1
#    route-target import 803:1
#
#    ip vrf vpn804
#    description vpn804
#    rd 804:1
#    route-target export 804:1
#    route-target import 804:1
#
#    ip vrf vpn805
#    description vpn805
#    rd 805:1
#    route-target export 805:1
#    route-target import 805:1
#    
#    ip multicast-routing
#    mpls label protocol ldp
#    mpls traffic-eng tunnels
#    tag-switching tdp discovery directed-hello accept
#    
#    interface Loopback0
#    ip address 110.0.110.1 255.255.255.255
#    no ip directed-broadcast
#    
#    interface GigabitEthernet9/48
#    no ip address
#    no ip directed-broadcast
#    load-interval 30
#    duplex auto
#    speed auto
#    media-type rj45
#    negotiation auto
#    no shutdown
#    
#    interface GigabitEthernet9/48.1
#    description vpn801_ce
#    encapsulation dot1Q 801
#    ip vrf forwarding vpn801
#    ip address 100.21.0.1 255.255.255.0
#    no ip directed-broadcast
#    no cdp enable
#
#    interface GigabitEthernet9/48.2
#    description vpn802_ce
#    encapsulation dot1Q 802
#    ip vrf forwarding vpn802
#    ip address 100.22.0.1 255.255.255.0
#    no ip directed-broadcast
#    no cdp enable
#
#    interface GigabitEthernet9/48.3
#    description vpn803_ce
#    encapsulation dot1Q 803
#    ip vrf forwarding vpn803
#    ip address 100.23.0.1 255.255.255.0
#    no ip directed-broadcast
#    no cdp enable
#
#    interface GigabitEthernet9/48.4
#    description vpn804_ce
#    encapsulation dot1Q 804
#    ip vrf forwarding vpn804
#    ip address 100.24.0.1 255.255.255.0
#    no ip directed-broadcast
#    no cdp enable
#
#    interface GigabitEthernet9/48.5
#    description vpn805_ce
#    encapsulation dot1Q 805
#    ip vrf forwarding vpn805
#    ip address 100.25.0.1 255.255.255.0
#    no ip directed-broadcast
#    no cdp enable
#    
#    interface GigabitEthernet9/47
#    ip address 100.28.0.1 255.255.255.0
#    no ip directed-broadcast
#    ip ospf network broadcast
#    load-interval 30
#    duplex auto
#    speed auto
#    media-type rj45
#    negotiation auto
#    mpls label protocol ldp
#    tag-switching ip
#    no shutdown
#    
#    router ospf 101 vrf vpn801
#    log-adjacency-changes
#    network 100.21.0.0 0.0.0.255 area 0
#    redistribute bgp 1 subnets
#
#    router ospf 102 vrf vpn802
#    log-adjacency-changes
#    network 100.22.0.0 0.0.0.255 area 0
#    redistribute bgp 1 subnets
#
#    router ospf 103 vrf vpn803
#    log-adjacency-changes
#    network 100.23.0.0 0.0.0.255 area 0
#    redistribute bgp 1 subnets
#
#    router ospf 104 vrf vpn804
#    log-adjacency-changes
#    network 100.24.0.0 0.0.0.255 area 0
#    redistribute bgp 1 subnets
#
#    router ospf 105 vrf vpn805
#    log-adjacency-changes
#    network 100.25.0.0 0.0.0.255 area 0
#    redistribute bgp 1 subnets
#
#    router ospf 801
#    mpls traffic-eng router-id Loopback0
#    mpls traffic-eng area 0
#    log-adjacency-changes
#    network 100.28.0.0 0.0.0.255 area 0
#    
#    router bgp 1
#    no bgp default ipv4-unicast
#    bgp log-neighbor-changes
#    neighbor 110.0.110.100 remote-as 1
#    neighbor 110.0.110.100 update-source Loopback0
#    neighbor 110.0.110.101 remote-as 1
#    neighbor 110.0.110.101 update-source Loopback0
#    neighbor 110.0.110.102 remote-as 1
#    neighbor 110.0.110.102 update-source Loopback0
#    
#    address-family vpnv4
#    neighbor 110.0.110.100 activate
#    neighbor 110.0.110.100 send-community extended
#    neighbor 110.0.110.101 activate
#    neighbor 110.0.110.101 send-community extended
#    neighbor 110.0.110.102 activate
#    neighbor 110.0.110.102 send-community extended
#    exit-address-family
#    
#    address-family ipv4 vrf vpn801
#    redistribute ospf 101 match internal external 1 external 2
#    no synchronization
#    exit-address-family
#
#    address-family ipv4 vrf vpn802
#    redistribute ospf 102 match internal external 1 external 2
#    no synchronization
#    exit-address-family
#
#    address-family ipv4 vrf vpn803
#    redistribute ospf 103 match internal external 1 external 2
#    no synchronization
#    exit-address-family
#
#    address-family ipv4 vrf vpn804
#    redistribute ospf 104 match internal external 1 external 2
#    no synchronization
#    exit-address-family
#
#    address-family ipv4 vrf vpn805
#    redistribute ospf 105 match internal external 1 external 2
#    no synchronization
#    exit-address-family
#    end
#
#
# Erase DUT config:
#    
#    no ip vrf vpn801
#    no ip vrf vpn802
#    no ip vrf vpn803
#    no ip vrf vpn804
#    no ip vrf vpn805
#
#    no interface Loopback0
#    default interface GigabitEthernet9/48
#    no interface GigabitEthernet9/48.1
#    no interface GigabitEthernet9/48.2
#    no interface GigabitEthernet9/48.3
#    no interface GigabitEthernet9/48.4
#    no interface GigabitEthernet9/48.5
#
#    default interface GigabitEthernet9/47
#    no router ospf 101 vrf vpn801
#    no router ospf 102 vrf vpn802
#    no router ospf 103 vrf vpn803
#    no router ospf 104 vrf vpn804
#    no router ospf 105 vrf vpn805
#
#    no router bgp 1
#    no ip multicast-routing
#    no mpls label protocol ldp
#    no mpls traffic-eng tunnels
#
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
            set one   [format %u [expr {($a<<24)|($b<<16)|($c<<8)|$d}]]
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

proc script_increment_ipv4_net {ipAddress {netmask 24} {amount 1}} {
    set ipVal   0
    if {[scan $ipAddress "%d.%d.%d.%d" a b c d] == 4} {
        set ipVal   [format %u [expr {($a<<24)|($b<<16)|($c<<8)|$d}]]
    }
    set ipVal [mpexpr {($ipVal >> (32 - $netmask)) + $amount}]
    set ipVal [mpexpr {($ipVal << (32 - $netmask)) & 0xFFFFFFFF}]
    if [catch {set address [format "%s.%s.%s.%s" \
                [expr {(($ipVal >> 24) & 0xff)}] \
                [expr {(($ipVal >> 16) & 0xff)}] \
                [expr {(($ipVal >> 8 ) & 0xff)}] \
                [expr {$ipVal & 0xff}]]} address] {
        set address 0.0.0.0
    }
    return $address
}

package require Ixia
set test_name [info script]

set chassisIP                sylvester
set port_list                [list 4/1 4/2]

set pe_ip_address            110.0.110.100
set pe_ip_address_step       0.0.0.1
set pe_prefix_len            32
set pe_intf_ip_address       11.0.0.1
set pe_intf_ip_address_step  0.0.0.1
set pe_intf_mask             255.255.255.0
set pe_count                 3
set pe_bgp_peer_ip           110.0.110.1
set pe_bgp_peer_ip_step      0.0.0.0
set pe_bgp_router_id         1.2.3.4
set pe_bgp_router_id_step    1.2.3.4
set pe_bgp_as                1
set pe_bgp_as_step           0

set vrf_count                5
set vrf_rd_target_type       0
set vrf_rd_admin_value       801
set vrf_rd_admin_step        1
set vrf_rd_assign_value      1
set vrf_rd_assign_step       0
set vrf_target_type          "as"
set vrf_admin_value          801
set vrf_admin_step           1
set vrf_assign_value         1
set vrf_assign_step          0
set vrf_network              77.78.0.0
set vrf_network_mask         255.255.255.0
set vrf_num_routes           2
set vrf_prefix_len           16

set p_ip_address             100.28.0.2
set p_ip_address_step        0.0.0.0
set p_prefix_len             24
set p_gateway_ip             100.28.0.1
set p_gateway_ip_step        0.0.0.0
set p_ospf_router_id         1.2.3.4
set p_ospf_router_id_step    0.0.0.1
set p_ospf_area_id           0.0.0.0
set p_ospf_area_id_step      0.0.0.1
set p_lsr_id                 1.2.3.4
set p_lsr_id_step            0.0.0.1

set ce_ip_address            100.21.0.2
set ce_ip_address_step       0.1.0.0
set ce_prefix_len            24
set ce_gateway_ip            100.21.0.1
set ce_gateway_ip_step       0.1.0.0
set ce_vlan_id               801
set ce_vlan_id_step          1
set ce_ospf_router_id        5.6.7.8
set ce_ospf_router_id_step   0.0.0.1
set ce_ospf_area_id          0.0.0.0
set ce_ospf_area_id_step     0.0.0.0

set c_network1               67.67.68.0
set c_network1_step          1.0.0.0
set c_prefix_len1            24
set c_num_prefixes1          3

set c_network2               57.57.58.0
set c_network2_step          1.0.0.0
set c_prefix_len2            24
set c_num_prefixes2          2

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect \
        -reset                \
        -device    $chassisIP \
        -port_list $port_list \
        -username  ixiaApiUser]

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

set pe_port [lindex $port_handle 0]
set ce_port [lindex $port_handle 1]

################################################################################
# Initialize ports
################################################################################
set intf_status [::ixia::interface_config    \
        -port_handle     "$pe_port $ce_port" \
        -autonegotiation 1                   \
        -speed           ether1000           \
        -transmit_mode   advanced            ]
if {[keylget intf_status status] != $SUCCESS} {
    return "FAIL - $test_name - [keylget intf_status log]"
}

################################################################################
# Configure Provider OSPFv2 neighbor
################################################################################
set ospf_neighbor_status [::ixia::emulation_ospf_config      \
        -port_handle                $pe_port               \
        -reset                                             \
        -session_type               ospfv2                 \
        -mode                       create                 \
        -count                      1                      \
        -intf_ip_addr               $p_ip_address          \
        -intf_ip_addr_step          $p_ip_address_step     \
        -router_id                  $p_ospf_router_id      \
        -router_id_step             $p_ospf_router_id_step \
        -neighbor_intf_ip_addr      $p_gateway_ip          \
        -neighbor_intf_ip_addr_step $p_gateway_ip_step     \
        -area_id                    $p_ospf_area_id        \
        -area_id_step               $p_ospf_area_id_step   \
        -area_type                  external-capable       \
        -network_type               broadcast              ]

if {[keylget ospf_neighbor_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_neighbor_status log]"
}

################################################################################
# Configure OSPFv2 PEs
################################################################################
set p_ospf_handle           [keylget ospf_neighbor_status handle]
set pe_ip_address_temp      $pe_ip_address
set pe_intf_ip_address_temp $pe_intf_ip_address
for {set i 0} {$i < $pe_count} {incr i} {
    set route_config_status [::ixia::emulation_ospf_topology_route_config\
            -mode                   create                   \
            -handle                 $p_ospf_handle           \
            -type                   grid                     \
            -grid_router_id         $pe_ip_address_temp      \
            -grid_router_id_step    $pe_ip_address_step      \
            -grid_row               1                        \
            -grid_col               1                        \
            -grid_link_type         ptop_numbered            \
            -grid_prefix_start      $pe_ip_address_temp      \
            -grid_prefix_length     $pe_prefix_len           \
            -grid_prefix_step       $pe_ip_address_step      \
            -grid_te                0                        \
            -grid_connect           1 1                      \
            -interface_ip_address   $pe_intf_ip_address_temp \
            -interface_ip_mask      $pe_intf_mask            \
            -enable_advertise       1                        \
            ]
    
    if {[keylget route_config_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget route_config_status log]"
    }
    set pe_ip_address_temp      [script_increment_ipv4_address \
            $pe_ip_address_temp      $pe_ip_address_step]
    
    set pe_intf_ip_address_temp [script_increment_ipv4_address \
            $pe_intf_ip_address_temp $pe_intf_ip_address_step]
}

################################################################################
# Configure LDP Neighbor on P/PE port
################################################################################
set ldp_routers_status [::ixia::emulation_ldp_config \
        -mode                  create              \
        -reset                                     \
        -port_handle           $pe_port            \
        -label_adv             unsolicited         \
        -peer_discovery        link                \
        -count                 1                   \
        -intf_ip_addr          $p_ip_address       \
        -intf_ip_addr_step     $p_ip_address_step  \
        -intf_prefix_length    $p_prefix_len       \
        -lsr_id                $p_lsr_id           \
        -lsr_id_step           $p_lsr_id_step      \
        -label_space           0                   \
        -gateway_ip_addr       $p_gateway_ip       \
        -gateway_ip_addr_step  $p_gateway_ip_step  ]

if {[keylget ldp_routers_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_routers_status log]"
}
set ldp_handle [keylget ldp_routers_status handle]


################################################################################
# Configure ipv4_prefix fec type routes
################################################################################
set pe_ip_address_temp      $pe_ip_address
for {set i 0} {$i < $pe_count} {incr i} {
    set ldp_routers_status [::ixia::emulation_ldp_route_config \
            -mode                   create              \
            -handle                 $ldp_handle         \
            -fec_type               ipv4_prefix         \
            -label_msg_type         mapping             \
            -fec_ip_prefix_start    $pe_ip_address_temp \
            -fec_ip_prefix_length   $pe_prefix_len      \
            -egress_label_mode      imnull              ]
    
    set pe_ip_address_temp      [script_increment_ipv4_address \
            $pe_ip_address_temp      $pe_ip_address_step]
}


################################################################################
# Configure BGP Neighbor on PE port
################################################################################
set bgp_router_status [::ixia::emulation_bgp_config               \
        -mode                            reset                  \
        -port_handle                       $pe_port               \
        -count                             $pe_count              \
        -local_ip_addr                   $p_ip_address          \
        -local_addr_step                 $p_ip_address_step     \
        -remote_ip_addr                  $p_gateway_ip          \
        -remote_addr_step                $p_gateway_ip_step     \
        -local_loopback_ip_addr          $pe_ip_address         \
        -local_loopback_ip_addr_step     $pe_ip_address_step    \
        -remote_loopback_ip_addr         $pe_bgp_peer_ip        \
        -remote_loopback_ip_addr_step    $pe_bgp_peer_ip_step   \
        -local_router_id                 $pe_bgp_router_id      \
        -local_router_id_step            $pe_bgp_router_id_step \
        -neighbor_type                   internal               \
        -ip_version                      4                      \
        -local_as                        $pe_bgp_as             \
        -local_as_mode                   fixed                  \
        -active_connect_enable                                  \
        -ipv4_mpls_vpn_nlri                                     ]
        

if {[keylget bgp_router_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_router_status log]"
}
set bgp_neighbor_handles  [keylget bgp_router_status handles]


################################################################################
# Configure VRFs on the BGP Neighbor
################################################################################
set vrf_network_temp $vrf_network
foreach {bgp_neighbor_handle} $bgp_neighbor_handles {
    set bgp_route_range_status [::ixia::emulation_bgp_route_config \
            -mode                      add                       \
            -handle                    $bgp_neighbor_handle      \
            -ip_version                4                         \
            -prefix                    $vrf_network_temp         \
            -prefix_step               1                         \
            -netmask                   $vrf_network_mask         \
            -label_value               55                        \
            -label_step                1                         \
            -num_sites                 $vrf_count                \
            -num_routes                $vrf_num_routes           \
            -rd_type                   $vrf_rd_target_type       \
            -rd_admin_value            $vrf_rd_admin_value       \
            -rd_admin_step             $vrf_rd_admin_step        \
            -rd_assign_value           $vrf_rd_assign_value      \
            -rd_assign_step            $vrf_rd_assign_step       \
            -target_type               $vrf_target_type          \
            -target                    $vrf_admin_value          \
            -target_step               $vrf_admin_step           \
            -target_assign             $vrf_assign_value         \
            -target_assign_step        $vrf_assign_step          \
            -import_target_type        $vrf_target_type          \
            -import_target             $vrf_admin_value          \
            -import_target_step        $vrf_admin_step           \
            -import_target_assign      $vrf_assign_value         \
            -import_target_assign_step $vrf_assign_step          \
            -local_pref                0                         \
            -next_hop_enable           1                         \
            -origin_route_enable                                 \
            -enable_traditional_nlri   1                         \
            -ipv4_mpls_vpn_nlri                                  ]
    
    if {[keylget bgp_route_range_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget bgp_route_range_status log]"
    }
    for {set i 0} {$i < $vrf_count} {incr i} {
        set vrf_network_temp [script_increment_ipv4_net \
                $vrf_network_temp $vrf_prefix_len]
    }
}


################################################################################
# Configure OSPFv2 CE neighbors
################################################################################
set ospf_neighbor_status [::ixia::emulation_ospf_config        \
        -port_handle                $ce_port                 \
        -reset                                               \
        -session_type               ospfv2                   \
        -mode                       create                   \
        -count                      $vrf_count               \
        -intf_ip_addr               $ce_ip_address           \
        -intf_ip_addr_step          $ce_ip_address_step      \
        -router_id                  $ce_ospf_router_id       \
        -router_id_step             $ce_ospf_router_id_step  \
        -neighbor_intf_ip_addr      $ce_gateway_ip           \
        -neighbor_intf_ip_addr_step $ce_gateway_ip_step      \
        -vlan_id                    $ce_vlan_id              \
        -vlan_id_step               $ce_vlan_id_step         \
        -area_id                    $ce_ospf_area_id         \
        -area_id_step               $ce_ospf_area_id_step    \
        -area_type                  external-capable         \
        -network_type               broadcast                ]

if {[keylget ospf_neighbor_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_neighbor_status log]"
}

set ospf_ce_handles [keylget ospf_neighbor_status handle]


################################################################################
# Configure two route ranges on each OSPFv2 CE neighbor
################################################################################
set c_network1_temp $c_network1
set c_network2_temp $c_network2
foreach {ospf_ce_handle} $ospf_ce_handles {
    set ospf_route_status [::ixia::emulation_ospf_topology_route_config \
            -mode                      create                    \
            -handle                    $ospf_ce_handle           \
            -type                      summary_routes            \
            -summary_prefix_start      $c_network1_temp          \
            -summary_prefix_step       1                         \
            -summary_prefix_length     $c_prefix_len1            \
            -summary_number_of_prefix  $c_num_prefixes1          ]
    if {[keylget ospf_route_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget ospf_route_status log]"
    }
    set c_network1_temp [script_increment_ipv4_address \
            $c_network1_temp $c_network1_step]
    
    set ospf_route_status [::ixia::emulation_ospf_topology_route_config \
            -mode                      create                    \
            -handle                    $ospf_ce_handle           \
            -type                      summary_routes            \
            -summary_prefix_start      $c_network2_temp          \
            -summary_prefix_step       1                         \
            -summary_prefix_length     $c_prefix_len2            \
            -summary_number_of_prefix  $c_num_prefixes2          ]
    if {[keylget ospf_route_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget ospf_route_status log]"
    }
    set c_network2_temp [script_increment_ipv4_address \
            $c_network2_temp $c_network2_step]
}


################################################################################
# START OSPF (PE)
################################################################################
set ospf_emulation_status [::ixia::emulation_ospf_control \
        -handle $p_ospf_handle \
        -mode   start        ]

if {[keylget ospf_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_emulation_status log]"
}

################################################################################
# START LDP (PE)
################################################################################
set ldp_emulation_status [::ixia::emulation_ldp_control \
        -handle $ldp_handle \
        -mode   start       ]

if {[keylget ldp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_emulation_status log]"
}


################################################################################
# START OSPF (CE)
################################################################################
set ospf_emulation_status [::ixia::emulation_ospf_control \
        -handle $ospf_ce_handle \
        -mode   start        ]

if {[keylget ospf_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_emulation_status log]"
}

# Wait for OSPF routes and for LDP labels to be learned 
after 40000


################################################################################
# START BGP (PE)
################################################################################
set bgp_emulation_status [::ixia::emulation_bgp_control \
        -port_handle $pe_port \
        -mode        start    ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}

# Set up the bgp statistics after starting the protocol
set bgp_emulation_status [::ixia::emulation_bgp_control \
        -handle $bgp_neighbor_handle \
        -mode   statistic            ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}

after 60000

set retries 5
################################################################################
# Send ARP
################################################################################
while {$retries > 0} {
    set intf_status [::ixia::interface_config    \
            -port_handle    "$pe_port $ce_port"  \
            -arp_send_req   1                    ]
    if {[keylget intf_status status] != $SUCCESS} {
        return "FAIL - $test_name - [keylget intf_status log]"
    }
    
    if {[keylget intf_status $pe_port.arp_request_success] == $::SUCCESS && \
            [keylget intf_status $ce_port.arp_request_success] == $::SUCCESS} {
        break
    } elseif {$retries > 0} {
        after 1000
        puts "Sending ARP request ..."
        update idletasks
    }
    incr retries -1
}

if {[keylget intf_status $pe_port.arp_request_success] != $::SUCCESS} {
    return "FAIL - $test_name - ARP request failed on port $pe_port."
}

if {[keylget intf_status $ce_port.arp_request_success] != $::SUCCESS} {
    return "FAIL - $test_name - ARP request failed on port $ce_port."
}

################################################################################
# Generate traffic on PE and CE ports
################################################################################
set stream_status [::ixia::l3vpn_generate_stream \
        -reset                        \
        -pe_port_handle      $pe_port \
        -ce_port_handle      $ce_port \
        -stream_generation   both     \
        -pe_label_protocol   ldp      \
        -ce_routing_protocol ospf     \
        -length_mode         random   \
        -l3_length_min       128      \
        -l3_length_max       1024     \
        -enable_pgid         1        \
        -pgid_value          1234     \
        -rate_percent        1        ]
if {[keylget stream_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget stream_status log]"
}

################################################################################
# Clear stats before sending traffic
################################################################################
set clear_stats_status [::ixia::traffic_control \
        -port_handle "$pe_port $ce_port"      \
        -action      clear_stats              ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget clear_stats_status log]"
}

################################################################################
# Start traffic on PE and CE ports
################################################################################
set traffic_status [::ixia::traffic_control \
        -port_handle "$pe_port $ce_port"    \
        -action sync_run                    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

after 40000


################################################################################
# Stop traffic on PE and CE ports
################################################################################
set traffic_status [::ixia::traffic_control \
        -port_handle "$pe_port $ce_port"    \
        -action stop                        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

after 5000


################################################################################
# Print traffic stats
################################################################################
set pe_stats [::ixia::traffic_stats -port_handle $pe_port -mode aggregate]
if {[keylget pe_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pe_stats log]"
}

set ce_stats [::ixia::traffic_stats -port_handle $ce_port -mode aggregate]
if {[keylget ce_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ce_stats log]"
}

set pe_transmit [keylget pe_stats $pe_port.aggregate.tx.pkt_count]
set ce_transmit [keylget ce_stats $ce_port.aggregate.tx.pkt_count]

set pe_stats [::ixia::traffic_stats -port_handle $pe_port -packet_group_id 1234]
if {[keylget pe_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pe_stats log]"
}

set ce_stats [::ixia::traffic_stats -port_handle $ce_port -packet_group_id 1234]
if {[keylget ce_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ce_stats log]"
}

set pe_receive [keylget pe_stats $pe_port.pgid.rx.pkt_count.1234]
set ce_receive [keylget ce_stats $ce_port.pgid.rx.pkt_count.1234]

puts "                          PE port              CE port"
puts "-------------------------------------------------------"
puts [format "Frames sent          %12s         %12s" \
        $pe_transmit $ce_transmit]
puts [format "Frames received      %12s         %12s" \
        $pe_receive $ce_receive]

return "SUCCESS - $test_name - [clock format [clock seconds]]"
