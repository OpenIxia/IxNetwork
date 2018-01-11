################################################################################
# $Revision: 0.1 $                                                             #
# $Author: Vijay Anantha Murthy $                                              #
#                                                                              #
#    Copyright © by IXIA                                                       #
#    1997 - 2007                                                               #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    03/11/2012 Initial Version                                                #
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

#######################################################
#                                                     #
# Description:                                        #
#    This sample creates an IGMP v3 host,             #
#    two pools of five multicast groups               #
#    and two pools of three multicast sources.        #
#    It adds the multicast groups                     #
#    from the first pool to the host.                 #
#    Then it adds the multicast sources from          #
#    both source pools to the multicast groups        #
#    in the second group pool. These                  #
#    multicast groups are added to the host.          #
#                                                     #
#######################################################
# Source all libraries in the beginning
use warnings;
use strict;
use bignum;
use Carp;

# use lib where the HLPAPI files are located
# This can be moved to .pl files in the JT framework
# It is typically: "/volume/labtools/ixia/<version_number>/lib/library/common/ixia_hl_lib-<version>"
# For Ex:
# use lib "/volume/labtools/ixia/6.30.850.7/lib";
# use lib "/volume/labtools/ixia/6.30.850.7/lib/library/common/ixia_hl_lib-6.30";
use lib "/home/vmurthy/hlpapi/ixos/ixos6.30.850.7/lib";
use lib "/home/vmurthy/hlpapi/ixos/ixos6.30.850.7/lib/library/common/ixia_hl_lib-6.30";
use ixiahlt;
use ixiaixn;

# Declare the Chassis IP address and the Ports that will be used
my $test_name      = "IxNetwork_IGMPv3_create_host_groups_sources";
my $chassisIP      = "10.64.99.12";
my @port_list      = ("1/9", "1/10");
my $ixNetTclServer = "10.64.99.7";
my $user           = "ixiaHlpapiUser";

# Initialize values for HLPAPI scripts
my $_result_               = '';
my @status_keys            = ();
my %status_keys            = ();
my $port_handle            = '';
my $vport_list             = '';
my $vport_protocols_handle = '';
my $status                 = '';
my @_handles_              = ();
my @return_interfaces      = ();
my @return_router          = ();
my @portHandleList         = ();
my $key                    = '';
my $value                  = '';

sub catch_error {
    if (ixiahlt::status_item('status') != 1) {
        print ("n#################################################### n");
        print ("ERROR: n$test_name : ". ixiahlt::status_item('status'));
        print ("n#################################################### n");
        die ("ERROR: n$test_name : Please check values and the port handles!!!");
}}

#######################################################
# Connects to the IxNetwork Tcl Server,               #
# Tcl Server, and the chassis.                        #
# Takes ownership of the ports.                       #
# Notes:                                              #
# IxNetwork Tcl Server must be running on a client PC #
# Tcl Server must be running on a client PC           #
# When using P2NO HLTSET, for loading the             #
# IxTclNetwork package please                         #
# provide .ixnetwork_tcl_server parameter             #
# to ::ixia::connect                                  #
#######################################################
$_result_ = ixiahlt::connect({
    reset                => 1,
    device               => $chassisIP ,
    port_list            => \@port_list,
    ixnetwork_tcl_server => $ixNetTclServer ,
    tcl_server           => $chassisIP ,
    break_locks          => 1,
    username             => $user,
    guard_rail           => "statistics",
});
&catch_error();

@status_keys = ixiahlt::status_item_keys();
$port_handle = ixiahlt::status_item('port_handle');
$vport_list = ixiahlt::status_item('vport_list');
$vport_protocols_handle = ixiahlt::status_item('vport_protocols_handle');
$status = ixiahlt::status_item('status');

# Assign portHandleList with port handles values
foreach my $port (@port_list) {
    $port_handle = ixiahlt::status_item("port_handle.$chassisIP.$port");
    push(@portHandleList, $port_handle);
}

#######################################################
# Configure layer 1 port settings (speed)             #
#######################################################
my $speed           = "auto";
my $autonegotiation = 1;
my $duplex          = "auto";
my $phy_mode        = "copper";

