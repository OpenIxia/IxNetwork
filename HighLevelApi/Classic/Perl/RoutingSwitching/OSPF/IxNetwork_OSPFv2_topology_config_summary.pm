#################################################################################
# $Revision: 0.1 $                                                              #
# $Author:   Vijay Anantha Murthy $                                             #
#                                                                               #
#                                                                               #
#    Copyright © by IXIA                                                        #
#    1997 - 2012                                                                #
#    All Rights Reserved.                                                       #
#                                                                               #
#    Revision Log:                                                              #
#                                                                               #
#    10-11-2012 Initial Version 0.1                                             #
#                                                                               #
#                                                                               #
#                                                                               #
#################################################################################

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
#    This sample creates two OSPFv2 routers           #
#    on two different ports. Then on                  #
#    the first router it configures a pool of         #
#    summary routes.                                  #
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
my $test_name      = "IxNetwork_OSPFv2_topology_config_summary";
my $chassisIP      = "10.64.99.12";
my @port_list      = ("1/9", "1/10");
my $ixNetTclServer = "10.64.99.7";
my $user           = "ixiaHlpapiUser";
my $speed           = "auto";
my $autonegotiation = 1;           
my $duplex          = "auto";         
my $phy_mode        = "copper";

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
# Configure interface in the test                     #
# IPv4                                                #
#######################################################
$_result_ = ixiahlt::interface_config ({
    mode        => 'config',
    port_handle => $portHandleList[0],
    intf_mode   => 'ethernet',
    speed       => $speed,
    duplex      => $duplex,
    phy_mode    => $phy_mode,
});
&catch_error();

#######################################################
#  Configure n OSPFv2 neighbors                       #
#######################################################
$_result_ = ixiahlt::emulation_ospf_config ({
	port_handle                => $portHandleList[0],         
	reset                      => 1,                 
	session_type               => 'ospfv2',         
	mode                       => 'create',           
	count                      => 1,               
	mac_address_init           => '1000.0000.0001',   
	intf_ip_addr               => '100.1.1.1',        
	intf_ip_addr_step          => '0.0.1.0',          
	router_id                  => '1.1.1.1',          
	router_id_step             => '0.0.1.0',          
	neighbor_intf_ip_addr      => '100.1.1.2',        
	neighbor_intf_ip_addr_step => '0.0.1.0',          
	vlan_id_step               => 5,                
	area_id                    => '0.0.0.1',          
	area_id_step               => '0.0.0.1',          
	area_type                  => 'external-capable', 
	authentication_mode        => 'null',             
	dead_interval              => 222,              
	hello_interval             => 333,              
	interface_cost             => 55,               
	lsa_discard_mode           => 1,                
	mtu                        => 670,              
	network_type               => 'ptop',             
	demand_circuit             => 1,
});
&catch_error();

@status_keys = ixiahlt::status_item_keys();
my $session_handle = ixiahlt::status_item('handle');

#######################################################
#  Configure a single router behind a session router  #
#######################################################
$_result_ = ixiahlt::emulation_ospf_topology_route_config ({
	mode                      => 'create',                  
	handle                    => $session_handle,        
	type                      => 'summary_routes',          
	summary_number_of_prefix  => 10,           
	summary_prefix_start      => '55.0.0.1',     
	summary_prefix_length     => 24,           
	summary_prefix_metric     => 5,
});
&catch_error();

#######################################################
#  Configure OSPF on second port                      #
#######################################################
$_result_ = ixiahlt::emulation_ospf_config ({
	port_handle                => $portHandleList[1],        
	reset                      => 1,                
	session_type               => 'ospfv2',           
	mode                       => 'create',           
	count                      => 1,               
	mac_address_init           => '1000.0000.0002',   
	intf_ip_addr               => '100.1.1.2',        
	intf_ip_addr_step          => '0.0.1.0',          
	router_id                  => '7.7.7.7',          
	router_id_step             => '0.0.1.0',          
	neighbor_intf_ip_addr      => '100.1.1.1',        
	neighbor_intf_ip_addr_step => '0.0.1.0',          
	vlan_id_step               => '5',                
	area_id                    => '0.0.0.1',          
	area_id_step               => '0.0.0.1',          
	area_type                  => 'external-capable', 
	authentication_mode        => 'null',             
	dead_interval              => 222,              
	hello_interval             => 333,              
	interface_cost             => 55,               
	lsa_discard_mode           => 0,                
	mtu                        => 670,               
	network_type               => 'ptop',              
	demand_circuit             => 1,
});
&catch_error();
sleep(10);

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