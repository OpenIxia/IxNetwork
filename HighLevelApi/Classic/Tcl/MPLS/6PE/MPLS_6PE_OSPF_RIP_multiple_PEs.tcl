################################################################################
# Version 1.0    $Revision: 1 $
#
#    Copyright © 1997 - 2006 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10/02/2006 LRaicea
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
#    used for PEs and P router. The other port is used for CE routers.         #
#    Streams are created on CE port and then traffic is started.               #
#    At the end statistics are retrieved.                                      #
#                                                                              #
#         ------       -----           -----          ------                   #
#        |  PEs |-----|  P  |---------| DUT |--------|  CEs |                  #
#         ------       -----     |     -----     |    ------                   #
#                                |               |                             #
#               Ixia port 1      |  Cisco 6500   |    Ixia port 2              #
#                                                                              #
#    PE runs mBGP                                                              #
#    P  runs LDP and OSPF                                                      #
#    CE runs RIPng                                                             #
#    DUT: Cisco 6500                                                           #
#    IOS: s72033-ipservicesk9-mz.122-18.SXF.bin                                #
#                                                                              #
# DUT configuration:                                                           #
#    ipv6 unicast-routing
#    ipv6 cef distributed
#
#    mpls label protocol ldp
#    mpls ipv6 source-interface Loopback220
#
#    interface Loopback220
#    ip address 220.0.220.1 255.255.255.255
#
#    interface GigabitEthernet9/40
#    no ip address
#    no shutdown
#
#    interface GigabitEthernet9/40.801
#    description CE1
#    encapsulation dot1Q 801
#    ipv6 address 801::1/64
#    ipv6 rip vpn6pe enable
#    ipv6 rip vpn6pe default-information originate
#
#    interface GigabitEthernet9/40.802
#    description CE2
#    encapsulation dot1Q 802
#    ipv6 address 802::1/64
#    ipv6 rip vpn6pe enable
#    ipv6 rip vpn6pe default-information originate
#
#    interface GigabitEthernet9/40.803
#    description CE3
#    encapsulation dot1Q 803
#    ipv6 address 803::1/64
#    ipv6 rip vpn6pe enable
#    ipv6 rip vpn6pe default-information originate
#
#    interface GigabitEthernet9/39
#    description ToProvider
#    ip address 200.28.0.1 255.255.255.0
#    ip ospf network broadcast
#    mpls label protocol ldp
#    tag-switching ip
#    no shutdown
#
#    router ospf 220
#    mpls traffic-eng router-id Loopback220
#    mpls traffic-eng area 0
#    log-adjacency-changes
#    network 200.28.0.0 0.0.0.255 area 0
#
#    ipv6 router rip vpn6pe
#    maximum-paths 1
#    no split-horizon
#    poison-reverse
# 
#    router bgp 1
#    neighbor 220.0.220.201 remote-as 1
#    neighbor 220.0.220.201 update-source Loopback220
#    neighbor 220.0.220.202 remote-as 1
#    neighbor 220.0.220.202 update-source Loopback220
#    neighbor 220.0.220.203 remote-as 1
#    neighbor 220.0.220.203 update-source Loopback220
#    neighbor 220.0.220.204 remote-as 1
#    neighbor 220.0.220.204 update-source Loopback220
#    neighbor 220.0.220.205 remote-as 1
#    neighbor 220.0.220.205 update-source Loopback220
#
#    address-family ipv6
#    neighbor 220.0.220.201 activate
#    neighbor 220.0.220.201 send-label
#    neighbor 220.0.220.202 activate
#    neighbor 220.0.220.202 send-label
#    neighbor 220.0.220.203 activate
#    neighbor 220.0.220.203 send-label
#    neighbor 220.0.220.204 activate
#    neighbor 220.0.220.204 send-label
#    neighbor 220.0.220.205 activate
#    neighbor 220.0.220.205 send-label
#    redistribute rip vpn6pe
#    exit-address-family
#    end
#
# Erase DUT config:
#    
#    no ipv6 cef distributed
#    no ipv6 unicast-routing
#    
#    no mpls label protocol ldp
#    no mpls ipv6 source-interface Loopback220
#    
#    no interface Loopback220
#    default interface GigabitEthernet9/40
#    no interface GigabitEthernet9/40.801
#    no interface GigabitEthernet9/40.802
#    no interface GigabitEthernet9/40.803
#    default interface GigabitEthernet9/39
#    no router ospf 220
#    no ipv6 router rip vpn6pe
#    no router bgp 1
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#                                                                              #
################################################################################

