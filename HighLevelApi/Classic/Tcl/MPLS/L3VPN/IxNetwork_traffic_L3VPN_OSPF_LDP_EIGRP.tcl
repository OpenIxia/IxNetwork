################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10-17-2007 LRaicea - created sample
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
#    This sample creates a L3VPN DUT setup.                                    #
#                                                                              #
#    It uses two Ixia ports. One port is used for PEs and P router             #
#    configuration. The other port is used for CE routers configuration.       #
#    Streams are generated on both ports and then started.                     #
#                                                                              #
#         ------        -----           -----          ------                  #
#        |  PEs  |-----|  P  |---------| DUT |--------|  CEs |                 #
#         ------        -----     |     -----     |    ------                  #
#                                 |               |                            #
#               Ixia port 1       |  Cisco 7200   |    Ixia port 2             #
#                                                                              #
#    PEs runs mBGP, LDP and OSPFv2                                             #
#    P  runs LDP and OSPFv2                                                    #
#    CE runs EIGRP                                                             #
#                                                                              #
################################################################################

################################################################################
# DUT config:                                                                  #
#
# configure terminal
# !
# ip subnet-zero
# !
# ip cef
# !
# ip vrf vpn401
#  rd 1:401
#  route-target both 1:401
# !
# ip vrf vpn402
#  rd 1:402
#  route-target both 1:402
# !
# ip vrf vpn403
#  rd 1:403
#  route-target both 1:403
# !
# ip vrf vpn404
#  rd 1:404
#  route-target both 1:404
# !
# ip vrf vpn405
#  rd 1:405
#  route-target both 1:405
# !
# mpls label protocol ldp
# !
# interface Loopback0
#  ip address 20.0.0.1 255.255.255.255
# !
# interface GigabitEthernet0/2
#  ip address 21.0.0.1 255.255.255.0
#  mpls label protocol ldp
#  mpls ip
#  no shutdown
# !
# interface GigabitEthernet0/3
#  no ip address
#  no shutdown
# !
# interface GigabitEthernet0/3.401
#  encapsulation dot1Q 401
#  ip vrf forwarding vpn401
#  ip address 22.1.1.1 255.255.255.0
# !
# interface GigabitEthernet0/3.402
#  encapsulation dot1Q 402
#  ip vrf forwarding vpn402
#  ip address 22.1.2.1 255.255.255.0
# !
# interface GigabitEthernet0/3.403
#  encapsulation dot1Q 403
#  ip vrf forwarding vpn403
#  ip address 22.1.3.1 255.255.255.0
# !
# interface GigabitEthernet0/3.404
#  encapsulation dot1Q 404
#  ip vrf forwarding vpn404
#  ip address 22.1.4.1 255.255.255.0
# !
# interface GigabitEthernet0/3.405
#  encapsulation dot1Q 405
#  ip vrf forwarding vpn405
#  ip address 22.1.5.1 255.255.255.0
# !
# router eigrp 500
#  address-family ipv4 vrf vpn401
#   redistribute bgp 1 metric 10000 1 255 1 1500
#   no auto-summary
#   network 22.1.1.0 0.0.0.255
#   default-metric 10000 1 255 1 1500
#   autonomous-system 500
#  exit-address-family
#     
#  address-family ipv4 vrf vpn402
#   redistribute bgp 1 metric 10000 1 255 1 1500
#   no auto-summary
#   network 22.1.2.0 0.0.0.255
#   default-metric 10000 1 255 1 1500
#   autonomous-system 500
#  exit-address-family
#  !
#  address-family ipv4 vrf vpn403
#   redistribute bgp 1 metric 10000 1 255 1 1500
#   no auto-summary
#   network 22.1.3.0 0.0.0.255
#   default-metric 10000 1 255 1 1500
#   autonomous-system 500
#  exit-address-family
#  !
#  address-family ipv4 vrf vpn404
#   redistribute bgp 1 metric 10000 1 255 1 1500
#   no auto-summary
#   network 22.1.4.0 0.0.0.255
#   default-metric 10000 1 255 1 1500
#   autonomous-system 500
#  exit-address-family
#  !
#  address-family ipv4 vrf vpn405
#   redistribute bgp 1 metric 10000 1 255 1 1500
#   no auto-summary
#   network 22.1.5.0 0.0.0.255
#   default-metric 10000 1 255 1 1500
#   autonomous-system 500
#  exit-address-family
#  !
# router ospf 1
#  network 20.0.0.1 0.0.0.0 area 0
#  network 21.0.0.0 0.0.0.255 area 0
# !
# router bgp 1
#  no synchronization
#  redistribute rip metric 1
#  neighbor 20.0.0.2 remote-as 1
#  neighbor 20.0.0.2 update-source Loopback0
#  neighbor 20.0.0.3 remote-as 1
#  neighbor 20.0.0.3 update-source Loopback0
#  neighbor 20.0.0.4 remote-as 1
#  neighbor 20.0.0.4 update-source Loopback0
#  no auto-summary
#  !
#  address-family vpnv4
#  neighbor 20.0.0.2 activate
#  neighbor 20.0.0.2 send-community extended
#  neighbor 20.0.0.3 activate
#  neighbor 20.0.0.3 send-community extended
#  neighbor 20.0.0.4 activate
#  neighbor 20.0.0.4 send-community extended
#  exit-address-family
#  !
#  address-family ipv4 vrf vpn401
#  redistribute eigrp 500
#  no synchronization
#  exit-address-family
#  !
#  address-family ipv4 vrf vpn402
#  redistribute eigrp 500
#  no synchronization
#  exit-address-family
#  !
#  address-family ipv4 vrf vpn403
#  redistribute eigrp 500
#  no synchronization
#  exit-address-family
#  !
#  address-family ipv4 vrf vpn404
#  redistribute eigrp 500
#  no synchronization
#  exit-address-family
#  !
#  address-family ipv4 vrf vpn405
#  redistribute eigrp 500
#  no synchronization
#  exit-address-family
# !
# end
################################################################################

