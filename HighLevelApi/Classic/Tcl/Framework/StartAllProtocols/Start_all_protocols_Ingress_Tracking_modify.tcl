#################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-20-2007 Mchakravarthy - created sample
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
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#   This sample configures IPv4 traffic items and modifes the ingress tracking #
#  	 and validates it												           #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################

global cfgErrors

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
# Common procedures used for verifying with IxNet values
################################################################################
proc print_flow_stats {flow_traffic_status} {
    set flow_results [list                                                  \
        "Tx Frames"                     tx.total_pkts			13893		\
        "Rx Frames"                     rx.total_pkts			13893		\
        "Tx pkt_rate"                   tx.total_pkt_rate		3089		\
    ]

    set flows [keylget flow_traffic_status flow]
    foreach flow [keylkeys flows] {
        set flow_key [keylget flow_traffic_status flow.$flow]
        puts "\tFlow $flow"
        foreach {name key value} [subst $[subst flow_results]] {
			set statValue [keylget flow_traffic_status flow.$flow.$key] 
            puts "\t\t$name: $statValue"			
			if {$name == "Loss %"} {
				if {$statValue > $value} {			
					puts "FAIL - $name"
					return 0
				}
			} elseif {$statValue < $value} {
				puts "FAIL - $name"
				return 0
			}
        }
    }
	return 1
}

################################################################################
# General script variables
################################################################################
set test_name                                   [info script]
set chassis_ip									10.205.16.54
set port_list									[list 2/5 2/6]
set break_locks									1
set tcl_server									10.205.16.54
set ixnetwork_tcl_server						localhost
set port_count									2
set cfgErrors									0
################################################################################
# START - Connect to the chassis
################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect

puts "Starting - $test_name - [clock format [clock seconds]]"
puts "Start connecting to chassis ..."

set connect_status [::ixia::connect                                        	   \
            -reset                                                             \
            -device               $chassis_ip                                  \
            -port_list            $port_list                                   \
            -break_locks          $break_locks                                 \
            -tcl_server           $tcl_server                                  \
            -ixnetwork_tcl_server $ixnetwork_tcl_server                        \
            -interactive          1                                            \
            ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set i 0
puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port    
    incr i
}
puts "End connecting to chassis ..."

################################################################################
# END - Connect to the chassis
################################################################################

################################################################################
# START - Interface configuration - Port 0
################################################################################
puts "Start interface configuration for Port:$port_0"

set interface_status_0 [::ixia::interface_config 		\
        -port_handle        		$port_0        		\
		-l23_config_type 			protocol_interface	\
        -intf_ip_addr       		11.1.1.1      		\
        -gateway            		11.1.1.2     		\
        -netmask            		255.255.255.0		\
		-arp_on_linkup 				1					\
        -ns_on_linkup 				1					\
        -single_arp_per_gateway 	1					\
        -single_ns_per_gateway		1					\
		-autonegotiation			1              		\
        -duplex             		auto           		\
        -speed              		auto           		\
        -intf_mode          		ethernet         	]
if {[keylget interface_status_0 status] != $::SUCCESS} {
	puts "FAIL - $test_name - [keylget interface_status_0 log]"
	return 0
}

set interface_handle_0 [keylget interface_status_0 interface_handle]
puts "Interface Handle: $interface_handle_0"
puts "End interface configuration for Port:$port_0"

################################################################################
# START - Interface configuration - Port 1
################################################################################

puts "Start interface configuration for Port:$port_1"

set interface_status_1 [::ixia::interface_config    \
        -port_handle        	$port_1       		\
		-l23_config_type 		protocol_interface	\
        -intf_ip_addr       	11.1.1.2      		\
        -gateway            	11.1.1.1     		\
        -netmask            	255.255.255.0		\
		-arp_on_linkup 			1					\
        -ns_on_linkup 			1					\
        -single_arp_per_gateway 1					\
        -single_ns_per_gateway	1					\
		-autonegotiation		1              		\
        -duplex             	auto           		\
        -speed              	auto           		\
        -intf_mode          	ethernet         ]
if {[keylget interface_status_1 status] != $::SUCCESS} {
	puts "FAIL - $test_name - [keylget interface_status_1 log]"
	return 0
}