$_result_ = ixiahlt::interface_config({
    mode        => 'config',
    port_handle => \@portHandleList,
    intf_mode   => 'ethernet',
    speed       => $speed,
    duplex      => $duplex,
    phy_mode    => $phy_mode,
});
&catch_error();

#######################################################
#  Configure interfaces and create IGMP sessions      #
#######################################################
$_result_ = ixiahlt::emulation_igmp_config ({
	port_handle                  =>  $portHandleList[0],
	mode                         =>  'create',
	reset                        =>  1,
	msg_interval                 =>  1000,
	igmp_version                 =>  'v3',
	ip_router_alert              =>  1,
	general_query                =>  1,
	group_query                  =>  1,
	unsolicited_report_interval  =>  50,
	suppress_report              =>  0,
	max_response_control         =>  1,
	max_response_time            =>  0,
	filter_mode                  =>  'include',
	count                        =>  '1',
	intf_ip_addr                 =>  '100.41.1.2',
	neighbor_intf_ip_addr        =>  '100.41.1.1',
	intf_prefix_len              =>  24,
	vlan_id_mode                 =>  'increment',
	vlan_id                      =>  10,
	vlan_id_step                 =>  1,
	vlan_user_priority           =>  7,
});
&catch_error();

my $igmp_handle = ixiahlt::status_item('handle');

#######################################################
# Create multicast group pool number 1                #
#######################################################
$_result_ = ixiahlt::emulation_multicast_group_config ({
	mode          => 'create',
	num_groups    => 5,
	ip_addr_start => '226.0.1.1',
	ip_addr_step  => '0.0.0.1',
	ip_prefix_len => 24,
});
&catch_error();

my $igmp_group1_handle = ixiahlt::status_item('handle');

#######################################################
# Create multicast group pool number 2                #
#######################################################
$_result_ = ixiahlt::emulation_multicast_group_config ({
	mode          => 'create',
	num_groups    => 5,
	ip_addr_start => '227.0.1.1',
	ip_addr_step  => '0.0.0.1',
	ip_prefix_len => 24,
});
&catch_error();

my $igmp_group2_handle = ixiahlt::status_item('handle');

#######################################################
# Create multicast source pool number 1               #
#######################################################
$_result_ = ixiahlt::emulation_multicast_source_config ({
	mode          => 'create',
	num_sources   => 5,
	ip_addr_start => '100.41.1.1',
	ip_addr_step  => '0.0.1.0',
	ip_prefix_len => 24,
});
&catch_error();

my $igmp_source1_handle = ixiahlt::status_item('handle');

#######################################################
# Create multicast source pool number 2               #
#######################################################
$_result_ = ixiahlt::emulation_multicast_source_config ({
	mode          => 'create',
	num_sources   => 5,
	ip_addr_start => '100.43.1.1',
	ip_addr_step  => '0.0.1.0',
	ip_prefix_len => 24,
});
&catch_error();

my $igmp_source2_handle = ixiahlt::status_item('handle');

#######################################################
# Create group member for session1 with               #
# group_pool_handle group1                            #
#######################################################
$_result_ = ixiahlt::emulation_igmp_group_config ({
	mode              => 'create',          
	session_handle    => $igmp_handle,        
	group_pool_handle => $igmp_group1_handle,
});
&catch_error();

my @source_pool_handle_list;
push (@source_pool_handle_list, $igmp_source1_handle);
push (@source_pool_handle_list, $igmp_source2_handle);

#######################################################
# Create group member for session1 with               #
# group_pool_handle group2 and source handle          #
# source1 and source2                                 #
#######################################################
$_result_ = ixiahlt::emulation_igmp_group_config ({ 
	mode               => 'create',          
	session_handle     => $igmp_handle,        
	group_pool_handle  => $igmp_group2_handle,
	source_pool_handle => \@source_pool_handle_list,
});
&catch_error();

#######################################################
# Clean up the session:                               #
# Disconnects from  IxNetwork Tcl server,             #
# Tcl server, and Chassis.                            #
# Clears the ownership from a list of ports.          #
#######################################################
$_result_ = ixiahlt::cleanup_session ({
    port_handle => \@portHandleList,
    reset       => 1
});

print ("\n\n$test_name : TEST COMPLETED SUCCESSFULLY!\n");
