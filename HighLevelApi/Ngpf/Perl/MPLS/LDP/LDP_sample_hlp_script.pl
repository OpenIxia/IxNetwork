################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
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
#    This script intends to demonstrate how to use NGPF OSPFv2 API.            #
#                                                                              #
#    1. It will create 2 OSPFv2 topologies, each having an ipv4 network        #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start the ospfv2 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Enable the Ospfv2 simulated topologies External Route type1, which     #
#       was disabled by default and apply change on the fly.                   #
#    6. Retrieve protocol learned info again and notice the difference with    #
#       previously retrieved learned info.                                     #
#    7. Configure L2-L3 traffic.                                               #
#    8. Start the L2-L3 traffic.                                               #
#    9. Retrieve L2-L3 traffic stats.                                          #
#   10. Stop L2-L3 traffic.                                                    #
#   11. Stop all protocols.                                                    # #                                                                              #           
# Ixia Software:                                                               #
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
my @chassis             = ('10.216.108.82');
my $tcl_server          = '10.216.108.82';
my @port_list           = ([ '8/3', '8/4' ]);
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
    topology_name      => "{ldp Topology 1}",
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
    device_group_name            => "{ldp Topology 1 Router}",
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
    topology_name      => "{ldp Topology 2}",
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
    device_group_name            => "{ldp Topology 2 Router}",
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
    gateway_step                      => "0.0.0.0",
    intf_ip_addr                      => "20.20.20.2",
    intf_ip_addr_step                 => "0.0.0.0",
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
    gateway_step                      => "0.0.0.0",
    intf_ip_addr                      => "20.20.20.1",
    intf_ip_addr_step                 => "0.0.0.0",
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

