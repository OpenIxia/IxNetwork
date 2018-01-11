################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    20/01/2015 - Subhradip Pramanik - created sample                          #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF LDP API.               #
#                                                                              #
#    About Topology:                                                           #
#         Within topology both Provider Edge(PE) and Provider(P) Routers       #
#     are created. P router is emulated in the front Device Group(DG), which   #
#    consists of both OSPF as routing protocol as well as Basic LDP sessions   #
#     for Transport Label Distribution Protocol. The chained DG act as PE      #
#     Router, where LDP Extended Martini is configured for VPN Label           #
#     distribution protocol. Bidirectional L2-L3 Traffic is configured in      #
#    between two CE cloud and L4-L7 AppLib Traffic are created.                #
#     Script Flow:                                                             #
#     1. Configuration of protocols.                                           #
#    Configuration flow of the script is as follow:                            #
#         i.    Adding of OSPF router.                                         #
#         ii.   Adding of Network Cloud.                                       #
#         iii.  Adding of chain DG.                                            #
#         iv.   Adding of LDP(basic session) on Front DG                       #
#         v.    Adding of LDP Extended Martini(Targeted sess.) over chained DG.#
#         vi.   Adding of LDP PW/VPLS Tunnel over LDP Extended Martini.        #
#    2. Start the LDP protocol.                                                #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Changing Label in one side of VPN Ranges & apply change on the fly     #
#    6. Retrieve protocol learned info again and notice the difference with    #
#       previously retrieved learned info.                                     #
#    7. Configure L2-L3 traffic.                                               #
#    8. Start the L2-L3 traffic.                                               #
#    9. Retrieve L2-L3 traffic stats.                                          #
#   10. Stop L2-L3 traffic.                                                    #
#   11. Stop all protocols.                                                    #
# Ixia Software :                                                              #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################

################################################################################
# Utilities                                                                    #
################################################################################
if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

# End Utilities ################################################################

################################################################################
# Connection to the chassis, IxNetwork Tcl Server                              #
################################################################################
set chassis_ip        {10.216.102.209}
set tcl_server        10.216.102.209
set port_list         {1/3 1/4}
set ixNetwork_client  "10.216.108.49:8999"
set test_name         [info script]
puts "Connecting to chassis and client..."
set connect_status [::ixiangpf::connect       \
    -reset                   1                \
    -device                  $chassis_ip      \
    -port_list               $port_list       \
    -ixnetwork_tcl_server    $ixNetwork_client\
    -tcl_server              $tcl_server      \
]
if {0} {
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}
}
# Connecting to Chassis
puts "End connecting to chassis ..."

# Retrieving port handles, for later use
set port1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]

################################################################################
# Creating topology and device group                                           #
################################################################################
# Creating a topology on first port
puts "Adding topology 1 on port 1"

set topology_1_status [::ixiangpf::topology_config              \
    -topology_name      {Topology for FEC128 1}                 \
    -port_handle        "$port1"                                \
]
if {[keylget topology_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget topology_1_status log]"
        return 0
    }
set topology_1_handle [keylget topology_1_status topology_handle]
# Creating a device group in topology 1
puts "Creating device group in 1st port"
set device_group_1_status [::ixiangpf::topology_config     \
    -topology_handle              $topology_1_handle       \
    -device_group_name            {Provider Router 1}      \
    -device_group_multiplier      1                        \
    -device_group_enabled         1                        \
]
if {[keylget device_group_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget device_group_1_status log]"
        return 0
}
set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]
# Creating a topology on 2nd port
puts "Adding topology 1 on port 1"
set topology_2_status [::ixiangpf::topology_config              \
    -topology_name      {Topology for FEC128 1}                 \
    -port_handle        "$port2"                                \
]
if {[keylget topology_2_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget topology_2_status log]"
        return 0
    }
