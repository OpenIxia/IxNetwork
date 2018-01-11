################################################################################
# Version 1.0    $Revision: 1 $
# $Author: $
#
#    Copyright © 1997 - 2010 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#
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
# Description                                                                  #
#                                                                              #
# This fcoe sample script is using two Ixia back-2-back ports.                 #
# On one port is the fcoe forwarder.                                           #
# The other port is the fcoe client.                                           #
# Configure fcoe forwader first.                                               #
# Then confgure fcoe client.                                                   #
# At this point, must wait for fcoe ports to reapply. Sleeping for 45 seconds. #
#                                                                              #
# For traffic_config emulation src/dst handles, must be in this format:        #
#     ::ixNet::OBJ-/vport:1/protocolStack                                      #
#                                                                              #
################################################################################

package require Ixia

set ixNetworkTclServer 10.200.31.79
set chassisIp 10.200.120.117
set portList [list 5/3 5/4]
set userName hgee

proc KeylPrint {keylist {space ""}} {
    upvar $keylist kl
    set result ""
    foreach key [keylkeys kl] {
	set value [keylget kl $key]
	if {[catch {keylkeys value}]} {
	    append result "$space$key: $value\n"
	} else {
	    set newspace "$space "
	    append result "$space$key:\n[KeylPrint value $newspace]"
	}
    }
    return $result
}

# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide Â–ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
			-reset                                  \
			-ixnetwork_tcl_server   $ixNetworkTclServer     \
			-device                 $chassisIp      \
			-port_list              $portList      \
			-tcl_server             $chassisIp     \
			-username               $userName \
		       ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_array [keylget connect_status port_handle.$chassisIp]

set port0 [keylget port_array [lindex $portList 0]]
set port1 [keylget port_array [lindex $portList 1]]

puts "\n--- connect_status: [KeylPrint connect_status]\n"

puts "\n --- Setting FCOE Priority Groups ---"
set interface_status [::ixia::interface_config \
			  -port_handle $port0\
			  -fcoe_priority_groups {none 3 none none 0 none}\
			  -fcoe_priority_group_size 8\
			  -fcoe_flow_control_type ieee802.1Qbb\
			  -intf_mode ethernet_fcoe\
			  -fcoe_support_data_center_mode 1\
			  -speed ether10000lan\
			  ]


set interface_status [::ixia::interface_config \
			  -port_handle $port1\
			  -fcoe_priority_groups {none 3 none none 0 none}\
			  -fcoe_priority_group_size 8\
			  -fcoe_flow_control_type ieee802.1Qbb\
			  -intf_mode ethernet_fcoe\
			  -fcoe_support_data_center_mode 1\
			  -speed ether10000lan\
			  ]


puts "\nConfiguring fcoe_fwd_config ..."
set _result_ [::ixia::fcoe_fwd_config  \
		  -mode create \
		  -parent_handle $port0 \
		  -style //vport/protocolStack/ethernet/fcoeFwdEndpoint/range \
		  -fip_vnport_keep_alive_period 90000 \
		  -fip_advertisement_period 8000 \
		  -fip_priority 128 \
		  -fip_clear_vlink_port_ids 01.00.01 \
		  -fip_clear_vlink_on_expire True \
		  -fip_fka_dbit False \
		  -fip_enabled True \
		  -fc_map 0E.FC.01 \
		  -vlan_ids {} \
		  -fip_version 1 \
		  -fip_addressing_mode fabric-provided \
		  -fip_vlan_discovery False \
		  -operating_mode VF_PORT \
		  -name_server_commands {{1} {1}} \
		  -logo_reject_interval 0 \
		  -plogi_reject_interval 0 \
		  -name VXPORT-FCF-R1 \
		  -enabled True \
		  -b2b_rx_size 2112 \
		  -fabric_name B0:00:0E:FC:00:00:00:00 \
		  -switch_name A0:00:0E:FC:00:00:00:00 \
		  -fdisc_reject_interval 0 \
		  -flogi_reject_interval 0 \
		  -name_server True \
		  -vlan_range_enabled False \
		  -vlan_range_vlan_id_info  { \
						  { \
							-priority 1 \
							-unique_count 4094 \
							-tpid 0x8100 \
							-increment 1 \
							-name VLAN-1 \
							-enabled False \
							-increment_step 1 \
							-first_id 1 \
						    } \
						  { \
							-priority 1 \
							-unique_count 4094 \
							-tpid 0x8100 \
							-increment 1 \
							-name VLAN-2 \
							-enabled False \
							-increment_step 1 \
							-first_id 1 \
						    } \
					      } \
		  -mac_range_count 1 \
		  -mac_range_mac AA:BB:CC:00:00:00 \
		  -mac_range_name MAC-R5 \
		  -mac_range_increment_by 00:00:00:00:00:01 \
		  -mac_range_mtu 1500 \
		  -vlan_range_id_incr_mode 2 \
		  -mac_range_enabled True \
		 ]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
    puts "\nError: Configuring fcoe fowarder"
    exit
}

