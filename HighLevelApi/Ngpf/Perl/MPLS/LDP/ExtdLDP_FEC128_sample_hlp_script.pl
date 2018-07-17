################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    20/01/2015 - Subhradip Pramanik - created sample                          #
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
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF LDP API.               #
#                                                                              #
#    About Topology:                                                           #
#         Within topology both Provider Edge(PE) and Provider(P) Routers       #
#     are created. P router is emulated in the front Device Group(DG), which   #
#    consists of both OSPF as routing protocol as well as Basic LDP sessions   #
#     for Transport Label Distribution Protocol. The chained DG act as PE      #
#     Router, where LDP Extended Martini is configured for VPN Label           #
#     distribution protocol. Bidirectional L2-L3 Traffic is configured in      #
#    between two CE cloud is created.                #
#     Script Flow:                                                             #
#     1. Configuration of protocols.                                           #
#    Configuration flow of the script is as follow:                            #
#         i.    Adding of OSPF router.                                         #
#         ii.   Adding of Network Cloud.                                       #
#         iii.  Adding of chain DG.                                            #
#         iv.   Adding of LDP(basic session) on Front DG                       #
#         v.    Adding of LDP Extended Martini(Targeted sess.) over chained DG.#
#         vi.   Adding of LDP PW/VPLS Tunnel over LDP Extended Martini.        #
#    2. Start the LDP protocol.                                                #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Disable/Enable the LDP FECs and change label & apply change on the fly #
#    6. Retrieve protocol learned info again and notice the difference with    #
#       previously retrieved learned info.                                     #
#    7. Configure L2-L3 traffic.                                               #
#    8. Start the L2-L3 traffic.                                               #
#    9. Retrieve L2-L3 traffic stats.                                          #
#   10. Stop L2-L3 traffic.                                                    #
#   11. Stop all protocols.                                                    #
# Ixia Software :                                                              #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################

################################################################################
# Utils                                                                        #	
################################################################################

# Libraries to be included
# package require Ixia
# Other procedures used in the script, that do not use HL API configuration/control procedures

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
    #use lib "C:/Program Files (x86)/Ixia/hltapi/4.95.117.44/TclScripts/lib/hltapi/library/common/ixiangpf/perl";

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
my @chassis             = ('10.216.108.123');
my $tcl_server          = '10.216.108.123';
my @port_list           = ([ '2/3', '2/4' ]);
my $ixNetwork_client    = '10.216.108.49:8999';

print "Connecting to chassis and client\n";
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