set topology_2_handle [keylget topology_2_status topology_handle]
# Creating a device group in topology 2
puts "Creating device group in second port"
set device_group_2_status [::ixiangpf::topology_config     \
    -topology_handle              $topology_2_handle       \
    -device_group_name            {Provider Router 2}      \
    -device_group_multiplier      1                        \
    -device_group_enabled         1                        \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget device_group_2_status log]"
        return 0
}
set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]
# Creating ethernet stack for the first Device Group
puts "creating ethernet stack within Device Group 1"
set ethernet_1_status [::ixiangpf::interface_config          \
    -protocol_name                {Ethernet 1}               \
    -protocol_handle              $deviceGroup_1_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 18.03.73.c7.6c.b1          \
]

if {[keylget ethernet_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ethernet_1_status log]"
        return 0
}

set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]
# Creating ethernet stack for the second Device Group
puts "creating ethernet stack within Device Group 2"
set ethernet_2_status [::ixiangpf::interface_config          \
    -protocol_name                {Ethernet 2}               \
    -protocol_handle              $deviceGroup_2_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 18.03.73.c7.6c.01          \
]

if {[keylget ethernet_2_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ethernet_2_status log]"
        return 0
}
set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]

# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group                                 
puts "Creating IPv4 Stack on top of Ethernet Stack for the first Device Group"  
set ipv4_1_status [::ixiangpf::interface_config                \
    -protocol_name                     {IPv4 1}                \
    -protocol_handle                   $ethernet_1_handle      \
    -ipv4_resolve_gateway              1                       \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01       \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00       \
    -gateway                           20.20.20.1              \
    -intf_ip_addr                      20.20.20.2              \
    -netmask                           255.255.255.0           \
    ]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ipv4_1_status log]"
        return 0
}
set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]
# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group                                 
puts "Creating IPv4 Stack on top of Ethernet Stack for the second Device Group"  
set ipv4_2_status [::ixiangpf::interface_config                \
    -protocol_name                     {IPv4 1}                \
    -protocol_handle                   $ethernet_2_handle      \
    -ipv4_resolve_gateway              1                       \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01       \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00       \
    -gateway                           20.20.20.2              \
    -intf_ip_addr                      20.20.20.1              \
    -netmask                           255.255.255.0           \
    ]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ipv4_1_status log]"
        return 0
}
set ipv4_2_handle [keylget ipv4_2_status ipv4_handle]

################################################################################
# Other protocol configurations                                                # 
################################################################################
# This will create OSPFv2 on top of IP within Topology 1 
puts "Creating OSPFv2 on top of IPv4 1 stack"
set ospfv2_1_status [::ixiangpf::emulation_ospf_config                                   \
    -handle                                                    $ipv4_1_handle            \
    -mode                                                      create                    \
    -network_type                                              ptop                      \
    -protocol_name                                             {OSPFv2-IF 1}             \
    -router_id                                                 193.0.0.1                 \
]
if {[keylget ospfv2_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ospfv2_1_status log]"
        return 0
}
# This will create OSPFv2 on top of IP within Topology 2 
puts "Creating OSPFv2 on top of IPv4 2 stack"
set ospfv2_2_status [::ixiangpf::emulation_ospf_config                                   \
    -handle                                                    $ipv4_2_handle            \
    -mode                                                      create                    \
    -network_type                                              ptop                      \
    -protocol_name                                             {OSPFv2-IF 2}             \
    -router_id                                                 194.0.0.1                 \
]

if {[keylget ospfv2_2_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ospfv2_2_status log]"
        return 0
}

# This will create LDP Router and interface over IP for the 1st Device Group  with lsr_id="193.0.0.1".
puts "Creating LDP Router Stack on top of IPv4 1 stack"
set ldp_basic_router_1_status [::ixiangpf::emulation_ldp_config \
    -handle                       $ipv4_1_handle                \
    -mode                         create                        \
    -lsr_id                       193.0.0.1                     \
    -interface_name               {LDP-IF 1}                    \
    -router_name                  {LDP 1}                       \
]
if {[keylget ldp_basic_router_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ldp_basic_router_1_status log]"
        return 0
}
set ldpBasicRouter_1_handle [keylget ldp_basic_router_1_status ldp_basic_router_handle]
# Creating LDP Interface Stack on top of IPv4 1 stack for first device Group
puts "Creating LDP Interface Stack on top of IPv4 1 stack" 
set ldp_connected_interface_1_status [::ixiangpf::emulation_ldp_config \
    -handle                    $ipv4_1_handle                          \
    -mode                      create                                  \
    -interface_name            {LDP-IF 1}                              \
]
if {[keylget ldp_connected_interface_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ldp_connected_interface_1_status log]"
        return 0
}
set ldpConnectedInterface_1_handle [keylget ldp_connected_interface_1_status ldp_connected_interface_handle]