puts "\n---- 2: [KeylPrint _result_] ---\n"

# ::ixia::hag::ixn::auto::fcoeFwdVxPort-1
set fcoe_forwarderHandle [keylget _result_ handles]

puts "\n--- fcoe_forwarderHandle: $fcoe_forwarderHandle ----\n"

puts "\nConfiguring fcoe_fwd_vnport_config ..."
# //vport/protocolStack/ethernet/fcoeFwdEndpoint/secondaryRange/fcoeFwdVnPortRange
set _result_ [::ixia::fcoe_fwd_vnport_config  \
		  -mode create \
		  -parent_handle $fcoe_forwarderHandle \
		  -style //vport/protocolStack/ethernet/fcoeFwdEndpoint/secondaryRange \
		  -plogi_target_name {} \
		  -plogi_mesh_mode one-to-one \
		  -node_wwn_increment 00:00:00:00:00:00:00:01 \
		  -plogi_enabled False \
		  -name VNPORT-FCF-R1 \
		  -plogi_dest_id 01.B6.69 \
		  -enabled True \
		  -node_wwn_start 30:00:0E:FC:00:00:00:00 \
		  -simulated False \
		  -port_id_start 01.00.01 \
		  -vx_port_name VXPORT-FCF-R1 \
		  -count 1 \
		  -port_wwn_start 20:00:0E:FC:00:00:00:00 \
		  -port_wwn_increment 00:00:00:00:00:00:00:01 \
		  -port_id_increment 00.00.01 \
		  -b2b_rx_size 2112 \
		 ]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
    puts "\nError: fcoe_fwd_vnport_config"
    exit
}

puts "\n1: Configuring fcoe_fwd_vnport_config ..."
# //vport/protocolStack/ethernet/fcoeFwdEndpoint/secondaryRange/fcoeFwdVnPortRange
set _result_ [::ixia::fcoe_fwd_vnport_config  \
		  -mode add \
		  -style //vport/protocolStack/ethernet/fcoeFwdEndpoint/secondaryRange \
		  -plogi_target_name VNPORT-FLOGI-R5 \
		  -plogi_mesh_mode one-to-one \
		  -node_wwn_increment 00:00:00:00:00:00:00:00 \
		  -plogi_enabled True \
		  -name VNPORT-FCF-FLOGI-R1 \
		  -plogi_dest_id 01.B6.69 \
		  -enabled True \
		  -node_wwn_start 21:00:0E:FC:00:00:00:00 \
		  -simulated True \
		  -port_id_start 01.00.02 \
		  -vx_port_name VXPORT-FCF-R1 \
		  -count 1 \
		  -port_wwn_start 31:00:0E:FC:00:00:00:00 \
		  -port_wwn_increment 00:00:00:00:00:00:00:01 \
		  -port_id_increment 00.00.01 \
		  -b2b_rx_size 2112 \
		 ]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
    puts "\nError:"
    exit
}