set interface_handle_1 [keylget interface_status_1 interface_handle]
puts "Interface Handle: $interface_handle_1"
puts "End interface configuration for Port:$port_1"

################################################################################
# Configure BGP on port_0
#################################################################################

set bgp_router_status_1	[::ixia::emulation_bgp_config					\
		-mode							reset							\
		-port_handle					$port_0							\
		-mac_address_start				0000.72f5.e74d					\
		-netmask						24								\
		-ip_version						4								\
		-retry_time						120								\
		-retries						0								\
		-local_as_mode					fixed							\
		-bfd_registration_mode			multi_hop						\
		-local_router_id				2.2.2.2							\
		-remote_loopback_ip_addr		1.1.1.1							\
		-remote_ip_addr					20.20.20.2						\
		-bfd_registration				0								\
		-local_router_id_enable			1								\
		-hold_time						90								\
		-ipv4_mpls_nlri					1								\
		-ipv4_mpls_vpn_nlri				1								\
		-ipv4_multicast_nlri			1								\
		-ipv4_unicast_nlri				1								\
		-ipv6_mpls_nlri					1								\
		-ipv6_mpls_vpn_nlri				1								\
		-ipv6_multicast_nlri			1								\
		-ipv6_unicast_nlri				1								\
		-local_as						100								\
		-local_loopback_ip_addr			2.2.2.2							\
		-local_ip_addr					20.20.20.1						\
		-next_hop_ip					0.0.0.0							\
		-updates_per_iteration			1								\
		-restart_time					45								\
		-staggered_start_time			0								\
		-stale_time						0								\
		-tcp_window_size				8192							\
		-neighbor_type					internal						\
		-update_interval				0								\
		-vpls							disabled						]
		
#Check status
if {[keylget bgp_router_status_1 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget bgp_router_status_1 log]"
return 0
}

set bgp_handles_1 [keylget bgp_router_status_1 handles]

set bgp_routes_status_1	[::ixia::emulation_bgp_route_config				\
		-mode							add								\
		-handle							$bgp_handles_1					\
		-num_sites						1								\
		-as_path						{}								\
		-label_value					16								\
		-label_incr_mode				rd								\
		-label_step						1								\
		-import_target_type				as								\
		-import_target					100								\
		-import_target_assign			1								\
		-target_type					as								\
		-target							100								\
		-target_assign					1								\
		-rd_admin_value					100								\
		-rd_assign_value				1								\
		-rd_type						0								\
		-next_hop_enable				1								\
		-origin_route_enable			1								\
		-enable_traditional_nlri		1								\
		-ipv4_mpls_vpn_nlri				1								\
		-ipv6_mpls_vpn_nlri				1								\
		-packing_from					0								\
		-prefix_from					24								\
		-ip_version						4								\
		-prefix_step					1								\
		-local_pref						0								\
		-prefix							22.22.1.0						\
		-next_hop						0.0.0.0							\
		-next_hop_mode					increment						\
		-next_hop_set_mode				same							\
		-num_routes						50								\
		-origin							igp								\
		-originator_id					0.0.0.0							\
		-packing_to						0								\
		-prefix_to						24								]
		
#Check status
if {[keylget bgp_routes_status_1 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget bgp_routes_status_1 log]"
return 0
}

set vpn_sources [keylget bgp_routes_status_1 bgp_routes]

################################################################################
# Configure OSPF on port_0
#################################################################################

