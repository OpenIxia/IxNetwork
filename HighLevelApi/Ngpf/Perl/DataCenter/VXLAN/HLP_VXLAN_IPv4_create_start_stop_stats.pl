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
#	 The script configures 2 VXLAN stacks and the chained device groups        #
#	 with IPv4 VMs. Start protocols and get/print stats.    				   #
#																			   #
# Module:                                                                      #
#    The sample was tested on a FlexAP10G16S module.                   		   #
#                                                                              #
################################################################################

# Source all libraries in the beginning
use warnings;
use strict;
use bignum;
use Carp;
use Cwd 'abs_path';

# use lib where the HLPAPI files are located

use lib "C:/Program Files (x86)/Ixia/hltapi/4.90.0.64/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.30";
use lib "C:/Program Files (x86)/Ixia/hltapi/4.90.0.64/TclScripts/lib/hltapi/library/common/ixiangpf/perl";

use ixiahlt {
IXIA_VERSION => 'HLTSET166',
TclAutoPath => ['C:/Program Files (x86)/Ixia/IxOS/6.70.0.30','C:/Program Files (x86)/Ixia/hltapi/4.90.0.64/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.30','C:/Program Files (x86)/Ixia/hltapi/4.90.0.64/TclScripts/lib', 'C:/Program Files (x86)/Ixia/IxNetwork/7.30.0.213-EB/TclScripts/lib/ixTcl1.0','C:/Program Files (x86)/Ixia/IxNetwork/7.30.0.213-EB/TclScripts/lib/IxTclNetwork'],
};

use ixiahlt;
use ixiaixn;
use ixiangpf;


# Declare the Chassis IP address and the Ports that will be used
my $test_name              = "basic_VXLAN_config";
my $chassis                = "10.205.15.184";
my $tcl_server             = "10.205.15.184";
my @port_list              = ("9/1", "9/9");
my $ixnetwork_tcl_server   = "localhost";
my $wait_time              = 5;
my $test_dir_path          = abs_path();

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

# Initialize values for HLPAPI scripts
my $_result_               = '';
my $status                 = '';
my $port_handle            = '';
my @status_keys            = ();
my %status_keys            = ();
my @portHandleList         = ();

