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
#    stacks over PPPoX configurations.			       						   #
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
my $chassis                = "10.205.15.75";
my $tcl_server             = "10.205.15.75";
my @port_list              = ("1/7", "1/8");
my $ixnetwork_tcl_server   = "localhost";
my $wait_time              = 5;
my $test_dir_path          = abs_path();

my $PASSED				   = '0';
my $FAILED				   = '1';

my $_result_			   = '';
my @status_keys			   = ();	
my $status                 = '';
my $port_handle            = '';
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

	$_result_ = ixiangpf::connect ({
		reset                  => '1',
		device                 => $chassis,
		ixnetwork_tcl_server   => $ixnetwork_tcl_server,
		tcl_server             => $tcl_server,
		port_list              => \@port_list,
	});
	&catch_error();

	$port_handle = ixiangpf::status_item('port_handle');
	$status = ixiangpf::status_item('status');

	foreach my $port (@port_list) {
		$port_handle = ixiangpf::status_item("port_handle.$chassis.$port");
		push(@portHandleList, $port_handle);
	}

	my $port_1 = $portHandleList[0];
	my $port_2 = $portHandleList[1];

	print ("\nIxia port handles are @portHandleList ...\n");
	print ("End connecting to chassis ...\n");
	
	# Create the PPP server topology
	
	print "\n\nCreating PPP servers...";
	
    $_result_ = ixiangpf::topology_config ({
        topology_name      => "PPP Servers Topology",
        port_handle        => $port_1,
    });
	&catch_error();
    my $topology_1_handle = ixiangpf::status_item('topology_handle');
    
    $_result_ = ixiangpf::topology_config ({
        topology_handle              => "$topology_1_handle",
        device_group_name            => "PPP Servers",
        device_group_multiplier      => "2",
        device_group_enabled         => "1",
    });
	&catch_error();
    my $deviceGroup_1_handle = ixiangpf::status_item('device_group_handle');
       
    $_result_ = ixiangpf::interface_config ({
        protocol_handle              => $deviceGroup_1_handle,
        mtu                          => "1500",
        vlan                         => "0",
        use_vpn_parameters           => "0",
    });
	&catch_error();
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
	&catch_error();
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
	&catch_error();
    my $multivalue_9_handle = ixiangpf::status_item('multivalue_handle');
    
    $_result_ = ixiangpf::pppox_config ({
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
	&catch_error();
    my $pppoxserver_1_handle = ixiangpf::status_item('pppox_server_handle');
	
	print "\nDONE creating PPP servers.\n\n";
    
	# Create PPP Clients
	
	print "\n\nCreating PPP clients...\n";
	
    $_result_ = ixiangpf::topology_config ({
        topology_name      => "PPP Clients Topology",
        port_handle        => $port_2,
    });
	&catch_error();
    my $topology_2_handle = ixiangpf::status_item('topology_handle');
    
    $_result_ = ixiangpf::topology_config ({
        topology_handle              => $topology_2_handle,
        device_group_name            => "PPP Clients",
        device_group_multiplier      => "5",
    });
	&catch_error();
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
	&catch_error();
    my $multivalue_12_handle = ixiangpf::status_item('multivalue_handle');
    
    $_result_ = ixiangpf::pppox_config ({
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
	&catch_error();
    my $pppoxclient_1_handle = ixiangpf::status_item('pppox_client_handle');
    	
    my $multivalue_13_status = ixiangpf::multivalue_config ({
        pattern                => "distributed",
        distributed_value      => "1",
    });
	&catch_error();
    my $multivalue_13_handle = ixiangpf::status_item('multivalue_handle');
    
    my $multivalue_14_status = ixiangpf::multivalue_config ({
        pattern                => "distributed",
        distributed_value      => "10",
    });
	&catch_error();
    my $multivalue_14_handle = ixiangpf::status_item('multivalue_handle');
    
    my $multivalue_15_status = ixiangpf::multivalue_config ({
        pattern                => "distributed",
        distributed_value      => "10",
    });	
	&catch_error();
    my $multivalue_15_handle = ixiangpf::status_item('multivalue_handle');
    
    $_result_ = ixiangpf::pppox_config ({
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
	&catch_error();
	
	print "\nDONE creating and configuring PPP clients.\n\n";

	# DHCPv6 Client Stack  							    
		
	$_result_ = ixiangpf::emulation_dhcp_group_config    ({
			handle                      	=> $pppoxclient_1_handle         ,
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

	print "\nDONE creating and configuring DHCPv6 clients.\n\n";
	
	# DHCPv6 Server Stack
	
	$_result_ = ixiangpf::emulation_dhcp_server_config  ({
			handle                             => $pppoxserver_1_handle            ,
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
	my $dhcp_server_1_handle = ixiangpf::status_item('dhcpv6server_handle');	
	
	sleep(3);
	
	print "\nDONE creating and configuring DHCPv6 servers.\n\n";
	
	$_result_ = ixiangpf::test_control({
		action	=>	'start_protocol',
		handle	=>	$deviceGroup_1_handle,
	});
	&catch_error();
	
	sleep(20);

	$_result_ = ixiangpf::test_control({
		action	=>	'start_protocol',
		handle	=>	$pppoxclient_1_handle,
	});	
	
	sleep(20);

	$_result_ = ixiangpf::test_control({
		action	=>	'start_protocol',
		handle	=>	$dhcpclient_1_handle,
	});		
	
	sleep(20);
	
	$_result_ = ixiangpf::emulation_dhcp_stats({
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
	
	return $PASSED;
}

my $test_result = main(@ARGV);
print "\nTest execution complete.\nStatus: $test_result\n";
    