set ospf_router_status_1	[::ixia::emulation_ospf_config				\
		-mode							create							\
		-port_handle					$port_0							\
		-lsa_discard_mode				1								\
		-session_type					ospfv2							\
		-area_id						0.0.0.0							\
		-area_type						external-capable				\
		-dead_interval					40								\
		-hello_interval					10								\
		-interface_cost					10								\
		-authentication_mode			null							\
		-mtu							1500							\
		-neighbor_router_id				0.0.0.0							\
		-network_type					ptop							\
		-option_bits					42								\
		-router_priority				2								\
		-te_enable						1								\
		-te_max_bw						125000000						\
		-te_max_resv_bw					125000000						\
		-te_metric						1								\
		-te_unresv_bw_priority0			125000000						\
		-te_unresv_bw_priority1			125000000						\
		-te_unresv_bw_priority2			125000000						\
		-te_unresv_bw_priority3			125000000						\
		-te_unresv_bw_priority4			125000000						\
		-te_unresv_bw_priority5			125000000						\
		-te_unresv_bw_priority6			125000000						\
		-te_unresv_bw_priority7			125000000						\
		-bfd_registration				0								\
		-intf_ip_addr					20.20.20.1						\
		-intf_prefix_length				24								\
		-neighbor_intf_ip_addr			20.20.20.2						\
		-vlan							0								\
		-vlan_id						1								\
		-vlan_user_priority				0								\
		-mac_address_init				0000.72f5.e74d					\
		-graceful_restart_enable		0								\
		-router_id						2.2.2.2							]
		
#Check status
if {[keylget ospf_router_status_1 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget ospf_router_status_1 log]"
	return 0
}

set ospf_handle_1 [keylget ospf_router_status_1 handle]

set ospf_route_status_1 [::ixia::emulation_ospf_topology_route_config	\
		-mode							create							\
		-handle							$ospf_handle_1					\
		-count							1								\
		-type							grid							\
		-interface_ip_address			2.2.2.2							\
		-interface_ip_mask				255.255.255.255					\
		-interface_ip_options			64								\
		-neighbor_router_id				0.0.0.0							\
		-link_type						stub							\
		-router_abr						0								\
		-router_asbr					0								\
		-router_te						0								\
		-grid_connect					{0 0}							\
		-enable_advertise				0								\
		-grid_col						0								\
		-grid_row						0								\
		-grid_router_id					0.0.0.0							\
		-grid_router_id_step			0.0.0.0							\
		-grid_link_type					broadcast						\
		-grid_prefix_start				0.0.0.0							\
		-grid_prefix_length				0								\
		-grid_prefix_step				0.0.0.0							]
		
#Check status
if {[keylget ospf_route_status_1 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget ospf_route_status_1 log]"
	return 0
}

set route_config_status	[::ixia::emulation_ospf_lsa_config				\
		-mode								create						\
		-session_type						ospfv2                      \
		-type								opaque_type_10				\
		-handle								$ospf_handle_1				\
		-adv_router_id						20.20.20.1					\
		-opaque_tlv_type					link						\
		-opaque_enable_link_id				1							\
		-opaque_enable_link_metric			1							\
		-opaque_enable_link_resource_class	1							\
		-opaque_enable_link_type			1							\
		-opaque_enable_link_local_ip_addr	1							\
		-opaque_enable_link_max_bw			1							\
		-opaque_enable_link_max_resv_bw		1							\
		-opaque_enable_link_remote_ip_addr	1							\
		-opaque_enable_link_unresv_bw		1							\
		-opaque_link_id						20.20.20.1					\
		-opaque_link_local_ip_addr			20.20.20.1					\
		-opaque_link_metric					1							\
		-opaque_link_remote_ip_addr			20.20.20.2					\
		-opaque_link_resource_class			0xaa000000					\
		-opaque_link_type					ptop						\
		-opaque_link_unresv_bw_priority		{125000000 125000000 125000000 125000000 125000000 125000000 125000000 125000000} \
		-opaque_link_max_bw					250000000					\
		-opaque_link_max_resv_bw			250000000					\
		-link_state_id						20.20.20.1					\
		-options							64							]
		
if {[keylget route_config_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget route_config_status log]"
    return 0
}

################################################################################
# Configure RSVP on port_0
#################################################################################

