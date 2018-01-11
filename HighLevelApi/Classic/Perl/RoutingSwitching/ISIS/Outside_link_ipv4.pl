################################################################################
# Version 1.0    $Revision: #1 $
# $Author: cm $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-27-2013 LBose - Initial Version
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
#    This sample script creates the ISIS outside link with IPv4 Addresses      #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#                                                                              #
################################################################################
# Source all libraries in the beginning
use warnings;
use strict;
use bignum;
use Carp;

# use lib where the HLPAPI files are located
# It is typically: "C:/Program Files/Ixia/hltapi/<version_number>/TclScripts/lib/hltapi/library/common/ixia_hl_lib-<version>"
# For Ex:
# use lib "C:/Program Files/Ixia/hltapi/4.70.0.213/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.10";
use lib "C:/Program Files/Ixia/hltapi/4.70.0.213/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.10";

use ixiahlt;
use ixiaixn;

# Declare the Chassis IP address and the Ports that will be used
my $test_name              = "Outside_link_ipv4";
my $chassis_ip             = "10.206.27.55";
my $tcl_server             = "10.206.27.55";
my $ixnetwork_tcl_server   = "192.168.4.6";
my @port_list              = ("10/1", "10/2");
my @port_names             = ("test_port_1", "test_port_2");
my break_locks             = 1;

################################################################################
# Function to catch the errors and print it on the screen             .        #
################################################################################
sub catch_error {
    if (ixiahlt::status_item('status') != 1) {
        print ("n#################################################### n");
        print ("ERROR: n$test_name : ". ixiahlt::status_item('status'));
        print ("n#################################################### n");
        die ("ERROR: n$test_name : Please check values and the port handles!!!");
    }
}

# Initialize values for HLPAPI scripts
my $_result_               = '';
my $status                 = '';
my @portHandleList         = ();

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
$_result_ = ixiahlt::connect( {
    reset                => 1,
    device               => $chassis_ip,
    port_list            => \@port_list,
    tcl_server           => $tcl_server,
    ixnetwork_tcl_server => $ixnetwork_tcl_server,
});
&catch_error();

# Assign portHandleList with port handles values
my $port_handle     = "";
foreach my $port (@port_list) {
    $port_handle = ixiahlt::status_item("port_handle.$chassis_ip.$port");
    push(@portHandleList, $port_handle);
}

my $port_0 = $portHandleList[0];
my $port_1 = $portHandleList[1];

# Get the vport Info
$_result_ = ixiahlt::vport_info( {
    mode               => 'set_info',
    port_list          => \@portHandleList,
    port_name_list     => \@port_names         
});
&catch_error();

print ("End connecting to chassis ...\n");
################################################################################
# END - Connect to the chassis                                                 #
################################################################################

################################################################################
# START - Interface configuration - L1                                         #
################################################################################
print  ("Start interface configuration L1 ...\n");
$_result_ = ixiahlt::interface_config( {
    port_handle      => \@portHandleList,
    autonegotiation  => 1,
    speed            => 'auto',
});
&catch_error();

################################################################################
#                    Configure the first IS-IS L1L2 router                     #
################################################################################
print ("Configuring ISIS on Port0..\n");
$_result_ = ixiahlt::emulation_isis_config( {
    mode                           => 'create',
    reset                          => 1,
    port_handle                    => $port_0,
    intf_ip_addr                   => '22.1.1.2',
    gateway_ip_addr                => '22.1.1.1',
    intf_ip_prefix_length          => 24,
    mac_address_init               => '0000.0000.0001',
    count                          => 1,
    wide_metrics                   => 1,
    discard_lsp                    => 1,
    attach_bit                     => 1,
    partition_repair               => 1,
    overloaded                     => 1,
    lsp_refresh_interval           => 888,
    lsp_life_time                  => 777,
    max_packet_size                => 1492,
    intf_metric                    => 0,
    routing_level                  => 'L1L2',
});
&catch_error();

