#!/usr/bin/tclsh

# Description
#
# This fcoe sample script is using two Ixia back-2-back ports.
# On one port is the fcoe forwarder.
# The other port is the fcoe client.
# Configure fcoe forwader first.
# Then confgure fcoe client.
# At this point, must wait for fcoe ports to reapply. Sleeping for 45 seconds.
#
# For traffic_config emulation src/dst handles, must be in this format:
#     ::ixNet::OBJ-/vport:1/protocolStack
# 

package require Ixia
source /home/hgee/Dropbox/MyIxiaWork/IxNet_tclApi.tcl

set ixNetworkTclServer 192.168.70.127
set chassisIp 10.219.116.72
set portList [list 1/1 1/2]
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
# provide ixnetwork_tcl_server parameter to ::ixia::connect
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
set vportList [keylget connect_status vport_protocols_handle]
set port1Vport [lindex $vportList 0]
set port2Vport [lindex $vportList 1]

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
		  -mac_range_count 1 \
		  -mac_range_mac AA:BB:CC:00:00:00 \
		  -mac_range_name MAC-R5 \
		  -mac_range_increment_by 00:00:00:00:00:01 \
		  -mac_range_mtu 1500 \
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
		  -mac_range_mac AA:BB:CD:00:00:00 \
		  -mac_range_mtu 1500 \
		  -mac_range_count 1 \
		  -mac_range_increment_by 00:00:00:00:00:01 \
		  -mac_range_name MAC-R6 \
		  -mac_range_enabled True \
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
		       -emulation_src_handle $port1Vport \
		       -emulation_dst_handle $port2Vport \
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

StartTrafficHlt

set stats [GetStats]
puts "\n[KeylPrint stats]"