set rsvp_router_status_1 [::ixia::emulation_rsvp_config					\
		-mode								create						\
		-port_handle						$port_0						\
		-count								1							\
		-ip_version							4							\
		-egress_label_mode					exnull						\
		-record_route						1							\
		-resv_state_refresh_timeout			30000						\
		-resv_confirm						0							\
		-resv_state_timeout_count			3							\
		-path_state_refresh_timeout			30000						\
		-path_state_timeout_count			3							\
		-enable_bgp_over_lsp				1							\
		-actual_restart_time				15000						\
		-neighbor_intf_ip_addr				20.20.20.2					\
		-graceful_restart					0							\
		-hello_msgs							0							\
		-intf_prefix_length					24							\
		-vlan								0							\
		-vlan_id							1							\
		-vlan_user_priority					0							\
		-mac_address_init					0000.72f5.e74d				\
		-graceful_restart_start_time		30000						\
		-graceful_restart_up_time			30000						\
		-hello_interval						5							\
		-hello_retry_count					3							\
		-max_label_value					100000						\
		-min_label_value					1000						\
		-graceful_restarts_count			0							\
		-intf_ip_addr						20.20.20.1					\
		-graceful_restart_recovery_time		30000						\
		-refresh_reduction					0							\
		-graceful_restart_restart_time		30000						\
		-srefresh_interval					30000						]
	
#Check status
if {[keylget rsvp_router_status_1 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget rsvp_router_status_1 log]"
	return 0
}

set rsvp_router_handle_1 [keylget rsvp_router_status_1 handles]

################################################################################
# Configure RSVP Tunnel on port_0
################################################################################

set rsvp_tunnel_status_1 [::ixia::emulation_rsvp_tunnel_config			\
		-mode								create						\
		-handle								$rsvp_router_handle_1		\
		-count								1							\
		-egress_leaf_range_count			1							\
		-egress_leaf_ip_count				1							\
		-ingress_bandwidth					0							\
		-session_attr_bw_protect			0							\
		-fast_reroute						0							\
		-session_attr_resource_affinities	0							\
		-session_attr_ra_exclude_any		0							\
		-fast_reroute_bandwidth				0							\
		-avoid_node_id						{}							\
		-plr_id								{}							\
		-fast_reroute_exclude_any			0							\
		-facility_backup					0							\
		-fast_reroute_holding_priority		7							\
		-fast_reroute_hop_limit				3							\
		-fast_reroute_include_all			0							\
		-fast_reroute_include_any			0							\
		-one_to_one_backup					0							\
		-send_detour						0							\
		-fast_reroute_setup_priority		7							\
		-session_attr_hold_priority			7							\
		-session_attr_ra_include_all		0							\
		-session_attr_ra_include_any		0							\
		-ingress_ip_addr					2.2.2.2						\
		-session_attr_label_record			0							\
		-session_attr_local_protect			1							\
		-lsp_id_count						1							\
		-lsp_id_start						1							\
		-sender_tspec_max_pkt_size			0							\
		-sender_tspec_min_policed_size		0							\
		-session_attr_node_protect			0							\
		-sender_tspec_peak_data_rate		0							\
		-session_attr_se_style				1							\
		-session_attr_setup_priority		7							\
		-sender_tspec_token_bkt_rate		0							\
		-sender_tspec_token_bkt_size		0							\
		-ero								0							\
		-rro								0							\
		-tunnel_id_count					1							\
		-tunnel_id_start					1							\
		-rsvp_behavior						rsvpIngress					\
		-emulation_type						rsvpte						\
		-egress_ip_addr						1.1.1.1						\
		-enable_append_connected_ip			1							\
		-enable_prepend_tunnel_head_ip		1							\
		-enable_prepend_tunnel_leaf_ip		1							\
		-enable_send_as_rro					1							\
		-enable_send_as_srro				0							]
		
#Check status
if {[keylget rsvp_tunnel_status_1 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget rsvp_tunnel_status_1 log]"
	return 0
}

set rsvp_tunnel_status_2 [::ixia::emulation_rsvp_tunnel_config			\
		-mode								create						\
		-handle								$rsvp_router_handle_1		\
		-count								1							\
		-egress_leaf_range_count			1							\
		-egress_leaf_ip_count				1							\
		-ingress_bandwidth					0							\
		-egress_behavior					always_use_configured_style \
		-reservation_style					se							\
		-rsvp_behavior						rsvpEgress					\
		-emulation_type						rsvpte						\
		-egress_ip_addr						2.2.2.2						\
		-enable_append_connected_ip			1							\
		-enable_prepend_tunnel_head_ip		1							\
		-enable_prepend_tunnel_leaf_ip		1							\
		-enable_send_as_rro					1							\
		-enable_send_as_srro				0							]
		
