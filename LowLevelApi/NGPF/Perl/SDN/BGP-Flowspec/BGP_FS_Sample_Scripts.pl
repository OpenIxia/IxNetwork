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
#    This script intends to demonstrate how to use NGPF BGP API                #
#    It will create 2 BGP topologies, it will start the emulation and          #
#    than it will retrieve and display few statistics and modify the FLOW-SPEC #
#    field through HLT.                         						       #
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
    topology_name      => "{BGP Topology 1}",
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
    device_group_name            => "{BGP Topology 1 Router}",
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
    topology_name      => "{BGP Topology 2}",
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
    device_group_name            => "{BGP Topology 2 Router}",
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

# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group                                 
print "Creating IPv4 Stack on top of Ethernet Stack for the first Device Group\n";
my $ipv4_1_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv4 1}",
    protocol_handle                   => "$ethernet_1_handle",
    ipv4_resolve_gateway              => "1",
    ipv4_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv4_manual_gateway_mac_step      => "00.00.00.00.00.00",
    gateway                           => "200.200.200.10",
    gateway_step                      => "0.0.0.0",
    intf_ip_addr                      => "200.200.200.20",
    intf_ip_addr_step                 => "0.0.0.0",
    netmask                           => "255.255.255.0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv4_1_handle = $HashRef->{'ipv4_handle'};

# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group
print "Creating IPv4 Stack on top of Ethernet Stack for the second Device Group\n";
my $ipv4_2_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv4 2}",
    protocol_handle                   => "$ethernet_2_handle",
    ipv4_resolve_gateway              => "1",
    ipv4_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv4_manual_gateway_mac_step      => "00.00.00.00.00.00",
    gateway                           => "200.200.200.20",
    gateway_step                      => "0.0.0.0",
    intf_ip_addr                      => "200.200.200.10",
    intf_ip_addr_step                 => "0.0.0.0",
    netmask                           => "255.255.255.0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv4_2_handle = $HashRef->{'ipv4_handle'};

