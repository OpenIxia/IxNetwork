################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Matei-Eugen Vasile $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    4-30-2007 Matei-Eugen Vasile
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
#    This sample creates a 6PE DUT setup.                                      #
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
#    CE runs IS-IS                                                             #
#                                                                              #
################################################################################

################################################################################
# DUT config:                                                                  #
################################################################################
# conf t
# !
# ip subnet-zero
# !
# ip cef
# !
# ipv6 unicast-routing
# mpls label protocol ldp
# mpls ipv6 source-interface Loopback0
# !
# interface Loopback0
#  ip address 20.0.0.1 255.255.255.255
# !
# interface FastEthernet5/0
#  ip address 21.0.0.1 255.255.255.0
#  mpls label protocol ldp
#  mpls ip
#  no shutdown
# !
# interface FastEthernet6/0
#  no ip address
#  no shutdown
# !
# interface FastEthernet6/0.601
#  encapsulation dot1Q 601
#  ipv6 address 2007:1::1/64
#  ipv6 enable
#  ipv6 router isis 600
# !
# interface FastEthernet6/0.602
#  encapsulation dot1Q 602
#  ipv6 address 2007:2::1/64
#  ipv6 enable
#  ipv6 router isis 600
# !
# interface FastEthernet6/0.603
#  encapsulation dot1Q 603
#  ipv6 address 2007:3::1/64
#  ipv6 enable
#  ipv6 router isis 600
# !
# interface FastEthernet6/0.604
#  encapsulation dot1Q 604
#  ipv6 address 2007:4::1/64
#  ipv6 enable
#  ipv6 router isis 600
# !
# interface FastEthernet6/0.605
#  encapsulation dot1Q 605
#  ipv6 address 2007:5::1/64
#  ipv6 enable
#  ipv6 router isis 600
# !
# router ospf 1
#  network 20.0.0.1 0.0.0.0 area 0
#  network 21.0.0.0 0.0.0.255 area 0
# !
# router isis 600
#  net 49.0000.0001.0001.0000.0000.0001.00
#  is-type level-1
#  metric-style transition
#  redistribute bgp 1
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
#  address-family ipv6
#  neighbor 20.0.0.2 activate
#  neighbor 20.0.0.2 send-label
#  neighbor 20.0.0.3 activate
#  neighbor 20.0.0.3 send-label
#  neighbor 20.0.0.4 activate
#  neighbor 20.0.0.4 send-label
#  redistribute connected
#  redistribute isis 600 level-1
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

proc script_increment_ipv6_address {ip_addr ip_addr_step} {
    set addr_words [split $ip_addr :]
    set step_words [split $ip_addr_step :]
    set index 7
    set result [list]
    set carry 0
    while {$index >= 0} {
        scan [lindex $addr_words $index] "%x" addr_word
        scan [lindex $step_words $index] "%x" step_word
        set value [expr $addr_word + $step_word + $carry]
        set carry [expr $value / 0xFFFF]
        set value [expr $value % 0xFFFF]
        lappend result $value
        incr index -1
    }
    set new_addr [format "%04x" [lindex $result 7]]
    for {set i 6} {$i >= 0} {incr i -1} {
        append new_addr ":[format "%04x" [lindex $result $i]]"
    }
    return $new_addr
}

proc script_expand_ipv6_address {ip_addr} {
    if {![regexp {(.*)::(.*)} $ip_addr {} before after]} {
        set ip_addr [split $ip_addr :]
        set new_addr "[format "%04x" 0x[lindex $ip_addr 0]]"
        for {set i 1} {$i < [llength $ip_addr]} {incr i} {
            append new_addr ":[format "%04x" 0x[lindex $ip_addr $i]]"
        }
    } else {
        set before [split $before :]
        set after [split $after :]
        set zeroes_length [expr 8 - [llength $before] - \
                [llength $after]]
        set new_addr ""
        if {[llength $before] > 0} {
            append new_addr "[format "%04x" 0x[lindex $before 0]]"
            for {set i 1} {$i < [llength $before]} {incr i} {
                append new_addr ":[format "%04x" 0x[lindex $before $i]]"
            }
        }
        if {$zeroes_length > 0} {
            if {[llength $before] > 0} {
                append new_addr ":0000"
            } else {
                append new_addr "0000"
            }
            for {set i 1} {$i < $zeroes_length} {incr i} {
                append new_addr ":0000"
            }
        }
        if {[llength $after] > 0} {
            for {set i 0} {$i < [llength $after]} {incr i} {
                append new_addr ":[format "%04x" 0x[lindex $after $i]]"
            }
        }
    }
    return $new_addr
}

