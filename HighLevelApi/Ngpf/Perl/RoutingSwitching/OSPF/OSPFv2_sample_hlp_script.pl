################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    20/01/2015 - Abhijit Dhar - created sample                                #
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
# This script intends to demonstrate how to use NGPF OSPFv2 API.               #
#                                                                              #
# About Topology:                                                              #
# This topology has two b2b connected device group, with each device group     #
# having a 1) OSPFv2 router and 2) a network group range. The network group    #
# range has a device group behind to simulate the applib traffic.              #
#                                                                              #
# Script Flow:                                                                 #
#  1. Configure the topology as described above.                               #
#  2. Start the OSPFv2 protocol.                                               #
#  3. Retrieve protocol learned info.                                          #
#  4. Retrieve protocol statistics.                                            #
#  5. Disable OSPFv2 network group range                                       #
#  6. Retrieve protocol learned info again and notice the difference with      #
#     previously retrieved learned info.                                       #
#  7. Enable the network group range                                           #
#  8. Retrieve protocol learned info again.                                    #
#  9. Configure L2-L3 traffic.                                                 #
# 10. Configure application traffic.                                           #
# 11. Start the L2-L3 traffic.                                                 #
# 12. Start the application traffic.                                           #
# 13. Retrieve Application traffic stats.                                      #
# 14. Retrieve L2-L3 traffic stats.                                            #
# 15. Stop L2-L3 traffic.                                                      #
# 16. Stop Application traffic.                                                #
# 17. Stop all protocols.                                                      #
#                                                                              #
# Ixia Software :                                                              #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################

################################################################################
# Utils                                                                        #    
################################################################################
# Running from Linux:

	# use lib ".";
	# use lib "..";
	# use lib "../..";
	# use lib "/root/hltapi/library/common/ixia_hl_lib-7.30";
	# use lib "/root/hltapi/library/common/ixiangpf/perl";
	# use lib "/root/ixos/lib/PerlApi";
	# use ixiahlt {TclAutoPath => ['/root/ixos/lib','/root/hltapi']};
       # use ixiahlt {IXIA_VERSION => $ENV{'IXIA_VERSION'}, TclAutoPath  => [$ENV{'PERL_IXOS_LIB_PATH'}, $ENV{'PERL_IXNET_LIB_PATH'}]};


# Running from Windows: 

	# use lib "C:/Program Files (x86)/Ixia/hltapi/4.95.117.44/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.40";
	# use lib "C:/Program Files (x86)/Ixia/hltapi/4.95.117.44/TclScripts/lib/hltapi/library/common/ixiangpf/perl";

# Loading Ixia packages
use ixiangpf;

use warnings;
use strict;
use bignum;
use Carp;

# Using a hash reference for the HLP procedures 
# (since they return values in form of hashes)
our $HashRef = {};
# Using a common variable to retain the status of each command
our $command_status = '';

my $_result_ = '';
my $_control_status_ = '';
my $_dhcp_stats_ = '';
my @status_keys = ();

################################################################################
# Connection to the chassis, IxNetwork Tcl Server                              #
################################################################################
my @chassis          = ('10.205.28.170');
my $tcl_server       = '10.205.28.170';
my @port_list        = (['1/7', '1/8']);
my $ixNetwork_client = '10.205.28.41:8981';

print "Connecting to chassis and client\n";
$_result_ = ixiangpf::connect({
    reset                => 1,
    device               => @chassis,
    port_list            => @port_list,
    ixnetwork_tcl_server => $ixNetwork_client,
    tcl_server           => $tcl_server,
    break_locks          => 1,
});
@status_keys = ixiangpf::status_item_keys();
$command_status = ixiangpf::status_item('status');
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

# Saving the port handles, which will be used later on in the script
my $port_handles = ixiangpf::status_item('vport_list');
my @port_handles_list = split(/ /,$port_handles);