################################################################################
# Other protocol configurations                                                # 
################################################################################
# This will create BGP Stack on top of IPv4 stack @PEER1 SIDE
print "Creating BGP Stack on top of IPv4 Stack in Topology 1\n";    
my $bgp_v4_interface_1_status = ixiangpf::emulation_bgp_config ({
    mode                                         => "enable",
    active                                       => "1",
    md5_enable                                   => "0",
    md5_key                                      => "",
    handle                                       => "$ipv4_1_handle",
    ip_version                                   => "4",
    remote_ip_addr                               => "200.200.200.10",
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
    ipv6_filter_unicast_nlri                     => "0",
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
    routers_mac_or_irb_mac_address               => "00:01:01:00:00:01",
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
    capability_ipv6_unicast_flowSpec             => "0",
    filter_ipv6_unicast_flowSpec                 => "0",
    always_include_tunnel_enc_ext_community      => "false",
    ip_vrf_to_ip_vrf_type                        => "interfacefullWithUnnumberedCorefacingIRB",
    irb_interface_label                          => "16",
    irb_ipv4_address                             => "10.0.1.1",                                      
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgpInterface_1_handle = $HashRef->{'bgp_handle'};

# This will create BGP IPv4 Flow-Spec on top of BGP Stack
print "Enabling BGP FLOW-Spec and with configure Flow-spec on top BGP Stack of Topology1 !!!!!!!";
my $bgp_flow_spec_ranges_list_v4_1_status = ixiangpf::emulation_bgp_flow_spec_config ({
    mode                                               => "enable",
    fs_mode                                            => "fsv4",
    handle                                             => "$bgpInterface_1_handle",
    no_of_flowSpecRangeV4                              => "1",
    active                                             => "1",
    flowSpecName                                       => "{BGP Flow Spec 11-1}",
    fsv4_enableDestPrefix                              => "1",
    fsv4_destPrefix                                    => "1.1.0.1",
    fsv4_destPrefixLength                              => "24",
    fsv4_enableSrcPrefix                               => "1",
    fsv4_srcPrefix                                     => "1.0.1.1",
    fsv4_srcPrefixLength                               => "24",
    fsv4_ipProto                                       => "123",
    portMatch                                          => "345",
    destPortMatch                                      => "567",
    srcPortMatch                                       => "789",
    icmpTypeMatch                                      => "100||200",
    icmpCodeMatch                                      => "100||150-200&&>250",
    tcpFlagsMatch                                      => "(cwr)",
    dscpMatch                                          => "25",
    fsv4_fragmentMatch                                 => "(lf)",
    enable_traffic_rate                                => "1",
    trafficRate                                        => "1000",
    enable_trafficAction                               => "1",
    terminalAction                                     => "1",
    trafficActionSample                                => "1",
    enable_redirect                                    => "1",
    redirect_ext_communities_type                      => "rdIPv4",
    as_2_bytes                                         => "1",
    as_4_bytes                                         => "1",
    fsv4_ipv4                                          => "1.1.1.1",
    assigned_number_2_octets                           => "200",
    assigned_number_4_octets                           => "100",
    Cbit                                               => "1",
    nextHop                                            => "1.1.1.1",
    enable_trafficMarking                              => "1",
    dscp                                               => "20",
    enable_next_hop                                    => "1",
    set_next_hop                                       => "manually",
    set_next_hop_ip_type                               => "ipv4",
    ipv4_next_hop                                      => "100.100.100.10",
    ipv6_next_hop                                      => "0:0:0:0:0:0:0:0",
    enable_origin                                      => "1",
    origin                                             => "igp",
    enable_local_preference                            => "1",
    local_preference                                   => "200",
    enable_multi_exit_discriminator                    => "1",
    multi_exit_discriminator                           => "1234",
    enable_atomic_aggregate                            => "1",
    enable_aggregator_id                               => "1",
    aggregator_id                                      => "4.4.4.4",
    aggregator_as                                      => "10",
    enable_originator_id                               => "1",
    originator_id                                      => "3.3.3.3",
    enable_community                                   => "1",
    number_of_communities                              => "1",
    community_type                                     => "no_export",
    community_as_number                                => "123",
    community_last_two_octets                          => "1234",
    enable_ext_community                               => "1",
    number_of_ext_communities                          => "1",
    ext_communities_type                               => "admin_as_two_octet",
    ext_communities_subtype                            => "route_target",
    ext_community_as_number                            => "1",
    ext_community_target_assigned_number_4_octets      => "100",
    ext_community_ip                                   => "1.1.1.1",
    ext_community_as_4_bytes                           => "1",
    ext_community_target_assigned_number_2_octets      => "200",
    ext_community_opaque_data                          => "ff",
    ext_community_colorCObits                          => "00",
    ext_community_colorReservedBits                    => "1",
    ext_community_colorValue                           => "100",
    ext_community_linkBandwidth                        => "1000",
    enable_override_peer_as_set_mode                   => "1",
    as_path_set_mode                                   => "include_as_seq",
    enable_as_path_segments                            => "1",
    no_of_as_path_segments                             => "1",
    enable_as_path_segment                             => "1",
    as_path_segment_type                               => "as_set",
    number_of_as_number_in_segment                     => "1",
    as_path_segment_enable_as_number                   => "1",
    as_path_segment_as_number                          => "1",
    enable_cluster                                     => "1",
    no_of_clusters                                     => "1",
    cluster_id                                         => "1.1.1.1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgp_flow_spec_ranges_list_v4_1_handle = $HashRef->{'bgp_flowSpecV4_handle'};

# This will create BGP Stack on top of IPv4 stack @PEER2 SIDE
print "Creating BGP Stack on top of IPv4 Stack in Topology 2\n";
my $bgp_v4_interface_2_status = ixiangpf::emulation_bgp_config ({
    mode                                         => "enable",
    active                                       => "1",
    md5_enable                                   => "0",
    md5_key                                      => "",
    handle                                       => "$ipv4_2_handle",
    ip_version                                   => "4",
    remote_ip_addr                               => "200.200.200.20",
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
    ipv6_filter_unicast_nlri                     => "0",
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
    routers_mac_or_irb_mac_address               => "00:01:02:00:00:01",
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
    capability_ipv6_unicast_flowSpec             => "0",
    filter_ipv6_unicast_flowSpec                 => "0",
    always_include_tunnel_enc_ext_community      => "false",
    ip_vrf_to_ip_vrf_type                        => "interfacefullWithUnnumberedCorefacingIRB",
    irb_interface_label                          => "16",
    irb_ipv4_address                             => "11.0.1.1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgpInterface_2_handle = $HashRef->{'bgp_handle'};

# This will create BGP IPv4 Flow-Spec on top of BGP Stack @PEER2 SIDE
print "Enabling BGP FLOW-Spec and with configure Flow-spec on top BGP Stack of Topology2 !!!!!!!";
my $bgp_flow_spec_ranges_list_v4_2_status = ixiangpf::emulation_bgp_flow_spec_config ({
    mode                                               => "enable",
    fs_mode                                            => "fsv4",
    handle                                             => "$bgpInterface_2_handle",
    no_of_flowSpecRangeV4                              => "1",
    active                                             => "1",
    flowSpecName                                       => "{BGP Flow Spec 11-1}",
    fsv4_enableDestPrefix                              => "1",
    fsv4_destPrefix                                    => "200.1.0.0",
    fsv4_destPrefixLength                              => "24",
    fsv4_enableSrcPrefix                               => "1",
    fsv4_srcPrefix                                     => "1.0.1.1",
    fsv4_srcPrefixLength                               => "24",
    fsv4_ipProto                                       => "234",
    portMatch                                          => "456",
    destPortMatch                                      => "678",
    srcPortMatch                                       => "890",
    icmpTypeMatch                                      => ">100||<200",
    icmpCodeMatch                                      => "10||15-20&&>25",
    tcpFlagsMatch                                      => "(not)(cwr|syn)",
    dscpMatch                                          => "50",
    fsv4_fragmentMatch                                 => "(ff)",
    enable_traffic_rate                                => "1",
    trafficRate                                        => "1000",
    enable_trafficAction                               => "1",
    terminalAction                                     => "1",
    trafficActionSample                                => "1",
    enable_redirect                                    => "1",
    redirect_ext_communities_type                      => "rdIPv4",
    as_2_bytes                                         => "1",
    as_4_bytes                                         => "1",
    fsv4_ipv4                                          => "1.1.1.1",
    assigned_number_2_octets                           => "300",
    assigned_number_4_octets                           => "200",
    Cbit                                               => "1",
    nextHop                                            => "1.1.1.1",
    enable_trafficMarking                              => "1",
    dscp                                               => "10",
    enable_next_hop                                    => "1",
    set_next_hop                                       => "sameaslocalip",
    set_next_hop_ip_type                               => "ipv4",
    ipv4_next_hop                                      => "0.0.0.0",
    ipv6_next_hop                                      => "0:0:0:0:0:0:0:0",
    enable_origin                                      => "1",
    origin                                             => "igp",
    enable_local_preference                            => "1",
    local_preference                                   => "100",
    enable_multi_exit_discriminator                    => "1",
    multi_exit_discriminator                           => "100",
    enable_atomic_aggregate                            => "1",
    enable_aggregator_id                               => "1",
    aggregator_id                                      => "5.5.5.5",
    aggregator_as                                      => "100",
    enable_originator_id                               => "1",
    originator_id                                      => "6.6.6.6",
    enable_community                                   => "1",
    number_of_communities                              => "1",
    community_type                                     => "no_export",
    community_as_number                                => "1000",
    community_last_two_octets                          => "1000",
    enable_ext_community                               => "1",
    number_of_ext_communities                          => "1",
    ext_communities_type                               => "admin_as_two_octet",
    ext_communities_subtype                            => "route_target",
    ext_community_as_number                            => "1",
    ext_community_target_assigned_number_4_octets      => "100",
    ext_community_ip                                   => "1.1.1.1",
    ext_community_as_4_bytes                           => "1",
    ext_community_target_assigned_number_2_octets      => "200",
    ext_community_opaque_data                          => "ab",
    ext_community_colorCObits                          => "01",
    ext_community_colorReservedBits                    => "1",
    ext_community_colorValue                           => "200",
    ext_community_linkBandwidth                        => "2000",
    enable_override_peer_as_set_mode                   => "1",
    as_path_set_mode                                   => "include_as_seq",
    enable_as_path_segments                            => "1",
    no_of_as_path_segments                             => "1",
    enable_as_path_segment                             => "1",
    as_path_segment_type                               => "as_set",
    number_of_as_number_in_segment                     => "1",
    as_path_segment_enable_as_number                   => "1",
    as_path_segment_as_number                          => "1",
    enable_cluster                                     => "1",
    no_of_clusters                                     => "1",
    cluster_id                                         => "2.2.2.2",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgp_flow_spec_ranges_list_v4_2_handle = $HashRef->{'bgp_flowSpecV4_handle'};
#####################################################################################
#Modifying the value of FLOW-SPEC Field of BGP PEER1 and PEER2
#####################################################################################
print "After 5 secs Modify the value of FLOW-SPEC fields of BGP PEER1";
sleep(5);

my $bgp_flow_spec_ranges_list_v4_1_status1 = ixiangpf::emulation_bgp_flow_spec_config ({
    mode                                               => "modify",
    fs_mode                                            => "fsv4",
    handle                                             => "$bgp_flow_spec_ranges_list_v4_1_handle",
    no_of_flowSpecRangeV4                              => "1",
    active                                             => "1",
    flowSpecName                                       => "{BGP Flow Spec 11-1}",
    fsv4_enableDestPrefix                              => "1",
    fsv4_destPrefix                                    => "10.10.110.111",
    fsv4_destPrefixLength                              => "16",
    fsv4_enableSrcPrefix                               => "1",
    fsv4_srcPrefix                                     => "144.44.144.144",
    fsv4_srcPrefixLength                               => "16",
    fsv4_ipProto                                       => "321",
    portMatch                                          => "543",
    destPortMatch                                      => "567",
    srcPortMatch                                       => "789",
    icmpTypeMatch                                      => "10||20",
    icmpCodeMatch                                      => "100||15-20&&>25",
    tcpFlagsMatch                                      => "(syn)",
    dscpMatch                                          => "15",
    fsv4_fragmentMatch                                 => "(lf)",
    enable_traffic_rate                                => "1",
    trafficRate                                        => "100",
    enable_trafficAction                               => "1",
    terminalAction                                     => "1",
    trafficActionSample                                => "1",
    enable_redirect                                    => "1",
    redirect_ext_communities_type                      => "rdIPv4",
    as_2_bytes                                         => "1",
    as_4_bytes                                         => "1",
    fsv4_ipv4                                          => "11.11.11.11",
    assigned_number_2_octets                           => "2",
    assigned_number_4_octets                           => "10",
    Cbit                                               => "1",
    nextHop                                            => "12.12.12.12",
    enable_trafficMarking                              => "1",
    dscp                                               => "15",
    enable_next_hop                                    => "1",
    set_next_hop                                       => "manually",
    set_next_hop_ip_type                               => "ipv4",
    ipv4_next_hop                                      => "10.10.10.13",
    ipv6_next_hop                                      => "A0:b0:c0:d0:e0:f0:10:20",
    enable_origin                                      => "1",
    origin                                             => "igp",
    enable_local_preference                            => "1",
    local_preference                                   => "20",
    enable_multi_exit_discriminator                    => "1",
    multi_exit_discriminator                           => "124",
    enable_atomic_aggregate                            => "1",
    enable_aggregator_id                               => "1",
    aggregator_id                                      => "43.43.43.43",
    aggregator_as                                      => "12",
    enable_originator_id                               => "1",
    originator_id                                      => "33.33.33.33",
    enable_community                                   => "1",
    number_of_communities                              => "1",
    community_type                                     => "no_export",
    community_as_number                                => "12",
    community_last_two_octets                          => "124",
    enable_ext_community                               => "1",
    number_of_ext_communities                          => "1",
    ext_communities_type                               => "admin_as_two_octet",
    ext_communities_subtype                            => "route_target",
    ext_community_as_number                            => "1",
    ext_community_target_assigned_number_4_octets      => "10",
    ext_community_ip                                   => "14.14.14.14",
    ext_community_as_4_bytes                           => "1",
    ext_community_target_assigned_number_2_octets      => "20",
    ext_community_opaque_data                          => "EE",
    ext_community_colorCObits                          => "11",
    ext_community_colorReservedBits                    => "1",
    ext_community_colorValue                           => "10",
    ext_community_linkBandwidth                        => "100",
    enable_override_peer_as_set_mode                   => "1",
    as_path_set_mode                                   => "include_as_seq",
    enable_as_path_segments                            => "1",
    no_of_as_path_segments                             => "1",
    enable_as_path_segment                             => "1",
    as_path_segment_type                               => "as_set",
    number_of_as_number_in_segment                     => "1",
    as_path_segment_enable_as_number                   => "1",
    as_path_segment_as_number                          => "1",
    enable_cluster                                     => "1",
    no_of_clusters                                     => "1",
    cluster_id                                         => "13.13.31.31",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}

print "After 5 secs Modify the value of FLOW-SPEC fields of BGP PEER2";
sleep(5);
my $bgp_flow_spec_ranges_list_v4_2_status2 = ixiangpf::emulation_bgp_flow_spec_config ({
    mode                                               => "modify",
    fs_mode                                            => "fsv4",
    handle                                             => "$bgp_flow_spec_ranges_list_v4_2_handle",
    no_of_flowSpecRangeV4                              => "1",
    active                                             => "1",
    flowSpecName                                       => "{BGP Flow Spec 11-1}",
    fsv4_enableDestPrefix                              => "1",
    fsv4_destPrefix                                    => "20.1.0.230",
    fsv4_destPrefixLength                              => "8",
    fsv4_enableSrcPrefix                               => "1",
    fsv4_srcPrefix                                     => "14.0.51.61",
    fsv4_srcPrefixLength                               => "16",
    fsv4_ipProto                                       => "23",
    portMatch                                          => "45",
    destPortMatch                                      => "67",
    srcPortMatch                                       => "89",
    icmpTypeMatch                                      => ">10||<20",
    icmpCodeMatch                                      => "8||14-25&&>25",
    tcpFlagsMatch                                      => "(not)(fin|syn)",
    dscpMatch                                          => "5",
    fsv4_fragmentMatch                                 => "(lf)",
    enable_traffic_rate                                => "1",
    trafficRate                                        => "100",
    enable_trafficAction                               => "1",
    terminalAction                                     => "1",
    trafficActionSample                                => "1",
    enable_redirect                                    => "1",
    redirect_ext_communities_type                      => "rdIPv4",
    as_2_bytes                                         => "1",
    as_4_bytes                                         => "1",
    fsv4_ipv4                                          => "12.12.13.14",
    assigned_number_2_octets                           => "30",
    assigned_number_4_octets                           => "20",
    Cbit                                               => "1",
    nextHop                                            => "12.11.13.14",
    enable_trafficMarking                              => "1",
    dscp                                               => "11",
    enable_next_hop                                    => "1",
    set_next_hop                                       => "sameaslocalip",
    set_next_hop_ip_type                               => "ipv4",
    ipv4_next_hop                                      => "20.220.20.110",
    ipv6_next_hop                                      => "0a:0b:c0:d0:e0:f0:e0:0",
    enable_origin                                      => "1",
    origin                                             => "igp",
    enable_local_preference                            => "1",
    local_preference                                   => "10",
    enable_multi_exit_discriminator                    => "1",
    multi_exit_discriminator                           => "10",
    enable_atomic_aggregate                            => "1",
    enable_aggregator_id                               => "1",
    aggregator_id                                      => "57.85.85.59",
    aggregator_as                                      => "10",
    enable_originator_id                               => "1",
    originator_id                                      => "64.65.66.68",
    enable_community                                   => "1",
    number_of_communities                              => "1",
    community_type                                     => "no_export",
    community_as_number                                => "100",
    community_last_two_octets                          => "100",
    enable_ext_community                               => "1",
    number_of_ext_communities                          => "1",
    ext_communities_type                               => "admin_as_two_octet",
    ext_communities_subtype                            => "route_target",
    ext_community_as_number                            => "1",
    ext_community_target_assigned_number_4_octets      => "10",
    ext_community_ip                                   => "17.18.19.10",
    ext_community_as_4_bytes                           => "1",
    ext_community_target_assigned_number_2_octets      => "20",
    ext_community_opaque_data                          => "45",
    ext_community_colorCObits                          => "10",
    ext_community_colorReservedBits                    => "1",
    ext_community_colorValue                           => "20",
    ext_community_linkBandwidth                        => "200",
    enable_override_peer_as_set_mode                   => "1",
    as_path_set_mode                                   => "include_as_seq",
    enable_as_path_segments                            => "1",
    no_of_as_path_segments                             => "1",
    enable_as_path_segment                             => "1",
    as_path_segment_type                               => "as_set",
    number_of_as_number_in_segment                     => "1",
    as_path_segment_enable_as_number                   => "1",
    as_path_segment_as_number                          => "1",
    enable_cluster                                     => "1",
    no_of_clusters                                     => "1",
    cluster_id                                         => "22.23.24.25",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}


############################################################################
# Start BGP protocol                                                       #
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

