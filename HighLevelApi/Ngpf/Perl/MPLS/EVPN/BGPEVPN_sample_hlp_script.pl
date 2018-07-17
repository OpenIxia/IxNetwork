################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright 1997 - 2016 by IXIA                                             #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    27/06/2016 - Poulomi Chatterjee - created sample                          #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL NOTICE:                                 #
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
# meet the user’s requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT IS WITH THE  #
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
#    This script intends to demonstrate how to use NGPF BGP EVPN HLP API.      #
#                                                                              #
# 1. It will create 2 BGP EVPN topologies in following way.                    #
#   - Configure LDP in each connected Device Group.                            #
#   - Configure OSPF in connected Devicr Group to Advertise Loopback Address   #
#       of BGP.                                                                #
#   - Configure Network Groups behind each Device Groups.                      #
#   - Add chained Device Group behind each Network Group, add IPv4 Loopback in #
#      these Device Groups.                                                    #
#   - Configure BGP Peer over IPv4 Loopback .                                  #
#   - Configure EVI stack over BGP.                                            #
#   - Configure MAC Pools behing BGP EVPN Device Group.                        #
#   - Add IPv4/IPv6 Prefixes in Mac Pools.                                     #
# 2. Start all protocol.                                                       #
# 3. Retrieve protocol statistics.                                             #
# 4. Retrieve protocol learned info.                                           #
# 5. Configure L2-L3 traffic.                                                  #
# 6. Start the L2-L3 traffic.                                                  #
# 7. Retrieve L2-L3 traffic stats.                                             #
# 8. Stop L2-L3 traffic.                                                       #
# 9. Stop allprotocols.                                                        #
#                                                                              #
# Ixia Software:                                                               #
#    IxOS      8.10-EB                                                         #
#    IxNetwork 8.10-EB                                                         #
################################################################################

################################################################################
# Running from Linux:
#
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
print "Connecting to chassis ...\n";
my @chassis             = ('10.216.108.82');
my $tcl_server          = '10.216.108.82';
my @port_list           = ([ '7/5', '7/6' ]);
my $ixNetwork_client    = '10.216.104.58:8335';

