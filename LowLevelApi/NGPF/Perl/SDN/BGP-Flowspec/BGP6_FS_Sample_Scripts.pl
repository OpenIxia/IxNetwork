################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
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
#    Description:                                                              #
#    This script intends to demonstrate how to use NGPF BGP6 API               #
#    It will create 2 BGP topologies, it will start the emulation and          #
#    than it will retrieve and display few statistics and modify the FLOW-SPEC #
#    field through HLT.                         						       #
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
my @chassis             = ('10.39.50.122');
my $tcl_server          = '10.39.50.122';
my @port_list           = ([ '1/7', '1/8' ]);
my $ixNetwork_client    = '10.39.43.12:8009';

# Connecting to chassis and client
print "Connecting to Chassis and Client...\n";
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

# Retrieving port handles, for later use
my $port_handles = ixiangpf::status_item('vport_list');
my @port_handles_list = split(/ /,$port_handles);

################################################################################
# Creating topology and device group                                           #
################################################################################
# Creating a topology on first port
print "Adding Topology 1 on Port 1\n";    
my $topology_1_status = ixiangpf::topology_config ({
    topology_name      => "{BGP6 Topology 1}",
    port_handle        => $port_handles_list[0],
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $topology_1_handle = $HashRef->{'topology_handle'};
 
# Creating a device group in topology 
print "Creating device group 1 in topology 1\n";   
my $device_group_1_status = ixiangpf::topology_config ({
    topology_handle              => "$topology_1_handle",
    device_group_name            => "{BGP6 Topology 1 Router}",
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
my $deviceGroup_1_handle = $HashRef->{'device_group_handle'};

# Creating a topology on second port
print "Adding Topology 2 on Port 2\n";
my $topology_2_status = ixiangpf::topology_config ({
    topology_name      => "{BGP6 Topology 2}",
    port_handle        => $port_handles_list[1],
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $topology_2_handle = $HashRef->{'topology_handle'};

# Creating a device group in topology
print "Creating device group 2 in topology 2\n";
my $device_group_2_status = ixiangpf::topology_config ({
    topology_handle              => "$topology_2_handle",
    device_group_name            => "{BGP6 Topology 2 Router}",
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
my $deviceGroup_2_handle = $HashRef->{'device_group_handle'};

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
    ipv6_gateway                      => "2000:0:0:1:0:0:0:1",
    ipv6_gateway_step                 => "::0",
    ipv6_intf_addr                    => "2000:0:0:1:0:0:0:2",
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
my $ipv6_1_handle = $HashRef->{'ipv6_handle'};

# Creating IPv6 Stack on top of Ethernet Stack for the Second Device Group
print "Creating IPv6 Stack on top of Ethernet Stack for the second Device Group\n";
my $ipv6_2_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv6 2}",
    protocol_handle                   => "$ethernet_2_handle",
    ipv6_multiplier                   => "1",
    ipv6_resolve_gateway              => "1",
    ipv6_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step      => "00.00.00.00.00.00",
    ipv6_gateway                      => "2000:0:0:1:0:0:0:2",
    ipv6_gateway_step                 => "::0",
    ipv6_intf_addr                    => "2000:0:0:1:0:0:0:1",
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
my $ipv6_2_handle = $HashRef->{'ipv6_handle'};

################################################################################
# Other protocol configurations                                                # 
################################################################################
# This will create BGP6 Stack on top of IPv6 stack @PEER1 side 
print "Creating BGP6 Stack on top of IPv6 Stack in Topology 1 with AFI/SAFI Config\n";    
my $bgp_v6_interface_1_status = ixiangpf::emulation_bgp_config ({
    mode                                         => "enable",
    active                                       => "1",
    md5_enable                                   => "0",
    md5_key                                      => "Ixia",
    handle                                       => "$ipv6_1_handle",
    ip_version                                   => "6",
    remote_ipv6_addr                             => "2000:0:0:1:0:0:0:1",
    next_hop_enable                              => "0",
    next_hop_ip                                  => "0.0.0.0",
    enable_4_byte_as                             => "0",
    local_as                                     => "0",
    local_as4                                    => "0",
    update_interval                              => "0",
    count                                        => "1",
    local_router_id                              => "192.0.0.1",
    local_router_id_step                         => "0.0.0.0",
    hold_time                                    => "90",
    neighbor_type                                => "internal",
    graceful_restart_enable                      => "0",
    restart_time                                 => "45",
    stale_time                                   => "0",
    tcp_window_size                              => "8192",
    local_router_id_enable                       => "1",
    ipv4_capability_mdt_nlri                     => "0",
    ipv4_capability_unicast_nlri                 => "1",
    ipv4_filter_unicast_nlri                     => "1",
    ipv4_capability_multicast_nlri               => "1",
    ipv4_filter_multicast_nlri                   => "0",
    ipv4_capability_mpls_nlri                    => "1",
    ipv4_filter_mpls_nlri                        => "0",
    ipv4_capability_mpls_vpn_nlri                => "1",
    ipv4_filter_mpls_vpn_nlri                    => "0",
    ipv6_capability_unicast_nlri                 => "1",
    ipv6_filter_unicast_nlri                     => "1",
    ipv6_capability_multicast_nlri               => "1",
    ipv6_filter_multicast_nlri                   => "0",
    ipv6_capability_mpls_nlri                    => "1",
    ipv6_filter_mpls_nlri                        => "0",
    ipv6_capability_mpls_vpn_nlri                => "1",
    ipv6_filter_mpls_vpn_nlri                    => "0",
    capability_route_refresh                     => "1",
    capability_route_constraint                  => "0",
    ttl_value                                    => "64",
    updates_per_iteration                        => "1",
    bfd_registration                             => "0",
    bfd_registration_mode                        => "multi_hop",
    vpls_capability_nlri                         => "1",
    vpls_filter_nlri                             => "0",
    act_as_restarted                             => "0",
    discard_ixia_generated_routes                => "0",
    flap_down_time                               => "0",
    local_router_id_type                         => "same",
    enable_flap                                  => "0",
    send_ixia_signature_with_routes              => "0",
    flap_up_time                                 => "0",
    ipv4_capability_multicast_vpn_nlri           => "0",
    ipv4_filter_multicast_vpn_nlri               => "0",
    ipv6_capability_multicast_vpn_nlri           => "0",
    ipv6_filter_multicast_vpn_nlri               => "0",
    advertise_end_of_rib                         => "0",
    configure_keepalive_timer                    => "0",
    keepalive_timer                              => "30",
    as_path_set_mode                             => "no_include",
    router_id                                    => "192.0.0.1",
    filter_link_state                            => "0",
    capability_linkstate_nonvpn                  => "0",
    bgp_ls_id                                    => "0",
    instance_id                                  => "0",
    number_of_communities                        => "1",
    enable_community                             => "0",
    number_of_ext_communities                    => "1",
    enable_ext_community                         => "0",
    enable_override_peer_as_set_mode             => "0",
    bgp_ls_as_set_mode                           => "include_as_seq",
    number_of_as_path_segments                   => "1",
    enable_as_path_segments                      => "1",
    number_of_clusters                           => "1",
    enable_cluster                               => "0",
    ethernet_segments_count                      => "0",
    filter_evpn                                  => "0",
    evpn                                         => "0",
    operational_model                            => "symmetric",
    routers_mac_or_irb_mac_address               => "00:01:03:00:00:01",
    capability_ipv4_unicast_add_path             => "0",
    capability_ipv6_unicast_add_path             => "0",
    ipv4_mpls_add_path_mode                      => "both",
    ipv6_mpls_add_path_mode                      => "both",
    ipv4_unicast_add_path_mode                   => "both",
    ipv6_unicast_add_path_mode                   => "both",
    ipv4_mpls_capability                         => "0",
    ipv6_mpls_capability                         => "0",
    capability_ipv4_mpls_add_path                => "0",
    capability_ipv6_mpls_add_path                => "0",
    custom_sid_type                              => "40",
    srgb_count                                   => "1",
    start_sid                                    => "16000",
    sid_count                                    => "8000",
    ipv4_multiple_mpls_labels_capability         => "0",
    ipv6_multiple_mpls_labels_capability         => "0",
    mpls_labels_count_for_ipv4_mpls_route        => "1",
    mpls_labels_count_for_ipv6_mpls_route        => "1",
    noOfUserDefinedAfiSafi                       => "0",
    capability_ipv4_unicast_flowSpec             => "1",
    filter_ipv4_unicast_flowSpec                 => "1",
    capability_ipv6_unicast_flowSpec             => "1",
    filter_ipv6_unicast_flowSpec                 => "1",
    always_include_tunnel_enc_ext_community      => "false",
    ip_vrf_to_ip_vrf_type                        => "interfacefullWithUnnumberedCorefacingIRB",
    irb_interface_label                          => "16",
    irb_ipv6_address                             => "10:0:0:0:0:0:0:1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgpInterface_1_handle = $HashRef->{'bgp_handle'};

# This will create BGP IPv6 Flow-Spec on top of BGP6 Stack
print "Enabling BGP IPv6 FLOW-Spec and with configure Flow-spec on top BGP6 Stack of Topology1 !!!!!!!";
my $bgp_flow_spec_ranges_list_v6_1_status = ixiangpf::emulation_bgp_flow_spec_config ({
    mode                                               => "enable",
    fs_mode                                            => "fsv6",
    handle                                             => "$bgpInterface_1_handle",
    no_of_flowSpecRangeV6                              => "1",
    active                                             => "1",
    flowSpecName                                       => "{BGP Flow Spec 11-1}",
    fsv6_enableDestPrefix                              => "1",
    fsv6_destPrefix                                    => "1:0:0:0:0:0:1:1",
    fsv6_destPrefixLength                              => "64",
    fsv6_destPrefixOffset                              => "34",
    fsv6_enableSrcPrefix                               => "1",
    fsv6_srcPrefix                                     => "1:1:0:0:0:0:0:1",
    fsv6_srcPrefixLength                               => "80",
    fsv6_srcPrefixOffset                               => "48",
    fsv6_nextHeader                                    => "120",
    portMatch                                          => "10",
    destPortMatch                                      => "40",
    srcPortMatch                                       => "50",
    icmpTypeMatch                                      => "80",
    icmpCodeMatch                                      => "90",
    tcpFlagsMatch                                      => "(cwr)",
    ipPacketMatch                                      => "110",
    dscpMatch                                          => "10",
    fsv6_fragmentMatch                                 => "(lf)",
    fsv6_flowLabel                                     => "40",
    enable_traffic_rate                                => "1",
    trafficRate                                        => "1000",
    enable_trafficAction                               => "1",
    terminalAction                                     => "1",
    trafficActionSample                                => "1",
    enable_redirect                                    => "1",
    redirect_ext_communities_type                      => "rdIPv4",
    as_2_bytes                                         => "100",
    as_4_bytes                                         => "400",
    fsv6_ipv6                                          => "1:1:0:0:0:0:0:1",
    assigned_number_2_octets                           => "500",
    assigned_number_4_octets                           => "800",
    Cbit                                               => "1",
    nextHop                                            => "1.1.1.1",
    enable_trafficMarking                              => "1",
    dscp                                               => "10",
    fsv6_enable_redirectIPv6                           => "1",
    fsv6_redirectIPv6                                  => "1:1:0:0:0:0:0:1",
    enable_next_hop                                    => "1",
    set_next_hop                                       => "sameaslocalip",
    set_next_hop_ip_type                               => "ipv4",
    ipv4_next_hop                                      => "10.10.10.10",
    ipv6_next_hop                                      => "a:0:0:0:0:0:0:b",
    enable_origin                                      => "1",
    origin                                             => "igp",
    enable_local_preference                            => "1",
    local_preference                                   => "100",
    enable_multi_exit_discriminator                    => "1",
    multi_exit_discriminator                           => "300",
    enable_atomic_aggregate                            => "1",
    enable_aggregator_id                               => "1",
    aggregator_id                                      => "2.2.2.2",
    aggregator_as                                      => "200",
    enable_originator_id                               => "1",
    originator_id                                      => "6.6.6.6",
    enable_community                                   => "1",
    number_of_communities                              => "1",
    community_type                                     => "no_export",
    community_as_number                                => "123",
    community_last_two_octets                          => "234",
    enable_ext_community                               => "1",
    number_of_ext_communities                          => "1",
    ext_communities_type                               => "admin_as_two_octet",
    ext_communities_subtype                            => "route_target",
    ext_community_as_number                            => "123",
    ext_community_target_assigned_number_4_octets      => "1",
    ext_community_ip                                   => "1.1.1.1",
    ext_community_as_4_bytes                           => "1",
    ext_community_target_assigned_number_2_octets      => "1",
    ext_community_opaque_data                          => "aa",
    ext_community_colorCObits                          => "00",
    ext_community_colorReservedBits                    => "123",
    ext_community_colorValue                           => "1234",
    ext_community_linkBandwidth                        => "1000",
    enable_override_peer_as_set_mode                   => "1",
    as_path_set_mode                                   => "include_as_seq",
    enable_as_path_segments                            => "1",
    no_of_as_path_segments                             => "1",
    enable_as_path_segment                             => "1",
    as_path_segment_type                               => "as_set",
    number_of_as_number_in_segment                     => "1",
    as_path_segment_enable_as_number                   => "1",
    as_path_segment_as_number                          => "100",
    enable_cluster                                     => "1",
    no_of_clusters                                     => "1",
    cluster_id                                         => "1.2.3.4",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgp_flow_spec_ranges_list_v6_1_handle = $HashRef->{'bgp_flowSpecV6_handle'};

# This will create BGP6 Stack on top of IPv6 stack @PEER2 SIDE
print "Creating BGP6 Stack on top of IPv6 Stack in Topology 2\n";
my $bgp_v6_interface_2_status = ixiangpf::emulation_bgp_config ({
    mode                                         => "enable",
    active                                       => "1",
    md5_enable                                   => "0",
    md5_key                                      => "Ixia",
    handle                                       => "$ipv6_2_handle",
    ip_version                                   => "6",
    remote_ipv6_addr                             => "2000:0:0:1:0:0:0:2",
    next_hop_enable                              => "0",
    next_hop_ip                                  => "0.0.0.0",
    enable_4_byte_as                             => "0",
    local_as                                     => "0",
    local_as4                                    => "0",
    update_interval                              => "0",
    count                                        => "1",
    local_router_id                              => "193.0.0.1",
    local_router_id_step                         => "0.0.0.0",
    hold_time                                    => "90",
    neighbor_type                                => "internal",
    graceful_restart_enable                      => "0",
    restart_time                                 => "45",
    stale_time                                   => "0",
    tcp_window_size                              => "8192",
    local_router_id_enable                       => "1",
    ipv4_capability_mdt_nlri                     => "0",
    ipv4_capability_unicast_nlri                 => "1",
    ipv4_filter_unicast_nlri                     => "1",
    ipv4_capability_multicast_nlri               => "1",
    ipv4_filter_multicast_nlri                   => "0",
    ipv4_capability_mpls_nlri                    => "1",
    ipv4_filter_mpls_nlri                        => "0",
    ipv4_capability_mpls_vpn_nlri                => "1",
    ipv4_filter_mpls_vpn_nlri                    => "0",
    ipv6_capability_unicast_nlri                 => "1",
    ipv6_filter_unicast_nlri                     => "1",
    ipv6_capability_multicast_nlri               => "1",
    ipv6_filter_multicast_nlri                   => "0",
    ipv6_capability_mpls_nlri                    => "1",
    ipv6_filter_mpls_nlri                        => "0",
    ipv6_capability_mpls_vpn_nlri                => "1",
    ipv6_filter_mpls_vpn_nlri                    => "0",
    capability_route_refresh                     => "1",
    capability_route_constraint                  => "0",
    ttl_value                                    => "64",
    updates_per_iteration                        => "1",
    bfd_registration                             => "0",
    bfd_registration_mode                        => "multi_hop",
    vpls_capability_nlri                         => "1",
    vpls_filter_nlri                             => "0",
    act_as_restarted                             => "0",
    discard_ixia_generated_routes                => "0",
    flap_down_time                               => "0",
    local_router_id_type                         => "same",
    enable_flap                                  => "0",
    send_ixia_signature_with_routes              => "0",
    flap_up_time                                 => "0",
    ipv4_capability_multicast_vpn_nlri           => "0",
    ipv4_filter_multicast_vpn_nlri               => "0",
    ipv6_capability_multicast_vpn_nlri           => "0",
    ipv6_filter_multicast_vpn_nlri               => "0",
    advertise_end_of_rib                         => "0",
    configure_keepalive_timer                    => "0",
    keepalive_timer                              => "30",
    as_path_set_mode                             => "no_include",
    router_id                                    => "193.0.0.1",
    filter_link_state                            => "0",
    capability_linkstate_nonvpn                  => "0",
    bgp_ls_id                                    => "0",
    instance_id                                  => "0",
    number_of_communities                        => "1",
    enable_community                             => "0",
    number_of_ext_communities                    => "1",
    enable_ext_community                         => "0",
    enable_override_peer_as_set_mode             => "0",
    bgp_ls_as_set_mode                           => "include_as_seq",
    number_of_as_path_segments                   => "1",
    enable_as_path_segments                      => "1",
    number_of_clusters                           => "1",
    enable_cluster                               => "0",
    ethernet_segments_count                      => "0",
    filter_evpn                                  => "0",
    evpn                                         => "0",
    operational_model                            => "symmetric",
    routers_mac_or_irb_mac_address               => "00:01:04:00:00:01",
    capability_ipv4_unicast_add_path             => "0",
    capability_ipv6_unicast_add_path             => "0",
    ipv4_mpls_add_path_mode                      => "both",
    ipv6_mpls_add_path_mode                      => "both",
    ipv4_unicast_add_path_mode                   => "both",
    ipv6_unicast_add_path_mode                   => "both",
    ipv4_mpls_capability                         => "0",
    ipv6_mpls_capability                         => "0",
    capability_ipv4_mpls_add_path                => "0",
    capability_ipv6_mpls_add_path                => "0",
    custom_sid_type                              => "40",
    srgb_count                                   => "1",
    start_sid                                    => "16000",
    sid_count                                    => "8000",
    ipv4_multiple_mpls_labels_capability         => "0",
    ipv6_multiple_mpls_labels_capability         => "0",
    mpls_labels_count_for_ipv4_mpls_route        => "1",
    mpls_labels_count_for_ipv6_mpls_route        => "1",
    noOfUserDefinedAfiSafi                       => "0",
    capability_ipv4_unicast_flowSpec             => "1",
    filter_ipv4_unicast_flowSpec                 => "1",
    capability_ipv6_unicast_flowSpec             => "1",
    filter_ipv6_unicast_flowSpec                 => "1",
    always_include_tunnel_enc_ext_community      => "false",
    ip_vrf_to_ip_vrf_type                        => "interfacefullWithUnnumberedCorefacingIRB",
    irb_interface_label                          => "16",
    irb_ipv6_address                             => "10:0:0:0:0:0:0:1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgpInterface_2_handle = $HashRef->{'bgp_handle'};


# This will create BGP IPv6 Flow-Spec on top of BGP6 Stack @PEER2 SIDE
print "Enabling BGP IPv6 FLOW-Spec and with configure Flow-spec on top BGP6 Stack of Topology2 !!!!!!!";
my $bgp_flow_spec_ranges_list_v6_2_status = ixiangpf::emulation_bgp_flow_spec_config ({
    mode                                               => "enable",
    fs_mode                                            => "fsv6",
    handle                                             => "$bgpInterface_2_handle",
    no_of_flowSpecRangeV6                              => "1",
    active                                             => "1",
    flowSpecName                                       => "{BGP Flow Spec 11-1}",
    fsv6_enableDestPrefix                              => "1",
    fsv6_destPrefix                                    => "1:0:0:0:0:0:1:1",
    fsv6_destPrefixLength                              => "64",
    fsv6_destPrefixOffset                              => "34",
    fsv6_enableSrcPrefix                               => "1",
    fsv6_srcPrefix                                     => "1:1:0:0:0:0:0:1",
    fsv6_srcPrefixLength                               => "96",
    fsv6_srcPrefixOffset                               => "64",
    fsv6_nextHeader                                    => "120",
    portMatch                                          => "20",
    destPortMatch                                      => "30",
    srcPortMatch                                       => "60",
    icmpTypeMatch                                      => "70",
    icmpCodeMatch                                      => "100",
    tcpFlagsMatch                                      => "(fin)",
    ipPacketMatch                                      => "120",
    dscpMatch                                          => "20",
    fsv6_fragmentMatch                                 => "(ff)",
    fsv6_flowLabel                                     => "30",
    enable_traffic_rate                                => "1",
    trafficRate                                        => "2000",
    enable_trafficAction                               => "1",
    terminalAction                                     => "1",
    trafficActionSample                                => "1",
    enable_redirect                                    => "1",
    redirect_ext_communities_type                      => "rdIPv4",
    as_2_bytes                                         => "200",
    as_4_bytes                                         => "300",
    fsv6_ipv6                                          => "1:1:0:0:0:0:0:1",
    assigned_number_2_octets                           => "600",
    assigned_number_4_octets                           => "700",
    Cbit                                               => "1",
    nextHop                                            => "1.1.1.1",
    enable_trafficMarking                              => "1",
    dscp                                               => "20",
    fsv6_enable_redirectIPv6                           => "1",
    fsv6_redirectIPv6                                  => "1:1:0:0:0:0:0:1",
    enable_next_hop                                    => "1",
    set_next_hop                                       => "manually",
    set_next_hop_ip_type                               => "ipv6",
    ipv4_next_hop                                      => "11.11.11.11",
    ipv6_next_hop                                      => "c:0:0:0:0:0:0:d",
    enable_origin                                      => "1",
    origin                                             => "igp",
    enable_local_preference                            => "1",
    local_preference                                   => "200",
    enable_multi_exit_discriminator                    => "1",
    multi_exit_discriminator                           => "400",
    enable_atomic_aggregate                            => "1",
    enable_aggregator_id                               => "1",
    aggregator_id                                      => "3.3.3.3",
    aggregator_as                                      => "300",
    enable_originator_id                               => "1",
    originator_id                                      => "7.7.7.7",
    enable_community                                   => "1",
    number_of_communities                              => "1",
    community_type                                     => "no_export",
    community_as_number                                => "321",
    community_last_two_octets                          => "432",
    enable_ext_community                               => "1",
    number_of_ext_communities                          => "1",
    ext_communities_type                               => "admin_as_two_octet",
    ext_communities_subtype                            => "route_target",
    ext_community_as_number                            => "1",
    ext_community_target_assigned_number_4_octets      => "1",
    ext_community_ip                                   => "1.1.1.1",
    ext_community_as_4_bytes                           => "1",
    ext_community_target_assigned_number_2_octets      => "1",
    ext_community_opaque_data                          => "bb",
    ext_community_colorCObits                          => "00",
    ext_community_colorReservedBits                    => "214",
    ext_community_colorValue                           => "567",
    ext_community_linkBandwidth                        => "2000",
    enable_override_peer_as_set_mode                   => "1",
    as_path_set_mode                                   => "include_as_seq",
    enable_as_path_segments                            => "1",
    no_of_as_path_segments                             => "1",
    enable_as_path_segment                             => "1",
    as_path_segment_type                               => "as_set",
    number_of_as_number_in_segment                     => "1",
    as_path_segment_enable_as_number                   => "1",
    as_path_segment_as_number                          => "200",
    enable_cluster                                     => "1",
    no_of_clusters                                     => "1",
    cluster_id                                         => "5.6.7.8",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgp_flow_spec_ranges_list_v6_2_handle = $HashRef->{'bgp_flowSpecV6_handle'};
#####################################################################################
#Modifying the value of FLOW-SPEC Field of BGP6 PEER1 and PEER2
#####################################################################################
print "After 5 secs Modify the value of FLOW-SPEC fields of BGP6 PEER1";
sleep(5);

my $bgp_flow_spec_ranges_list_v6_1_status1 = ixiangpf::emulation_bgp_flow_spec_config ({
    mode                                               => "modify",
    fs_mode                                            => "fsv6",
    handle                                             => "$bgp_flow_spec_ranges_list_v6_1_handle",
    no_of_flowSpecRangeV6                              => "1",
    active                                             => "1",
    flowSpecName                                       => "{BGP Flow Spec 11-1}",
    fsv6_enableDestPrefix                              => "1",
    fsv6_destPrefix                                    => "1a:0b:0c:d0:e0:f0:21:31",
    fsv6_destPrefixLength                              => "54",
    fsv6_destPrefixOffset                              => "24",
    fsv6_enableSrcPrefix                               => "1",
    fsv6_srcPrefix                                     => "11:12:03:04:50:60:08:1",
    fsv6_srcPrefixLength                               => "60",
    fsv6_srcPrefixOffset                               => "24",
    fsv6_nextHeader                                    => "110",
    portMatch                                          => "110",
    destPortMatch                                      => "402",
    srcPortMatch                                       => "502",
    icmpTypeMatch                                      => "50",
    icmpCodeMatch                                      => "30",
    tcpFlagsMatch                                      => "(fin)",
    ipPacketMatch                                      => "100",
    dscpMatch                                          => "5",
    fsv6_fragmentMatch                                 => "(ff)",
    fsv6_flowLabel                                     => "20",
    enable_traffic_rate                                => "1",
    trafficRate                                        => "100",
    enable_trafficAction                               => "1",
    terminalAction                                     => "1",
    trafficActionSample                                => "1",
    enable_redirect                                    => "1",
    redirect_ext_communities_type                      => "rdIPv4",
    as_2_bytes                                         => "10",
    as_4_bytes                                         => "40",
    fsv6_ipv6                                          => "1a:b1:c0:d0:e0:f0:30:1",
    assigned_number_2_octets                           => "50",
    assigned_number_4_octets                           => "80",
    Cbit                                               => "1",
    nextHop                                            => "13.14.15.16",
    enable_trafficMarking                              => "1",
    dscp                                               => "5",
    fsv6_enable_redirectIPv6                           => "1",
    fsv6_redirectIPv6                                  => "1a:b1:d0:c0:e0:f0:0:1",
    enable_next_hop                                    => "1",
    set_next_hop                                       => "sameaslocalip",
    set_next_hop_ip_type                               => "ipv4",
    ipv4_next_hop                                      => "120.120.130.140",
    ipv6_next_hop                                      => "a:0:aa0:ff0:ee0:dd0:ccc0:bbb",
    enable_origin                                      => "1",
    origin                                             => "igp",
    enable_local_preference                            => "1",
    local_preference                                   => "10",
    enable_multi_exit_discriminator                    => "1",
    multi_exit_discriminator                           => "30",
    enable_atomic_aggregate                            => "1",
    enable_aggregator_id                               => "1",
    aggregator_id                                      => "22.22.22.22",
    aggregator_as                                      => "20",
    enable_originator_id                               => "1",
    originator_id                                      => "66.66.66.66",
    enable_community                                   => "1",
    number_of_communities                              => "1",
    community_type                                     => "no_export",
    community_as_number                                => "12",
    community_last_two_octets                          => "23",
    enable_ext_community                               => "1",
    number_of_ext_communities                          => "1",
    ext_communities_type                               => "admin_as_two_octet",
    ext_communities_subtype                            => "route_target",
    ext_community_as_number                            => "12",
    ext_community_target_assigned_number_4_octets      => "1",
    ext_community_ip                                   => "15.15.15.51",
    ext_community_as_4_bytes                           => "1",
    ext_community_target_assigned_number_2_octets      => "1",
    ext_community_opaque_data                          => "EE",
    ext_community_colorCObits                          => "11",
    ext_community_colorReservedBits                    => "13",
    ext_community_colorValue                           => "134",
    ext_community_linkBandwidth                        => "100",
    enable_override_peer_as_set_mode                   => "1",
    as_path_set_mode                                   => "include_as_seq",
    enable_as_path_segments                            => "1",
    no_of_as_path_segments                             => "1",
    enable_as_path_segment                             => "1",
    as_path_segment_type                               => "as_set",
    number_of_as_number_in_segment                     => "1",
    as_path_segment_enable_as_number                   => "1",
    as_path_segment_as_number                          => "10",
    enable_cluster                                     => "1",
    no_of_clusters                                     => "1",
    cluster_id                                         => "11.22.33.54",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}

print "After 5 secs Modify the value of FLOW-SPEC fields of BGP6 PEER2";
sleep(5);

my $bgp_flow_spec_ranges_list_v6_2_status2 = ixiangpf::emulation_bgp_flow_spec_config ({
    mode                                               => "modify",
    fs_mode                                            => "fsv6",
    handle                                             => "$bgp_flow_spec_ranges_list_v6_2_handle",
    no_of_flowSpecRangeV6                              => "1",
    active                                             => "1",
    flowSpecName                                       => "{BGP Flow Spec 11-1}",
    fsv6_enableDestPrefix                              => "1",
    fsv6_destPrefix                                    => "1aa:0bbb:ccc0:ddd0:eee0:0:1:1",
    fsv6_destPrefixLength                              => "34",
    fsv6_destPrefixOffset                              => "24",
    fsv6_enableSrcPrefix                               => "1",
    fsv6_srcPrefix                                     => "1a:e1:f0:3330:4440:550:0:1",
    fsv6_srcPrefixLength                               => "36",
    fsv6_srcPrefixOffset                               => "26",
    fsv6_nextHeader                                    => "111",
    portMatch                                          => "234",
    destPortMatch                                      => "345",
    srcPortMatch                                       => "666",
    icmpTypeMatch                                      => "7",
    icmpCodeMatch                                      => "10",
    tcpFlagsMatch                                      => "(syn)",
    ipPacketMatch                                      => "12",
    dscpMatch                                          => "2",
    fsv6_fragmentMatch                                 => "(lf)",
    fsv6_flowLabel                                     => "3",
    enable_traffic_rate                                => "1",
    trafficRate                                        => "200",
    enable_trafficAction                               => "1",
    terminalAction                                     => "1",
    trafficActionSample                                => "1",
    enable_redirect                                    => "1",
    redirect_ext_communities_type                      => "rdIPv4",
    as_2_bytes                                         => "20",
    as_4_bytes                                         => "30",
    fsv6_ipv6                                          => "1a:1b:330:4405:055:066:077:188",
    assigned_number_2_octets                           => "60",
    assigned_number_4_octets                           => "70",
    Cbit                                               => "1",
    nextHop                                            => "13.14.15.17",
    enable_trafficMarking                              => "1",
    dscp                                               => "2",
    fsv6_enable_redirectIPv6                           => "1",
    fsv6_redirectIPv6                                  => "133:1444:055:066:077:088:099:1",
    enable_next_hop                                    => "1",
    set_next_hop                                       => "manually",
    set_next_hop_ip_type                               => "ipv6",
    ipv4_next_hop                                      => "110.110.110.110",
    ipv6_next_hop                                      => "c:0ee:0ff:044:055:066:077:d",
    enable_origin                                      => "1",
    origin                                             => "igp",
    enable_local_preference                            => "1",
    local_preference                                   => "20",
    enable_multi_exit_discriminator                    => "1",
    multi_exit_discriminator                           => "40",
    enable_atomic_aggregate                            => "1",
    enable_aggregator_id                               => "1",
    aggregator_id                                      => "36.36.36.36",
    aggregator_as                                      => "30",
    enable_originator_id                               => "1",
    originator_id                                      => "75.75.75.75",
    enable_community                                   => "1",
    number_of_communities                              => "1",
    community_type                                     => "no_export",
    community_as_number                                => "32",
    community_last_two_octets                          => "43",
    enable_ext_community                               => "1",
    number_of_ext_communities                          => "1",
    ext_communities_type                               => "admin_as_two_octet",
    ext_communities_subtype                            => "route_target",
    ext_community_as_number                            => "1",
    ext_community_target_assigned_number_4_octets      => "1",
    ext_community_ip                                   => "51.51.51.51",
    ext_community_as_4_bytes                           => "1",
    ext_community_target_assigned_number_2_octets      => "1",
    ext_community_opaque_data                          => "cc",
    ext_community_colorCObits                          => "10",
    ext_community_colorReservedBits                    => "21",
    ext_community_colorValue                           => "56",
    ext_community_linkBandwidth                        => "200",
    enable_override_peer_as_set_mode                   => "1",
    as_path_set_mode                                   => "include_as_seq",
    enable_as_path_segments                            => "1",
    no_of_as_path_segments                             => "1",
    enable_as_path_segment                             => "1",
    as_path_segment_type                               => "as_set",
    number_of_as_number_in_segment                     => "1",
    as_path_segment_enable_as_number                   => "1",
    as_path_segment_as_number                          => "20",
    enable_cluster                                     => "1",
    no_of_clusters                                     => "1",
    cluster_id                                         => "55.66.77.88",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
############################################################################
# Start BGP6 protocol                                                       #
############################################################################
print "Waiting 5 seconds before starting protocol(s) ...\n";
sleep(5);
my $run_status = ixiangpf::test_control({
    action => 'start_all_protocols'
});
@status_keys = ixiangpf::status_item_keys();
$command_status = ixiangpf::status_item('status');
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
print "Waiting for 60 seconds\n";
sleep(60);

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
print "Fetching BGP aggregated statistics\n";
my $protostats = ixiangpf::emulation_bgp_info({
    handle => $bgpInterface_1_handle, 
    mode   => 'stats_per_device_group'
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
# Retrieve Learned Info                                                    #
############################################################################
print "Fetching BGP Learned Info\n";
my $bgpLearnedInfo = ixiangpf::emulation_bgp_info({
    handle => $bgpInterface_1_handle,
    mode => 'learned_info'
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

