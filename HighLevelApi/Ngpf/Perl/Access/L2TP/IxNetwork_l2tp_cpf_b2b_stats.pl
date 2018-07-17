################################################################################
# Version 1.0    $Revision: #1 $
# $Author: cm $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10-29-2013 Stefan Popi
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
#    This sample configures a scenario with 2 L2TP Access                      #
#    Concentrators and 2 L2TP Network Servers.                                 #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10GE LSM XM3 module.                           #
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
use lib "C:/Program Files (x86)/Ixia/hltapi/4.80.101.24/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.20";
use lib "C:/Program Files (x86)/Ixia/hltapi/4.80.101.24/TclScripts/lib/hltapi/library/common/ixiangpf/perl";

use ixiahlt;
use ixiaixn;
use ixiangpf;


# Declare the Chassis IP address and the Ports that will be used
my $test_name              = "l2tp_cpf_b2b_modify_remove";
my $chassis                = "ixro-hlt-xm2-01";
my $tcl_server             = "ixro-hlt-xm2-01";
my @port_list              = ("1/5", "1/6");
my $ixnetwork_tcl_server   = "127.0.0.1";
my $wait_time              = 5;
my $test_dir_path          = abs_path();

################################################################################
# Function to catch the errors and print it on the screen             .        #
################################################################################
sub catch_error {
    if (ixiangpf::status_item('status') != 1) {
        print ("\n#################################################### \n");
        print ("ERROR: \n$test_name : ". ixiangpf::status_item('log'));
        print ("\n#################################################### \n");
        die ("ERROR: \n$test_name : Please check values and the port handles!!!");
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

$_result_ = ixiangpf::connect ({
    reset                  => '1',
    device                 => $chassis,
    ixnetwork_tcl_server   => $ixnetwork_tcl_server,
    tcl_server             => $tcl_server,
    port_list              => \@port_list,
});
ixiatcl::_xeval('puts $::KLV');

&catch_error();

@status_keys = ixiangpf::status_item_keys();
$port_handle = ixiangpf::status_item('port_handle');
$status = ixiangpf::status_item('status');

# Assign portHandleList with port handles values
foreach my $port (@port_list) {
    $port_handle = ixiangpf::status_item("port_handle.$chassis.$port");
    push(@portHandleList, $port_handle);
}

my $port_1 = $portHandleList[0];
my $port_2 = $portHandleList[1];

print ("\nIxia port handles are @portHandleList ...\n");
print ("End connecting to chassis ...\n");


my $topology_1_status = ixiangpf::topology_config ({
    topology_name    => 'Topology 1',
    port_handle      => $port_1,
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $topology_1_handle = ixiangpf::status_item('topology_handle');

my $device_group_1_status = ixiangpf::topology_config ({
    topology_handle          => $topology_1_handle,
    device_group_name        => 'Device Group 1',
    device_group_multiplier  => '3',
    device_group_enabled     => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_1_handle = ixiangpf::status_item('device_group_handle');

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


my $multivalue_2_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '100.1.0.1',
    counter_step           => '0.0.0.1',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_2_handle = ixiangpf::status_item('multivalue_handle');

my $ipv4_1_status = ixiangpf::interface_config ({
    protocol_name                     => 'IPv4 1',
    protocol_handle                   => $ethernet_1_handle,
    ipv4_resolve_gateway              => '1',
    ipv4_manual_gateway_mac           => '00.00.00.00.00.01',
    ipv4_manual_gateway_mac_step      => '00.00.00.00.00.00',
    gateway                           => '0.0.0.0',
    gateway_step                      => '0.0.0.0',
    intf_ip_addr                      => $multivalue_2_handle,
    netmask                           => '255.255.255.0',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $ipv4_1_handle = ixiangpf::status_item('ipv4_handle');

my $multivalue_3_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '100.1.0.100',
    counter_step           => '0.0.0.1',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_3_handle = ixiangpf::status_item('multivalue_handle');


my $lac_1_status = ixiangpf::l2tp_config ({
    l2tp_dst_addr           => $multivalue_3_handle,
    mode                    => 'lac',
    handle                  => $ipv4_1_handle,
    num_tunnels             => '1',
    protocol_name           => 'L2TP Access Concentrator 1',
    action                  => 'create',
    avp_hide                => '0',
    ctrl_chksum             => '1',
    ctrl_retries            => '30',
    data_chksum             => '0',
    hello_interval          => '60',
    hello_req               => '0',
    hostname                => 'ixia',
    init_ctrl_timeout       => '2',
    length_bit              => '0',
    max_ctrl_timeout        => '8',
    offset_bit              => '0',
    offset_byte             => '0',
    offset_len              => '0',
    redial                  => '0',
    redial_max              => '20',
    redial_timeout          => '10',
    rws                     => '10',
    secret                  => 'ixia',
    sequence_bit            => '0',
    tun_auth                => 'tunnel_authentication_disabled',
    udp_dst_port            => '1701',
    udp_src_port            => '1701',
    bearer_capability       => 'both',
    bearer_type             => 'analog',
    framing_capability      => 'sync',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $lac_1_handle = ixiangpf::status_item('lac_handle');

my $device_group_2_status = ixiangpf::topology_config ({
    device_group_name            => 'Device Group 2',
    device_group_multiplier      => '2',
    device_group_enabled         => '1',
    device_group_handle          => $deviceGroup_1_handle,
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_2_handle = ixiangpf::status_item('device_group_handle');


my $multivalue_4_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '00.12.01.00.00.01',
    counter_step           => '00.00.00.00.00.01',
    counter_direction      => 'increment',
    nest_step              => '00.00.00.00.00.01,00.00.01.00.00.00',
    nest_owner             => '$deviceGroup_1_handle,$topology_1_handle)',
    nest_enabled           => '0,1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_4_handle = ixiangpf::status_item('multivalue_handle');

my $ethernet_2_status = ixiangpf::interface_config ({
    protocol_name                => 'Ethernet 2',
    protocol_handle              => $deviceGroup_2_handle,
    connected_to_handle          => $ethernet_1_handle,
    mtu                          => '1500',
    src_mac_addr                 => $multivalue_4_handle,
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
    echo_req                             => '0',
    echo_rsp                             => '1',
    ip_cp                                => 'ipv4_cp',
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
    redial                               => '1',
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
    lcp_max_failure                      => '5',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $pppoxclient_1_handle = ixiangpf::status_item('pppox_client_handle');

my $device_group_3_status = ixiangpf::topology_config ({
    topology_handle              => $topology_1_handle,
    device_group_name            => 'Device Group 4',
    device_group_multiplier      => '10',
    device_group_enabled         => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_3_handle = ixiangpf::status_item('device_group_handle');

my $multivalue_5_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '00.14.01.00.00.01',
    counter_step           => '00.00.00.00.00.01',
    counter_direction      => 'increment',
    nest_step              => '00.00.01.00.00.00',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_5_handle = ixiangpf::status_item('multivalue_handle');


my $ethernet_3_status = ixiangpf::interface_config ({
    protocol_name                => 'Ethernet 4',
    protocol_handle              => $deviceGroup_3_handle,
    mtu                          => '1500',
    src_mac_addr                 => $multivalue_5_handle,
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
my $ethernet_3_handle = ixiangpf::status_item('ethernet_handle');


my $multivalue_6_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '102.1.0.1',
    counter_step           => '0.0.0.1',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_1_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_6_handle = ixiangpf::status_item('multivalue_handle');


my $ipv4_2_status = ixiangpf::interface_config ({
    protocol_name                     => '{IPv4 3}',
    protocol_handle                   => $ethernet_3_handle,
    ipv4_resolve_gateway              => '1',
    ipv4_manual_gateway_mac           => '00.00.00.00.00.01',
    ipv4_manual_gateway_mac_step      => '00.00.00.00.00.00',
    gateway                           => '0.0.0.0',
    gateway_step                      => '0.0.0.0',
    intf_ip_addr                      => $multivalue_6_handle,
    netmask                           => '255.255.255.0',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $ipv4_2_handle = ixiangpf::status_item('ipv4_handle');


my $multivalue_7_status = ixiangpf::multivalue_config ({
    pattern           => 'custom',
    nest_step         => '0.1.0.0',
    nest_owner        => $topology_1_handle,
    nest_enabled      => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_7_handle = ixiangpf::status_item('multivalue_handle');


my $custom_1_status = ixiangpf::multivalue_config ({
    multivalue_handle      => $multivalue_7_handle,
    custom_start           => '102.1.0.100',
    custom_step            => '0.0.0.0',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $custom_1_handle = ixiangpf::status_item('custom_handle');


my $increment_1_status = ixiangpf::multivalue_config ({
    custom_handle               => $custom_1_handle,
    custom_increment_value      => '0.0.0.1',
    custom_increment_count      => '50',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $increment_1_handle = ixiangpf::status_item('increment_handle');

my $lac_2_status = ixiangpf::l2tp_config ({
    l2tp_dst_addr           => $multivalue_7_handle,
    mode                    => 'lac',
    handle                  => $ipv4_2_handle,
    num_tunnels             => '5',
    protocol_name           => 'L2TP Access Concentrator 2',
    action                  => 'create',
    avp_hide                => '0',
    ctrl_chksum             => '1',
    ctrl_retries            => '30',
    data_chksum             => '0',
    hello_interval          => '60',
    hello_req               => '0',
    hostname                => 'ixia',
    init_ctrl_timeout       => '2',
    length_bit              => '0',
    max_ctrl_timeout        => '8',
    offset_bit              => '0',
    offset_byte             => '0',
    offset_len              => '0',
    redial                  => '0',
    redial_max              => '20',
    redial_timeout          => '10',
    rws                     => '10',
    secret                  => 'ixia',
    sequence_bit            => '0',
    tun_auth                => 'tunnel_authentication_disabled',
    udp_dst_port            => '1701',
    udp_src_port            => '1701',
    bearer_capability       => 'both',
    bearer_type             => 'analog',
    framing_capability      => 'sync',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $lac_2_handle = ixiangpf::status_item('lac_handle');

my $device_group_4_status = ixiangpf::topology_config ({
    device_group_name            => 'Device Group 5',
    device_group_multiplier      => '1',
    device_group_enabled         => '1',
    device_group_handle          => $deviceGroup_3_handle,
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_4_handle = ixiangpf::status_item('device_group_handle');


my $multivalue_8_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '00.15.01.00.00.01',
    counter_step           => '00.00.00.00.00.01',
    counter_direction      => 'increment',
    nest_step              => '00.00.00.00.00.01,00.00.01.00.00.00',
    nest_owner             => '$deviceGroup_3_handle,$topology_1_handle',
    nest_enabled           => '0,1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_8_handle = ixiangpf::status_item('multivalue_handle');


my $ethernet_4_status = ixiangpf::interface_config ({
    protocol_name                => 'Ethernet 5',
    protocol_handle              => $deviceGroup_4_handle,
    connected_to_handle          => $ethernet_3_handle,
    mtu                          => '1500',
    src_mac_addr                 => $multivalue_8_handle,
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
my $ethernet_4_handle = ixiangpf::status_item('ethernet_handle');


my $pppoxclient_2_status = ixiangpf::pppox_config ({
    port_role                            => 'access',
    handle                               => $ethernet_4_handle,
    protocol_name                        => 'PPPoX Client 2',
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
    echo_req                             => '0',
    echo_rsp                             => '1',
    ip_cp                                => 'ipv4_cp',
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
    redial                               => '1',
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
    lcp_max_failure                      => '5',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $pppoxclient_2_handle = ixiangpf::status_item('pppox_client_handle');


my $topology_2_status = ixiangpf::topology_config ({
    topology_name      => 'Topology 2',
    port_handle        => $port_2,
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $topology_2_handle = ixiangpf::status_item('topology_handle');


my $device_group_5_status = ixiangpf::topology_config ({
    topology_handle              => $topology_2_handle,
    device_group_name            => 'Device Group 3',
    device_group_multiplier      => '5',
    device_group_enabled         => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_5_handle = ixiangpf::status_item('device_group_handle');


my $multivalue_9_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '00.13.01.00.00.01',
    counter_step           => '00.00.00.00.00.01',
    counter_direction      => 'increment',
    nest_step              => '00.00.01.00.00.00',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_9_handle = ixiangpf::status_item('multivalue_handle');


my $ethernet_5_status = ixiangpf::interface_config ({
    protocol_name                => 'Ethernet 3',
    protocol_handle              => $deviceGroup_5_handle,
    mtu                          => '1500',
    src_mac_addr                 => $multivalue_9_handle,
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
my $ethernet_5_handle = ixiangpf::status_item('ethernet_handle');


my $multivalue_10_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '100.1.0.100',
    counter_step           => '0.0.0.1',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_10_handle = ixiangpf::status_item('multivalue_handle');


my $ipv4_3_status = ixiangpf::interface_config ({
    protocol_name                     => 'IPv4 2',
    protocol_handle                   => $ethernet_5_handle,
    ipv4_resolve_gateway              => '1',
    ipv4_manual_gateway_mac           => '00.00.00.00.00.01',
    ipv4_manual_gateway_mac_step      => '00.00.00.00.00.00',
    gateway                           => '0.0.0.0',
    gateway_step                      => '0.0.0.0',
    intf_ip_addr                      => $multivalue_10_handle,
    netmask                           => '255.255.255.0',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $ipv4_3_handle = ixiangpf::status_item('ipv4_handle');


my $lns_1_status = ixiangpf::l2tp_config ({
    mode                    => 'lns',
    handle                  => $ipv4_3_handle,
    protocol_name           => 'L2TP Network Server 1',
    action                  => 'create',
    avp_hide                => '0',
    ctrl_chksum             => '1',
    ctrl_retries            => '30',
    data_chksum             => '0',
    hello_interval          => '60',
    hello_req               => '0',
    hostname                => 'ixia',
    init_ctrl_timeout       => '2',
    length_bit              => '0',
    max_ctrl_timeout        => '8',
    no_call_timeout         => '5',
    offset_bit              => '0',
    offset_byte             => '0',
    offset_len              => '0',
    rws                     => '10',
    secret                  => 'ixia',
    sequence_bit            => '0',
    tun_auth                => 'tunnel_authentication_disabled',
    udp_dst_port            => '1701',
    udp_src_port            => '1701',
    bearer_capability       => 'both',
    bearer_type             => 'analog',
    framing_capability      => 'sync',
    lns_host_name           => 'ixia',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $lns_1_handle = ixiangpf::status_item('lns_handle');


my $multivalue_11_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '2.2.2.2',
    counter_step           => '0.0.1.0',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_11_handle = ixiangpf::status_item('multivalue_handle');


my $multivalue_12_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '1:1:1:0:0:0:0:0',
    counter_step           => '0:0:1:0:0:0:0:0',
    counter_direction      => 'increment',
    nest_step              => '0:1:0:0:0:0:0:0',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_12_handle = ixiangpf::status_item('multivalue_handle');


my $multivalue_13_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '0:11:22:11:0:0:0:1',
    counter_step           => '0:0:0:1:0:0:0:0',
    counter_direction      => 'increment',
    nest_step              => '0:0:1:0:0:0:0:0',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_13_handle = ixiangpf::status_item('multivalue_handle');

my $pppoxserver_1_status = ixiangpf::pppox_config ({
    port_role                            => 'network',
    handle                               => $lns_1_handle,
    protocol_name                        => 'PPPoX Server 1',
    enable_mru_negotiation               => '0',
    desired_mru_rate                     => '1492',
    enable_max_payload                   => '0',
    server_ipv6_ncp_configuration        => 'clientmay',
    server_ipv4_ncp_configuration        => 'clientmay',
    lcp_enable_accm                      => '0',
    lcp_accm                             => 'ffffffff',
    num_sessions                         => '2',
    auth_req_timeout                     => '10',
    config_req_timeout                   => '10',
    echo_req                             => '0',
    echo_rsp                             => '1',
    ip_cp                                => 'ipv4_cp',
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
    ipv6_pool_prefix                     => $multivalue_12_handle,
    ipv6_pool_addr_prefix_len            => '64',
    ppp_local_iid                        => $multivalue_13_handle,
    ppp_local_ip                         => $multivalue_11_handle,
    ppp_local_ip_step                    => '0.0.0.1',
    ppp_local_iid_step                   => '1',
    ppp_peer_iid                         => '0:11:11:11:0:0:0:1',
    ppp_peer_iid_step                    => '1',
    ppp_peer_ip                          => '1.1.1.1',
    ppp_peer_ip_step                     => '0.0.0.1',
    send_dns_options                     => '0',
    dns_server_list                      => '2001:0:0:0:0:0:0:1',
    server_dns_options                   => 'disable_extension',
    server_dns_primary_address           => '10.10.10.10',
    server_dns_secondary_address         => '11.11.11.11',
    server_netmask_options               => 'disable_extension',
    server_netmask                       => '255.255.255.0',
    server_wins_options                  => 'disable_extension',
    server_wins_primary_address          => '10.10.10.10',
    server_wins_secondary_address        => '11.11.11.11',
    accept_any_auth_value                => '0',
    lcp_max_failure                      => '5',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $pppoxserver_1_handle = ixiangpf::status_item('pppox_server_handle');
my $pppoxServerSessions_1_handle = ixiangpf::status_item('pppox_server_sessions_handle');

my $device_group_6_status  = ixiangpf::topology_config ({
    topology_handle              => $topology_2_handle,
    device_group_name            => 'Device Group 6',
    device_group_multiplier      => '50',
    device_group_enabled         => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $deviceGroup_6_handle = ixiangpf::status_item('device_group_handle');


my $multivalue_14_status  = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '00.16.01.00.00.01',
    counter_step           => '00.00.00.00.00.01',
    counter_direction      => 'increment',
    nest_step              => '00.00.01.00.00.00',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_14_handle = ixiangpf::status_item('multivalue_handle');

my $ethernet_6_status = ixiangpf::interface_config ({
    protocol_name                => 'Ethernet 6',
    protocol_handle              => $deviceGroup_6_handle,
    mtu                          => '1500',
    src_mac_addr                 => $multivalue_14_handle,
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
my $ethernet_6_handle = ixiangpf::status_item('ethernet_handle');


my $multivalue_15_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '102.1.0.100',
    counter_step           => '0.0.0.1',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_15_handle = ixiangpf::status_item('multivalue_handle');


my $ipv4_4_status = ixiangpf::interface_config ({
    protocol_name                     => 'IPv4 4',
    protocol_handle                   => $ethernet_6_handle,
    ipv4_resolve_gateway              => '1',
    ipv4_manual_gateway_mac           => '00.00.00.00.00.01',
    ipv4_manual_gateway_mac_step      => '00.00.00.00.00.00',
    gateway                           => '0.0.0.0',
    gateway_step                      => '0.0.0.0',
    intf_ip_addr                      => $multivalue_15_handle,
    netmask                           => '255.255.255.0',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $ipv4_4_handle = ixiangpf::status_item('ipv4_handle');


my $lns_2_status = ixiangpf::l2tp_config ({
    mode                    => 'lns',
    handle                  => $ipv4_4_handle,
    protocol_name           => 'L2TP Network Server 2',
    action                  => 'create',
    avp_hide                => '0',
    ctrl_chksum             => '1',
    ctrl_retries            => '30',
    data_chksum             => '0',
    hello_interval          => '60',
    hello_req               => '0',
    hostname                => 'ixia',
    init_ctrl_timeout       => '2',
    length_bit              => '0',
    max_ctrl_timeout        => '8',
    no_call_timeout         => '5',
    offset_bit              => '0',
    offset_byte             => '0',
    offset_len              => '0',
    rws                     => '10',
    secret                  => 'ixia',
    sequence_bit            => '0',
    tun_auth                => 'tunnel_authentication_disabled',
    udp_dst_port            => '1701',
    udp_src_port            => '1701',
    bearer_capability       => 'both',
    bearer_type             => 'analog',
    framing_capability      => 'sync',
    lns_host_name           => 'ixia',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $lns_2_handle = ixiangpf::status_item('lns_handle');


my $multivalue_16_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '3.2.2.2',
    counter_step           => '0.0.1.0',
    counter_direction      => 'increment',
    nest_step              => '0.1.0.0',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_16_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_17_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '2:1:1:0:0:0:0:0',
    counter_step           => '0:0:1:0:0:0:0:0',
    counter_direction      => 'increment',
    nest_step              => '0:1:0:0:0:0:0:0',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_17_handle = ixiangpf::status_item('multivalue_handle');

my $multivalue_18_status = ixiangpf::multivalue_config ({
    pattern                => 'counter',
    counter_start          => '0:12:22:11:0:0:0:1',
    counter_step           => '0:0:0:1:0:0:0:0',
    counter_direction      => 'increment',
    nest_step              => '0:0:1:0:0:0:0:0',
    nest_owner             => $topology_2_handle,
    nest_enabled           => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $multivalue_18_handle = ixiangpf::status_item('multivalue_handle');


my $pppoxserver_2_status = ixiangpf::pppox_config ({
    port_role                            => 'network',
    handle                               => $lns_2_handle,
    protocol_name                        => 'PPPoX Server 2',
    enable_mru_negotiation               => '0',
    desired_mru_rate                     => '1492',
    enable_max_payload                   => '0',
    server_ipv6_ncp_configuration        => 'clientmay',
    server_ipv4_ncp_configuration        => 'clientmay',
    lcp_enable_accm                      => '0',
    lcp_accm                             => 'ffffffff',
    num_sessions                         => '20',
    auth_req_timeout                     => '10',
    config_req_timeout                   => '10',
    echo_req                             => '0',
    echo_rsp                             => '1',
    ip_cp                                => 'ipv4_cp',
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
    ipv6_pool_prefix                     => $multivalue_17_handle,
    ipv6_pool_addr_prefix_len            => '64',
    ppp_local_iid                        => $multivalue_18_handle,
    ppp_local_ip                         => $multivalue_16_handle,
    ppp_local_ip_step                    => '0.0.0.1',
    ppp_local_iid_step                   => '1',
    ppp_peer_iid                         => '0:11:11:11:0:0:0:1',
    ppp_peer_iid_step                    => '1',
    ppp_peer_ip                          => '1.1.1.1',
    ppp_peer_ip_step                     => '0.0.0.1',
    send_dns_options                     => '0',
    dns_server_list                      => '2001:0:0:0:0:0:0:1',
    server_dns_options                   => 'disable_extension',
    server_dns_primary_address           => '10.10.10.10',
    server_dns_secondary_address         => '11.11.11.11',
    server_netmask_options               => 'disable_extension',
    server_netmask                       => '255.255.255.0',
    server_wins_options                  => 'disable_extension',
    server_wins_primary_address          => '10.10.10.10',
    server_wins_secondary_address        => '11.11.11.11',
    accept_any_auth_value                => '0',
    lcp_max_failure                      => '5',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $pppoxserver_2_handle = ixiangpf::status_item('pppox_server_handle');
my $pppoxServerSessions_2_handle = ixiangpf::status_item('pppox_server_sessions_handle');
    
print ("waiting for ports to become available ...");
sleep (5);

print ("Starting protocols ...");
my $control_start = ixiahlt::test_control ({
    action => 'start_all_protocols',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();

sleep (15);        
print ("Getting statistics per port...");
my $l2tp_port_stats = ixiangpf::l2tp_stats ({
    port_handle => $port_handle,
    mode        => 'aggregate',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
     
print ("Stopping protocols ...");
my $control_stop = ixiahlt::test_control({
    action => 'stop_all_protocols',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();

print ("\n\n$test_name : TEST COMPLETED SUCCESSFULLY!\n");