proc script_increment_ipv4_address {ip_addr ip_addr_step} {
    set addr_words [split $ip_addr .]
    set step_words [split $ip_addr_step .]
    set index 3
    set result [list]
    set carry 0
    while {$index >= 0} {
        scan [lindex $addr_words $index] "%u" addr_word
        scan [lindex $step_words $index] "%u" step_word
        set value [expr $addr_word + $step_word + $carry]
        set carry [expr $value / 0xFF]
        set value [expr $value % 0xFF]
        lappend result $value
        incr index -1
    }
    set new_addr [format "%u" [lindex $result 3]]
    for {set i 2} {$i >= 0} {incr i -1} {
        append new_addr ".[format "%u" [lindex $result $i]]"
    }
    return $new_addr
}

package require Ixia
set test_name               [info script]

set chassisIP               sylvester
set port_list               [list 2/3 2/4]

set pe_ip_address           20.0.0.2
set pe_ip_address_step      0.0.0.1
set pe_prefix_len           32
set pe_intf_ip_address      23.0.0.2
set pe_intf_ip_address_step 0.0.0.1
set pe_intf_mask            255.255.255.0
set pe_count                3
set pe_bgp_peer_ip          20.0.0.1
set pe_bgp_peer_ip_step     0.0.0.0
set pe_bgp_router_id        1.2.3.4
set pe_bgp_router_id_step   0.0.0.1
set pe_bgp_as               1
set pe_bgp_as_step          0

set vrf_count               5
set vrf_rd_target_type      0
set vrf_rd_admin_value      1
set vrf_rd_admin_step       0
set vrf_rd_assign_value     401
set vrf_rd_assign_step      1
set vrf_target_type         "as"
set vrf_admin_value         1
set vrf_admin_step          0
set vrf_assign_value        401
set vrf_assign_step         1
set vrf_site                100.2.1.0
set vrf_site_step           0.1.0.0
set vrf_network_step        0.0.1.0
set vrf_network_mask        255.255.255.192
set vrf_label_value         55
set vrf_num_routes          2

set p_ip_address            21.0.0.2
set p_ip_address_step       0.0.0.0
set p_prefix_len            24
set p_gateway_ip            21.0.0.1
set p_gateway_ip_step       0.0.0.0
set p_ospf_router_id        1.2.3.4
set p_ospf_router_id_step   0.0.0.0
set p_ospf_area_id          0.0.0.0
set p_ospf_area_id_step     0.0.0.0
set p_lsr_id                1.2.3.4
set p_lsr_id_step           0.0.0.0