puts "\n2: Configuring fcoe_fwd_vnport_config ..."
# //vport/protocolStack/ethernet/fcoeFwdEndpoint/secondaryRange/fcoeFwdVnPortRange
set _result_ [::ixia::fcoe_fwd_vnport_config  \
		  -mode add \
		  -style //vport/protocolStack/ethernet/fcoeFwdEndpoint/secondaryRange \
		  -plogi_target_name {} \
		  -plogi_mesh_mode one-to-one \
		  -node_wwn_increment 00:00:00:00:00:00:00:00 \
		  -plogi_enabled False \
		  -name VNPORT-FCF-FDISC-R1 \
		  -plogi_dest_id 01.B6.69 \
		  -enabled False \
		  -node_wwn_start 21:00:0E:FC:00:00:00:00 \
		  -simulated True \
		  -port_id_start 03.00.01 \
		  -vx_port_name VXPORT-FCF-R1 \
		  -count 1 \
		  -port_wwn_start 41:00:0E:FC:00:00:00:00 \
		  -port_wwn_increment 00:00:00:00:00:00:00:01 \
		  -port_id_increment 00.00.01 \
		  -b2b_rx_size 2112 \
		 ]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
    puts "\nError"
    exit
}


puts "\nConfiguring fcoe_fwd_options_config ..."
# $port0 = 1/10/1
# //vport/protocolStack/fcoeFwdOptions
set _result_ [::ixia::fcoe_fwd_options_config  \
		  -mode create \
		  -parent_handle $port0 \
		  -style //vport/protocolStack \
		  -max_packets_per_second 500 \
		  -unsol_discovery_tpid 0x8100,0x88A8 \
		  -override_global_rate False \
		 ]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
    puts "\nError"
    exit
}

puts "\nConfiguring fcoe_config for fcoe client ..."
# port1 = 1/10/2
set _result_ [::ixia::fcoe_config  \
		  -mode create \
		  -parent_handle $port1 \
		  -style //vport/protocolStack/ethernet/fcoeClientEndpoint/range \
		  -fdisc_name_server_query_parameter_value {} \
		  -fdisc_name_server_query_parameter_type kPortIdentifier \
		  -fdisc_name_server_query_command kGidA \
		  -fdisc_prli_enabled False \
		  -fdisc_state_change_registration_option kFabricDetected \
		  -fdisc_state_change_registration False \
		  -fdisc_source_oui 0E.FC.00 \
		  -fdisc_override_node_wwn False \
		  -fdisc_count 1 \
		  -fdisc_name_server_query False \
		  -fdisc_name_server_registration True \
		  -fdisc_source_oui_increment 00.00.01 \
		  -fdisc_name_server_commands {{1} {1}} \
		  -fdisc_plogi_dest_id 01.B6.69 \
		  -fdisc_plogi_mesh_mode one-to-one \
		  -fdisc_enabled False \
		  -fdisc_name VNPORT-FDISC-R5 \
		  -fdisc_plogi_target_name {} \
		  -fdisc_port_wwn_increment 00:00:00:00:00:00:00:01 \
		  -fdisc_port_wwn_start 42:00:0E:FC:00:00:00:00 \
		  -fdisc_node_wwn_start 22:00:0E:FC:00:00:00:00 \
		  -fdisc_plogi_enabled False \
		  -fdisc_node_wwn_increment 00:00:00:00:00:00:00:00 \
		  -flogi_node_wwn_start 22:00:0E:FC:00:00:00:00 \
		  -flogi_port_wwn_start 32:00:0E:FC:00:00:00:00 \
		  -flogi_fip_vlan_discovery False \
		  -flogi_name_server_commands {{1} {1}} \
		  -flogi_name VNPORT-FLOGI-R5 \
		  -flogi_unicast_fip_solicit none \
		  -flogi_name_server_query_parameter_value {} \
		  -flogi_port_wwn_increment 00:00:00:00:00:00:00:01 \
		  -flogi_node_wwn_increment 00:00:00:00:00:00:00:00 \
		  -flogi_source_oui 0E.FC.00 \
		  -flogi_plogi_target_name {} \
		  -flogi_plogi_enabled False \
		  -flogi_fip_option_set_name {} \
		  -flogi_name_server_query False \
		  -flogi_fip_vlan_discovery_untagged True \
		  -flogi_state_change_registration_option kFabricDetected \
		  -flogi_plogi_mesh_mode one-to-one \
		  -flogi_fip_solicit_timeout 60 \
		  -flogi_name_server_query_command kGidA \
		  -vlan_range_id_incr_mode 2 \
		  -mac_range_mac AA:BB:CD:00:00:00 \
		  -mac_range_mtu 1500 \
		  -mac_range_count 1 \
		  -mac_range_increment_by 00:00:00:00:00:01 \
		  -mac_range_name MAC-R6 \
		  -mac_range_enabled True \
		  -vlan_range_vlan_id_info  { \
						  { \
							-priority 1 \
							-unique_count 4094 \
							-tpid 0x8100 \
							-increment 1 \
							-name VLAN-1 \
							-enabled False \
							-increment_step 1 \
							-first_id 1 \
						    } \
						  { \
							-priority 1 \
							-unique_count 4094 \
							-tpid 0x8100 \
							-increment 1 \
							-name VLAN-2 \
							-enabled False \
							-increment_step 1 \
							-first_id 1 \
						    } \
					      } \
		  -vlan_range_enabled False \
		  -flogi_count 1 \
		  -flogi_prli_enabled False \
		  -flogi_name_server_query_parameter_type kPortIdentifier \
		  -flogi_fip_addressing_mode fabric-provided \
		  -flogi_fip_destination_mac_address aa:bb:cc:00:00:00 \
		  -flogi_state_change_registration False \
		  -flogi_name_server_registration True \
		  -flogi_source_oui_increment 00.00.01 \
		  -flogi_enabled True \
		  -flogi_fip_enabled True \
		  -flogi_fip_vendor_id AA:BB:CC:DD:EE:FF:11:22 \
		  -flogi_plogi_dest_id 01.B6.69 \
		 ]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
    puts "\nError: fcoe_config on $port1"
    exit
}

