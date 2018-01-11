################################################################################
# Version 1.0    $Revision: 2 $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    16/8-2005 DRusu
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
#    This sample creates a 6PE setup. It uses two Ixia ports. One port is      #
#    used as a PE and P router. One port is used as CE router.                 #
#    Streams are generated on both ports and then started.                     #
#                                                                              #
#         ------       -----           -----          ------                   #
#        |  PE  |-----|  P  |---------| DUT |--------|  CE  |                  #
#         ------       -----     |     -----     |    ------                   #
#                                |               |                             #
#               Ixia port 1      |  Cisco 6500   |    Ixia port 2              #
#                                                                              #
#    PE runs mBGP                                                              #
#    P  runs LDP and ISIS                                                      #
#    CE runs ISIS (v6)                                                         #
#                                                                              #
#    Cisco configuration:                                                      #
#        ipv6 cef
#
#        ipv6 unicast-routing
#
#        mpls label protocol ldp
#        mpls ipv6 source-interface Loopback901
#
#        interface Loopback901
#        ip address 110.0.110.1 255.255.255.255
#
#        interface GigabitEthernet1/29
#        no ip address
#
#        interface GigabitEthernet1/29.1
#        description vpn901_ce
#        encapsulation dot1Q 901
#        ipv6 address 20::1/64
#        ipv6 router isis vpn901
#
#        interface GigabitEthernet1/30
#        description vpn901_pe
#        ip address 100.28.0.1 255.255.255.0
#        mpls label protocol ldp
#        tag-switching ip
#        ip router isis vpn9011
#
#        router isis vpn9011
#        net 49.1111.1111.1111.1111.00
#        is-type level-1-2
#        metric-style transition
#
#        router isis vpn901
#        net 49.1111.1111.1111.1111.00
#        is-type level-1-2
#        redistribute bgp 1 metric 20 level-1-2
#        metric-style transition
#
#        router bgp 1
#        neighbor 110.0.110.100 remote-as 1
#        neighbor 110.0.110.100 update-source Loopback901
#
#        address-family ipv6
#        neighbor 110.0.110.100 activate
#        neighbor 110.0.110.100 send-label
#        redistribute isis level-1-2 vpn901
#        exit-address-family
#        end
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM100TXS8 module.                              #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP        sylvester
set port_list        [list 1/1 1/2]

set pe_ip_address    110.0.110.100
set bgp_peer_ip      110.0.110.1

set p_ip_address     100.28.0.2
set p_prefix_len     24
set p_gateway_ip     100.28.0.1
set p_mac_address    0000.0002.0003

set ce_ip_address    20::21
set ce_prefix_len    64
set ce_vlan_id       901
set ce_mac_address   0000.0001.0002

set bgp_router_id    1.2.3.4
set bgp_as           1
set isis_router_id   1.2.3.4
set p_lsr_id         1.2.3.4

set pe_adv_label_start 101
set pe_adv_network     30::0
set pe_adv_prefix_len  64
set pe_adv_num_routes  2

set isis_ce_router_id 5.6.7.8

set c_network1       31::0
set c_prefix_len1    64
set c_num_prefixes1  3

set c_network2       32::0
set c_prefix_len2    64
set c_num_prefixes2  2

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

# Initialize ports
set intf_status [::ixia::interface_config    \
        -port_handle      $pe_port           \
        -autonegotiation  1                  \
        -transmit_mode    advanced           \
        -signature_offset 62                 \
        -pgid_offset      66                 ]
set intf_status [::ixia::interface_config    \
        -port_handle      $ce_port           \
        -autonegotiation  1                  \
        -transmit_mode    advanced           ]
        
#################################################
#  Configure ISIS neighbor on P/PE port         #
#################################################
set isis_router_status [::ixia::emulation_isis_config     \
        -mode                           create          \
        -reset                                                   \
        -port_handle                    $pe_port        \
        -intf_ip_addr                   $p_ip_address   \
        -gateway_ip_addr                $p_gateway_ip   \
        -intf_ip_prefix_length          $p_prefix_len   \
        -mac_address_init               $p_mac_address  \
        -count                                1               \
        -intf_metric                    0               \
        -routing_level                  L1L2            \
        -te_enable                      0               \
        -te_router_id                   $isis_router_id ]
if {[keylget isis_router_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_router_status log]"
}

set isis_router_handle [keylget isis_router_status handle]