#Check status
if {[keylget rsvp_tunnel_status_2 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget rsvp_tunnel_status_2 log]"
	return 0
}

################################################################################
# Configure BGP on port_1
################################################################################

set bgp_router_status_2	[::ixia::emulation_bgp_config					\
		-mode							reset							\
		-port_handle					$port_1							\
		-mac_address_start				0000.72f6.e759					\
		-netmask						24								\
		-ip_version						4								\
		-retry_time						120								\
		-retries						0								\
		-local_as_mode					fixed							\
		-bfd_registration_mode			multi_hop						\
		-local_router_id				1.1.1.1							\
		-remote_loopback_ip_addr		2.2.2.2							\
		-remote_ip_addr					20.20.20.1						\
		-bfd_registration				0								\
		-local_router_id_enable			1								\
		-hold_time						90								\
		-ipv4_mpls_nlri					1								\
		-ipv4_mpls_vpn_nlri				1								\
		-ipv4_multicast_nlri			1								\
		-ipv4_unicast_nlri				1								\
		-ipv6_mpls_nlri					1								\
		-ipv6_mpls_vpn_nlri				1								\
		-ipv6_multicast_nlri			1								\
		-ipv6_unicast_nlri				1								\
		-local_as						100								\
		-local_loopback_ip_addr			1.1.1.1							\
		-local_ip_addr					20.20.20.2						\
		-next_hop_ip					0.0.0.0							\
		-updates_per_iteration			1								\
		-restart_time					45								\
		-staggered_start_time			0								\
		-stale_time						0								\
		-tcp_window_size				8192							\
		-neighbor_type					internal						\
		-update_interval				0								\
		-vpls							disabled						]
		
#Check status
if {[keylget bgp_router_status_2 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget bgp_router_status_2 log]"
return 0
}

set bgp_handles_2 [keylget bgp_router_status_2 handles]

set bgp_routes_status_2	[::ixia::emulation_bgp_route_config				\
		-mode							add								\
		-handle							$bgp_handles_2					\
		-num_sites						1								\
		-as_path						{}								\
		-label_value					16								\
		-label_incr_mode				rd								\
		-label_step						1								\
		-import_target_type				as								\
		-import_target					100								\
		-import_target_assign			1								\
		-target_type					as								\
		-target							100								\
		-target_assign					1								\
		-rd_admin_value					100								\
		-rd_assign_value				1								\
		-rd_type						0								\
		-next_hop_enable				1								\
		-origin_route_enable			1								\
		-enable_traditional_nlri		1								\
		-ipv4_mpls_vpn_nlri				1								\
		-ipv6_mpls_vpn_nlri				1								\
		-packing_from					0								\
		-prefix_from					24								\
		-ip_version						4								\
		-prefix_step					1								\
		-local_pref						0								\
		-prefix							32.22.1.0						\
		-next_hop						0.0.0.0							\
		-next_hop_mode					increment						\
		-next_hop_set_mode				same							\
		-num_routes						50								\
		-origin							igp								\
		-originator_id					0.0.0.0							\
		-packing_to						0								\
		-prefix_to						24								]
		
#Check status
if {[keylget bgp_routes_status_2 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget bgp_routes_status_2 log]"
	return 0
}

set vpn_destinations [keylget bgp_routes_status_2 bgp_routes]

################################################################################
# Configure OSPF on port_1
################################################################################

set ospf_router_status_2	[::ixia::emulation_ospf_config				\
		-mode							create							\
		-port_handle					$port_1							\
		-lsa_discard_mode				1								\
		-session_type					ospfv2							\
		-area_id						0.0.0.0							\
		-area_type						external-capable				\
		-dead_interval					40								\
		-hello_interval					10								\
		-interface_cost					10								\
		-authentication_mode			null							\
		-mtu							1500							\
		-neighbor_router_id				0.0.0.0							\
		-network_type					ptop							\
		-option_bits					42								\
		-router_priority				2								\
		-te_enable						1								\
		-te_max_bw						125000000						\
		-te_max_resv_bw					125000000						\
		-te_metric						1								\
		-te_unresv_bw_priority0			125000000						\
		-te_unresv_bw_priority1			125000000						\
		-te_unresv_bw_priority2			125000000						\
		-te_unresv_bw_priority3			125000000						\
		-te_unresv_bw_priority4			125000000						\
		-te_unresv_bw_priority5			125000000						\
		-te_unresv_bw_priority6			125000000						\
		-te_unresv_bw_priority7			125000000						\
		-bfd_registration				0								\
		-intf_ip_addr					20.20.20.2						\
		-intf_prefix_length				24								\
		-neighbor_intf_ip_addr			20.20.20.1						\
		-vlan							0								\
		-vlan_id						1								\
		-vlan_user_priority				0								\
		-mac_address_init				0000.72f6.e759					\
		-graceful_restart_enable		0								\
		-router_id						1.1.1.1							]
		