my $router_handle1 = ixiahlt::status_item('handle');
################################################################################
#           Add a Grid Network Ranges for the first IS-IS router               #
################################################################################
my  $ip_version_1                              = 4;
my  $grid_start_system_id_1                    = 000000000011;
my  $grid_system_id_step_1                     = 000000000001;
my  $grid_row_1                                = 1;
my  $grid_col_1                                = 1;
my  $grid_stub_per_router_1                    = 10;
my  $grid_router_id_1                          = '192.168.1.1';
my  $grid_router_id_step_1                     = '0.1.0.0';
my  $grid_ip_start_1                           = '192.20.20.1';
my  $grid_ip_pfx_len_1                         = 24;
my  $grid_ip_step_1                            = '0.0.1.0';
my  @grid_connect_1                            = (1, 1);
my  $grid_link_type_1                          = 'ptop';
my  $grid_router_metric_1                      = 10;
my  $grid_router_up_down_bit_1                 = 0;
my  $grid_router_origin_1                      = 'external';
my  $grid_user_wide_metric_1                   = 0;
my  @grid_ol_ip_and_prefix_1                   = ("10.0.0.1/24,10.0.0.2/24", "11.0.0.1/24,11.0.0.2/24");
my  @grid_ol_connection_row_1                  = (1, 1);
my  @grid_ol_connection_col_1                  = (1, 1);
my  @grid_ol_linked_rid_1                      = (1, 2);
my  @grid_ol_metric_1                          = (1, 2);
my  @grid_ol_admin_group_1                     = (1, 2);
my  @grid_ol_max_bw_1                          = (10, 11);
my  @grid_ol_max_resv_bw_1                     = (12, 13);
my  @grid_ol_unresv_bw_priority0_1             = (14, 15);
my  @grid_ol_unresv_bw_priority1_1             = (16, 17);
my  @grid_ol_unresv_bw_priority2_1             = (18, 19);
my  @grid_ol_unresv_bw_priority3_1             = (20, 21);
my  @grid_ol_unresv_bw_priority4_1             = (22, 23);
my  @grid_ol_unresv_bw_priority5_1             = (24, 25);
my  @grid_ol_unresv_bw_priority6_1             = (26, 27);
my  @grid_ol_unresv_bw_priority7_1             = (228, 29);
my  $isis_router_networkRange_handle_list_1   =    "";

$_result_ = ixiahlt::emulation_isis_topology_route_config ( {
    mode                           => 'create',
    handle                         => $router_handle1,
    type                           => 'grid',
    ip_version                     => $ip_version_1 ,
    grid_outside_link              => 1,
    grid_ol_connection_row         => \@grid_ol_connection_row_1 ,
    grid_ol_connection_col         => \@grid_ol_connection_col_1 ,
    grid_ol_linked_rid             => \@grid_ol_linked_rid_1 ,
    grid_ol_admin_group            => \@grid_ol_admin_group_1 ,
    grid_ol_ip_and_prefix          => \@grid_ol_ip_and_prefix_1 ,
    grid_ol_metric                 => \@grid_ol_metric_1 ,
    grid_ol_max_bw                 => \@grid_ol_max_bw_1 ,
    grid_ol_max_resv_bw            => \@grid_ol_max_resv_bw_1 ,
    grid_ol_unresv_bw_priority0    => \@grid_ol_unresv_bw_priority0_1 ,
    grid_ol_unresv_bw_priority1    => \@grid_ol_unresv_bw_priority1_1 ,
    grid_ol_unresv_bw_priority2    => \@grid_ol_unresv_bw_priority2_1 ,
    grid_ol_unresv_bw_priority3    => \@grid_ol_unresv_bw_priority3_1 ,
    grid_ol_unresv_bw_priority4    => \@grid_ol_unresv_bw_priority4_1 ,
    grid_ol_unresv_bw_priority5    => \@grid_ol_unresv_bw_priority5_1 ,
    grid_ol_unresv_bw_priority6    => \@grid_ol_unresv_bw_priority6_1 ,
    grid_ol_unresv_bw_priority7    => \@grid_ol_unresv_bw_priority7_1 ,
    grid_start_system_id           => $grid_start_system_id_1 ,
    grid_system_id_step            => $grid_system_id_step_1 ,
    grid_row                       => $grid_row_1 ,
    grid_col                       => $grid_col_1 ,
    grid_stub_per_router           => $grid_stub_per_router_1 ,
    grid_router_id                 => $grid_router_id_1 ,
    grid_router_id_step            => $grid_router_id_step_1 ,
    grid_ip_start                  => $grid_ip_start_1 ,
    grid_ip_pfx_len                => $grid_ip_pfx_len_1 ,
    grid_ip_step                   => $grid_ip_step_1 ,
    grid_connect                   => \@grid_connect_1 ,
    grid_link_type                 => $grid_link_type_1 ,
    grid_router_metric             => $grid_router_metric_1 ,
    grid_router_up_down_bit        => $grid_router_up_down_bit_1 ,
    grid_router_origin             => $grid_router_origin_1 ,
    grid_user_wide_metric          => $grid_user_wide_metric_1 ,              
});
&catch_error();

