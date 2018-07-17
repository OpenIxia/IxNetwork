################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright 1997 - 2016 by IXIA                                             #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/08/2016 - Poulomi Chatterjee - created sample                          #
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
#    This script intends to demonstrate how to use NGPF RSVPTE P2P HLP API.    #
#                                                                              #
# 1. It will create 2 RSVP-TE P2P topologies.                                  #
#      - Configure P2P Ingress LSPs in Topology 1.                             #
#      - Configure P2P Egress LSPs in Topology 2.                              #
# 2. Start all protocol.                                                       #
# 3. Retrieve protocol statistics.                                             #
# 4. Retrieve protocol learned info.                                           #
# 5. On The Fly deactivate/activate LSPs.                                      #
# 6. Configure L2-L3 traffic.                                                  #
# 7. Start the L2-L3 traffic.                                                  #
# 8. Retrieve L2-L3 traffic stats.                                             #
# 9. Stop L2-L3 traffic.                                                       #
# 10. Stop allprotocols.                                                       #
#                                                                              #
# Ixia Software:                                                               #
#    IxOS      8.10-EA                                                         #
#    IxNetwork 8.10-EA-Update(2)                                               #
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
my @port_list           = (['7/7', '7/8']);
my $ixNetwork_client    = '10.216.108.14:2666';

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
    topology_name    =>  "{RSVP-TE P2P Topology 1}",
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
    device_group_name            => "{Device Group 1}",
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
    topology_name    =>  "{RSVP-TE P2P Topology 2}",
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
    device_group_name            => "{Device Group 2}",
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
my $deviceGroup_2_handle = $HashRef->{'device_group_handle'};

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
    protocol_handle              => "$deviceGroup_2_handle",
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
# Configure RSVP Topologies in both ports as described in Description Section  #
#  above.                                                                      #
################################################################################ 

#-------------------------------------------------------------------------------#
# Configuring RSVPTE protocols in Topology 1                                    #
#-------------------------------------------------------------------------------#

