################################################################################
# Version 1.0    $Revision: #1 $
# $Author: Daria Badea
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    03-18-2014 
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
#	 The script configures on two back to back ports DHCPv4 Client/Server      #
#    stacks over LAC/LNS configurations			       						   #
#																			   #
# Module:                                                                      #
#    The sample was tested on an 10G LSM XM8S module.                   	   #
#                                                                              #
################################################################################

# Source all libraries in the beginning
use warnings;
use strict;
use bignum;
use Carp;
use Cwd 'abs_path';

# use lib where the HLPAPI files are located

use lib "C:/Program Files (x86)/Ixia/hltapi/4.90.0.67/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.30";
use lib "C:/Program Files (x86)/Ixia/hltapi/4.90.0.67/TclScripts/lib/hltapi/library/common/ixiangpf/perl";

use ixiahlt {
IXIA_VERSION => 'HLTSET166',
TclAutoPath => ['C:/Program Files (x86)/Ixia/IxOS/6.70.0.33','C:/Program Files (x86)/Ixia/hltapi/4.90.0.67/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.30','C:/Program Files (x86)/Ixia/hltapi/4.90.0.67/TclScripts/lib', 'C:/Program Files (x86)/Ixia/IxNetwork/7.30.0.225-EB/TclScripts/lib/ixTcl1.0','C:/Program Files (x86)/Ixia/IxNetwork/7.30.0.225-EB/TclScripts/lib/IxTclNetwork'],
};

use ixiahlt;
use ixiaixn;
use ixiangpf;


# Declare the Chassis IP address and the Ports that will be used
my $test_name              = "DHCPoL2TP";
my $chassis                = "10.205.15.62";
my $tcl_server             = "10.205.15.62";
my @port_list              = ("12/7", "12/8");
my $ixnetwork_tcl_server   = "localhost";
my $wait_time              = 5;
my $test_dir_path          = abs_path();

my $PASSED				   = '0';
my $FAILED				   = '1';


my $status                 = '';
my $port_handle            = '';
my @status_keys            = ();
my %status_keys            = ();
my @portHandleList         = ();

################################################################################
# Function to catch the errors and print it on the screen                      #
################################################################################

sub catch_error {
    if (ixiangpf::status_item('status') != 1) {
        print ("\n#################################################### \n");
        print ("ERROR: \n$test_name : ". ixiangpf::status_item('log'));
        print ("\n#################################################### \n");
        return $FAILED
    }
}

