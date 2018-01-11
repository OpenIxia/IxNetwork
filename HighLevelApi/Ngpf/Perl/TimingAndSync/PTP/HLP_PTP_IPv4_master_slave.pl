################################################################################
# Version 1.0    $Revision: #1 $
# $Author: Daria Badea
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    04-01-2014 
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
#	 The script configures 2 PTP stacks, master and slave.					   #
#	 Dynamics: Start/stop protocols and get stats.     						   #
#																			   #
# Module:                                                                      #
#    The sample was tested on a LSM XM8S module.	                   		   #
#                                                                              #
################################################################################


# Source all libraries in the beginning
use warnings;
use strict;
use bignum;
use Carp;
use Cwd 'abs_path';

# use lib where the HLPAPI files are located

use lib "C:/Program Files (x86)/Ixia/hltapi/4.90.0.72/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.30";
use lib "C:/Program Files (x86)/Ixia/hltapi/4.90.0.72/TclScripts/lib/hltapi/library/common/ixiangpf/perl";

use ixiahlt {
IXIA_VERSION => 'HLTSET166',
TclAutoPath => ['C:/Program Files (x86)/Ixia/IxOS/6.70.0.50','C:/Program Files (x86)/Ixia/hltapi/4.90.0.72/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.30','C:/Program Files (x86)/Ixia/hltapi/4.90.0.72/TclScripts/lib', 'C:/Program Files (x86)/Ixia/IxNetwork/7.30.0.244-EB/TclScripts/lib/ixTcl1.0','C:/Program Files (x86)/Ixia/IxNetwork/7.30.0.244-EB/TclScripts/lib/IxTclNetwork'],
};

use ixiahlt;
use ixiaixn;
use ixiangpf;