proc script_increment_ipv6_address {prefix step} {
    set segments    8
    # Expand prefix
    set segmentsBefore {}
    set segmentsAfter   $prefix
    regexp {(.*)::(.*)} $prefix result segmentsBefore segmentsAfter
    set segmentsBefore [split $segmentsBefore :]
    set segmentsAfter  [split $segmentsAfter  :]
    set segmentsNeeded [expr  $segments - \
            ([llength $segmentsBefore] + \
            [llength $segmentsAfter])]
    
    set segmentListPrefix "$segmentsBefore\
            [string repeat " 0" $segmentsNeeded] $segmentsAfter"
    
    set expandedPrefix [list]
    foreach segment $segmentListPrefix {
        lappend expandedPrefix [format "%04x" 0x$segment]
    }
    set expandedPrefix 0x[join $expandedPrefix ""]
    
    # Expand step
    set segmentsBefore {}
    set segmentsAfter   $step
    regexp {(.*)::(.*)} $step result segmentsBefore segmentsAfter
    set segmentsBefore [split $segmentsBefore :]
    set segmentsAfter  [split $segmentsAfter  :]
    set segmentsNeeded [expr  $segments - \
            ([llength $segmentsBefore] + \
            [llength $segmentsAfter])]
    
    set segmentListStep "$segmentsBefore\
            [string repeat " 0" $segmentsNeeded] $segmentsAfter"
    
    set expandedStep [list]
    foreach segment $segmentListStep {
        lappend expandedStep [format "%04x" 0x$segment]
    }
    set expandedStep 0x[join $expandedStep ""]
    
    
    set val [mpexpr $expandedPrefix + $expandedStep]
    set width $segments
    set retVal {}
    while {$width} {
        set retVal [linsert $retVal 0 [format "%04x" [mpexpr $val & 65535]]]
        incr width -1
        set val [mpexpr $val >> 16]
    }
    return [join $retVal :]
}

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

package require Ixia

set test_name           [info script]
set chassisIP           sylvester
set port_list           [list 4/1 4/2]

set pe_count            5
set pe_ip_addr          220.0.220.201
set pe_ip_addr_step     0.0.0.1
set pe_prefix_len       32
set pe_intf_addr        11.0.11.201
set pe_intf_addr_step   0.0.0.1
set pe_intf_mask        255.255.255.255
set pe_gw_addr          220.0.220.1
set pe_gw_addr_step     0.0.0.0
set pe_as_number        1

set p_ip_addr           200.28.0.2
set p_ip_addr_step      0.0.0.0
set p_prefix_len        24
set p_gw_addr           200.28.0.1
set p_gw_addr_step      0.0.0.0
set p_ospf_area_id      0.0.0.0
set p_ospf_area_id_step 0.0.0.0

set ce_count            3
set ce_ip_addr          801::801
set ce_ip_addr_step     1::1
set ce_prefix_len       64
set ce_vlan_id          801
set ce_vlan_id_step     1

set pe_adv_label_start  31
set pe_adv_network      31::0
set pe_adv_prefix_len   64
set pe_adv_network_step 1::0
set pe_adv_num_routes   2

set c_network1          41::0
set c_network1_step     1::0
set c_prefix_len1       64
set c_num_prefixes1     3

set c_network2          51::0
set c_network2_step     1::0
set c_prefix_len2       64
set c_num_prefixes2     2

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
        -signature_offset 70                 \
        -pgid_offset      74                 ]

set intf_status [::ixia::interface_config    \
        -port_handle      $ce_port           \
        -autonegotiation  1                  \
        -transmit_mode    advanced           ]
        