# This will create LDP Router and interface over IP for the 1st Device Group  with lsr_id="194.0.0.1".
puts "Creating LDP Router Stack on top of IPv4 2 stack"
    set ldp_basic_router_2_status [::ixiangpf::emulation_ldp_config \
    -handle                       $ipv4_2_handle                    \
    -mode                         create                            \
    -lsr_id                       194.0.0.1                         \
    -interface_name               {LDP-IF 2}                        \
    -router_name                  {LDP 2}                           \
]
if {[keylget ldp_basic_router_2_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ldp_basic_router_2_status log]"
        return 0
}
set ldpBasicRouter_2_handle [keylget ldp_basic_router_2_status ldp_basic_router_handle]

#Creating LDP Interface Stack on top of IPv4 1 stack for second device Group
puts "Creating LDP Interface Stack on top of IPv4 2 stack" 
set ldp_connected_interface_2_status [::ixiangpf::emulation_ldp_config \
    -handle                    $ipv4_2_handle                          \
    -mode                      create                                  \
    -interface_name            {LDP-IF 2}                              \
]
if {[keylget ldp_connected_interface_2_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ldp_connected_interface_2_status log]"
        return 0
}
set ldpConnectedInterface_2_handle [keylget ldp_connected_interface_2_status ldp_connected_interface_handle]

# Creating IPv4 prefix pool of Network for Network Cloud behind first Device Group with "ipv4_prefix_network_address" =201.1.0.1
puts "Creating IPv4 prefix pool behind first Device Group" 
set network_group_1_status [::ixiangpf::network_group_config         \
    -protocol_handle                      $deviceGroup_1_handle      \
    -protocol_name                        {Network Cloud 1}          \
    -connected_to_handle                  $ethernet_1_handle         \
    -type                                 ipv4-prefix                \
    -ipv4_prefix_network_address          201.1.0.1                  \
    -ipv4_prefix_length                   32                         \
    -ipv4_prefix_number_of_addresses      1                          \
    ]
