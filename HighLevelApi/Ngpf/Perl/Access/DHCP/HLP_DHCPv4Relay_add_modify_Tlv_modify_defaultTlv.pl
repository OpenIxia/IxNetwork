################################################################################
# Version 1.0    $Revision: #1 $
# $Author: Alexandra Apetroaei
#
#    Copyright © 1997 - 20014 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
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
#	 The script adds DHCP Relay protocol and configures TLVs on it.			   #
#	 Add a new TLV. Modify the new TLV.										   #
#	 Modiy one of the default TLVs.     						         	   #
#																			   #
# Module:                                                                      #
#    The sample was tested on a LSM XM8S module.	                   		   #
#                                                                              #
################################################################################


use warnings;
use strict;
use bignum;
use Carp;
use Cwd 'abs_path';


# use lib where the HLPAPI files are located
use lib '/home/aapetroaei/ixos/lib/hltapi/library/common/ixia_hl_lib-7.40';
use lib '/home/aapetroaei/ixos/lib/hltapi/library/common/ixiangpf/perl';
use lib '/home/aapetroaei/ixos/lib/PerlApi';

use ixiahlt {
IXIA_VERSION => 'HLTSET174',
TclAutoPath => ['/home/aapetroaei/ixos/lib','/home/aapetroaei/ixos/lib/hltapi']
};

use ixiahlt;
use ixiaixn;
use ixiangpf;


# Declare the Chassis IP address and the Ports that will be used
my $test_name              = 'DHCPv6_LDRA_config_with_LTV';
my $chassis                = '10.205.15.90';
my $tcl_server             = '10.205.15.90';
my @port_list              = ('11/3', '11/4');
my $ixnetwork_tcl_server   = 'ixro-smqa-r-22';
#my $wait_time              = 5;


my $PASSED				   = '0';
my $FAILED				   = '1';

my $status                 = '';
my $_result_                 = '';
my $port_handle            = '';
my @status_keys            = ();
my %status_keys            = ();
my @portHandleList         = ();


################################################################################
# Function to catch the errors and print it on the screen                      #
################################################################################