# Declare the Chassis IP address and the Ports that will be used
my $test_name              = "basic_PTP_IPv4_config";
my $chassis                = "10.205.15.184";
my $tcl_server             = "10.205.15.184";
my @port_list              = ("9/1", "9/9");
my $ixnetwork_tcl_server   = "localhost";

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
	# Create a topology and a device group for PTP      #
	#####################################################
	
	print ("\n\nConfiguring PTP master...\n\n");
	
	$_result_ = ixiangpf::topology_config ({
			topology_name           => 'PTP Master Topology',
			port_handle				=> $port_0,
			device_group_multiplier	=> 1,
			device_group_name       => 'PTP Master Device Group',
			device_group_enabled    => 1,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $dg_handle_1 = ixiangpf::status_item('device_group_handle');

	my $mac_start		= "0000.0005.0001";
	my $mac_step		= "0000.0000.1000";

	$_result_ = ixiangpf::interface_config ({
			protocol_handle		=> $dg_handle_1,
			src_mac_addr       	=> $mac_start,
			src_mac_addr_step		=> $mac_step,
			intf_ip_addr			=> "111.1.1.1" ,
			gateway					=> "111.1.1.2" ,
			ipv4_resolve_gateway	=> "0" ,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $ethernet_handle_1 = ixiangpf::status_item('ethernet_handle');
	my $ipv4_handle_1 = ixiangpf::status_item('ipv4_handle');

	#####################################################
	# PTP Master 1 Stack							    #
	#####################################################

	$_result_ = ixiangpf::ptp_over_ip_config ({
			parent_handle						=>		$ipv4_handle_1 ,
			profile								=> 		"ieee1588" ,
			role								=> 		"master" ,
			mode                                =>      "create" ,
			name                                =>      "PTP IPv4 Master" ,
			port_number                         =>     	"6323" ,
			communication_mode                  => 		"multicast" ,
			domain                              => 		"123" ,
			priority1                           => 		"10" ,
			priority2                           => 		"100" ,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $ptp_master_handle = ixiangpf::status_item('ptp_handle');

	#####################################################
	# Create a topology and a device group for PTP      #
	#####################################################
	
	print ("\n\nConfiguring PTP slave...\n\n");
	
	$_result_ = ixiangpf::topology_config ({
			topology_name           => 'PTP Slave Topology',
			port_handle				=> $port_1,
			device_group_multiplier	=> 1,
			device_group_name       => 'PTP Slave Device Group',
			device_group_enabled    => 1,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $dg_handle_2 = ixiangpf::status_item('device_group_handle');

	my $mac_start		= "0000.0006.0001";
	my $mac_step		= "0000.0000.1000";

	my $command_status = ixiangpf::interface_config ({
			protocol_handle		=> $dg_handle_2,
			src_mac_addr       	=> $mac_start,
			src_mac_addr_step		=> $mac_step,
			intf_ip_addr			=> "111.1.1.2" ,
			gateway					=> "111.1.1.1" ,
			ipv4_resolve_gateway	=> "0" ,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $ethernet_handle_2 = ixiangpf::status_item('ethernet_handle');
	my $ipv4_handle_2 = ixiangpf::status_item('ipv4_handle');

	#####################################################
	# PTP Slave 1 Stack			    				    #
	#####################################################

	$_result_ = ixiangpf::ptp_over_ip_config ({
			parent_handle						=>		$ipv4_handle_2 ,
			profile								=> 		"ieee1588" ,
			role								=> 		"slave" ,
			mode                                =>      "create" ,
			name                                =>      "PTP IPv4 Slave" ,
			port_number                         =>     	"6323" ,
			communication_mode                  => 		"multicast" ,
			domain                              => 		"123" ,
			priority1                           => 		"10" ,
			priority2                           => 		"100" ,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();
	my $ptp_slave_handle = ixiangpf::status_item('ptp_handle');
	
	#####################################################
	# START PTP					    				    #
	#####################################################
	
	print ("\n\nStart PTP...\n\n");
	
	$_result_ = ixiangpf::ptp_over_ip_control ({
			action		=>		'start'	,
			handle		=>		$ptp_master_handle	,
	});
	&catch_error();

	sleep (5);

	$_result_ = ixiangpf::ptp_over_ip_control ({
			action		=>		'start'	,
			handle		=>		$ptp_slave_handle	,
	});
	&catch_error();	
	
	sleep (20);

	#####################################################
	# PTP STATS					    				    #
	#####################################################
	
	print ("\n\nCollect PTP stats...\n\n");
	
	$_result_ = ixiangpf::ptp_over_ip_stats ({
			mode			=>		'aggregate'		,
			port_handle		=>		$port_0	,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();

	print "\nThe aggregate statistics for PTP port 1 are:\n";
	my $ptp_1_aggregate_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($ptp_1_aggregate_stats);
	print "\n";	

	$_result_ = ixiangpf::ptp_over_ip_stats ({
			mode			=>		'aggregate'		,
			port_handle		=>		$port_1	,
	});
	&catch_error();

	@status_keys = ixiangpf::status_item_keys();

	print "\nThe aggregate statistics for PTP port 2 are:\n";
	my $ptp_2_aggregate_stats = ixiangpf::get_result_hash();
	ixiangpf::PrintHash($ptp_2_aggregate_stats);
	print "\n";	

	if ($ptp_1_aggregate_stats->{$port_0}->{'gen'}->{'sessions_up'} ne '1') {
		print ("FAILED - PTP Master sessions not up!");
		return $FAILED
	}

	if ($ptp_2_aggregate_stats->{$port_1}->{'gen'}->{'sessions_up'} ne '1') {
		print ("FAILED - PTP Slave sessions not up!");
		return $FAILED
	}
	
	#####################################################
	# STOP PTP					    				    #
	#####################################################
	
	print ("\n\nStop PTP...\n\n");
	
	$_result_ = ixiangpf::ptp_over_ip_control ({
			action		=>		'stop'	,
			handle		=>		$ptp_master_handle	,
	});
	&catch_error();

	sleep (5);

	$_result_ = ixiangpf::ptp_over_ip_control ({
			action		=>		'stop'	,
			handle		=>		$ptp_slave_handle	,
	});
	&catch_error();	
	
	print "\n\nPerforming final session cleanup...\n";
	
	my $_result_ = ixiangpf::cleanup_session();
	&catch_error();
	
	print "\nSession cleanup completed.\n";
	
	return $PASSED
}

my $test_result = main(@ARGV);
print "\nTest execution complete.\nStatus: $test_result\n";