#Creating RSVP-IF on top of ipv4 1 stack
print "Creating RSVP-IF on top of ipv4 1 stack\n";
my $rsvpte_if_1_status = ixiangpf::emulation_rsvp_config ({
    mode                                         => "create",
    handle                                       => "$ipv4_1_handle",
    using_gateway_ip                             => "1",
    dut_ip                                       => "20.20.20.1",
    label_space_start                            => "2000",
    label_space_end                              => "300000",
    rsvp_neighbor_active                         => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $rsvpteIf_1_handle = $HashRef->{'rsvpte_if_1_status'};

#Adding Network Group behind first DG 
print "Adding Network Group behind first DG\n";
my $network_group_1_status = ixiangpf::network_group_config ({
    protocol_handle                       => "$deviceGroup_1_handle",
    protocol_name                         => "{Network Group 1}",
    multiplier                            => "1",
    enable_device                         => "1",
    connected_to_handle                   => "$ethernet_1_handle",
    type                                  => "ipv4-prefix",
    ipv4_prefix_network_address           => "4.4.4.1",
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

# Adding second Device Group behind Network Group
print "Adding second Device Group behind Network Group\n";
my $device_group_20_status = ixiangpf::topology_config ({
    device_group_name            => "{RSVP 1}",
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
my $deviceGroup_20_handle = ixiangpf::status_item('device_group_handle');

# Adding ipv4 loopback in Second Device Group
print "Adding ipv4 loopback in Second Device Group\n"; 
my $ipv4_loopback_1_status = ixiangpf::interface_config ({
    protocol_name            => "{IPv4 Loopback 1}",
    protocol_handle          => "$deviceGroup_20_handle",
    enable_loopback          => "1",
    connected_to_handle      => "$networkGroup_1_handle",
    intf_ip_addr             => "4.4.4.1",
    intf_ip_addr_step        => "0.0.0.1",
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

# Adding RSVPTE LSPs over ipv4 Loopback
print "Adding RSVPTE LSPs over ipv4 Loopback\n";
my $rsvpte_lsps_1_status = ixiangpf::emulation_rsvp_tunnel_config ({
    mode                        => "create",
    handle                      => "$ipv4Loopback_1_handle",
    p2p_ingress_lsps_count      => "2",
    enable_p2p_egress           => "0",
    lsp_active                  => "true",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $rsvpteLsps_1_handle = ixiangpf::status_item('rsvpte_lsp_handle');

# Configure RSVPTE LSP parameters in ingress side
print "Configure RSVPTE LSP parameters in ingress side\n";

my $multivalue_1_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "5.5.5.1",
    counter_step           => "0.0.3.0",
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

my $multivalue_2_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "1",
    counter_step           => "1",
    counter_direction      => "increment",
    nest_step              => "1,1,0",
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
my $multivalue_2_handle = ixiangpf::status_item('multivalue_handle');

my $rsvp_p2_p_ingress_lsps_1_status = ixiangpf::emulation_rsvp_tunnel_config ({
    mode                                       => "create",
    handle                                     => "$rsvpteLsps_1_handle",
    rsvp_p2p_ingress_enable                    => "1",
    remote_ip                                  => "$multivalue_1_handle",
    tunnel_id                                  => "$multivalue_2_handle",
    lsp_id                                     => "101",
    using_headend_ip                           => "true",
    backup_lsp_id                              => "5000",
    enable_path_re_optimization                => "true",
    p2p_ingress_active                         => "true",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $rsvpP2PIngressLsps_1_handle = ixiangpf::status_item('rsvpte_p2p_ingress_handle');

print "Ingress Side topology Configuration complete in port 1...\n";

#---------------------------------------------------------------------------------#
# Configuring RSVPTE protocols in Topology 2                                      #
#---------------------------------------------------------------------------------#

my $multivalue_5_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "101.1.0.1",
    counter_step           => "0.0.1.0",
    counter_direction      => "increment",
    nest_step              => "0.0.0.1",
    nest_owner             => "$topology_2_handle",
    nest_enabled           => "0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_5_handle = ixiangpf::status_item('multivalue_handle');

#Creating RSVP-IF on top of ipv4 2 stack
print "Creating RSVP-IF on top of ipv4 2 stack\n";
my $rsvpte_if_2_status = ixiangpf::emulation_rsvp_config ({
    mode                                         => "create",
    handle                                       => "$ipv4_2_handle",
    using_gateway_ip                             => "1",
    dut_ip                                       => "$multivalue_5_handle",
    label_space_start                            => "1500",
    label_space_end                              => "10000",
    rsvp_neighbor_active                         => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $rsvpteIf_2_handle = ixiangpf::status_item('rsvp_if_handle');

#Adding IPv4 Prefix Pools behind first DG
print "Adding IPv4 Prefix Pools behind first DG\n";
my $network_group_6_status = ixiangpf::network_group_config ({
    protocol_handle                       => "$deviceGroup_2_handle",
    protocol_name                         => "{Network Group 2}",
    multiplier                            => "2",
    enable_device                         => "1",
    connected_to_handle                   => "$ethernet_2_handle",
    type                                  => "ipv4-prefix",
    ipv4_prefix_network_address           => "5.5.5.1",
    ipv4_prefix_network_address_step      => "0.0.3.0",
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

# Add DG2 behind IPv4 Prefix Pool
print "Add DG2 behind IPv4 Prefix Pool\n";
my $device_group_4_status = ixiangpf::topology_config ({
    device_group_name            => "{Device Group 4}",
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
my $deviceGroup_4_handle = ixiangpf::status_item('device_group_handle');

# Add ipv4 loopback in DG2
print "Add ipv4 loopback in DG2\n";

my $multivalue_6_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "5.5.5.1",
    counter_step           => "0.0.3.0",
    counter_direction      => "increment",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_6_handle = ixiangpf::status_item('multivalue_handle');

my $ipv4_loopback_2_status = ixiangpf::interface_config ({
    protocol_name            => "{IPv4 Loopback 2}",
    protocol_handle          => "$deviceGroup_4_handle",
    enable_loopback          => "1",
    connected_to_handle      => "$networkGroup_6_handle",
    intf_ip_addr             => "$multivalue_6_handle",
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

# Adding RSVP LSPs over ipv4 Loopback
print "Adding RSVP LSPs over ipv4 Loopback\n";
my $rsvpte_lsps_2_status = ixiangpf::emulation_rsvp_tunnel_config ({
    mode                        => "create",
    handle                      => "$ipv4Loopback_2_handle",
    p2p_ingress_lsps_count      => "0",
    enable_p2p_egress           => "1",
    lsp_active                  => "true",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $rsvpteLsps_2_handle = ixiangpf::status_item('rsvpte_lsp_handle');

# Configure RSVPTE LSP parameters in egress side
print "Configure RSVPTE LSP parameters in egress side\n";
my $multivalue_7_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "2001",
    counter_step           => "1",
    counter_direction      => "increment",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_7_handle = ixiangpf::status_item('multivalue_handle');

my $rsvp_p2_p_egress_lsps_1_status = ixiangpf::emulation_rsvp_tunnel_config ({
    mode                                     => "create",
    handle                                   => "$rsvpteLsps_2_handle",
    rsvp_p2p_egress_enable                   => "1",
    egress_refresh_interval                  => "30000",
    egress_timeout_multiplier                => "3",
    send_reservation_confirmation            => "false",
    enable_fixed_label_for_reservations      => "true",
    label_value                              => "$multivalue_7_handle",
    reservation_style                        => "se",
    reflect_rro                              => "true",
    egress_number_of_rro_sub_objects         => "0",
    egress_active                            => "true",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $rsvpP2PEgressLsps_1_handle = ixiangpf::status_item('rsvpte_p2p_egress_handle');

print "Egress Side topology Configuration complete in port 2...\n";

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
print "Fetching RSVP statistics\n";
# Check Stats using RSVP-IF handle
print "Check Stats using RSVP-IF handle ...\n";
my $protostats = ixiangpf::emulation_rsvp_info({
    handle => $rsvpteIf_2_handle,
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
print "Fetching RSVPTE P2P learned info\n";
# Check Learned Info
print "Check Learned Info ...\n";

print "RSVPTE P2P Interface1 learned info\n";
my $lInfo = ixiangpf::emulation_rsvp_info({
    handle => $rsvpteIf_2_handle,
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
# On The Fly Deactivate/Activate LSPs 
############################################################################
print "On The Fly Deactivate Egress Lsps\n";
my $deactivate_lsp = ixiangpf::emulation_rsvp_tunnel_config ({
   handle =>  '/topology:2/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/rsvpteLsps:1/rsvpP2PEgressLsps',
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

print "On The Fly Activate Egress Lsps\n";
my $enable_cmac = ixiangpf::emulation_rsvp_tunnel_config ({
   handle => '/topology:2/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/rsvpteLsps:1/rsvpP2PEgressLsps',
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
    emulation_src_handle    =>        [[$rsvpP2PIngressLsps_1_handle]],
    emulation_dst_handle    =>        [[$rsvpP2PEgressLsps_1_handle]],
    name                    =>        'RSVP-P2P-Traffic',
    circuit_endpoint_type   =>        'ipv4',
    rate_pps                =>        '1000',
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