set ce_ip_address           22.1.1.2
set ce_ip_address_step      0.0.1.0
set ce_prefix_len           24
set ce_gateway_ip           22.1.1.1
set ce_gateway_ip_step      0.0.1.0
set ce_vlan_id              401
set ce_vlan_id_step         1
set ce_eigrp_router_id      5.6.7.8
set ce_eigrp_router_id_step 0.0.0.1
set ce_eigrp_as             500
set ce_eigrp_as_step        0

set ce_site1                 110.1.1.0
set ce_site1_step            0.0.1.0
set ce_prefix1_len           26
set ce_num_prefixes1         3

set ce_site2                 120.1.1.0
set ce_site2_step            0.0.1.0
set ce_prefix2_len           26
set ce_num_prefixes2         2

################################################################################
# Connect to the chassis, reset to factory defaults and take ownership         #
################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                         \
        -reset                                                              \
        -ixnetwork_tcl_server   localhost                                   \
        -device                 $chassisIP                                  \
        -port_list              $port_list                                  \
        ]
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
set port_0 $pe_port
set port_1 $ce_port

################################################################################
# Initialize ports                                                             #
################################################################################
set intf_status [::ixia::interface_config                                   \
        -port_handle        "$pe_port $ce_port"                             \
        -autonegotiation    1                                               \
        -speed              ether1000                                       \
        -transmit_mode      advanced                                        \
        ]
if {[keylget intf_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget intf_status log]"
}

################################################################################
# Configure an OSPFv2 emulated router on the provider port                     #
################################################################################
set ospf_neighbor_status [::ixia::emulation_ospf_config                     \
        -port_handle                $pe_port                                \
        -reset                                                              \
        -session_type               ospfv2                                  \
        -mode                       create                                  \
        -count                      1                                       \
        -intf_ip_addr               $p_ip_address                           \
        -intf_ip_addr_step          $p_ip_address_step                      \
        -router_id                  $p_ospf_router_id                       \
        -router_id_step             $p_ospf_router_id_step                  \
        -neighbor_intf_ip_addr      $p_gateway_ip                           \
        -neighbor_intf_ip_addr_step $p_gateway_ip_step                      \
        -area_id                    $p_ospf_area_id                         \
        -area_id_step               $p_ospf_area_id_step                    \
        -area_type                  external-capable                        \
        -network_type               broadcast                               \
        -option_bits                0x02                                    \
        ]
if {[keylget ospf_neighbor_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_neighbor_status log]"
}
set p_ospf_handle [keylget ospf_neighbor_status handle]

################################################################################
# Add routes on the OSPFv2 router from the provider port                       #
################################################################################
set pe_ip_address_temp      $pe_ip_address
set pe_intf_ip_address_temp $pe_intf_ip_address
for {set i 0} {$i < $pe_count} {incr i} {
    set route_config_status [::ixia::emulation_ospf_topology_route_config   \
            -mode                   create                                  \
            -handle                 $p_ospf_handle                          \
            -type                   grid                                    \
            -grid_router_id         $pe_ip_address_temp                     \
            -grid_router_id_step    $pe_ip_address_step                     \
            -grid_row               1                                       \
            -grid_col               1                                       \
            -grid_link_type         ptop_numbered                           \
            -grid_prefix_start      $pe_ip_address_temp                     \
            -grid_prefix_length     $pe_prefix_len                          \
            -grid_prefix_step       $pe_ip_address_step                     \
            -grid_te                0                                       \
            -grid_connect           1 1                                     \
            -interface_ip_address   $pe_intf_ip_address_temp                \
            -interface_ip_mask      $pe_intf_mask                           \
            -enable_advertise       1                                       \
            ]
    if {[keylget route_config_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget route_config_status log]"
    }

    set pe_ip_address_temp [script_increment_ipv4_address                   \
            $pe_ip_address_temp $pe_ip_address_step                         \
            ]
    set pe_intf_ip_address_temp [script_increment_ipv4_address              \
            $pe_intf_ip_address_temp $pe_intf_ip_address_step               \
            ]
}

