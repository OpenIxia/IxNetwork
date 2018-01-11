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
#    This sample creates a L3VPN setup. It uses two Ixia ports. One port is    #
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
#    P  runs LDP and OSPF                                                      #
#    CE runs eBGP                                                              #
#                                                                              #
#    Cisco configuration:                                                      #
#        mpls label protocol ldp
#
#        ip vrf vpn901
#        description vpn901
#        rd 901:1
#        route-target export 901:1
#        route-target import 901:1
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
#        ip vrf forwarding vpn901
#        ip address 100.27.0.1 255.255.255.0
#
#        interface GigabitEthernet1/30
#        description vpn901_pe
#        ip address 100.28.0.1 255.255.255.0
#        ip ospf network broadcast
#        mpls label protocol ldp
#        tag-switching ip
#
#        router ospf 901
#        mpls traffic-eng router-id Loopback901
#        mpls traffic-eng area 0
#        log-adjacency-changes
#        network 100.28.0.0 0.0.0.255 area 0
#
#        router bgp 1
#        neighbor 110.0.110.100 remote-as 1
#        neighbor 110.0.110.100 update-source Loopback901
#
#        address-family vpnv4
#        neighbor 110.0.110.100 activate
#        neighbor 110.0.110.100 send-community extended
#        exit-address-family
#
#        address-family ipv4 vrf vpn901
#        neighbor 100.27.0.2 remote-as 101
#        neighbor 100.27.0.2 activate
#        no auto-summary
#        no synchronization
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

set ce_ip_address    100.27.0.2
set ce_prefix_len    24
set ce_gateway_ip    100.27.0.1
set ce_vlan_id       901
set ce_mac_address   0000.0001.0002

set bgp_router_id    1.2.3.4
set bgp_as           1
set ospf_router_id   1.2.3.4
set ospf_area_id     0.0.0.0
set p_lsr_id         1.2.3.4

set rd_target_type   0
set rd_admin_value   901
set rd_assign_value  1
set vrf_target_type  "as"
set vrf_admin_value  901
set vrf_assign_value 1
set vrf_network      77.77.78.0
set vrf_prefix       255.255.255.0
set vrf_num_routes   2

set bgp_ce_router_id 5.6.7.8
set bgp_ce_as        101

set c_network1       67.67.68.0
set c_prefix1        255.255.255.0
set c_num_prefixes1  3

set c_network2       57.57.58.0
set c_prefix2        255.255.255.0
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
        -port_handle     "$pe_port $ce_port" \
        -autonegotiation 1                   \
        -transmit_mode   advanced            ]

#################################################
#  Configure OSPFv2 neighbor on P/PE port       #
#################################################
set ospf_neighbor_status [::ixia::emulation_ospf_config \
        -port_handle                $pe_port         \
        -reset                                       \
        -session_type               ospfv2           \
        -mode                       create           \
        -count                      1                \
        -mac_address_init           $p_mac_address   \
        -intf_ip_addr               $p_ip_address    \
        -intf_ip_addr_step          0.0.1.0          \
        -router_id                  $ospf_router_id  \
        -router_id_step             0.0.1.0          \
        -neighbor_intf_ip_addr      $p_gateway_ip    \
        -neighbor_intf_ip_addr_step 0.0.1.0          \
        -loopback_ip_addr           $pe_ip_address   \
        -loopback_ip_addr_step      0.0.1.0          \
        -area_id                    $ospf_area_id    \
        -area_id_step               0.0.0.1          \
        -area_type                  external-capable \
        -network_type               broadcast        ]

if {[keylget ospf_neighbor_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_neighbor_status log]"
}

set ospf_handle [keylget ospf_neighbor_status handle]
##################### End of OSPF PE configuration ##################


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
        -port_handle                     $pe_port       \
        -local_ip_addr                   $p_ip_address  \
        -remote_ip_addr                  $p_gateway_ip  \
        -local_addr_step                 0.0.0.1        \
        -local_loopback_ip_addr          $pe_ip_address \
        -remote_loopback_ip_addr         $bgp_peer_ip   \
        -local_loopback_ip_addr_step     0.0.1.0        \
        -count                           1              \
        -mac_address_start               $p_mac_address \
        -local_router_id                 $bgp_router_id \
        -neighbor_type                   internal       \
        -ip_version                      4              \
        -local_as                        $bgp_as        \
        -local_as_mode                   fixed          \
        -active_connect_enable                          \
        -ipv4_mpls_vpn_nlri                             ]
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
        -ip_version              4                         \
        -prefix                  $vrf_network              \
        -prefix_step             1                         \
        -netmask                 $vrf_prefix               \
        -label_value             55                        \
        -num_sites               1                         \
        -num_routes              $vrf_num_routes           \
        -label_step              1                         \
        -rd_type                 $rd_target_type           \
        -rd_admin_value          $rd_admin_value           \
        -rd_assign_value         $rd_assign_value          \
        -rd_admin_step           1                         \
        -rd_assign_step          1                         \
        -target_type             $vrf_target_type          \
        -target                  $vrf_admin_value          \
        -target_assign           $vrf_assign_value         \
        -import_target_type      $vrf_target_type          \
        -import_target           $vrf_admin_value          \
        -import_target_assign    $vrf_assign_value         \
        -local_pref              0                         \
        -next_hop_enable         1                         \
        -origin_route_enable                               \
        -enable_traditional_nlri 1                         \
        -ipv4_mpls_vpn_nlri                                ]
if {[keylget bgp_route_range_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_route_range_status log]"
}
##################### End of iBGP PE configuration ##################


