################################################################################
# Version 1.0    $Revision: #1 $
# $Author: cm $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-26-2013 LBose - Initial Version
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
#    This sample script creates the IGMP V1/V2/V3 queriers using two ports     #
#                                                                              #
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
my $test_name              = "IGMP_querier_advanced";
my $chassis_ip             = "10.206.27.55";
my $tcl_server             = "10.206.27.55";
my $ixnetwork_tcl_server   = "192.168.4.6";
my @port_list              = ("10/1", "10/2");

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
my @query_handle_List       = ();
my @host_handle_List       = ();

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
$_result_ = ixiahlt::connect( {
    reset                => 1,
    device               => $chassis_ip,
    port_list            => \@port_list,
    ixnetwork_tcl_server => $ixnetwork_tcl_server ,
    tcl_server           => $tcl_server ,
});
&catch_error();

# Assign portHandleList with port handles values
my $port_handle     = "";
foreach my $port (@port_list) {
    $port_handle = ixiahlt::status_item("port_handle.$chassis_ip.$port");
    push(@portHandleList, $port_handle);
}

my $port_1 = $portHandleList[0];
my $port_2 = $portHandleList[1];

#################################################################################
#  Configure interfaces and create IGMP sessions                                # 
#################################################################################
print ("Configure IGMP v2 hosts\n");

my  $ip_router_alert2         = 1;
my  $host2                    = "90.34.1.1";
my  $query2                   = "90.34.1.2";
my  $vlan_id2                 = 10;
my  $vlan_id_step2            = 1;
my  $vlan_user_priority2      = 4;

$_result_ = ixiahlt::emulation_igmp_config ( {
    port_handle           => $port_1,
    reset                 => 1,
    mode                  => 'create',
    msg_interval          => 167,
    igmp_version          => 'v2',
    ip_router_alert       => $ip_router_alert2,
    general_query         => 0,
    group_query           => 0,
    filter_mode           => 'exclude',
    count                 => 1,
    intf_ip_addr          => $host2,
    neighbor_intf_ip_addr => $query2,
    intf_prefix_len       => 24,
    vlan_id_mode          => 'increment',
    vlan_id               => $vlan_id2,
    vlan_id_step          => $vlan_id_step2,
    vlan_user_priority    => $vlan_user_priority2,
});
&catch_error();

my $host_handle_v2 = ixiahlt::status_item('handle');
push(@host_handle_List, $host_handle_v2);

print ("Create v2 IGMP group\n");

my  $session_handle2      = "90.34.1.1";
my  @mgroup_params2       = ("226.0.2.1/0.0.0.1/5",  "226.0.2.6/0.0.0.2/4");
my  @msource_params2      = ("100.0.2.2/0.0.0.2/2,110.0.2.2/0.0.0.1/3",  "120.0.2.2/0.0.0.1/5,130.0.2.2/0.0.0.1/5,140.0.2.2/0.0.0.1/5");

$_result_ = ixiahlt::emulation_igmp_group_config ( {
    mode                 =>  'create',
    session_handle       => $session_handle2,
    group_pool_handle    => \@mgroup_params2,
    source_pool_handle   => \@msource_params2,
});
&catch_error();

my $group1_handle = ixiahlt::status_item('group_pool_handle');

#################################################################################
#                        IGMP v3 hosts                                          #
#################################################################################
print ("Configure IGMP v3 hosts\n");

my  $ip_router_alert3         = 1;
my  $host3                    = "100.0.1.2";
my  $query3                   = "100.0.1.1";
my  $vlan_id3                 = 10;
my  $vlan_id_step3            = 1;
my  $vlan_user_priority3      = 4;

$_result_ = ixiahlt::emulation_igmp_config ( {
    port_handle           => $port_1,
    mode                  => 'create',
    msg_interval          => 167,
    igmp_version          => 'v3',
    ip_router_alert       => $ip_router_alert3,
    general_query         => 0,
    group_query           => 0,
    filter_mode           => 'exclude',
    count                 => 1,
    intf_ip_addr          => $host3,
    neighbor_intf_ip_addr => $query3,
    intf_prefix_len       => 20,
    vlan_id_mode          => 'increment',
    vlan_id               => $vlan_id3,
    vlan_id_step          => $vlan_id_step3,
    vlan_user_priority    => $vlan_user_priority3,
});
&catch_error();

my $host_handle_v3 = ixiahlt::status_item('handle');
push(@host_handle_List, $host_handle_v3);

print ("Create IGMP v3 group\n");
my  $session_handle3  = "100.0.1.2";
my  @mgroup_params3   = ("226.0.1.1/0.0.0.1/5",  "226.0.1.6/0.0.0.2/4");
my  @msource_params3  = ("100.0.1.2/0.0.0.2/2,110.0.1.2/0.0.0.1/3",  "120.0.1.2/0.0.0.1/5,130.0.1.2/0.0.0.1/5,140.0.1.2/0.0.0.1/5");