################################################################################
# Configure OSPFv2 P and PEs
################################################################################
set ospf_neighbor_status [::ixia::emulation_ospf_config    \
        -port_handle                $pe_port             \
        -reset                                           \
        -session_type               ospfv2               \
        -mode                       create               \
        -count                      1                    \
        -intf_ip_addr               $p_ip_addr           \
        -intf_ip_addr_step          $p_ip_addr_step      \
        -router_id                  $p_ip_addr           \
        -router_id_step             $p_ip_addr_step      \
        -neighbor_intf_ip_addr      $p_gw_addr           \
        -neighbor_intf_ip_addr_step $p_gw_addr_step      \
        -area_id                    $p_ospf_area_id      \
        -area_id_step               $p_ospf_area_id_step \
        -area_type                  external-capable     \
        -network_type               broadcast            ]

if {[keylget ospf_neighbor_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_neighbor_status log]"
}

set p_ospf_handle           [keylget ospf_neighbor_status handle]
set pe_ip_addr_temp         $pe_ip_addr
set pe_intf_addr_temp       $pe_intf_addr
for {set i 0} {$i < $pe_count} {incr i} {
    set route_config_status [::ixia::emulation_ospf_topology_route_config\
            -mode                   create                   \
            -handle                 $p_ospf_handle           \
            -type                   grid                     \
            -grid_router_id         $pe_ip_addr_temp         \
            -grid_router_id_step    $pe_ip_addr_step         \
            -grid_row               1                        \
            -grid_col               1                        \
            -grid_link_type         ptop_numbered            \
            -grid_prefix_start      $pe_ip_addr_temp         \
            -grid_prefix_length     $pe_prefix_len           \
            -grid_prefix_step       $pe_ip_addr_step         \
            -grid_te                0                        \
            -grid_connect           1 1                      \
            -interface_ip_address   $pe_intf_addr_temp       \
            -interface_ip_mask      $pe_intf_mask            \
            -enable_advertise       1                        \
            ]
    
    if {[keylget route_config_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget route_config_status log]"
    }
    set pe_ip_addr_temp         [script_increment_ipv4_address \
            $pe_ip_addr_temp   $pe_ip_addr_step]
    
    set pe_intf_addr_temp [script_increment_ipv4_address \
            $pe_intf_addr_temp $pe_intf_addr_step]
}

################################################################################
# Configure LDP P and PEs
################################################################################
set ldp_routers_status [::ixia::emulation_ldp_config \
        -mode                  create              \
        -port_handle           $pe_port            \
        -label_adv             unsolicited         \
        -peer_discovery        link                \
        -count                 1                   \
        -intf_ip_addr          $p_ip_addr          \
        -intf_prefix_length    $p_prefix_len       \
        -intf_ip_addr_step     $p_ip_addr_step     \
        -lsr_id                $p_ip_addr          \
        -lsr_id_step           $p_ip_addr_step     \
        -label_space           0                   \
        -gateway_ip_addr       $p_gw_addr          \
        -gateway_ip_addr_step  $p_gw_addr_step     \
        -reset                                     ]

if {[keylget ldp_routers_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_routers_status log]"
}

set p_ldp_handle    [keylget ldp_routers_status handle]
set pe_ip_addr_temp $pe_ip_addr
for {set i 0} {$i < $pe_count} {incr i} {
    set ldp_routers_status [::ixia::emulation_ldp_route_config \
            -mode                   create              \
            -handle                 $p_ldp_handle       \
            -fec_type               ipv4_prefix         \
            -label_msg_type         mapping             \
            -fec_ip_prefix_start    $pe_ip_addr_temp    \
            -fec_ip_prefix_length   $pe_prefix_len      \
            -egress_label_mode      imnull              ]
    
    set pe_ip_addr_temp      [script_increment_ipv4_address \
            $pe_ip_addr_temp $pe_ip_addr_step]
}