#############################################
# Configure BGP Neighbor on CE port         #
#############################################
set bgp_router_status [::ixia::emulation_bgp_config          \
        -mode                            reset             \
        -port_handle                     $ce_port          \
        -local_ip_addr                   $ce_ip_address    \
        -remote_ip_addr                  $ce_gateway_ip    \
        -local_addr_step                 0.0.0.1           \
        -count                           1                 \
        -mac_address_start               $ce_mac_address   \
        -local_router_id                 $bgp_ce_router_id \
        -vlan_id                         $ce_vlan_id       \
        -neighbor_type                   external          \
        -ip_version                      4                 \
        -local_as                        $bgp_ce_as        \
        -local_as_mode                   fixed             \
        -active_connect_enable                             \
        -ipv4_unicast_nlri                                 ]
if {[keylget bgp_router_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_router_status log]"
}
set bgp_ce_neighbor_handle [keylget bgp_router_status handles]

#############################################
# Configure two route ranges on BGP neighbor#
#############################################
set bgp_route_range_status [::ixia::emulation_bgp_route_config \
        -mode                    add                       \
        -handle                  $bgp_ce_neighbor_handle   \
        -ip_version              4                         \
        -prefix                  $c_network1               \
        -prefix_step             1                         \
        -netmask                 $c_prefix1                \
        -num_sites               1                         \
        -num_routes              $c_num_prefixes1          \
        -next_hop_enable         1                         \
        -origin_route_enable                               \
        -enable_traditional_nlri 1                         \
        -ipv4_unicast_nlri                                 ]
if {[keylget bgp_route_range_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_route_range_status log]"
}

set bgp_route_range_status [::ixia::emulation_bgp_route_config \
        -mode                     add                       \
        -handle                   $bgp_ce_neighbor_handle   \
        -ip_version               4                         \
        -prefix                   $c_network2               \
        -prefix_step              1                         \
        -netmask                  $c_prefix2                \
        -num_sites                1                         \
        -num_routes               $c_num_prefixes2          \
        -next_hop_enable          1                         \
        -origin_route_enable                                \
        -enable_traditional_nlri  1                         \
        -ipv4_unicast_nlri                                  ]
if {[keylget bgp_route_range_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_route_range_status log]"
}
##################### End of eBGP CE configuration ##################


######################
# START OSPF on      #
######################
set ospf_emulation_status [::ixia::emulation_ospf_control \
        -handle $ospf_handle \
        -mode   start        ]
if {[keylget ospf_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_emulation_status log]"
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
# START BGP (CE) on  #
######################
set bgp_emulation_status [::ixia::emulation_bgp_control \
        -port_handle $ce_port \
        -mode        start    ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}
# Set up the statistics for the bgp port after the protocol is running
set bgp_emulation_status [::ixia::emulation_bgp_control \
        -handle $bgp_ce_neighbor_handle \
        -mode   statistic               ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}

######################
# START BGP (PE) on  #
######################
set bgp_emulation_status [::ixia::emulation_bgp_control \
        -port_handle $pe_port \
        -mode        start    ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}
# Set up the statistics for the bgp port after the protocol is running
set bgp_emulation_status [::ixia::emulation_bgp_control \
        -handle $bgp_neighbor_handle \
        -mode   statistic            ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}

# Just waiting an arbitrary 2 minutes for the routes to be learned.  More 
# specific looping could occur to read the values and see if they exist
after 120000

set done false
while {!$done} {
    set interface_status [::ixia::interface_config  \
            -port_handle     $pe_port               \
            -arp_send_req    1                      ]
    if {[keylget interface_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget interface_status log]"
    }
    puts "interface_status: $interface_status"

    if {[catch {set arp_request_success [keylget interface_status \
            $pe_port.arp_request_success]}] || $arp_request_success == 1} {
        set done true
    }
}

set done false
while {!$done} {
    set interface_status [::ixia::interface_config  \
            -port_handle     $ce_port               \
            -arp_send_req    1                      ]
    if {[keylget interface_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget interface_status log]"
    }
    puts "interface_status: $interface_status"

    if {[catch {set arp_request_success [keylget interface_status \
            $ce_port.arp_request_success]}] || $arp_request_success == 1} {
        set done true
    }
}

#############################################
# Generate traffic on PE and CE ports       #
#############################################
set stream_status [::ixia::l3vpn_generate_stream \
        -pe_port_handle      $pe_port \
        -ce_port_handle      $ce_port \
        -stream_generation   both     \
        -pe_label_protocol   ldp      \
        -ce_routing_protocol bgp      \
        -reset                        \
        -length_mode         random   \
        -l3_length_min       128      \
        -l3_length_max       1024     \
        -enable_pgid         1        \
        -pgid_value          1234     ]
if {[keylget stream_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget stream_status log]"
}

#############################################
# Start traffic on PE and CE ports          #
#############################################
# Clear stats before sending traffic
set clear_stats_status [::ixia::traffic_control \
        -port_handle "$pe_port $ce_port"      \
        -action      clear_stats              ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget clear_stats_status log]"
}

set traffic_status [::ixia::traffic_control \
        -port_handle "$pe_port $ce_port"    \
        -action sync_run                    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

# Run the traffic for 30 seconds
after 30000

#############################################
# Stop traffic on PE and CE ports           #
#############################################
set traffic_status [::ixia::traffic_control \
        -port_handle "$pe_port $ce_port"    \
        -action stop                        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

# Pause to let the traffic and statistics settle
after 5000

#############################################
# Print traffic stats                       #
#############################################
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

