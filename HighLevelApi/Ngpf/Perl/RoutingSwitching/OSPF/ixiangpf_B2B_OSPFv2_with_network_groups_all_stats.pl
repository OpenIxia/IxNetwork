################################################################################
# Version 1																	   #
# Author: agrigoroaia														   #
#																			   #
# Copyright © 1997 - 2013 by IXIA											   #
# All Rights Reserved.														   #
#																			   #
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
#    This sample configures OSPFv2 routers and retrieves statistics.	       #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################
################################################################################
#                                                                              #
# 							 SCRIPT DETAILS                                    #
# 							 ==============                                    #
#                                                                              #
# Edit the following lines and replace %HLT_PATH% with the actual			   #
# installation path for you HLT API release									   #
#                                                                              #
# use lib "%HLT_PATH%/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.20";  #
# use lib "%HLT_PATH%/TclScripts/lib/hltapi/library/common/ixiangpf/perl";	   #
#                                                                              #
#                                                                              #
# Ensure that Perl is installed on the machine that hosts the IxNetwork		   #
# server.																	   #
#                                                                              #
# Enable low level Perl support for IxNetwork by copying IxNetwork.pm from	   #
#	%IXN_INSTALL_PATH%/API/Perl/IxNetwork.pm								   #
# to																		   #
#	%DEFAULT_PERL_DIR%%/site/lib											   #
#                                                                              #
#                                                                              #
# Run the sample script by calling											   #
# 	perl dhcp.pl															   #
#		-ixnetwork_server 10.0.0.1 -chassis 10.0.0.100 -port_list "1/1 1/2"	   #
#                                                                              #
# The following command line arguments are required							   #
#                                                                              #
#	-ixnetwork_server														   #
#	 The address of the IxNetwork server that will be used to execute		   #
#	 the script																   #
#                                                                              #
#	-chassis																   #
#	 The address of the chassis that will be used to execute the script		   #
#                                                                              #
#	-port_list																   #
#	 A quoted, space separated list that lists the ports that will be used by  #
#	 the current script.													   #
#	 The ports are specified using the regular HLT API syntax of:			   #
#		 %CARD_NO%/%PORT_NO%												   #
#                                                                              #
#                                                                              #
# The current script requires:											 	   #
#	- an IxNetwork 7.20 (or newer) server									   #
#	- a compatible IXIA chassis with 2 B2B ports							   #
#                                                                              #
################################################################################

use ixiahlt;
use ixiangpf;

use strict;
use warnings;