################################################################################
# Configure an LDP emulated router on the provider port                        #
################################################################################
set ldp_routers_status [::ixia::emulation_ldp_config                        \
        -mode                   create                                      \
        -reset                                                              \
        -port_handle            $pe_port                                    \
        -label_adv              unsolicited                                 \
        -peer_discovery         link                                        \
        -count                  1                                           \
        -intf_ip_addr           $p_ip_address                               \
        -intf_ip_addr_step      $p_ip_address_step                          \
        -intf_prefix_length     $p_prefix_len                               \
        -lsr_id                 $p_lsr_id                                   \
        -lsr_id_step            $p_lsr_id_step                              \
        -label_space            0                                           \
        -gateway_ip_addr        $p_gateway_ip                               \
        -gateway_ip_addr_step   $p_gateway_ip_step                          \
        ]
if {[keylget ldp_routers_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_routers_status log]"
}
set p_ldp_handle [keylget ldp_routers_status handle]

################################################################################
# Advertising a FEC for each semulated PE router                               #
################################################################################
set pe_ip_address_temp      $pe_ip_address
for {set i 0} {$i < $pe_count} {incr i} {
    set ldp_routers_status [::ixia::emulation_ldp_route_config              \
            -mode                   create                                  \
            -handle                 $p_ldp_handle                           \
            -fec_type               ipv4_prefix                             \
            -fec_ip_prefix_start    $pe_ip_address_temp                     \
            -fec_ip_prefix_length   $pe_prefix_len                          \
            -egress_label_mode      imnull                                  \
            ]
    if {[keylget ldp_routers_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget ldp_routers_status log]"
    }
    
    set pe_ip_address_temp [script_increment_ipv4_address                   \
            $pe_ip_address_temp $pe_ip_address_step                         \
            ]
}

################################################################################
# Configure a BGP neighbor on the provider port                                #
################################################################################
set bgp_router_status [::ixia::emulation_bgp_config                         \
        -mode                           reset                               \
        -port_handle                    $pe_port                            \
        -count                          $pe_count                           \
        -local_ip_addr                  $p_ip_address                       \
        -local_addr_step                $p_ip_address_step                  \
        -remote_ip_addr                 $p_gateway_ip                       \
        -remote_addr_step               $p_gateway_ip_step                  \
        -local_loopback_ip_addr         $pe_ip_address                      \
        -local_loopback_ip_addr_step    $pe_ip_address_step                 \
        -remote_loopback_ip_addr        $pe_bgp_peer_ip                     \
        -remote_loopback_ip_addr_step   $pe_bgp_peer_ip_step                \
        -local_router_id                $pe_bgp_router_id                   \
        -local_router_id_step           $pe_bgp_router_id_step              \
        -neighbor_type                  internal                            \
        -ip_version                     4                                   \
        -local_as                       $pe_bgp_as                          \
        -local_as_mode                  fixed                               \
        -active_connect_enable                                              \
        -ipv4_mpls_vpn_nlri                                                 \
        ]
if {[keylget bgp_router_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_router_status log]"
}
set pe_bgp_handles [keylget bgp_router_status handles]