################################################################################
#                   Configure the second IS-IS L1L2 router                     #
################################################################################
print ("Configuring ISIS on Port1..");

$_result_ = ixiahlt::emulation_isis_config ( {
    mode                           => 'create',
    reset                          => 1,
    port_handle                    => $port_1,
    intf_ip_addr                   => '22.1.1.1',
    gateway_ip_addr                => '22.1.1.2',
    intf_ip_prefix_length          => 24,
    mac_address_init               => '0000.0000.0002',
    count                          => 1,
    wide_metrics                   => 1,
    discard_lsp                    => 1,
    attach_bit                     => 1,
    partition_repair               => 1,
    overloaded                     => 1,
    lsp_refresh_interval           => 888,
    lsp_life_time                  => 777,
    max_packet_size                => 1492,
    intf_metric                    => 0,
    routing_level                  => 'L1L2',
});
&catch_error();

my $router_handle2 = ixiahlt::status_item('handle');
################################################################################
#           Add a Grid Network Ranges for the second IS-IS router              #
################################################################################
my  $ip_version_2                     = 4;
my  $grid_start_system_id_2           = '0000000011';
my  $grid_system_id_step_2            = '000000000001';
my  $grid_row_2                       = 2;
my  $grid_col_2                       = 2;
my  $grid_stub_per_router_2           = 10;
my  $grid_router_id_2                 = '193.168.1.1';
my  $grid_router_id_step_2            = '0.1.0.0';
my  $grid_ip_start_2                  = '193.20.20.1';
my  $grid_ip_pfx_len_2                = 24;
my  $grid_ip_step_2                   = '0.0.1.0';
my  @grid_connect_2                   = (2, 2);
my  $grid_link_type_2                 = 'ptop';
my  $grid_router_metric_2             = 10;
my  $grid_router_up_down_bit_2        = 0;
my  $grid_router_origin_2             = 'external';
my  $grid_user_wide_metric_2          = 0;
my  @grid_ol_ip_and_prefix_2          = ("12.0.0.1/24,12.0.0.2/24", "13.0.0.1/24,13.0.0.2/24");
my  @grid_ol_connection_row_2        = (1, 1);
my  @grid_ol_connection_col_2         = (1, 1);
my  @grid_ol_linked_rid_2             = (255, 256);
my  @grid_ol_metric_2                 = (355, 356);
my  @grid_ol_admin_group_2            = (455, 456);
my  @grid_ol_max_bw_2                 = (555, 556);
my  @grid_ol_max_resv_bw_2            = (655, 656);
my  @grid_ol_unresv_bw_priority0_2    = (755, 756);
my  @grid_ol_unresv_bw_priority1_2    = (855, 856);
my  @grid_ol_unresv_bw_priority2_2    = (955, 956);
my  @grid_ol_unresv_bw_priority3_2    = (1055, 1056);
my  @grid_ol_unresv_bw_priority4_2    = (1165, 1156);
my  @grid_ol_unresv_bw_priority5_2    = (1175, 1176);
my  @grid_ol_unresv_bw_priority6_2    = (1185, 1186);
my  @grid_ol_unresv_bw_priority7_2    = (1195, 1196);
my  $isis_router_networkRange_handle_list =  "";

