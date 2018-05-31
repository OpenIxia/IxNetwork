################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    05/01/2015 - Rudra Dutta - created sample                                 #
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
#    This script intends to demonstrate how to use NGPF BGP+ API.              #
#                                                                              #
#    1. It will create 2 BGP+ topologies, each having an ipv6 network          #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start BGP+ protocol.                                                   #
#    3. Retrieve protocol statistics.                                          #
#    4. Enable the BGP+ Learned Information on the fly.                        #
#    5. Retrieve BGP+ IPv6 Learned Information.                                #
#    6. Configure L2-L3 traffic.                                               #
#    7. Configure application traffic.                                         #
#    8. Start the L2-L3 traffic.                                               #
#    9. Start the application traffic.                                         #
#   10. Retrieve Appilcation traffic stats.                                    #
#   11. Retrieve L2-L3 traffic stats.                                          #
#   12. Stop L2-L3 traffic.                                                    #
#   13. Stop Application traffic.                                              #
#   14. Stop all protocols.                                                    #
#                                                                              #
# Ixia Software:                                                               #
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

# Using a hash reference for the HLP procedures (since they return values in form of hashes)
our $HashRef = {};
#Using a common variable to retain the status of each command
our $command_status = '';

my $_result_ = '';
my $_control_status_ = '';
my $_dhcp_stats_ = '';
my @status_keys = ();

################################################################################
# Connection to the chassis, IxNetwork Tcl Server                              #
################################################################################
my @chassis             = ('10.205.28.170');
my $tcl_server          = '10.205.28.170';
my @port_list           = ([ '1/7', '1/8' ]);
my $ixNetwork_client    = '10.205.28.41:8981';

