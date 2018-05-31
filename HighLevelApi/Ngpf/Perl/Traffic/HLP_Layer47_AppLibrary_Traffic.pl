################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    01/20/2014 - Alexandru Iordachescu - created sample                       #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#   The script below walks through the workflow of an AppLibrary end to end    #	
#	test, using the below steps:											   #	
#		1. Connection to the chassis, IxNetwork Tcl Server 					   #
#		2. Topology configuration											   #
#		3. Configure trafficItem 1 for Layer 4-7 AppLibrary Profile			   #	
#		4. Configure trafficItem 2 for Layer 4-7 AppLibrary Profile			   #
#		5. Start protocols													   #	
#		6. Apply and run AppLibrary traffic									   #
#		7. Drill down per IP addresses during traffic run					   #
#		8. Stop Traffic.													   #	
#																			   #	
#                                                                              #
################################################################################

################################################################################
# Utils									       								   #	
################################################################################
use warnings;
use strict;
use bignum;
use Carp;
use Cwd 'abs_path';

use lib "C:/Program Files (x86)/Ixia/hltapi/4.97.0.2/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.50";
use lib "C:/Program Files (x86)/Ixia/hltapi/4.97.0.2/TclScripts/lib/hltapi/library/common/ixiangpf/perl";

use ixiangpf;

if (!(defined &handle_error)) {
    sub handle_error() {
        eval {
            ixnHLT_errorHandler('');
        };
        if ($@) {
            my $log = ixiangpf::status_item('log');
            Carp::confess("log: $log\n\n");
        }
    }
}
if (!(defined &ixnHLT_logger)) {
  sub ixnHLT_logger {my $s=shift; print($s."\n");}
}

################################################################################
# Connection to the chassis, IxNetwork Tcl Server                 	       #
################################################################################
my %ixnHLT = ();
my @chassis = ('10.205.23.34');
my $tcl_server = '10.205.23.34';
my $ixnetwork_tcl_server = 'localhost:8109';
my @port_list = ([ '2/9', '2/10', '2/11', '2/12' ]);
my @vport_name_list = ([ 'Ethernet - 001', 'Ethernet - 002', 'Ethernet - 003', 'Ethernet - 004' ]);

@{$ixnHLT{'path_list'}} = ([ '//vport:<1>', '//vport:<2>', '//vport:<3>', '//vport:<4>' ]);

my $_result_ = ixiangpf::connect({
reset => 1,
device => \@chassis,
port_list => \@port_list,
ixnetwork_tcl_server => $ixnetwork_tcl_server,
tcl_server => $tcl_server,
});

if (ixiangpf::status_item('status') != 1) {
    ixnHLT_errorHandler('connect');
	}
	

my @chassis_vport_list = ();
for (my $_x = 0; $_x < $#chassis+1; $_x++) {
    my @ch_vport_list = ();
    for (my $_y = 0; $_y < $#{$port_list[$_x]}+1; $_y++) {
        my $port = $port_list[$_x][$_y];
        my $path = $ixnHLT{'path_list'}[$_x][$_y];
        my $_ph = '';
        eval {
            $_ph = ixiangpf::status_item("port_handle.$chassis[$_x].$port");
        } or do {
            Carp::confess("could not connect to chassis=$chassis[$_x],port=<$port>");
        };
        $ixnHLT{"PORT-HANDLE,$path"} = $_ph;
        push @ch_vport_list, $_ph;
    }
    push @chassis_vport_list, \@ch_vport_list;
}

#for (my $_x = 0; $_x < $#chassis+1; $_x++) {
#    my $port_name_list = ([ $vport_name_list[$_x] ]);
#
#    ixiangpf::vport_info({
#        mode => 'set_info',
#       port_list => $chassis_vport_list[$_x],
#       port_name_list => $port_name_list
#   });
 #   if (ixiangpf::status_item('status') != 1) {
 #       ixnHLT_errorHandler('ixiangpf::vport_info');
  #  }
#}

