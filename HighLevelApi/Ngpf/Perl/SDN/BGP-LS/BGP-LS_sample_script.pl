################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    10/05/2016 - Shilpam Sinha - created sample                                 #
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
#    Description:                                                                           #
#    This script intends to demonstrate how to use NGPF BGP API                #
#    It will create 2 BGP topologies, it will start the emulation and          #
#    than it will retrieve and display few statistics                          #
# Ixia Software:                                                              #
#    IxOS      8.10 EA                                                         #
#    IxNetwork 8.10 EA  
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
my @chassis             = ('10.216.108.99');
my $tcl_server          = '10.216.108.99';
my @port_list           = ([ '11/5', '11/6' ]);
my $ixNetwork_client    = '10.216.104.58:8119';

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
    gateway                           => "20.20.20.1",
    gateway_step                      => "0.0.0.0",
    intf_ip_addr                      => "20.20.20.2",
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
    gateway                           => "20.20.20.2",
    gateway_step                      => "0.0.0.0",
    intf_ip_addr                      => "20.20.20.1",
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
# This will create BGP Stack on top of IPv4 stack
print "Creating BGP Stack on top of IPv4 Stack in Topology 1\n";    
my $bgp_v4_interface_1_status = ixiangpf::emulation_bgp_config ({
    mode                                              => "enable",                  
    active                                            => "1",
    md5_enable                                        => "0",                          
    handle                                            => "$ipv4_1_handle",             
    ip_version                                        => "4",
    remote_ip_addr                                    => "20.20.20.1",                 
    next_hop_enable                                   => "0",                          
    next_hop_ip                                       => "0.0.0.0",
    filter_link_state                                 => "1",                          
    capability_linkstate_nonvpn                       => "1",                          
    bgp_ls_id                                         => "300",                        
    instance_id                                       => "400",
    number_of_communities                             => "1",                          
    enable_community                                  => "0",                          
    community_type                                    => "no_export",                  
    community_as_number                               => "0",                          
    community_last_two_octets                         => "0",                          
    number_of_ext_communities                         => "1",                          
    enable_ext_community                              => "0",                          
    ext_communities_type                              => "admin_as_two_octet",         
    ext_communities_subtype                           => "route_target",               
    ext_community_as_number                           => "1",                          
    ext_community_as_4_bytes                          => "1",                          
    ext_community_ip                                  => "1.1.1.1",                    
    ext_community_opaque_data                         => "0",                          
    enable_override_peer_as_set_mode                  => "0",                          
    bgp_ls_as_set_mode                                => "include_as_seq",             
    number_of_as_path_segments                        => "1",                          
    enable_as_path_segments                           => "1",                          
    enable_as_path_segment                            => "1",                          
    number_of_as_number_in_segment                    => "1",                          
    as_path_segment_type                              => "as_set",                     
    as_path_segment_enable_as_number                  => "1",                          
    as_path_segment_as_number                         => "1",                          
    number_of_clusters                                => "1",                          
    enable_cluster                                    => "0",                          
    cluster_id                                        => "0.0.0.0",                                      
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgpInterface_1_handle = $HashRef->{'bgp_handle'};

print "Creating BGP Stack on top of IPv4 Stack in Topology 2\n";
my $bgp_v4_interface_2_status = ixiangpf::emulation_bgp_config ({
    mode                                              => "enable",
    active                                            => "1",
    md5_enable                                        => "0",
    handle                                            => "$ipv4_2_handle",
    ip_version                                        => "4",
    remote_ip_addr                                    => "20.20.20.2",
    next_hop_enable                                   => "0",
    next_hop_ip                                       => "0.0.0.0",
    filter_link_state                                 => "1",
    capability_linkstate_nonvpn                       => "1",
    bgp_ls_id                                         => "300",
    instance_id                                       => "400",
    number_of_communities                             => "1",
    enable_community                                  => "0",
    community_type                                    => "no_export",
    community_as_number                               => "0",
    community_last_two_octets                         => "0",
    number_of_ext_communities                         => "1",
    enable_ext_community                              => "0",
    ext_communities_type                              => "admin_as_two_octet",
    ext_communities_subtype                           => "route_target",
    ext_community_as_number                           => "1",
    ext_community_as_4_bytes                          => "1",
    ext_community_ip                                  => "1.1.1.1",
    ext_community_opaque_data                         => "0",
    enable_override_peer_as_set_mode                  => "0",
    bgp_ls_as_set_mode                                => "include_as_seq",
    number_of_as_path_segments                        => "1",
    enable_as_path_segments                           => "1",
    enable_as_path_segment                            => "1",
    number_of_as_number_in_segment                    => "1",
    as_path_segment_type                              => "as_set",
    as_path_segment_enable_as_number                  => "1",
    as_path_segment_as_number                         => "1",
    number_of_clusters                                => "1",
    enable_cluster                                    => "0",
    cluster_id                                        => "0.0.0.0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgpInterface_2_handle = $HashRef->{'bgp_handle'};

print "Creating OSPFv2 Stack on top of IPv4 1 stack on Topology 1";
my $ospfv2_1_status = ixiangpf::emulation_ospf_config({
    handle                                                    =>"$ipv4_1_handle",            
    area_id                                                   => "0.0.0.0",
    area_id_as_number                                         => "0",                         
    area_id_type                                              => "number",                    
    authentication_mode                                       => "null",                      
    dead_interval                                             => "40",                        
    hello_interval                                            => "10",                        
    router_interface_active                                   => "1",                         
    enable_fast_hello                                         => "0",                         
    hello_multiplier                                          => "2",                         
    max_mtu                                                   => "1500",                      
    protocol_name                                             => "OSPFv2-IF 1",             
    router_active                                             => "1",                         
    router_asbr                                               => "0",                         
    do_not_generate_router_lsa                                => "0",                         
    router_abr                                                => "0",                         
    inter_flood_lsupdate_burst_gap                            => "33",                        
    lsa_refresh_time                                          => "1800",                      
    lsa_retransmit_time                                       => "5",                         
    max_ls_updates_per_burst                                  => "1",                         
    oob_resync_breakout                                       => "0",                         
    interface_cost                                            => "10",                         
    lsa_discard_mode                                          => "1",                         
    md5_key_id                                                => "1",                         
    network_type                                              => "ptop",                      
    mode                                                      => "create",                    
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}

print "Creating OSPFv2 Stack on top of IPv4 1 stack on Topology 2";
my $ospfv2_2_status = ixiangpf::emulation_ospf_config({
    handle                                                    => "$ipv4_2_handle",
    area_id                                                   => "0.0.0.0",
    area_id_as_number                                         => "0",
    area_id_type                                              => "number",
    authentication_mode                                       => "null",
    dead_interval                                             => "40",
    hello_interval                                            => "10",
    router_interface_active                                   => "1",
    enable_fast_hello                                         => "0",
    hello_multiplier                                          => "2",
    max_mtu                                                   => "1500",
    protocol_name                                             => "OSPFv2-IF 1",
    router_active                                             => "1",
    router_asbr                                               => "0",
    do_not_generate_router_lsa                                => "0",
    router_abr                                                => "0",
    inter_flood_lsupdate_burst_gap                            => "33",
    lsa_refresh_time                                          => "1800",
    lsa_retransmit_time                                       => "5",
    max_ls_updates_per_burst                                  => "1",
    oob_resync_breakout                                       => "0",
    interface_cost                                            => "10",
    lsa_discard_mode                                          => "1",
    md5_key_id                                                => "1",
    network_type                                              => "ptop",
    mode                                                      => "create",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}

############################################
## Network Group Config
############################################
print "Creating BGP Network Group on Port 1";
my $network_group_1_status = ixiangpf::network_group_config({
    protocol_handle                      => "$deviceGroup_2_handle",
    protocol_name                        => "Direct/Static Routes",
    multiplier                           => "2",
    enable_device                        => "1",
    connected_to_handle                  => "$ethernet_2_handle",
    type                                 => "ipv4-prefix",
    ipv4_prefix_network_address          => "200.1.0.0",
    ipv4_prefix_network_address_step     => "0.1.0.0",                    
    ipv4_prefix_length                   => "24",
    ipv4_prefix_number_of_addresses      => "2",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_1_handle = $HashRef->{'network_group_handle'};

my $network_group_2_status = ixiangpf::network_group_config({
    protocol_handle                   => "$deviceGroup_2_handle",      
    protocol_name                     => "IPv6 Prefix NLRI",
    connected_to_handle               => "$ethernet_2_handle",
    type                              => "ipv6-prefix",                
    multiplier                        => "2",                          
    enable_device                     => "1",                          
    ipv6_prefix_network_address       => "3000:0:1:1:0:0:0:0",         
    ipv6_prefix_network_address_step  => "0:0:1:0:0:0:0:0",            
    ipv6_prefix_length                => "64",                         
    ipv6_prefix_number_of_addresses   => "2"                          
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_2_handle = $HashRef->{'network_group_handle'};

my $network_group_3_status = ixiangpf::network_group_config({
    protocol_handle                   => "$deviceGroup_2_handle",
    protocol_name                     => "IPv4 Prefix NLRI",
    connected_to_handle               => "$ethernet_2_handle",         
    type                              => "ipv4-prefix",                
    multiplier                        => "2",                          
    enable_device                     => "1",                          
    ipv4_prefix_network_address       => "200.1.0.0",                  
    ipv4_prefix_network_address_step  => "0.1.0.0",                    
    ipv4_prefix_length                => "24",                         
    ipv4_prefix_number_of_addresses   => "2"                          
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_3_handle = $HashRef->{'network_group_handle'};

my $network_group_4_status = ixiangpf::network_group_config({
    protocol_handle                   => "$deviceGroup_2_handle",      
    protocol_name                     => "Node/Link/Prefix NLRI",    
    multiplier                        => "1",                          
    enable_device                     => "1",                          
    type                              => "mesh",                       
    mesh_number_of_nodes              => "3",                          
    mesh_include_emulated_device      => "0",                          
    mesh_link_multiplier              => "1",                          
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
# OTF changing the valye of BGPLS ID & Instance ID                         #
############################################################################
print "Changing BGPLS ID and Instance ID On The Fly";
my $bgp_v4_interface_2_status = ixiangpf::emulation_bgp_config({
    mode                                               => "modify",
    active                                             => "1",                          
    md5_enable                                         => "0",                          
    handle                                             => "$bgpInterface_2_handle",     
    ip_version                                         => "4",                          
    bgp_ls_id                                          => "700",                        
    instance_id                                        => "800",                        
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
    handle => "$ipv4_1_handle",
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