sub catch_error {
    if (ixiangpf::status_item('status') != 1) {
        print ('\n', '####################################################', '\n');
        print ('ERROR: \n$test_name : '. ixiangpf::status_item('log'));
        print ('\n', '####################################################', '\n');
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

	@status_keys = ixiangpf::status_item_keys();
	$port_handle = ixiangpf::status_item('port_handle');
	$status = ixiangpf::status_item('status');

	# Assign portHandleList with port handles values
	foreach my $port (@port_list) {
		$port_handle = ixiangpf::status_item("port_handle.$chassis.$port");
		push(@portHandleList, $port_handle);
	}

	my $port_0 = $portHandleList[0];
	my $port_1 = $portHandleList[1];

	print ("\nIxia port handles are @portHandleList ...\n");
	print ("End connecting to chassis ...\n");

	#####################################################
	# Create a topology and a device group for DHCP Relay      #
	#####################################################


	$_result_ = ixiangpf::topology_config ({
			topology_name           => 'Client Topology',
			port_handle				=> $port_0,
			device_group_multiplier	=> 1,
			device_group_name       => 'DHCP Relay Device Group',
			device_group_enabled    => 1,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $dg_handle_1 = ixiangpf::status_item('device_group_handle');

	my $mac_start		= "0000.0004.0001";
	my $mac_step		= "0000.0000.1000";

	my $command_status = ixiangpf::interface_config ({
			protocol_handle		=> $dg_handle_1,
			src_mac_addr       	=> $mac_start,
			src_mac_addr_step	=> $mac_step,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $ethernet_handle_1 = ixiangpf::status_item('ethernet_handle');

	#####################################################
	# DHCP Relay Stack							    #
	#####################################################

	my $multivalue_1_status = ixiangpf::multivalue_config({
		pattern              =>  'single_value',
		single_value		 => '2000:0:0:0:0:0:0:1'
    });

    @status_keys = ixiangpf::status_item_keys();
    my $multivalue_1_handle = ixiangpf::status_item('multivalue_handle');

	
	my $multivalue_2_status = ixiangpf::multivalue_config({
		pattern             =>  'single_value',
		single_value 		=> '3000:0:0:0:0:0:0:1'
    });

    @status_keys = ixiangpf::status_item_keys();
    my $multivalue_2_handle = ixiangpf::status_item('multivalue_handle');

	$_result_ = ixiangpf::emulation_dhcp_group_config ({
			handle							=>	$ethernet_handle_1,
			mode 							=> 'create_relay_agent',
			dhcp_range_ip_type 				=> 'ipv6',
			dhcp_range_relay_type 			=> 'lightweight',
			dhcp_range_relay_destination 	=> $multivalue_1_handle,
			dhcp_range_relay_first_address 	=> $multivalue_2_handle,
			protocol_name  					=> '{DHCPv6 LDRA 1}',
			});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $relay_1_handle = ixiangpf::status_item('dhcpv6relayagent_handle');
	
	$_result_ = ixiangpf::topology_config ({
			topology_handle         => $dg_handle_1,	
			device_group_multiplier	=> 50,
			device_group_name       => 'DHCP Client Device Group',
			device_group_enabled    => 1,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $dg_handle_3 = ixiangpf::status_item('device_group_handle');

	my $mac_start1		= "0000.0005.0001";
	my $mac_step1		= "0000.0000.1000";

	$_result_ = ixiangpf::interface_config ({
			protocol_handle		=> $dg_handle_3,
			src_mac_addr       	=> $mac_start1,
			src_mac_addr_step	=> $mac_step1,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $ethernet_handle_3 = ixiangpf::status_item('ethernet_handle');

	#####################################################
	# DHCP Client Stack							    #
	#####################################################

	$_result_ = ixiangpf::emulation_dhcp_group_config ({
			handle				=>	$ethernet_handle_3 ,
			dhcp_range_ip_type 	=> 'ipv6',
			protocol_name       => '{DHCPv6 Client 1}',			
			});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $dhcp_client_handle = ixiangpf::status_item('dhcpv6client_handle');
	
	#####################################################
	# Add TLVs							    #
	#####################################################
	print "\n";
	print "Use tlv_config to add TLV option 12 on DHCPv6Relay:\n";	
	print "\n";
	$_result_ = ixiangpf::tlv_config ({
			protocol 	=> 'dhcp6_relay',
			handle		=>		$relay_1_handle ,
			mode	 	=> 'create_tlv',
			tlv_name 	=> "12"
			});
	&catch_error();
	
	@status_keys = ixiangpf::status_item_keys();
	print "\n";
	print "tlv_config returns the following keys:\n";
	ixiangpf::PrintHash(ixiangpf::get_result_hash());
	print "\n";
# tlv_config returns the following keys:
# status => 1
# tlv_type_handle => /topology:1/deviceGroup:1/ethernet:1/lightweightDhcpv6relayAgent:2/lightweightDhcp6RelayTlvProfile/tlvProfile/tlv:4/type
# tlv_value_handle => /topology:1/deviceGroup:1/ethernet:1/lightweightDhcpv6relayAgent:2/lightweightDhcp6RelayTlvProfile/tlvProfile/tlv:4/value
# tlv_length_handle => /topology:1/deviceGroup:1/ethernet:1/lightweightDhcpv6relayAgent:2/lightweightDhcp6RelayTlvProfile/tlvProfile/tlv:4/length
# tlv_handle => /topology:1/deviceGroup:1/ethernet:1/lightweightDhcpv6relayAgent:2/lightweightDhcp6RelayTlvProfile/tlvProfile/tlv:4
# /topology:1/deviceGroup:1/ethernet:1/lightweightDhcpv6relayAgent:2/lightweightDhcp6RelayTlvProfile/tlvProfile/tlv:4/type =>
#    tlv_field_handle => /topology:1/deviceGroup:1/ethernet:1/lightweightDhcpv6relayAgent:2/lightweightDhcp6RelayTlvProfile/tlvProfile/tlv:4/type/object:1/field
# /topology:1/deviceGroup:1/ethernet:1/lightweightDhcpv6relayAgent:2/lightweightDhcp6RelayTlvProfile/tlvProfile/tlv:4/value =>
#    tlv_field_handle => /topology:1/deviceGroup:1/ethernet:1/lightweightDhcpv6relayAgent:2/lightweightDhcp6RelayTlvProfile/tlvProfile/tlv:4/value/object:1/field

	my $tlv_12_handle 			= ixiangpf::status_item('tlv_handle');
	my $tlv_12_handle_value 	= ixiangpf::status_item('tlv_value_handle');
	my $tlv_12_handle_type 		= ixiangpf::status_item('tlv_type_handle');
	my $tlv_12_handle_length 	= ixiangpf::status_item('tlv_length_handle');
	my $tlv_12_handle_value_field 	= ixiangpf::status_item("$tlv_12_handle_value.tlv_field_handle");
	my $tlv_12_handle_type_field 	= ixiangpf::status_item("$tlv_12_handle_type.tlv_field_handle");

	#####################################################
	# Modify & check TLV values					        #
	#####################################################	
	
	#####################################################
	# TLV 12							    #
	#####################################################

	print "Use tlv_config to modify a field of the TLV option 12 on DHCPv6Relay:\n";	
	print "\n";
	
	my $multivalue_3_status = ixiangpf::multivalue_config({
    	pattern             => 'single_value',
		single_value 		=> '3000:0:0:0:0:0:0:10',
    });

    @status_keys = ixiangpf::status_item_keys();
    my $multivalue_3_handle = ixiangpf::status_item('multivalue_handle');
	
	$_result_ = ixiangpf::tlv_config ({
			handle		=>	$tlv_12_handle_value_field ,
			mode 		=> 'modify',
			field_value => $multivalue_3_handle,
			});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();

	###################################################
	#TLV 18							    #
	###################################################
	print "\n";
	print "Use tlv_config to modify one of the default TLVs: Modify option 18 on DHCPv6Relay:\n";
	print "\n";
	my $tlv_18_handle 		= $relay_1_handle.'/lightweightDhcp6RelayTlvProfile/tlvProfile/defaultTlv:1';
	my $tlv_18_value_handle = $tlv_18_handle.'/value/object:1/field';
	
	my $multivalue_4_status = ixiangpf::multivalue_config({
		pattern => 'string',
		string_pattern => "Interface{Inc:1,1}"
    });

    @status_keys = ixiangpf::status_item_keys();
    my $multivalue_4_handle = ixiangpf::status_item('multivalue_handle');
	
	$_result_ = ixiangpf::tlv_config ({
			handle		=>	$tlv_18_value_handle ,
			mode 		=> 'modify',
			field_value => $multivalue_4_handle,
			});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();


# #############################################################################
#                               CLEANUP SESSION
# #############################################################################

	print '\n\nPerforming final session cleanup...\n';

	my $_result_ = ixiangpf::cleanup_session();
	&catch_error();

	print '\nSession cleanup completed.\n';	
	return $PASSED
}
	

	
my $test_result = main(@ARGV);
print "\nTest execution complete.\nStatus: $test_result\n";


