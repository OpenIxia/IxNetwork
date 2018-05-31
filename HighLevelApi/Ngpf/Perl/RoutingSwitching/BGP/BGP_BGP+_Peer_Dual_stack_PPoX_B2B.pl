#################################################################################
# Version 1    $Revision: #1 $
# $Author: cm $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    08-15-2013 Mchakravarthy - created sample
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
#    This sample configures BGP and BGP+ Peers over PPoX Client and Server     #
#    and retreives session stats                                               #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################
# Source all libraries in the beginning
use warnings;
use strict;
use bignum;
use Carp;
use Cwd 'abs_path';

# use lib where the HLPAPI files are located
# It is typically: "C:/Program Files/Ixia/hltapi/<version_number>/TclScripts/lib/hltapi/library/common/ixia_hl_lib-<version>"
# For Ex:
# use lib "C:/Program Files/Ixia/hltapi/4.70.0.213/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.10";
use lib "C:/Program Files/Ixia/hltapi/4.80.0.52/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.20";
use lib "C:/Program Files/Ixia/hltapi/4.80.0.52/TclScripts/lib/hltapi/library/common/ixiangpf/perl";

use ixiahlt;
use ixiaixn;
use ixiangpf;

# Declare the Chassis IP address and the Ports that will be used
my $test_name              = "BGP_BGP+_Peer_4_DG_IPv4_IPv6_B2B";
my @chassis                = ('10.206.27.55');
my $tcl_server             = "127.0.0.1";
my @port_list              = ("10/1", "10/2");
my $ixnetwork_tcl_server   = "127.0.0.1";
my $wait_time              = 5;
my $test_dir_path          = abs_path();

################################################################################
# Function to catch the errors and print it on the screen             .        #
################################################################################
sub catch_error {
    if (ixiangpf::status_item('status') != 1) {
        print ("n#################################################### n");
        print ("ERROR: n$test_name : ". ixiangpf::status_item('log'));
        print ("n#################################################### n");
        die ("ERROR: n$test_name : Please check values and the port handles!!!");
    }
}

# Initialize values for HLPAPI scripts
my $_result_               = '';
my $status                 = '';
my $port_handle            = '';
my @status_keys            = ();
my %status_keys            = ();
my @portHandleList         = ();

################################################################################
# START - Connect to the chassis
################################################################################

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect

$_result_ = ixiahlt::connect ( {
    mode                   => "connect",
    device                 => \@chassis,
    ixnetwork_tcl_server   => $ixnetwork_tcl_server,
    tcl_server             => $tcl_server,
    port_list              => \@port_list,
});


&catch_error();

@status_keys = ixiahlt::status_item_keys();
$port_handle = ixiahlt::status_item('port_handle');
$status = ixiahlt::status_item('status');

# Assign portHandleList with port handles values
foreach my $port (@port_list) {
    $port_handle = ixiahlt::status_item("port_handle.$chassis_ip.$port");
    push(@portHandleList, $port_handle);
}

my $port_0 = $portHandleList[0];
my $port_1 = $portHandleList[1];

print ("\nIxia port handles are @portHandleList ...\n");
print ("End connecting to chassis ...\n");

################################################################################
# END - Connect to the chassis
################################################################################

#########################################################################################################################
##                                                     Topology 1 Config                                               ##
#########################################################################################################################

my @status_keys = ();