$_result_ = ixiahlt::emulation_igmp_group_config ( {
    mode                 => 'create',
    session_handle       => $session_handle3,
    group_pool_handle    => \@mgroup_params3,
    source_pool_handle   => \@msource_params3,
});
&catch_error();

my $group2_handle = ixiahlt::status_item('group_pool_handle');

#################################################################################
#                   IGMP v1 hosts                                               #
#################################################################################
print ("Configure IGMP v1 hosts\n");
my  $ip_router_alert1         = 1;
my  $host1                    = "40.0.1.2";
my  $query1                   = "40.0.1.1";
my  $vlan_id1                 = 20;
my  $vlan_id_step1            = 1;
my  $vlan_user_priority1      = 5;

$_result_ = ixiahlt::emulation_igmp_config ( {
    port_handle           => $port_1,
    mode                  => 'create',
    msg_interval          => 167,
    igmp_version          => 'v1',
    ip_router_alert       => $ip_router_alert1,
    general_query         => 0,
    group_query           => 0,
    filter_mode           => 'exclude',
    count                 => 1,
    intf_ip_addr          => $host1,
    neighbor_intf_ip_addr => $query1,
    intf_prefix_len       => 20,
    vlan_id_mode          => 'increment',
    vlan_id               => $vlan_id1,
    vlan_id_step          => $vlan_id_step1,
    vlan_user_priority    => $vlan_user_priority1,
});
&catch_error();

my $host_handle_v1 = ixiahlt::status_item('handle');
push(@host_handle_List, $host_handle_v1);

print ("Configure IGMP v1 group\n");

my  $session_handle1  = "40.0.1.2";

my  @mgroup_params1   = ("226.0.3.1/0.0.0.1/5", "226.0.3.6/0.0.0.2/4");
my  @msource_params1  = ("100.0.3.2/0.0.0.2/2,110.0.3.2/0.0.0.1/3", "120.0.3.2/0.0.0.1/5,130.0.3.2/0.0.0.1/5,140.0.3.2/0.0.0.1/5");

$_result_ = ixiahlt::emulation_igmp_group_config ( {
    mode                 => 'create',
    session_handle       => $session_handle1,
    group_pool_handle    => \@mgroup_params1,
    source_pool_handle   => \@msource_params1,
});
&catch_error();

my $group3_handle = ixiahlt::status_item('group_pool_handle');

##############################################################################
#                       Create IGMP queriers                                 #
##############################################################################
print ("Configure IGMP v2 querier...\n");
my  $ip_router_alert4         = 1;
my  $host4                    = "90.34.1.1";
my  $query4                   = "90.34.1.2";
my  $vlan_id4                 = 10;
my  $vlan_id_step4            = 1;
my  $vlan_user_priority4      = 4;

$_result_ = ixiahlt::emulation_igmp_querier_config ( {
    port_handle                            => $port_2,
    mode                                   => 'create',
    reset                                  => 1,
    specific_query_response_interval       => 300,
    robustness_variable                    => 2,
    support_older_version_host             => 1,
    support_older_version_querier          => 1,
    support_election                       => 1,
    specific_query_transmission_count      => 2,
    startup_query_count                    => 2,
    igmp_version                           => 'v2',
    discard_learned_info                   => 0,
    general_query_response_interval        => 600,
    msg_count_per_interval                 => 0,
    msg_interval                           => 0,
    count                                  => 1,
    intf_ip_addr                           => $query4,
    neighbor_intf_ip_addr                  => $host4,
    intf_prefix_len                        => 20,
    vlan_id_mode                           => 'increment',
    vlan_id                                => $vlan_id4,
    vlan_id_step                           => 0,
    vlan_user_priority                     => $vlan_user_priority4,
    ip_router_alert                        => 1,
    mac_address_init                       => '0002.c1cc.ddd0',
    mac_address_step                       => '0000.0000.0001',
    override_existence_check               => 1,
    override_tracking                      => 1,
    vci                                    => 3400,
    vci_step                               => 535,
    vpi                                    => 100,
    vpi_step                               => 90,
    query_interval                         => 450,
});
&catch_error();

my $query_handle_v2 = ixiahlt::status_item('handle');
push(@query_handle_List, $query_handle_v2);

##############################################################################
#        IGMPv3 queriers                                                     #
##############################################################################

print ("Configure IGMP v3 querier...\n");
my  $ip_router_alert5         = 1;
my  $host5                    = "100.0.1.2";
my  $query5                  = "100.0.1.1";
my  $vlan_id5                 = 10;
my  $vlan_id_step5            = 1;
my  $vlan_user_priority5      = 4;