set route_config_status [::ixia::emulation_isis_topology_route_config \
        -mode                   create                  \
        -handle                 $isis_router_handle     \
        -type                   stub                    \
        -ip_version             4                       \
        -stub_ip_start          $pe_ip_address          \
        -stub_ip_pfx_len        32                      \
        -stub_count             1                       \
        -stub_metric            1                       \
        -stub_up_down_bit       0                       ]
if {[keylget route_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget route_config_status log]"
}
##################### End of ISIS PE configuration ##################


#############################################
# Configure LDP Neighbor on P/PE port       #
#############################################
set ldp_routers_status [::ixia::emulation_ldp_config \
        -mode                  create              \
        -port_handle           $pe_port            \
        -label_adv             unsolicited         \
        -peer_discovery        link                \
        -count                 1                   \
        -intf_ip_addr          $p_ip_address       \
        -intf_prefix_length    $p_prefix_len       \
        -intf_ip_addr_step     0.0.1.0             \
        -lsr_id                $p_lsr_id           \
        -label_space           0                   \
        -lsr_id_step           0.0.1.0             \
        -mac_address_init      $p_mac_address      \
        -gateway_ip_addr       $p_gateway_ip       \
        -gateway_ip_addr_step  0.0.1.0             \
        -reset                                     ]

if {[keylget ldp_routers_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_routers_status log]"
}

set ldp_handle [keylget ldp_routers_status handle]

#################################################
#  Configure ipv4_prefix fec type routes        #
#################################################
set ldp_routers_status [::ixia::emulation_ldp_route_config \
        -mode                   create              \
        -handle                 $ldp_handle         \
        -fec_type               ipv4_prefix         \
        -label_msg_type         mapping             \
        -fec_ip_prefix_start    $pe_ip_address      \
        -fec_ip_prefix_length   32                  \
        -egress_label_mode      imnull              ]

##################### End of LDP PE configuration ##################


#############################################
# Configure BGP Neighbor on PE port         #
#############################################
set bgp_router_status [::ixia::emulation_bgp_config       \
        -mode                            reset          \
        -port_handle                        $pe_port       \
        -local_ip_addr                   $p_ip_address  \
        -remote_ip_addr                  $p_gateway_ip  \
        -local_addr_step                 0.0.0.1        \
        -local_loopback_ip_addr          $pe_ip_address \
        -remote_loopback_ip_addr         $bgp_peer_ip   \
        -local_loopback_ip_addr_step     0.0.1.0        \
        -count                              1              \
        -mac_address_start               $p_mac_address \
        -local_router_id                 $bgp_router_id \
        -neighbor_type                   internal       \
        -ip_version                      4              \
        -local_as                        $bgp_as        \
        -local_as_mode                   fixed          \
        -active_connect_enable                          \
        -ipv4_unicast_nlri                              \
        -ipv4_mpls_vpn_nlri                             \
        -ipv6_mpls_nlri                                 ]

if {[keylget bgp_router_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_router_status log]"
}
set bgp_neighbor_handle [keylget bgp_router_status handles]

#############################################
# Configure L3 VPN Site on the BGP Neighbor #
#############################################
set bgp_route_range_status [::ixia::emulation_bgp_route_config \
        -mode                    add                       \
        -handle                  $bgp_neighbor_handle      \
        -ip_version              6                         \
        -prefix                  $pe_adv_network           \
        -prefix_step             1                         \
        -ipv6_prefix_length      $pe_adv_prefix_len        \
        -label_value             $pe_adv_label_start       \
        -num_sites               1                         \
        -num_routes              $pe_adv_num_routes        \
        -label_step              1                         \
        -local_pref              0                         \
        -next_hop_enable         1                         \
        -origin_route_enable                               \
        -enable_traditional_nlri 1                         \
        -ipv6_mpls_nlri                                    ]
if {[keylget bgp_route_range_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_route_range_status log]"
}
##################### End of iBGP PE configuration ##################



#############################################
# Configure ISIS router on CE port          #
#############################################
set isis_router_status [::ixia::emulation_isis_config         \
        -mode                           create              \
        -reset                                                       \
        -port_handle                    $ce_port            \
        -ip_version                     6                   \
        -intf_ipv6_addr                 $ce_ip_address      \
        -intf_ipv6_prefix_length        $ce_prefix_len      \
        -mac_address_init               $ce_mac_address     \
        -vlan_id                        $ce_vlan_id         \
        -count                                1                   \
        -intf_metric                    0                   \
        -routing_level                  L1L2                \
        -te_enable                      0                   \
        -te_router_id                   $isis_ce_router_id  ]
