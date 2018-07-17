#################################################################################
# Version 1    $Revision: #1 $
# $Author: cm $
#
#    Copyright © 1997 - 2014 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    08-18-2014 RCsutak - created sample
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
#   This sample connects to an IxNetwork client and loads an ixncfg containing #
#   traffic items. Using the retrieved information, it sets the global traffic #
#   option called "Frame Ordering" to the new option "Peak Loading".           #
# Module:                                                                      #
#   The sample was tested on a LSM XMVDC16NG module.                           #
#                                                                              #
################################################################################

use lib ".";
use lib "..";
use lib "../..";

#use lib "wherever your ixiatcl.pm is installed";
#use lib "wherever your ixiangpf.pm is installed";


use ixiahlt;
use ixiangpf;

use warnings;
use strict;
use bignum;
use Carp;

use IxNetwork;

our $HashRef = {};
our $command_status = '';

sub peak_loading {
	my $_result_ = '';
    my $_control_status_ = '';
  	my @status_keys = ();

	

# Connection 
	my $chassis = 'ixro-hlt-xm2-09';
	my $tcl_server = 'ixro-hlt-xm2-09';
	my @port_list = ([ '2/1', '2/2', '2/3', '2/4']);
	my $guard_rail = 'statistics';
	my $ixNetServer = 'localhost';
    my $config_file = 'peak_loading_ipv4_vlan_traffic.ixncfg';
	


        
	$_result_ = ixiangpf::connect({
		port_list	         	=> \@port_list,
		device				 	=> $chassis,
		ixnetwork_tcl_server 	=> $ixNetServer,
		tcl_server				=> $tcl_server,
        config_file             => $config_file,
        break_locks             => 1,
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
	
    my $ixNet =  new IxNetwork(); 
	$ixNet->connect('localhost', '-port', 8009, '-version', '7.40');
    
    my $ti_name=ixiangpf::status_item('traffic_config');
    my @aux =split('{',$ti_name);
    my @aux2 = split('}',$aux[1]);
    $ti_name = $aux2[0];
    my $ti = ixiangpf::status_item($ti_name.".traffic_config.traffic_item");
    print("traffic item = $ti\n");
    
    my $run_status = ixiangpf::test_control({
		action		=> 'start_all_protocols',
	});
	
	@status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		print "Error: $error";
		return "FAILED - $error";
	}

sleep(5);    
    $_result_=ixiangpf::traffic_config({
        mode                            => 'modify',
        global_dest_mac_retry_count     => '3',
        global_dest_mac_retry_delay     => '3',
        global_enable_dest_mac_retry    => '1',
        global_enable_mac_change_on_fly => '1',
        global_frame_ordering           => 'peak_loading',
        stream_id                       => $ti,
    });
    
    @status_keys = ixiangpf::status_item_keys();
	$command_status = ixiangpf::status_item('status');
	if ($command_status != $ixiangpf::SUCCESS) {
		my $error = ixiangpf::status_item('log');
		print "Error: $error";
		return "FAILED - $error";
	}
    
my $ordering_mode = $ixNet->getAttribute('/traffic','-frameOrderingMode');
print "Frame ordering mode set is : $ordering_mode\n";

print "SUCCESS - Script has run without errors!\n";
return 1;
}
&peak_loading;