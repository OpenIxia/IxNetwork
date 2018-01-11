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
#    This sample configures a simple scenario with a L2TP Access               #
#    Concentrator and a L2TP Network Server                                    #
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

my $remove_l2tp_configuration = 1;

#####################################################
# Create a topology and a device group for L2tp LAC #
#####################################################

my $topology_status = ixiangpf::topology_config ({
        topology_name           => 'L2tp Access Concentrator',
		port_handle				=> $port_1,
		device_group_multiplier	=> 10,
        device_group_name       => 'LAC DG',
        device_group_enabled    => 1,
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $dg_handle_1 = ixiangpf::status_item('device_group_handle');

my $mac_start		= "0000.0005.0001";
my $mac_step		= "0000.0000.1000";

my $command_status = ixiangpf::interface_config ({
		protocol_handle		=> $dg_handle_1,
		src_mac_addr       	=> $mac_start,
		src_mac_addr_step		=> $mac_step,
});

&catch_error();

@status_keys = ixiangpf::status_item_keys();
my $ethernet_handle_1 = ixiangpf::status_item('ethernet_handle');


my $mv_custom_distribution = ixiangpf::multivalue_config ({
        mode                  => 'create',
        pattern               => 'string',
        string_pattern        => 'User{Inc:1}_Pwd{Inc:100}',
});

&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $mv_cd_handle = ixiangpf::status_item('multivalue_handle');

#####################################################
# Create a topology and a device group for L2tp LNS #
#####################################################
my $topology_status_2 = ixiangpf::topology_config ({
        topology_name            => 'L2tp Network Server',
		port_handle			     => $port_2,
		device_group_multiplier  => '2',
        device_group_name        => 'LNS DG',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $dg_handle_2 = ixiangpf::status_item('device_group_handle');

my $mac_start_2 = "0000.0005.0001";
my $mac_step_2  = "0000.0000.1000";

my $command_status_2 = ixiangpf::interface_config ({
		protocol_handle			=> $dg_handle_2,
		src_mac_addr       		=> $mac_start_2,
		src_mac_addr_step		=> $mac_step_2,
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $ethernet_handle_2 = ixiangpf::status_item('ethernet_handle');


#########################################
#  Configure sessions                   #
#########################################

my $tunnel_count        = 10;
my $sessions_per_tunnel = 10;
my $l2tp_domain_group   = "UserIxia";

my $config_lac_status = ixiangpf::l2tp_config ({
        mode                          => "lac",
        handle                        => $ethernet_handle_1,
        num_tunnels                   => $tunnel_count,
        sessions_per_tunnel           => $sessions_per_tunnel,
        protocol_name                 => 'Ixia LAC',
        l2tp_dst_addr                 => '12.70.0.1',
        l2tp_dst_step                 => '0.0.0.0',
        l2tp_src_addr                 => '12.70.0.2',
        l2tp_src_step                 => '0.0.0.1',
        domain_group_map              => '$mv_cd_handle',
        attempt_rate                  => '100',
        sequence_bit                  => '1',
        offset_bit                    => '1',
        length_bit                    => '1',
        tun_auth                      => '1',
        redial                        => '1',
        data_chksum                   => '1',
        ctrl_chksum                   => '1',
        hello_req                     => '1',
        avp_hide                      => '1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $lac_handle = ixiangpf::status_item('lac_handle');


my $config_lns_status = ixiangpf::l2tp_config ({
        mode                            => 'lns',
        handle                          => $ethernet_handle_2,
        l2_encap                        => 'ethernet_ii',
        num_tunnels                     => $tunnel_count,
        sessions_per_tunnel             => $sessions_per_tunnel,
        l2tp_dst_addr                   => '12.70.0.1',
        l2tp_dst_step                   => '0.0.0.0',
        l2tp_src_addr                   => '12.70.0.2',
        l2tp_src_step                   => '0.0.0.1',
        attempt_rate                    => '100',
        username                        => 'ixia_lns_user',
        password                        => 'ixia_lns_pass',
        chap_name                       => 'ixia_chap_name',
        chap_secret                     => 'ixia_chap_secret',
        enable_domain_groups            => '1',
        domain_group_map                => $l2tp_domain_group,
        sequence_bit                    => '1',
        offset_bit                      => '1',
        length_bit                      => '1',
        tun_auth                        => '1',
        redial                          => '1',
        ctrl_chksum                     => '1',
        data_chksum                     => '1',
        hello_req                       => '1',
        avp_hide                        => '1',
        offset_byte                     => '89',
        udp_src_port                    => '1600',
        udp_dst_port                    => '1800',
        redial_timeout                  => '13',
        rws                             => '15',
        offset_len                      => '16',
        max_ctrl_timeout                => '9',
        redial_max                      => '2048',
        secret                          => 'ixia_secret',
        hostname                        => 'ixia_dut',
        init_ctrl_timeout               => '6',
        hello_interval                  => '101',
        framing_capability              => 'async',
        ctrl_retries                    => '11',
        bearer_type                     => 'digital',
        bearer_capability               => 'digital',
        accept_any_auth_value           => '1',
        max_auth_req                    => '121',
        auth_req_timeout                => '132',
        auth_mode                       => 'pap_or_chap',
        ppp_client_iid                  => '00:55:55:55:00:00:00:01',
        ppp_client_iid_step             => '00:00:00:00:00:00:00:03',
        ppp_client_ip                   => '22.22.22.1',
        ppp_client_step                 => '0.0.0.3',
        dns_server_list                 => '100:0:0:1:0:0:0:0',
        echo_req_interval               => '17',
        send_dns_options                => '1',
        echo_req                        => '1',
        echo_rsp                        => '1',
        ipv6_pool_addr_prefix_len       => '90',
        ipv6_pool_prefix                => '1:1:1:1:1:1:1:1',
        ipv6_pool_prefix_len            => '72',
        lcp_accm                        => '234',
        lcp_enable_accm                 => '1',
        max_configure_req               => '111',
        max_terminate_req               => '120',
        config_req_timeout              => '55',
        enable_mru_negotiation          => '1',
        desired_mru_rate                => '70',
        protocol_name                   => "Ixia LNS",
        max_ipcp_req                    => '14',
        ipcp_req_timeout                => '15',
        ip_cp                           => 'dual_stack',
        ppp_server_iid                  => '00:66:66:66:00:00:00:01',
        ppp_server_ip                   => '45.45.45.1',
        server_dns_options              => 'supply_primary_and_secondary',
        ppp_local_iid_step              => '3',
        ppp_local_ip_step               => '0.0.15.15',
        server_ipv4_ncp_configuration   => 'clientmay',
        server_netmask                  => '255.255.255.128',
        server_netmask_options          => 'supply_netmask',
        server_primary_dns_address      => '12.12.12.1',
        server_secondary_dns_address    => '13.13.13.1',
        server_ipv6_ncp_configuration   => 'clientmay',
        server_wins_options             => 'supply_primary_and_secondary',
        server_wins_primary_address     => '21.21.21.1',
        server_wins_secondary_address   => '31.31.31.1',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();
my $lns_handle = ixiangpf::status_item('lns_handle');


#########################################
#  Modify sessions                      #
#########################################

my $modify_lac_status = ixiangpf::l2tp_config ({
        mode                    => 'lac',
        action                  => 'modify',
        handle                  => $lac_handle,
        num_tunnels             => $tunnel_count,
        l2tp_dst_addr           => '20.20.0.1',
        protocol_name           => "Modified Ixia LAC",
        attempt_rate            => '20',
        offset_byte             => '30',
        udp_src_port            => '1600',
        udp_dst_port            => '1800',
        redial_timeout          => '10',
        rws                     => '11',
        offset_len              => '12',
        max_ctrl_timeout        => '13',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();

my $modify_lns_status = ixiangpf::l2tp_config ({
        mode                     => 'lns',
        action                   => 'modify',
        handle                   => $lns_handle,
        num_tunnels              => $tunnel_count,
        protocol_name            => "Modified Ixia LNS",
        attempt_rate             => '15',
        offset_byte              => '25',
        udp_src_port             => '1650',
        udp_dst_port             => '1850',
        redial_timeout           => '15',
        rws                      => '16',
        offset_len               => '17',
        max_ctrl_timeout         => '18',
});
&catch_error();
@status_keys = ixiangpf::status_item_keys();

#########################################
#  Remove sessions                      #
#########################################

if ($remove_l2tp_configuration == 1) {
    my $remove_lac_status = ixiangpf::l2tp_config ({
            mode                  => 'lac',
            action                => 'remove',
            handle                => $lac_handle,              
            delete_attached_ppp   => '1',
    });
    &catch_error();
    @status_keys = ixiangpf::status_item_keys();

    my $remove_lns_status = ixiangpf::l2tp_config ({
            mode               => 'lns',
            action             => 'remove',
            handle             => $lns_handle,
    });
    &catch_error();
    @status_keys = ixiangpf::status_item_keys();
}

print ("\n\n$test_name : TEST COMPLETED SUCCESSFULLY!\n");