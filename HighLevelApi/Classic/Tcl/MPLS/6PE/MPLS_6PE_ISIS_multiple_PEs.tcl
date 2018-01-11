################################################################################
# Version 1.0    $Revision: 1 $
#
#    Copyright © 1997 - 2006 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10/033/2006 LRaicea
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
#    P  runs LDP and ISISv4                                                    #
#    CE runs ISISv6                                                            #
#    DUT: Cisco 6500                                                           #
#    IOS: s72033-ipservicesk9-mz.122-18.SXF.bin                                #
#                                                                              #
# DUT configuration:                                                           #
#
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
#    ipv6 address 801::/64
#    ipv6 router isis 6pe_CEside
# 
#    interface GigabitEthernet9/40.802
#    description CE2
#    encapsulation dot1Q 802
#    ipv6 address 802::/64
#    ipv6 router isis 6pe_CEside
#    
#    interface GigabitEthernet9/40.803
#    description CE3
#    encapsulation dot1Q 803
#    ipv6 address 803::/64
#    ipv6 router isis 6pe_CEside
#    
#    interface GigabitEthernet9/39
#    description ToProvider
#    ip address 200.28.0.1 255.255.255.0
#    ip router isis 6pe_PEside
#    mpls label protocol ldp
#    tag-switching ip
#    no shutdown
#    
#    router isis 6pe_PEside
#    net 49.1111.1111.1111.1111.00
#    is-type level-1
#    metric-style transition
#    
#    router isis 6pe_CEside
#    net 50.1111.1111.1111.1111.00
#    is-type level-1
#    redistribute bgp 1 metric 20 level-1
#    metric-style transition
#    
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
#    redistribute isis 6pe_CEside level-1
#    exit-address-family
#    end
#
# Erase DUT configuration:
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
#                                                                                 #
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

set test_name             [info script]
set chassisIP             sylvester
set port_list             [list 4/1 4/2]

set pe_count               5
set pe_ip_addr             220.0.220.201
set pe_ip_addr_step        0.0.0.1
set pe_prefix_len          32
set pe_intf_addr           11.0.11.201
set pe_intf_addr_step      0.0.0.1
set pe_intf_mask           255.255.255.255
set pe_intf_prefix_len     32
set pe_gw_addr             220.0.220.1
set pe_gw_addr_step        0.0.0.0
set pe_as_number           1

set p_ip_addr              200.28.0.2
set p_ip_addr_step         0.0.0.0
set p_prefix_len           24
set p_gw_addr              200.28.0.1
set p_gw_addr_step         0.0.0.0
set p_isis_area_id         "49 11 11 11"
set p_isis_area_id_step    "00 00 00 00"
set p_isis_system_id       0x111111111200
set p_isis_system_id_step  0

set ce_count               3
set ce_ip_addr             801::801
set ce_ip_addr_step        1::1
set ce_prefix_len          64
set ce_vlan_id             801
set ce_vlan_id_step        1
set ce_isis_area_id        "50 11 11 11"
set ce_isis_area_id_step   "00 00 00 00"
set ce_isis_system_id      0x111111111200
set ce_isis_system_id_step 1

set pe_adv_label_start     31
set pe_adv_network         31::0
set pe_adv_prefix_len      64
set pe_adv_network_step    1::0
set pe_adv_num_routes      2

set c_network1             41::0
set c_network1_step        1::0
set c_prefix_len1          64
set c_num_prefixes1        3

set c_network2             51::0
set c_network2_step        1::0
set c_prefix_len2          64
set c_num_prefixes2        2

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
# Configure ISIS P and PEs
################################################################################
set isis_router_status [::ixia::emulation_isis_config             \
        -mode                           create                  \
        -reset                                                           \
        -port_handle                    $pe_port                \
        -intf_ip_addr                   $p_ip_addr              \
        -intf_ip_addr_step              $p_ip_addr_step         \
        -gateway_ip_addr                $p_gw_addr              \
        -gateway_ip_addr_step           $p_gw_addr_step         \
        -intf_ip_prefix_length          $p_prefix_len           \
        -count                                1                       \
        -intf_metric                    0                       \
        -routing_level                  L1                      \
        -te_enable                      0                       \
        -area_id                        $p_isis_area_id         \
        -area_id_step                   $p_isis_area_id_step    \
        -system_id                      $p_isis_system_id       \
        -system_id_step                 $p_isis_system_id_step  \
        ]

