################################################################################
# Version 1.0    $Revision: #1 $                                               #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    10/05/2016 - Abhijit Dhar - created sample                                #
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
#    This script intends to demonstrate how to use NGPF ISIS-SR API            #
#    It will create 2 ISIS-SR topologies, it will start the emulation and      #
#    than it will retrieve and display few statistics                          #
# Ixia Software:                                                               #
#    IxOS      8.10 EA                                                         #
#    IxNetwork 8.10 EA                                                         #
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

# Using a hash reference for the HLP procedures (since they return values
# in form of hashes)
our $HashRef = {};

#Using a common variable to retain the status of each command
our $command_status  = '';
my $_result_         = '';
my $_control_status_ = '';
my $_dhcp_stats_     = '';
my @status_keys      = ();

################################################################################
# Connection to the chassis, IxNetwork Tcl Server                              #
################################################################################
my @chassis             = ('10.216.108.96');
my $tcl_server          = '10.216.108.96';
my @port_list           = ([ '4/3', '4/4' ]);
my $ixNetwork_client    = '10.216.108.113:8074';

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
print("Adding topology 1 on port 1\n");
my $topology_1_status = ixiangpf::topology_config({
    topology_name  =>    "ISIS Topology 1",
    port_handle    =>    $port_handles_list[0],
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $topology_1_handle = $HashRef->{'topology_handle'};

# Creating a device group in topology 
print("Creating device group 1 in topology 1\n"); 
my $device_group_1_status = ixiangpf::topology_config({
    topology_handle          =>    $topology_1_handle,
    device_group_name        =>    "ISIS Topology 1 Router",
    device_group_multiplier  =>    1,
    device_group_enabled     =>    1,
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_1_handle = $HashRef->{'device_group_handle'};

# Creating a topology on second port
print("Adding topology 2 on port 2\n");
my $topology_2_status = ixiangpf::topology_config({
    topology_name   =>   "ISIS Topology 2",
    port_handle     =>   $port_handles_list[1],                 
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
print("Creating device group 2 in topology 2\n");
my $device_group_2_status = ixiangpf::topology_config({
    topology_handle         =>  $topology_2_handle,
    device_group_name       =>  "ISIS Topology 2 Router",
    device_group_multiplier =>  1,
    device_group_enabled   =>  1,
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $device_group_2_handle = $HashRef->{'device_group_handle'};

################################################################################
#  Configure protocol interfaces                                               #
################################################################################
# Creating Ethernet stack for first device group
my $ethernet_1_status = ixiangpf::interface_config ({
    protocol_name           => "{Ethernet 1}",
    protocol_handle         => "$deviceGroup_1_handle",
    mtu                     => "1500",
    src_mac_addr            => "18.03.73.c7.6c.b1",
    src_mac_addr_step       => "00.00.00.00.00.00",
    vlan                    => "0",
    vlan_id_count           => "0",
    use_vpn_parameters      => "0",
    site_id                 => "0",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $ethernet_1_handle = $HashRef->{'ethernet_handle'};

# Creating Ethernet stack for second device group
my $ethernet_2_status = ixiangpf::interface_config ({
    protocol_name           => "{Ethernet 2}",
    protocol_handle         => "$device_group_2_handle",
    mtu                     => "1500",
    src_mac_addr            => "18.03.73.c7.6c.01",
    src_mac_addr_step       => "00.00.00.00.00.00",
    vlan                    => "0",
    vlan_id_count           => "0",
    use_vpn_parameters      => "0",
    site_id                 => "0",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $ethernet_2_handle = $HashRef->{'ethernet_handle'};

# Creating IPv4 stack for first device group
my $ipv4_1_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv4 1}",
    protocol_handle                   => "$ethernet_1_handle",
    ipv4_resolve_gateway              => "1",
    ipv4_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv4_manual_gateway_mac_step      => "00.00.00.00.00.00",
    gateway                           => "20.20.20.1",
    gateway_step                      => "0.0.0.0",
    intf_ip_addr                      => "20.20.20.2",
    intf_ip_addr_step                 => "0.0.0.0",
    netmask                           => "255.255.255.0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $ipv4_1_handle = $HashRef->{'ipv4_handle'};

# Creating IPv4 stack for first second device group
my $ipv4_2_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv4 2}",
    protocol_handle                   => "$ethernet_2_handle",
    ipv4_resolve_gateway              => "1",
    ipv4_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv4_manual_gateway_mac_step      => "00.00.00.00.00.00",
    gateway                           => "20.20.20.2",
    gateway_step                      => "0.0.0.0",
    intf_ip_addr                      => "20.20.20.1",
    intf_ip_addr_step                 => "0.0.0.0",
    netmask                           => "255.255.255.0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $ipv4_2_handle = $HashRef->{'ipv4_handle'};

################################################################################
# configure ISIS on topology 1                                                 #
# Following are the new SR related parameters                                  #
#   -sr_tunnel_active                                                          #
#   -number_of_sr_tunnels                                                      #
#   -sr_tunnel_description                                                     #
#   -using_head_end_node_prefix                                                #
#   -source_ipv4                                                               #
#   -source_ipv6                                                               # 
#   -number_of_segments                                                        #
#   -enable_segment                                                            #
#   -segment_type                                                              #
#   -node_system_id                                                            #
#   -neighbour_node_system_id                                                  #
################################################################################
my $isis_l3_router_1_status = ixiangpf::emulation_isis_config ({
    mode                                 => "create",
    area_authentication_mode             => "null",
    area_id                              => "490001",
    area_id_step                         => "0",
    attach_bit                           => "1",
    bfd_registration                     => "0",
    enable_host_name                     => "0",
    discard_lsp                          => "0",
    domain_authentication_mode           => "null",
    graceful_restart                     => "0",
    graceful_restart_mode                => "normal",
    graceful_restart_version             => "draft4",
    graceful_restart_restart_time        => "30",
    handle                               => "$ethernet_1_handle",
    hello_interval_level1                => "10",
    hello_interval_level2                => "10",
    intf_metric                          => "10",
    intf_type                            => "broadcast",
    l1_router_priority                   => "0",
    l2_router_priority                   => "0",
    lsp_life_time                        => "1200",
    lsp_refresh_interval                 => "900",
    max_packet_size                      => "1492",
    partition_repair                     => "0",
    overloaded                           => "0",
    routing_level                        => "L2",
    system_id                            => "64:01:00:01:00:00",
    system_id_step                       => "00:00:00:00:00:01",
    te_enable                            => "0",
    te_router_id                         => "0.0.0.0",
    te_router_id_step                    => "0.0.0.0",
    te_admin_group                       => "0",
    te_metric                            => "0",
    te_max_bw                            => "125000000",
    te_max_resv_bw                       => "125000000",
    te_unresv_bw_priority0               => "125000000",
    te_unresv_bw_priority1               => "125000000",
    te_unresv_bw_priority2               => "125000000",
    te_unresv_bw_priority3               => "125000000",
    te_unresv_bw_priority4               => "125000000",
    te_unresv_bw_priority5               => "125000000",
    te_unresv_bw_priority6               => "125000000",
    te_unresv_bw_priority7               => "125000000",
    wide_metrics                         => "1",
    enable_mt_ipv6                       => "0",
    csnp_interval                        => "10000",
    protocol_name                        => "{ISIS-L3 IF 1}",
    hello_padding                        => "1",
    router_id                            => "1.1.1.1",
    ipv6_mt_metric                       => "10",
    enable3_way_handshake                => "0",
    extended_local_circuit_id            => "1",
    level1_dead_interval                 => "30",
    level2_dead_interval                 => "30",
    enable_configured_hold_time          => "0",
    configured_hold_time                 => "30",
    auth_type                            => "none",
    auto_adjust_mtu                      => "1",
    auto_adjust_area                     => "1",
    auto_adjust_supported_protocols      => "0",
    active                               => "1",
    max_area_addresses                   => "3",
    psnp_interval                        => "2000",
    pdu_min_tx_interval                  => "5000",
    ignore_receive_md5                   => "1",
    pdu_per_burst                        => "1",
    pdu_burst_gap                        => "33",
    if_active                            => "1",
    traffic_engineering_name             => "{Traffic Engineering 1}",
    enable_sr                            => "1",
    node_prefix                          => "1.1.1.1",
    mask                                 => "32",
    d_bit                                => "0",
    s_bit                                => "0",
    redistribution                       => "up",
    r_flag                               => "0",
    n_flag                               => "1",
    p_flag                               => "0",
    e_flag                               => "0",
    v_flag                               => "0",
    l_flag                               => "0",
    ipv4_flag                            => "1",
    ipv6_flag                            => "1",
    configure_sid_index_label            => "1",
    sid_index_label                      => "1",
    algorithm                            => "0",
    srgb_range_count                     => "1",
    start_sid_label                      => "13000",
    sid_count                            => "8000",
    interface_enable_adj_sid             => "0",
    interface_adj_sid                    => "9001",
    interface_override_f_flag            => "0",
    interface_f_flag                     => "0",
    interface_b_flag                     => "0",
    interface_v_flag                     => "1",
    interface_l_flag                     => "1",
    interface_s_flag                     => "0",
    interface_weight                     => "0",
    number_of_sr_tunnels                 => "0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $isisL3_1_handle = $HashRef->{'isis_l3_handle'};

################################################################################
# Configure the fillowing ISIS-SR tunnel multivalues here                      #
# -sr_tunnel_description                                                       #
# -node_system_id 1, 2, 3, 4                                                   #
# -source_ipv4                                                                 #
# -source_ipv6                                                                 #
# -neighbour_node_system_id 1, 2, 3, 4                                         #
################################################################################
# sr_tunnel_description
my $sr_tunnel_description_status = ixiangpf::multivalue_config ({
    pattern             => "string",
    string_pattern      => "SR Tunnel ID {Inc:0,1}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $sr_tunnel_description_handle = $HashRef->{'multivalue_handle'};

# source_ipv4    
my $source_ipv4_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "101.0.0.1",
    counter_step           => "0.0.0.1",
    counter_direction      => "increment",
    nest_step              => "0.1.0.0",
    nest_owner             => "$topology_2_handle",
    nest_enabled           => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $source_ipv4_handle = $HashRef->{'multivalue_handle'};

# source_ipv6
my $source_ipv6_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "1000:0:1:0:0:0:0:1",
    counter_step           => "0:0:0:0:0:0:0:1",
    counter_direction      => "increment",
    nest_step              => "0:0:0:1::",
    nest_owner             => "$topology_2_handle",
    nest_enabled           => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $source_ipv6_handle = $HashRef->{'multivalue_handle'};

# node_system_id 1    
my $node_system_id1_status = ixiangpf::multivalue_config ({
    pattern                 => "counter",
    counter_start           => "65:01:00:01:00:00",
    counter_step            => "00:00:00:01:00:00",
    counter_direction       => "increment",
    nest_step               => "00:01:00:00:00:00",
    nest_owner              => "$topology_2_handle",
    nest_enabled            => "1",
    overlay_value           => "AB:01:00:00:00:01,AB:01:00:00:00:01",
    overlay_value_step      => "AB:01:00:00:00:01,AB:01:00:00:00:01",
    overlay_index           => "1,2",
    overlay_index_step      => "0,0",
    overlay_count           => "1,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $node_system_id1_handle = $HashRef->{'multivalue_handle'};

# node_system_id 2    
my $node_system_id2_status = ixiangpf::multivalue_config ({
    pattern                 => "counter",
    counter_start           => "69:01:00:01:00:00",
    counter_step            => "00:00:00:01:00:00",
    counter_direction       => "increment",
    nest_step               => "00:01:00:00:00:00",
    nest_owner              => "$topology_2_handle",
    nest_enabled            => "1",
    overlay_value           => "AB:01:00:00:00:02,AB:01:00:00:00:02",
    overlay_value_step      => "AB:01:00:00:00:02,AB:01:00:00:00:02",
    overlay_index           => "1,2",
    overlay_index_step      => "0,0",
    overlay_count           => "1,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $node_system_id2_handle = $HashRef->{'multivalue_handle'};

# node_system_id 3    
my $node_system_id3_status = ixiangpf::multivalue_config ({
    pattern                 => "counter",
    counter_start           => "6A:01:00:01:00:00",
    counter_step            => "00:00:00:01:00:00",
    counter_direction       => "increment",
    nest_step               => "00:01:00:00:00:00",
    nest_owner              => "$topology_2_handle",
    nest_enabled            => "1",
    overlay_value           => "AB:01:00:00:00:05,AB:01:00:00:00:05",
    overlay_value_step      => "AB:01:00:00:00:05,AB:01:00:00:00:05",
    overlay_index           => "1,2",
    overlay_index_step      => "0,0",
    overlay_count           => "1,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $node_system_id3_handle = $HashRef->{'multivalue_handle'};

# node_system_id 4    
my $node_system_id4_status = ixiangpf::multivalue_config ({
    pattern                 => "counter",
    counter_start           => "6B:01:00:01:00:00",
    counter_step            => "00:00:00:01:00:00",
    counter_direction       => "increment",
    nest_step               => "00:01:00:00:00:00",
    nest_owner              => "$topology_2_handle",
    nest_enabled            => "1",
    overlay_value           => "AB:01:00:00:00:06,AB:01:00:00:00:08",
    overlay_value_step      => "AB:01:00:00:00:06,AB:01:00:00:00:08",
    overlay_index           => "1,2",
    overlay_index_step      => "0,0",
    overlay_count           => "1,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $node_system_id4_handle = $HashRef->{'multivalue_handle'};

# neighbour_node_system_id 1
my $neighbour_node_system_id1_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "65:01:00:01:00:00",
    counter_step           => "00:00:00:01:00:00",
    counter_direction      => "increment",
    nest_step              => "00:01:00:00:00:00",
    nest_owner             => "$topology_2_handle",
    nest_enabled           => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $neighbour_node_system_id1_handle = $HashRef->{'multivalue_handle'};

# neighbour_node_system_id 2
my $neighbour_node_system_id2_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "69:01:00:01:00:00",
    counter_step           => "00:00:00:01:00:00",
    counter_direction      => "increment",
    nest_step              => "00:01:00:00:00:00",
    nest_owner             => "$topology_2_handle",
    nest_enabled           => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $neighbour_node_system_id2_handle = $HashRef->{'multivalue_handle'};

# neighbour_node_system_id 3
my $neighbour_node_system_id3_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "6A:01:00:01:00:00",
    counter_step           => "00:00:00:01:00:00",
    counter_direction      => "increment",
    nest_step              => "00:01:00:00:00:00",
    nest_owner             => "$topology_2_handle",
    nest_enabled           => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $neighbour_node_system_id3_handle = $HashRef->{'multivalue_handle'};

# neighbour_node_system_id 4
my $neighbour_node_system_id4_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "6B:01:00:01:00:00",
    counter_step           => "00:00:00:01:00:00",
    counter_direction      => "increment",
    nest_step              => "00:01:00:00:00:00",
    nest_owner             => "$topology_2_handle",
    nest_enabled           => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $neighbour_node_system_id4_handle = $HashRef->{'multivalue_handle'};

################################################################################
# configure ISIS on topology 2                                                 #
# Following are the new SR related parameters                                  #
#   -sr_tunnel_active                                                          #  
#   -number_of_sr_tunnels                                                      #
#   -sr_tunnel_description                                                     #
#   -using_head_end_node_prefix                                                #
#   -source_ipv4                                                               #
#   -source_ipv6                                                               #
#   -number_of_segments                                                        #
#   -enable_segment                                                            #
#   -segment_type                                                              #
#   -node_system_id                                                            #
#   -neighbour_node_system_id                                                  #
################################################################################
my $isis_l3_router_2_status = ixiangpf::emulation_isis_config ({
    mode                                 => "create",
    area_authentication_mode             => "null",
    area_id                              => "490001",
    area_id_step                         => "0",
    attach_bit                           => "1",
    bfd_registration                     => "0",
    enable_host_name                     => "0",
    discard_lsp                          => "0",
    domain_authentication_mode           => "null",
    graceful_restart                     => "0",
    graceful_restart_mode                => "normal",
    graceful_restart_version             => "draft4",
    graceful_restart_restart_time        => "30",
    handle                               => "$ethernet_2_handle",
    hello_interval_level1                => "10",
    hello_interval_level2                => "10",
    intf_metric                          => "10",
    intf_type                            => "broadcast",
    l1_router_priority                   => "0",
    l2_router_priority                   => "0",
    lsp_life_time                        => "1200",
    lsp_refresh_interval                 => "900",
    max_packet_size                      => "1492",
    partition_repair                     => "0",
    overloaded                           => "0",
    routing_level                        => "L2",
    system_id                            => "65:01:00:01:00:00",
    system_id_step                       => "00:00:00:00:00:01",
    te_enable                            => "0",
    te_router_id                         => "0.0.0.0",
    te_router_id_step                    => "0.0.0.0",
    te_admin_group                       => "0",
    te_metric                            => "0",
    te_max_bw                            => "125000000",
    te_max_resv_bw                       => "125000000",
    te_unresv_bw_priority0               => "125000000",
    te_unresv_bw_priority1               => "125000000",
    te_unresv_bw_priority2               => "125000000",
    te_unresv_bw_priority3               => "125000000",
    te_unresv_bw_priority4               => "125000000",
    te_unresv_bw_priority5               => "125000000",
    te_unresv_bw_priority6               => "125000000",
    te_unresv_bw_priority7               => "125000000",
    wide_metrics                         => "0",
    enable_mt_ipv6                       => "0",
    csnp_interval                        => "10000",
    protocol_name                        => "{ISIS-L3 IF 2}",
    hello_padding                        => "1",
    router_id                            => "1.1.1.2",
    ipv6_mt_metric                       => "10",
    enable3_way_handshake                => "0",
    extended_local_circuit_id            => "1",
    level1_dead_interval                 => "30",
    level2_dead_interval                 => "30",
    enable_configured_hold_time          => "0",
    configured_hold_time                 => "30",
    auth_type                            => "none",
    auto_adjust_mtu                      => "1",
    auto_adjust_area                     => "1",
    auto_adjust_supported_protocols      => "0",
    active                               => "1",
    max_area_addresses                   => "3",
    psnp_interval                        => "2000",
    pdu_min_tx_interval                  => "5000",
    ignore_receive_md5                   => "1",
    pdu_per_burst                        => "1",
    pdu_burst_gap                        => "33",
    if_active                            => "1",
    traffic_engineering_name             => "{Traffic Engineering 2}",
    enable_sr                            => "0",
    node_prefix                          => "1.1.1.2",
    mask                                 => "32",
    d_bit                                => "0",
    s_bit                                => "0",
    redistribution                       => "up",
    r_flag                               => "0",
    n_flag                               => "1",
    p_flag                               => "0",
    e_flag                               => "0",
    v_flag                               => "0",
    l_flag                               => "0",
    ipv4_flag                            => "1",
    ipv6_flag                            => "1",
    configure_sid_index_label            => "1",
    sid_index_label                      => "0",
    algorithm                            => "0",
    srgb_range_count                     => "1",
    start_sid_label                      => "14000",
    sid_count                            => "8000",
    interface_enable_adj_sid             => "0",
    interface_adj_sid                    => "9001",
    interface_override_f_flag            => "0",
    interface_f_flag                     => "0",
    interface_b_flag                     => "0",
    interface_v_flag                     => "1",
    interface_l_flag                     => "1",
    interface_s_flag                     => "0",
    interface_weight                     => "0",
    sr_tunnel_active                     => "1",
    number_of_sr_tunnels                 => "2",
    sr_tunnel_description                => "$sr_tunnel_description_handle",
    using_head_end_node_prefix           => "1",
    source_ipv4                          => "$source_ipv4_handle",
    source_ipv6                          => "$source_ipv6_handle",
    number_of_segments                   => "4",
    enable_segment                       => "1 1 1 1",
    segment_type                         => "node node node node",
    node_system_id                       => "$node_system_id1_handle $node_system_id2_handle $node_system_id3_handle $node_system_id4_handle",
    neighbour_node_system_id             => "$neighbour_node_system_id1_handle $neighbour_node_system_id2_handle $neighbour_node_system_id3_handle $neighbour_node_system_id4_handle",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}

################################################################################
# Adding network topology (Topology 1)                                         #
################################################################################
my $network_group_1_status = ixiangpf::network_group_config ({
    protocol_handle                   => "$deviceGroup_1_handle",
    protocol_name                     => "{Network Group 1}",
    multiplier                        => "1",
    enable_device                     => "1",
    type                              => "grid",
    grid_col                          => "3",
    grid_row                          => "3",
    grid_include_emulated_device      => "0",
    grid_link_multiplier              => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_1_handle = $HashRef->{'network_group_handle'};

################################################################################
# Create the following network group multivalues                               #
# -si_adj_sid                                                                  #
# -from_ip                                                                     #
# -to_ip                                                                       #
# -from_ipv6                                                                   #
# -to_ipv6                                                                     #
# -router_system_id                                                            #
# -pseudo_node_node_prefix                                                     #
# -pseudo_node_rtrcap_id                                                       #
# -pseudo_node_sid_index_label                                                 #
# -grid_router_id                                                              #
# -pseudo_node_route_ipv4_sid_index_label                                      #
################################################################################ 
# si_adj_sid attribute
my $si_adj_sid_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "9001",
    counter_step           => "1",
    counter_direction      => "increment",
    nest_step              => "1,0",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $si_adj_sid_handle = $HashRef->{'multivalue_handle'};

# from_ip    
my $from_ip_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "31.0.10.1",
    counter_step           => "0.0.1.0",
    counter_direction      => "increment",
    nest_step              => "0.0.0.1,0.1.0.0",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $from_ip_handle = $HashRef->{'multivalue_handle'};

# to_ip    
my $to_ip_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "31.0.10.2",
    counter_step           => "0.0.1.0",
    counter_direction      => "increment",
    nest_step              => "0.0.0.1,0.1.0.0",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $to_ip_handle = $HashRef->{'multivalue_handle'};

# from_ipv6    
my $from_ipv6_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "aa:0:0:0:0:0:0:1",
    counter_step           => "0:0:0:0:0:0:1:0",
    counter_direction      => "increment",
    nest_step              => "::1,0:0:0:1::",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $from_ipv6_handle = $HashRef->{'multivalue_handle'};

# to_ipv6    
my $to_ipv6_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "aa:0:0:0:0:0:0:2",
    counter_step           => "0:0:0:0:0:0:1:0",
    counter_direction      => "increment",
    nest_step              => "::1,0:0:1::",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $to_ipv6_handle = $HashRef->{'multivalue_handle'};

# router_system_id    
my $router_system_id_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "AB:01:00:00:00:01",
    counter_step           => "00:00:00:00:00:01",
    counter_direction      => "increment",
    nest_step              => "00:00:00:00:00:01,00:01:00:00:00:00",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $router_system_id_handle = $HashRef->{'multivalue_handle'};

# pseudo_node_node_prefix    
my $pseudo_node_node_prefix_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "1.1.1.1",
    counter_step           => "0.0.0.1",
    counter_direction      => "increment",
    nest_step              => "0.0.0.1,0.1.0.0",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $pseudo_node_node_prefix_handle = $HashRef->{'multivalue_handle'};

# pseudo_node_rtrcap_id    
my $pseudo_node_rtrcap_id_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "1.1.1.1",
    counter_step           => "0.0.0.1",
    counter_direction      => "increment",
    nest_step              => "0.0.0.1,0.1.0.0",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $pseudo_node_rtrcap_id_handle = $HashRef->{'multivalue_handle'};

# pseudo_node_sid_index_label
my $pseudo_node_sid_index_label_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "0",
    counter_step           => "1",
    counter_direction      => "increment",
    nest_step              => "1,0",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $pseudo_node_sid_index_label_handle = $HashRef->{'multivalue_handle'};

# grid_router_id    
my $grid_router_id_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "201.1.0.0",
    counter_step           => "0.1.0.0",
    counter_direction      => "increment",
    nest_step              => "0.0.0.1,0.1.0.0",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $grid_router_id_handle = $HashRef->{'multivalue_handle'};

# pseudo_node_route_ipv4_sid_index_label 
my $pseudo_node_route_ipv4_sid_index_label_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "1",
    counter_step           => "1",
    counter_direction      => "increment",
    nest_step              => "1,0",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $pseudo_node_route_ipv4_sid_index_label_handle = $HashRef->{'multivalue_handle'};

# grid_ipv6_router_id    
my $grid_ipv6_router_id_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "3000:0:1:1:0:0:0:0",
    counter_step           => "0:0:0:1:0:0:0:0",
    counter_direction      => "increment",
    nest_step              => "::1,0:0:1::",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $grid_ipv6_router_id_handle = $HashRef->{'multivalue_handle'};

# pseudo_node_route_ipv6_sid_index_label
my $pseudo_node_route_ipv6_sid_index_label_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "1",
    counter_step           => "1",
    counter_direction      => "increment",
    nest_step              => "1,0",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
my $pseudo_node_route_ipv6_sid_index_label_handle = $HashRef->{'multivalue_handle'};

################################################################################
# Configuring the ISIS-SR network topology                                     #
################################################################################
my $network_group_2_status = ixiangpf::emulation_isis_network_group_config ({
    handle                                                => "$networkGroup_1_handle",
    mode                                                  => "modify",
    connected_to_handle                                   => "$ethernet_1_handle",
    router_system_id                                      => "$router_system_id_handle",
    enable_mt_ipv6                                        => "0",
    ipv6_mt_metric                                        => "10",
    enable_wide_metric                                    => "1",
    router_te                                             => "0",
    router_id                                             => "0.0.0.0",
    node_active                                           => "1",
    admin_group                                           => "0",
    metric_level                                          => "0",
    max_bw                                                => "125000000",
    max_resv_bw                                           => "125000000",
    bw_priority0                                          => "125000000",
    bw_priority1                                          => "125000000",
    bw_priority2                                          => "125000000",
    bw_priority3                                          => "125000000",
    bw_priority4                                          => "125000000",
    bw_priority5                                          => "125000000",
    bw_priority6                                          => "125000000",
    bw_priority7                                          => "125000000",
    from_ip                                               => "$from_ip_handle",
    to_ip                                                 => "$to_ip_handle",
    enable_ip                                             => "1",
    subnet_prefix_length                                  => "24",
    from_ipv6                                             => "$from_ipv6_handle",
    to_ipv6                                               => "$to_ipv6_handle",
    enable_ipv6                                           => "0",
    subnet_ipv6_prefix_length                             => "64",
    to_node_active                                        => "1",
    to_node_link_metric                                   => "10",
    from_node_active                                      => "1",
    from_node_link_metric                                 => "10",
    sim_topo_active                                       => "1",
    sim_topo_enable_host_name                             => "0",
    sim_topo_ipv4_node_route_count                        => "0",
    sim_topo_ipv6_node_route_count                        => "0",
    grid_router_id                                        => "$grid_router_id_handle",
    grid_router_ip_pfx_len                                => "16",
    grid_stub_per_router                                  => "1",
    grid_router_route_step                                => "1",
    grid_router_metric                                    => "0",
    grid_router_origin                                    => "stub",
    grid_router_up_down_bit                               => "0",
    grid_node_step                                        => "256",
    grid_router_active                                    => "1",
    grid_ipv6_router_id                                   => "$grid_ipv6_router_id_handle",
    grid_ipv6_router_ip_pfx_len                           => "64",
    grid_ipv6_stub_per_router                             => "1",
    grid_ipv6_router_route_step                           => "1",
    grid_ipv6_router_metric                               => "0",
    grid_ipv6_router_origin                               => "stub",
    grid_ipv6_router_up_down_bit                          => "0",
    grid_ipv6_node_step                                   => "256",
    link_type                                             => "pttopt",
    si_enable_adj_sid                                     => "0",
    si_adj_sid                                            => "$si_adj_sid_handle",
    si_b_flag                                             => "0",
    si_override_f_flag                                    => "0",
    si_f_flag                                             => "0",
    si_v_flag                                             => "1",
    si_l_flag                                             => "1",
    si_s_flag                                             => "0",
    si_weight                                             => "0",
    pseudo_node_enable_sr                                 => "1",
    pseudo_node_node_prefix                               => "$pseudo_node_node_prefix_handle",
    pseudo_node_mask                                      => "32",
    pseudo_node_rtrcap_id                                 => "$pseudo_node_rtrcap_id_handle",
    pseudo_node_d_bit                                     => "0",
    pseudo_node_s_bit                                     => "0",
    pseudo_node_redistribution                            => "up",
    pseudo_node_r_flag                                    => "0",
    pseudo_node_n_flag                                    => "1",
    pseudo_node_p_flag                                    => "0",
    pseudo_node_e_flag                                    => "0",
    pseudo_node_v_flag                                    => "0",
    pseudo_node_l_flag                                    => "0",
    pseudo_node_ipv4_flag                                 => "1",
    pseudo_node_ipv6_flag                                 => "1",
    pseudo_node_configure_sid_index_label                 => "1",
    pseudo_node_sid_index_label                           => "$pseudo_node_sid_index_label_handle",
    pseudo_node_algorithm                                 => "0",
    pseudo_node_srgb_range_count                          => "1",
    pseudo_node_start_sid_label                           => "16000",
    pseudo_node_sid_count                                 => "8000",
    pseudo_node_route_ipv4_r_flag                         => "0",
    pseudo_node_route_ipv4_n_flag                         => "0",
    pseudo_node_route_ipv4_p_flag                         => "0",
    pseudo_node_route_ipv4_e_flag                         => "0",
    pseudo_node_route_ipv4_v_flag                         => "0",
    pseudo_node_route_ipv4_l_flag                         => "0",
    pseudo_node_route_ipv4_configure_sid_index_label      => "1",
    pseudo_node_route_ipv4_sid_index_label                => "$pseudo_node_route_ipv4_sid_index_label_handle",
    pseudo_node_route_ipv6_r_flag                         => "0",
    pseudo_node_route_ipv6_n_flag                         => "0",
    pseudo_node_route_ipv6_p_flag                         => "0",
    pseudo_node_route_ipv6_e_flag                         => "0",
    pseudo_node_route_ipv6_v_flag                         => "0",
    pseudo_node_route_ipv6_l_flag                         => "0",
    pseudo_node_route_ipv6_configure_sid_index_label      => "1",
    pseudo_node_route_ipv6_sid_index_label                => "$pseudo_node_route_ipv6_sid_index_label_handle",
    grid_ipv6_router_active                               => "0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my     $error = $HashRef->{'log'};
    print  "Error: $error";
    return "FAILED - $error";
}
  
################################################################################
# Start all configured protocols                                               #
################################################################################
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

################################################################################
# Fetch and print stats                                                        #
################################################################################
print "Fetching learned info\n";
my $handle = $isisL3_1_handle;
$run_status = ixiangpf::emulation_isis_info({
    handle  => $handle, 
    mode    => "stats",
});

@status_keys = ixiangpf::status_item_keys();
for my $key (@status_keys) {
    my $value = ixiangpf::status_item($key);
    print("$key = $value\n");
}

################################################################################
# Configuring traffic items                                                    #
################################################################################
# Set traffic source and destination endpoints
my $sources      = "/topology:2/deviceGroup:1/isisL3Router:1/isisSRTunnelList";
my $destination1 = "/topology:1/deviceGroup:1/ethernet:1/ipv4:1";

# Set tracking options
my $track_by1 = "trackingenabled0";
my $track_by2 = "mplsMplsLabelValue0";
my $track_by3 = "mplsMplsLabelValue1";
my $track_by4 = "mplsMplsLabelValue2";
my $track_by5 = "mplsMplsLabelValue3";

print "Configuring L2-L3 traffic\n";
$run_status = ixiangpf::traffic_config({
    mode                 => "create",
    traffic_generator    => "ixnetwork_540",
    endpointset_count    => "1",
    emulation_src_handle => $sources,
    emulation_dst_handle => "$destination1",
    track_by             => "$track_by1 $track_by2 $track_by3 $track_by4 $track_by5",
    rate_pps             => 1000,
    frame_size           => 512,
});

############################################################################
# Start L2-L3 traffic                                                      #
############################################################################
print "Starting Traffic...\n";
$run_status = ixiangpf::traffic_control({
    action            => "run",
    traffic_generator => "ixnetwork_540",
    type              => "{l23 l47}",
});

# Run traffic for 30 seconds
print("Run traffic for 30 seconds\n");
sleep(30);

############################################################################
# Retrieve L2-L3 traffic stats                                             #
############################################################################
$run_status = ixiangpf::traffic_stats({ 
    mode              => "all",
    traffic_generator => "ixnetwork_540",
    measure_mode      => "mixed",
});

@status_keys = ixiangpf::status_item_keys();
for my $key (@status_keys) {
    my $value = ixiangpf::status_item($key);
    print("$key = $value\n");
}

############################################################################
# Stop L2-L3 traffic started earlier                                       #
# Stop application traffic started earlier                                 #
############################################################################
print "Stopping Traffic...\n";
$run_status = ::ixiangpf::traffic_control({
    action            => "stop",
    traffic_generator => "ixnetwork_540",
    type              => "{l23 l47}",
});
   
############################################################################
# Stop all protocols                                                       #
############################################################################
print "Stopping all protocol(s) ...\n";
$run_status = ixiangpf::test_control({
    action => "stop_all_protocols",
});
print "!!!!! TEST ENDS !!!!!\n";