# Creating a topology on first port
print "Adding topology 1 on port 1\n";     
my $topology_1_status = ixiangpf::topology_config ({
    topology_name      => "{Topology for FEC128 1}",
    port_handle        => $port_handles_list[0],
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
	my $error = ixiangpf::status_item('log');
	print "Error: $error";
	return "FAILED - $error";
}
my $topology_1_handle = $HashRef->{'topology_handle'};

# Creating a device group in topology 
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
    

# Creating a topology on second port
print "Adding topology 2 on port 2\n";
my $topology_2_status = ixiangpf::topology_config ({
    topology_name      => "{Topology for FEC128 2}",
    port_handle        => $port_handles_list[1],
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $topology_2_handle = $HashRef->{'topology_handle'};

# Creating a device group in topology
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
my $deviceGroup_2_handle = $HashRef->{'device_group_handle'};

################################################################################
#  Configure protocol interfaces                                               #
################################################################################

# Creating ethernet stack for the first Device Group 
print "Creating ethernet stack for the first Device Group\n";
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
    my $error = ixiangpf::status_item('log');
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

# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group 
print "Creating IPv4 2 stack on ethernet 2 stack for the second Device Group\n";
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
# Other protocol configurations                                                # 
################################################################################
# This will create OSPFv2 on top of IP within Topology 1 
print "Creating OSPFv2 on top of IPv4 1 stack\n";
my $ospfv2_1_status =ixiangpf::emulation_ospf_config ({
     handle                                                 => $ipv4_1_handle,
     mode                                                   => "create",
     network_type                                           => "ptop",
     protocol_name                                          => "{OSPFv2-IF 1}",
     router_id                                              => "193.0.0.1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
# This will create OSPFv2 on top of IP within Topology 2
print "Creating OSPFv2 on top of IPv4 2 stack\n";
my $ospfv2_2_status =ixiangpf::emulation_ospf_config ({
     handle                                                 => $ipv4_2_handle,
     mode                                                   => "create",
     network_type                                           => "ptop",
     protocol_name                                          => "{OSPFv2-IF 2}",
     router_id                                              => "194.0.0.1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
# This will create LDP Router and interface over IP for the first Device Group with lsr_id="193.0.0.1".
print "Creating LDP Router Stack on top of IPv4 1 stack\n";
my $ldp_basic_router_1_status =ixiangpf::emulation_ldp_config ({
     handle                       => $ipv4_1_handle,
     mode                         => "create",
     lsr_id                       => "193.0.0.1",
     interface_name               => "{LDP-IF 1}",
     router_name                  => "{LDP 1}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ldpBasicRouter_1_handle = $HashRef->{'ldp_basic_router_handle'};
# Creating LDP Interface Stack on top of IPv4 1 stack for first device Group
print "Creating LDP Interface Stack on top of IPv4 1 stack\n";
my $ldp_connected_interface_1_status = ixiangpf::emulation_ldp_config ({
    handle                    => $ipv4_1_handle,
    mode                      => "create",
    interface_name            => "{LDP-IF 1}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ldpConnectedInterface_1_handle = $HashRef->{'ldp_connected_interface_handle'};


# This will create LDP Router and interface over IP for the second Device Group with lsr_id="194.0.0.1".
print "Creating LDP Router Stack on top of IPv4 2 stack\n";
my $ldp_basic_router_2_status =ixiangpf::emulation_ldp_config ({
     handle                       => $ipv4_2_handle,
     mode                         => "create",
     lsr_id                       => "194.0.0.1",
     interface_name               => "{LDP-IF 2}",
     router_name                  => "{LDP 2}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ldpBasicRouter_2_handle = $HashRef->{'ldp_basic_router_handle'};
# Creating LDP Interface Stack on top of IPv4 2 stack for second device Group
print "Creating LDP Interface Stack on top of IPv4 2 stack\n";
my $ldp_connected_interface_2_status = ixiangpf::emulation_ldp_config ({
    handle                    => $ipv4_2_handle,
    mode                      => "create",
    interface_name            => "{LDP-IF 2}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ldpConnectedInterface_2_handle = $HashRef->{'ldp_connected_interface_handle'};

# Creating IPv4 prefix pool of Network for Network Cloud behind first Device Group  with "ipv4_prefix_network_address" =201.1.0.1
print "Creating IPv4 prefix pool behind first Device Group\n";
my $network_group_1_status = ixiangpf::network_group_config ({
    protocol_handle                   => $deviceGroup_1_handle,
    protocol_name                     =>  "{Network Cloud 1}",
    connected_to_handle               =>  $ethernet_1_handle,
    type                              =>  "ipv4-prefix",
    ipv4_prefix_network_address       =>  "201.1.0.1",
    ipv4_prefix_length                =>  "32",
    ipv4_prefix_number_of_addresses   =>  "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_1_handle = $HashRef->{'network_group_handle'};
my $ipv4PrefixPools_1_handle = $HashRef->{'ipv4_prefix_pools_handle'};


# Creating IPv4 prefix pool of Network for Network Cloud behind second Device Group  with "ipv4_prefix_network_address" =202.1.0.1
print "Creating IPv4 prefix pool behind second Device Group\n";
my $network_group_2_status = ixiangpf::network_group_config ({
    protocol_handle                   => $deviceGroup_2_handle,
    protocol_name                     =>  "{Network Cloud 2}",
    connected_to_handle               =>  $ethernet_2_handle,
    type                              =>  "ipv4-prefix",
    ipv4_prefix_network_address       =>  "202.1.0.1",
    ipv4_prefix_length                =>  "32",
    ipv4_prefix_number_of_addresses   =>  "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_2_handle = $HashRef->{'network_group_handle'};
my $ipv4PrefixPools_2_handle = $HashRef->{'ipv4_prefix_pools_handle'};
# Modifying in IPv4 prefix for LDP Router related Configurations "label_value_start"=17
print "Modification of LDP related parameters in Network Cloud\n";
$network_group_1_status = ixiangpf::emulation_ldp_route_config ({
    handle                   => $networkGroup_1_handle,
    mode                     => "modify",
    egress_label_mode        => "fixed",
    fec_type                 => "ipv4_prefix",
    label_value_start        => "17",
    label_value_start_step   => "1",
    lsp_handle               => $networkGroup_1_handle,
    fec_name                 => "{LDP FEC Range 1}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

# Modifying in IPv4 prefix for LDP Router related Configurations "label_value_start"=18
print "Modification of LDP related parameters in Network Cloud\n";
$network_group_2_status = ixiangpf::emulation_ldp_route_config ({
    handle                   => $networkGroup_2_handle,
    mode                     => "modify",
    egress_label_mode        => "fixed",
    fec_type                 => "ipv4_prefix",
    label_value_start        => "18",
    label_value_start_step   => "1",
    lsp_handle               => $networkGroup_2_handle,
    fec_name                 => "{LDP FEC Range 2}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

# Going to create Chained Device Group 3  behind Network Cloud 1 within Topology 1 and renaming of that chained DG to "Provider Edge Router 1"
print "Going to create Chained DG 3 in Topology 1 behind Network Cloud 1 and renaming it\n";
my $device_group_1_1_status = ixiangpf::topology_config ({
    device_group_name          => "{Provider Edge Router 1}",
    device_group_multiplier    => "1",
    device_group_enabled       => "1",
    device_group_handle        => $networkGroup_1_handle,
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_1_1_handle = $HashRef->{'device_group_handle'};

# Creating multivalue loopback adderress within chained DG in Topology 1
print "Creating multivalue for loopback adderress within chained DG\n";
my $multivalue1_1_status = ixiangpf::multivalue_config ({
   pattern              => "counter",
   counter_start        => "201.1.0.1",
   counter_step         => "0.0.0.1",
   counter_direction    => "increment",
   nest_step            => "0.0.0.1,0.0.0.1,0.1.0.0",
   nest_owner           => "$networkGroup_1_handle,$deviceGroup_1_handle,$topology_1_handle",
   nest_enabled         => "0,0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_4_handle = $HashRef->{'multivalue_handle'};

# Creating Loopback behind Chained DG.
print "Creating Loopback behind Chained DG\n";
my $ipv4_loopback_1_status = ixiangpf::interface_config ({
   protocol_name         => "{IPv4 Loopback 1}",
   protocol_handle       => $deviceGroup_1_1_handle,
   enable_loopback       => "1",
   connected_to_handle   => $networkGroup_1_handle,
   intf_ip_addr          => $multivalue_4_handle,
   netmask               => "255.255.255.255",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv4Loopback_1_handle = $HashRef->{'ipv4_loopback_handle'};

# Going to create Chained Device Group 4  behind Network Cloud 1 within Topology 4 and renaming of that chained DG to "Provider Edge Router 2"
print "Going to create Chained DG 4 in Topology 2 behind Network Cloud 2 and renaming it\n";
my $device_group_1_1_status = ixiangpf::topology_config ({
    device_group_name          => "{Provider Edge Router 2}",
    device_group_multiplier    => "1",
    device_group_enabled       => "1",
    device_group_handle        => $networkGroup_2_handle,
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_2_1_handle = $HashRef->{'device_group_handle'};

# Creating multivalue loopback adderress within chained DG in Topology 1
print "Creating multivalue for loopback adderress within chained DG\n";
my $multivalue2_1_status = ixiangpf::multivalue_config ({
   pattern              => "counter",
   counter_start        => "202.1.0.1",
   counter_step         => "0.0.0.1",
   counter_direction    => "increment",
   nest_step            => "0.0.0.1,0.0.0.1,0.1.0.0",
   nest_owner           => "$networkGroup_2_handle,$deviceGroup_2_handle,$topology_2_handle",
   nest_enabled         => "0,0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_6_handle = $HashRef->{'multivalue_handle'};

# Creating Loopback behind Chained DG.
print "Creating Loopback behind Chained DG\n";
my $ipv4_loopback_2_status = ixiangpf::interface_config ({
   protocol_name         => "{IPv4 Loopback 2}",
   protocol_handle       => $deviceGroup_2_1_handle,
   enable_loopback       => "1",
   connected_to_handle   => $networkGroup_2_handle,
   intf_ip_addr          => $multivalue_6_handle,
   netmask               => "255.255.255.255",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv4Loopback_2_handle = $HashRef->{'ipv4_loopback_handle'};

#Adding Targeted Router and LDP PW/VPLS on top of Loopback within Chained device group under topology 1 lsr_id="195.0.0.1",remote_ip_addr ="202.1.0.1",remote_ip_addr_step="0.0.0.1"
print "Adding Targeted Router under topology 1\n";
my $ldp_targeted_router_1_status =ixiangpf::emulation_ldp_config ({
   handle                    =>  $ipv4Loopback_1_handle,
   mode                      =>  "create",
   label_adv                 =>  "unsolicited",
   lsr_id                    =>  "195.0.0.1",
   remote_ip_addr            =>  "202.1.0.1",
   remote_ip_addr_step       =>  "0.0.0.1",
   target_name               =>  "{LDP 3}",
   initiate_targeted_hello   =>  "1",
   targeted_peer_name        =>  "{LDP Targeted Peers 1}",
   lpb_interface_name        =>  "{LDP-IF 3}",
   lpb_interface_active      =>  "1",
}); 
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ldpTargetedRouter_1_handle = $HashRef->{'ldp_targeted_router_handle'};

# Configuration LDP PW/VPLS on top of on top of Targeted Router fec_vc_label_value_start="216", fec_vc_peer_address="202.1.0.1",fec_vc_type="eth",
print "Configuring LDP PW/VPLS on top of on top of Targeted Router\n";
my $ldppwvpls_1_status = ixiangpf::emulation_ldp_route_config ({
   mode                                 =>  "create",
   handle                               =>  $ldpTargetedRouter_1_handle,
   fec_type                             =>  "vc",
   fec_vc_count                         =>  "1",
   fec_vc_fec_type                      =>  "pw_id_fec",
   fec_vc_group_id                      =>  "1",
   fec_vc_id_start                      =>  "1",
   fec_vc_name                          =>  "{LDP PW/VPLS 1}",
   fec_vc_active                        =>  "1",
   fec_vc_label_value_start             =>  "216",
   fec_vc_peer_address                  =>  "202.1.0.1",
   fec_vc_type                          =>  "eth",
   fec_vc_pw_status_code                =>  "clear_fault_code",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ldppwvpls_1_handle = $HashRef->{'ldppwvpls_handle'};

#Adding Targeted Router and LDP PW/VPLS on top of Loopback within Chained device group under topology 1 lsr_id="196.0.0.1",remote_ip_addr ="201.1.0.1",remote_ip_addr_step="0.0.0.1"
print "Adding Targeted Router under topology 1\n";
my $ldp_targeted_router_2_status =ixiangpf::emulation_ldp_config ({
   handle                    =>  $ipv4Loopback_2_handle,
   mode                      =>  "create",
   label_adv                 =>  "unsolicited",
   lsr_id                    =>  "196.0.0.1",
   remote_ip_addr            =>  "201.1.0.1",
   remote_ip_addr_step       =>  "0.0.0.1",
   target_name               =>  "{LDP 4}",
   initiate_targeted_hello   =>  "1",
   targeted_peer_name        =>  "{LDP Targeted Peers 2}",
   lpb_interface_name        =>  "{LDP-IF 4}",
   lpb_interface_active      =>  "1",
}); 
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ldpTargetedRouter_2_handle = $HashRef->{'ldp_targeted_router_handle'};

# Configuration LDP PW/VPLS on top of on top of Targeted Router fec_vc_label_value_start="516", fec_vc_peer_address="201.1.0.1",fec_vc_type="eth",
print "Configuring LDP PW/VPLS on top of on top of Targeted Router\n";
my $ldppwvpls_2_status = ixiangpf::emulation_ldp_route_config ({
   mode                                 =>  "create",
   handle                               =>  $ldpTargetedRouter_2_handle,
   fec_type                             =>  "vc",
   fec_vc_count                         =>  "1",
   fec_vc_fec_type                      =>  "pw_id_fec",
   fec_vc_group_id                      =>  "1",
   fec_vc_id_start                      =>  "1",
   fec_vc_name                          =>  "{LDP PW/VPLS 2}",
   fec_vc_active                        =>  "1",
   fec_vc_label_value_start             =>  "516",
   fec_vc_peer_address                  =>  "201.1.0.1",
   fec_vc_type                          =>  "eth",
   fec_vc_pw_status_code                =>  "clear_fault_code",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ldppwvpls_2_handle = $HashRef->{'ldppwvpls_handle'};

# Configuration of MAC Pool behind Chained Device within Topology 1
print "Configuring CE MAC Pool in Topology 1\n";
my $network_group_5_status =ixiangpf::network_group_config ({
   protocol_handle               =>  "$deviceGroup_1_1_handle",
   protocol_name                 =>  "{CE MAC Cloud 1}",
   connected_to_handle           =>  $ldppwvpls_1_handle,
   type                          =>  "mac-pools",
   mac_pools_mac                 =>  "a0.12.01.00.00.01",
}); 
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_4_handle = $HashRef->{'network_group_handle'};
my $macPools_1_handle = $HashRef->{'mac_pools_handle'};

# Configuration of MAC Pool behind Chained Device within Topology 2
print "Configuring CE MAC Pool in Topology 2\n";
my $network_group_5_status =ixiangpf::network_group_config ({
   protocol_handle               =>  "$deviceGroup_2_1_handle",
   protocol_name                 =>  "{CE MAC Cloud 2}",
   connected_to_handle           =>  $ldppwvpls_2_handle,
   type                          =>  "mac-pools",
   mac_pools_mac                 =>  "a0.11.01.00.00.01",
}); 
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_5_handle = $HashRef->{'network_group_handle'};
my $macPools_2_handle = $HashRef->{'mac_pools_handle'};
print "Waiting 5 seconds before starting protocol(s) ...\n";
sleep(5);

############################################################################
# Start LDP  protocol                                                      #
############################################################################
print "Starting LDP in topology1\n";
ixiangpf::emulation_ldp_control({
    handle => $topology_1_handle,
    mode   => 'start'});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
print "Starting LDP in topology2\n";
ixiangpf::test_control({
    handle => $topology_2_handle,
    action => 'start_protocol',});    
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}    
print "Waiting for 20 seconds\n";
sleep(20);
############################################################################
# Retrieve protocol statistics                                             #
############################################################################
print "Fetching LDP aggregated statistics for Topology 2\n";
my $aggregate_stats = ixiangpf::emulation_ldp_info({
    handle => $ldpTargetedRouter_2_handle,
    mode   => 'stats'
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
# Retrieve protocol learned info                                           #
############################################################################
print "Fetching LDP  aggregated learned info for Topology 1.";
my $learnedinfo = ixiangpf::emulation_ldp_info({
    handle => $ldpTargetedRouter_1_handle,
    mode   => 'lsp_labels'
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
    my $allLi = ixiangpf::status_item($my_key);
    print "==================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "==================================================================\n";
}

############################################################################
# Changing Label in both sides of FEC Ranges                               #
############################################################################
print "Changing Label value for Topology 1 LDP VPN Ranges:\n";
my $ldppwvpls_1_status = ixiangpf::emulation_ldp_route_config ({
    mode                      => "modify",
    handle                    => "$ldppwvpls_2_handle",
    lsp_handle                => "$ldppwvpls_2_handle",
    fec_vc_label_value_start  =>  "5001",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
     my $error = ixiangpf::status_item('log');
     print "Error: $error";
     return "FAILED - $error";
 }    

############################################################################
# Applying changes one the fly                                             #
############################################################################
print "Applying changes on the fly\n";
my $applyChanges = ixiangpf::test_control({
   handle => $ipv4_1_handle,
   action => 'apply_on_the_fly_changes',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(5);
############################################################################
# Retrieve protocol learned info again and notice the difference with      #
# previously retrieved learned info.                                       #
############################################################################
print "Fetching LDP  aggregated learned info for Topology 2.";
$learnedinfo = ixiangpf::emulation_ldp_info({
    handle => $ldpTargetedRouter_1_handle,
    mode   => 'lsp_labels'
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
    my $allLi = ixiangpf::status_item($my_key);
    print "==================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "==================================================================\n";
}
############################################################################
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv4 FEC Range, Destination->IPv4 FEC Range       #
# 2. Type      : Unicast IPv4 traffic                                      #
# 3. Flow Group: On IPv4 Destination Address                               #
# 4. Rate      : 100000 packets per second                                 #
# 5. Frame Size: 64 bytes                                                  #
# 6. Tracking  : Source Destination EndPoint Set                           #
############################################################################
print "Configuring L2-L3 traffic\n";  
$_result_ = ixiangpf::traffic_config({
    mode                                    => 'create',
    traffic_generator                       => 'ixnetwork_540',
    endpointset_count                       => '1',
    emulation_src_handle                    => $macPools_1_handle,
    emulation_dst_handle                    => $macPools_2_handle,
    frame_sequencing                        => 'disable',
    frame_sequencing_mode                   => 'rx_threshold',
    name                                    => 'Traffic_1_Item',
    circuit_endpoint_type                   => 'ethernet_vlan',                              
    rate_pps                                => '100000',                                      
    frame_size                              => '64',                                           
    mac_dst_mode                            => "fixed",
    mac_src_mode                            => "fixed",
    mac_src_tracking                        => "1",
    track_by                                => '{ethernetIiSourceaddress0 trackingenabled0 ethernetIiDestinationaddress0}'
});

@status_keys = ixiahlt::status_item_keys();
    $command_status = ixiahlt::status_item('status');
    if ($command_status != 1) {
        my $error = ixiahlt::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
    }
sleep(5);

############################################################################
# Start L2-L3 traffic configured earlier                                   #
############################################################################
print "Running Traffic...\n";
$_result_ = ixiangpf::traffic_control({
    action              => 'run',
    traffic_generator   => 'ixnetwork_540',
    type                => 'l23',
});

@status_keys = ixiahlt::status_item_keys();
    $command_status = ixiahlt::status_item('status');
    if ($command_status != 1) {
        my $error = ixiahlt::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
    }
print "Let the traffic run for 20 seconds ...\n";
sleep(20);
############################################################################
# Retrieve L2-L3 traffic stats                                             #
############################################################################
print "Retrieving L2-L3 traffic stats\n";
my $protostats = ixiangpf::traffic_stats({
    mode              => 'all',
    traffic_generator => 'ixnetwork_540',
    measure_mode      => 'mixed',
});
@status_keys = ixiahlt::status_item_keys();
    $command_status = ixiahlt::status_item('status');
    if ($command_status != 1) {
        my $error = ixiahlt::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
    }

############################################################################
# Stop L2-L3 traffic started earlier                                       #
############################################################################
print "Stopping Traffic...\n";
$_result_ = ixiangpf::traffic_control({
    action            => 'stop',
    traffic_generator => 'ixnetwork_540',
    type              => 'l23',
});

@status_keys = ixiahlt::status_item_keys();
    $command_status = ixiahlt::status_item('status');
    if ($command_status != 1) {
        my $error = ixiahlt::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
    }
sleep(5);
############################################################################
# Stop all protocols                                                       #
############################################################################
print "Stopping all protocol(s) ...\n";
my $stop_status = ixiangpf::test_control({
    action      => "stop_all_protocols",
});

@status_keys = ixiahlt::status_item_keys();
    $command_status = ixiahlt::status_item('status');
    if ($command_status != 1) {
        my $error = ixiahlt::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
    }
sleep(2);

print "!!! Test Script Ends !!!\n";           
print "SUCCESS - $0\n";         