if {[keylget network_group_1_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $network_group_1_status
}
set networkGroup_1_handle [keylget network_group_1_status network_group_handle]
set ipv4PrefixPools_1_handle [keylget network_group_1_status ipv4_prefix_pools_handle]

# Modifying in IPv4 prefix for LDP Router related Configurations
puts "Modification of LDP related parameters in Network Cloud"
set network_group_1_status [::ixiangpf::emulation_ldp_route_config \
    -mode                        modify                            \
    -handle                      $networkGroup_1_handle            \
    -egress_label_mode           fixed                             \
    -fec_type                    ipv4_prefix                       \
    -label_value_start           17                                \
    -label_value_start_step      1                                 \
    -lsp_handle                  $networkGroup_1_handle            \
    -fec_active                  1                                 \
    -fec_name                    {LDP FEC Range 1}                 \
]
if {[keylget network_group_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget network_group_1_status log]"
        return 0
}

# Creating IPv4 prefix pool of Network for Network Cloud behind second Device Group  with "ipv4_prefix_network_address" =202.1.0.1
puts "Creating IPv4 prefix pool behind second Device Group" 
set network_group_2_status [::ixiangpf::network_group_config         \
    -protocol_handle                      $deviceGroup_2_handle      \
    -protocol_name                        {Network Cloud 2}          \
    -multiplier                           1                          \
    -enable_device                        1                          \
    -connected_to_handle                  $ethernet_2_handle         \
    -type                                 ipv4-prefix                \
    -ipv4_prefix_network_address          202.1.0.1                  \
    -ipv4_prefix_length                   32                         \
    -ipv4_prefix_number_of_addresses      1                          \
    ]
if {[keylget network_group_2_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget network_group_2_status log]"
        return 0
}
set networkGroup_2_handle [keylget network_group_2_status network_group_handle]
set ipv4PrefixPools_2_handle [keylget network_group_2_status ipv4_prefix_pools_handle]

# Modifying in IPv4 prefix for LDP Router related Configurations "label_value_start"=18
puts "Modification of LDP related parameters in Network Cloud"
set network_group_2_status [::ixiangpf::emulation_ldp_route_config \
    -mode                        modify                            \
    -handle                      $networkGroup_2_handle            \
    -egress_label_mode           fixed                             \
    -fec_type                    ipv4_prefix                       \
    -label_value_start           18                                \
    -label_value_start_step      1                                 \
    -lsp_handle                  $networkGroup_2_handle            \
    -fec_name                    {LDP FEC Range 2}                 \
]
if {[keylget network_group_2_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget network_group_2_status log]"
        return 0
}
# Going to create Chained Device Group 3  behind Network Cloud 1 within Topology 1 and renaming of that chained DG to "Provider Edge Router 1"
puts "Going to create Chained DG 3 in Topology 1 behind Network Cloud 1 and renaming it"
set device_group_1_1_status [::ixiangpf::topology_config            \
    -device_group_name            {Provider Edge Router 1}      \
    -device_group_multiplier      1                             \
    -device_group_enabled         1                             \
    -device_group_handle          $networkGroup_1_handle        \
]
if {[keylget device_group_1_1_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $device_group_1_1_status
    }
set deviceGroup_1_1_handle [keylget device_group_1_1_status device_group_handle]
# Creating multivalue loopback adderress within chained DG in Topology 1
puts "Creating multivalue for loopback adderress within chained DG";
set multivalue1_1_status [::ixiangpf::multivalue_config                                           \
    -pattern                counter                                                              \
    -counter_start          201.1.0.1                                                            \
    -counter_step           0.0.0.1                                                              \
    -counter_direction      increment                                                            \
    -nest_step              0.0.0.1,0.0.0.1,0.1.0.0                                              \
    -nest_owner             $networkGroup_1_handle,$deviceGroup_1_handle,$topology_1_handle      \
    -nest_enabled           0,0,1                                                                \
]
if {[keylget multivalue1_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget multivalue1_1_status log]"
        return 0
}
set multivalue_4_handle [keylget multivalue1_1_status multivalue_handle]
# Creating Loopback behind Chained DG.
puts "Creating Loopback behind Chained DG"
set ipv4_loopback_1_status [::ixiangpf::interface_config    \
    -protocol_name            {IPv4 Loopback 1}             \
    -protocol_handle          $deviceGroup_1_1_handle       \
    -enable_loopback          1                             \
    -connected_to_handle      $networkGroup_1_handle        \
    -intf_ip_addr             $multivalue_4_handle          \
    -netmask                  255.255.255.255               \
]

if {[keylget ipv4_loopback_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ipv4_loopback_1_status log]"
        return 0
}
set ipv4Loopback_1_handle [keylget ipv4_loopback_1_status ipv4_loopback_handle]

# Going to create Chained Device Group 4  behind Network Cloud 1 within Topology 1 and renaming of that chained DG to "Provider Edge Router 2"
puts "Going to create Chained DG 4 in Topology 2 behind Network Cloud 2 and renaming it"
set device_group_2_1_status [::ixiangpf::topology_config            \
    -device_group_name            {Provider Edge Router 2}      \
    -device_group_multiplier      1                             \
    -device_group_enabled         1                             \
    -device_group_handle          $networkGroup_2_handle        \
]
if {[keylget device_group_2_1_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $device_group_2_1_status
    }
set deviceGroup_2_1_handle [keylget device_group_2_1_status device_group_handle]
# Creating multivalue loopback adderress within chained DG in Topology 2
puts "Creating multivalue for loopback adderress within chained DG 4";
set multivalue2_1_status [::ixiangpf::multivalue_config                                           \
    -pattern                counter                                                              \
    -counter_start          202.1.0.1                                                            \
    -counter_step           0.0.0.1                                                              \
    -counter_direction      increment                                                            \
    -nest_step              0.0.0.1,0.0.0.1,0.1.0.0                                              \
    -nest_owner             $networkGroup_2_handle,$deviceGroup_2_handle,$topology_2_handle      \
    -nest_enabled           0,0,1                                                                \
]
if {[keylget multivalue2_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget multivalue2_1_status log]"
        return 0
}
set multivalue_5_handle [keylget multivalue2_1_status multivalue_handle]
# Creating Loopback behind Chained Device Group 4 within Device Group.
puts "Creating Loopback behind Chained DG 4"
set ipv4_loopback_2_status [::ixiangpf::interface_config    \
    -protocol_name            {IPv4 Loopback 2}             \
    -protocol_handle          $deviceGroup_2_1_handle       \
    -enable_loopback          1                             \
    -connected_to_handle      $networkGroup_2_handle        \
    -intf_ip_addr             $multivalue_5_handle          \
    -netmask                  255.255.255.255               \
]

if {[keylget ipv4_loopback_2_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ipv4_loopback_2_status log]"
        return 0
}
set ipv4Loopback_2_handle [keylget ipv4_loopback_2_status ipv4_loopback_handle]


#Adding Targeted Router and LDP PW/VPLS on top of Loopback within Chained device group under topology 1 lsr_id="195.0.0.1",remote_ip_addr ="202.1.0.1",remote_ip_addr_step="0.0.0.1"
puts "Adding Targeted Router under topology 1"
set ldp_targeted_router_1_status [::ixiangpf::emulation_ldp_config \
    -handle                        $ipv4Loopback_1_handle          \
    -mode                          create                          \
    -label_adv                     unsolicited                     \
    -lsr_id                        195.0.0.1                       \
    -remote_ip_addr                202.1.0.1                       \
    -remote_ip_addr_step           0.0.0.1                         \
    -target_name                   {LDP 3}                         \
    -initiate_targeted_hello       1                               \
    -targeted_peer_name            {LDP Targeted Peers 1}          \
    -lpb_interface_name            {LDP-IF 3}                      \
    -lpb_interface_active          1                               \
]    
if {[keylget ldp_targeted_router_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ldp_targeted_router_1_status log]"
        return 0
}
set ldpTargetedRouter_1_handle [keylget ldp_targeted_router_1_status ldp_targeted_router_handle]
# Configuration LDP PW/VPLS on top of on top of Targeted Router fec_vc_label_value_start="216", fec_vc_peer_address="202.1.0.1",fec_vc_type="eth",
puts "Configuring LDP PW/VPLS on top of on top of Targeted Router"  
set ldppwvpls_1_status [::ixiangpf::emulation_ldp_route_config                \
    -mode                                    create                           \
    -handle                                  $ldpTargetedRouter_1_handle      \
    -fec_type                                vc                               \
    -fec_vc_count                            1                                \
    -fec_vc_fec_type                         pw_id_fec                        \
    -fec_vc_group_id                         1                                \
    -fec_vc_id_start                         1                                \
    -fec_vc_name                             {LDP PW/VPLS 1}                  \
    -fec_vc_active                           1                                \
    -fec_vc_label_value_start                216                              \
    -fec_vc_peer_address                     202.1.0.1                        \
    -fec_vc_type                             eth                              \
    -fec_vc_pw_status_code                   clear_fault_code                 \
]
if {[keylget ldppwvpls_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ldppwvpls_1_status log]"
        return 0
}
set ldppwvpls_1_handle [keylget ldppwvpls_1_status ldppwvpls_handle]

#Adding Targeted Router and LDP PW/VPLS on top of Loopback within Chained device group under topology 2
puts "Adding Targeted Router under topology 2"
set ldp_targeted_router_2_status [::ixiangpf::emulation_ldp_config \
    -handle                        $ipv4Loopback_2_handle          \
    -mode                          create                          \
    -label_adv                     unsolicited                     \
    -lsr_id                        196.0.0.1                       \
    -remote_ip_addr                201.1.0.1                       \
    -remote_ip_addr_step           0.0.0.1                         \
    -peer_count                    1                               \
    -target_name                   {LDP 4}                         \
    -targeted_peer_name            {LDP Targeted Peers 2}          \
    -lpb_interface_name            {LDP-IF 4}                      \
    -lpb_interface_active          1                               \
]

if {[keylget ldp_targeted_router_2_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ldp_targeted_router_2_status log]"
        return 0
}
set ldpTargetedRouter_2_handle [keylget ldp_targeted_router_2_status ldp_targeted_router_handle]
# Configuration LDP PW/VPLS on top of on top of Targeted Router
puts "Configuring LDP PW/VPLS on top of on top of Targeted Router"  
set ldppwvpls_2_status [::ixiangpf::emulation_ldp_route_config                \
    -mode                                    create                           \
    -handle                                  $ldpTargetedRouter_2_handle      \
    -fec_type                                vc                               \
    -fec_vc_count                            1                                \
    -fec_vc_fec_type                         pw_id_fec                        \
    -fec_vc_group_id                         1                                \
    -fec_vc_id_start                         1                                \
    -fec_vc_name                             {LDP PW/VPLS 1}                  \
    -fec_vc_active                           1                                \
    -fec_vc_label_value_start                516                              \
    -fec_vc_peer_address                     201.1.0.1                        \
    -fec_vc_type                             eth                              \
    -fec_vc_pw_status_code                   clear_fault_code                 \
    -return_detailed_handles     1                                            \
]
if {[keylget ldppwvpls_2_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget ldppwvpls_2_status log]"
        return 0
}
set ldppwvpls_2_handle [keylget ldppwvpls_2_status ldppwvpls_handle]
# Configuration of MAC Pool behind Chained Device within Topology 1
puts "Configuring CE MAC Pool in Topology 1"
set network_group_5_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_1_1_handle    \
    -protocol_name                     {CE MAC Cloud 1}           \
    -connected_to_handle               $ldppwvpls_1_handle        \
    -type                              mac-pools                  \
    -mac_pools_mac                     a0.12.01.00.00.01          \
]
if {[keylget network_group_5_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget network_group_5_status log]"
        return 0
}
set networkGroup_4_handle [keylget network_group_5_status network_group_handle]
set macPools_1_handle [keylget network_group_5_status mac_pools_handle]

# Configuration of MAC Pool behind Chained Device within Topology 2
puts "Configuring CE MAC Pool in Topology 2"
set network_group_4_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_2_1_handle    \
    -protocol_name                     {CE MAC Cloud 2}           \
    -connected_to_handle               $ldppwvpls_2_handle        \
    -type                              mac-pools                  \
    -mac_pools_mac                     a0.11.01.00.00.01          \
]
if {[keylget network_group_4_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget network_group_4_status log]"
        return 0
}
set networkGroup_5_handle [keylget network_group_4_status network_group_handle]
set macPools_2_handle [keylget network_group_4_status mac_pools_handle]

# Configuration Block Ends Here    
puts "Waiting 5 seconds before starting protocol(s) ..."
after 5000
############################################################################
# Start all protocols                                                      #
############################################################################
puts "Starting all protocol(s) ..."
set r [::ixia::test_control -action start_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $r
}
puts "Waiting for 30 seconds"
after 30000

############################################################################
#  Retrieve protocol statistics                                            #
############################################################################
puts "Fetching targeted LDP aggregated statistics for Topology 2."
set aggregate_stats [::ixiangpf::emulation_ldp_info   \
    -handle $ldpTargetedRouter_2_handle               \
    -mode "stats"]
foreach stat $aggregate_stats {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}
############################################################################
# 4. Retrieve protocol learned info.                                       #
############################################################################
puts "Fetching LDP aggregated learned info for Topology 1."
set learned_info [::ixiangpf::emulation_ldp_info           \
   -handle $ldpTargetedRouter_1_handle                     \
   -mode "lsp_labels"]
foreach li $learned_info {
    puts "=================================================================="
    puts "$li"
    puts "=================================================================="
}
############################################################################
# Changing Label in both sides of VPN Ranges.                              #
############################################################################
puts "Changing Label value for Topology 1 LDP VPN Ranges:" 
set ldppwvpls_1_status [::ixiangpf::emulation_ldp_route_config \
         -mode                        modify                   \
         -handle                      $ldppwvpls_2_handle      \
         -lsp_handle                  $ldppwvpls_2_handle      \
         -fec_vc_label_value_start    5001                     \
     ]
if {[keylget ldppwvpls_1_status status] != $::SUCCESS} {
         $::ixnHLT_errorHandler [info script] $ldppwvpls_1_status
}    

################################################################################
# Applying changes one the fly                                                 #
################################################################################
puts "Applying changes on the fly"
set applyChanges [::ixiangpf::test_control \
   -handle $ipv4_1_handle \
   -action apply_on_the_fly_changes]
if {[keylget applyChanges status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget applyChanges log]"
    return 0
}
after 5000

############################################################################
# Retrieve protocol learned info again and notice the difference with      #
# previouly retrieved learned info                                         #   
############################################################################
puts "Fetching LDP aggregated learned info for Topology 2."
set learned_info [::ixiangpf::emulation_ldp_info           \
   -handle $ldpTargetedRouter_2_handle                     \
   -mode "lsp_labels"]
foreach li $learned_info {
    puts "=================================================================="
    puts "$li"
    puts "=================================================================="
}
############################################################################ 
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv4, Destination->Multicast group                #
# 2. Type      : Multicast IPv4 traffic                                    #
# 3. Flow Group: On IPv4 Destination Address                               #
# 4. Rate      : 100000 packets per second                                 #
# 5. Frame Size: 64 bytes                                                  #
# 6. Tracking  : IPv4 Destination Address                                  #
############################################################################
set _result_ [::ixia::traffic_config                                                                                   \
    -mode                                     create                                                                   \
    -traffic_generator                        ixnetwork_540                                                            \
    -endpointset_count                        1                                                                        \
    -emulation_src_handle                     $macPools_1_handle                                                       \
    -emulation_dst_handle                     $macPools_2_handle                                                       \
    -frame_sequencing                         disable                                                                  \
    -frame_sequencing_mode                    rx_threshold                                                             \
    -name                                     Traffic_Item_1                                                           \
    -circuit_endpoint_type                    ethernet_vlan                                                            \
    -rate_pps                                 100000                                                                   \
    -frame_size                               64                                                                       \
    -mac_dst_mode                             fixed                                                                    \
    -mac_src_mode                             fixed                                                                    \
    -mac_src_tracking                         1                                                                        \
    -track_by                                 {ethernetIiSourceaddress0 trackingenabled0 ethernetIiDestinationaddress0}\
]
if {[keylget _result_ status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
    return 0
}

############################################################################
# Start L2-L3 traffic configured earlier                                   #
# Start application traffic configured earlier                             #
############################################################################
puts "Running Traffic..."
set r [::ixia::traffic_control       \
    -action run                      \
    -traffic_generator ixnetwork_540 \
    -type {l23}                  \
]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}

puts "Let the traffic run for 30 seconds ..."                
after 30000

############################################################################
# Retrieve Application traffic stats                                       # 
# Retrieve L2-L3 traffic stats                                             # 
############################################################################
set r [::ixia::traffic_stats        \
    -mode all                       \
    -traffic_generator ixnetwork_540\
    -measure_mode mixed             \
    ]
foreach stat $r {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}
############################################################################
# Stop L2-L3 traffic started earlier                                       #
# Stop application traffic started earlier                                 #
############################################################################
puts "Stopping Traffic..."
set r [::ixia::traffic_control             \
    -action stop                           \
    -traffic_generator ixnetwork_540       \
    -type {l23 l47} ]
if {[keylget r status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $r
}
############################################################################
# Stop all protocols                                                       #
############################################################################
puts "Stopping all protocol(s) ..."
set r [::ixia::test_control -action stop_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "!!! Test Script Ends !!!"           
return 1