my $topology_1_status = ixiangpf::topology_config ({
    topology_name      => 'Topology 1',
    port_handle        => $port_0,
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $topology_1_handle = ixiangpf::status_item('topology_handle');

#########################################################################################################################
##                                                     Device Group 1 Config                                           ##
#########################################################################################################################

my $device_group_1_status = ixiangpf::topology_config ({
    topology_handle              => $topology_1_handle,
    device_group_name            => 'Device Group 1',
    device_group_multiplier      => '1',
    device_group_enabled         => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_1_handle = ixiangpf::status_item('device_group_handle');

############################################
## Ethernet Config
############################################

my $multivalue_1_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '00.11.01.00.00.01',
    counter_step           => '00.00.00.00.00.01',
    counter_direction      => 'increment',
    nest_step              => '00.00.01.00.00.00',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_1_handle = ixiangpf::status_item('multivalue_handle');

my $ethernet_1_status = ixiangpf::interface_config ({
    protocol_name                => 'Ethernet 1',
    protocol_handle              => $deviceGroup_1_handle,
    mtu                          => '1500',
    src_mac_addr                 => $multivalue_1_handle,
    vlan                         => '0',
    vlan_id                      => '1',
    vlan_id_step                 => '0',
    vlan_id_count                => '1',
    vlan_tpid                    => '0x8100',
    vlan_user_priority           => '0',
    vlan_user_priority_step      => '0',
    use_vpn_parameters           => '0',
    site_id                      => '0',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $ethernet_1_handle = ixiangpf::status_item('ethernet_handle');

############################################
## PPoX Server Config
############################################

my $multivalue_2_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '1',
    counter_step           => '0',
    counter_direction      => 'increment',
    nest_step              => '1',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '0',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_2_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_3_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '1.1.1.2',
    counter_step           => '0.0.1.0',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_3_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_4_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '1.1.1.1',
    counter_step           => '0.0.1.0',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_4_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_5_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '11:0:0:0:0:0:0:11',
    counter_step           => '0:0:1:0:0:0:0:0',
    counter_direction      => 'increment',
    nest_step              => '0:1:0:0:0:0:0:0',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_5_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_6_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '11:0:0:0:0:0:0:11',
    counter_step           => '0:0:0:1:0:0:0:0',
    counter_direction      => 'increment',
    nest_step              => '0:0:1:0:0:0:0:0',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_6_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_7_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '11:0:0:0:0:0:0:1',
    counter_step           => '0:0:0:1:0:0:0:0',
    counter_direction      => 'increment',
    nest_step              => '0:0:1:0:0:0:0:0',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_7_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_8_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '2001:0:0:0:0:0:0:1',
    counter_step           => '0:0:0:1:0:0:0:0',
    counter_direction      => 'increment',
    nest_step              => '0:0:1:0:0:0:0:0',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_8_handle = ixiangpf::status_item('multivalue_handle');

my $pppoxserver_1_status = ixiangpf::pppox_config ({
    port_role                            => 'network',
    handle                               => $ethernet_1_handle,
    protocol_name                        => 'PPPoX Server 1',
    enable_mru_negotiation               => '0',
    desired_mru_rate                     => '1492',
    enable_max_payload                   => '0',
    server_ipv6_ncp_configuration        => 'clientmay',
    server_ipv4_ncp_configuration        => 'clientmay',
    lcp_enable_accm                      => '0',
    lcp_accm                             => 'ffffffff',
    num_sessions                         => '1',
    auth_req_timeout                     => '10',
    config_req_timeout                   => '10',
    echo_req                             => $multivalue_2_handle,
    echo_rsp                             => '1',
    ip_cp                                => 'dual_stack',
    ipcp_req_timeout                     => '10',
    max_auth_req                         => '20',
    max_terminate_req                    => '3',
    password                             => 'password',
    chap_secret                          => 'secret',
    username                             => 'user',
    chap_name                            => 'user',
    mode                                 => 'add',
    auth_mode                            => 'none',
    echo_req_interval                    => '10',
    max_configure_req                    => '3',
    max_ipcp_req                         => '3',
    ac_name                              => 'ixia',
    enable_domain_group_map              => '0',
    enable_server_signal_iwf             => '0',
    enable_server_signal_loop_char       => '0',
    enable_server_signal_loop_encap      => '0',
    enable_server_signal_loop_id         => '0',
    ipv6_pool_prefix_len                 => '48',
    ipv6_pool_prefix                     => $multivalue_5_handle,
    ipv6_pool_addr_prefix_len            => '64',
    ppp_local_iid                        => $multivalue_7_handle,
    ppp_local_ip                         => $multivalue_4_handle,
    ppp_local_ip_step                    => '0.0.0.1',
    ppp_peer_iid                         => $multivalue_6_handle,
    ppp_peer_ip                          => $multivalue_3_handle,
    ppp_peer_ip_step                     => '0.0.0.1',
    send_dns_options                     => '0',
    dns_server_list                      => $multivalue_8_handle,
    server_dns_options                   => 'disable_extension',
    server_dns_primary_address           => '10.10.10.10',
    server_dns_secondary_address         => '11.11.11.11',
    server_netmask_options               => 'disable_extension',
    server_netmask                       => '255.255.255.0',
    server_wins_options                  => 'disable_extension',
    server_wins_primary_address          => '10.10.10.10',
    server_wins_secondary_address        => '11.11.11.11',
    accept_any_auth_value                => '0',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $pppoxserver_1_handle = ixiangpf::status_item('pppox_server_handle');

############################################
## BGP Peer Config
############################################

my $multivalue_9_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '192.0.0.1',
    counter_step           => '0.0.0.1',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_9_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_10_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => 'true',
    counter_step           => 'false',
    counter_direction      => 'increment',
    nest_step              => 'true',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '0',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_10_handle = ixiangpf::status_item('multivalue_handle');

my $bgp_ipv4_peer_1_status = ixiangpf::emulation_bgp_config ({
    mode                                    => 'enable',
    md5_enable                              => '0',
    handle                                  => $pppoxserver_1_handle,
    remote_ip_addr                          => '1.1.1.2',
    remote_addr_step                        => '0.0.0.0',
    enable_4_byte_as                        => '0',
    local_as                                => '1',
    update_interval                         => '0',
    count                                   => '1',
    local_router_id                         => $multivalue_9_handle,
    hold_time                               => '90',
    neighbor_type                           => 'external',
    graceful_restart_enable                 => '0',
    restart_time                            => '45',
    stale_time                              => '0',
    tcp_window_size                         => '8192',
    local_router_id_enable                  => '1',
    ipv4_capability_mdt_nlri                => 'false',
    ipv4_capability_unicast_nlri            => 'true',
    ipv4_filter_unicast_nlri                => $multivalue_10_handle,
    ipv4_capability_multicast_nlri          => 'true',
    ipv4_filter_multicast_nlri              => 'false',
    ipv4_capability_mpls_nlri               => 'true',
    ipv4_filter_mpls_nlri                   => 'false',
    ipv4_capability_mpls_vpn_nlri           => 'true',
    ipv4_filter_mpls_vpn_nlri               => 'false',
    ipv6_capability_unicast_nlri            => 'true',
    ipv6_filter_unicast_nlri                => 'false',
    ipv6_capability_multicast_nlri          => 'true',
    ipv6_filter_multicast_nlri              => 'false',
    ipv6_capability_mpls_nlri               => 'true',
    ipv6_filter_mpls_nlri                   => 'false',
    ipv6_capability_mpls_vpn_nlri           => 'true',
    ipv6_filter_mpls_vpn_nlri               => 'false',
    ttl_value                               => '64',
    updates_per_iteration                   => '1',
    bfd_registration                        => '0',
    bfd_registration_mode                   => 'multi_hop',
    vpls_capability_nlri                    => 'true',
    vpls_filter_nlri                        => 'false',
    act_as_restarted                        => '0',
    discard_ixia_generated_routes           => '0',
    flap_down_time                          => '0',
    local_router_id_type                    => 'same',
    enable_flap                             => '0',
    send_ixia_signature_with_routes         => '0',
    flap_up_time                            => '0',
    vpls_enable_next_hop                    => '0',
    vpls_next_hop                           => '0.0.0.0',
    ipv4_capability_multicast_vpn_nlri      => 'false',
    ipv4_filter_multicast_vpn_nlri          => 'false',
    ipv6_capability_multicast_vpn_nlri      => 'false',
    ipv6_filter_multicast_vpn_nlri          => 'false',
    advertise_end_of_rib                    => '0',
    configure_keepalive_timer               => '0',
    keepalive_timer                         => '30',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $bgpIpv4Peer_1_handle = ixiangpf::status_item('bgp_handle');

############################################
## BGP+ Peer Config
############################################

my $multivalue_11_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '192.0.0.1',
    counter_step           => '0.0.0.1',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_11_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_12_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => 'true',
    counter_step           => 'false',
    counter_direction      => 'increment',
    nest_step              => 'true',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '0',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_12_handle = ixiangpf::status_item('multivalue_handle');

my $bgp_ipv6_peer_1_status = ixiangpf::emulation_bgp_config ({
    mode                                    => 'enable',
    md5_enable                              => '0',
    handle                                  => $pppoxserver_1_handle,
    remote_ipv6_addr                        => '11:0:0:0:1100:0:0:11',
    remote_addr_step                        => '0:0:0:0:0:0:0:0',
    enable_4_byte_as                        => '0',
    local_as                                => '3',
    update_interval                         => '0',
    count                                   => '1',
    local_router_id                         => $multivalue_11_handle,
    hold_time                               => '90',
    neighbor_type                           => 'external',
    graceful_restart_enable                 => '0',
    restart_time                            => '45',
    stale_time                              => '0',
    tcp_window_size                         => '8192',
    local_router_id_enable                  => '1',
    ipv4_capability_mdt_nlri                => 'false',
    ipv4_capability_unicast_nlri            => 'true',
    ipv4_filter_unicast_nlri                => 'false',
    ipv4_capability_multicast_nlri          => 'true',
    ipv4_filter_multicast_nlri              => 'false',
    ipv4_capability_mpls_nlri               => 'true',
    ipv4_filter_mpls_nlri                   => 'false',
    ipv4_capability_mpls_vpn_nlri           => 'true',
    ipv4_filter_mpls_vpn_nlri               => 'false',
    ipv6_capability_unicast_nlri            => 'true',
    ipv6_filter_unicast_nlri                => $multivalue_12_handle,
    ipv6_capability_multicast_nlri          => 'true',
    ipv6_filter_multicast_nlri              => 'false',
    ipv6_capability_mpls_nlri               => 'true',
    ipv6_filter_mpls_nlri                   => 'false',
    ipv6_capability_mpls_vpn_nlri           => 'true',
    ipv6_filter_mpls_vpn_nlri               => 'false',
    ttl_value                               => '64',
    updates_per_iteration                   => '1',
    bfd_registration                        => '0',
    bfd_registration_mode                   => 'multi_hop',
    vpls_capability_nlri                    => 'true',
    vpls_filter_nlri                        => 'false',
    act_as_restarted                        => '0',
    discard_ixia_generated_routes           => '0',
    flap_down_time                          => '0',
    local_router_id_type                    => 'same',
    enable_flap                             => '0',
    send_ixia_signature_with_routes         => '0',
    flap_up_time                            => '0',
    vpls_enable_next_hop                    => '0',
    vpls_next_hop                           => '0.0.0.0',
    ipv4_capability_multicast_vpn_nlri      => 'false',
    ipv4_filter_multicast_vpn_nlri          => 'false',
    ipv6_capability_multicast_vpn_nlri      => 'false',
    ipv6_filter_multicast_vpn_nlri          => 'false',
    advertise_end_of_rib                    => '0',
    configure_keepalive_timer               => '0',
    keepalive_timer                         => '30',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $bgpIpv6Peer_1_handle = ixiangpf::status_item('bgp_handle');
my $session_handle = ixiangpf::status_item("handle");

############################################
## Network Group Config
############################################

my $multivalue_13_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '3000:0:1:1:0:0:0:0',
    counter_step           => '0:0:0:1:0:0:0:0',
    counter_direction      => 'increment',
    nest_step              => '0:0:0:0:0:0:0:1,0:0:1:0:0:0:0:0',
    nest_owner             => $deviceGroup_1_handle,$topology_1_handle,
    nest_enabled           => '0,1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_13_handle = ixiangpf::status_item('multivalue_handle');

my $network_group_1_status = ixiangpf::network_group_config ({
    protocol_handle                      => $deviceGroup_1_handle,
    connected_to_handle                  => $pppoxserver_1_handle,
    type                                 => 'ipv6-prefix',
    multiplier                           => '1',
    enable_device                        => '1',
    ipv6_prefix_network_address          => $multivalue_13_handle,
    ipv6_prefix_length                   => '64',
    ipv6_prefix_number_of_addresses      => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $networkGroup_1_handle = ixiangpf::status_item('network_group_handle');

my $multivalue_14_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '200.1.0.0',
    counter_step           => '0.1.0.0',
    counter_direction      => 'increment',
    nest_step              => '0.0.0.1,0.1.0.0',
    nest_owner             => $deviceGroup_1_handle,$topology_1_handle,
    nest_enabled           => '0,1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_14_handle = ixiangpf::status_item('multivalue_handle');

my $network_group_2_status = ixiangpf::network_group_config ({
    protocol_handle                      => $deviceGroup_1_handle,
    connected_to_handle                  => $pppoxserver_1_handle,
    type                                 => 'ipv4-prefix',
    multiplier                           => '1',
    enable_device                        => '1',
    ipv4_prefix_network_address          => $multivalue_14_handle,
    ipv4_prefix_length                   => '24',
    ipv4_prefix_number_of_addresses      => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $networkGroup_2_handle = ixiangpf::status_item('network_group_handle');

#########################################################################################################################
##                                                     Topology 2 Config                                               ##
#########################################################################################################################

my $topology_2_status = ixiangpf::topology_config ({
    topology_name      => 'Topology 2',
    port_handle        => $port_1,
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $topology_2_handle = ixiangpf::status_item('topology_handle');

#########################################################################################################################
##                                                     Device Group 2 Config                                           ##
#########################################################################################################################

my $device_group_2_status = ixiangpf::topology_config ({
    topology_handle              => $topology_2_handle,
    device_group_name            => 'Device Group 2',
    device_group_multiplier      => '1',
    device_group_enabled         => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_2_handle = ixiangpf::status_item('device_group_handle');

############################################
## Ethernet Config
############################################

my $multivalue_15_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '00.12.01.00.00.01',
    counter_step           => '00.00.00.00.00.01',
    counter_direction      => 'increment',
    nest_step              => '00.00.01.00.00.00',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_15_handle = ixiangpf::status_item('multivalue_handle');

my $ethernet_2_status = ixiangpf::interface_config ({
    protocol_name                => 'Ethernet 2',
    protocol_handle              => $deviceGroup_2_handle,
    mtu                          => '1500',
    src_mac_addr                 => $multivalue_15_handle,
    vlan                         => '0',
    vlan_id                      => '1',
    vlan_id_step                 => '0',
    vlan_id_count                => '1',
    vlan_tpid                    => '0x8100',
    vlan_user_priority           => '0',
    vlan_user_priority_step      => '0',
    use_vpn_parameters           => '0',
    site_id                      => '0',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $ethernet_2_handle = ixiangpf::status_item('ethernet_handle');

my $multivalue_16_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '1',
    counter_step           => '0',
    counter_direction      => 'increment',
    nest_step              => '1',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '0',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_16_handle = ixiangpf::status_item('multivalue_handle');

############################################
## PPoX Client Config
############################################

my $pppoxclient_1_status = ixiangpf::pppox_config ({
    port_role                            => 'access',
    handle                               => $ethernet_2_handle,
    protocol_name                        => 'PPPoX Client 1',
    unlimited_redial_attempts            => '0',
    enable_mru_negotiation               => '0',
    desired_mru_rate                     => '1492',
    max_payload                          => '1700',
    enable_max_payload                   => '0',
    client_ipv6_ncp_configuration        => 'learned',
    client_ipv4_ncp_configuration        => 'learned',
    lcp_enable_accm                      => '0',
    lcp_accm                             => 'ffffffff',
    ac_select_mode                       => 'first_responding',
    auth_req_timeout                     => '10',
    config_req_timeout                   => '10',
    echo_req                             => $multivalue_16_handle,
    echo_rsp                             => '1',
    ip_cp                                => 'dual_stack',
    ipcp_req_timeout                     => '10',
    max_auth_req                         => '20',
    max_padi_req                         => '5',
    max_padr_req                         => '5',
    max_terminate_req                    => '3',
    padi_req_timeout                     => '10',
    padr_req_timeout                     => '10',
    password                             => 'password',
    chap_secret                          => 'secret',
    username                             => 'user',
    chap_name                            => 'user',
    mode                                 => 'add',
    auth_mode                            => 'none',
    echo_req_interval                    => '10',
    max_configure_req                    => '3',
    max_ipcp_req                         => '3',
    actual_rate_downstream               => '10',
    actual_rate_upstream                 => '10',
    data_link                            => 'ethernet',
    enable_domain_group_map              => '0',
    enable_client_signal_iwf             => '0',
    enable_client_signal_loop_char       => '0',
    enable_client_signal_loop_encap      => '0',
    enable_client_signal_loop_id         => '0',
    intermediate_agent_encap1            => 'untagged_eth',
    intermediate_agent_encap2            => 'na',
    ppp_local_iid                        => '0:11:11:11:0:0:0:1',
    ppp_local_ip                         => '1.1.1.1',
    redial                               => '0',
    redial_max                           => '20',
    redial_timeout                       => '10',
    service_type                         => 'any',
    client_dns_options                   => 'disable_extension',
    client_dns_primary_address           => '8.8.8.8',
    client_dns_secondary_address         => '9.9.9.9',
    client_netmask_options               => 'disable_extension',
    client_netmask                       => '255.0.0.0',
    client_wins_options                  => 'disable_extension',
    client_wins_primary_address          => '8.8.8.8',
    client_wins_secondary_address        => '9.9.9.9',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $pppoxclient_1_handle = ixiangpf::status_item('pppox_client_handle');

############################################
## BGP Peer Config
############################################

my $multivalue_17_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '193.0.0.1',
    counter_step           => '0.0.0.1',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_17_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_18_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => 'true',
    counter_step           => 'false',
    counter_direction      => 'increment',
    nest_step              => 'true',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '0',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_18_handle = ixiangpf::status_item('multivalue_handle');

my $bgp_ipv4_peer_2_status = ixiangpf::emulation_bgp_config ({
    mode                                    => 'enable',
    md5_enable                              => '0',
    handle                                  => $pppoxclient_1_handle,
    remote_ip_addr                          => '1.1.1.1',
    remote_addr_step                        => '0.0.0.0',
    enable_4_byte_as                        => '0',
    local_as                                => '2',
    update_interval                         => '0',
    count                                   => '1',
    local_router_id                         => $multivalue_17_handle,
    hold_time                               => '90',
    neighbor_type                           => 'external',
    graceful_restart_enable                 => '0',
    restart_time                            => '45',
    stale_time                              => '0',
    tcp_window_size                         => '8192',
    local_router_id_enable                  => '1',
    ipv4_capability_mdt_nlri                => 'false',
    ipv4_capability_unicast_nlri            => 'true',
    ipv4_filter_unicast_nlri                => $multivalue_18_handle,
    ipv4_capability_multicast_nlri          => 'true',
    ipv4_filter_multicast_nlri              => 'false',
    ipv4_capability_mpls_nlri               => 'true',
    ipv4_filter_mpls_nlri                   => 'false',
    ipv4_capability_mpls_vpn_nlri           => 'true',
    ipv4_filter_mpls_vpn_nlri               => 'false',
    ipv6_capability_unicast_nlri            => 'true',
    ipv6_filter_unicast_nlri                => 'false',
    ipv6_capability_multicast_nlri          => 'true',
    ipv6_filter_multicast_nlri              => 'false',
    ipv6_capability_mpls_nlri               => 'true',
    ipv6_filter_mpls_nlri                   => 'false',
    ipv6_capability_mpls_vpn_nlri           => 'true',
    ipv6_filter_mpls_vpn_nlri               => 'false',
    ttl_value                               => '64',
    updates_per_iteration                   => '1',
    bfd_registration                        => '0',
    bfd_registration_mode                   => 'multi_hop',
    vpls_capability_nlri                    => 'true',
    vpls_filter_nlri                        => 'false',
    act_as_restarted                        => '0',
    discard_ixia_generated_routes           => '0',
    flap_down_time                          => '0',
    local_router_id_type                    => 'same',
    enable_flap                             => '0',
    send_ixia_signature_with_routes         => '0',
    flap_up_time                            => '0',
    vpls_enable_next_hop                    => '0',
    vpls_next_hop                           => '0.0.0.0',
    ipv4_capability_multicast_vpn_nlri      => 'false',
    ipv4_filter_multicast_vpn_nlri          => 'false',
    ipv6_capability_multicast_vpn_nlri      => 'false',
    ipv6_filter_multicast_vpn_nlri          => 'false',
    advertise_end_of_rib                    => '0',
    configure_keepalive_timer               => '0',
    keepalive_timer                         => '30',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $bgpIpv4Peer_2_handle = ixiangpf::status_item('bgp_handle');

############################################
## BGP+ Peer Config
############################################

my $multivalue_19_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '193.0.0.1',
    counter_step           => '0.0.0.1',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_19_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_20_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => 'true',
    counter_step           => 'false',
    counter_direction      => 'increment',
    nest_step              => 'true',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '0',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_20_handle = ixiangpf::status_item('multivalue_handle');

my $bgp_ipv6_peer_2_status = ixiangpf::emulation_bgp_config ({
    mode                                    => 'enable',
    md5_enable                              => '0',
    handle                                  => $pppoxclient_1_handle,
    remote_ipv6_addr                        => '11:0:0:0:1100:0:0:1',
    remote_addr_step                        => '0:0:0:0:0:0:0:0',
    enable_4_byte_as                        => '0',
    local_as                                => '4',
    update_interval                         => '0',
    count                                   => '1',
    local_router_id                         => $multivalue_19_handle,
    hold_time                               => '90',
    neighbor_type                           => 'external',
    graceful_restart_enable                 => '0',
    restart_time                            => '45',
    stale_time                              => '0',
    tcp_window_size                         => '8192',
    local_router_id_enable                  => '1',
    ipv4_capability_mdt_nlri                => 'false',
    ipv4_capability_unicast_nlri            => 'true',
    ipv4_filter_unicast_nlri                => 'false',
    ipv4_capability_multicast_nlri          => 'true',
    ipv4_filter_multicast_nlri              => 'false',
    ipv4_capability_mpls_nlri               => 'true',
    ipv4_filter_mpls_nlri                   => 'false',
    ipv4_capability_mpls_vpn_nlri           => 'true',
    ipv4_filter_mpls_vpn_nlri               => 'false',
    ipv6_capability_unicast_nlri            => 'true',
    ipv6_filter_unicast_nlri                => $multivalue_20_handle,
    ipv6_capability_multicast_nlri          => 'true',
    ipv6_filter_multicast_nlri              => 'false',
    ipv6_capability_mpls_nlri               => 'true',
    ipv6_filter_mpls_nlri                   => 'false',
    ipv6_capability_mpls_vpn_nlri           => 'true',
    ipv6_filter_mpls_vpn_nlri               => 'false',
    ttl_value                               => '64',
    updates_per_iteration                   => '1',
    bfd_registration                        => '0',
    bfd_registration_mode                   => 'multi_hop',
    vpls_capability_nlri                    => 'true',
    vpls_filter_nlri                        => 'false',
    act_as_restarted                        => '0',
    discard_ixia_generated_routes           => '0',
    flap_down_time                          => '0',
    local_router_id_type                    => 'same',
    enable_flap                             => '0',
    send_ixia_signature_with_routes         => '0',
    flap_up_time                            => '0',
    vpls_enable_next_hop                    => '0',
    vpls_next_hop                           => '0.0.0.0',
    ipv4_capability_multicast_vpn_nlri      => 'false',
    ipv4_filter_multicast_vpn_nlri          => 'false',
    ipv6_capability_multicast_vpn_nlri      => 'false',
    ipv6_filter_multicast_vpn_nlri          => 'false',
    advertise_end_of_rib                    => '0',
    configure_keepalive_timer               => '0',
    keepalive_timer                         => '30',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $bgpIpv6Peer_2_handle = ixiangpf::status_item('bgp_handle');

############################################
## Network Group Config
############################################

my $multivalue_21_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '3000:1:1:1:0:0:0:0',
    counter_step           => '0:0:0:1:0:0:0:0',
    counter_direction      => 'increment',
    nest_step              => '0:0:0:0:0:0:0:1,0:0:1:0:0:0:0:0',
    nest_owner             => $deviceGroup_2_handle,$topology_2_handle,
    nest_enabled           => '0,1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_21_handle = ixiangpf::status_item('multivalue_handle');

my $network_group_3_status = ixiangpf::network_group_config ({
    protocol_handle                      => $deviceGroup_2_handle,
    connected_to_handle                  => $pppoxclient_1_handle,
    type                                 => 'ipv6-prefix',
    multiplier                           => '1',
    enable_device                        => '1',
    ipv6_prefix_network_address          => $multivalue_21_handle,
    ipv6_prefix_length                   => '64',
    ipv6_prefix_number_of_addresses      => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $networkGroup_3_handle = ixiangpf::status_item('network_group_handle');

my $multivalue_22_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '201.1.0.0',
    counter_step           => '0.1.0.0',
    counter_direction      => 'increment',
    nest_step              => '0.0.0.1,0.1.0.0',
    nest_owner             => $deviceGroup_2_handle,$topology_2_handle,
    nest_enabled           => '0,1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_22_handle = ixiangpf::status_item('multivalue_handle');

my $network_group_4_status = ixiangpf::network_group_config ({
    protocol_handle                      => $deviceGroup_2_handle,
    connected_to_handle                  => $pppoxclient_1_handle,
    type                                 => 'ipv4-prefix',
    multiplier                           => '1',
    enable_device                        => '1',
    ipv4_prefix_network_address          => $multivalue_22_handle,
    ipv4_prefix_length                   => '24',
    ipv4_prefix_number_of_addresses      => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $networkGroup_4_handle = ixiangpf::status_item('network_group_handle');

############################################
## Globals Config
############################################

my $bgp_ipv4_peer_3_status = ixiangpf::emulation_bgp_config ({
    mode        => 'enable',
    handle      => '/globals',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

my $bgp_ipv6_peer_3_status = ixiangpf::emulation_bgp_config ({
    mode        => 'enable',
    handle      => '/globals',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

my $ethernet_3_status = ixiangpf::interface_config ({
    protocol_handle                     => '/globals',
    ethernet_attempt_enabled            => '0',
    ethernet_attempt_rate               => '200',
    ethernet_attempt_interval           => '1000',
    ethernet_attempt_scale_mode         => 'port',
    ethernet_diconnect_enabled          => '0',
    ethernet_disconnect_rate            => '200',
    ethernet_disconnect_interval        => '1000',
    ethernet_disconnect_scale_mode      => 'port',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

my $multivalue_23_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '1',
    counter_step           => '0',
    counter_direction      => 'increment',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_23_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_24_status = ixiangpf::multivalue_config ({
    pattern                => 'distributed',
    distributed_value      => '1',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_24_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_25_status = ixiangpf::multivalue_config ({
    pattern                => 'distributed',
    distributed_value      => '10',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_25_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_26_status = ixiangpf::multivalue_config ({
    pattern                => 'distributed',
    distributed_value      => '10',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $multivalue_26_handle = ixiangpf::status_item('multivalue_handle');

my $pppoxclient_2_status = ixiangpf::pppox_config ({
    port_role                                => 'access',
    handle                                   => '/globals',
    mode                                     => 'add',
    ipv6_global_address_mode                 => 'icmpv6',
    ra_timeout                               => '30',
    create_interfaces                        => $multivalue_23_handle,
    attempt_rate                             => '200',
    attempt_max_outstanding                  => '400',
    attempt_interval                         => '1000',
    attempt_enabled                          => '1',
    attempt_scale_mode                       => 'port',
    disconnect_rate                          => '200',
    disconnect_max_outstanding               => '400',
    disconnect_interval                      => '1000',
    disconnect_enabled                       => '1',
    disconnect_scale_mode                    => 'port',
    enable_session_lifetime                  => '0',
    min_lifetime                             => $multivalue_24_handle,
    max_lifetime                             => $multivalue_25_handle,
    enable_session_lifetime_restart          => '0',
    max_session_lifetime_restarts            => $multivalue_26_handle,
    unlimited_session_lifetime_restarts      => '0',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

############################################
## Start Protocols
############################################

my $bgp_start_1_status = ixiangpf::emulation_bgp_control ({
    handle                              => $bgpIpv4Peer_1_handle,
    mode                                => 'start',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

my $bgp_start_2_status = ixiangpf::emulation_bgp_control ({
    handle                              => $bgpIpv4Peer_2_handle,
    mode                                => 'start',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

my $bgp_start_3_status = ixiangpf::emulation_bgp_control ({
    handle                              => $bgpIpv6Peer_1_handle,
    mode                                => 'start',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

my $bgp_start_4_status = ixiangpf::emulation_bgp_control ({
    handle                              => $bgpIpv6Peer_2_handle,
    mode                                => 'start',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

print("Wait for 30 seconds");
sleep(30);

############################################
## Stats for BGP
############################################

my $bgp_stats_1_status = ixiangpf::emulation_bgp_control ({
    handle                              => $bgpIpv4Peer_1_handle,
    mode                                => 'stats',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

my $format = "%-40s %-s %-10s\n";
my $stat_value = '';

$stat_value = ixiangpf::status_item("$port_0.aggregate.status");        
printf $format, "status", "=", $stat_value;

$stat_value = ixiangpf::status_item("$port_0.aggregate.sessions_configured");        
printf $format, "sessions_configured", "=", $stat_value;

$stat_value = ixiangpf::status_item("$port_0.aggregate.sessions_established");        
printf $format, "sessions_established", "=", $stat_value;

my $bgp_session_2_status = ixiangpf::emulation_bgp_control ({
    handle                              => $bgpIpv6Peer_1_handle,
    mode                                => 'stats',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

$stat_value = ixiangpf::status_item("$session_handle.session.session_status");        
printf $format, "session_status", "=", $stat_value;

$stat_value = ixiangpf::status_item("$session_handle.session.fsm_state");        
printf $format, "fsm_state", "=", $stat_value;

############################################
## Start Protocols
############################################

my $bgp_stop_1_status = ixiangpf::emulation_bgp_control ({
    handle                              => $bgpIpv4Peer_1_handle,
    mode                                => 'stop',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

my $bgp_stop_2_status = ixiangpf::emulation_bgp_control ({
    handle                              => $bgpIpv4Peer_2_handle,
    mode                                => 'stop',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

my $bgp_stop_3_status = ixiangpf::emulation_bgp_control ({
    handle                              => $bgpIpv6Peer_1_handle,
    mode                                => 'stop',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

my $bgp_stop_4_status = ixiangpf::emulation_bgp_control ({
    handle                              => $bgpIpv6Peer_2_handle,
    mode                                => 'stop',
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();

print("Wait for 30 seconds");
sleep(30);

print ("\n\n$test_name : TEST COMPLETED SUCCESSFULLY!\n");