# Configuration of LDP Router and LDP Interface for the first Device Group with label space = 30, hello interval= 10, hold time = 45, keepalive interval = 30, keepalive holdtime =30
print "Creating LDP Router for 1st Device Group\n";
my $ldp_basic_router_1_status = ixiangpf::emulation_ldp_config ({
    handle                       => "$ipv4_1_handle",
    mode                         => "create",
    label_adv                    => "unsolicited",
    lsr_id                       => "193.0.0.1",
    label_space                  => "30",
    hello_interval               => "10",
    hello_hold_time              => "30",
    keepalive_interval           => "30",
    keepalive_holdtime           => "45",
    interface_name               => "{LDP-IF 1}",
    interface_multiplier         => "1",
    interface_active             => "1",
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

print "Creating LDP Router for 2nd Device Group\n";
my $ldp_basic_router_2_status = ixiangpf::emulation_ldp_config ({
    handle                       => "$ipv4_2_handle",
    mode                         => "create",
    label_adv                    => "unsolicited",
    lsr_id                       => "194.0.0.1",
    label_space                  => "30",
    hello_interval               => "10",
    hello_hold_time              => "30",
    keepalive_interval           => "30",
    keepalive_holdtime           => "45",
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

# Configuration of IPv4 Prefix which will used as FEC Range for the first Device Group with ipv4_prefix_network_address = "201.1.0.1
print "Creating multivalue for IPv4 prefix LDP_1_Network_Group\n";
my $network_group_1_status = ixiangpf::network_group_config ({
   protocol_handle                      => "$deviceGroup_1_handle",
   protocol_name                        => "LDP_1_Network_Group",
   multiplier                           => "10",
   enable_device                        => "1",
   connected_to_handle                  => "$ethernet_1_handle",
   type                                 => "ipv4-prefix",
   ipv4_prefix_network_address          => "201.1.0.0",
   ipv4_prefix_length                   => "24",
   ipv4_prefix_number_of_addresses      => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_1_handle = ixiangpf::status_item('network_group_handle');
my $ipv4PrefixPools_1_handle = ixiangpf::status_item('ipv4_prefix_pools_handle');

# Modifying FEC Range Parameters label value start =516
print "Modifying LDP FEC Ranges info for LDP_1_Network_Group\n";
my $network_group_2_status = ixiangpf::emulation_ldp_route_config ({
    mode                        => "modify",
    handle                      => "$networkGroup_1_handle",
    fec_type                    => "ipv4_prefix",
    label_value_start           => "516",
    label_value_start_step      => "1",
    lsp_handle                  => "$networkGroup_1_handle",
    fec_name                    => "{LDP FEC Range 1}",    
    });
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $fec_handle_1 = ixiangpf::status_item('fecproperty_handle');
# Configuration of IPv4 Prefix which will used as FEC Range for the second Device Group with ipv4_prefix_network_address = "202.1.0.1
print "Creating multivalue for IPv4 prefix LDP_2_Network_Group\n";
$network_group_1_status = ixiangpf::network_group_config ({
   protocol_handle                      => "$deviceGroup_2_handle",
   protocol_name                        => "LDP_2_Network_Group",
   multiplier                           => "10",
   enable_device                        => "1",
   connected_to_handle                  => "$ethernet_2_handle",
   type                                 => "ipv4-prefix",
   ipv4_prefix_network_address          => "202.1.0.0",
   ipv4_prefix_length                   => "24",
   ipv4_prefix_number_of_addresses      => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_2_handle = ixiangpf::status_item('network_group_handle');
my $ipv4PrefixPools_2_handle = ixiangpf::status_item('ipv4_prefix_pools_handle');

# Modifying FEC Range Parameters with label_value_start="216"
print "Modifying LDP FEC Ranges info for LDP_2_Network_Group\n";
$network_group_2_status = ixiangpf::emulation_ldp_route_config ({
    mode                        => "modify",
    handle                      => "$networkGroup_2_handle",
    fec_type                    => "ipv4_prefix",
    label_value_start           => "216",
    label_value_start_step      => "1",
    lsp_handle                  => "$networkGroup_2_handle",
    fec_name                    => "{LDP FEC Range 2}",    
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $fec_handle_2 = ixiangpf::status_item('fecproperty_handle');
# Creating multivalue for Device Group 3 for multiplier 10 
print "Creating multivalue for Device Group 3\n";
$device_group_2_status = ixiangpf::topology_config ({
    device_group_name            => "{Device Group 3}",
    device_group_multiplier      => "10",
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
$deviceGroup_2_handle = ixiangpf::status_item('device_group_handle');
# Creating of Chained Device Group for configuration of loopback behind first Device Group
print "Creating IPv4 loopback for configuring L4-L7 App Traffic for Topology 1\n";
my $ipv4_loopback_1_status = ixiangpf::interface_config ({
    protocol_name            => "{IPv4 Loopback 1}",
    protocol_handle          => "$deviceGroup_2_handle",
    enable_loopback          => "1",
    connected_to_handle      => "$networkGroup_1_handle",
    intf_ip_addr             => "201.1.0.0",
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
# # Creating multivalue for Device Group 4 for multiplier 10  
print "Creating multivalue for Device Group 4\n";
my $device_group_4_status = ixiangpf::topology_config ({
        device_group_name            => "{Device Group 4}",
        device_group_multiplier      => "10",
        device_group_enabled         => "1",
        device_group_handle          => "$networkGroup_2_handle",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_4_handle = ixiangpf::status_item('device_group_handle');
# Creating of Chained Device Group for configuration of loopback behind second Device Group
print "Creating IPv4 loopback for configuring L4-L7 App Traffic for Topology 2\n";
my $ipv4_loopback_2_status = ixiangpf::interface_config ({
    protocol_name            => "{IPv4 Loopback 2}",
    protocol_handle          => "$deviceGroup_4_handle",
    enable_loopback          => "1",
    connected_to_handle      => "$networkGroup_2_handle",
    intf_ip_addr             => "202.1.0.0",
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
print "Fetching LDP aggregated statistics for Topology 1\n";
my $aggregate_stats = ixiangpf::emulation_ldp_info({
    handle => $ldpBasicRouter_1_handle,
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
print "Fetching LDP  aggregated learned info for Topology 2.";
my $learnedinfo = ixiangpf::emulation_ldp_info({
    handle => $ldpBasicRouter_2_handle,
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
print "Changing Label value for Topology 2 LDP  FEC Ranges:";
$network_group_2_status = ixiangpf::emulation_ldp_route_config ({
    handle                               => $fec_handle_2,
    mode                                 => "modify",
    label_value_start                    => "5016",
    label_value_start_step               => "100",
    lsp_handle                           => $fec_handle_2,
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
print "Fetching LDP  aggregated learned info for Topology 1.";
$learnedinfo = ixiangpf::emulation_ldp_info({
    handle => $ldpBasicRouter_1_handle,
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
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : Source Destination EndPoint Set                           #
############################################################################
print "Configuring L2-L3 traffic\n";  
$_result_ = ixiahlt::traffic_config({
    mode                                    => 'create',
    traffic_generator                       => 'ixnetwork_540',
    endpointset_count                       => '1',
    emulation_src_handle                    => $ipv4PrefixPools_1_handle,
    emulation_dst_handle                    => $ipv4PrefixPools_2_handle,
    frame_sequencing                        => 'disable',
    frame_sequencing_mode                   => 'rx_threshold',
    name                                    => 'Traffic_1_Item',
    circuit_endpoint_type                   => 'ipv4',
    transmit_distribution                   => 'ipv4DestIp0',                               
    rate_pps                                => '1000',                                      
    frame_size                              => '512',                                       
    track_by                                => '{sourceDestEndpointPair0 trackingenabled0}'
});
    
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

############################################################################
# Start L2-L3 traffic configured earlier                                   #
############################################################################
print "Running Traffic...\n";
$_result_ = ixiahlt::traffic_control({
    action              => 'run',
    traffic_generator   => 'ixnetwork_540',
    type                => 'l23',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Let the traffic run for 20 seconds ...\n";
sleep(20);
############################################################################
# Retrieve L2-L3 traffic stats                                             #
############################################################################
print "Retrieving L2-L3 traffic stats\n";
my $protostats = ixiahlt::traffic_stats({
    mode              => 'all',
    traffic_generator => 'ixnetwork_540',
    measure_mode      => 'mixed',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}   
@status_keys = ixiahlt::status_item_keys();
 foreach (@status_keys) {
    my $my_key = $_;
    my $allStats = ixiahlt::status_item($my_key);
    print "==================================================================\n";
    print "\n$my_key: $allStats\n\n";
    print "==================================================================\n";
 }
############################################################################
# Stop L2-L3 traffic started earlier                                       #
############################################################################
print "Stopping Traffic...\n";
$_result_ = ixiahlt::traffic_control({
    action            => 'stop',
    traffic_generator => 'ixnetwork_540',
    type              => 'l23',
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
# Stop all protocols                                                       #
############################################################################
print "Stopping all protocol(s) ...\n";
ixiahlt::test_control({action => 'stop_all_protocols'});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(2);

print "!!! Test Script Ends !!!\n";           
print "SUCCESS - $0\n";         