#Check status
if {[keylget ospf_router_status_2 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget ospf_router_status_2 log]"
	return 0
}

set ospf_handle_2 [keylget ospf_router_status_2 handle]


set ospf_route_status_2 [::ixia::emulation_ospf_topology_route_config	\
		-mode							create							\
		-handle							$ospf_handle_2					\
		-count							1								\
		-type							grid							\
		-interface_ip_address			1.1.1.1							\
		-interface_ip_mask				255.255.255.255					\
		-interface_ip_options			64								\
		-neighbor_router_id				0.0.0.0							\
		-link_type						stub							\
		-router_abr						0								\
		-router_asbr					0								\
		-router_te						0								\
		-grid_connect					{0 0}							\
		-enable_advertise				0								\
		-grid_col						0								\
		-grid_row						0								\
		-grid_router_id					0.0.0.0							\
		-grid_router_id_step			0.0.0.0							\
		-grid_link_type					broadcast						\
		-grid_prefix_start				0.0.0.0							\
		-grid_prefix_length				0								\
		-grid_prefix_step				0.0.0.0							]
		
#Check status
if {[keylget ospf_route_status_2 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget ospf_route_status_2 log]"
	return 0
}

################################################################################
# Configure RSVP on port_1
################################################################################

set rsvp_router_status_2 [::ixia::emulation_rsvp_config					\
		-mode								create						\
		-port_handle						$port_1						\
		-count								1							\
		-ip_version							4							\
		-egress_label_mode					exnull						\
		-record_route						1							\
		-resv_state_refresh_timeout			30000						\
		-resv_confirm						0							\
		-resv_state_timeout_count			3							\
		-path_state_refresh_timeout			30000						\
		-path_state_timeout_count			3							\
		-enable_bgp_over_lsp				1							\
		-actual_restart_time				15000						\
		-neighbor_intf_ip_addr				20.20.20.1					\
		-graceful_restart					0							\
		-hello_msgs							0							\
		-intf_prefix_length					24							\
		-vlan								0							\
		-vlan_id							1							\
		-vlan_user_priority					0							\
		-mac_address_init					0000.72f6.e759				\
		-graceful_restart_start_time		30000						\
		-graceful_restart_up_time			30000						\
		-hello_interval						5							\
		-hello_retry_count					3							\
		-max_label_value					100000						\
		-min_label_value					1000						\
		-graceful_restarts_count			0							\
		-intf_ip_addr						20.20.20.2					\
		-graceful_restart_recovery_time		30000						\
		-refresh_reduction					0							\
		-graceful_restart_restart_time		30000						\
		-srefresh_interval					30000						]
	
#Check status
if {[keylget rsvp_router_status_2 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget rsvp_router_status_2 log]"
	return 0
}

set rsvp_router_handle_2 [keylget rsvp_router_status_2 handles]

################################################################################
# Configure RSVP Tunnel on port_1
################################################################################