################################################################################
# Configure VRFs on each BGP Neighbor                                          #
################################################################################
set vrf_site_temp $vrf_site
set vpn_route_ranges [list]
set vrf_label_value_site $vrf_label_value
foreach {pe_bgp_handle} $pe_bgp_handles {
    set vrf_network_temp $vrf_site_temp
    set vrf_label_value_temp $vrf_label_value_site
    set vrf_rd_admin_value_temp $vrf_rd_admin_value
    set vrf_rd_assign_value_temp $vrf_rd_assign_value
    set vrf_admin_value_temp $vrf_admin_value
    set vrf_assign_value_temp $vrf_assign_value
    for {set l3site 0} {$l3site < $vrf_count} {incr l3site} {
        set bgp_route_range_status [::ixia::emulation_bgp_route_config      \
                -mode                       add                             \
                -handle                     $pe_bgp_handle                  \
                -ip_version                 4                               \
                -prefix                     $vrf_network_temp               \
                -prefix_step                1                               \
                -netmask                    $vrf_network_mask               \
                -label_value                $vrf_label_value_temp           \
                -label_step                 0                               \
                -num_sites                  1                               \
                -num_routes                 $vrf_num_routes                 \
                -rd_type                    $vrf_rd_target_type             \
                -rd_admin_value             $vrf_rd_admin_value_temp        \
                -rd_admin_step              0                               \
                -rd_assign_value            $vrf_rd_assign_value_temp       \
                -rd_assign_step             0                               \
                -target_type                $vrf_target_type                \
                -target                     $vrf_admin_value_temp           \
                -target_step                0                               \
                -target_assign              $vrf_assign_value_temp          \
                -target_assign_step         0                               \
                -import_target_type         $vrf_target_type                \
                -import_target              $vrf_admin_value_temp           \
                -import_target_step         0                               \
                -import_target_assign       $vrf_assign_value_temp          \
                -import_target_assign_step  0                               \
                -local_pref                 0                               \
                -next_hop_enable            1                               \
                -origin_route_enable                                        \
                -enable_traditional_nlri    1                               \
                -ipv4_mpls_vpn_nlri                                         \
                ]
        if {[keylget bgp_route_range_status status] != $::SUCCESS} {
            return "FAIL - $test_name - [keylget bgp_route_range_status log]"
        }
        set vpn_route_ranges [concat $vpn_route_ranges                      \
                [keylget bgp_route_range_status bgp_routes]                 \
                ]

        set vrf_network_temp [script_increment_ipv4_address                 \
                $vrf_network_temp $vrf_network_step                         \
                ]
        incr vrf_label_value_temp
        incr vrf_rd_admin_value_temp $vrf_rd_admin_step
        incr vrf_rd_assign_value_temp $vrf_rd_assign_step
        incr vrf_admin_value_temp $vrf_admin_step
        incr vrf_assign_value_temp $vrf_assign_step
    }

    set vrf_site_temp [script_increment_ipv4_address                        \
            $vrf_site_temp $vrf_site_step                                   \
            ]
    incr vrf_label_value_site $vrf_count
}

################################################################################
# Configure EIGRP emulated routers on the customer port                        #
################################################################################
set eigrp_router_status [::ixia::emulation_eigrp_config                      \
        -mode                           create                               \
        -reset             			                                         \
        -port_handle                    $ce_port                             \
        -count      		            $vrf_count                           \
        -intf_ip_addr                   $ce_ip_address                       \
        -intf_ip_addr_step              $ce_ip_address_step                  \
        -router_id                      $ce_eigrp_router_id                  \
        -router_id_step                 $ce_eigrp_router_id_step             \
        -intf_gw_ip_addr                $ce_gateway_ip                       \
        -intf_gw_ip_addr_step           $ce_gateway_ip_step                  \
        -vlan                           1                                    \
        -vlan_id                        $ce_vlan_id                          \
        -vlan_id_step                   $ce_vlan_id_step                     \
        -discard_learned_routes         0                                    \
        -as_number                      $ce_eigrp_as                         \
        -as_number_step                 $ce_eigrp_as_step                    \
        ]


if {[keylget eigrp_router_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget eigrp_router_status log]"
}
set ce_eigrp_handles [keylget eigrp_router_status router_handles]

################################################################################
# Configure two route ranges on each customer router                           #
################################################################################
set ce_site1_temp $ce_site1
set ce_site2_temp $ce_site2
foreach {ce_eigrp_handle} $ce_eigrp_handles {
    set eigrp_route_status [::ixia::emulation_eigrp_route_config            \
            -mode                       create                              \
            -handle                     $ce_eigrp_handle                    \
            -type                       internal                            \
            -prefix_start               $ce_site1_temp                      \
            -prefix_length              $ce_prefix1_len                     \
            -num_prefixes               $ce_num_prefixes1                   \
            ]
    if {[keylget eigrp_route_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget eigrp_route_status log]"
    }
    set ce_site1_temp [script_increment_ipv4_address                        \
            $ce_site1_temp $ce_site1_step                                   \
            ]
    
    set eigrp_route_status [::ixia::emulation_eigrp_route_config            \
            -mode                       create                              \
            -handle                     $ce_eigrp_handle                    \
            -type                       internal                            \
            -prefix_start               $ce_site2_temp                      \
            -prefix_length              $ce_prefix2_len                     \
            -num_prefixes               $ce_num_prefixes2                   \
            ]
    if {[keylget eigrp_route_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget eigrp_route_status log]"
    }
    set ce_site2_temp [script_increment_ipv4_address                        \
            $ce_site2_temp $ce_site2_step                                   \
            ]
}

