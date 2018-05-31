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
#    This sample configures PPPoX Client and Server protocols and retrieves    #
#    statistics.				                                               #
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
	
	my $port_handles = ixiangpf::status_item('vport_list');
	my @port_handles_list = split(/ /,$port_handles);
	my @topology_1_ports = ($port_handles_list[0]);
	my @topology_2_ports = ($port_handles_list[2]);

	# Create the PPP server topology
	print "\n\nCreating PPP servers...";
	
    my $topology_1_status = ixiangpf::topology_config ({
        topology_name      => "PPP Servers Topology",
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
        topology_handle              => "$topology_1_handle",
        device_group_name            => "PPP Servers",
        device_group_multiplier      => "2",
        device_group_enabled         => "1",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $deviceGroup_1_handle = ixiangpf::status_item('device_group_handle');
       
    my $ethernet_1_status = ixiangpf::interface_config ({
        protocol_handle              => $deviceGroup_1_handle,
        mtu                          => "1500",
        vlan                         => "0",
        use_vpn_parameters           => "0",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $ethernet_1_handle = ixiangpf::status_item('ethernet_handle');
       
    my $multivalue_7_status = ixiangpf::multivalue_config ({
        pattern                 => "single_value",
        single_value            => "0",
        nest_step               => "1",
        nest_owner              => "$topology_1_handle",
        nest_enabled            => "0",
        overlay_value           => "1",
        overlay_value_step      => "0",
        overlay_index           => "1",
        overlay_index_step      => "0",
        overlay_count           => "1",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_7_handle = ixiangpf::status_item('multivalue_handle');
    
    
    my $multivalue_9_status = ixiangpf::multivalue_config ({
        pattern                 => "single_value",
        single_value            => "0",
        nest_step               => "1",
        nest_owner              => "$topology_1_handle",
        nest_enabled            => "0",
        overlay_value           => "1",
        overlay_value_step      => "0",
        overlay_index           => "2",
        overlay_index_step      => "0",
        overlay_count           => "1",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_9_handle = ixiangpf::status_item('multivalue_handle');
    
    my $pppoxserver_1_status = ixiangpf::pppox_config ({
        port_role                            => "network",
        handle                               => $ethernet_1_handle,
        enable_mru_negotiation               => "0",
        desired_mru_rate                     => "1492",
        enable_max_payload                   => "0",
        server_ipv6_ncp_configuration        => "clientmay",
        server_ipv4_ncp_configuration        => "clientmay",
        num_sessions                         => "5",
        auth_req_timeout                     => "10",
        config_req_timeout                   => "10",
        echo_req                             => "0",
        echo_rsp                             => "1",
        ip_cp                                => "ipv6_cp",
        ipcp_req_timeout                     => "10",
        max_auth_req                         => "20",
        max_terminate_req                    => "3",
        password                             => "pwd",
        username                             => "user",
        mode                                 => "add",
        auth_mode                            => "pap",
        echo_req_interval                    => "10",
        max_configure_req                    => "3",
        max_ipcp_req                         => "3",
        ac_name                              => "ixia",
        enable_domain_group_map              => "0",
        enable_server_signal_iwf             => "0",
        enable_server_signal_loop_char       => "0",
        enable_server_signal_loop_encap      => "0",
        enable_server_signal_loop_id         => "0",
        ipv6_pool_prefix_len                 => "48",
        ppp_local_ip_step                    => "0.0.0.1",
        ppp_local_iid_step                   => "1",
        ppp_peer_iid_step                    => "1",
        ppp_peer_ip_step                     => "0.0.0.1",
        send_dns_options                     => "$multivalue_7_handle",
        server_dns_options                   => "disable_extension",
        server_dns_primary_address           => "10.10.10.10",
        server_dns_secondary_address         => "11.11.11.11",
        server_netmask_options               => "disable_extension",
        server_netmask                       => "255.255.255.0",
        server_wins_options                  => "disable_extension",
        server_wins_primary_address          => "10.10.10.10",
        server_wins_secondary_address        => "11.11.11.11",
        accept_any_auth_value                => "$multivalue_9_handle",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $pppoxserver_1_handle = ixiangpf::status_item('pppox_server_handle');
	
	print "\nDONE creating PPP servers.\n";
    
	# Create PPP Clients
	print "\n\nCreating PPP clients...\n";
	
    my $topology_2_status = ixiangpf::topology_config ({
        topology_name      => "PPP Clients Topology",
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
        device_group_name            => "PPP Clients",
        device_group_multiplier      => "10",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $deviceGroup_2_handle = ixiangpf::status_item('device_group_handle');       
	
    my $multivalue_12_status = ixiangpf::multivalue_config ({
        pattern                      => "repeatable_random",
        nest_step                    => "1",
        nest_owner                   => "$topology_2_handle",
        nest_enabled                 => "0",
        repeatable_random_seed       => "1",
        repeatable_random_count      => "4000000",
        repeatable_random_fixed      => "5",
        repeatable_random_mask       => "25",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_12_handle = ixiangpf::status_item('multivalue_handle');
    
    my $pppoxclient_1_status = ixiangpf::pppox_config ({
        port_role                            => "access",
        handle                               => $deviceGroup_2_handle,
        unlimited_redial_attempts            => "0",
        enable_mru_negotiation               => "0",
        desired_mru_rate                     => "1492",
        max_payload                          => "1700",
        enable_max_payload                   => "0",
        client_ipv6_ncp_configuration        => "learned",
        client_ipv4_ncp_configuration        => "learned",
        lcp_enable_accm                      => "0",
        lcp_accm                             => "ffffffff",
        ac_select_mode                       => "first_responding",
        auth_req_timeout                     => "10",
        config_req_timeout                   => "10",
        echo_req                             => "0",
        echo_rsp                             => "1",
        ip_cp                                => "ipv6_cp",
        ipcp_req_timeout                     => "10",
        max_auth_req                         => "20",
        max_padi_req                         => "5",
        max_padr_req                         => "5",
        max_terminate_req                    => "3",
        padi_req_timeout                     => "10",
        padr_req_timeout                     => "10",
        password                             => "pwd",
        chap_secret                          => "secret",
        username                             => "user",
        chap_name                            => "user",
        mode                                 => "add",
        auth_mode                            => "pap",
        echo_req_interval                    => "10",
        max_configure_req                    => "3",
        max_ipcp_req                         => "3",
        actual_rate_downstream               => "10",
        actual_rate_upstream                 => "10",
        data_link                            => "ethernet",
        enable_domain_group_map              => "0",
        enable_client_signal_iwf             => "0",
        enable_client_signal_loop_char       => "0",
        enable_client_signal_loop_encap      => "0",
        enable_client_signal_loop_id         => "0",
        intermediate_agent_encap1            => "untagged_eth",
        intermediate_agent_encap2            => "na",
        ppp_local_iid                        => "0:11:11:11:0:0:0:1",
        ppp_local_ip                         => "1.1.1.1",
        redial_timeout                       => "10",
        service_type                         => "any",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $pppoxclient_1_handle = ixiangpf::status_item('pppox_client_handle');
    	
    my $multivalue_13_status = ixiangpf::multivalue_config ({
        pattern                => "distributed",
        distributed_value      => "1",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_13_handle = ixiangpf::status_item('multivalue_handle');
    
    my $multivalue_14_status = ixiangpf::multivalue_config ({
        pattern                => "distributed",
        distributed_value      => "10",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_14_handle = ixiangpf::status_item('multivalue_handle');
    
    my $multivalue_15_status = ixiangpf::multivalue_config ({
        pattern                => "distributed",
        distributed_value      => "10",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
    my $multivalue_15_handle = ixiangpf::status_item('multivalue_handle');
    
    my $pppoxclient_2_status = ixiangpf::pppox_config ({
        port_role                                => "access",
        handle                                   => "/globals",
        mode                                     => "add",
        ipv6_global_address_mode                 => "icmpv6",
        ra_timeout                               => "30",
        create_interfaces                        => "0",
        attempt_rate                             => "200",
        attempt_max_outstanding                  => "400",
        attempt_interval                         => "1000",
        attempt_enabled                          => "1",
        attempt_scale_mode                       => "port",
        disconnect_rate                          => "200",
        disconnect_max_outstanding               => "400",
        disconnect_interval                      => "1000",
        disconnect_enabled                       => "1",
        disconnect_scale_mode                    => "port",
        enable_session_lifetime                  => "0",
        min_lifetime                             => "$multivalue_13_handle",
        max_lifetime                             => "$multivalue_14_handle",
        enable_session_lifetime_restart          => "0",
        max_session_lifetime_restarts            => "$multivalue_15_handle",
        unlimited_session_lifetime_restarts      => "0",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\nDONE creating and configuring PPP clients.\n";
	
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
	
	print "\n\nSleeping for 60 seconds to allow sessions to get negociated...";
	
	# Sleep for 60 seconds
	sleep(60);

	print "\nDONE waiting for protocol start.\n";
	
	# Get statistics
	print "\n\nGetting statistics for PPP...\n";

	my $pppox_clients = $pppoxclient_1_handle;
	$_result_ = ixiangpf::pppox_stats({
        handle				=>	$pppox_clients,
		mode				=>	'aggregate',
		execution_timeout	=>	60,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\nThe aggregate statistics for the PPP clients are:\n";
	my $ppp_client_aggregate_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($ppp_client_aggregate_stats);
	print "\n";	
	
	$_result_ = ixiangpf::pppox_stats({
        handle				=>	$pppox_clients,
		mode				=>	'session',
		execution_timeout	=>	60,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\nThe per-session statistics for the PPP clients are:\n";
	my $ppp_client_session_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($ppp_client_session_stats);
	print "\n";	
    
	my $pppox_servers = $pppoxserver_1_handle;
	$_result_ = ixiangpf::pppox_stats({
        handle				=>	$pppox_servers,
		mode				=>	'aggregate',
		execution_timeout	=>	60,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\nThe aggregate statistics for the PPP servers are:\n";
	my $ppp_server_aggregate_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($ppp_server_aggregate_stats);
	print "\n";		
	
	$_result_ = ixiangpf::pppox_stats({
        handle				=>	$pppox_servers,
		mode				=>	'session',
		execution_timeout	=>	60,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\nThe per-session statistics for the PPP servers are:\n";
	my $ppp_server_session_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($ppp_server_session_stats);
	print "\n";	
	
	
	$_result_ = ixiangpf::pppox_stats({
		mode				=>	'session_all',
		execution_timeout	=>	60,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\nThe per-session statistics for the PPP protocol are:\n";
	my $ppp_session_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($ppp_session_stats);
	print "\n";	
    
	print "\nDONE getting PPP statistics.\n";
	
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
}

my $test_result = main(@ARGV);
print "\nTest execution complete.\nStatus: $test_result\n";
    