$_result_ = ixiangpf::connect({
    reset                   => 1,
    device                  => @chassis,
    port_list               => @port_list,
    ixnetwork_tcl_server    => $ixNetwork_client,
    tcl_server              => $tcl_server,
    break_locks             => 1,
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

# Creating a topology in first port
print "Adding topology:1 in port 1\n"; 
my $topology_1_status = ixiangpf::topology_config ({
    topology_name    =>  "{EVPN Topology 1}",
    port_handle      =>  $port_handles_list[0],
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $topology_1_handle = ixiangpf::status_item('topology_handle');

# Creating  device group 1 in topology 1
print "Creating device group 1 in topology 1\n";
my $device_group_1_status = ixiangpf::topology_config ({
    topology_handle              => "$topology_1_handle",
    device_group_name            => "{Provider Router 1}",
    device_group_multiplier      => "1",
    device_group_enabled         => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_1_handle = $HashRef->{'device_group_handle'};

# Creating a topology in second port
print "Adding topology 2 in port 2\n";
my $topology_2_status = ixiangpf::topology_config ({
    topology_name    =>  "{EVPN Topology 2}",
    port_handle      =>  $port_handles_list[1],
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $topology_2_handle = ixiangpf::status_item('topology_handle');

# Creating device group 2 in topology 2
print "Creating device group 2 in topology 2\n";
my $device_group_2_status = ixiangpf::topology_config ({
    topology_handle              => "$topology_2_handle",
    device_group_name            => "{Provider Router 2}",
    device_group_multiplier      => "1",
    device_group_enabled         => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_4_handle = $HashRef->{'device_group_handle'};

################################################################################
#  Configure protocol interfaces                                               #
################################################################################

# Creating ethernet stack in device group 1
print "Creating ethernet stack in first device group\n";
my $ethernet_1_status = ixiangpf::interface_config ({
    protocol_name                => "{Ethernet 1}",
    protocol_handle              => "$deviceGroup_1_handle",
    mtu                          => "1500",
    src_mac_addr                 => "18.03.73.c7.6c.b5",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

my $ethernet_1_handle = $HashRef->{'ethernet_handle'};

# Creating ethernet stack in device group 2
print "Creating ethernet stack in second device group\n";
my $ethernet_2_status = ixiangpf::interface_config ({
    protocol_name                => "{Ethernet 2}",
    protocol_handle              => "$deviceGroup_4_handle",
    mtu                          => "1500",
    src_mac_addr                 => "18.03.73.c7.6c.b6",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ethernet_2_handle = $HashRef->{'ethernet_handle'};

# Creating IPv4 Stack on top of Ethernet Stack
print "Creating IPv4  stack on first ethernet stack\n"; 
my $ipv4_1_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv4 1}",
    protocol_handle                   => "$ethernet_1_handle",
    ipv4_resolve_gateway              => "1",
    ipv4_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv4_manual_gateway_mac_step      => "00.00.00.00.00.00",
    gateway                           => "20.20.20.1",
    intf_ip_addr                      => "20.20.20.2",
    netmask                           => "255.255.255.0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

my $ipv4_1_handle = $HashRef->{'ipv4_handle'};

# Creating IPv4 Stack on top of Ethernet Stack
print "Creating IPv4 stack on second ethernet stack\n";   
my $ipv4_2_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv4 2}",
    protocol_handle                   => "$ethernet_2_handle",
    ipv4_resolve_gateway              => "1",
    ipv4_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv4_manual_gateway_mac_step      => "00.00.00.00.00.00",
    gateway                           => "20.20.20.2",
    intf_ip_addr                      => "20.20.20.1",
    netmask                           => "255.255.255.0",
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
# Configure BGP EVPN Topologies in both ports as described in Description Sec- #
#  tion above.                                                                 #
################################################################################ 

#Creating LDP Stack on top of ipv4 1 stack
print "Creating LDP Stack on top of ipv4 1 stack\n";
my $ldp_basic_router_1_status = ixiangpf::emulation_ldp_config ({
    handle                       => "$ipv4_1_handle",
    mode                         => "create",
    lsr_id                       => "192.0.0.1",
    interface_name               => "{LDP-IF 1}",
    interface_multiplier         => "1",
    interface_active             => "1",
    router_name                  => "{LDP 1}",
    router_multiplier            => "1",
    router_active                => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ldpBasicRouter_1_handle = $HashRef->{'ldp_basic_router_handle'};

my $ldp_connected_interface_1_status = ixiangpf::emulation_ldp_config ({
    handle                    => "$ipv4_1_handle",
    mode                      => "create",
    label_adv                 => "unsolicited",
    label_space               => "0",
    hello_interval            => "5",
    hello_hold_time           => "15",
    auth_mode                 => "null",
    bfd_registration          => "0",
    interface_name            => "{LDP-IF 1}",
    interface_multiplier      => "1",
    interface_active          => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ldpConnectedInterface_1_handle = ixiangpf::status_item('ldp_connected_interface_handle');

#Creating OSPF Stack on top of ipv4 1 stack
print "Creating OSPF Stack on top of ipv4 1 stack\n";
my $ospfv2_1_status = ixiangpf::emulation_ospf_config ({
    handle                                                    => "$ipv4_1_handle",
    router_interface_active                                   => "1",
    protocol_name                                             => "{OSPFv2-IF 1}",
    router_active                                             => "1",
    router_id                                                 => "192.0.0.1",
    network_type                                              => "ptop",
    mode                                                      => "create",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ospfv2_1_handle = ixiangpf::status_item('ospfv2_handle');
  
#Adding IPv4 Prefix Pools behind first DG
print "Adding IPv4 Prefix Pools behind first DG\n";
my $network_group_1_status = ixiangpf::network_group_config ({
    protocol_handle                       => "$deviceGroup_1_handle",
    protocol_name                         => "{Network Group 1}",
    multiplier                            => "1",
    enable_device                         => "1",
    connected_to_handle                   => "$ethernet_1_handle",
    type                                  => "ipv4-prefix",
    ipv4_prefix_network_address           => "2.2.2.2",
    ipv4_prefix_network_address_step      => "0.0.0.0",
    ipv4_prefix_length                    => "32",
    ipv4_prefix_multiplier                => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv4PrefixPools_1_handle = ixiangpf::status_item('ipv4_prefix_pools_handle');
my $networkGroup_1_handle = ixiangpf::status_item('network_group_handle');

# Configuring OSPF Prefix Pool Parameters   
print "Configuring OSPF Prefix Pool Parameters\n";
my $network_group_2_status = ixiangpf::emulation_ospf_network_group_config ({
    handle                           => "$networkGroup_1_handle",
    mode                             => "modify",
    ipv4_prefix_metric               => "0",
    ipv4_prefix_active               => "1",
    ipv4_prefix_allow_propagate      => "0",
    ipv4_prefix_route_origin         => "another_area",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
 
# Configuring LDP Prefix Pool Parameters   
print "Configuring LDP Prefix Pool Parameters\n";
my $network_group_3_status = ixiangpf::emulation_ldp_route_config ({
    mode                        => "modify",
    handle                      => "$networkGroup_1_handle",
    egress_label_mode           => "fixed",
    fec_type                    => "ipv4_prefix",
    label_value_start           => "101",
    label_value_start_step      => "0",
    lsp_handle                  => "$networkGroup_1_handle",
    packing_enable              => "0",
    fec_active                  => "1",
    fec_name                    => "{LDP FEC Range 1}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

# Add DG2 behind IPv4 Prefix Pool
print "Add DG2 behind IPv4 Prefix Pool\n";
my $device_group_3_status = ixiangpf::topology_config ({
    device_group_name            => "{PE 1}",
    device_group_multiplier      => "1",
    device_group_enabled         => "1",
    device_group_handle          => "$networkGroup_1_handle",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_3_handle = ixiangpf::status_item('device_group_handle');
    
my $multivalue_1_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "2.2.2.2",
    counter_step           => "0.0.0.1",
    counter_direction      => "increment",
    nest_step              => "0.0.0.1,0.0.0.1,0.1.0.0",
    nest_owner             => "$networkGroup_1_handle,$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_1_handle = ixiangpf::status_item('multivalue_handle');
    
# Add ipv4 loopback in DG2
print "Add ipv4 loopback in DG2\n";
my $ipv4_loopback_1_status = ixiangpf::interface_config ({
    protocol_name            => "{IPv4 Loopback 1}",
    protocol_handle          => "$deviceGroup_3_handle",
    enable_loopback          => "1",
    connected_to_handle      => "$networkGroup_1_handle",
    intf_ip_addr             => "$multivalue_1_handle",
    netmask                  => "255.255.255.255",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $ipv4Loopback_1_handle = ixiangpf::status_item('ipv4_loopback_handle');

# Adding BGP peer over ipv4 Loopback
print "Adding BGP peer over ipv4 Loopback\n";
my $bgp_ipv4_peer_1_status = ixiangpf::emulation_bgp_config ({
    mode                                    => "enable",
    active                                  => "1",
    handle                                  => "$ipv4Loopback_1_handle",
    ip_version                              => "4",
    local_as                                => "100",
    count                                   => "1",
    local_router_id                         => "2.2.2.2",
    remote_loopback_ip_addr                 => "3.2.2.2",
    ethernet_segments_count                 => "1",
    filter_evpn                             => "1",
    evpn                                    => "1",
    operational_model                       => "symmetric",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $bgpIpv4Peer_1_handle = ixiangpf::status_item('bgp_handle');

# Add BGP EVPN stack on top of BGP
print "Add BGP EVPN stack on top of BGP\n";
my $bgp_i_pv4_evpn_evi_1_status = ixiangpf::emulation_bgp_route_config ({
        handle      => "$bgpIpv4Peer_1_handle",
        mode        => "create",
        evpn        => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $bgpIPv4EvpnEvi_1_handle = ixiangpf::status_item('evpn_evi');

# Configure BGP Ethernet Segment stack 
print "Configure BGP Ethernet Segment stack\n";
my $bgpEthernetSegmentV4_1_status = ixiangpf::emulation_bgp_config ({
    mode                                               => "modify",
    handle                                             => "$bgpIpv4Peer_1_handle",
    active_ethernet_segment                            => "1",
    esi_type                                           => "type0",
    esi_value                                          => "1",
    esi_label                                          => "16",
    advertise_inclusive_multicast_route                => "1",
    evis_count                                         => "1",
    enable_next_hop                                    => "1",
    ethernet_segment_name                              => "{BGP Ethernet Segment 2}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

# Configure EVI parameters
print "Configure EVI parameters\n";
my $bgpIPv4EvpnEvi_2_status_modify = ixiangpf::emulation_bgp_route_config ({
    handle                                           => "$bgpIpv4Peer_1_handle",
    mode                                             => "modify",
    active                                           => "1",
    num_broadcast_domain                             => "1",
    evpn                                             => "1",
    no_of_mac_pools                                  => "1",
    enable_broadcast_domain                          => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
    
# Create MAC/IP Pool behind PE Router 1
print "Create MAC/IP Pool behind PE Router 1\n";
my $network_group_4_status = ixiangpf::network_group_config ({
    protocol_handle                       => "$deviceGroup_3_handle",
    protocol_name                         => "MAC_IP_1",
    multiplier                            => "1",
    enable_device                         => "1",
    connected_to_handle                   => "$bgpIPv4EvpnEvi_1_handle",
    type                                  => "mac-ipv4-prefix",
    mac_pools_multiplier                  => "1",
    mac_pools_prefix_length               => "48",
    mac_pools_mac                         => "a0.11.01.00.00.03",
    ipv4_prefix_network_address           => "201.1.0.1",
    ipv4_prefix_network_address_step      => "0.0.0.1",
    ipv4_prefix_length                    => "32",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $macPools_1_handle = ixiangpf::status_item('mac_pools_handle');
my $ipv4PrefixPools_2_handle = ixiangpf::status_item('ipv4_prefix_pools_handle');
my $networkGroup_4_handle = ixiangpf::status_item('network_group_handle');

# Configure BGP properties in MAC Pool
print "Configure BGP properties in MAC Pool\n";
my $network_group_5_status = ixiangpf::emulation_bgp_route_config ({
    handle                                          => "$networkGroup_4_handle",
    mode                                            => "create",
    active                                          => "1",
    max_route_ranges                                => "1",
    label_step                                      => "1",
    label_mode                                      => "fixed",
    advertise_ipv4_address                          => "1",
    active_ts                                       => "1",
    enable_second_label                             => "0",
    second_label_start                              => "16",
    cmac                                            => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Configuration complete in port 1...\n";

#---------------------------------------------------------------------------------#
#Creating LDP Stack on top of ipv4 2 stack
print "Creating LDP Stack on top of ipv4 2 stack\n";
my $ldp_basic_router_2_status = ixiangpf::emulation_ldp_config ({
    handle                       => "$ipv4_2_handle",
    mode                         => "create",
    lsr_id                       => "194.0.0.1",
    interface_name               => "{LDP-IF 2}",
    interface_multiplier         => "1",
    interface_active             => "1",
    router_name                  => "{LDP 2}",
    router_multiplier            => "1",
    router_active                => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ldpBasicRouter_2_handle = ixiangpf::status_item('ldp_basic_router_handle');

my $ldp_connected_interface_2_status = ixiangpf::emulation_ldp_config ({
    handle                    => "$ipv4_2_handle",
    mode                      => "create",
    label_adv                 => "unsolicited",
    label_space               => "0",
    hello_interval            => "5",
    hello_hold_time           => "15",
    auth_mode                 => "null",
    bfd_registration          => "0",
    interface_name            => "{LDP-IF 2}",
    interface_multiplier      => "1",
    interface_active          => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ldpConnectedInterface_2_handle = ixiangpf::status_item('ldp_connected_interface_handle');

#Creating OSPF Stack on top of ipv4 2 stack
print "Creating OSPF Stack on top of ipv4 2 stack\n";
my $ospfv2_2_status = ixiangpf::emulation_ospf_config ({
    handle                                                    => "$ipv4_2_handle",
    protocol_name                                             => "{OSPFv2-IF 2}",
    router_active                                             => "1",
    network_type                                              => "ptop",
    router_id                                                 => "194.0.0.1",
    mode                                                      => "create",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ospfv2_2_handle = ixiangpf::status_item('ospfv2_handle');

#Adding IPv4 Prefix Pools behind first DG
print "Adding IPv4 Prefix Pools behind first DG\n";
my $network_group_6_status = ixiangpf::network_group_config ({
    protocol_handle                       => "$deviceGroup_4_handle",
    protocol_name                         => "{Network Group 2}",
    multiplier                            => "1",
    enable_device                         => "1",
    connected_to_handle                   => "$ethernet_2_handle",
    type                                  => "ipv4-prefix",
    ipv4_prefix_network_address           => "3.2.2.2",
    ipv4_prefix_network_address_step      => "0.0.0.0",
    ipv4_prefix_length                    => "32",
    ipv4_prefix_multiplier                => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv4PrefixPools_3_handle = ixiangpf::status_item('ipv4_prefix_pools_handle');
my $networkGroup_6_handle = ixiangpf::status_item('network_group_handle');

# Configuring OSPF Prefix Pool Parameters
print "Configuring OSPF Prefix Pool Parameters\n";
my $network_group_7_status = ixiangpf::emulation_ospf_network_group_config ({
    handle                           => "$networkGroup_6_handle",
    mode                             => "modify",
    ipv4_prefix_metric               => "0",
    ipv4_prefix_active               => "1",
    ipv4_prefix_allow_propagate      => "0",
    ipv4_prefix_route_origin         => "another_area",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

# Configuring LDP Prefix Pool Parameters
print "Configuring LDP Prefix Pool Parameters\n";
my $network_group_8_status = ixiangpf::emulation_ldp_route_config ({
    mode                        => "modify",
    handle                      => "$networkGroup_6_handle",
    egress_label_mode           => "fixed",
    fec_type                    => "ipv4_prefix",
    label_value_start           => "201",
    label_value_start_step      => "0",
    lsp_handle                  => "$networkGroup_6_handle",
    packing_enable              => "0",
    fec_active                  => "1",
    fec_name                    => "{LDP FEC Range 2}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

# Add DG2 behind IPv4 Prefix Pool
print "Add DG2 behind IPv4 Prefix Pool\n";
my $device_group_4_status = ixiangpf::topology_config ({
    device_group_name            => "{PE 2}",
    device_group_multiplier      => "1",
    device_group_enabled         => "1",
    device_group_handle          => "$networkGroup_6_handle",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_5_handle = ixiangpf::status_item('device_group_handle');

# Add ipv4 loopback in DG2
print "Add ipv4 loopback in DG2\n";
my $multivalue_15_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "3.2.2.2",
    counter_step           => "0.0.0.1",
    counter_direction      => "increment",
    nest_step              => "0.0.0.1,0.0.0.1,0.1.0.0",
    nest_owner             => "$networkGroup_6_handle,$deviceGroup_3_handle,$topology_2_handle",
    nest_enabled           => "0,0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_15_handle = ixiangpf::status_item('multivalue_handle');

my $ipv4_loopback_2_status = ixiangpf::interface_config ({
    protocol_name            => "{IPv4 Loopback 2}",
    protocol_handle          => "$deviceGroup_5_handle",
    enable_loopback          => "1",
    connected_to_handle      => "$networkGroup_6_handle",
    intf_ip_addr             => "$multivalue_15_handle",
    netmask                  => "255.255.255.255",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv4Loopback_2_handle = ixiangpf::status_item('ipv4_loopback_handle');

# Adding BGP peer over ipv4 Loopback
print "Adding BGP peer over ipv4 Loopback\n";
my $bgp_ipv4_peer_2_status = ixiangpf::emulation_bgp_config ({
    mode                                    => "enable",
    active                                  => "1",
    handle                                  => "$ipv4Loopback_2_handle",
    ip_version                              => "4",
    remote_ip_addr                          => "2.2.2.2",
    local_as                                => "100",
    count                                   => "1",
    local_router_id                         => "3.2.2.2",
    ethernet_segments_count                 => "1",
    filter_evpn                             => "1",
    evpn                                    => "1",
    operational_model                       => "symmetric",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $bgpIpv4Peer_2_handle = ixiangpf::status_item('bgp_handle');

# Add BGP EVPN stack on top of BGP
print "Add BGP EVPN stack on top of BGP\n";
my $bgp_i_pv4_evpn_evi_3_status = ixiangpf::emulation_bgp_route_config ({
    handle      => "$bgpIpv4Peer_2_handle",
    mode        => "create",
    evpn        => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $bgpIPv4EvpnEvi_3_handle = ixiangpf::status_item('evpn_evi');

# Configure BGP Ethernet Segment stack
print "Configure BGP Ethernet Segment stack\n";
my $bgpEthernetSegmentV4_2_status = ixiangpf::emulation_bgp_config ({
    mode                                               => "modify",
    handle                                             => "$bgpIpv4Peer_2_handle",
    active_ethernet_segment                            => "1",
    esi_type                                           => "type0",
    esi_value                                          => "2",
    support_multihomed_es_auto_discovery               => "1",
    evis_count                                         => "1",
    ethernet_segment_name                              => "{BGP Ethernet Segment 4}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

# Configure EVI parameters
print "Configure EVI parameters\n";
my $bgpIPv4EvpnEvi_4_status_modify = ixiangpf::emulation_bgp_route_config ({
    handle                                           => "$bgpIpv4Peer_2_handle",
    mode                                             => "modify",
    active                                           => "1",
    evpn                                             => "1",
    no_of_mac_pools                                  => "1",
    enable_broadcast_domain                          => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

# Create MAC/IP Pool behind PE Router 2
print "Create MAC/IP Pool behind PE Router 2\n";
my $network_group_9_status = ixiangpf::network_group_config ({
    protocol_handle                       => "$deviceGroup_5_handle",
    protocol_name                         => "MAC_IP_2",
    multiplier                            => "1",
    enable_device                         => "1",
    connected_to_handle                   => "$bgpIPv4EvpnEvi_3_handle",
    type                                  => "mac-ipv4-prefix",
    mac_pools_multiplier                  => "1",
    mac_pools_prefix_length               => "48",
    mac_pools_mac                         => "a0.12.01.00.00.03",
    ipv4_prefix_network_address           => "201.1.0.5",
    ipv4_prefix_network_address_step      => "0.0.0.1",
    ipv4_prefix_length                    => "32",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $macPools_2_handle = ixiangpf::status_item('mac_pools_handle');
my $ipv4PrefixPools_4_handle = ixiangpf::status_item('ipv4_prefix_pools_handle');
my $networkGroup_9_handle = ixiangpf::status_item('network_group_handle');

# Configure BGP properties in MAC Pool
print "Configure BGP properties in MAC Pool\n";
my $network_group_10_status = ixiangpf::emulation_bgp_route_config ({
    handle                                          => "$networkGroup_9_handle",
    mode                                            => "create",
    active                                          => "1",
    max_route_ranges                                => "1",
    advertise_ipv4_address                          => "1",
    active_ts                                       => "1",
    first_label_start                               => "216",
    enable_second_label                             => "1",
    second_label_start                              => "316",
    label_mode                                      => "fixed",
    cmac                                            => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Configuration complete in port 2...\n";

###########################################################################
# Start protocols                                                         #
############################################################################

print "Starting all protocol(s) ...\n";
my $startProtocol = ixiahlt::test_control({action => 'start_all_protocols'});
@status_keys = ixiangpf::status_item_keys();
$command_status = ixiangpf::status_item('status');
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
print "Waiting for 120 seconds\n";
sleep(60);

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
print "Fetching BGP statistics\n";
# Check Stats using BGP Router handle
print "Check Stats using BGP Router handle ...\n";
my $protostats = ixiangpf::emulation_bgp_info({
    handle => $bgpIpv4Peer_1_handle,
    mode   => 'stats'});
@status_keys = ixiangpf::status_item_keys();
foreach (@status_keys) {
    my $my_key = $_;
    my $allStats = ixiangpf::status_item($my_key);
    print "==================================================================\n";
    print "\n$my_key: $allStats\n\n";
    print "==================================================================\n";
}

############################################################################
# Retrieve protocol learned info                                           #
############################################################################
print "Fetching EVPN  learned info\n";
# Check Learned Info for port 2 using BGP Router handle
print "Check Learned Info using BGP Router handle ...\n";
my $lInfo = ixiangpf::emulation_bgp_info({
    handle => $bgpIpv4Peer_1_handle,
    mode => 'learned_info'});
@status_keys = ixiangpf::status_item_keys();
foreach (@status_keys) {
    my $my_key = $_;
    my $allLearnedInfo = ixiangpf::status_item($my_key);
    print "==================================================================\n";
    print "\n$my_key: $allLearnedInfo\n\n";
    print "==================================================================\n";
}

############################################################################
# On The Fly disable/enable C-MAC 
############################################################################
print "On The Fly disable C-MAC\n";
#(handle : user needs to create and provide handle for cMacProperties, as scriptgen does not return this handle by default)
my $disable_cmac = ixiangpf::emulation_bgp_route_config ({
   handle =>  '/topology:1/deviceGroup:1/networkGroup:1/deviceGroup:1/networkGroup:1/macPools:1/cMacProperties:3',
   mode => 'disable'});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Apply On The Fly changes\n";
my $applyChanges = ixiangpf::test_control ({
   action => 'apply_on_the_fly_changes'});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(30);

print "On The Fly enable C-MAC\n";
#(handle : user needs to create and provide handle for cMacProperties, as scriptgen does not return this handle by default)
my $enable_cmac = ixiangpf::emulation_bgp_route_config ({
   handle => '/topology:1/deviceGroup:1/networkGroup:1/deviceGroup:1/networkGroup:1/macPools:1/cMacProperties:3',
   mode => 'enable'});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Apply On The Fly changes\n";
my $applyChanges1 = ixiangpf::test_control ({
   action =>  'apply_on_the_fly_changes'});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(30);

############################################################################
# Configure L2-L3 traffic                                                  #
############################################################################
print "Configure L2-L3 traffic\n";
# Configure L2-L3 IPv4 Traffic

$_result_ = ixiangpf::traffic_config ({
    mode                    =>        'create',
    traffic_generator       =>        'ixnetwork_540',
    endpointset_count       =>        '1',
    emulation_src_handle    =>        [[$networkGroup_4_handle]],
    emulation_dst_handle    =>        [[$networkGroup_9_handle]],
    name                    =>        'Traffic_Item_1',
    circuit_endpoint_type   =>        'ipv4',
    rate_pps                =>        '100',
    track_by                =>        'trackingenabled0 mplsFlowDescriptor0',
});
my @current_config_elements1 = ixiangpf::status_item('traffic_item');
my $current_config_element1 = $current_config_elements1[0];

print "Configured L2-L3 IPv4 traffic item!!!\n";

############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
print "\n Running L2-L3 Traffic...\n";
$_result_ = ixiangpf::traffic_control ({
    action               => 'run',
    traffic_generator    => 'ixnetwork_540',
    type                 => 'l23',
});

print "Let the traffic run for 30 seconds ...\n";
sleep(30);

############################################################################
# Retrieve L2-L3 traffic stats                                             #
############################################################################
print "Retrieving traffic stats\n";
print "Retrieving All traffic stats\n";
$protostats = ixiangpf::traffic_stats ({
    mode                => 'all',
    traffic_generator   => 'ixnetwork_540',
    measure_mode        => 'mixed',
});

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
print "Stopping L2-L3 Traffic...\n";
$_result_ = ixiangpf::traffic_control ({
    action              => 'stop',
    traffic_generator   => 'ixnetwork_540',
    type                => 'l23',
});

############################################################################
# Stop all protocols                                                       #
############################################################################
print "Stopping all protocol(s) ...\n";
my $stop_status = ixiangpf::test_control ({
    action      => "stop_all_protocols",
});
@status_keys = ixiangpf::status_item_keys();
$command_status = ixiangpf::status_item('status');
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(5);

print "!!! Test Script Ends !!!\n";
print "SUCCESS - $0\n";