################################################################################
# Start OSPFv2 on the provider port                                            #
################################################################################
set ospf_emulation_status [::ixia::emulation_ospf_control                   \
        -port_handle        $pe_port                                        \
        -mode               start                                           \
        ]
if {[keylget ospf_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_emulation_status log]"
}

################################################################################
# Start LDP on the provider port                                               #
################################################################################
set ldp_emulation_status [::ixia::emulation_ldp_control                     \
        -port_handle        $pe_port                                        \
        -mode               start                                           \
        ]
if {[keylget ldp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_emulation_status log]"
}

################################################################################
# Start BGP on the provider port                                               #
################################################################################
set bgp_emulation_status [::ixia::emulation_bgp_control                     \
        -port_handle        $pe_port                                        \
        -mode               start                                           \
        ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}

################################################################################
# Start EIGRP on the client port                                              #
################################################################################
set eigrp_emulation_status [::ixia::emulation_eigrp_control                 \
        -port_handle        $ce_port                                        \
        -mode               start                                           \
        ]
if {[keylget eigrp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget eigrp_emulation_status log]"
}

################################################################################
# Wait for the BGP sessions to establish                                       #
################################################################################
set bgp_sessions_established 0
set retries                  10
while {($bgp_sessions_established < $pe_count) && ($retries >= 0)} {
    # For IxTclNetwork, this command returns per port stats, 
    # evenif a neighbor handle is specified
    set bgp_aggregate_status [ixia::emulation_bgp_info                      \
            -handle      [lindex $pe_bgp_handles 0]                         \
            -mode        stats                                              ]

    if {[keylget bgp_aggregate_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget bgp_aggregate_status log]"
    }
    puts "Retrieving aggregate BGP stats, number of retries left: $retries ..."
    update idletasks
    if {![catch {keylget bgp_aggregate_status sessions_established}]} {
        set bgp_sessions_established \
                [keylget bgp_aggregate_status sessions_established]
    }
    incr retries -1
    if {$bgp_sessions_established < $pe_count} {
        after 1000
    }
}
if {$bgp_sessions_established < $pe_count} {
    return "FAIL - $test_name - Not all BGP sessions have been established."
}
puts "There are $bgp_sessions_established BGP sessions established ..."
update idletasks
################################################################################
# Wait for the BGP information to be learned                                   #
################################################################################
set min_bgp_learned_routes [mpexpr $vrf_count * \
        ($ce_num_prefixes1 + $ce_num_prefixes2 + 1)]