$_result_ = ixiahlt::emulation_igmp_querier_config ( {
    port_handle                        => $port_2,
    mode                               => 'create',
    specific_query_response_interval   => 300,
    robustness_variable                => 4,
    support_older_version_host         => 1,
    support_older_version_querier      => 1,
    support_election                   => 1,
    specific_query_transmission_count  => 4,
    startup_query_count                => 1,
    igmp_version                       => 'v3',
    discard_learned_info               => 0,
    general_query_response_interval    => 4200,
    msg_count_per_interval             => 9,
    msg_interval                       => 4,
    count                              => 1,
    intf_ip_addr                       => $query5,
    neighbor_intf_ip_addr              => $host5,
    intf_prefix_len                    => 24,
    vlan_id_mode                       => 'increment',
    vlan_id                            => $vlan_id5,
    vlan_id_step                       => $vlan_id_step5,
    vlan_user_priority                 => $vlan_user_priority5,
    ip_router_alert                    => 1,
    mac_address_init                   => "00ab.cccc.ddd0",
    mac_address_step                   => "0000.0000.0001",
    override_existence_check           => 1,
    override_tracking                  => 1,
    vci                                => 3400,
    vci_step                           => 535,
    vpi                                => 100,
    vpi_step                           => 90,
    query_interval                     => 30,
});
&catch_error();

my $query_handle_v3 = ixiahlt::status_item('handle');
push(@query_handle_List, $query_handle_v3);

##############################################################################
#   IGMPv1 queriers                                                          #
##############################################################################
print ("Configure IGMP v1 querier...\n");
my  $ip_router_alert6         = 1;
my  $host6                    = "40.0.1.2";
my  $query6                   = "40.0.1.1";
my  $vlan_id6                 = 20;
my  $vlan_id_step6            = 1;
my  $vlan_user_priority6      = 5;

$_result_ = ixiahlt::emulation_igmp_querier_config ( {
    port_handle                        => $port_2,
    mode                               => 'create',
    specific_query_response_interval   => 100,
    robustness_variable                => 1,
    support_older_version_host         => 1,
    support_older_version_querier      => 1,
    support_election                   => 1,
    specific_query_transmission_count  => 4,
    startup_query_count                => 1,
    igmp_version                       => 'v1',
    discard_learned_info               => 0,
    general_query_response_interval    => 4200,
    msg_count_per_interval             => 7,
    msg_interval                       => 3,
    count                              => 1,
    intf_ip_addr                       => $query6,
    neighbor_intf_ip_addr              => $host6,
    intf_prefix_len                    => 24,
    vlan_id_mode                       => 'increment',
    vlan_id                            => $vlan_id6,
    vlan_id_step                       => $vlan_id_step6,
    vlan_user_priority                 => $vlan_user_priority6,
    ip_router_alert                    => 1,
    mac_address_init                   => '00ab.0ccc.ddd0',
    mac_address_step                   => '0000.0000.0001',
    override_existence_check           => 1,
    override_tracking                  => 1,
    vci                                => 3400,
    vci_step                           => 335,
    vpi                                => 200,
    vpi_step                           => 40,
    query_interval                     => 20,
});
&catch_error();

my $query_handle_v1 = ixiahlt::status_item('handle');
push(@query_handle_List, $query_handle_v1);

##############################################################################
#                             Start IGMP                                     #
##############################################################################
print ("Start protocol...\n");
$_result_ = ixiahlt::emulation_igmp_control ( {
    mode       => 'start',
    handle     => \@query_handle_List,
});
&catch_error();



sleep (10);

##############################################################################
#                           Restart IGMP queriers                            #
##############################################################################
print ("Restart IGMP querier\n");
$_result_ = ixiahlt::emulation_igmp_control ( {
    mode   => 'restart',
    handle => \@query_handle_List,
});
&catch_error();

##############################################################################
#                           Join/Leave IGMP host                             #
##############################################################################
print ("Leave IGMP host\n");
$_result_ = ixiahlt::emulation_igmp_control ( {
    mode   => 'leave',
    handle => \@host_handle_List,
});
&catch_error();

sleep (5);
print ("Join IGMP host\n");

$_result_ = ixiahlt::emulation_igmp_control ( {
    mode       => 'join',
    handle     => \@host_handle_List,
});
&catch_error();

##############################################################################
#                           Stop IGMP                                        #
##############################################################################

sleep (5);
print ("Stop IGMP\n");

$_result_ = ixiahlt::emulation_igmp_control ( {
    mode       => 'stop',
    handle     => \@query_handle_List,
});
&catch_error();

$_result_ = ixiahlt::emulation_igmp_control ( {
    mode       => 'stop',
    handle     => \@host_handle_List,
});
&catch_error();

print ("\n\n$test_name : TEST COMPLETED SUCCESSFULLY!\n");