if {[keylget isis_router_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_router_status log]"
}
puts "1: Created ISIS Provider neighbor"
set p_isis_handle     [keylget isis_router_status handle]
set pe_ip_addr_temp   $pe_ip_addr
set pe_intf_addr_temp $pe_intf_addr
for {set i 1} {$i <= $pe_count} {incr i} {
    set route_config_status [::ixia::emulation_isis_topology_route_config \
            -mode                    create                   \
            -handle                  $p_isis_handle           \
            -type                    grid                     \
            -ip_version              4                        \
            -grid_start_system_id    111111111[expr $i + 2]00 \
            -grid_system_id_step     000000000001             \
            -grid_user_wide_metric   0                        \
            -grid_row                1                        \
            -grid_col                1                        \
            -grid_ip_start           $pe_intf_addr_temp       \
            -grid_ip_step            $pe_intf_addr_step       \
            -grid_ip_pfx_len         $pe_intf_prefix_len      \
            -grid_connect            1 1                      \
            -grid_interface_metric   1                        \
            -grid_link_type          ptop                     \
            -grid_stub_per_router    1                        \
            -grid_router_id          $pe_ip_addr_temp         \
            -grid_router_id_step     $pe_ip_addr_step         \
            -grid_router_ip_pfx_len  $pe_prefix_len           \
            -grid_router_metric      0                        \
            -grid_router_up_down_bit 0                        \
            -grid_router_origin      stub                     \
            -grid_te                 0                        \
            ]
    
    if {[keylget route_config_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget route_config_status log]"
    }
    
    set pe_ip_addr_temp   [script_increment_ipv4_address \
            $pe_ip_addr_temp    $pe_ip_addr_step]
    
    set pe_intf_addr_temp [script_increment_ipv4_address \
            $pe_intf_addr_temp  $pe_intf_addr_step]
}
puts "2: Created ISIS PE neighbors"
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
puts "3: Created LDP Provider"
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
puts "4: Created LDP PEs"
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
puts "5: Created BGP PEs"
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
    
    set  pe_adv_network_temp [script_increment_ipv6_address \
            $pe_adv_network_temp $pe_adv_network_step]
    
    incr pe_adv_label_start_temp $pe_adv_num_routes
}
puts "6: Created BGP MPLS routes"
################################################################################
# Configure ISIS CE neighbors
################################################################################
set isis_router_status [::ixia::emulation_isis_config              \
        -mode                           create                   \
        -reset                                                            \
        -port_handle                    $ce_port                 \
        -count                                $ce_count                \
        -ip_version                     6                        \
        -intf_ipv6_addr                 $ce_ip_addr              \
        -intf_ipv6_addr_step            $ce_ip_addr_step         \
        -intf_ipv6_prefix_length        $ce_prefix_len           \
        -intf_metric                    0                        \
        -vlan_id                        $ce_vlan_id              \
        -vlan_id_step                   $ce_vlan_id_step         \
        -routing_level                  L1                       \
        -te_enable                      0                        \
        -area_id                        $ce_isis_area_id         \
        -area_id_step                   $ce_isis_area_id_step    \
        -system_id                      $ce_isis_system_id       \
        -system_id_step                 $ce_isis_system_id_step  ]


if {[keylget isis_router_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_router_status log]"
}
puts "7: Created ISIS CEs"
set isis_ce_handles [keylget isis_router_status handle]

################################################################################
# Configure two route ranges on each ISIS CE neighbor
################################################################################
set c_network1_temp $c_network1
set c_network2_temp $c_network2
foreach {isis_ce_handle} $isis_ce_handles {
    set route_config_status [::ixia::emulation_isis_topology_route_config \
            -mode                   create                  \
            -handle                 $isis_ce_handle         \
            -type                   stub                    \
            -ip_version             6                       \
            -stub_ipv6_start        $c_network1_temp        \
            -stub_ipv6_pfx_len      $c_prefix_len1          \
            -stub_count             $c_num_prefixes1        \
            -stub_metric            1                       \
            -stub_up_down_bit       0                       ]
    
    if {[keylget route_config_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget route_config_status log]"
    }
    set c_network1_temp [script_increment_ipv6_address \
            $c_network1_temp $c_network1_step]
    
    set route_config_status [::ixia::emulation_isis_topology_route_config \
            -mode                   create                  \
            -handle                 $isis_ce_handle         \
            -type                   stub                    \
            -ip_version             6                       \
            -stub_ipv6_start        $c_network2_temp        \
            -stub_ipv6_pfx_len      $c_prefix_len2          \
            -stub_count             $c_num_prefixes2        \
            -stub_metric            1                       \
            -stub_up_down_bit       0                       ]
    
    if {[keylget route_config_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget route_config_status log]"
    }
    set c_network2_temp [script_increment_ipv6_address \
            $c_network2_temp $c_network2_step]
}
puts "8: Created ISIS routes"
################################################################################
# START ISIS
################################################################################
set isis_emulation_status [::ixia::emulation_isis_control \
        -handle      $p_isis_handle \
        -mode        start          ]

if {[keylget isis_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_emulation_status log]"
}

set isis_emulation_status [::ixia::emulation_isis_control \
        -handle      $isis_ce_handle \
        -mode        start           ]

if {[keylget isis_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_emulation_status log]"
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
# Create streams on CE port
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


################################################################################
# Stop traffic on CE port
################################################################################
set traffic_status [::ixia::traffic_control \
        -port_handle $ce_port               \
        -action      stop                   ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

after 5000

################################################################################
# Print traffic stats
################################################################################
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