package require Ixia

set test_name               [info script]

set chassisIP               10.205.19.96
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

set pe_adv_label_start      102
set pe_adv_network          [script_expand_ipv6_address 10:2::]
set pe_adv_prefix_len       64
set pe_adv_network_step     [script_expand_ipv6_address 0:1::]
set pe_adv_num_routes       2

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

set ce_count                5
set ce_ip_address           [script_expand_ipv6_address 2007:1::2]
set ce_ip_address_step      [script_expand_ipv6_address 0:1::]
set ce_prefix_len           64
set ce_vlan_id              601
set ce_vlan_id_step         1

set c_site1                 [script_expand_ipv6_address 20:1:1::]
set c_site1_step            [script_expand_ipv6_address 0:0:1::]
set c_prefix1_step          [script_expand_ipv6_address 0:0:0:8::]
set c_prefix1_len           64
set c_num_prefixes1         3

set c_site2                 [script_expand_ipv6_address 30:1:1::]
set c_site2_step            [script_expand_ipv6_address 0:0:1::]
set c_prefix2_step          [script_expand_ipv6_address 0:0:0:8::]
set c_prefix2_len           64
set c_num_prefixes2         2


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
set ospf_neighbor_status [::ixia::emulation_ospf_config                       \
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
set ldp_routers_status [::ixia::emulation_ldp_config                          \
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
set ldp_handle [keylget ldp_routers_status handle]

################################################################################
# Advertising a FEC for each semulated PE router                               #
################################################################################
set pe_ip_address_temp      $pe_ip_address
for {set i 0} {$i < $pe_count} {incr i} {
    set ldp_routers_status [::ixia::emulation_ldp_route_config                \
            -mode                   create                                  \
            -handle                 $ldp_handle                             \
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
set bgp_router_status [::ixia::emulation_bgp_config                           \
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
        -ipv6_mpls_nlri                                                     \
        ]
if {[keylget bgp_router_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_router_status log]"
}
set bgp_neighbor_handles [keylget bgp_router_status handles]

################################################################################
# Configure MPLS route ranges on each BGP Neighbor                             #
################################################################################
set pe_adv_network_temp     $pe_adv_network
set pe_adv_label_start_temp $pe_adv_label_start
foreach {bgp_neighbor_handle} $bgp_neighbor_handles {
    set bgp_route_range_status [::ixia::emulation_bgp_route_config          \
            -mode                       add                                 \
            -handle                     $bgp_neighbor_handle                \
            -ip_version                 6                                   \
            -prefix                     $pe_adv_network_temp                \
            -prefix_step                1                                   \
            -ipv6_prefix_length         $pe_adv_prefix_len                  \
            -label_value                $pe_adv_label_start_temp            \
            -label_step                 0                                   \
            -num_sites                  1                                   \
            -num_routes                 $pe_adv_num_routes                  \
            -local_pref                 0                                   \
            -next_hop_enable            1                                   \
            -origin_route_enable                                            \
            -enable_traditional_nlri    1                                   \
            -ipv6_mpls_nlri                                                 \
            ]
    if {[keylget bgp_route_range_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget bgp_route_range_status log]"
    }
    
    set pe_adv_network_temp [script_increment_ipv6_address \
            $pe_adv_network_temp $pe_adv_network_step]
    incr pe_adv_label_start_temp $pe_adv_num_routes
}

################################################################################
# Configure IS-IS emulated routers on the customer port                        #
################################################################################
set isis_neighbor_status [::ixia::emulation_isis_config                       \
        -port_handle                $ce_port                                \
        -reset                                                              \
        -mode                       create                                  \
        -count                      $ce_count                               \
        -ip_version                 6                                       \
        -system_id                  "00 00 00 00 01 00"                     \
        -system_id_step             "00 00 00 00 01 00"                     \
        -intf_ipv6_addr             $ce_ip_address                          \
        -intf_ipv6_addr_step        $ce_ip_address_step                     \
        -intf_ipv6_prefix_length    $ce_prefix_len                          \
        -vlan_id                    $ce_vlan_id                             \
        -vlan_id_step               $ce_vlan_id_step                        \
        -routing_level              L1                                      \
        -intf_type                  broadcast                               \
        -loopback_ip_addr_count     0                                       \
        ]
if {[keylget isis_neighbor_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_neighbor_status log]"
}
set isis_ce_handles [keylget isis_neighbor_status handle]

################################################################################
# Configure two route ranges on each customer router                           #
################################################################################
set c_site1_temp $c_site1
set c_site2_temp $c_site2
foreach {isis_ce_handle} $isis_ce_handles {
    set isis_route_status [::ixia::emulation_isis_topology_route_config     \
            -mode                   create                                  \
            -handle                 $isis_ce_handle                         \
            -type                   stub                                    \
            -ip_version             6                                       \
            -stub_ipv6_start        $c_site1_temp                           \
            -stub_ipv6_step         $c_prefix1_step                         \
            -stub_ipv6_pfx_len      $c_prefix1_len                          \
            -stub_count             $c_num_prefixes1                        \
            -stub_metric            1                                       \
            ]
    if {[keylget isis_route_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget isis_route_status log]"
    }
    set c_site1_temp [script_increment_ipv6_address                         \
            $c_site1_temp $c_site1_step                                     \
            ]
    
    set isis_route_status [::ixia::emulation_isis_topology_route_config     \
            -mode                   create                                  \
            -handle                 $isis_ce_handle                         \
            -type                   stub                                    \
            -ip_version             6                                       \
            -stub_ipv6_start        $c_site2_temp                           \
            -stub_ipv6_step         $c_prefix2_step                         \
            -stub_ipv6_pfx_len      $c_prefix2_len                          \
            -stub_count             $c_num_prefixes2                        \
            -stub_metric            1                                       \
            ]
    if {[keylget isis_route_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget isis_route_status log]"
    }
    set c_site2_temp [script_increment_ipv6_address                         \
            $c_site2_temp $c_site2_step                                     \
            ]
}

################################################################################
# Start OSPFv2 on the provider port                                            #
################################################################################
set ospf_emulation_status [::ixia::emulation_ospf_control                     \
        -port_handle        $pe_port                                        \
        -mode               start                                           \
        ]
if {[keylget ospf_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_emulation_status log]"
}

################################################################################
# Start LDP on the provider port                                               #
################################################################################
set ldp_emulation_status [::ixia::emulation_ldp_control                       \
        -port_handle        $pe_port                                        \
        -mode               start                                           \
        ]
if {[keylget ldp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_emulation_status log]"
}

################################################################################
# Start BGP on the provider port                                               #
################################################################################
set bgp_emulation_status [::ixia::emulation_bgp_control                       \
        -port_handle        $pe_port                                        \
        -mode               start                                           \
        ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}

################################################################################
# Start IS-IS on the client port                                               #
################################################################################
set isis_emulation_status [::ixia::emulation_isis_control                     \
        -port_handle        $ce_port                                        \
        -mode               start                                           \
        ]
if {[keylget isis_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_emulation_status log]"
}

################################################################################
# Wait for the routes to be learned                                            #
################################################################################
after 30000

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
# Generate traffic from the router on the first port to the one on the second  #
################################################################################
set traffic_status [::ixia::traffic_config                                  \
        -mode                   create                                      \
        -traffic_generator      ixnetwork                                   \
        -transmit_mode          continuous                                  \
        -name                   "6PE_OSPF_LDP_IS-IS_Traffic"                \
        -src_dest_mesh          one_to_one                                  \
        -route_mesh             one_to_one                                  \
        -circuit_type           6pe                                         \
        -circuit_endpoint_type  ipv6                                        \
        -emulation_src_handle   [lindex $bgp_neighbor_handles 0]            \
        -emulation_dst_handle   [lindex $isis_ce_handles 0]                 \
        -track_by               endpoint_pair                               \
        -stream_packing         one_stream_per_endpoint_pair                \
        -pkts_per_burst         2                                           \
        -rate_percent           4.5                                         \
        -enforce_min_gap        9                                           \
        -tx_delay               10                                          \
        -inter_frame_gap        8                                           \
        -inter_burst_gap        11                                          \
        -inter_stream_gap       12                                          \
        -length_mode            fixed                                       \
        -frame_size             512                                         \
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
        puts "\t\t$name: [keylget aggregated_traffic_status\
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
                puts "\t\t$name: [keylget stream_traffic_status\
                        [subst $[subst port_$i]].stream.$stream.$dir.$key]"
            }
        }
    }
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