foreach {pe_bgp_handle} $pe_bgp_handles {
    set bgp_learned_routes 0
    set retries            10
    while {($bgp_learned_routes < $min_bgp_learned_routes) && ($retries >= 0)} {
        set bgp_learned_status [ixia::emulation_bgp_info                    \
                -handle      $pe_bgp_handle                                 \
                -mode        labels                                         ]
    
        if {[keylget bgp_learned_status status] != $::SUCCESS} {
            return "FAIL - $test_name - [keylget bgp_learned_status log]"
        }
        puts "Retrieving learned BGP stats, number of retries left: $retries ..."
        update idletasks
        if {![catch {keylkeys bgp_learned_status}]} {
            set bgp_learned_routes \
                    [llength [keylkeys bgp_learned_status]]
        }
        incr retries -1
        if {$bgp_learned_routes < $min_bgp_learned_routes} {
            after 1000
        }
    }
    if {$bgp_learned_routes < $min_bgp_learned_routes} {
        return "FAIL - $test_name - Not all routes have been learned for\
                BGP neighbor $pe_bgp_handle."
    }
    puts "BGP routes learned for neighbor ${pe_bgp_handle}:"
    update idletasks
    foreach key [keylkeys bgp_learned_status] {
        if {$key == "status"} {continue}
        puts [format "\t\t%s/%s,\t\tnext hop: %s"        \
            [keylget bgp_learned_status $key.network]    \
            [keylget bgp_learned_status $key.prefix_len] \
            [keylget bgp_learned_status $key.next_hop]   ]
        update idletasks
    }
}
################################################################################
# Wait for the EIGRP information to be learned                                 #
################################################################################
set min_eigrp_learned_routes [mpexpr $pe_count * $vrf_num_routes]
foreach {ce_eigrp_handle} $ce_eigrp_handles {
    set eigrp_learned_routes 0
    set retries              10
    while {($eigrp_learned_routes < $min_eigrp_learned_routes) && ($retries >= 0)} {
        set eigrp_learned_status [ixia::emulation_eigrp_info                \
                -handle      $ce_eigrp_handle                               \
                -mode        learned_info                                   ]
    
        if {[keylget eigrp_learned_status status] != $::SUCCESS} {
            return "FAIL - $test_name - [keylget eigrp_learned_status log]"
        }
        puts "Retrieving learned BGP stats, number of retries left: $retries ..."
        update idletasks
        if {![catch {keylkeys eigrp_learned_status ${ce_port}.${ce_eigrp_handle}.route}]} {
            set eigrp_learned_routes \
                    [llength [keylkeys eigrp_learned_status \
                    ${ce_port}.${ce_eigrp_handle}.route]]
        }
        incr retries -1
        if {$eigrp_learned_routes < $min_eigrp_learned_routes} {
            after 1000
        }
    }
    if {$eigrp_learned_routes < $min_eigrp_learned_routes} {
        return "FAIL - $test_name - Not all routes have been learned for\
                EIGRP router $ce_eigrp_handle."
    }
    puts "EIGRP routes learned for neighbor ${ce_eigrp_handle}:"
    update idletasks
    foreach key [keylkeys eigrp_learned_status ${ce_port}.${ce_eigrp_handle}.route] {
        if {$key == "status"} {continue}
        puts [format "\t\t%s/%s,\t\tnext hop: %s" \
            [keylget eigrp_learned_status \
            ${ce_port}.${ce_eigrp_handle}.route.$key.prefix]        \
            [keylget eigrp_learned_status \
            ${ce_port}.${ce_eigrp_handle}.route.$key.prefix_length] \
            [keylget eigrp_learned_status \
            ${ce_port}.${ce_eigrp_handle}.route.$key.next_hop]      ]
        update idletasks
    }
}

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