if {[keylget isis_router_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_router_status log]"
}

set isis_ce_router_handle [keylget isis_router_status handle]

###############################################
# Configure two route ranges on ISIS router   #
###############################################
set route_config_status [::ixia::emulation_isis_topology_route_config \
        -mode                   create                  \
        -handle                 $isis_ce_router_handle  \
        -type                   stub                    \
        -ip_version             6                       \
        -stub_ipv6_start        $c_network1             \
        -stub_ipv6_pfx_len      $c_prefix_len1          \
        -stub_count             $c_num_prefixes1        \
        -stub_metric            1                       \
        -stub_up_down_bit       0                       ]

if {[keylget route_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget route_config_status log]"
}
set route_config_status [::ixia::emulation_isis_topology_route_config \
        -mode                   create                  \
        -handle                 $isis_ce_router_handle  \
        -type                   stub                    \
        -ip_version             6                       \
        -stub_ipv6_start        $c_network2             \
        -stub_ipv6_pfx_len      $c_prefix_len2          \
        -stub_count             $c_num_prefixes2        \
        -stub_metric            1                       \
        -stub_up_down_bit       0                       ]

if {[keylget route_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget route_config_status log]"
}
##################### End of ISIS CE configuration ##################


######################
# START ISIS on      #
######################
set isis_emulation_status [::ixia::emulation_isis_control \
        -handle      $isis_router_handle                \
        -mode        start                              ]

if {[keylget isis_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_emulation_status log]"
}

######################
# START LDP on       #
######################
set ldp_emulation_status [::ixia::emulation_ldp_control \
        -handle $ldp_handle \
        -mode   start       ]

if {[keylget ldp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_emulation_status log]"
}

######################
# START ISIS (CE) on #
######################
set isis_emulation_status [::ixia::emulation_isis_control \
        -handle      $isis_ce_router_handle             \
        -mode        start                              ]

if {[keylget isis_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_emulation_status log]"
}

after 35000

######################
# START BGP on       #
######################
set bgp_emulation_status [::ixia::emulation_bgp_control \
        -port_handle $pe_port \
        -mode        start    ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}
# Set up the statistics after starting bgp protocol
set bgp_emulation_status [::ixia::emulation_bgp_control \
        -handle $bgp_neighbor_handle \
        -mode   statistic            ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}

after 30000

#############################################
# Create stream on CE ports                 #
#############################################
set traffic_status [::ixia::traffic_config   \
        -mode                reset           \
        -port_handle         $ce_port        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}
set traffic_status [::ixia::traffic_config   \
        -mode                create          \
        -port_handle         $ce_port        \
        -length_mode         random          \
        -l3_length_min       128             \
        -l3_length_max       1024            \
        -enable_pgid         1               \
        -pgid_value          1234            \
        -l3_protocol         ipv6            \
        -ipv6_src_addr       $c_network1     \
        -ipv6_src_mode       fixed           \
        -ipv6_dst_addr       $pe_adv_network \
        -ipv6_dst_mode       fixed           \
        -mac_dst_mode        discovery       \
        -vlan                enable          \
        -vlan_id             901             \
        -vlan_id_mode        fixed           ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

#############################################
# Start traffic on CE port                  #
#############################################
# Clear stats before sending traffic
set clear_stats_status [::ixia::traffic_control \
        -port_handle "$pe_port $ce_port"      \
        -action      clear_stats              ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget clear_stats_status log]"
}

set traffic_status [::ixia::traffic_control \
        -port_handle $ce_port               \
        -action sync_run                    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

after 40000

#############################################
# Stop traffic on CE port                   #
#############################################
set traffic_status [::ixia::traffic_control \
        -port_handle $ce_port               \
        -action stop                        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

after 5000

#############################################
# Print traffic stats                       #
#############################################
set ce_stats [::ixia::traffic_stats -port_handle $ce_port -mode aggregate]
if {[keylget ce_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ce_stats log]"
}

set ce_transmit [keylget ce_stats $ce_port.aggregate.tx.pkt_count]

set pe_stats [::ixia::traffic_stats -port_handle $pe_port -packet_group_id 1234]
if {[keylget pe_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pe_stats log]"
}

set pe_receive [keylget pe_stats $pe_port.pgid.rx.pkt_count.1234]

puts "                             Sent             Received"
puts "-------------------------------------------------------"
puts [format "Frames               %12s         %12s" \
        $ce_transmit $pe_receive]