set rsvp_tunnel_status_3 [::ixia::emulation_rsvp_tunnel_config			\
		-mode								create						\
		-handle								$rsvp_router_handle_2		\
		-count								1							\
		-egress_leaf_range_count			1							\
		-egress_leaf_ip_count				1							\
		-ingress_bandwidth					0							\
		-session_attr_bw_protect			0							\
		-fast_reroute						0							\
		-session_attr_resource_affinities	0							\
		-session_attr_ra_exclude_any		0							\
		-fast_reroute_bandwidth				0							\
		-avoid_node_id						{}							\
		-plr_id								{}							\
		-fast_reroute_exclude_any			0							\
		-facility_backup					0							\
		-fast_reroute_holding_priority		7							\
		-fast_reroute_hop_limit				3							\
		-fast_reroute_include_all			0							\
		-fast_reroute_include_any			0							\
		-one_to_one_backup					0							\
		-send_detour						0							\
		-fast_reroute_setup_priority		7							\
		-session_attr_hold_priority			7							\
		-session_attr_ra_include_all		0							\
		-session_attr_ra_include_any		0							\
		-ingress_ip_addr					1.1.1.1						\
		-session_attr_label_record			0							\
		-session_attr_local_protect			1							\
		-lsp_id_count						1							\
		-lsp_id_start						1							\
		-sender_tspec_max_pkt_size			0							\
		-sender_tspec_min_policed_size		0							\
		-session_attr_node_protect			0							\
		-sender_tspec_peak_data_rate		0							\
		-session_attr_se_style				1							\
		-session_attr_setup_priority		7							\
		-sender_tspec_token_bkt_rate		0							\
		-sender_tspec_token_bkt_size		0							\
		-ero								0							\
		-rro								0							\
		-tunnel_id_count					1							\
		-tunnel_id_start					1							\
		-rsvp_behavior						rsvpIngress					\
		-emulation_type						rsvpte						\
		-egress_ip_addr						2.2.2.2						\
		-enable_append_connected_ip			1							\
		-enable_prepend_tunnel_head_ip		1							\
		-enable_prepend_tunnel_leaf_ip		1							\
		-enable_send_as_rro					1							\
		-enable_send_as_srro				0							]
		
#Check status
if {[keylget rsvp_tunnel_status_3 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget rsvp_tunnel_status_3 log]"
	return 0
}

set rsvp_tunnel_status_4 [::ixia::emulation_rsvp_tunnel_config			\
		-mode								create						\
		-handle								$rsvp_router_handle_2		\
		-count								1							\
		-egress_leaf_range_count			1							\
		-egress_leaf_ip_count				1							\
		-ingress_bandwidth					0							\
		-egress_behavior					always_use_configured_style \
		-reservation_style					se							\
		-rsvp_behavior						rsvpEgress					\
		-emulation_type						rsvpte						\
		-egress_ip_addr						1.1.1.1						\
		-enable_append_connected_ip			1							\
		-enable_prepend_tunnel_head_ip		1							\
		-enable_prepend_tunnel_leaf_ip		1							\
		-enable_send_as_rro					1							\
		-enable_send_as_srro				0							]
		
#Check status
if {[keylget rsvp_tunnel_status_4 status] != $::SUCCESS}   {
	puts "FAIL - $test_name - [keylget rsvp_tunnel_status_4 log]"
	return 0
}

puts $vpn_sources
puts $vpn_destinations


################################################################################
# Start All Protocols on both ports                                            #
################################################################################
puts ">>> STARTING ALL PROTOCOLS..."
set start_protcols_status [::ixia::test_control -action start_all_protocols -port_handle $port_handle]

puts ">>> PROTOCOLS STARTED! GETTING STATS ..."

for {set i 0} {$i < 20} {incr i} {

set rsvp_stats_handle_1 [::ixia::emulation_rsvp_info						\
        -mode                       stats									\
        -port_handle                $port_1									\
        -handle                     [keylget rsvp_router_status_1 handles]	]

if {[keylget rsvp_stats_handle_1 status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget rsvp_stats_handle_1 log]"
    return 0
}

set total_lsp_count [keylget rsvp_stats_handle_1 total_lsp_count]
puts "total_lsp_count : $total_lsp_count"


if {$total_lsp_count == 2 } {
	break
}

################################################################################
# Retreive RSVP stats				                                           #
################################################################################

set rsvp_stats_handle_2 [::ixia::emulation_rsvp_info						\
        -mode                       stats									\
        -port_handle                $port_1									\
        -handle                     [keylget rsvp_router_status_2 handles]	]

if {[keylget rsvp_stats_handle_2 status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget rsvp_stats_handle_2 log]"
    return 0
}

set total_lsp_count [keylget rsvp_stats_handle_2 total_lsp_count]
puts "total_lsp_count : $total_lsp_count"

if {$total_lsp_count == 2 } {
	break
}
after 1000
}