sub main {

	################################################################################
	# START - Connect to the chassis
	################################################################################

	my $connect_status = ixiangpf::connect ({
		reset                  => '1',
		device                 => $chassis,
		ixnetwork_tcl_server   => $ixnetwork_tcl_server,
		tcl_server             => $tcl_server,
		port_list              => \@port_list,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	$port_handle = ixiangpf::status_item('port_handle');
	$status = ixiangpf::status_item('status');

	# Assign portHandleList with port handles values
	foreach my $port (@port_list) {
		$port_handle = ixiangpf::status_item("port_handle.$chassis.$port");
		push(@portHandleList, $port_handle);
	}

	my $port_1 = $portHandleList[0];
	my $port_2 = $portHandleList[1];

	print ("\nIxia port handles are @portHandleList ...\n");
	print ("End connecting to chassis ...\n");

	#####################################################
	# Create a topology and a device group for LAC      #
	#####################################################

	my $topology_status = ixiangpf::topology_config ({
			topology_name           => 'LAC 1',
			port_handle				=> $port_1,
			device_group_multiplier	=> 10,
			device_group_name       => 'LAC DG 1',
			device_group_enabled    => 1,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $dg_handle_1 = ixiangpf::status_item('device_group_handle');
	my $topology_handle_1 = ixiangpf::status_item('topology_handle');
	
	my $mac_start		= "0000.0005.0001";
	my $mac_step		= "0000.0000.1000";

	my $interface_status = ixiangpf::interface_config ({
			protocol_handle			=> $dg_handle_1,
			src_mac_addr       		=> $mac_start,
			src_mac_addr_step		=> $mac_step,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $ethernet_handle_1 = ixiangpf::status_item('ethernet_handle');

	#####################################################
	# LAC Stack		    							    #
	#####################################################
	
	my $tunnel_count   			=  '1';
	my $sessions_per_tunnel 	=  '10';
	
	my $LAC_status = ixiangpf::l2tp_config ({
		    mode                               => 'lac'                             ,
		    handle                             => $ethernet_handle_1              ,
		    action                             => 'create'                          ,
		    sessions_per_tunnel                => $sessions_per_tunnel            ,
		    num_tunnels                        => $tunnel_count                   ,
		    l2tp_dst_addr                      => '12.70.1.1'                       ,
		    l2tp_dst_step                      => '0.0.0.1'                         ,
		    l2tp_src_gw                		   => '0.0.0.0'               			,
		    l2tp_src_prefix_len            	   => '16'                    			,
		    l2tp_src_addr                      => '12.70.0.1'                       ,
		    l2tp_src_count                     => $tunnel_count                   ,
		    l2tp_src_step                      => '0.0.0.1'                         ,
		    enable_term_req_timeout            => '0'                               ,
		    udp_src_port                       => '1600'                            ,
		    udp_dst_port                       => '1800'                            ,
		    redial_timeout                     => '13'                              ,
		    rws                                => '15'                              ,
		    offset_len                         => '16'                              ,
		    max_ctrl_timeout                   => '9'                               ,
		    redial_max                         => '2048'                            ,
		    hostname                           => 'ixia_dut'                      ,
		    secret                             => 'ixia_secret'                   ,
		    hostname_wc                        => '1'                               ,
		    secret_wc                          => '1'                               ,
		    wildcard_bang_start                => '1'                               ,
		    wildcard_bang_end                  => $sessions_per_tunnel            ,
		    wildcard_dollar_start              => '1'                               ,
		    wildcard_dollar_end                => $tunnel_count                   ,
		    username                           => 'ixia_#_?'                      ,
		    password                           => 'pwd_#_?'                       ,
		    username_wc                        => '1'                               ,
		    password_wc                        => '1'                               ,
		    wildcard_pound_start               => '1'                               ,
		    wildcard_pound_end                 => $tunnel_count                   ,
		    wildcard_question_start            => '1'                               ,
		    wildcard_question_end              => $sessions_per_tunnel            ,
		    init_ctrl_timeout                  => '6'                               ,
		    hello_interval                     => '101'                             ,
		    framing_capability                 => 'async'                           ,
		    ctrl_retries                       => '11'                              ,
		    bearer_type                        => 'digital'                         ,
		    bearer_capability                  => 'digital'                         ,
		    enable_mru_negotiation             => '1'                               ,
		    desired_mru_rate                   => '1501'                            ,
		    lcp_enable_accm                    => '1'                               ,
		    lcp_accm                           => '1501'                            ,
		    max_auth_req                       => '15'                              ,
		    auth_req_timeout                   => '7'                               ,
		    auth_mode                          => 'pap_or_chap'                     ,
		    chap_name                          => 'ixia_chap_name'                  ,
		    chap_secret                        => 'ixia_chap_secret'                ,
		    client_dns_options                 => 'request_primary_and_secondary'   ,
		    ppp_client_ip                      => '3.3.3.3'                         ,
		    ppp_client_step                    => '0.0.0.2'                         ,
		    ppp_client_iid                     => '00:44:44:44:00:00:00:01'         ,
		    client_ipv4_ncp_configuration      => 'request'                         ,
		    client_netmask                     => '255.255.0.0'                     ,
		    client_netmask_options             => 'request_specific_netmask'        ,
		    client_ipv6_ncp_configuration      => 'request'                         ,
		    client_wins_options                => 'request_primaryandsecondary_wins',
		    client_wins_primary_address        => '88.88.88.88'                     ,
		    client_wins_secondary_address      => '99.99.99.99'                     ,
		    enable_domain_groups               => '1'                               ,
		    echo_req                           => '1'                               ,
		    echo_req_interval                  => '9'                               ,
		    echo_rsp                           => '1'                               ,
		    max_configure_req                  => '8'                               ,
		    max_terminate_req                  => '6'                               ,
		    config_req_timeout                 => '25'                              ,
		    protocol_name                      => 'Ixia LAC'                      ,
		    max_ipcp_req                       => '12'                              ,
		    ipcp_req_timeout                   => '13'                              ,
		    ip_cp                              => 'dual_stack'                      ,
		    client_primary_dns_address         => '5.5.5.5'                         ,
		    client_secondary_dns_address       => '6.6.6.6'                         ,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $pppox_1_handle = ixiangpf::status_item('pppox_client_handle');
	
	#####################################################
	# DHCPv6 Client Stack  							    #
	#####################################################
	
	my $dhcp_config_for_lac = ixiangpf::emulation_dhcp_group_config    ({
			handle                      	=> $pppox_1_handle         ,
			mode                    		=> 'create'        ,
			dhcp_range_ip_type              => 'ipv6'        ,
			dhcp6_range_duid_enterprise_id  => '15'        ,
			dhcp6_range_duid_type           => 'duid_en'        ,
			dhcp6_range_duid_vendor_id      => '20'        ,
			dhcp6_range_duid_vendor_id_increment    => '2'        ,
			dhcp_range_renew_timer          => '10'        ,
			dhcp6_use_pd_global_address     => '1'        ,
			protocol_name                	=> 'Ixia DHCPv6'    ,
			dhcp6_range_ia_type        		=> 'iana_iapd'        ,
			dhcp6_range_ia_t2            	=> '40000'        ,
			dhcp6_range_ia_t1            	=> '30000'        ,
			dhcp6_range_ia_id_increment     => '2'        ,
			dhcp6_range_ia_id            	=> '20'        ,
	});
	&catch_error();
	
	my $dhcpclient_1_handle = ixiangpf::status_item('dhcpv6client_handle');
	
	#####################################################
	# Create a topology and a device group for LNS      #
	#####################################################

	my $topology_status_2 = ixiangpf::topology_config ({
			topology_name           => 'LNS 1',
			port_handle				=> $port_2,
			device_group_multiplier	=> 10,
			device_group_name       => 'LNS DG 1',
			device_group_enabled    => 1,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $dg_handle_2 = ixiangpf::status_item('device_group_handle');
	my $topology_handle_2 = ixiangpf::status_item('topology_handle');
	
	my $mac_start		= "0000.0065.0001";
	my $mac_step		= "0000.0000.1000";

	my $command_status = ixiangpf::interface_config ({
			protocol_handle			=> $dg_handle_2,
			src_mac_addr       		=> $mac_start,
			src_mac_addr_step		=> $mac_step,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $ethernet_handle_2 = ixiangpf::status_item('ethernet_handle');
	
	#####################################################
	# LNS Stack		    							    #
	#####################################################	

	my $tunnel_count        = '10';
	my $sessions_per_tunnel = '50';
	
	my $LNS_status = ixiangpf::l2tp_config ({
			mode                          	=> 'lns'                             ,
			handle                          => $ethernet_handle_2           ,
			protocol_name                	=> 'L2TP Network Server'        ,
			action                          => 'create'                          ,
			num_tunnels                     => $tunnel_count                   ,
			sessions_per_tunnel             => $sessions_per_tunnel            ,
			l2tp_src_addr                   => '12.70.1.1'                       ,
			l2tp_src_count                  =>    $tunnel_count                   ,
			l2tp_src_gw                  => '0.0.0.0'                ,
			l2tp_src_step                =>       '0.0.0.1'                         ,
			l2tp_src_prefix_len            => '16'                    ,
			enable_term_req_timeout          =>   '0'                               ,
			username                           => 'ixia_lns_user'                   ,
			password                           => 'ixia_lns_pass'                   ,
			chap_name                          => 'ixia_chap_name'                  ,
			chap_secret                        => 'ixia_chap_secret'                ,
			enable_domain_groups               => '1'                               ,
			udp_src_port                       => '1800'                            ,
			udp_dst_port                       => '1600'                            ,
			redial_timeout                     => '13'                              ,
			rws                                => '15'                              ,
			offset_len                         => '16'                              ,
			max_ctrl_timeout                   => '9'                               ,
			redial_max                         => '2048'                            ,
			secret                             => 'ixia_secret'                     ,
			hostname                           => 'ixia_dut'                        ,
			init_ctrl_timeout                  => '6'                               ,
			hello_interval                     => '101'                             ,
			framing_capability                 => 'async'                           ,
			ctrl_retries                       => '11'                              ,
			bearer_type                        => 'digital'                         ,
			bearer_capability                  => 'digital'                         ,
			accept_any_auth_value              => '1'                               ,
			max_auth_req                       => '121'                             ,
			auth_req_timeout                   => '132'                             ,
			auth_mode                          => 'pap_or_chap'                     ,
			ppp_client_iid                     => '00:55:55:55:00:00:00:01'         ,
			ppp_client_iid_step                => '00:00:00:00:00:00:00:01'         ,
			ppp_client_ip                      => '22.22.22.1'                      ,
			ppp_client_step                    => '0.0.0.3'                         ,
			dns_server_list                    => '100:0:0:1:0:0:0:0'               ,
			echo_req_interval                  => '17'                              ,
			send_dns_options                   => '1'                               ,
			echo_req                           => '1'                               ,
			echo_rsp                           => '1'                               ,
			ipv6_pool_addr_prefix_len          => '90'                              ,
			ipv6_pool_prefix                   => '1:1:1:1:1:1:1:1'                 ,
			ipv6_pool_prefix_len               => '72'                              ,
			lcp_accm                           => '234'                             ,
			lcp_enable_accm                    => '1'                               ,
			max_configure_req                  => '111'                             ,
			max_terminate_req                  => '120'                             ,
			config_req_timeout                 => '55'                              ,
			enable_mru_negotiation             => '1'                               ,
			desired_mru_rate                   => '1501'                            ,
			max_ipcp_req                       => '14'                              ,
			ipcp_req_timeout                   => '15'                              ,
			ip_cp                              => 'dual_stack'                      ,
			ppp_server_iid                     => '00:66:66:66:00:00:00:01'         ,
			ppp_server_ip                      => '45.45.45.1'                      ,
			server_dns_options                 => 'supply_primary_and_secondary'    ,
			ppp_local_iid_step                 => '3'                               ,
			ppp_local_ip_step                  => '0.0.15.15'                       ,
			server_ipv4_ncp_configuration      => 'clientmay'                       ,
			server_netmask                     => '255.255.255.128'                 ,
			server_netmask_options             => 'supply_netmask'                  ,
			server_primary_dns_address         => '12.12.12.1'                      ,
			server_secondary_dns_address       => '13.13.13.1'                      ,
			server_ipv6_ncp_configuration      => 'clientmay'                       ,
			server_wins_options                => 'supply_primary_and_secondary'    ,
			server_wins_primary_address        => '21.21.21.1'                      ,
			server_wins_secondary_address      => '31.31.31.1'                      ,
	});
	&catch_error();
	
	@status_keys = ixiangpf::status_item_keys();
	my $pppox_2_handle = ixiangpf::status_item('pppox_server_handle');	
	
	my $dhcp_server_config_for_lns = ixiangpf::emulation_dhcp_server_config  ({
			handle                             => $pppox_2_handle            ,
			mode                    		   => 'create'                ,
			dhcp6_ia_type                      => 'iana_iapd'                ,
			protocol_name                      => 'Ixia DHCPv6 Server'        ,
			ip_dns1                            => '11:0:0:0:0:0:0:1'            ,
			ip_dns2                            => '22:0:0:0:0:0:0:1'            ,
			ip_version                         => '6'                    ,
			ipaddress_count                    => '1'                    ,
			ipaddress_pool                     => '5:a::1'                ,
			ipaddress_pool_prefix_length       => '64'                    ,
			lease_time                         => '86400'                ,
			pool_address_increment             => '0:0:0:0:0:0:0:1'            ,
			start_pool_prefix                  => '55:aa::'                ,
			pool_prefix_increment              => '1:0:0:0:0:0:0:0'            ,
			pool_prefix_size                   => '1'                    ,
			prefix_length                      => '64'                    ,
			custom_renew_time                  => '34560'                              ,
			custom_rebind_time                 => '55296'                              ,
			use_custom_times                   => '1'                                  ,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $dhcp_server_1_handle = ixiangpf::status_item('dhcpv6server_handle');
	
	sleep(3);
	
	my $start_servers = ixiangpf::test_control({
		action	=>	'start_protocol',
		handle	=>	$dhcp_server_1_handle,
	});
	&catch_error();
	
	sleep(10);
	
	my $start_clients = ixiangpf::test_control({
		action	=>	'start_protocol',
		handle	=>	$dhcpclient_1_handle,
	});
	&catch_error();
	
	sleep(20);
	
	my $server_status = ixiangpf::emulation_dhcp_server_stats({
		dhcp_handle			=>	$dhcp_server_1_handle,
		action				=>	'collect',
		execution_timeout	=>	'60',
	});
	&catch_error();
	
	@status_keys = ixiangpf::status_item_keys();
	print "\nThe returned DHCPv4 server statistics are:\n";
	my $server_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($server_stats);
	print "\n";
	
	my $client_status = ixiangpf::emulation_dhcp_stats({
		handle				=>	$dhcpclient_1_handle,
		mode				=>	'aggregate_stats',
		dhcp_version		=>	'dhcp6',
		execution_timeout	=>	'60',
	});
	&catch_error();
	
	@status_keys = ixiangpf::status_item_keys();
	print "\nThe aggragted DHCPv4 client statistics are:\n";
	my $client_aggregate_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($client_aggregate_stats);
	print "\n";
		
	return $PASSED
}

my $test_result = main(@ARGV);
print "\nTest execution complete.\nStatus: $test_result\n";