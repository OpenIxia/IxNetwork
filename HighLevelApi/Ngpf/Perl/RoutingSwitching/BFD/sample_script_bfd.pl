#################################################################################
# Version 1    $Revision: #1 $
# $Author: cm $
#
#    Copyright © 1997 - 2016 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    12/05/2016 Dhiraj Khandelwal - created sample
#
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
################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample configures BFD over IPv6 and IPv6 Loopback.			       #
#     Here we perform:			                                               #
#			-Start All Protocols 											   #
#			-Fetch Stats And Learned Info 									   #
#			-Perform action start and stop bfd interfaces 					   #
#                                                                              #
################################################################################
# Source all libraries in the beginning
use warnings;
use strict;
use bignum;
use Carp;
use Cwd 'abs_path';

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
my @chassis             = ('10.216.108.130');
my $tcl_server          = '10.216.108.130';
my @port_list           = ([ '12/1', '12/2' ]);
my $ixNetwork_client    = '10.216.108.86:8237';

print "Connecting to Chassis and Client\n";
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

my $port_0 = $port_handles_list[0];
my $port_1 = $port_handles_list[1];
################################################################################
# END - Connect to the chassis
################################################################################


################################################################################
## Topology, Ethernet and IPv6 Configuration
################################################################################

my $topology_1_status = ixiangpf::topology_config ({
    topology_name      => "{Topology 1}",
    port_handle        => $port_0,
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $topology_1_handle = ixiangpf::status_item('topology_handle');

my $device_group_1_status = ixiangpf::topology_config ({
    topology_handle              => "$topology_1_handle",
    device_group_name            => "{Device Group 1}",
    device_group_multiplier      => "3",
    device_group_enabled         => "1",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_1_handle = ixiangpf::status_item('device_group_handle');

my $multivalue_1_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "00.11.01.00.00.01",
    counter_step           => "00.00.00.00.00.01",
    counter_direction      => "increment",
    nest_step              => "00.00.01.00.00.00",
    nest_owner             => "$topology_1_handle",
    nest_enabled           => "1",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $multivalue_1_handle = ixiangpf::status_item('multivalue_handle');

my $ethernet_1_status = ixiangpf::interface_config ({
    protocol_name                => "{Ethernet 1}",
    protocol_handle              => "$deviceGroup_1_handle",
    mtu                          => "1500",
    src_mac_addr                 => "$multivalue_1_handle",
    vlan                         => "1",
    vlan_id                      => "1",
    vlan_id_step                 => "1",
    vlan_id_count                => "1",
    vlan_tpid                    => "0x8100",
    vlan_user_priority           => "0",
    vlan_user_priority_step      => "0",
    use_vpn_parameters           => "0",
    site_id                      => "0",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}

@status_keys = ixiangpf::status_item_keys();
my $ethernet_1_handle = ixiangpf::status_item('ethernet_handle');

my $multivalue_2_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "2000:0:0:1:0:0:0:2",
    counter_step           => "0:0:0:1:0:0:0:0",
    counter_direction      => "increment",
    nest_step              => "0:0:0:1:0:0:0:0",
    nest_owner             => "$topology_1_handle",
    nest_enabled           => "1",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $multivalue_2_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_3_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "2000:0:0:1:0:0:0:1",
    counter_step           => "0:0:0:1:0:0:0:0",
    counter_direction      => "increment",
    nest_step              => "0:0:0:1:0:0:0:0",
    nest_owner             => "$topology_1_handle",
    nest_enabled           => "1",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $multivalue_3_handle = ixiangpf::status_item('multivalue_handle');

my $ipv6_1_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv6 1}",
    protocol_handle                   => "$ethernet_1_handle",
    ipv6_multiplier                   => "1",
    ipv6_resolve_gateway              => "1",
    ipv6_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step      => "00.00.00.00.00.00",
    ipv6_gateway                      => "$multivalue_3_handle",
    ipv6_intf_addr                    => "$multivalue_2_handle",
    ipv6_prefix_length                => "64",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}

@status_keys = ixiangpf::status_item_keys();
my $ipv6_1_handle = ixiangpf::status_item('ipv6_handle');

my $multivalue_4_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "192.0.0.1",
    counter_step           => "0.0.0.1",
    counter_direction      => "increment",
    nest_step              => "0.1.0.0",
    nest_owner             => "$topology_1_handle",
    nest_enabled           => "1",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $multivalue_4_handle = ixiangpf::status_item('multivalue_handle');


############################################################
## BFD Configuration
############################################################
my $bfdv6_interface_1_status = ixiangpf::emulation_bfd_config ({
    count                           => "1",
    echo_rx_interval                => "0",
    echo_timeout                    => "1500",
    echo_tx_interval                => "0",
    control_plane_independent       => "0",
    enable_demand_mode              => "0",
    flap_tx_interval                => "0",
    handle                          => "$ipv6_1_handle",
    min_rx_interval                 => "1000",
    mode                            => "create",
    detect_multiplier               => "3",
    poll_interval                   => "0",
    router_id                       => "$multivalue_4_handle",
    tx_interval                     => "1000",
    configure_echo_source_ip        => "0",
    echo_source_ip6                 => "0:0:0:0:0:0:0:0",
    ip_diff_serv                    => "0",
    interface_active                => "1",
    interface_name                  => "{BFDv6 IF 1}",
    router_active                   => "1",
    router_name                     => "{BfdRouter 1}",
    session_count                   => "1",
    enable_auto_choose_source       => "1",
    enable_learned_remote_disc      => "1",
    ip_version                      => "6",
    session_discriminator           => "1",
    session_discriminator_step      => "0",
    remote_discriminator            => "1",
    remote_discriminator_step       => "0",
    source_ipv6_addr                => "0:0:0:0:0:0:0:0",
    remote_ipv6_addr                => "2000:0:0:1:0:0:0:1",
    remote_ipv6_addr_step           => "0:0:0:1:0:0:0:0",
    hop_mode                        => "singlehop",
    session_active                  => "1",
    session_name                    => "{BFDv6 Session 1}",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $bfdv6Interface_1_handle = ixiangpf::status_item('bfd_v6_interface_handle');

my $device_group_2_status = ixiangpf::topology_config ({
    device_group_name            => "{Device Group 2}",
    device_group_multiplier      => "1",
    device_group_enabled         => "1",
    device_group_handle          => "$deviceGroup_1_handle",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_2_handle = ixiangpf::status_item('device_group_handle');

my $multivalue_5_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "2222:0:0:0:0:0:0:1",
    counter_step           => "0:0:0:0:0:0:0:1",
    counter_direction      => "increment",
    nest_step              => "0:0:0:0:0:0:0:1,0:0:0:1:0:0:0:0",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $multivalue_5_handle = ixiangpf::status_item('multivalue_handle');

my $ipv6_loopback_1_status = ixiangpf::interface_config ({
    protocol_name            => "{IPv6 Loopback 1}",
    protocol_handle          => "$deviceGroup_2_handle",
    enable_loopback          => "1",
    connected_to_handle      => "$ethernet_1_handle",
    ipv6_multiplier          => "1",
    ipv6_intf_addr           => "$multivalue_5_handle",
    ipv6_prefix_length       => "128",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}

@status_keys = ixiangpf::status_item_keys();
my $ipv6Loopback_1_handle = ixiangpf::status_item('ipv6_loopback_handle');

my $bfdv6_interface_2_status = ixiangpf::emulation_bfd_config ({
    count                           => "1",
    echo_rx_interval                => "0",
    echo_timeout                    => "1500",
    echo_tx_interval                => "0",
    control_plane_independent       => "0",
    enable_demand_mode              => "0",
    flap_tx_interval                => "0",
    handle                          => "$ipv6Loopback_1_handle",
    min_rx_interval                 => "1000",
    mode                            => "create",
    detect_multiplier               => "3",
    poll_interval                   => "0",
    router_id                       => "$multivalue_4_handle",
    tx_interval                     => "1000",
    configure_echo_source_ip        => "0",
    echo_source_ip6                 => "0:0:0:0:0:0:0:0",
    ip_diff_serv                    => "0",
    interface_active                => "1",
    interface_name                  => "{BFDv6 IF 2}",
    router_active                   => "1",
    router_name                     => "{BfdRouter 2}",
    session_count                   => "1",
    enable_auto_choose_source       => "1",
    enable_learned_remote_disc      => "1",
    ip_version                      => "6",
    session_discriminator           => "1",
    session_discriminator_step      => "0",
    remote_discriminator            => "1",
    remote_discriminator_step       => "0",
    source_ipv6_addr                => "0:0:0:0:0:0:0:0",
    remote_ipv6_addr                => "2222:0:1:0:0:0:0:1",
    remote_ipv6_addr_step           => "0:0:0:0:0:0:0:1",
    hop_mode                        => "multiplehop",
    session_active                  => "1",
    session_name                    => "{BFDv6 Session 2}",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $bfdv6Interface_2_handle = ixiangpf::status_item('bfd_v6_interface_handle');

my $topology_2_status = ixiangpf::topology_config ({
    topology_name      => "{Topology 2}",
    port_handle        => $port_1,
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $topology_2_handle = ixiangpf::status_item('topology_handle');

my $device_group_3_status = ixiangpf::topology_config ({
    topology_handle              => "$topology_2_handle",
    device_group_name            => "{Device Group 3}",
    device_group_multiplier      => "3",
    device_group_enabled         => "1",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_3_handle = ixiangpf::status_item('device_group_handle');

my $multivalue_6_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "00.12.01.00.00.01",
    counter_step           => "00.00.00.00.00.01",
    counter_direction      => "increment",
    nest_step              => "00.00.01.00.00.00",
    nest_owner             => "$topology_2_handle",
    nest_enabled           => "1",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $multivalue_6_handle = ixiangpf::status_item('multivalue_handle');

my $ethernet_2_status = ixiangpf::interface_config ({
    protocol_name                => "{Ethernet 2}",
    protocol_handle              => "$deviceGroup_3_handle",
    mtu                          => "1500",
    src_mac_addr                 => "$multivalue_6_handle",
    vlan                         => "1",
    vlan_id                      => "1",
    vlan_id_step                 => "1",
    vlan_id_count                => "1",
    vlan_tpid                    => "0x8100",
    vlan_user_priority           => "0",
    vlan_user_priority_step      => "0",
    use_vpn_parameters           => "0",
    site_id                      => "0",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}

@status_keys = ixiangpf::status_item_keys();
my $ethernet_2_handle = ixiangpf::status_item('ethernet_handle');

my $multivalue_7_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "2000:0:0:1:0:0:0:1",
    counter_step           => "0:0:0:1:0:0:0:0",
    counter_direction      => "increment",
    nest_step              => "0:0:0:1:0:0:0:0",
    nest_owner             => "$topology_2_handle",
    nest_enabled           => "1",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $multivalue_7_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_8_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "2000:0:0:1:0:0:0:2",
    counter_step           => "0:0:0:1:0:0:0:0",
    counter_direction      => "increment",
    nest_step              => "0:0:0:1:0:0:0:0",
    nest_owner             => "$topology_2_handle",
    nest_enabled           => "1",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $multivalue_8_handle = ixiangpf::status_item('multivalue_handle');

my $ipv6_2_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv6 2}",
    protocol_handle                   => "$ethernet_2_handle",
    ipv6_multiplier                   => "1",
    ipv6_resolve_gateway              => "1",
    ipv6_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step      => "00.00.00.00.00.00",
    ipv6_gateway                      => "$multivalue_8_handle",
    ipv6_intf_addr                    => "$multivalue_7_handle",
    ipv6_prefix_length                => "64",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}

@status_keys = ixiangpf::status_item_keys();
my $ipv6_2_handle = ixiangpf::status_item('ipv6_handle');

my $multivalue_9_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "194.0.0.1",
    counter_step           => "0.0.0.1",
    counter_direction      => "increment",
    nest_step              => "0.1.0.0",
    nest_owner             => "$topology_2_handle",
    nest_enabled           => "1",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $multivalue_9_handle = ixiangpf::status_item('multivalue_handle');

my $bfdv6_interface_3_status = ixiangpf::emulation_bfd_config ({
    count                           => "1",
    echo_rx_interval                => "0",
    echo_timeout                    => "1500",
    echo_tx_interval                => "0",
    control_plane_independent       => "0",
    enable_demand_mode              => "0",
    flap_tx_interval                => "0",
    handle                          => "$ipv6_2_handle",
    min_rx_interval                 => "1000",
    mode                            => "create",
    detect_multiplier               => "3",
    poll_interval                   => "0",
    router_id                       => "$multivalue_9_handle",
    tx_interval                     => "1000",
    configure_echo_source_ip        => "0",
    echo_source_ip6                 => "0:0:0:0:0:0:0:0",
    ip_diff_serv                    => "0",
    interface_active                => "1",
    interface_name                  => "{BFDv6 IF 3}",
    router_active                   => "1",
    router_name                     => "{BfdRouter 3}",
    session_count                   => "1",
    enable_auto_choose_source       => "1",
    enable_learned_remote_disc      => "1",
    ip_version                      => "6",
    session_discriminator           => "1",
    session_discriminator_step      => "0",
    remote_discriminator            => "1",
    remote_discriminator_step       => "0",
    source_ipv6_addr                => "0:0:0:0:0:0:0:0",
    remote_ipv6_addr                => "2000:0:0:1:0:0:0:2",
    remote_ipv6_addr_step           => "0:0:0:1:0:0:0:0",
    hop_mode                        => "singlehop",
    session_active                  => "1",
    session_name                    => "{BFDv6 Session 3}",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $bfdv6Interface_3_handle = ixiangpf::status_item('bfd_v6_interface_handle');

my $device_group_4_status = ixiangpf::topology_config ({
    device_group_name            => "{Device Group 4}",
    device_group_multiplier      => "1",
    device_group_enabled         => "1",
    device_group_handle          => "$deviceGroup_3_handle",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_4_handle = ixiangpf::status_item('device_group_handle');

my $multivalue_10_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "2222:0:1:0:0:0:0:1",
    counter_step           => "0:0:0:0:0:0:0:1",
    counter_direction      => "increment",
    nest_step              => "0:0:0:0:0:0:0:1,0:0:0:1:0:0:0:0",
    nest_owner             => "$deviceGroup_3_handle,$topology_2_handle",
    nest_enabled           => "0,1",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $multivalue_10_handle = ixiangpf::status_item('multivalue_handle');

my $ipv6_loopback_2_status = ixiangpf::interface_config ({
    protocol_name            => "{IPv6 Loopback 2}",
    protocol_handle          => "$deviceGroup_4_handle",
    enable_loopback          => "1",
    connected_to_handle      => "$ethernet_2_handle",
    ipv6_multiplier          => "1",
    ipv6_intf_addr           => "$multivalue_10_handle",
    ipv6_prefix_length       => "128",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}

@status_keys = ixiangpf::status_item_keys();
my $ipv6Loopback_2_handle = ixiangpf::status_item('ipv6_loopback_handle');

my $bfdv6_interface_4_status = ixiangpf::emulation_bfd_config ({
    count                           => "1",
    echo_rx_interval                => "0",
    echo_timeout                    => "1500",
    echo_tx_interval                => "0",
    control_plane_independent       => "0",
    enable_demand_mode              => "0",
    flap_tx_interval                => "0",
    handle                          => "$ipv6Loopback_2_handle",
    min_rx_interval                 => "1000",
    mode                            => "create",
    detect_multiplier               => "3",
    poll_interval                   => "0",
    router_id                       => "$multivalue_9_handle",
    tx_interval                     => "1000",
    configure_echo_source_ip        => "0",
    echo_source_ip6                 => "0:0:0:0:0:0:0:0",
    ip_diff_serv                    => "0",
    interface_active                => "1",
    interface_name                  => "{BFDv6 IF 4}",
    router_active                   => "1",
    router_name                     => "{BfdRouter 4}",
    session_count                   => "1",
    enable_auto_choose_source       => "1",
    enable_learned_remote_disc      => "1",
    ip_version                      => "6",
    session_discriminator           => "1",
    session_discriminator_step      => "0",
    remote_discriminator            => "1",
    remote_discriminator_step       => "0",
    source_ipv6_addr                => "0:0:0:0:0:0:0:0",
    remote_ipv6_addr                => "2222:0:0:0:0:0:0:1",
    remote_ipv6_addr_step           => "0:0:0:0:0:0:0:1",
    hop_mode                        => "multiplehop",
    session_active                  => "1",
    session_name                    => "{BFDv6 Session 4}",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();
my $bfdv6Interface_4_handle = ixiangpf::status_item('bfd_v6_interface_handle');


my $ipv6_3_status = ixiangpf::interface_config ({
    protocol_handle                   => "/globals",
    ns_on_linkup                      => "0",
    single_ns_per_gateway             => "1",
    ipv6_send_ns_rate                 => "200",
    ipv6_send_ns_interval             => "1000",
    ipv6_send_ns_max_outstanding      => "400",
    ipv6_send_ns_scale_mode           => "port",
    ipv6_attempt_enabled              => "0",
    ipv6_attempt_rate                 => "200",
    ipv6_attempt_interval             => "1000",
    ipv6_attempt_scale_mode           => "port",
    ipv6_diconnect_enabled            => "0",
    ipv6_disconnect_rate              => "200",
    ipv6_disconnect_interval          => "1000",
    ipv6_disconnect_scale_mode        => "port",
    ipv6_re_send_ns_on_link_up        => "true",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();

my $ethernet_3_status = ixiangpf::interface_config ({
    protocol_handle                     => "/globals",
    ethernet_attempt_enabled            => "0",
    ethernet_attempt_rate               => "200",
    ethernet_attempt_interval           => "1000",
    ethernet_attempt_scale_mode         => "port",
    ethernet_diconnect_enabled          => "0",
    ethernet_disconnect_rate            => "200",
    ethernet_disconnect_interval        => "1000",
    ethernet_disconnect_scale_mode      => "port",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
    handle_error();
}
@status_keys = ixiangpf::status_item_keys();



print(q(Waiting 60 seconds before starting protocol(s) ...));
sleep(60);

#############################################################################
#Starting All Protocols
#############################################################################   

print(q(Starting all protocol(s) ...));
ixiahlt::test_control({action => 'start_all_protocols'});
if (ixiahlt::status_item('status') != 1) {
    print('ixiahlt::traffic_control');
}
sleep(60);

#############################################################################
#Fetching aggregate stats using emulation_bfd_info
#############################################################################    
my $status  = ::ixiangpf::emulation_bfd_info({
mode => "aggregate",
handle => "/topology:1/deviceGroup:1/ethernet:1/ipv6:1/bfdv6Interface:1" });

@status_keys = ixiangpf::status_item_keys();
print "==================================================================\n";
print "@status_keys\n";
print "==================================================================\n";
if (ixiahlt::status_item('status') != 1) {
    print('error in getting stats');
} else {
     foreach (@status_keys) {
        my $myKey = $_;
        my $value = ixiangpf::status_item($myKey);
        print "emulation_bfd_info_key = $myKey\n";
        print "emulation_bfd_info_val = $value\n";
}

my $conf_up = ixiangpf::status_item("Port1.aggregate.sessions_configured_up");
print "Session Conigured Up : $conf_up";
}

##############################################################################
#Fetching Learned Info using emulation_bfd_info
##############################################################################   
my $info_status  = ::ixiangpf::emulation_bfd_info({
    mode => "learned_info",
    handle => "/topology:1/deviceGroup:1/ethernet:1/ipv6:1/bfdv6Interface:1" });

@status_keys = ixiangpf::status_item_keys();
if (ixiahlt::status_item('status') != 1) {
    print('error in getting learned');
} else {
    foreach (@status_keys) {
	    my $myKey = $_;
	    my $value = ixiangpf::status_item($myKey);
	    print "emulation_bgp_info_key = $myKey\n";
	    print "emulation_bgp_info_val = $value\n";
    }
}

print "Learned info available";

###############################################################################
#Applying action Stop on BFD interfaces using emulation_bfd_control
###############################################################################

my $stop_status  = ::ixiangpf::emulation_bfd_control({
mode => "stop",
handle => "/topology:1/deviceGroup:1/ethernet:1/ipv6:1/bfdv6Interface:1" });

sleep(10);

################################################################################
#Starting BFD interface suing emulation_bfd_control
################################################################################    
my $start_status  = ::ixiangpf::emulation_bfd_control({
mode => "start",
handle => "/topology:1/deviceGroup:1/ethernet:1/ipv6:1/bfdv6Interface:1" });

sleep(10);
print "TEST COMPLETED";