sub main {

	my @inputArgs = @_;
	
	# Parse the input arguments looking for the IxNetwork server, chassis and ports
	my $index = 0;
	++$index until $inputArgs[$index] eq '-ixnetwork_server' or $index > $#inputArgs;
	my $ixNetServer = $inputArgs[$index+1];
	
	$index = 0;
	++$index until $inputArgs[$index] eq '-chassis' or $index > $#inputArgs;
	my $chassis = $inputArgs[$index+1];
	
	$index = 0;
	++$index until $inputArgs[$index] eq '-port_list' or $index > $#inputArgs;
	my $ports = $inputArgs[$index+1];
	my @port_list = split(/ /, $ports);

	# Initialize variables that are used to get the command status
	my $_result_ = '';
	my @status_keys = ();
	my $command_status = '';    
	
	# Connect and add chassis & ports
	$_result_ = ixiangpf::connect({
		reset                => '1',
		port_list	         => \@port_list,
		device				 => $chassis,
		ixnetwork_tcl_server => $ixNetServer,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}

	# Create source topology
	print "\n\nCreating a topology which will advertise multiple OSPF routes...\n";
	
	my $port_handles = ixiangpf::status_item('vport_list');
	my @port_handles_list = split(/ /,$port_handles);
	my @topology_1_ports = ($port_handles_list[0]);
	my @topology_2_ports = ($port_handles_list[2]);
	
	my $topology_1_status = ixiangpf::topology_config ({
		topology_name      => 'Source Topology',
        port_handle        => \@topology_1_ports,
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $topology_1_handle = ixiangpf::status_item('topology_handle');
    
    my $device_group_1_status = ixiangpf::topology_config ({
        topology_handle              => $topology_1_handle,
        device_group_name            => 'OSPF Advertising Servers',
        device_group_multiplier      => '2',
        device_group_enabled         => '1',
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $deviceGroup_1_handle = ixiangpf::status_item('device_group_handle');
    
    my $multivalue_1_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "00.11.01.00.00.01",
        counter_step           => "00.00.00.00.00.01",
        counter_direction      => "increment",
        nest_step              => "00.00.01.00.00.00",
        nest_owner             => "$topology_1_handle",
        nest_enabled           => "1",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_1_handle = ixiangpf::status_item('multivalue_handle');
    
    my $ethernet_1_status = ixiangpf::interface_config ({
        protocol_name                => "Ethernet 1",
        protocol_handle              => "$deviceGroup_1_handle",
        mtu                          => "1500",
        src_mac_addr                 => "$multivalue_1_handle",
        vlan                         => "0",
        vlan_id                      => "1",
        vlan_id_step                 => "0",
        vlan_id_count                => "1",
        vlan_tpid                    => "0x8100",
        vlan_user_priority           => "0",
        vlan_user_priority_step      => "0",
        use_vpn_parameters           => "0",
        site_id                      => "0",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $ethernet_1_handle = ixiangpf::status_item('ethernet_handle');
    
    my $ipv4_1_status = ixiangpf::interface_config ({
        protocol_name                => "IPv4 1",
        protocol_handle              => "$ethernet_1_handle",
        ipv4_resolve_gateway         => "1",
        ipv4_manual_gateway_mac      => "00.00.00.00.00.01",
        gateway                      => "1.0.0.2",
        gateway_step                 => "0.0.0.0",
        intf_ip_addr                 => "1.0.0.1",
        intf_ip_addr_step            => "0.0.0.0",
        netmask                      => "255.255.255.0",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $ipv4_1_handle = ixiangpf::status_item('ipv4_handle');
    
    my $multivalue_2_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "0",
        counter_step           => "0",
        counter_direction      => "increment",
        nest_step              => "1",
        nest_owner             => "$topology_1_handle",
        nest_enabled           => "0",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_2_handle = ixiangpf::status_item('multivalue_handle');
    
    my $ospfv2_1_status = ixiangpf::emulation_ospf_config ({
        handle                                                    => "$ipv4_1_handle",
        area_id                                                   => "0.0.0.0",
        area_id_as_number                                         => "0",
        area_id_type                                              => "ip",
        authentication_mode                                       => "null",
        dead_interval                                             => "40",
        demand_circuit                                            => "0",
        graceful_restart_enable                                   => "0",
        hello_interval                                            => "10",
        router_interface_active                                   => "1",
        enable_fast_hello                                         => "0",
        hello_multiplier                                          => "2",
        max_mtu                                                   => "1500",
        protocol_name                                             => "OSPFv2-IF 1",
        router_active                                             => "1",
        router_asbr                                               => "0",
        do_not_generate_router_lsa                                => "0",
        router_abr                                                => "0",
        inter_flood_lsupdate_burst_gap                            => "33",
        lsa_refresh_time                                          => "1800",
        lsa_retransmit_time                                       => "5",
        max_ls_updates_per_burst                                  => "1",
        oob_resync_breakout                                       => "0",
        interface_cost                                            => "10",
        lsa_discard_mode                                          => "$multivalue_2_handle",
        md5_key_id                                                => "1",
        network_type                                              => "ptop",
        neighbor_router_id                                        => "0.0.0.0",
        type_of_service_routing                                   => "0",
        external_capabilities                                     => "1",
        multicast_capability                                      => "0",
        nssa_capability                                           => "0",
        external_attribute                                        => "0",
        opaque_lsa_forwarded                                      => "0",
        unused                                                    => "0",
        router_id                                                 => "1.0.0.1",
        router_id_step                                            => "0.0.0.0",
        router_priority                                           => "2",
        te_enable                                                 => "0",
        te_max_bw                                                 => "0",
        te_max_resv_bw                                            => "0",
        te_unresv_bw_priority0                                    => "0",
        te_unresv_bw_priority1                                    => "0",
        te_unresv_bw_priority2                                    => "0",
        te_unresv_bw_priority3                                    => "0",
        te_unresv_bw_priority4                                    => "0",
        te_unresv_bw_priority5                                    => "0",
        te_unresv_bw_priority6                                    => "0",
        te_unresv_bw_priority7                                    => "0",
        te_metric                                                 => "0",
        te_admin_group                                            => "0",
        validate_received_mtu                                     => "1",
        graceful_restart_helper_mode_enable                       => "0",
        strict_lsa_checking                                       => "1",
        support_reason_sw_restart                                 => "1",
        support_reason_sw_reload_or_upgrade                       => "1",
        support_reason_switch_to_redundant_processor_control      => "1",
        support_reason_unknown                                    => "1",
        mode                                                      => "create",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $ospfv2_1_handle = ixiangpf::status_item('ospfv2_handle');
    
    my $multivalue_3_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "200.1.0.0",
        counter_step           => "0.1.0.0",
        counter_direction      => "increment",
        nest_step              => "0.0.0.1,0.1.0.0",
        nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
        nest_enabled           => "0,1",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_3_handle = ixiangpf::status_item('multivalue_handle');
    
    my $network_group_1_status = ixiangpf::emulation_ospf_network_group_config ({
        handle                               => "$ospfv2_1_handle",
        type                                 => "ipv4-prefix",
        multiplier                           => "50",
        enable_device                        => "1",
        connected_to_handle                  => "$ethernet_1_handle",
        ipv4_prefix_network_address          => "$multivalue_3_handle",
        ipv4_prefix_length                   => "24",
        ipv4_prefix_number_of_addresses      => "1",
        ipv4_prefix_metric                   => "0",
        ipv4_prefix_active                   => "1",
        ipv4_prefix_allow_propagate          => "0",
        ipv4_prefix_route_origin             => "another_area",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $networkGroup_1_handle = ixiangpf::status_item('network_group_handle');
    
    
    my $multivalue_4_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "201.1.0.0",
        counter_step           => "0.1.0.0",
        counter_direction      => "increment",
        nest_step              => "0.0.0.1,0.1.0.0",
        nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
        nest_enabled           => "0,1",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_4_handle = ixiangpf::status_item('multivalue_handle');
    
    my $network_group_2_status = ixiangpf::emulation_ospf_network_group_config ({
        handle                               => "$ospfv2_1_handle",
        type                                 => "ipv4-prefix",
        multiplier                           => "2",
        enable_device                        => "1",
        connected_to_handle                  => "$ethernet_1_handle",
        ipv4_prefix_network_address          => "$multivalue_4_handle",
        ipv4_prefix_length                   => "24",
        ipv4_prefix_number_of_addresses      => "1",
        ipv4_prefix_metric                   => "0",
        ipv4_prefix_active                   => "1",
        ipv4_prefix_allow_propagate          => "0",
        ipv4_prefix_route_origin             => "another_area",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $networkGroup_2_handle = ixiangpf::status_item('network_group_handle');
    
    
    my $multivalue_5_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "202.1.0.0",
        counter_step           => "0.1.0.0",
        counter_direction      => "increment",
        nest_step              => "0.0.0.1,0.1.0.0",
        nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
        nest_enabled           => "0,1",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_5_handle = ixiangpf::status_item('multivalue_handle');
    
    my $network_group_3_status = ixiangpf::emulation_ospf_network_group_config ({
        handle                               => "$ospfv2_1_handle",
        type                                 => "ipv4-prefix",
        multiplier                           => "5",
        enable_device                        => "1",
        connected_to_handle                  => "$ethernet_1_handle",
        ipv4_prefix_network_address          => "$multivalue_5_handle",
        ipv4_prefix_length                   => "24",
        ipv4_prefix_number_of_addresses      => "1",
        ipv4_prefix_metric                   => "0",
        ipv4_prefix_active                   => "1",
        ipv4_prefix_allow_propagate          => "0",
        ipv4_prefix_route_origin             => "another_area",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $networkGroup_3_handle = ixiangpf::status_item('network_group_handle');
    
	print "\nDONE creating source topology.\n";
	
    # Create destination topology
	print "\n\nCreating a destination topology containing only OSPF routers...\n";
    
	my $topology_2_status = ixiangpf::topology_config ({
        topology_name      => 'Destination Topology',
        port_handle        => \@topology_2_ports,
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $topology_2_handle = ixiangpf::status_item('topology_handle');
    
    my $device_group_2_status = ixiangpf::topology_config ({
        topology_handle              => $topology_2_handle,
        device_group_name            => 'OSPF Standalone Server',
        device_group_multiplier      => "1",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $deviceGroup_2_handle = ixiangpf::status_item('device_group_handle');
    
    my $multivalue_6_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "00.12.01.00.00.01",
        counter_step           => "00.00.00.00.00.01",
        counter_direction      => "increment",
        nest_step              => "00.00.01.00.00.00",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "1",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_6_handle = ixiangpf::status_item('multivalue_handle');
    
    my $ethernet_2_status = ixiangpf::interface_config ({
        protocol_name                => "Ethernet 2",
        protocol_handle              => "$deviceGroup_2_handle",
        mtu                          => "1500",
        src_mac_addr                 => "$multivalue_6_handle",
        vlan                         => "0",
        vlan_id                      => "1",
        vlan_id_step                 => "0",
        vlan_id_count                => "1",
        vlan_tpid                    => "0x8100",
        vlan_user_priority           => "0",
        vlan_user_priority_step      => "0",
        use_vpn_parameters           => "0",
        site_id                      => "0",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $ethernet_2_handle = ixiangpf::status_item('ethernet_handle');
    
    my $ipv4_2_status = ixiangpf::interface_config ({
        protocol_name                => "IPv4 2",
        protocol_handle              => "$ethernet_2_handle",
        ipv4_resolve_gateway         => "1",
        ipv4_manual_gateway_mac      => "00.00.00.00.00.01",
        gateway                      => "1.0.0.1",
        gateway_step                 => "0.0.0.0",
        intf_ip_addr                 => "1.0.0.2",
        intf_ip_addr_step            => "0.0.0.0",
        netmask                      => "255.255.255.0",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $ipv4_2_handle = ixiangpf::status_item('ipv4_handle');
    
    my $multivalue_7_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "0",
        counter_step           => "0",
        counter_direction      => "increment",
        nest_step              => "1",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "0",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_7_handle = ixiangpf::status_item('multivalue_handle');
    
    my $ospfv2_2_status = ixiangpf::emulation_ospf_config ({
        handle                                                    => "$ipv4_2_handle",
        area_id                                                   => "0.0.0.0",
        area_id_as_number                                         => "0",
        area_id_type                                              => "ip",
        authentication_mode                                       => "null",
        dead_interval                                             => "40",
        demand_circuit                                            => "0",
        graceful_restart_enable                                   => "0",
        hello_interval                                            => "10",
        router_interface_active                                   => "1",
        enable_fast_hello                                         => "0",
        hello_multiplier                                          => "2",
        max_mtu                                                   => "1500",
        protocol_name                                             => "OSPFv2-IF 2",
        router_active                                             => "1",
        router_asbr                                               => "0",
        do_not_generate_router_lsa                                => "0",
        router_abr                                                => "0",
        inter_flood_lsupdate_burst_gap                            => "33",
        lsa_refresh_time                                          => "1800",
        lsa_retransmit_time                                       => "5",
        max_ls_updates_per_burst                                  => "1",
        oob_resync_breakout                                       => "0",
        interface_cost                                            => "10",
        lsa_discard_mode                                          => "$multivalue_7_handle",
        md5_key_id                                                => "1",
        network_type                                              => "ptop",
        neighbor_router_id                                        => "0.0.0.0",
        type_of_service_routing                                   => "0",
        external_capabilities                                     => "1",
        multicast_capability                                      => "0",
        nssa_capability                                           => "0",
        external_attribute                                        => "0",
        opaque_lsa_forwarded                                      => "0",
        unused                                                    => "0",
        router_id                                                 => "1.0.0.2",
        router_id_step                                            => "0.0.0.0",
        router_priority                                           => "2",
        te_enable                                                 => "0",
        te_max_bw                                                 => "0",
        te_max_resv_bw                                            => "0",
        te_unresv_bw_priority0                                    => "0",
        te_unresv_bw_priority1                                    => "0",
        te_unresv_bw_priority2                                    => "0",
        te_unresv_bw_priority3                                    => "0",
        te_unresv_bw_priority4                                    => "0",
        te_unresv_bw_priority5                                    => "0",
        te_unresv_bw_priority6                                    => "0",
        te_unresv_bw_priority7                                    => "0",
        te_metric                                                 => "0",
        te_admin_group                                            => "0",
        validate_received_mtu                                     => "1",
        graceful_restart_helper_mode_enable                       => "0",
        strict_lsa_checking                                       => "1",
        support_reason_sw_restart                                 => "1",
        support_reason_sw_reload_or_upgrade                       => "1",
        support_reason_switch_to_redundant_processor_control      => "1",
        support_reason_unknown                                    => "1",
        mode                                                      => "create",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $ospfv2_2_handle = ixiangpf::status_item('ospfv2_handle');
    
	print "\nDONE creating destination topology.\n";
	
	# Start protocols
	print "\n\nStarting protocols...\n";
	
	$_result_ = ixiangpf::test_control({
		action	=>	'start_protocol',
		handle	=>	$topology_1_handle,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}	
	
	$_result_ = ixiangpf::test_control({
		action	=>	'start_protocol',
		handle	=>	$topology_2_handle,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\n\nSleeping for 30 seconds to allow OSPF routes to be advertised...";
	
	# Sleep for 30 seconds
	sleep(30);

	print "\nDONE waiting for protocol start and route advertisment.\n";
	
	# Get statistics
	print "\n\nGetting statistics for OSPF stacks...\n";

	$_result_ = ixiangpf::emulation_ospf_info({
		handle				=>	$ospfv2_1_handle,
		mode				=>	'aggregate_stats',
		execution_timeout	=>	'60',
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\nThe aggregated OSPF statistics for $ospfv2_1_handle are:\n";
	my $ospf_1_aggregate_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($ospf_1_aggregate_stats);
	print "\n";

	$_result_ = ixiangpf::emulation_ospf_info({
		handle				=>	$ospfv2_1_handle,
		mode				=>	'session',
		execution_timeout	=>	'60',
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\nThe per-session OSPF statistics for $ospfv2_1_handle are:\n";
	my $ospf_1_session_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($ospf_1_session_stats);
	print "\n";
	
	$_result_ = ixiangpf::emulation_ospf_info({
		handle				=>	$ospfv2_2_handle,
		mode				=>	'learned_info',
		execution_timeout	=>	'60',
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\nThe learned info for the standalone OSPF router is:\n";
	my $ospf_1_session_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($ospf_1_session_stats);
	print "\n";	
    
	print "\nDONE getting OSPF statistics.\n";
	
	# Stop all and clean up
	print "\n\nStopping all protocols...\n";
	$_result_ = ixiangpf::test_control({
		action	=>	'stop_all_protocols',
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}

	print "\n\nSleeping for 30 seconds to allow them to go down...";
	
	# Sleep for 30 seconds
	sleep(30);

	print "\nDONE waiting for protocol stop.\n";

	# Remove all topologies
	print "\n\nRemoving topologies...\n";
	
	$_result_ = ixiangpf::topology_config({
		mode			=>	'destroy',
		topology_handle	=>	$topology_1_handle,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}

	$_result_ = ixiangpf::topology_config({
		mode			=>	'destroy',
		topology_handle	=>	$topology_2_handle,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}

	print "\nDONE removing topologies.\n";
	
	# Clean up the session
	print "\n\nPerforming final session cleanup...\n";
	
	$_result_ = ixiangpf::cleanup_session();
	
	print "\nSession cleanup completed.\n";

	return "SUCCESS";	
	return "SUCCESS";
}

my $test_result = main(@ARGV);
print "\nTest execution complete.\nStatus: $test_result\n";
    