################################################################################
# Creating topology and device group                                           #
################################################################################

# Creating a topology on first port
print "Adding topology 1 on port 1\n";     
my $topology_1_status = ixiangpf::topology_config ({
    topology_name => "{Topology for OSPFv2 1}",
    port_handle   => $port_handles_list[0],
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $topology_1_handle = $HashRef->{'topology_handle'};

# Creating a device group in topology 
print "Creating device group 1 in topology 1\n";      
my $device_group_1_status = ixiangpf::topology_config ({
    topology_handle         => "$topology_1_handle",
    device_group_name       => "{OSPFv2 Router 1}",
    device_group_multiplier => "1",
    device_group_enabled    => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_1_handle = $HashRef->{'device_group_handle'};
    

# Creating a topology on second port
print "Adding topology 2 on port 2\n";
my $topology_2_status = ixiangpf::topology_config ({
    topology_name => "{Topology for OSPFv2 2}",
    port_handle   => $port_handles_list[1],
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $topology_2_handle = $HashRef->{'topology_handle'};

# Creating a device group in topology
print "Creating device group 2 in topology 2\n";
my $device_group_2_status = ixiangpf::topology_config ({
    topology_handle         => "$topology_2_handle",
    device_group_name       => "{Provider Router 2}",
    device_group_multiplier => "1",
    device_group_enabled    => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_2_handle = $HashRef->{'device_group_handle'};

################################################################################
#  Configure protocol interfaces                                               #
################################################################################

# Creating ethernet stack for the first Device Group 
print "Creating ethernet stack for the first Device Group\n";
my $ethernet_1_status = ixiangpf::interface_config ({
    protocol_name     => "{Ethernet 1}",
    protocol_handle   => "$deviceGroup_1_handle",
    mtu               => "1500",
    src_mac_addr      => "18.03.73.c7.6c.b1",
    src_mac_addr_step => "00.00.00.00.00.00",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ethernet_1_handle = $HashRef->{'ethernet_handle'};

# Creating ethernet stack for the second Device Group
print "Creating ethernet for the second Device Group\n";
my $ethernet_2_status = ixiangpf::interface_config ({
    protocol_name     => "{Ethernet 2}",
    protocol_handle   => "$deviceGroup_2_handle",
    mtu               => "1500",
    src_mac_addr      => "18.03.73.c7.6c.01",
    src_mac_addr_step => "00.00.00.00.00.00",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ethernet_2_handle = $HashRef->{'ethernet_handle'};

# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group                                 
print "Creating IPv4 Stack on top of Ethernet Stack for the first Device Group\n";     
my $ipv4_1_status = ixiangpf::interface_config ({
    protocol_name                => "{IPv4 1}",
    protocol_handle              => "$ethernet_1_handle",
    ipv4_resolve_gateway         => "1",
    ipv4_manual_gateway_mac      => "00.00.00.00.00.01",
    ipv4_manual_gateway_mac_step => "00.00.00.00.00.00",
    gateway                      => "20.20.20.1",
    intf_ip_addr                 => "20.20.20.2",
    netmask                      => "255.255.255.0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv4_1_handle = $HashRef->{'ipv4_handle'};

# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group 
print "Creating IPv4 2 stack on ethernet 2 stack for the second Device Group\n";
my $ipv4_2_status = ixiangpf::interface_config ({
    protocol_name                => "{IPv4 2}",
    protocol_handle              => "$ethernet_2_handle",
    ipv4_resolve_gateway         => "1",
    ipv4_manual_gateway_mac      => "00.00.00.00.00.01",
    ipv4_manual_gateway_mac_step => "00.00.00.00.00.00",
    gateway                      => "20.20.20.2",
    intf_ip_addr                 => "20.20.20.1",
    netmask                      => "255.255.255.0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv4_2_handle = $HashRef->{'ipv4_handle'};

################################################################################
# Other protocol configurations                                                #
################################################################################
# This will create OSPFv2 on top of IP within Topology 1 
print "Creating OSPFv2 on top of IPv4 1 stack\n";
my $ospfv2_1_status = ixiangpf::emulation_ospf_config ({
     handle                  => $ipv4_1_handle,
     mode                    => "create",
     network_type            => "ptop",
     protocol_name           => "{OSPFv2-IF 1}",
     lsa_discard_mode        => "0",
     router_id               => "193.0.0.1",
     router_interface_active => "1",
     router_active           => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ospfv2_handle1 = $HashRef->{'ospfv2_handle'};

# This will create OSPFv2 on top of IP within Topology 2
print "Creating OSPFv2 on top of IPv4 2 stack\n";
my $ospfv2_2_status = ixiangpf::emulation_ospf_config ({
     handle                  => $ipv4_2_handle,
     mode                    => "create",
     network_type            => "ptop",
     protocol_name           => "{OSPFv2-IF 2}",
     lsa_discard_mode        => "0",   
     router_id               => "194.0.0.1",
     router_interface_active => "1",
     router_active           => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ospfv2_handle2 = $HashRef->{'ospfv2_handle'};

# Creating IPv4 prefix pool of Network for Network Cloud behind first
# Device Group  with "ipv4_prefix_network_address" = 201.1.0.1
print "Creating IPv4 prefix pool behind first Device Group\n";
my $network_group_1_status = ixiangpf::network_group_config ({
    protocol_handle                 => $deviceGroup_1_handle,
    protocol_name                   => "{Network Cloud 1}",
    connected_to_handle             => $ethernet_1_handle,
    type                            => "ipv4-prefix",
    ipv4_prefix_network_address     => "201.1.0.1",
    ipv4_prefix_length              => "32",
    ipv4_prefix_number_of_addresses => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_1_handle = $HashRef->{'network_group_handle'};
my $ipv4PrefixPools_1_handle = $HashRef->{'ipv4_prefix_pools_handle'};

print "Configuring OSPFv2 group range for topology 1\n";
my  $ospfv2_network_group_1_status = ixiangpf::emulation_ospf_network_group_config({
    handle                   => $networkGroup_1_handle, 
    mode                     => "modify",
    ipv4_prefix_active       => "1",
    ipv4_prefix_route_origin => "another_area",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

# Creating IPv4 prefix pool of Network for Network Cloud behind second 
# Device Group  with "ipv4_prefix_network_address" =202.1.0.1
print "Creating IPv4 prefix pool behind second Device Group\n";
my $network_group_2_status = ixiangpf::network_group_config ({
    protocol_handle                 => $deviceGroup_2_handle,
    protocol_name                   => "{Network Cloud 2}",
    connected_to_handle             => $ethernet_2_handle,
    type                            => "ipv4-prefix",
    ipv4_prefix_network_address     => "202.1.0.1",
    ipv4_prefix_length              => "32",
    ipv4_prefix_number_of_addresses => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_2_handle = $HashRef->{'network_group_handle'};
my $ipv4PrefixPools_2_handle = $HashRef->{'ipv4_prefix_pools_handle'};

print "Configuring OSPFv2 group range for topology 2\n";
my  $ospfv2_network_group_2_status = ixiangpf::emulation_ospf_network_group_config({
    handle                   => $networkGroup_2_handle,
    mode                     => "modify",
    ipv4_prefix_active       => "1",
    ipv4_prefix_route_origin => "another_area",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

# Going to create Chained Device Group 3  behind Network Cloud 1 within
# Topology 1 and renaming of that chained DG to "Loopback Router 1"
print "Going to create Chained DG 3 in Topology 1 behind Network Cloud 1 and renaming it\n";
my $device_group_1_1_status = ixiangpf::topology_config ({
    device_group_name       => "{Loopback Router 1}",
    device_group_multiplier => "1",
    device_group_enabled    => "1",
    device_group_handle     => $networkGroup_1_handle,
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_1_1_handle = $HashRef->{'device_group_handle'};

# Creating multivalue loopback adderress within chained DG in Topology 1
print "Creating multivalue for loopback adderress within chained DG\n";
my $multivalue1_1_status = ixiangpf::multivalue_config ({
   pattern           => "counter",
   counter_start     => "201.1.0.1",
   counter_step      => "0.0.0.1",
   counter_direction => "increment",
   nest_step         => "0.0.0.1,0.0.0.1,0.1.0.0",
   nest_owner        => "$networkGroup_1_handle,$deviceGroup_1_handle,$topology_1_handle",
   nest_enabled      => "0,0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_4_handle = $HashRef->{'multivalue_handle'};

# Creating Loopback behind Chained DG.
print "Creating Loopback behind Chained DG\n";
my $ipv4_loopback_1_status = ixiangpf::interface_config ({
   protocol_name       => "{IPv4 Loopback 1}",
   protocol_handle     => $deviceGroup_1_1_handle,
   enable_loopback     => "1",
   connected_to_handle => $networkGroup_1_handle,
   intf_ip_addr        => $multivalue_4_handle,
   netmask             => "255.255.255.255",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv4Loopback_1_handle = $HashRef->{'ipv4_loopback_handle'};

# Going to create Chained Device Group 4 behind Network Cloud 1 within
# Topology 4 and renaming of that chained DG to "Provider Edge Router 2"
print "Going to create Chained DG 4 in Topology 2 behind Network Cloud 2 and renaming it\n";
my $device_group_2_1_status = ixiangpf::topology_config ({
    device_group_name       => "{Loopback Router 2}",
    device_group_multiplier => "1",
    device_group_enabled    => "1",
    device_group_handle     => $networkGroup_2_handle,
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_2_1_handle = $HashRef->{'device_group_handle'};

# Creating multivalue loopback adderress within chained DG in Topology 1
print "Creating multivalue for loopback adderress within chained DG\n";
my $multivalue2_1_status = ixiangpf::multivalue_config ({
   pattern           => "counter",
   counter_start     => "202.1.0.1",
   counter_step      => "0.0.0.1",
   counter_direction => "increment",
   nest_step         => "0.0.0.1,0.0.0.1,0.1.0.0",
   nest_owner        => "$networkGroup_2_handle,$deviceGroup_2_handle,$topology_2_handle",
   nest_enabled      => "0,0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_6_handle = $HashRef->{'multivalue_handle'};

# Creating Loopback behind Chained DG.
print "Creating Loopback behind Chained DG\n";
my $ipv4_loopback_2_status = ixiangpf::interface_config ({
   protocol_name       => "{IPv4 Loopback 2}",
   protocol_handle     => $deviceGroup_2_1_handle,
   enable_loopback     => "1",
   connected_to_handle => $networkGroup_2_handle,
   intf_ip_addr        => $multivalue_6_handle,
   netmask             => "255.255.255.255",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv4Loopback_2_handle = $HashRef->{'ipv4_loopback_handle'};


print "Waiting 5 seconds before starting protocol(s) ...\n";
sleep(5);

################################################################################
# Start OSPFv2  protocol                                                       #
################################################################################
print "Starting OSPFv2 in topology1\n";
ixiangpf::test_control({
    handle => $topology_1_handle,
    action => 'start_protocol',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Starting OSPFv2 in topology2\n";
ixiangpf::test_control({
    handle => $topology_2_handle,
    action => 'start_protocol',
});    
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}    
print "Waiting for 30 seconds\n";
sleep(30);

###############################################################################
# Retrieve OSPFv2 learned info                                                #
###############################################################################
print "Retrieving OSPFv2 learned info\n";
my $learned_info = ixiangpf::emulation_ospf_info({
    handle => $ospfv2_handle1,
    mode   => "learned_info",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
@status_keys = ixiangpf::status_item_keys();
foreach (@status_keys) {
    my $my_key = $_;
    my $allLi = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "=================================================================\n";
}

###############################################################################
# Retrieve OSPFv2 stat                                                        #
###############################################################################
print "Retrieving OSPFv2 stat\n";
my $learned_stat = ixiangpf::emulation_ospf_info({
    handle => $ospfv2_handle1,
    mode   => "aggregate_stats",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
@status_keys = ixiangpf::status_item_keys();
foreach (@status_keys) {
    my $my_key = $_;
    my $allLi = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "=================================================================\n";
}

################################################################################
# Disable the OSPFv2 group range                                               #
################################################################################
print "Disabling the OSPFv2 group-range on the topology 2\n";
my $ospfv2_2_modify_status = ixiangpf::emulation_ospf_network_group_config({
    handle             => "$networkGroup_2_handle",
    mode               => "modify",
    ipv4_prefix_active => "0", 
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

################################################################################
# Applying changes one the fly                                                 #
################################################################################
print "Applying changes on the fly\n";
my $applyChanges = ixiangpf::test_control({
   handle => $ipv4_1_handle,
   action => 'apply_on_the_fly_changes',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Wait for 30 seconds";
sleep(30);
################################################################################
# Retrieve protocol learned info again and notice the difference with          #
# previously retrieved learned info                                            #
################################################################################
print "Fetching LDP aggregated learned info for Topology 2\n";
my $learnedinfo = ixiangpf::emulation_ospf_info({
    handle => $ospfv2_handle1,
    mode   => 'learned_info',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
@status_keys = ixiangpf::status_item_keys();
foreach (@status_keys) {
    my $my_key = $_;
    my $allLi = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "=================================================================\n";
}

################################################################################
# Enable the OSPFv2 group range                                                #
################################################################################
print "Disabling the OSPFv2 group-range on the topology 2\n";
$ospfv2_2_modify_status = ixiangpf::emulation_ospf_network_group_config({
    handle             => "$networkGroup_2_handle",
    mode               => "modify",
    ipv4_prefix_active => "1",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

################################################################################
# Applying changes one the fly                                                 #
################################################################################
print "Applying changes on the fly\n";
$applyChanges = ixiangpf::test_control({
   handle => $ipv4_1_handle,
   action => 'apply_on_the_fly_changes',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Wait for 30 seconds\n";
sleep(30);

################################################################################
# Retrieve protocol learned info again and notice the difference with          #
# previously retrieved learned info                                            #
################################################################################
print "Fetching LDP  aggregated learned info for Topology 2\n";
$learnedinfo = ixiangpf::emulation_ospf_info({
    handle => $ospfv2_handle1,
    mode   => 'learned_info',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
@status_keys = ixiangpf::status_item_keys();
foreach (@status_keys) {
    my $my_key = $_;
    my $allLi = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "=================================================================\n";
}

################################################################################
# Configure L2-L3 traffic                                                      #
# 1. Endpoints : Source->IPv4 FEC Range, Destination->IPv4 FEC Range           #
# 2. Type      : Unicast IPv4 traffic                                          #
# 3. Flow Group: On IPv4 Destination Address                                   #
# 4. Rate      : 100000 packets per second                                     #
# 5. Frame Size: 64 bytes                                                      #
# 6. Tracking  : Source Destination EndPoint Set                               #
################################################################################
print "Configuring L2-L3 traffic\n";  
$_result_ = ixiangpf::traffic_config({
    mode                  => 'create',
    traffic_generator     => 'ixnetwork_540',
    endpointset_count     => '1',
    emulation_src_handle  => $ipv4PrefixPools_1_handle,
    emulation_dst_handle  => $ipv4PrefixPools_2_handle,
    frame_sequencing      => 'disable',
    frame_sequencing_mode => 'rx_threshold',
    name                  => 'Traffic_1_Item',
    circuit_endpoint_type => 'ipv4',                              
    rate_pps              => '100000',                                      
    frame_size            => '64',                                           
    mac_dst_mode          => "fixed",
    mac_src_mode          => "fixed",
    mac_src_tracking      => "1",
    track_by              => '{sourceDestEndpointPair0 trackingenabled0}'
});
 
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

################################################################################# 
# Configure L4-L7 Application traffic                                           #
# 1. Endpoints      : Source->IPv4 Loopback, Destination->IPv4 Loopback         #
# 2. Flow Group     : On IPv4 Destination Address                               #
# 3. objective value: 100                                                       #
#################################################################################
print "Configuring L4-L7 App Lib traffic\n"; 
# L4-L7 applib profiles
my $traffic_item_1_status = ixiangpf::traffic_l47_config ({
    mode                        => 'create',
    name                        => 'Traffic Item 2',
    circuit_endpoint_type       => 'ipv4_application_traffic',
    emulation_src_handle        => $ipv4Loopback_1_handle,
    emulation_dst_handle        => $ipv4Loopback_2_handle,
    objective_type              => 'users',
    objective_value             => '100',
    objective_distribution      => 'apply_full_objective_to_each_port',
    enable_per_ip_stats         => '0',
    flows                       => "{Bandwidth_BitTorrent_File_Download 
                                     Bandwidth_eDonkey 
                                     Bandwidth_HTTP 
                                     Bandwidth_IMAPv4 
                                     Bandwidth_POP3 
                                     Bandwidth_Radius 
                                     Bandwidth_Raw 
                                     Bandwidth_Telnet 
                                     Bandwidth_uTorrent_DHT_File_Download 
                                     BBC_iPlayer BBC_iPlayer_Radio 
                                     BGP_IGP_Open_Advertise_Routes 
                                     BGP_IGP_Withdraw_Routes Bing_Search 
                                     BitTorrent_Ares_v217_File_Download 
                                     BitTorrent_BitComet_v126_File_Download 
                                     BitTorrent_Blizzard_File_Download 
                                     BitTorrent_Cisco_EMIX BitTorrent_Enterprise 
                                     BitTorrent_RMIX_5M}",
}); 
  
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
############################################################################
# Start L2-L3 traffic configured earlier                                   #
############################################################################
print "Running Traffic...\n";
$_result_ = ixiangpf::traffic_control({
    action              => 'run',
    traffic_generator   => 'ixnetwork_540',
    type                => 'l23 l47',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Let the traffic run for 20 seconds ...\n";
sleep(20);
############################################################################
# Retrieve L2-L3 traffic stats                                             #
############################################################################
print "Retrieving L2-L3 traffic stats\n";
my $protostats = ixiangpf::traffic_stats({
    mode              => 'all',
    traffic_generator => 'ixnetwork_540',
    measure_mode      => 'mixed',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}   
@status_keys = ixiangpf::status_item_keys();
 foreach (@status_keys) {
    my $my_key = $_;
    my $allStats = ixiangpf::status_item($my_key);
    print "==================================================================\n";
    print "\n$my_key: $allStats\n\n";
    print "==================================================================\n";
 }
############################################################################
# Stop L2-L3 traffic started earlier                                       #
############################################################################
print "Stopping Traffic...\n";
$_result_ = ixiangpf::traffic_control({
    action            => 'stop',
    traffic_generator => 'ixnetwork_540',
    type              => 'l23 l47',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(5);
############################################################################
# Stop all protocols                                                       #
############################################################################
print "Stopping all protocol(s) ...\n";
my $stop_status = ixiangpf::test_control({
    action      => "stop_all_protocols",
});
@status_keys = ixiangpf::status_item_keys();
$command_status = ixiangpf::status_item('status');
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(2);

print "!!! Test Script Ends !!!\n";           
print "SUCCESS - $0\n";         