################################################################################
# Configure BGP P and PEs 
################################################################################
set bgp_router_status [::ixia::emulation_bgp_config         \
        -mode                            reset            \
        -port_handle                        $pe_port         \
        -local_ip_addr                   $p_ip_addr       \
        -local_addr_step                 $p_ip_addr_step  \
        -remote_ip_addr                  $p_gw_addr       \
        -remote_addr_step                $p_gw_addr_step  \
        -local_loopback_ip_addr          $pe_ip_addr      \
        -local_loopback_ip_addr_step     $pe_ip_addr_step \
        -remote_loopback_ip_addr         $pe_gw_addr      \
        -remote_loopback_ip_addr_step    $pe_gw_addr_step \
        -local_router_id                 $pe_ip_addr      \
        -local_router_id_step            $pe_ip_addr_step \
        -count                              $pe_count        \
        -neighbor_type                   internal         \
        -ip_version                      4                \
        -local_as                        $pe_as_number    \
        -local_as_mode                   fixed            \
        -active_connect_enable                            \
        -ipv4_unicast_nlri                                \
        -ipv4_mpls_vpn_nlri                               \
        -ipv6_mpls_nlri                                   ]

if {[keylget bgp_router_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_router_status log]"
}
set bgp_neighbor_handles    [keylget bgp_router_status handles]
set pe_adv_network_temp     $pe_adv_network
set pe_adv_label_start_temp $pe_adv_label_start
foreach {bgp_neighbor_handle} $bgp_neighbor_handles {
    set bgp_route_range_status [::ixia::emulation_bgp_route_config \
            -mode                    add                       \
            -handle                  $bgp_neighbor_handle      \
            -ip_version              6                         \
            -prefix                  $pe_adv_network_temp      \
            -prefix_step             1                         \
            -ipv6_prefix_length      $pe_adv_prefix_len        \
            -label_value             $pe_adv_label_start_temp  \
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
    
    set pe_adv_network_temp [script_increment_ipv6_address \
            $pe_adv_network_temp $pe_adv_network_step]
    
    incr pe_adv_label_start_temp $pe_adv_num_routes
}



################################################################################
# Configure RIPng Neighbor on CE port
################################################################################
set rip_status [::ixia::emulation_rip_config            \
        -port_handle                 $ce_port         \
        -mode                        create           \
        -reset                                        \
        -session_type                ripng            \
        -intf_ip_addr                $ce_ip_addr      \
        -intf_ip_addr_step           $ce_ip_addr_step \
        -intf_prefix_length          $ce_prefix_len   \
        -receive_type                store            \
        -count                       $ce_count        \
        -vlan_id                     $ce_vlan_id      \
        -vlan_id_step                $ce_vlan_id_step \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

set rip_router_handles [keylget rip_status handle]
set c_network1_temp $c_network1
set c_network2_temp $c_network2
foreach {rip_router_handle} $rip_router_handles {
    set rip_status [::ixia::emulation_rip_route_config             \
            -handle                      $rip_router_handle      \
            -mode                        create                  \
            -reset                                               \
            -num_prefixes                $c_num_prefixes1        \
            -prefix_start                $c_network1_temp        \
            -prefix_length               $c_prefix_len1          ]
    
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    
    set rip_status [::ixia::emulation_rip_route_config             \
            -handle                      $rip_router_handle      \
            -mode                        create                  \
            -num_prefixes                $c_num_prefixes2        \
            -prefix_start                $c_network2_temp        \
            -prefix_length               $c_prefix_len2          ]
    
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    
    set c_network1_temp [script_increment_ipv6_address \
            $c_network1_temp $c_network1_step]
    
    set c_network2_temp [script_increment_ipv6_address \
            $c_network2_temp $c_network2_step]
}


################################################################################
# START OSPF
################################################################################
set ospf_emulation_status [::ixia::emulation_ospf_control \
        -handle      $p_ospf_handle \
        -mode        start          ]

if {[keylget ospf_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_emulation_status log]"
}


################################################################################
# START LDP
################################################################################
set ldp_emulation_status [::ixia::emulation_ldp_control \
        -port_handle $pe_port \
        -mode        start    ]

if {[keylget ldp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_emulation_status log]"
}


################################################################################
# START RIPng
################################################################################
set rip_emulation_status [::ixia::emulation_rip_control \
        -port_handle $ce_port           \
        -mode        start              ]

if {[keylget rip_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ripemulation_status log]"
}

after 40000


################################################################################
# START BGP
################################################################################
set bgp_emulation_status [::ixia::emulation_bgp_control \
        -port_handle $pe_port \
        -mode        start    ]

if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}

# Set up the statistics after starting the bgp protocol
set bgp_emulation_status [::ixia::emulation_bgp_control \
        -handle      $bgp_neighbor_handle \
        -mode        statistic            ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}

after 30000


################################################################################
# Create stream on CE ports
################################################################################
set traffic_status [::ixia::traffic_config   \
        -mode                reset           \
        -port_handle         $ce_port        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

set pe_adv_network_temp     $pe_adv_network
for {set i 0} {$i < $pe_count} {incr i} {
    set c_network1_temp $c_network1
    set c_network2_temp $c_network2
    set ce_vlan_id_temp $ce_vlan_id
    for {set j 0} {$j < $ce_count} {incr j} {
        set traffic_status [::ixia::traffic_config         \
                -mode                create                \
                -port_handle         $ce_port              \
                -rate_percent        1                     \
                -length_mode         random                \
                -l3_length_min       128                   \
                -l3_length_max       512                   \
                -enable_pgid         1                     \
                -pgid_value          1234                  \
                -signature_offset    70                    \
                -l3_protocol         ipv6                  \
                -ipv6_src_addr       $c_network1_temp      \
                -ipv6_src_mode       fixed                 \
                -ipv6_dst_addr       $pe_adv_network_temp  \
                -ipv6_dst_mode       fixed                 \
                -mac_dst_mode        discovery             \
                -vlan                enable                \
                -vlan_id             $ce_vlan_id_temp      \
                -vlan_id_mode        fixed                 ]
        
        if {[keylget traffic_status status] != $::SUCCESS} {
            return "FAIL - $test_name - [keylget traffic_status log]"
        }
        
        set traffic_status [::ixia::traffic_config         \
                -mode                create                \
                -port_handle         $ce_port              \
                -rate_percent        1                     \
                -length_mode         random                \
                -l3_length_min       128                   \
                -l3_length_max       512                   \
                -enable_pgid         1                     \
                -pgid_value          1234                  \
                -signature_offset    70                    \
                -l3_protocol         ipv6                  \
                -ipv6_src_addr       $c_network2_temp      \
                -ipv6_src_mode       fixed                 \
                -ipv6_dst_addr       $pe_adv_network_temp  \
                -ipv6_dst_mode       fixed                 \
                -mac_dst_mode        discovery             \
                -vlan                enable                \
                -vlan_id             $ce_vlan_id_temp      \
                -vlan_id_mode        fixed                 ]
        
        if {[keylget traffic_status status] != $::SUCCESS} {
            return "FAIL - $test_name - [keylget traffic_status log]"
        }
        
        set c_network1_temp [script_increment_ipv6_address \
                $c_network1_temp $c_network1_step]
        
        set c_network2_temp [script_increment_ipv6_address \
                $c_network2_temp $c_network2_step]
        
        incr ce_vlan_id_temp $ce_vlan_id_step
    }
    set pe_adv_network_temp [script_increment_ipv6_address \
            $pe_adv_network_temp $pe_adv_network_step]
}



################################################################################
# Start traffic on CE port
################################################################################
# Clear stats before sending traffic
set clear_stats_status [::ixia::traffic_control \
        -port_handle "$pe_port $ce_port"      \
        -action      clear_stats              ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget clear_stats_status log]"
}

set traffic_status [::ixia::traffic_control \
        -port_handle $ce_port               \
        -action      sync_run               ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

after 40000

#############################################
# Stop traffic on CE port                   #
#############################################
set traffic_status [::ixia::traffic_control \
        -port_handle $ce_port               \
        -action      stop                   ]
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

return "SUCCESS - $test_name - [clock format [clock seconds]]"
