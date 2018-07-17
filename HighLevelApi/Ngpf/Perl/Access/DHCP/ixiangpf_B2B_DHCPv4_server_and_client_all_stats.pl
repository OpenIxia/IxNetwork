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
#    This sample configures DHCPv4 Client and Server protocols and retrieves   #
#    statistics	.				                                               #
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
use IxNetwork;

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
	my @topology_2_ports = ($port_handles_list[1]);

	# Create the client topology
	print "\n\nCreating DHCPv4 clients...\n";
	
	my $client_dg_name = 'DHCPv4 Clients';
	$_result_ = ixiangpf::topology_config({
		port_handle				=>	\@topology_1_ports,
		topology_name			=>	'Client Topology',
		device_group_multiplier	=>	'50',
		device_group_name		=>	$client_dg_name,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}

	my $dg_1_handle = ixiangpf::status_item('device_group_handle');
	my $t_1_handle = ixiangpf::status_item('topology_handle');

	$_result_ = ixiangpf::emulation_dhcp_group_config({
		handle						=>	$dg_1_handle,
		dhcp_range_ip_type			=>	'ipv4',
		dhcp_range_renew_timer		=>	'0',
		dhcp_range_server_address	=>	'10.10.0.1',
		use_rapid_commit			=>	'0',
        dhcp_range_use_first_server	=>	'1',
        dhcp4_broadcast				=>	'0',		
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}

	my $dhcp_clients = ixiangpf::status_item('dhcpv4client_handle');
	
	# Modify the client protocol options
	print "\nUpdating DHCP client configurations...\n";
	
    my $dhcpv4client_3_status = ixiangpf::emulation_dhcp_config ({
        handle                             => "/globals",
        mode                               => "create",
        msg_timeout                        => "4",
        outstanding_releases_count         => "400",
        outstanding_session_count          => "400",
        release_rate                       => "200",
        request_rate                       => "200",
        retry_count                        => "3",
        client_port                        => "68",
        start_scale_mode                   => "port",
        stop_scale_mode                    => "port",
        interval_stop                      => "1000",
        interval_start                     => "1000",
        enable_restart                     => "0",
        enable_lifetime                    => "0",
        unlimited_restarts                 => "0",
        server_port                        => "67",
        msg_timeout_factor                 => "2",
        override_global_setup_rate         => "1",
        override_global_teardown_rate      => "1",
        ip_version                         => "4",
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}	

	# Modify the client stack
	my $dhcp_clients_count = 100;

	$_result_ = ixiangpf::emulation_dhcp_group_config({
		handle			=>	$dhcp_clients,
		mode			=>	'modify',
		num_sessions	=>	$dhcp_clients_count,
	});
		@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	print "\nDONE creating and configuring DHCP clients.";
	
	# Create the server topology
	print "\nCreating DHCP servers...\n";
	
	$_result_ = ixiangpf::topology_config({
		port_handle        		=>	\@topology_2_ports,
		topology_name			=>	'Server Topology',
		device_group_multiplier	=>	'2',
		device_group_name		=> 	'DHCP Servers',
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}

	my $dg_2_handle = ixiangpf::status_item('device_group_handle');
	my $t_2_handle = ixiangpf::status_item('topology_handle');
	
    $_result_ = ixiangpf::multivalue_config ({
        pattern			=>	'random',
        nest_step		=>	'00.00.00.00.00.01',
        nest_owner		=>	$t_2_handle,
        nest_enabled	=>	'0',
    });
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
    my $multivalue_handle = ixiangpf::status_item('multivalue_handle');	
	
    $_result_ = ixiangpf::interface_config ({
        protocol_handle			=>	$dg_2_handle,
        ipv4_resolve_gateway	=>	'0',
        ipv4_manual_gateway_mac	=>	$multivalue_handle,
        intf_ip_addr			=>	'10.10.0.1',
		intf_ip_addr_step		=>	'0.10.0.0',
    });	
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	my $ipv4_handle = ixiangpf::status_item('ipv4_handle');

	my $pool_start = '10.10.0.2';
	my $pool_step = '0.10.0.0';
	$_result_ = ixiangpf::emulation_dhcp_server_config({
		handle									=>	$ipv4_handle,
		mode									=>	'create',
		ip_version								=>	'4',
		dhcp_offer_router_address				=>	'10.10.0.1',
		dhcp_offer_router_address_inside_step	=>	'0.10.0.0',
		ip_dns1									=>	'8.8.8.8',
		ip_dns2									=>	'8.8.4.4',
		ipaddress_count							=>	'50',
		ipaddress_pool							=>	$pool_start,
		ipaddress_pool_inside_step				=>	$pool_step,
		ipaddress_pool_prefix_length			=>	'16',
		pool_address_increment					=>	'0.0.0.1',
		lease_time								=>	'86400',
		use_rapid_commit						=>	'0',
		echo_relay_info							=>	'1',
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}

	my $dhcp_servers = ixiangpf::status_item('dhcpv4server_handle');

	print "\nDONE creating and configuring DHCP servers.";
	
	# Create a low level IxNetwork connection
	print "\n\nChecking current configuration...\n";
	
	my $ixNetConnection = new IxNetwork();
	if (index($ixNetServer,':') > 0) {
		my @connect_options = split(/:/, $ixNetServer);
		$ixNetConnection->connect($connect_options[0], '-port', $connect_options[1]);
	} else {
		$ixNetConnection->connect($ixNetServer);
	}

	# Check server IP pool values
	my $objRef = $dhcp_servers . "/dhcp4ServerSessions";
	print "\nLooking at $objRef";
	
	my $ip_pool_mv = $ixNetConnection->getAttribute($objRef, '-ipAddress');
	
	$objRef = $ip_pool_mv . "/counter";	
	print "\nLookg at $objRef";
	
	my $poolStart = $ixNetConnection->getAttribute($objRef, '-start');
	my $poolStep = $ixNetConnection->getAttribute($objRef, '-step');
	if ($poolStart ne $pool_start || $poolStep ne $pool_step) {
		return "FAILED - Server IP pool was incorrectly configured. Expected the ip pool to be ($pool_start, $pool_step) and got ($poolStart, $poolStep).";
	}

	# Check number of clients
	my $dhcpClientsCount = $ixNetConnection->getAttribute($dhcp_clients, '-count');
	if ($dhcpClientsCount != $dhcp_clients_count) {
		return "FAILED - DHCP clients were incorrectly configured. Expected $dhcp_clients_count clients and got $dhcpClientsCount.";
	}

	print "\nDONE checking configuration.";
	
	# Start protocols
	print "\n\nStarting protocols...\n";
	
	$_result_ = ixiangpf::test_control({
		action	=>	'start_protocol',
		handle	=>	$dhcp_servers,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}	
	
	$_result_ = ixiangpf::test_control({
		action	=>	'start_protocol',
		handle	=>	$dhcp_clients,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\n\nSleeping for 30 seconds to allow the protocols to come up...";
	
	# Sleep for 10 seconds
	sleep(30);

	print "\nDONE waiting for protocol start.\n";
	
	# Get statistics
	print "\n\nGetting statistics for DHCP stacks...\n";
	
	$_result_ = ixiangpf::emulation_dhcp_server_stats({
		dhcp_handle			=>	$dhcp_servers,
		action				=>	'collect',
		execution_timeout	=>	'60',
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\nThe returned DHCPv4 server statistics are:\n";
	my $server_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($server_stats);
	print "\n";

	$_result_ = ixiangpf::emulation_dhcp_stats({
		handle				=>	$dhcp_clients,
		mode				=>	'aggregate_stats',
		dhcp_version		=>	'dhcp4',
		execution_timeout	=>	'60',
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\nThe aggragted DHCPv4 client statistics are:\n";
	my $client_aggregate_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($client_aggregate_stats);
	print "\n";
	
	if ($client_aggregate_stats->{$client_dg_name}->{'aggregate'}->{'status'} ne 'started') {
		return "FAILED - DHCP clients are not started.";
	}
	
	if ($client_aggregate_stats->{$client_dg_name}->{'aggregate'}->{'currently_bound'} != $dhcp_clients_count ) {
		return "FAILED - The numberof bound DHCP client sessions is incorrect. Expected $dhcp_clients_count ... got $client_aggregate_stats->{$client_dg_name}->{'aggregate'}->{'currently_bound'}";
	}
	
	$_result_ = ixiangpf::emulation_dhcp_stats({
		handle				=>	$dhcp_clients,
		mode				=>	'session',
		dhcp_version		=>	'dhcp4',
		execution_timeout	=>	'60',
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}
	
	print "\nThe per-session DHCPv4 client statistics are:\n";
	my $client_session_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($client_session_stats);
	print "\n";
	
	my @client_session_keys = keys(%$client_session_stats);
	my $expected_keys = $dhcp_clients_count + 1;
	my $actual_key_count = scalar(@client_session_keys);
	if ($actual_key_count != $expected_keys) {
		return "FAILED - Per-session statistics were returned for an incorrect number of sessions. Expected $expected_keys ... got $actual_key_count";
	}
	
	print "\nDONE getting DHCP statistics.\n";

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

	print "\n\nSleeping for 10 seconds to allow them to go down...";
	
	# Sleep for 10 seconds
	sleep(10);

	print "\nDONE waiting for protocol stop.\n";

	# Remove all topologies
	print "\n\nRemoving topologies...\n";
	
	$_result_ = ixiangpf::topology_config({
		mode			=>	'destroy',
		topology_handle	=>	$t_1_handle,
	});
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		return "FAILED - $error";
	}

	$_result_ = ixiangpf::topology_config({
		mode			=>	'destroy',
		topology_handle	=>	$t_2_handle,
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