################################################################################
# Configure Topology 1, Device Group 1                                         # 
################################################################################

my @status_keys = ();

my $topology_1_status = ixiangpf::topology_config ({
        topology_name      => "{Topology 1}",
        port_handle        => "$ixnHLT{'PORT-HANDLE,//vport:<1>'}", 
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
@status_keys = ixiangpf::status_item_keys();
my $topology_1_handle = ixiangpf::status_item('topology_handle');
    $ixnHLT{'HANDLE,//topology:<1>'} = $topology_1_handle;
    
my $device_group_1_status = ixiangpf::topology_config ({
        topology_handle              => "$topology_1_handle",
        device_group_name            => "{Device Group 1}",
        device_group_multiplier      => "45",
        device_group_enabled         => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_1_handle = ixiangpf::status_item('device_group_handle');
    $ixnHLT{'HANDLE,//topology:<1>/deviceGroup:<1>'} = $deviceGroup_1_handle;
    
################################################################################
# Configure protocol interfaces for first topology                             # 
################################################################################ 

my $multivalue_1_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "00.11.01.00.00.01",
        counter_step           => "00.00.00.00.00.01",
        counter_direction      => "increment",
        nest_step              => "00.00.01.00.00.00",
        nest_owner             => "$topology_1_handle",
        nest_enabled           => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
@status_keys = ixiangpf::status_item_keys();
my $multivalue_1_handle = ixiangpf::status_item('multivalue_handle');

my $ethernet_1_status = ixiangpf::interface_config ({
        protocol_name                => "{Ethernet 1}",
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
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
@status_keys = ixiangpf::status_item_keys();
my $ethernet_1_handle = ixiangpf::status_item('ethernet_handle');
$ixnHLT{'HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>'} = $ethernet_1_handle;

my $multivalue_2_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "100.1.0.1",
        counter_step           => "0.0.0.1",
        counter_direction      => "increment",
        nest_step              => "0.1.0.0",
        nest_owner             => "$topology_1_handle",
        nest_enabled           => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
@status_keys = ixiangpf::status_item_keys();
    my $multivalue_2_handle = ixiangpf::status_item('multivalue_handle');
    
my $multivalue_3_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "101.1.0.1",
        counter_step           => "255.255.255.255",
        counter_direction      => "decrement",
        nest_step              => "0.0.0.1",
        nest_owner             => "$topology_1_handle",
        nest_enabled           => "0",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
@status_keys = ixiangpf::status_item_keys();
    my $multivalue_3_handle = ixiangpf::status_item('multivalue_handle');
    
my $ipv4_1_status = ixiangpf::interface_config ({
        protocol_name                     => "{IPv4 1}",
        protocol_handle                   => "$ethernet_1_handle",
        ipv4_resolve_gateway              => "1",
        ipv4_manual_gateway_mac           => "00.00.00.00.00.01",
        ipv4_manual_gateway_mac_step      => "00.00.00.00.00.00",
        gateway                           => "$multivalue_3_handle",
        intf_ip_addr                      => "$multivalue_2_handle",
        netmask                           => "255.255.255.0",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
@status_keys = ixiangpf::status_item_keys();
    my $ipv4_1_handle = ixiangpf::status_item('ipv4_handle');
    $ixnHLT{'HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>'} = $ipv4_1_handle;

################################################################################
# Configure Topology 2, Device Group 2                                         # 
################################################################################ 

my $topology_2_status = ixiangpf::topology_config ({
        topology_name      => "{Topology 2}",
        port_handle        => "$ixnHLT{'PORT-HANDLE,//vport:<2>'}",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }

@status_keys = ixiangpf::status_item_keys();
my $topology_2_handle = ixiangpf::status_item('topology_handle');
    $ixnHLT{'HANDLE,//topology:<2>'} = $topology_2_handle;
    
my $device_group_2_status = ixiangpf::topology_config ({
        topology_handle              => "$topology_2_handle",
        device_group_name            => "{Device Group 2}",
        device_group_multiplier      => "45",
        device_group_enabled         => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }

@status_keys = ixiangpf::status_item_keys();
    my $deviceGroup_2_handle = ixiangpf::status_item('device_group_handle');
    $ixnHLT{'HANDLE,//topology:<2>/deviceGroup:<1>'} = $deviceGroup_2_handle;
	
################################################################################
# Configure protocol interfaces for second topology                            # 
################################################################################ 

my $multivalue_4_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "00.12.01.00.00.01",
        counter_step           => "00.00.00.00.00.01",
        counter_direction      => "increment",
        nest_step              => "00.00.01.00.00.00",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
@status_keys = ixiangpf::status_item_keys();
    my $multivalue_4_handle = ixiangpf::status_item('multivalue_handle');
    
my $ethernet_2_status = ixiangpf::interface_config ({
        protocol_name                => "{Ethernet 2}",
        protocol_handle              => "$deviceGroup_2_handle",
        mtu                          => "1500",
        src_mac_addr                 => "$multivalue_4_handle",
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
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
@status_keys = ixiangpf::status_item_keys();
    my $ethernet_2_handle = ixiangpf::status_item('ethernet_handle');
    $ixnHLT{'HANDLE,//topology:<2>/deviceGroup:<1>/ethernet:<1>'} = $ethernet_2_handle;
    
my $multivalue_5_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "101.1.0.1",
        counter_step           => "0.0.0.1",
        counter_direction      => "increment",
        nest_step              => "0.1.0.0",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
@status_keys = ixiangpf::status_item_keys();
    my $multivalue_5_handle = ixiangpf::status_item('multivalue_handle');
    

my $multivalue_6_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "100.1.0.1",
        counter_step           => "255.255.255.255",
        counter_direction      => "decrement",
        nest_step              => "0.0.0.1",
        nest_owner             => "$topology_2_handle",
        nest_enabled           => "0",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
    @status_keys = ixiangpf::status_item_keys();
    my $multivalue_6_handle = ixiangpf::status_item('multivalue_handle');
    
my $ipv4_2_status = ixiangpf::interface_config ({
        protocol_name                     => "{IPv4 2}",
        protocol_handle                   => "$ethernet_2_handle",
        ipv4_resolve_gateway              => "1",
        ipv4_manual_gateway_mac           => "00.00.00.00.00.01",
        ipv4_manual_gateway_mac_step      => "00.00.00.00.00.00",
        gateway                           => "$multivalue_6_handle",
        intf_ip_addr                      => "$multivalue_5_handle",
        netmask                           => "255.255.255.0",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
    @status_keys = ixiangpf::status_item_keys();
    my $ipv4_2_handle = ixiangpf::status_item('ipv4_handle');
    $ixnHLT{'HANDLE,//topology:<2>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>'} = $ipv4_2_handle;
    
################################################################################
# Configure Topology 3, Device Group 3                                         # 
################################################################################

my $topology_3_status = ixiangpf::topology_config ({
        topology_name      => "{Topology 3}",
        port_handle        => "$ixnHLT{'PORT-HANDLE,//vport:<3>'}", 
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }

@status_keys = ixiangpf::status_item_keys();
my $topology_3_handle = ixiangpf::status_item('topology_handle');
    $ixnHLT{'HANDLE,//topology:<3>'} = $topology_3_handle; 
    
my $device_group_3_status = ixiangpf::topology_config ({
        topology_handle              => "$topology_3_handle",
        device_group_name            => "{Device Group 3}",
        device_group_multiplier      => "45",
        device_group_enabled         => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }

@status_keys = ixiangpf::status_item_keys();
    my $deviceGroup_3_handle = ixiangpf::status_item('device_group_handle');
    $ixnHLT{'HANDLE,//topology:<3>/deviceGroup:<1>'} = $deviceGroup_3_handle;
	
################################################################################
# Configure protocol interfaces for the third topology                         # 
################################################################################ 

my $multivalue_7_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "00.13.01.00.00.01",
        counter_step           => "00.00.00.00.00.01",
        counter_direction      => "increment",
        nest_step              => "00.00.01.00.00.00",
        nest_owner             => "$topology_3_handle",
        nest_enabled           => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
@status_keys = ixiangpf::status_item_keys();
    my $multivalue_7_handle = ixiangpf::status_item('multivalue_handle');
    
my $ethernet_3_status = ixiangpf::interface_config ({
        protocol_name                => "{Ethernet 3}",
        protocol_handle              => "$deviceGroup_3_handle",
        mtu                          => "1500",
        src_mac_addr                 => "$multivalue_7_handle",
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
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
@status_keys = ixiangpf::status_item_keys();
    my $ethernet_3_handle = ixiangpf::status_item('ethernet_handle');
    $ixnHLT{'HANDLE,//topology:<3>/deviceGroup:<1>/ethernet:<1>'} = $ethernet_3_handle;
    
my $multivalue_8_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "3000:0:0:1:0:0:0:2",
        counter_step           => "0:0:0:1:0:0:0:0",
        counter_direction      => "increment",
        nest_step              => "0:0:0:1:0:0:0:0",
        nest_owner             => "$topology_3_handle",
        nest_enabled           => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
@status_keys = ixiangpf::status_item_keys();
    my $multivalue_8_handle = ixiangpf::status_item('multivalue_handle');
    

my $multivalue_9_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "3000:0:1:1:0:0:0:2",
        counter_step           => "0:0:0:1:0:0:0:0",
        counter_direction      => "increment",
        nest_step              => "0:0:0:1:0:0:0:0",
        nest_owner             => "$topology_3_handle",
        nest_enabled           => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
    @status_keys = ixiangpf::status_item_keys();
    my $multivalue_9_handle = ixiangpf::status_item('multivalue_handle');
    
my $ipv6_3_status = ixiangpf::interface_config ({
        protocol_name                     => "{IPv6 3}",
        protocol_handle                   => "$ethernet_3_handle",
        ipv6_multiplier			  => "1",
        ipv6_resolve_gateway              => "1",
        ipv6_manual_gateway_mac           => "00.00.00.00.00.01",
        ipv6_manual_gateway_mac_step      => "00.00.00.00.00.00",
        ipv6_gateway                      => "$multivalue_9_handle",
        ipv6_gateway_step                 => "::0",
        ipv6_intf_addr                    => "$multivalue_8_handle",
        ipv6_intf_addr_step               => "::0",        
        ipv6_prefix_length                => "64",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
    @status_keys = ixiangpf::status_item_keys();
    my $ipv6_3_handle = ixiangpf::status_item('ipv6_handle');
    $ixnHLT{'HANDLE,//topology:<3>/deviceGroup:<1>/ethernet:<1>/ipv6:<1>'} = $ipv6_3_handle;
    
################################################################################
# Configure Topology 4, Device Group 4                                         # 
################################################################################

my $topology_4_status = ixiangpf::topology_config ({
        topology_name      => "{Topology 4}",
        port_handle        => "$ixnHLT{'PORT-HANDLE,//vport:<4>'}", 
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }

@status_keys = ixiangpf::status_item_keys();
my $topology_4_handle = ixiangpf::status_item('topology_handle');
    $ixnHLT{'HANDLE,//topology:<4>'} = $topology_4_handle; 
    
my $device_group_4_status = ixiangpf::topology_config ({
        topology_handle              => "$topology_4_handle",
        device_group_name            => "{Device Group 4}",
        device_group_multiplier      => "45",
        device_group_enabled         => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }

@status_keys = ixiangpf::status_item_keys();
    my $deviceGroup_4_handle = ixiangpf::status_item('device_group_handle');
    $ixnHLT{'HANDLE,//topology:<4>/deviceGroup:<1>'} = $deviceGroup_4_handle;
    
    
################################################################################
# Configure protocol interfaces for the fourth topology                        # 
################################################################################

my $multivalue_10_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "00.14.01.00.00.01",
        counter_step           => "00.00.00.00.00.01",
        counter_direction      => "increment",
        nest_step              => "00.00.01.00.00.00",
        nest_owner             => "$topology_4_handle",
        nest_enabled           => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
@status_keys = ixiangpf::status_item_keys();
    my $multivalue_10_handle = ixiangpf::status_item('multivalue_handle');
    
my $ethernet_4_status = ixiangpf::interface_config ({
        protocol_name                => "{Ethernet 4}",
        protocol_handle              => "$deviceGroup_4_handle",
        mtu                          => "1500",
        src_mac_addr                 => "$multivalue_10_handle",
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
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
@status_keys = ixiangpf::status_item_keys();
    my $ethernet_4_handle = ixiangpf::status_item('ethernet_handle');
    $ixnHLT{'HANDLE,//topology:<4>/deviceGroup:<1>/ethernet:<1>'} = $ethernet_4_handle;
    
my $multivalue_11_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "3000:0:1:1:0:0:0:2",
        counter_step           => "0:0:0:1:0:0:0:0",
        counter_direction      => "increment",
        nest_step              => "0:0:0:1:0:0:0:0",
        nest_owner             => "$topology_4_handle",
        nest_enabled           => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
@status_keys = ixiangpf::status_item_keys();
    my $multivalue_11_handle = ixiangpf::status_item('multivalue_handle');
    

my $multivalue_12_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "3000:0:0:1:0:0:0:2",
        counter_step           => "0:0:0:1:0:0:0:0",
        counter_direction      => "increment",
        nest_step              => "0:0:0:1:0:0:0:0",
        nest_owner             => "$topology_4_handle",
        nest_enabled           => "1",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
    @status_keys = ixiangpf::status_item_keys();
    my $multivalue_12_handle = ixiangpf::status_item('multivalue_handle');
    
my $ipv6_4_status = ixiangpf::interface_config ({
        protocol_name                     => "{IPv6 4}",
        protocol_handle                   => "$ethernet_4_handle",
        ipv6_multiplier			  => "1",
        ipv6_resolve_gateway              => "1",
        ipv6_manual_gateway_mac           => "00.00.00.00.00.01",
        ipv6_manual_gateway_mac_step      => "00.00.00.00.00.00",
        ipv6_gateway                      => "$multivalue_12_handle",
        ipv6_gateway_step                 => "::0",
        ipv6_intf_addr                    => "$multivalue_11_handle",
        ipv6_intf_addr_step               => "::0",        
        ipv6_prefix_length                => "64",
    });
	if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    
    @status_keys = ixiangpf::status_item_keys();
    my $ipv6_4_handle = ixiangpf::status_item('ipv6_handle');
    $ixnHLT{'HANDLE,//topology:<4>/deviceGroup:<1>/ethernet:<1>/ipv6:<1>'} = $ipv6_4_handle;
    
####################################################
##Configure traffic for all configuration elements##

##########################################################
# Configure trafficItem 1 for Layer 4-7 AppLibrary Profile
########################################################## 

my $traffic_item_1_status = ixiangpf::traffic_l47_config ({
        mode                        => "create",
        name                        => "{Traffic Item_1}",
        circuit_endpoint_type       => "ipv4_application_traffic",
        emulation_src_handle        => "$ixnHLT{'HANDLE,//topology:<1>'} ",
        emulation_dst_handle        => "$ixnHLT{'HANDLE,//topology:<2>'} ",
        objective_type              => "users",
        objective_value             => "100",
        objective_distribution      => "apply_full_objective_to_each_port",
        enable_per_ip_stats         => "1",
        flows                       => "{IRC_Login_Auth_Failure IRC_Private_Chat iSCSI_Read_and_Write iTunes_Desktop_App_Store iTunes_Mobile_App_Store Jabber_Chat Laposte_Webmail_1307 LinkedIn Linkedin_1301 LPD}",
    });

if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    @status_keys = ixiangpf::status_item_keys();
    my $trafficItem_1_handle = ixiangpf::status_item('traffic_l47_handle');
    $ixnHLT{'HANDLE,//traffic/trafficItem:<0>'} = $trafficItem_1_handle;
    
    
##########################################################
# Configure trafficItem 2 for Layer 4-7 AppLibrary Profile
##########################################################

my $traffic_item_2_status = ixiangpf::traffic_l47_config ({
        mode                        => "create",
        name                        => "{Traffic Item_2}",
        circuit_endpoint_type       => "ipv6_application_traffic",
        emulation_src_handle        => "$ixnHLT{'HANDLE,//topology:<3>'} ",
        emulation_dst_handle        => "$ixnHLT{'HANDLE,//topology:<4>'} ",
        objective_type              => "users",
        objective_value             => "100",
        objective_distribution      => "apply_full_objective_to_each_port",
        enable_per_ip_stats         => "1",
        flows                       => "{MAX_Bandwidth_HTTP Microsoft_Update MMS_MM1_WAP_HTTP Modbus MS_SQL_Create MS_SQL_Delete MS_SQL_Drop MS_SQL_Insert MS_SQL_Server MS_SQL_Server_Advanced}",
    });

if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    @status_keys = ixiangpf::status_item_keys();
    my $trafficItem_2_handle = ixiangpf::status_item('traffic_l47_handle');
    $ixnHLT{'HANDLE,//traffic/trafficItem:<0>'} = $trafficItem_2_handle;
	
####################################################
# Start protocols                                  #
####################################################

$_result_ = '';
my @vlist = ();
my @stat_vpl = ();
my $waiting_for_stats = 0;
@status_keys = ();

ixnHLT_logger(q(Starting all protocol(s) ...));
ixiangpf::test_control({action => 'start_all_protocols'});
if (ixiangpf::status_item('status') != 1) {
    ixnHLT_errorHandler('ixiangpf::traffic_control');
}
sleep(10);

################################################################################
# Start traffic                                                                # 
################################################################################

ixnHLT_logger(q(Starting traffic...));
    $_result_ = ixiangpf::traffic_control({
        action => 'run',
        traffic_generator => 'ixnetwork_540',
        type => 'l47'    
    });
    # Check status
    if (ixiangpf::status_item('status') != 1) {
        ixnHLT_errorHandler('traffic_control');
		}

###############################################################################
# Performing drill downs on the TCP Statistics views                          #
###############################################################################

my @drillDownSelectedOptions =(['L47_traffic_item_tcp', 'per_ports_per_initiator_flows', 'initiatorPorts', 'L47_flow_initiator_tcp', 'per_initiator_ports', 'initiatorPorts']);
    
$_result_ = ixiangpf::traffic_stats({
    mode => "L47_traffic_item_tcp",
	drill_down_type => "per_ports_per_initiator_flows",
	drill_down_traffic_item => "$trafficItem_1_handle",
	drill_down_port => "$ixnHLT{'PORT-HANDLE,//vport:<1>'}",
	drill_down_flow => "IRC_Login_Auth_Failure"
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
sleep(30);
$_result_ = ixiangpf::traffic_stats({
    mode => "L47_flow_initiator_tcp",
	drill_down_type => "per_initiator_ports",
	drill_down_traffic_item => "$trafficItem_2_handle",
	drill_down_port => "$ixnHLT{'PORT-HANDLE,//vport:<3>'}",
	drill_down_flow => "Microsoft_Update"
});          
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }            
sleep(30);



#################################################### 
# Stop traffic                                     #
####################################################
sleep(10);
ixnHLT_logger(q(Stopping traffic...));
    $_result_ = ixiangpf::traffic_control({
        action => 'stop',
        traffic_generator => 'ixnetwork_540',
        type => 'l47'    
    });
    # Check status
    if (ixiangpf::status_item('status') != 1) {
        ixnHLT_errorHandler('traffic_control');
		}
		
        
sleep(15);

#################################################### 
# Test END                                         #
####################################################

print "###################\n";
print "Test run is PASSED\n";
print "###################\n";