my $PASSED				   = '0';
my $FAILED				   = '1';

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

	my $port_1 = $portHandleList[0];
	my $port_2 = $portHandleList[1];

	print ("\nIxia port handles are @portHandleList ...\n");
	print ("End connecting to chassis ...\n");

	#####################################################
	# Create a topology and a device group for VXLAN    #
	#####################################################

	my $topology_status = ixiangpf::topology_config ({
			topology_name           => 'VTEP Group 1',
			port_handle				=> $port_1,
			device_group_multiplier	=> 3,
			device_group_name       => 'VXLAN DG 1',
			device_group_enabled    => 1,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $dg_handle_1 = ixiangpf::status_item('device_group_handle');

	my $mac_start		= "0000.0005.0001";
	my $mac_step		= "0000.0000.1000";

	my $command_status = ixiangpf::interface_config ({
			protocol_handle		=> $dg_handle_1,
			src_mac_addr       	=> $mac_start,
			src_mac_addr_step		=> $mac_step,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $ethernet_handle_1 = ixiangpf::status_item('ethernet_handle');

	#####################################################
	# VXLAN 1 Stack									    #
	#####################################################

	my $vxlan_1_status = ixiangpf::emulation_vxlan_config ({
			create_ig	 				=>				'1'								,
			enable_resolve_gateway		=>				'1'								,			
			enable_static_info			=>				'1'								,		
			gateway						=>				'100.0.0.100'					,		
			gateway_step				=>				'0.0.0.1'						,		
			handle						=>				$ethernet_handle_1				,			
			ig_enable_resolve_gateway	=>				'1'								,				
			ig_gateway					=>				'70.0.0.100'					,		
			ig_gateway_step				=>				'0.0.0.1'						,			
			ig_intf_ip_addr				=>				'70.0.0.1'						,				
			ig_intf_ip_addr_step		=>				'0.0.0.1'						,				
			ig_intf_ip_prefix_length	=>				'16'							,				
			ig_mac_address_init			=>				'00:11:22:33:00:00'				,							
			ig_mac_address_step			=>				'00:00:00:00:00:11'				,							
			ig_mac_mtu					=>				'1453'							,	
			ig_manual_gateway_mac		=>				'00:00:00:00:00:12'				,							
			ig_manual_gateway_mac_step	=>				'00:00:00:00:00:01'				,								
			ig_vlan_id					=>				'300,400'						,	
			ig_vlan_id_step				=>				'1,1'							,		
			ig_vlan_user_priority		=>				'1,2'							,			
			intf_ip_addr				=>				'100.0.0.1'						,			
			intf_ip_addr_step			=>				'0.0.0.1'						,			
			intf_ip_prefix_length		=>				'16'							,			
			ip_num_sessions				=>				'3'								,		
			ipv4_multicast				=>				'225.1.1.1'						,			
			mode						=>				'create'						,
			ip_to_vxlan_multiplier		=>				'1'								,			
			remote_info_active			=>				'1' 							,			
			remote_vm_static_ipv4		=>				'100.0.0.101'					,					
			remote_vm_static_mac		=>				'aa:bb:cc:00:00:01'				,							
			remote_vtep_ipv4			=>				'70.0.0.100'					,				
			sessions_per_vxlan			=>				'2'								,		
			static_info_count			=>				'1'								,		
			vlan_id						=>				'100,200'						,	
			vlan_id_step				=>				'1,1'							,	
			vlan_user_priority			=>				'2,6'							,		
			vni							=>				'2233'							,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();

	my $vxlan_1_handle = ixiangpf::status_item('vxlan_handle');

	#####################################################
	# Create a topology and a device group for VXLAN    #
	#####################################################

	my $topology_status = ixiangpf::topology_config ({
			topology_name           => 'VTEP Group 2',
			port_handle				=> $port_2,
			device_group_multiplier	=> 3,
			device_group_name       => 'VXLAN DG 2',
			device_group_enabled    => 1,
	});

	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $dg_handle_1 = ixiangpf::status_item('device_group_handle');

	my $mac_start		= "0000.0006.0001";
	my $mac_step		= "0000.0000.1000";

	my $command_status = ixiangpf::interface_config ({
			protocol_handle		=> $dg_handle_1,
			src_mac_addr       	=> $mac_start,
			src_mac_addr_step		=> $mac_step,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $ethernet_handle_2 = ixiangpf::status_item('ethernet_handle');

	#####################################################
	# VXLAN 2 Stack									    #
	#####################################################

	my $vxlan_2_status = ixiangpf::emulation_vxlan_config ({
			create_ig	 				=>				'1'								,
			enable_resolve_gateway		=>				'1'								,			
			enable_static_info			=>				'1'								,		
			gateway						=>				'100.0.0.1'						,		
			gateway_step				=>				'0.0.0.1'						,		
			handle						=>				$ethernet_handle_2				,			
			ig_enable_resolve_gateway	=>				'1'								,				
			ig_gateway					=>				'70.0.0.1'						,		
			ig_gateway_step				=>				'0.0.0.1'						,			
			ig_intf_ip_addr				=>				'70.0.0.100'					,				
			ig_intf_ip_addr_step		=>				'0.0.0.1'						,				
			ig_intf_ip_prefix_length	=>				'16'							,				
			ig_mac_address_init			=>				'00:56:22:33:00:00'				,							
			ig_mac_address_step			=>				'00:00:00:00:00:11'				,							
			ig_mac_mtu					=>				'1453'							,	
			ig_manual_gateway_mac		=>				'00:00:00:00:00:72'				,							
			ig_manual_gateway_mac_step	=>				'00:00:00:00:00:01'				,								
			ig_vlan_id					=>				'300,400'						,	
			ig_vlan_id_step				=>				'1,1'							,		
			ig_vlan_user_priority		=>				'1,2'							,			
			intf_ip_addr				=>				'100.0.0.100'					,			
			intf_ip_addr_step			=>				'0.0.0.1'						,			
			intf_ip_prefix_length		=>				'16'							,			
			ip_num_sessions				=>				'3'								,		
			ipv4_multicast				=>				'225.1.1.1'						,			
			mode						=>				'create'						,
			ip_to_vxlan_multiplier		=>				'1'								,			
			remote_info_active			=>				'1' 							,			
			remote_vm_static_ipv4		=>				'100.0.0.101'					,					
			remote_vm_static_mac		=>				'aa:bb:cc:00:00:01'				,							
			remote_vtep_ipv4			=>				'70.0.0.100'					,				
			sessions_per_vxlan			=>				'2'								,		
			static_info_count			=>				'1'								,		
			vlan_id						=>				'100,200'						,	
			vlan_id_step				=>				'1,1'							,	
			vlan_user_priority			=>				'2,6'							,		
			vni							=>				'2233'							,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();

	my $vxlan_2_handle = ixiangpf::status_item('vxlan_handle');

	#####################################################
	# START VXLAN									    #
	#####################################################

	my $vxlan_start_1_status = ixiangpf::emulation_vxlan_control ({
			action		=>		'start'		,
			handle		=>		'/topology:1/deviceGroup:1/ethernet:1/ipv4:1/vxlan:1'	,
	});
	&catch_error();

	my $vxlan_start_2_status = ixiangpf::emulation_vxlan_control ({
			action		=>		'start'		,
			handle		=>		'/topology:2/deviceGroup:1/ethernet:1/ipv4:1/vxlan:1'	,
	});
	&catch_error();

	my $test_control_status = ixiangpf::test_control ({
			action		=>		'start_all_protocols'	,
	});
	&catch_error();

	sleep (10);

	#####################################################
	# VXLAN	STATS									    #
	#####################################################

	my $vxlan_1_stats = ixiangpf::emulation_vxlan_stats ({
			mode			=>		'aggregate_stats'		,
			port_handle		=>		$port_1	,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();

	print "\nThe aggregate statistics for VXLAN port 1 are:\n";
	my $vxlan_1_aggregate_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($vxlan_1_aggregate_stats);
	print "\n";	

	my $vxlan_2_stats = ixiangpf::emulation_vxlan_stats ({
			mode			=>		'aggregate_stats'		,
			port_handle		=>		$port_2	,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();

	print "\nThe aggregate statistics for VXLAN port 2 are:\n";
	my $vxlan_2_aggregate_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($vxlan_2_aggregate_stats);
	print "\n";	

	if ($vxlan_1_aggregate_stats->{$port_1}->{'aggregate'}->{'sessions_up'} ne '3') {
		print ("FAILED - VXLAN not negociated!");
		return $FAILED
	}

	if ($vxlan_2_aggregate_stats->{$port_2}->{'aggregate'}->{'sessions_up'} ne '3') {
		print ("FAILED - VXLAN not negociated!");
		return $FAILED
	}

	print "\n\nPerforming final session cleanup...\n";
	
	$_result_ = ixiangpf::cleanup_session();
	&catch_error();
	
	print "\nSession cleanup completed.\n";
	
	return $PASSED
}

my $test_result = main(@ARGV);
print "\nTest execution complete.\nStatus: $test_result\n";