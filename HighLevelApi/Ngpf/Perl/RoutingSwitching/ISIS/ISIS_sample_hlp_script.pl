################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/01/2015 - Poulomi Chatterjee - created sample                          #
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
#                                                                              #
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
#    This script intends to demonstrate how to use NGPF ISISL3 HLP API.        #
#                                                                              #
#    1. It will create 2 ISISL3 topologies, each having an IPv4 & IPv6 network #
#       topology and loopback device group behind the network group(NG) with   #
#       loopback interface on it. A loopback device group (DG) behind network  #
#       group is needed to support applib traffic.                             #
#    2. Start ISISL3 protocol.                                                 #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Configure L2-L3 traffic (IPv4 & IPv6).                                 #
#    6. Configure application traffic for IPv4/IPv6 Profile. [global variable  #
#       "traffic_mode" selects the profile to be configured.                   #
#       Options are: 1(for IPv4) & 2(for IPv6)                                 # 
#       Note: IPv4 & IPv6 both could not be configured in same endpoint set.   #
#    7. Start L2-L3 traffic.                                                   #
#    8. Start application traffic.                                             #
#    9. Retrieve Application traffic stats.                                    #
#   10. Retrieve L2-L3 traffic stats.                                          #
#   11. Stop L2-L3 traffic.                                                    #
#   12. Stop Application traffic.                                              #
#   13. Stop all protocols.                                                    #
# Ixia Software:                                                               #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################


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
print "Connecting to chassis ...\n";
my @chassis             = ('10.205.28.170');
my $tcl_server          = '10.205.28.170';
my @port_list           = ([ '1/5', '1/6' ]);
my $ixNetwork_client    = '10.205.28.41:8982';

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
# Configure Topology, Device Group                                             # 
################################################################################
# Creating a topology in first port
print "Adding topology 1 in port 1\n";
my $topology_1_status = ixiangpf::topology_config ({
        topology_name      => "{ISIS Topology 1}",
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
        topology_name      => "{ISIS Topology 2}",
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
my $device_group_4_status = ixiangpf::topology_config ({
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
my $deviceGroup_4_handle = $HashRef->{'device_group_handle'};

################################################################################
#  Configure protocol interfaces                                               #
################################################################################

# Creating ethernet stack in device group
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
    
# Creating ethernet stack in device group
print "Creating ethernet stack in second device group\n";
my $ethernet_2_status = ixiangpf::interface_config ({
        protocol_name                => "{Ethernet 2}",
        protocol_handle              => "$deviceGroup_4_handle",
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
        gateway                           => "20.20.20.2",
        intf_ip_addr                      => "20.20.20.1",
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
print "Creating IPv4  stack on second ethernet stack\n";
my $ipv4_2_status = ixiangpf::interface_config ({
        protocol_name                     => "{IPv4 2}",
        protocol_handle                   => "$ethernet_2_handle",
        ipv4_resolve_gateway              => "1",
        ipv4_manual_gateway_mac           => "00.00.00.00.00.01",
        ipv4_manual_gateway_mac_step      => "00.00.00.00.00.00",
        gateway                           => "20.20.20.1",
        intf_ip_addr                      => "20.20.20.2",
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
################################################################################
# Creating  ISIS Stack on top of ethernet stack                                #
# Descrtiption of protocol arguments : discard_lsp: enables learning LSPs      #
#                                      intf_type: sets interface type          #
#                                      system_id: sets system id               #   
#                                      protocol_name: sets prtoocol name       # 
#                                      active: activates ISIS router           #
#                                      if_active: activates router interface   #
################################################################################
print "Creating ISIS Stack on top of ethernet 1 stack\n";

my $isis_l3_1_status = ixiangpf::emulation_isis_config ({
        mode                                 => "create",
        discard_lsp                          => "0",
        handle                               => "$ethernet_1_handle",
        intf_type                            => "ptop",
        system_id                            => "67:01:00:01:00:00",
        protocol_name                        => "{ISIS-L3 IF 1}",
        active                               => "1",
        if_active                            => "1",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}

my $isisL3_1_handle = $HashRef->{'isis_l3_handle'};
    
# Creating ISIS Network Group in port 1
print "Creating ISIS IPv4 Network group in port 1\n"; 
my $network_group_1_status = ixiangpf::network_group_config ({
        protocol_handle                      => "$deviceGroup_1_handle",
        protocol_name                        => "{ISIS Network Group 1}",
        enable_device                        => "1",
        connected_to_handle                  => "$ethernet_1_handle",
        type                                 => "ipv4-prefix",
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
    
my $network_group_2_status = ixiangpf::emulation_isis_network_group_config ({
        handle                  => "$networkGroup_1_handle",
        mode                    => "modify",
        stub_router_origin      => "stub",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}    
my $device_group_2_status = ixiangpf::topology_config ({
        device_group_name            => "{Device Group 3}",
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
my $deviceGroup_2_handle = $HashRef->{'device_group_handle'};
    
# Creating ipv4 Loopback interface for applib traffic
print "Adding ipv4 loopback1 for applib traffic\n"; 
my $ipv4_loopback_1_status = ixiangpf::interface_config ({
        protocol_name            => "{IPv4 Loopback 1}",
        protocol_handle          => "$deviceGroup_2_handle",
        enable_loopback          => "1",
        connected_to_handle      => "$networkGroup_1_handle",
        intf_ip_addr             => "6.6.6.6",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $ipv4Loopback_1_handle = $HashRef->{'ipv4_loopback_handle'};

# Creating ISIS Network group 3 for ipv6 ranges
print "Creating ISIS Network group 3 for ipv6 ranges\n";    
my $network_group_3_status = ixiangpf::network_group_config ({
        protocol_handle                      => "$deviceGroup_1_handle",
        protocol_name                        => "{ISIS Network Group 3}",
        connected_to_handle                  => "$ethernet_1_handle",
        type                                 => "ipv6-prefix",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $networkGroup_3_handle = $HashRef->{'network_group_handle'};
my $ipv6PrefixPools_1_handle = $HashRef->{'ipv6_prefix_pools_handle'};
    
my $network_group_4_status = ixiangpf::emulation_isis_network_group_config ({
        handle                      => "$networkGroup_3_handle",
        mode                        => "modify",
        external_router_origin      => "stub",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}    
my $device_group_3_status = ixiangpf::topology_config ({
        device_group_name            => "{Device Group 6}",
        device_group_multiplier      => "1",
        device_group_enabled         => "1",
        device_group_handle          => "$networkGroup_3_handle",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $deviceGroup_3_handle = $HashRef->{'device_group_handle'};
    
#Creating ipv6 loopback 1 interface for applib traffic
print "Adding ipv6 loopback1 for applib traffic\n";    
my $ipv6_loopback_1_status = ixiangpf::interface_config ({
        protocol_name            => "{IPv6 Loopback 2}",
        protocol_handle          => "$deviceGroup_3_handle",
        enable_loopback          => "1",
        connected_to_handle      => "$networkGroup_3_handle",
        ipv6_intf_addr           => "2223:0:1:0:0:0:0:1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $ipv6Loopback_1_handle = $HashRef->{'ipv6_loopback_handle'};
################################################################################
# Creating  ISIS Stack on top of ethernet stack                                #
# Descrtiption of protocol arguments : discard_lsp: enables learning LSPs      #
#                                      intf_type: sets interface type          #
#                                      routing_level: sets routing level       #
#                                      system_id: sets system id               #   
#                                      protocol_name: sets prtoocol name       # 
#                                      active: activates ISIS router           #
#                                      if_active: activates router interface   #
################################################################################    
print "Creating ISIS Stack on top of Ethernet 2 stack\n";    

my $isis_l3_2_status = ixiangpf::emulation_isis_config ({
        mode                                 => "create",
        discard_lsp                          => "0",
        handle                               => "$ethernet_2_handle",
        intf_type                            => "ptop",
        routing_level                        => "L2",
        system_id                            => "68:01:00:01:00:00",
        protocol_name                        => "{ISIS-L3 IF 2}",
        active                               => "1",
        if_active                            => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $isisL3_2_handle = $HashRef->{'isis_l3_handle'};
    
# Creating IPv4 Prefix Ranges
print "Creating ISIS IPv4 Prefix Ranges\n";    
my $network_group_5_status = ixiangpf::network_group_config ({
        protocol_handle                      => "$deviceGroup_4_handle",
        protocol_name                        => "{ISIS Network Group 2}",
        multiplier                           => "1",
        enable_device                        => "1",
        connected_to_handle                  => "$ethernet_2_handle",
        type                                 => "ipv4-prefix",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $networkGroup_5_handle = $HashRef->{'network_group_handle'};
my $ipv4PrefixPools_3_handle = $HashRef->{'ipv4_prefix_pools_handle'};
    
my $network_group_6_status = ixiangpf::emulation_isis_network_group_config ({
        handle                  => "$networkGroup_5_handle",
        mode                    => "modify",
        stub_router_origin      => "stub",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}    

# Creating a device group in topology for loopback interface
print "Creating device group 2 in topology 2 for loopback interface\n";
my $device_group_5_status = ixiangpf::topology_config ({
        device_group_name            => "{Device Group 4}",
        device_group_multiplier      => "1",
        device_group_enabled         => "1",
        device_group_handle          => "$networkGroup_5_handle",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $deviceGroup_5_handle = $HashRef->{'device_group_handle'};
    
#Creating ipv4 loopback 2 for applib traffic
print "Adding ipv4 loopback2 for applib traffic\n";    
my $ipv4_loopback_2_status = ixiangpf::interface_config ({
        protocol_name            => "{IPv4 Loopback 2}",
        protocol_handle          => "$deviceGroup_5_handle",
        enable_loopback          => "1",
        connected_to_handle      => "$networkGroup_5_handle",
        intf_ip_addr             => "7.7.7.7",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $ipv4Loopback_2_handle = $HashRef->{'ipv4_loopback_handle'};
    
# Creating ISIS Prefix ranges
print "Creating ISIS IPv6 Prefix ranges\n"; 
my $network_group_7_status = ixiangpf::network_group_config ({
        protocol_handle                      => "$deviceGroup_4_handle",
        protocol_name                        => "{ISIS Network Group 4}",
        connected_to_handle                  => "$ethernet_2_handle",
        type                                 => "ipv6-prefix",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $networkGroup_7_handle = $HashRef->{'network_group_handle'};
my $ipv6PrefixPools_3_handle = $HashRef->{'ipv6_prefix_pools_handle'};
    
my $network_group_8_status = ixiangpf::emulation_isis_network_group_config ({
        handle                      => "$networkGroup_7_handle",
        mode                        => "modify",
        external_router_origin      => "stub",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}    

# Creating a device group in topology for loopback interface
print "Creating device group 2 in topology 2 for loopback interface\n";   
my $device_group_6_status = ixiangpf::topology_config ({
        device_group_name            => "{Device Group 5}",
        device_group_multiplier      => "1",
        device_group_enabled         => "1",
        device_group_handle          => "$networkGroup_7_handle",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $deviceGroup_6_handle = $HashRef->{'device_group_handle'};
   
 
my $ipv6_loopback_2_status = ixiangpf::interface_config ({
        protocol_name            => "{IPv6 Loopback 1}",
        protocol_handle          => "$deviceGroup_6_handle",
        enable_loopback          => "1",
        connected_to_handle      => "$networkGroup_7_handle",
        ipv6_multiplier          => "1",
        ipv6_intf_addr           => "2223:0:0:0:0:0:0:1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
}
my $ipv6Loopback_2_handle = $HashRef->{'ipv6_loopback_handle'};

print "Waiting 5 seconds before starting protocol(s) ...\n";
sleep(5);
sleep(5);
############################################################################
# Start All protocol                                                       #
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
print "Waiting for 30 seconds\n";
sleep(30);

############################################################################
# Retrieve protocol statistics                                             # 
############################################################################
print "Fetching ISISL3 aggregated statistics\n";
my $protostats = ixiangpf::emulation_isis_info({
        handle => $isisL3_1_handle,
        mode   => 'stats'}); 
    @status_keys = ixiangpf::status_item_keys();
    foreach (@status_keys) {
        my $my_key = $_;
        my $allStats = ixiangpf::status_item($my_key);
        print "==================================================================\n";
        print "\n$my_key: $allStats\n\n";
        print "==================================================================\n";
    }
    
################################################################################
# Configure_L2_L3_IPv4                                                         #
################################################################################
print "Configure L2-L3 IPv4 traffic\n";

$_result_ = ixiangpf::traffic_config({
        mode 					    => 'create',
        traffic_generator 			=> 'ixnetwork_540',
        endpointset_count 			=> 1,
        emulation_src_handle 		=> [[$ipv4PrefixPools_1_handle]],
        emulation_dst_handle 		=> [[$ipv4PrefixPools_3_handle]],
        name 					    => 'TI0-Traffic_Item_1',
        circuit_endpoint_type 		=> 'ipv4',
        track_by                    => 'trackingenabled0 ipv4DestIp0',
        frame_size                  => '512',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
    
my @current_config_elements1 = ixiangpf::status_item('traffic_item');
my $current_config_element1 = $current_config_elements1[0];
    

################################################################################
# Configure_L2_L3_IPv6                                                         #
################################################################################
print "Configure L2-L3 IPv6 traffic\n";

$_result_ = ixiangpf::traffic_config({
        mode 					    => 'create',
        traffic_generator 			=> 'ixnetwork_540',
        endpointset_count 			=> 1,
        emulation_src_handle 		=> [[$ipv6PrefixPools_1_handle]],
        emulation_dst_handle 		=> [[$ipv6PrefixPools_3_handle]],
        name 					    => 'TI1-Traffic_Item_2',
        circuit_endpoint_type 		=> 'ipv6',
        frame_size                  => '512',
        track_by                    => 'trackingenabled0 ipv6DestIp0',
});
    
my @current_config_elements = ixiangpf::status_item('traffic_item');
my $current_config_element = $current_config_elements[0];
    
################################################################################
# Configure_L4_L7 traffic                                                      #
################################################################################
# Set applib traffic mode
print "Set applib traffic mode in variable traffic_mode, for IPv4: 1, IPv6: 2\n";
my $traffic_mode = 1;

if ($traffic_mode == 1) {
    print "################################################################################\n";
    print "Configure_L4_L7_IPv4\n";
    print "################################################################################\n";
    print "Traffic_mode = IPv4\n";
    print "Configure L4-L7 IPv4 traffic\n";
    my $traffic_item_1_status = ixiangpf::traffic_l47_config ({
        mode                        => "create",
        name                        => "{Traffic Item 2}",
        circuit_endpoint_type       => "ipv4_application_traffic",
        emulation_src_handle        => $networkGroup_1_handle,
        emulation_dst_handle        => $networkGroup_5_handle,
        objective_type              => "users",
        objective_value             => "100",
        objective_distribution      => "apply_full_objective_to_each_port",
        enable_per_ip_stats         => "0",
        flows                       => "{Bandwidth_BitTorrent_File_Download Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4 Bandwidth_POP3 Bandwidth_Radius Bandwidth_Raw Bandwidth_Telnet Bandwidth_uTorrent_DHT_File_Download BBC_iPlayer BBC_iPlayer_Radio BGP_IGP_Open_Advertise_Routes BGP_IGP_Withdraw_Routes Bing_Search BitTorrent_Ares_v217_File_Download BitTorrent_BitComet_v126_File_Download BitTorrent_Blizzard_File_Download BitTorrent_Cisco_EMIX BitTorrent_Enterprise BitTorrent_File_Download BitTorrent_LimeWire_v5516_File_Download BitTorrent_RMIX_5M}",
    });

    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
    }
} elsif ($traffic_mode == 2) {
    print "################################################################################\n";
    print "Configure_L4_L7_IPv6\n";
    print "################################################################################\n";
    print "Traffic_mode = IPv6\n";
    print "Configure L4-L7 IPv6 traffic\n";
    my $traffic_item_2_status = ixiangpf::traffic_l47_config ({
        mode                        => "create",
        name                        => "{Traffic Item 2}",
        circuit_endpoint_type       => "ipv6_application_traffic",
        emulation_src_handle        => $networkGroup_3_handle,
        emulation_dst_handle        => $networkGroup_7_handle,
        objective_type              => "users",
        objective_value             => "100",
        objective_distribution      => "apply_full_objective_to_each_port",
        enable_per_ip_stats         => "0",
        flows                       => "{Bandwidth_BitTorrent_File_Download Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4 Bandwidth_POP3 Bandwidth_Radius Bandwidth_Raw Bandwidth_Telnet Bandwidth_uTorrent_DHT_File_Download BBC_iPlayer BBC_iPlayer_Radio BGP_IGP_Open_Advertise_Routes BGP_IGP_Withdraw_Routes Bing_Search BitTorrent_Ares_v217_File_Download BitTorrent_BitComet_v126_File_Download BitTorrent_Blizzard_File_Download BitTorrent_Cisco_EMIX BitTorrent_Enterprise BitTorrent_File_Download BitTorrent_LimeWire_v5516_File_Download BitTorrent_RMIX_5M}",
    });

    $HashRef = ixiangpf::get_result_hash();
    $command_status = $HashRef->{'status'};
    if ($command_status != $ixiangpf::SUCCESS) {
        my $error = ixiangpf::status_item('log');
        print "Error: $error";
        return "FAILED - $error";
    }
}
############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
print "Running Traffic...\n";
$_result_ = ixiangpf::traffic_control({
        action 			    => 'run',
        traffic_generator 	=> 'ixnetwork_540',
        type 			    => 'l23',
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
#  Start L4-L7 traffic configured earlier                                  #
############################################################################
print "Running Traffic...\n";
$_result_ = ixiangpf::traffic_control({
        action 			=> 'run',
        traffic_generator 	=> 'ixnetwork_540',
        type 			=> 'l47',
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
print "Retrieving All traffic stats\n";
$protostats = ixiangpf::traffic_stats({
    	mode 				    => 'all',
        traffic_generator 		=> 'ixnetwork_540',
        measure_mode 			=> 'mixed'
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
# Stop L2-L3 traffic started earlier                                       #
############################################################################
print "Stopping Traffic...\n";
$_result_ = ixiangpf::traffic_control({
        action 			    => 'stop',
        traffic_generator 	=> 'ixnetwork_540',
        type 			    => 'l23',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
    
############################################################################
# Stop L4-L7 traffic started earlier                                       #
############################################################################
print "Stopping Traffic...\n";
$_result_ = ixiangpf::traffic_control({
        action 			    => 'stop',
        traffic_generator 	=> 'ixnetwork_540',
        type 			    => 'l47',
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
my $stop_status = ixiangpf::test_control({
    action      => "stop_all_protocols",
});
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