################################################################################
################################################################################
# Delete all the streams first
################################################################################
set traffic_status [::ixia::traffic_config \
        -mode        reset                 \
        -port_handle $port_handle          \
        -traffic_generator ixnetwork_540   ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}


################################################################################
# Configure the IPv4 Traffic - 1
################################################################################

set rate_start_value        70
set frame_size_start        512


set src_handle $vpn_sources
#set src_handle $route_range_handle_port0
puts "SRC: $src_handle"
set dst_handle $vpn_destinations
#set dst_handle $route_range_handle_port1
puts "DST: $dst_handle"
      	        
set traffic_status_1 [::ixia::traffic_config       																	\
        -traffic_generator 							ixnetwork_540          											\
		-convert_to_raw								1																\
        -mode                						create               											\
		-circuit_type          						l3vpn                    										\
		-circuit_endpoint_type          			ipv4                    										\
		-track_by                       			endpoint_pair													\
		-stream_packing                       		one_stream_per_endpoint_pair									\
		-name                   					"PE_to_CE_Traffic"												\
		-endpointset_count							1																\
        -emulation_src_handle   					$src_handle													  	\
        -emulation_dst_handle   					$dst_handle														\
        -src_dest_mesh                  			one_to_one     	          										\
		-route_mesh									one_to_one														\
		-rate_percent                   			$rate_start_value       										\
        -frame_size                     			$frame_size_start       										\
		-l2_encap 									ethernet_ii														\
		-l3_protocol 								ipv4															\
		-source_filter								{all all}														\
		-destination_filter							{all all}														\
		-tx_mode									advanced														\
		-transmit_mode								continuous														\
		-tx_delay									3																\
		-tx_delay_unit								bytes															\
		-min_gap_bytes								18																\
		-frame_rate_distribution_port				split_evenly													\
		-frame_rate_distribution_stream				split_evenly													]
		
if {[keylget traffic_status_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status_1 log]"
    return 0
}

set traffic_item_1 [keylget traffic_status_1 traffic_item]
set traffic_item_1_tracking [ixNet getList [lindex [ixNet getList [ixNet getList [ixNet getRoot] traffic] trafficItem] 0] tracking]
puts "Tracking: $traffic_item_1_tracking"

################################################################################
# Modify ingress tracking - 1
################################################################################

set traffic_status_2	[::ixia::traffic_config									\
            -traffic_generator					ixnetwork_540					\
            -circuit_endpoint_type				ipv4							\
            -mode								modify							\
			-stream_id							[lindex $traffic_item_1 0]		\
			-track_by							source_ip						]

if {[keylget traffic_status_2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status_2 log]"
}
set traffic_item_2 [keylget traffic_status_2 traffic_item]
################################################################################
# Modify ingress tracking - 2
################################################################################

set traffic_status_3 [::ixia::traffic_config									\
            -traffic_generator					ixnetwork_540					\
            -circuit_endpoint_type				ipv4							\
            -mode								modify							\
			-stream_id							[lindex $traffic_item_2 0]		\
			-track_by							dest_ip							]

if {[keylget traffic_status_3 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status_3 log]"
}

################################################################################
# Running Traffic

################################################################################
puts "Running traffic with rate_percent : ${rate_start_value}%"

set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

after 20000

################################################################################
# Retreive Flow stats				                                           #
################################################################################

set flow_traffic_status  [::ixia::traffic_stats				\
        -traffic_generator              ixnetwork_540		\
        -mode                           flow				\
]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return 0
}
puts "Start Collecting stats"
if {[print_flow_stats $flow_traffic_status] != $::SUCCESS} {
	puts "FAIL - $test_name - Stats are not within Threshold value"
	return 0
}

after 10000

################################################################################
# Stop the traffic                                                             #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork_540                               ]
		
################################################################################
# Stop All Protocols on both ports                                            #
################################################################################

set stop_protcols_status [::ixia::test_control -action stop_all_protocols -port_handle $port_handle]

############################### SUCCESS or FAILURE #############################

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1

################################################################################

