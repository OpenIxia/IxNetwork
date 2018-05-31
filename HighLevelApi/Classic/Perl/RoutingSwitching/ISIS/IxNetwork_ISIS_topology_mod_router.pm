################################################################################
# $Revision: 0.1 $                                                             #
# $Author:   Vijay Anantha Murthy $                                            #
#                                                                              #
#                                                                              #
#    Copyright © by IXIA                                                       #
#    1997 - 2012                                                               #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    2-11-2012 Initial version                                                 #
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
#    This sample creates an ISIS router and           #
#    configures a route range for it.                 #
#    Then modifies the route range.                   #
#                                                     #
#######################################################
# Source all libraries in the beginning
use warnings;
use strict;
use bignum;
use Carp;

# use lib where the HLPAPI files are located
# This can be moved to .pl files in the JT framework
# It is typically:
# "/volume/labtools/ixia/<version_number>/lib/library/common/ixia_hl_lib-<version>"
# For Ex:
# use lib "/volume/labtools/ixia/6.30.850.7/lib";
# use lib "/volume/labtools/ixia/6.30.850.7/lib/library/common/ixia_hl_lib-6.30";
use lib "/home/vmurthy/hlpapi/ixos/ixos6.30.850.7/lib";
use lib "/home/vmurthy/hlpapi/ixos/ixos6.30.850.7/lib/library/common/ixia_hl_lib-6.30";
use ixiahlt;
use ixiaixn;

# Declare the Chassis IP address and the Ports that will be used
my $test_name      = "IxNetwork_ISIS_topology_mod_router";
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
#  Configure ISIS L1L2 neighbors interface            #
#######################################################
$_result_ = ixiahlt::emulation_isis_config ({
	mode                    => 'create',
	reset                   => 1,
	port_handle             => $portHandleList[0],
	intf_ip_addr            => '22.1.1.1',
	gateway_ip_addr         => '22.1.1.2',
	intf_ip_prefix_length   => 24,
	mac_address_init        => '0000.0000.0001',
	count                   => 1,
	wide_metrics            => 0,
	discard_lsp             => 1,
	attach_bit              => 0,
	partition_repair        => 1,
	overloaded              => 0,
	lsp_refresh_interval    => 10,
	lsp_life_time           => 777,
	max_packet_size         => 1492,
	intf_metric             => 0,
	routing_level           => 'L1L2',
	te_enable               => 0,
	te_router_id            => '198.0.0.1',
	te_max_bw               => 10,
	te_max_resv_bw          => 20,
	te_unresv_bw_priority0  => 0,
	te_unresv_bw_priority1  => 10,
	te_unresv_bw_priority2  => 20,
	te_unresv_bw_priority3  => 30,
	te_unresv_bw_priority4  => 40,
	te_unresv_bw_priority5  => 50,
	te_unresv_bw_priority6  => 60,
	te_unresv_bw_priority7  => 70,
	te_metric               => 10,
});
&catch_error();

#Get the list of ISIS router handle form the keye list returned
my $isis_router_handle = ixiahlt::status_item('handle');

$_result_ = ixiahlt::emulation_isis_config ({
        mode                    => 'create',
        reset                   => 1,
        port_handle             => $portHandleList[1],
        intf_ip_addr            => '22.1.1.2',
        gateway_ip_addr         => '22.1.1.1',
        intf_ip_prefix_length   => 24,
});
&catch_error();

#Get the list of ISIS router handle form the keye list returned
my $isis_router_handle1 = ixiahlt::status_item('handle');

#######################################################
#  Configure 2 IPv4 route range on each ISIS router   #
#######################################################
$_result_ = ixiahlt::emulation_isis_topology_route_config ({
	mode                        => 'create',
	handle                      => $isis_router_handle,
	type                        => 'router',
	ip_version                  => '4_6',
	router_system_id            => '112233445566',
	router_id                   => '44.0.0.1',
	router_area_id               => '000001 000002 112233',
	link_ip_addr                => '198.0.0.1',
	link_ip_prefix_length       => 24,
	link_enable                 => 1,
	link_ipv6_addr              => '4000::1',
	link_ipv6_prefix_length     => 64,
	link_narrow_metric          => 10,
	link_wide_metric            => 999,
	link_te                     => 1,
	link_te_metric              => 77,
	link_te_max_bw              => 1000,
	link_te_max_resv_bw         => 9999,
	link_te_unresv_bw_priority0 => 0,
	link_te_unresv_bw_priority1 => 1,
	link_te_unresv_bw_priority2 => 2,
	link_te_unresv_bw_priority3 => 3,
	link_te_unresv_bw_priority4 => 4,
	link_te_unresv_bw_priority5 => 5,
	link_te_unresv_bw_priority6 => 6,
	link_te_unresv_bw_priority7 => 7,
	link_te_admin_group         => 100,
});
&catch_error();

my $elem_handle = ixiahlt::status_item('elem_handle');

#######################################################
#  Modify the topology element                        #
#######################################################
$_result_ = ixiahlt::emulation_isis_topology_route_config ({
	mode                        => 'modify',
	handle                      => $isis_router_handle,
	elem_handle                 => $elem_handle,
	ip_version                  => '4_6',
	router_system_id            => '010203040506',
	router_id                   => '44.0.0.9',
	router_area_id              => '000001.000002.999999',
	link_ip_addr                => '198.0.0.9',
	link_ip_prefix_length       => 24,
	link_enable                 => 1,
	link_ipv6_addr              => '4000::9',
	link_ipv6_prefix_length     => 64,
	link_narrow_metric          => 10,
	link_wide_metric            => 999,
	link_te                     => 1,
	link_te_metric              => 77,
	link_te_max_bw              => 1000,
	link_te_max_resv_bw         => 9999,
	link_te_unresv_bw_priority0 => 07,
	link_te_unresv_bw_priority1 => 17,
	link_te_unresv_bw_priority2 => 27,
	link_te_unresv_bw_priority3 => 37,
	link_te_unresv_bw_priority4 => 47,
	link_te_unresv_bw_priority5 => 57,
	link_te_unresv_bw_priority6 => 67,
	link_te_unresv_bw_priority7 => 77,
	link_te_admin_group         => 999,
});
&catch_error();

$elem_handle = ixiahlt::status_item('elem_handle');

#######################################################
# START ISIS                                          #
#######################################################
$_result_ = ixiahlt::emulation_isis_control ({
    handle => $isis_router_handle,
    mode   => 'start',
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
