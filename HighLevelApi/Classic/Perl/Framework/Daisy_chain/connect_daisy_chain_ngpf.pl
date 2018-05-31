#################################################################################
# Version 1    $Revision: #1 $
# $Author: cm $
#
#    Copyright © 1997 - 2014 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    08-12-2014 RCsutak - created sample
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
#    This sample connects to a daisy chained topology and sets the chain	   # 
#    sequence and cable length for each slave, using the ixiangpf namespace.   #
# Module:                                                                      #
#    The sample was tested on a LSM XMVDC16NG module.                          #
#																			   # 
# Script details:															   # 
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
#                                                                              #                                                                            #
################################################################################


use lib ".";
use lib "..";
use lib "../..";



use ixiahlt;
use ixiangpf;

use warnings;
use strict;
use bignum;
use Carp;

our $CfgErrors = 0;
our $HashRef = {};
our $command_status = '';

sub DHCPv4v6 {
	my $_result_ = '';
    my $_control_status_ = '';
    my $_dhcp_stats_ = '';
	my @status_keys = ();

# Connection 
    my @chassis         = ("ixro-hlt-xm2-02", "ixro-hlt-xm2-03","ixro-hlt-xm2-09");
	my $tcl_server      = 'localhost';
	my @port_list      = (("2/1"), ("2/3"),("2/1"));
	my $guard_rail = 'statistics';
	my $ixNetServer = 'localhost';
    my @master_chassis  = ("none","ixro-hlt-xm2-02","ixro-hlt-xm2-02");
    my $chain_type      = "daisy";
    my $chain_type      = "daisy";
    my @cable_lengths   = (0,6,3);
    my @chain_seq       = (1,3,2);

    my $ixNet =  new IxNetwork(); 
	$ixNet->connect('localhost', '-port', 8009, '-version', '7.31');
	my $root = $ixNet->getRoot();
	
 	
	$_result_ = ixiangpf::connect({
        reset                   => 1,
		port_list	         	=> \@port_list,
		device				 	=> \@chassis,
		ixnetwork_tcl_server 	=> $ixNetServer,
		tcl_server				=> $tcl_server,
        break_locks             => 1,
        master_device           => \@master_chassis,
        chain_cables_length     =>\@cable_lengths ,
        chain_sequence       	=> \@chain_seq,
	});

	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		print "Error: $error";
		return "FAILED - $error";
	}

	my $port_handles = ixiangpf::status_item('vport_list');
	my @port_handles_list = split(/ /,$port_handles);
    
    
 ########################################################### # 1. Configure 2 topologies, each on one port.
 ########################################################### # 2. Configure a DHCPv6 server and a DHCPv6 client. 
 ########################################################### # 3. Configure a DHCPv4 server and a DHCPv4 client.
    
    my $topology_1_status = ixiangpf::topology_config ({
        topology_name      => "CLIENTS TOPOLOGY",
        port_handle        => "$port_handles_list[0]",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }

    my $topology_1_handle = $HashRef->{'topology_handle'};
   
    my $device_group_1_status = ixiangpf::topology_config ({
        topology_handle              => "$topology_1_handle",
        device_group_name            => "Clients Device Group",
        device_group_multiplier      => "10",
        device_group_enabled         => "1",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }

    my $device_group_1_handle = $HashRef->{'device_group_handle'};

    
    my $multivalue_1_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "00.11.01.00.00.01",
        counter_step           => "00.00.00.00.00.01",
        counter_direction      => "increment",
        nest_step              => "00.00.01.00.00.00",
        nest_owner             => "$topology_1_handle",
        nest_enabled           => "1",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }

    my $multivalue_1_handle = $HashRef->{'multivalue_handle'};
    
    my $ethernet_1_status = ixiangpf::interface_config ({
        protocol_name                => "Ethernet DHCPv4",
        protocol_handle              => "$device_group_1_handle",
        mtu                          => "1500",
        src_mac_addr                 => "$multivalue_1_handle",
        src_mac_addr_step            => "00.00.00.00.00.00",
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
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }

    my $ethernet_1_handle = $HashRef->{'ethernet_handle'};
 
    
    my $dhcpv4client_1_status = ixiangpf::emulation_dhcp_group_config ({
        dhcp_range_ip_type               => "ipv4",
        dhcp_range_renew_timer           => "0",
        dhcp_range_server_address        => "10.10.0.1",
        dhcp_range_use_first_server      => "1",
        handle                           => "$ethernet_1_handle",
        use_rapid_commit                 => "0",
        protocol_name                    => "DHCPv4 Clients",
        dhcp4_broadcast                  => "0",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }

    my $dhcpv4client_1_handle = $HashRef->{'dhcpv4client_handle'};

    
    my $multivalue_2_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "00.12.01.00.00.01",
        counter_step           => "00.00.00.00.00.01",
        counter_direction      => "increment",
        nest_step              => "00.00.01.00.00.00",
        nest_owner             => "$topology_1_handle",
        nest_enabled           => "1",
    });
    
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }

    my $multivalue_2_handle = $HashRef->{'multivalue_handle'};
    
    my $ethernet_2_status = ixiangpf::interface_config ({
        protocol_name                => "Ethernet DHCPv6",
        protocol_handle              => "$device_group_1_handle",
        mtu                          => "1500",
        src_mac_addr                 => "$multivalue_2_handle",
        src_mac_addr_step            => "00.00.00.00.00.00",
        vlan                         => "1",
        vlan_id                      => "10",
        vlan_id_step                 => "5",
        vlan_id_count                => "1",
        vlan_tpid                    => "0x8100",
        vlan_user_priority           => "0",
        vlan_user_priority_step      => "0",
        use_vpn_parameters           => "0",
        site_id                      => "0",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }

    my $ethernet_2_handle = $HashRef->{'ethernet_handle'};

    
    my $multivalue_3_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "10",
        counter_step           => "1",
        counter_direction      => "increment",
        nest_step              => "0",
        nest_owner             => "$topology_1_handle",
        nest_enabled           => "1",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $multivalue_3_handle = $HashRef->{'multivalue_handle'};
    
    my $dhcpv6client_1_status = ixiangpf::emulation_dhcp_group_config ({
        dhcp6_range_duid_enterprise_id            => "$multivalue_3_handle",
        dhcp6_range_duid_type                     => "duid_llt",
        dhcp6_range_duid_vendor_id                => "10",
        dhcp6_range_duid_vendor_id_increment      => "0",
        dhcp6_range_ia_id                         => "10",
        dhcp6_range_ia_id_increment               => "0",
        dhcp6_range_ia_t1                         => "302400",
        dhcp6_range_ia_t2                         => "483840",
        dhcp6_range_ia_type                       => "iana",
        dhcp_range_ip_type                        => "ipv6",
        dhcp_range_renew_timer                    => "0",
        handle                                    => "$ethernet_2_handle",
        use_rapid_commit                          => "0",
        protocol_name                             => "DHCPv6 Clients",
        enable_stateless                          => "0",
        dhcp6_use_pd_global_address               => "0",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }

    my $dhcpv6client_1_handle = $HashRef->{'dhcpv6client_handle'};
    my $dhcp6Iapd_1_handle = $HashRef->{'dhcpv6_iapd_handle'};
    my $dhcp6Iana_1_handle = $HashRef->{'dhcpv6_iana_handle'};
    
    my $topology_2_status = ixiangpf::topology_config ({
        topology_name      => "SERVERS TOPOLOGY",
        port_handle        => "$port_handles_list[1]",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $topology_2_handle = $HashRef->{'topology_handle'};
    
    my $device_group_2_status = ixiangpf::topology_config ({
        topology_handle              => "$topology_2_handle",
        device_group_name            => "Servers Device Group",
        device_group_multiplier      => "10",
        device_group_enabled         => "1",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $device_group_2_handle = $HashRef->{'device_group_handle'};

    my $multivalue_4_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "00.13.01.00.00.01",
        counter_step           => "00.00.00.00.00.01",
        counter_direction      => "increment",
        nest_step              => "00.00.01.00.00.00",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "1",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $multivalue_4_handle = $HashRef->{'multivalue_handle'};
    
    my $ethernet_3_status = ixiangpf::interface_config ({
        protocol_name                => "DHCPv4 Server Ethernet",
        protocol_handle              => "$device_group_2_handle",
        mtu                          => "1500",
        src_mac_addr                 => "$multivalue_4_handle",
        src_mac_addr_step            => "00.00.00.00.00.00",
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
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $ethernet_3_handle = $HashRef->{'ethernet_handle'};
   
    
    my $multivalue_5_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "5.5.5.2",
        counter_step           => "0.1.0.0",
        counter_direction      => "increment",
        nest_step              => "0.1.0.0",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "1",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $multivalue_5_handle = $HashRef->{'multivalue_handle'};
    
    my $multivalue_6_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "5.5.5.1",
        counter_step           => "0.1.0.0",
        counter_direction      => "increment",
        nest_step              => "0.1.0.0",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "1",
    });
  
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $multivalue_6_handle = $HashRef->{'multivalue_handle'};
    
    my $ipv4_1_status = ixiangpf::interface_config ({
        protocol_name                     => "Server IPv4",
        protocol_handle                   => "$ethernet_3_handle",
        ipv4_resolve_gateway              => "0",
        ipv4_manual_gateway_mac           => "00.00.00.00.00.01",
        ipv4_manual_gateway_mac_step      => "00.00.00.00.00.00",
        gateway                           => "$multivalue_6_handle",
        gateway_step                      => "0.0.0.0",
        intf_ip_addr                      => "$multivalue_5_handle",
        intf_ip_addr_step                 => "0.0.0.0",
        netmask                           => "255.255.255.0",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $ipv4_1_handle = $HashRef->{'ipv4_handle'};
 
    
    my $multivalue_7_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "10",
        counter_step           => "4",
        counter_direction      => "increment",
        nest_step              => "1",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "0",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $multivalue_7_handle = $HashRef->{'multivalue_handle'};
    
    my $multivalue_8_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "5.5.5.5",
        counter_step           => "0.1.0.0",
        counter_direction      => "increment",
        nest_step              => "0.1.0.0",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "1",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $multivalue_8_handle = $HashRef->{'multivalue_handle'};
    
    my $multivalue_9_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "86400",
        counter_step           => "1000",
        counter_direction      => "increment",
        nest_step              => "1",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "0",
    });
   
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $multivalue_9_handle = $HashRef->{'multivalue_handle'};
    
    my $dhcpv4server_1_status = ixiangpf::emulation_dhcp_server_config ({
        dhcp_offer_router_address                  => "0.0.0.0",
        dhcp_offer_router_address_inside_step      => "0.0.0.0",
        handle                                     => "$ipv4_1_handle",
        ip_dns1                                    => "0.0.0.0",
        ip_dns2                                    => "0.0.0.0",
        ip_version                                 => "4",
        ipaddress_count                            => "$multivalue_7_handle",
        ipaddress_pool                             => "$multivalue_8_handle",
        ipaddress_pool_prefix_length               => "24",
        ipaddress_pool_prefix_inside_step          => "0",
        lease_time                                 => "$multivalue_9_handle",
        mode                                       => "create",
        protocol_name                              => "DHCPv4 Servers",
        use_rapid_commit                           => "0",
        echo_relay_info                            => "1",
        pool_address_increment                     => "0.0.0.1",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $dhcpv4server_1_handle = $HashRef->{'dhcpv4server_handle'};

    
    my $multivalue_10_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "00.14.01.00.00.01",
        counter_step           => "00.00.00.00.00.01",
        counter_direction      => "increment",
        nest_step              => "00.00.01.00.00.00",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "1",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $multivalue_10_handle = $HashRef->{'multivalue_handle'};
    
    my $ethernet_4_status = ixiangpf::interface_config ({
        protocol_name                => "{Ethernet 4}",
        protocol_handle              => "$device_group_2_handle",
        mtu                          => "1500",
        src_mac_addr                 => "$multivalue_10_handle",
        src_mac_addr_step            => "00.00.00.00.00.00",
        vlan                         => "1",
        vlan_id                      => "10",
        vlan_id_step                 => "5",
        vlan_id_count                => "1",
        vlan_tpid                    => "0x8100",
        vlan_user_priority           => "0",
        vlan_user_priority_step      => "0",
        use_vpn_parameters           => "0",
        site_id                      => "0",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $ethernet_4_handle = $HashRef->{'ethernet_handle'};
  
    my $multivalue_11_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "2000:0:0:100:0:0:50:100",
        counter_step           => "0:0:0:0:0:0:1:1",
        counter_direction      => "decrement",
        nest_step              => "0:0:0:0:0:0:0:1",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "0",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $multivalue_11_handle = $HashRef->{'multivalue_handle'};
    
    my $multivalue_12_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "2000:0:0:100:0:0:50:1",
        counter_step           => "0:0:0:1:0:0:1:0",
        counter_direction      => "decrement",
        nest_step              => "0:0:0:1:0:0:0:0",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "1",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $multivalue_12_handle = $HashRef->{'multivalue_handle'};
    
    my $ipv6_1_status = ixiangpf::interface_config ({
        protocol_name                     => "IPv6 Servers",
        protocol_handle                   => "$ethernet_4_handle",
        ipv6_multiplier                   => "1",
        ipv6_resolve_gateway              => "0",
        ipv6_manual_gateway_mac           => "00.00.00.00.00.01",
        ipv6_manual_gateway_mac_step      => "00.00.00.00.00.00",
        ipv6_gateway                      => "$multivalue_12_handle",
        ipv6_gateway_step                 => "::0",
        ipv6_intf_addr                    => "$multivalue_11_handle",
        ipv6_intf_addr_step               => "::0",
        ipv6_prefix_length                => "64",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $ipv6_1_handle = $HashRef->{'ipv6_handle'};
  
    
    my $multivalue_13_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "2000:0:0:100:0:0:50:101",
        counter_step           => "0:0:0:0:0:0:1:0",
        counter_direction      => "decrement",
        nest_step              => "0:0:0:1:0:0:0:0",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "1",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $multivalue_13_handle = $HashRef->{'multivalue_handle'};
    
    my $multivalue_14_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "a1a1:0:0:0:0:0:0:0",
        counter_step           => "0:1:0:0:0:0:0:0",
        counter_direction      => "increment",
        nest_step              => "0:1:0:0:0:0:0:0",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "1",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $multivalue_14_handle = $HashRef->{'multivalue_handle'};
    
    my $dhcpv6server_1_status = ixiangpf::emulation_dhcp_server_config ({
        dhcp6_ia_type                     => "iana",
        handle                            => "$ipv6_1_handle",
        ip_dns1                           => "0:0:0:0:0:0:0:0",
        ip_dns2                           => "0:0:0:0:0:0:0:0",
        ip_version                        => "6",
        ipaddress_count                   => "20",
        ipaddress_pool                    => "$multivalue_13_handle",
        ipaddress_pool_prefix_length      => "64",
        ipaddress_pool_prefix_step        => "0",
        lease_time                        => "86400",
        mode                              => "create",
        protocol_name                     => "{DHCPv6 Servers}",
        use_rapid_commit                  => "0",
        pool_address_increment            => "0:0:0:0:0:0:0:1",
        start_pool_prefix                 => "$multivalue_14_handle",
        pool_prefix_increment             => "1:0:0:0:0:0:0:0",
        pool_prefix_size                  => "1",
        prefix_length                     => "64",
        custom_renew_time                 => "34560",
        custom_rebind_time                => "55296",
        use_custom_times                  => "0",
    });
    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = $HashRef->{'log'};
        print "Error: $error";
        return "FAILED - $error";
    }
    my $dhcpv6server_1_handle = $HashRef->{'dhcpv6server_handle'};

######################################################################### 4. Start the protocols and, after 5 seconds, stop them.

    my @dhcp_list = ($dhcpv6server_1_handle, $dhcpv4server_1_handle, $dhcpv6client_1_handle , $dhcpv4client_1_handle);
    print "Starting protocols .... \n\n";
    
    my $run_status = ixiangpf::test_control({
		action		=> 'start_protocol',
		handle		=> \@dhcp_list,
	});
	
	$HashRef = ixiangpf::get_result_hash();
	$command_status = $HashRef->{'status'};
	if ($command_status != $ixiangpf::SUCCESS){
		my $error = ixiangpf::status_item('log');
		print "Error: $error";
		return "FAILED - $error";
	}

    sleep(20);   

    print "Stopping protocols .... \n\n";
    # my $stop_status = ixiangpf::test_control({
		# action		=> 'stop_protocol',
		# handle		=> \@dhcp_list,
	# });
	
	# $HashRef = ixiangpf::get_result_hash();
	# $command_status = $HashRef->{'status'};
	# if ($command_status != $ixiangpf::SUCCESS){
		# my $error = ixiangpf::status_item('log');
		# print "Error: $error";
		# return "FAILED - $error";
	# }
    
    ixiangpf::test_control({action=> 'stop_all_protocols'});
    sleep(60);
    
######################################################################## 5. Remove the protocols and delete the Device Groups (DG) and topologies.
    
    my $remove_dhcp_status = ::ixiangpf::topology_config ({
        mode                => 'destroy',
        device_group_handle => \@dhcp_list,
    });
    $HashRef = ixiangpf::get_result_hash();
	$command_status = $HashRef->{'status'};
	if ($command_status != $ixiangpf::SUCCESS){
		my $error = ixiangpf::status_item('log');
		print "Error: $error";
		return "FAILED - $error";
	}
    my @ethernet_list_1 = ($ethernet_1_handle, $ethernet_2_handle);
    my $remove_eth_status = ::ixiangpf::topology_config ({
        mode                => 'destroy',
        device_group_handle => \@ethernet_list_1,
    });
    $HashRef = ixiangpf::get_result_hash();
	$command_status = $HashRef->{'status'};
	if ($command_status != $ixiangpf::SUCCESS){
		my $error = ixiangpf::status_item('log');
		print "Error: $error";
		return "FAILED - $error";
	}
    my @ip_list = ($ipv4_1_handle, $ipv6_1_handle);
    my $remove_ip_status = ::ixiangpf::topology_config ({
        mode                => 'destroy',
        device_group_handle => \@ip_list,
    });
    $HashRef = ixiangpf::get_result_hash();
	$command_status = $HashRef->{'status'};
	if ($command_status != $ixiangpf::SUCCESS){
		my $error = ixiangpf::status_item('log');
		print "Error: $error";
		return "FAILED - $error";
	}
    
    my @ethernet_list_2 = ($ethernet_3_handle, $ethernet_4_handle);
    my $remove_eth_status_2 = ::ixiangpf::topology_config ({
        mode                => 'destroy',
        device_group_handle => \@ethernet_list_2,
    });
    $HashRef = ixiangpf::get_result_hash();
	$command_status = $HashRef->{'status'};
	if ($command_status != $ixiangpf::SUCCESS){
		my $error = ixiangpf::status_item('log');
		print "Error: $error";
		return "FAILED - $error";
	}
    
    my @device_group_list = ($device_group_1_handle, $device_group_2_handle);
    my $remove_dg_status = ::ixiangpf::topology_config ({
        mode                => 'destroy',
        device_group_handle => $device_group_1_handle,
    });
    $HashRef = ixiangpf::get_result_hash();
	$command_status = $HashRef->{'status'};
	if ($command_status != $ixiangpf::SUCCESS){
		my $error = ixiangpf::status_item('log');
		print "Error: $error";
		return "FAILED - $error";
	}
	my $remove_dg_status_2 = ::ixiangpf::topology_config ({
        mode                => 'destroy',
        device_group_handle => $device_group_2_handle,
    });
    $HashRef = ixiangpf::get_result_hash();
	$command_status = $HashRef->{'status'};
	if ($command_status != $ixiangpf::SUCCESS){
		my $error = ixiangpf::status_item('log');
		print "Error: $error";
		return "FAILED - $error";
	}	
    my $dg_after_delete_1 = $ixNet->getList("$root$topology_1_handle",'deviceGroup');
    my $dg_after_delete_2 = $ixNet->getList("$root$topology_2_handle",'deviceGroup');

    if ($dg_after_delete_1 != $dg_after_delete_2 && $dg_after_delete_1 != ''){
        print "Error: device groups weren't destroyed correctly!\n";
		$CfgErrors +=1;
    }
    my @topologies = ($topology_1_handle, $topology_2_handle);
    
    my $remove_topologies_status = ::ixiangpf::topology_config ({
        mode                => 'destroy',
        device_group_handle => $topology_1_handle,
    });
    $HashRef = ixiangpf::get_result_hash();
	$command_status = $HashRef->{'status'};
	if ($command_status != $ixiangpf::SUCCESS){
		my $error = ixiangpf::status_item('log');
		print "Error: $error";
		return "FAILED - $error";
	}
    $remove_topologies_status = ::ixiangpf::topology_config ({
        mode                => 'destroy',
        device_group_handle => $topology_2_handle,
    });
    $HashRef = ixiangpf::get_result_hash();
	$command_status = $HashRef->{'status'};
	if ($command_status != $ixiangpf::SUCCESS){
		my $error = ixiangpf::status_item('log');
		print "Error: $error";
		return "FAILED - $error";
	}
    
    if ($CfgErrors != 0) {
        print " This script contains $CfgErrors errors! \n";
        return 0;
    }
    return 1;
}
&DHCPv4v6;