set fcoe_clientHandle [keylget _result_ handles]

puts "\n---- fcoe_clientHandle ----\n"

puts "\n--- fcoe client status: [KeylPrint _result_] ---\n"

puts "\nSleeping for 40 seconds for fcoe ports to finish reapplying ..."
after 45000

puts "\nConfiguring fcoe_client_options_config ..."
# //vport/protocolStack/fcoeClientOptions
set _result_ [::ixia::fcoe_client_options_config  \
		  -mode create \
		  -parent_handle $port1 \
		  -style //vport/protocolStack \
		  -max_packets_per_second 500 \
		  -associates [list /vport:1/protocolStack] \
		  -override_global_rate False \
		  -setup_rate 100 \
		  -teardown_rate 100 \
		 ]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
    puts "\nError: fcoe_client_options_config"
    exit
}

puts "\nConfiguring fcoe_fwd_globals_config ..."
# //globals/protocolStack/fcoeFwdGlobals
set _result_ [::ixia::fcoe_fwd_globals_config  \
		  -mode create \
		  -retry_interval 2 \
		  -accept_partial_config False \
		  -max_retries 5 \
		  -dcbx_timeout 60 \
		  -fip_clear_vlink_with_port_ids True \
		  -max_packets_per_second 500 \
		 ]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
    puts "\nError:"
    exit
}

puts "\nStarting fcoe protocol ..."
set r [::ixia::test_control -action start_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $r
}

puts "\nConfiguring traffic_config ..."
# src_handle : ::ixNet::OBJ-/vport:1/protocolStack
# dst_handle : ::ixNet::OBJ-/vport:2/protocolStack
set trafficConfig [::ixia::traffic_config\
		       -mode create \
		       -emulation_src_handle ::ixNet::OBJ-/vport:1/protocolStack \
		       -emulation_dst_handle ::ixNet::OBJ-/vport:2/protocolStack \
		       -circuit_endpoint_type fcoe \
		       -track_by  "traffic_item flowGroup0" \
		       -name "TrafficItem_1" \
		       -bidirectional 1 \
		       -rate_percent 10 \
		       -pkts_per_burst 10000 \
		       -transmit_mode single_burst \
		       -frame_size 100 \
		      ]

if {[keylget trafficConfig status] != $::SUCCESS}   {
    puts "FAIL:  Traffic Config"
}