print "Connecting to chassis and client\n";
$_result_ = ixiangpf::connect({
    reset                   => 1,
    device                  => @chassis,
    port_list               => @port_list,
    ixnetwork_tcl_server    => $ixNetwork_client,
    tcl_server              => $tcl_server,
    break_locks             => 1,
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
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
print "Adding Topology 1 on Port 1\n";
my $topology_1_status = ixiangpf::topology_config ({
    topology_name      => "{BGP+ Topology 1}",
    port_handle        => $port_handles_list[0],
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $topology_1_handle = ixiangpf::status_item('topology_handle');
 
# Creating a device group in topology 
print "Creating device group 1 in topology 1\n";   
my $device_group_1_status = ixiangpf::topology_config ({
    topology_handle              => "$topology_1_handle",
    device_group_name            => "{BGP+ Topology 1 Router}",
    device_group_multiplier      => "1",
    device_group_enabled         => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_1_handle = ixiangpf::status_item('device_group_handle');

# Creating a topology on second port
print "Adding Topology 2 on Port 2\n";
my $topology_2_status = ixiangpf::topology_config ({
    topology_name      => "{BGP+ Topology 2}",
    port_handle        => $port_handles_list[1],
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $topology_2_handle = ixiangpf::status_item('topology_handle');

# Creating a device group in topology
print "Creating device group 2 in topology 2\n";
my $device_group_2_status = ixiangpf::topology_config ({
    topology_handle              => "$topology_2_handle",
    device_group_name            => "{BGP+ Topology 2 Router}",
    device_group_multiplier      => "1",
    device_group_enabled         => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_2_handle = ixiangpf::status_item('device_group_handle');

################################################################################
#  Configure protocol interfaces                                               #
################################################################################

# Creating ethernet stack for the first Device Group 
my $ethernet_1_status = ixiangpf::interface_config ({
    protocol_name                => "{Ethernet 1}",
    protocol_handle              => "$deviceGroup_1_handle",
    mtu                          => "1500",
    src_mac_addr                 => "18.03.73.c7.6c.b1",
    src_mac_addr_step            => "00.00.00.00.00.00",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $ethernet_1_handle = $HashRef->{'ethernet_handle'};
    
# Creating ethernet stack for the second Device Group
print "Creating ethernet for the second Device Group\n";
my $ethernet_2_status = ixiangpf::interface_config ({
    protocol_name                => "{Ethernet 2}",
    protocol_handle              => "$deviceGroup_2_handle",
    mtu                          => "1500",
    src_mac_addr                 => "18.03.73.c7.6c.01",
    src_mac_addr_step            => "00.00.00.00.00.00",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ethernet_2_handle = $HashRef->{'ethernet_handle'};

# Creating IPv6 Stack on top of Ethernet Stack for the first Device Group                                 
print "Creating IPv6 Stack on top of Ethernet Stack for the first Device Group\n";
my $ipv6_1_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv6 1}",
    protocol_handle                   => "$ethernet_1_handle",
    ipv6_multiplier                   => "1",
    ipv6_resolve_gateway              => "1",
    ipv6_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step      => "00.00.00.00.00.00",
    ipv6_gateway                      => "11:0:0:0:0:0:0:2",
    ipv6_gateway_step                 => "::0",
    ipv6_intf_addr                    => "11:0:0:0:0:0:0:1",
    ipv6_intf_addr_step               => "::0",
    ipv6_prefix_length                => "64",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv6_1_handle = ixiangpf::status_item('ipv6_handle');

# Creating IPv6 Stack on top of Ethernet Stack for the first Device Group
print "Creating IPv6 Stack on top of Ethernet Stack for the second Device Group\n";
my $ipv6_2_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv6 2}",
    protocol_handle                   => "$ethernet_2_handle",
    ipv6_multiplier                   => "1",
    ipv6_resolve_gateway              => "1",
    ipv6_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step      => "00.00.00.00.00.00",
    ipv6_gateway                      => "11:0:0:0:0:0:0:1",
    ipv6_gateway_step                 => "::0",
    ipv6_intf_addr                    => "11:0:0:0:0:0:0:2",
    ipv6_intf_addr_step               => "::0",
    ipv6_prefix_length                => "64",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv6_2_handle = ixiangpf::status_item('ipv6_handle');

################################################################################
# Other protocol configurations                                                # 
################################################################################
# This will create BGP Stack on top of IPv6 stack

# Creating BGP Stack on top of IPv6 stack
print "Creating BGP+ Stack on top of IPv6 stack in first topology on port 1\n";
my $bgp_ipv6_peer_1_status = ixiangpf::emulation_bgp_config ({
    mode                                    => "enable",
    active                                  => "1",
    handle                                  => "$ipv6_1_handle",
    ip_version                              => "6",
    remote_ipv6_addr                        => "11:0:0:0:0:0:0:2",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgpIpv6Peer_1_handle = ixiangpf::status_item('bgp_handle');

print "Creating BGP+ Stack on top of IPv6 stack in first topology on port 2\n";
my $bgp_ipv6_peer_2_status = ixiangpf::emulation_bgp_config ({
    mode                                    => "enable",
    active                                  => "1",
    handle                                  => "$ipv6_2_handle",
    ip_version                              => "6",
    remote_ipv6_addr                        => "11:0:0:0:0:0:0:1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgpIpv6Peer_2_handle = ixiangpf::status_item('bgp_handle');
    
# Creating multivalue for network group
print "Creating multivalue pattern for BGP+ network group on Port 1\n";
my $multivalue_4_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "3000:0:1:1:0:0:0:0",
    counter_step           => "0:0:0:1:0:0:0:0",
    counter_direction      => "increment",
    nest_step              => "0:0:0:0:0:0:0:1,0:0:1:0:0:0:0:0",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_4_handle = ixiangpf::status_item('multivalue_handle');
    
# Creating BGP+ Network Group 
print "Creating BGP+ Network Group on Port 1\n";
my $network_group_1_status = ixiangpf::network_group_config ({
    protocol_handle                      => "$deviceGroup_1_handle",
    protocol_name                        => "BGP+_1_Network_Group1",
    multiplier                           => "1",
    enable_device                        => "1",
    connected_to_handle                  => "$ethernet_1_handle",
    type                                 => "ipv6-prefix",
    ipv6_prefix_network_address          => "$multivalue_4_handle",
    ipv6_prefix_length                   => "64",
    ipv6_prefix_number_of_addresses      => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_1_handle = ixiangpf::status_item('network_group_handle');
my $ipv6PrefixPools_1_handle = ixiangpf::status_item('ipv6_prefix_pools_handle');

# Creating multivalue for network group
print "Creating multivalue pattern for BGP+ network group on Port 2\n";
my $multivalue_10_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "3000:1:1:1:0:0:0:0",
    counter_step           => "0:0:0:1:0:0:0:0",
    counter_direction      => "increment",
    nest_step              => "0:0:0:0:0:0:0:1,0:0:1:0:0:0:0:0",
    nest_owner             => "$deviceGroup_2_handle,$topology_2_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_10_handle = ixiangpf::status_item('multivalue_handle');

# Creating BGP+ Network Group
print "Creating BGP+ Network Group on Port 2\n";
my $network_group_3_status = ixiangpf::network_group_config ({
    protocol_handle                      => "$deviceGroup_2_handle",
    protocol_name                        => "BGP+_2_Network_Group1",
    multiplier                           => "1",
    enable_device                        => "1",
    connected_to_handle                  => "$ethernet_2_handle",
    type                                 => "ipv6-prefix",
    ipv6_prefix_network_address          => "$multivalue_10_handle",
    ipv6_prefix_length                   => "64",
    ipv6_prefix_number_of_addresses      => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_3_handle = ixiangpf::status_item('network_group_handle');
my $ipv6PrefixPools_3_handle = ixiangpf::status_item('ipv6_prefix_pools_handle');

# Creating device group to add loopback
print "Creating device group to add loopback\n";
$device_group_2_status = ixiangpf::topology_config ({
    device_group_name            => "{Device Group 3}",
    device_group_multiplier      => "1",
    device_group_enabled         => "1",
    device_group_handle          => "$networkGroup_1_handle",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_3_handle = ixiangpf::status_item('device_group_handle');

# Creating multivalue pattern for IPv6 Loopback
print "Creating multivalue pattern for IPv6 Loopback on Port 1\n";
my $multivalue_7_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "3000:0:1:1:0:0:0:0",
    counter_step           => "0:0:0:0:0:0:0:1",
    counter_direction      => "increment",
    nest_step              => "0:0:0:0:0:0:0:1,0:0:0:0:0:0:0:1,0:0:0:1:0:0:0:0",
    nest_owner             => "$networkGroup_1_handle,$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_7_handle = ixiangpf::status_item('multivalue_handle');
    
# Creating IPv6 Loopback
print "Creating IPv6 Loopback on Port 1\n";
my $ipv6_loopback_1_status = ixiangpf::interface_config ({
    protocol_name            => "{IPv6 Loopback 1}",
    protocol_handle          => "$deviceGroup_3_handle",
    enable_loopback          => "1",
    connected_to_handle      => "$networkGroup_1_handle",
    ipv6_multiplier          => "1",
    ipv6_intf_addr           => "$multivalue_7_handle",
    ipv6_prefix_length       => "128",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv6Loopback_1_handle = ixiangpf::status_item('ipv6_loopback_handle');
    
# Creating device group to add loopback
print "Creating device group to add loopback\n";
my $device_group_4_status = ixiangpf::topology_config ({
    device_group_name            => "{Device Group 4}",
    device_group_multiplier      => "1",
    device_group_enabled         => "1",
    device_group_handle          => "$networkGroup_3_handle",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_4_handle = ixiangpf::status_item('device_group_handle');

# Creating multivalue pattern for IPv6 Loopback
print "Creating multivalue pattern for IPv6 Loopback on Port 2\n";    
my $multivalue_13_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "3000:1:1:1:0:0:0:0",
    counter_step           => "0:0:0:0:0:0:0:1",
    counter_direction      => "increment",
    nest_step              => "0:0:0:0:0:0:0:1,0:0:0:0:0:0:0:1,0:0:0:1:0:0:0:0",
    nest_owner             => "$networkGroup_3_handle,$deviceGroup_3_handle,$topology_2_handle",
    nest_enabled           => "0,0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_13_handle = ixiangpf::status_item('multivalue_handle');
    
# Creating multivalue pattern for IPv6 Loopback
print "Creating IPv6 Loopback behind Network Group in Topology 2\n";
my $ipv6_loopback_2_status = ixiangpf::interface_config ({
    protocol_name            => "{IPv6 Loopback 2}",
    protocol_handle          => "$deviceGroup_4_handle",
    enable_loopback          => "1",
    connected_to_handle      => "$networkGroup_3_handle",
    ipv6_multiplier          => "1",
    ipv6_intf_addr           => "$multivalue_13_handle",
    ipv6_prefix_length       => "128",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv6Loopback_2_handle = ixiangpf::status_item('ipv6_loopback_handle');
    
print "Waiting 05 seconds before starting protocol\n";
sleep(5);
    
############################################################################
# Start BGP protocol                                                       #
############################################################################
print "Starting BGP+ on Topology 1 & Topology 2\n";
ixiangpf::test_control({action => 'start_all_protocols'});
@status_keys = ixiangpf::status_item_keys();
$command_status = ixiangpf::status_item('status');
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
print "Waiting for 45 seconds\n";
sleep(45);

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
print "Fetching BGP aggregated statistics on Port 1";
my $protostats = ixiangpf::emulation_bgp_info({
    handle => $bgpIpv6Peer_1_handle,
    mode   => 'stats'}); 
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

print "Fetching BGP aggregated statistics on Port 2\n";
$protostats = ixiangpf::emulation_bgp_info({
    handle => $bgpIpv6Peer_2_handle,
    mode   => 'stats'});
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

################################################################################
# Enabling the IPv6 Filter for BGP Learned Information                         #
################################################################################
print "Enabling the IPv6 Learned Information for BGP\n";
my $bgp_1_status = ixiangpf::emulation_bgp_config ({
    handle                               => "$bgpIpv6Peer_1_handle",
    mode                                 => 'modify',
    ipv6_filter_unicast_nlri             => "1",
});
my $bgp_2_status = ixiangpf::emulation_bgp_config ({
    handle                               => "$bgpIpv6Peer_2_handle",
    mode                                 => 'modify',
    ipv6_filter_unicast_nlri             => "1",
});

################################################################################
# Applying changes one the fly                                                 #
################################################################################
print "Applying changes on the fly\n";
my $applyChanges = ixiangpf::test_control({
    action => 'apply_on_the_fly_changes',});
sleep(5);
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(10);

############################################################################
# Retrieve Learned Info                                                    #
############################################################################
print "Fetching BGP LearnedInfo on Port 1\n";
my $bgpLearnedInfo = ixiangpf::emulation_bgp_info({
    handle => $bgpIpv6Peer_1_handle,
    mode => 'learned_info'});
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

print "Fetching BGP LearnedInfo on Port 2\n";
$bgpLearnedInfo = ixiangpf::emulation_bgp_info({
    handle => $bgpIpv6Peer_2_handle,
    mode => 'learned_info'});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error\n";
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
# Configure L2-L3 traffic                                                  #
############################################################################
print "Configuring L2-L3 Traffic Item\n";
$_result_ = ixiangpf::traffic_config({
    mode => 'create',
    traffic_generator => 'ixnetwork_540',
    endpointset_count => 1,
    circuit_endpoint_type => 'ipv6',
    emulation_src_handle => $networkGroup_1_handle,
    emulation_dst_handle => $networkGroup_3_handle,
    rate_pps => '1000',	
    frame_size => '512',
    track_by => 'sourceDestEndpointPair0 trackingenabled0',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error\n";
    return "FAILED - $error";
}

############################################################################
# Configure L4-L7 traffic                                                  #
############################################################################
print "Configuring L4-L7 Traffic Item\n";
$_result_ = ixiangpf::traffic_l47_config ({
    mode                        => "create",
    name                        => "{Traffic Item 2}",
    circuit_endpoint_type       => "ipv6_application_traffic",
    emulation_src_handle        => $ipv6Loopback_1_handle,
    emulation_dst_handle        => $ipv6Loopback_2_handle,
    objective_type              => "users",
    objective_value             => "100",
    objective_distribution      => "apply_full_objective_to_each_port",
    enable_per_ip_stats         => "0",
    flows                       => "{AOL_Instant_Messenger AOL_Webmail AOL_Webmail_Deprecated AppleJuice AppLine_Demo_Superflow AppLine_Simple_Chat Ares_v2183042_Login_File_Download Average_Web_Page_2011 Bandwidth_BitTorrent_File_Download Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4 Bandwidth_POP3 Bandwidth_Radius Bandwidth_Raw Bandwidth_Telnet Bandwidth_uTorrent_DHT_File_Download}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error\n";
    return "FAILED - $error";
}
       
############################################################################
#  Start L2-L3 & L4-L7 traffic configured earlier                          #
############################################################################
print "Running Traffic\n";
$_result_ = ixiangpf::traffic_control({
    action 			=> 'run',
    traffic_generator 	=> 'ixnetwork_540',
    type 			=> ['l23','l47'],
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error\n";
    return "FAILED - $error";
}
print "Let the traffic run for 20 seconds\n";
sleep(20);
    
############################################################################
# Retrieve L2-L3 & L4-L7 traffic stats                                     #
############################################################################
print "Retrieving L2-L3 & L4-L7 traffic stats\n";
$protostats = ixiangpf::traffic_stats({
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
# Stop L2-L3 & L4-L7 traffic started earlier                               #
############################################################################
print "Stopping Traffic\n";
$_result_ = ixiangpf::traffic_control({
    action 			=> 'stop',
    traffic_generator 	=> 'ixnetwork_540',
    type 			=> ['l23','l47']
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error\n";
    return "FAILED - $error";
}
    
############################################################################
# Stop all protocols                                                       #
############################################################################
print "Stopping all protocol\n";
ixiangpf::test_control({action => 'stop_all_protocols'});
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
                    