$_result_ = ixiahlt::emulation_isis_topology_route_config ( {
    mode                           => 'create',
    handle                         => $router_handle2,
    type                           => 'grid',
    ip_version                     => $ip_version_2,
    grid_outside_link              => 1,
    grid_ol_connection_row         => \@grid_ol_connection_row_2,
    grid_ol_connection_col         => \@grid_ol_connection_col_2,
    grid_ol_linked_rid             => \@grid_ol_linked_rid_2,
    grid_ol_admin_group            => \@grid_ol_admin_group_2,
    grid_ol_ip_and_prefix          => \@grid_ol_ip_and_prefix_2,
    grid_ol_metric                 => \@grid_ol_metric_2,
    grid_ol_max_bw                 => \@grid_ol_max_bw_2,
    grid_ol_max_resv_bw            => \@grid_ol_max_resv_bw_2,
    grid_ol_unresv_bw_priority0    => \@grid_ol_unresv_bw_priority0_2,
    grid_ol_unresv_bw_priority1    => \@grid_ol_unresv_bw_priority1_2,
    grid_ol_unresv_bw_priority2    => \@grid_ol_unresv_bw_priority2_2,
    grid_ol_unresv_bw_priority3    => \@grid_ol_unresv_bw_priority3_2,
    grid_ol_unresv_bw_priority4    => \@grid_ol_unresv_bw_priority4_2,
    grid_ol_unresv_bw_priority5    => \@grid_ol_unresv_bw_priority5_2,
    grid_ol_unresv_bw_priority6    => \@grid_ol_unresv_bw_priority6_2,
    grid_ol_unresv_bw_priority7    => \@grid_ol_unresv_bw_priority7_2,
    grid_start_system_id           => $grid_start_system_id_2,
    grid_system_id_step            => $grid_system_id_step_2,
    grid_row                       => $grid_row_2,
    grid_col                       => $grid_col_2,
    grid_stub_per_router           => $grid_stub_per_router_2,
    grid_router_id                 => $grid_router_id_2,
    grid_router_id_step            => $grid_router_id_step_2,
    grid_ip_start                  => $grid_ip_start_2,
    grid_ip_pfx_len                => $grid_ip_pfx_len_2,
    grid_ip_step                   => $grid_ip_step_2,
    grid_connect                   => \@grid_connect_2,
    grid_link_type                 => $grid_link_type_2,
    grid_router_metric             => $grid_router_metric_2,
    grid_router_up_down_bit        => $grid_router_up_down_bit_2,
    grid_router_origin             => $grid_router_origin_2,
    grid_user_wide_metric          => $grid_user_wide_metric_2              
});
&catch_error();

################################################################################
#                           Start the IS-IS protocol emulation                 #
################################################################################
$_result_ = ixiahlt::emulation_isis_control ( {
    port_handle              => $port_0,
    mode                     => 'start',                                  
});
&catch_error();     

$_result_ = ixiahlt::emulation_isis_control ( {
    port_handle           => $port_1,
    mode                  => 'start',
});
&catch_error();    
########################>>>>>>>>


sleep (1);
print ("\n\n$test_name : TEST COMPLETED SUCCESSFULLY!\n");