################################################################################
# Generate traffic from PE to CE                                               #
################################################################################
set i 0
foreach {ce_eigrp_handle} $ce_eigrp_handles {
    set pe_bgp_route_handle ""
    for {set j 0} {$j < $pe_count} {incr j} {
        lappend pe_bgp_route_handle [lindex \
                $vpn_route_ranges [expr $j* $vrf_count + $i] ]
    }
    set traffic_status [::ixia::traffic_config                              \
            -mode                   create                                  \
            -traffic_generator      ixnetwork                               \
            -transmit_mode          continuous                              \
            -name                   "PE_to_CE_Traffic_$i"                   \
            -src_dest_mesh          one_to_one                              \
            -route_mesh             one_to_one                              \
            -circuit_type           l3vpn                                   \
            -circuit_endpoint_type  ipv4                                    \
            -emulation_src_handle   $pe_bgp_route_handle                    \
            -emulation_dst_handle   $ce_eigrp_handle                        \
            -track_by               endpoint_pair                           \
            -stream_packing         one_stream_per_endpoint_pair            \
            -pkts_per_burst         2                                       \
            -rate_percent           1                                       \
            -enforce_min_gap        9                                       \
            -tx_delay               10                                      \
            -inter_frame_gap        8                                       \
            -inter_burst_gap        11                                      \
            -inter_stream_gap       12                                      \
            -length_mode            fixed                                   \
            -frame_size             512                                     \
            ]
    if {[keylget traffic_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget traffic_status log]"
    }
    incr i
}
################################################################################
# Generate traffic from CE to PE                                               #
################################################################################
set i 0
foreach {ce_eigrp_handle} $ce_eigrp_handles {
    set pe_bgp_route_handle ""
    for {set j 0} {$j < $pe_count} {incr j} {
        lappend pe_bgp_route_handle [lindex \
                $vpn_route_ranges [expr $j* $vrf_count + $i] ]
    }
    set traffic_status [::ixia::traffic_config                              \
            -mode                   create                                  \
            -traffic_generator      ixnetwork                               \
            -transmit_mode          continuous                              \
            -name                   "CE_to_PE_Traffic_$i"                   \
            -src_dest_mesh          one_to_one                              \
            -route_mesh             one_to_one                              \
            -circuit_type           none                                    \
            -circuit_endpoint_type  ipv4                                    \
            -emulation_src_handle   $ce_eigrp_handle                        \
            -emulation_dst_handle   $pe_bgp_route_handle                    \
            -track_by               endpoint_pair                           \
            -stream_packing         one_stream_per_endpoint_pair            \
            -pkts_per_burst         2                                       \
            -rate_percent           1                                       \
            -enforce_min_gap        9                                       \
            -tx_delay               10                                      \
            -inter_frame_gap        8                                       \
            -inter_burst_gap        11                                      \
            -inter_stream_gap       12                                      \
            -length_mode            fixed                                   \
            -frame_size             512                                     \
            ]
    if {[keylget traffic_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget traffic_status log]"
    }
    incr i
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
set aggregated_traffic_results [list                                        \
        "Scheduled Frames Tx."          aggregate.tx.scheduled_pkt_count    \
        "Scheduled Frames Tx. Rate"     aggregate.tx.scheduled_pkt_rate     \
        "Line Speed"                    aggregate.tx.line_speed             \
        "Frames Tx."                    aggregate.tx.pkt_count              \
        "Total Frames Tx."              aggregate.tx.total_pkts             \
        "Frames Tx. Rate"               aggregate.tx.pkt_rate               \
        "Frames Tx. Rate"               aggregate.tx.total_pkt_rate         \
        "Bytes Tx."                     aggregate.tx.pkt_byte_count         \
        "Bytes Tx. Rate"                aggregate.tx.pkt_byte_rate          \
        "Tx. Rate (bps)"                aggregate.tx.pkt_bit_rate           \
        "Tx. Rate (Kbps)"               aggregate.tx.pkt_kbit_rate          \
        "Tx. Rate (Mbps)"               aggregate.tx.pkt_mbit_rate          \
        "Bytes Rx."                     aggregate.rx.pkt_byte_count         \
        "Bytes Rx. Rate"                aggregate.rx.pkt_byte_rate          \
        "Rx. Rate (bps)"                aggregate.rx.pkt_bit_rate           \
        "Rx. Rate (Kbps)"               aggregate.rx.pkt_kbit_rate          \
        "Rx. Rate (Mbps)"               aggregate.rx.pkt_mbit_rate          \
        "Data Integrity Frames Rx."     aggregate.rx.data_int_frames_count  \
        "Data Integrity Errors"         aggregate.rx.data_int_errors_count  \
        "Collisions"                    aggregate.rx.collisions_count       \
        "Valid Frames Rx."              aggregate.rx.pkt_count              \
        "Valid Frames Rx. Rate"         aggregate.rx.pkt_rate               \
        ]
for {set i 0} {$i < 2} {incr i} {
    puts "Port [subst $[subst port_$i]]:"
    puts "\tAggregated statistics:"
    foreach {name key} $aggregated_traffic_results {
        puts "\t\t[format %30s $name]: [keylget aggregated_traffic_status\
                [subst $[subst port_$i]].$key]"
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
for {set i 0} {$i < 2} {incr i} {
    puts "Port [subst $[subst port_$i]]:"
    set streams [keylget stream_traffic_status \
            [subst $[subst port_$i]].stream]
    foreach stream [keylkeys streams] {
        set stream_key [keylget stream_traffic_status \
                [subst $[subst port_$i]].stream.$stream]
        foreach dir [keylkeys stream_key] {
            puts "\tStream $stream - $dir:"
            foreach {name key} [subst $[subst stream_${dir}_results]] {
                puts "\t\t[format %30s $name]: [keylget stream_traffic_status\
                        [subst $[subst port_$i]].stream.$stream.$dir.$key]"
            }
        }
    }
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
