################################################################################
# Version 1.0    $Revision: #1 $                                               #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    06/10/2016 - Debarati Chakraborty - created sample                        #
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
#    This script intends to demonstrate how to use NGPF BGP RFC 3107, Add-Path,#
#    AIGP APIs                                                                 #
#    About Topology:                                                           #
#       The scenario consists of two BGP peers.                                #
#       Each of them capable of carrying Label information for the attached    #
#       advertising Route Range. Unidirectional Traffic is created in between  #
#       the peers.                                                             #
#         Script Flow:                                                         #
#        Step 1. Creation of 2 BGP topologies with RFC3107 IPv4 MPLS, AIGP,    #
#                Add-Path Capabilities                                         #
#        Step 2. Start of protocol                                             #
#        Step 3. Fetch Learned Info and fetch statistics.                      #
#        Step 4. Configuration L2-L3 Traffic                                   #
#        Step 5. Apply and Start of L2-L3 traffic                              #
#        Step 6. Display of L2-L3  traffic Stats                               #
#        Step 7. StopL2-L3 traffic and stop protocols.                         #
# Ixia Software:                                                               #
#    IxOS      8.10-EA                                                         #
#    IxNetwork 8.10-EA-Update(3)                                               #
################################################################################
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
my @chassis             = ('10.216.108.46');
my $tcl_server          = '10.216.25.8';
my @port_list           = ([ '1/3', '1/4' ]);
my $ixNetwork_client    = '10.216.25.8:8239';

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
    gateway                           => "100.1.0.1",
    gateway_step                      => "0.0.0.0",
    intf_ip_addr                      => "100.1.0.2",
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
$ipv4_1_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv4 2}",
    protocol_handle                   => "$ethernet_2_handle",
    ipv4_resolve_gateway              => "1",
    ipv4_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv4_manual_gateway_mac_step      => "00.00.00.00.00.00",
    gateway                           => "100.1.0.2",
    gateway_step                      => "0.0.0.0",
    intf_ip_addr                      => "100.1.0.1",
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
my $bgp_ipv4_peer_1_status = ixiangpf::emulation_bgp_config ({
        mode                                    => "enable",
        active                                  => "1",
        handle                                  => "$ipv4_1_handle",
        ip_version                              => "4",
        remote_ip_addr                          => "100.1.0.1",
        ipv4_capability_unicast_nlri            => "1",
        ipv4_filter_unicast_nlri                => "0",
        ipv4_filter_multicast_nlri              => "1",
        ipv4_capability_mpls_nlri               => "1",
        ipv4_filter_mpls_nlri                   => "1",
        ipv4_capability_mpls_vpn_nlri           => "1",
        ipv6_capability_unicast_nlri            => "1",
        ipv6_filter_unicast_nlri                => "1",
        ipv6_filter_multicast_nlri              => "1",
        ipv6_capability_mpls_nlri               => "1",
        ipv6_filter_mpls_nlri                   => "1",
        ipv6_capability_mpls_vpn_nlri           => "1",
        capability_route_refresh                => "1",
        ttl_value                               => "64",
        updates_per_iteration                   => "1",
        ipv4_mpls_add_path_mode                 => "sendonly",
        ipv6_mpls_add_path_mode                 => "sendonly",
        ipv4_unicast_add_path_mode              => "sendonly",
        ipv6_unicast_add_path_mode              => "sendonly",
        ipv4_mpls_capability                    => "1",
        capability_ipv4_mpls_add_path           => "1",
});

$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgpIpv4Peer_1_handle = $HashRef->{'bgp_handle'};

print "Creating BGP Stack on top of IPv4 Stack in Topology 2\n";
my $bgp_ipv4_peer_2_status = ixiangpf::emulation_bgp_config ({
        mode                                    => "enable",
        active                                  => "1",
        handle                                  => "$ipv4_2_handle",
        ip_version                              => "4",
        remote_ip_addr                          => "100.1.0.2",
        ipv4_capability_unicast_nlri            => "1",
        ipv4_filter_unicast_nlri                => "0",
        ipv4_filter_multicast_nlri              => "1",
        ipv4_capability_mpls_nlri               => "1",
        ipv4_filter_mpls_nlri                   => "1",
        ipv4_capability_mpls_vpn_nlri           => "1",
        ipv6_capability_unicast_nlri            => "1",
        ipv6_filter_unicast_nlri                => "1",
        ipv6_filter_multicast_nlri              => "1",
        ipv6_capability_mpls_nlri               => "1",
        ipv6_filter_mpls_nlri                   => "1",
        ipv6_capability_mpls_vpn_nlri           => "1",
        capability_route_refresh                => "1",
        ipv4_mpls_add_path_mode                 => "receiveonly",
        ipv6_mpls_add_path_mode                 => "receiveonly",
        ipv4_unicast_add_path_mode              => "receiveonly",
        ipv6_unicast_add_path_mode              => "receiveonly",
        ipv4_mpls_capability                    => "1",
        capability_ipv4_mpls_add_path           => "1",
    });
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $bgpIpv4Peer_2_handle = $HashRef->{'bgp_handle'};

# Creating multivalue for network group
print "Creating multivalue pattern for BGP network group on Port 1\n";
my $multivalue_4_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "205.1.0.1",
    counter_step           => "0.1.0.0",
    counter_direction      => "increment",
    nest_step              => "0.0.0.1,0.1.0.0",
    nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_4_handle = $HashRef->{'multivalue_handle'};

print "Creating multivalue pattern for BGP network group on Port 2\n";
my $multivalue_5_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "206.1.0.1",
    counter_step           => "0.1.0.0",
    counter_direction      => "increment",
    nest_step              => "0.0.0.1,0.1.0.0",
    nest_owner             => "$deviceGroup_2_handle,$topology_2_handle",
    nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_5_handle = $HashRef->{'multivalue_handle'};

# Creating BGP Network Group 
print "Creating BGP Network Group on Port 1\n";   
my $network_group_1_status = ixiangpf::network_group_config ({
    protocol_handle                      => "$deviceGroup_1_handle",
    protocol_name                        => "BGP_1_Network_Group1",
    multiplier                           => "5",
    enable_device                        => "1",
    connected_to_handle                  => "$ethernet_1_handle",
    type                                 => "ipv4-prefix",
    ipv4_prefix_network_address          => "$multivalue_4_handle",
    ipv4_prefix_length                   => "24",
    ipv4_prefix_number_of_addresses      => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_1_handle = $HashRef->{'network_group_handle'};
my $ipv4PrefixPools_1_handle = $HashRef->{'ipv4_prefix_pools_handle'};

print "Creating BGP Network Group on Port 2\n";
my $network_group_3_status = ixiangpf::network_group_config ({
        protocol_handle                      => "$deviceGroup_2_handle",
        protocol_name                        => "{Network Group 2}",
        multiplier                           => "5",
        enable_device                        => "1",
        connected_to_handle                  => "$ethernet_2_handle",
        type                                 => "ipv4-prefix",
        ipv4_prefix_network_address          => "$multivalue_5_handle",
        ipv4_prefix_length                   => "24",
        ipv4_prefix_number_of_addresses      => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_3_handle = $HashRef->{'network_group_handle'};
my $ipv4PrefixPools_2_handle = $HashRef->{'ipv4_prefix_pools_handle'};
	
# Creating multivalue for network group
print "Creating multivalue pattern for BGP network group on Port 1\n";
my $multivalue_6_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "1096",
        counter_step           => "10",
        counter_direction      => "increment",
        nest_step              => "1,1",
        nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
        nest_enabled           => "0,0",
    });
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_6_handle = $HashRef->{'multivalue_handle'};
    
my $multivalue_7_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "1111",
        counter_step           => "100",
        counter_direction      => "decrement",
        nest_step              => "1,0",
        nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
        nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_7_handle = $HashRef->{'multivalue_handle'};
    
my $multivalue_8_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "1048575",
        counter_step           => "10",
        counter_direction      => "decrement",
        nest_step              => "1,1",
        nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
        nest_enabled           => "0,0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_8_handle = $HashRef->{'multivalue_handle'};
    
my $multivalue_9_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "0",
        counter_step           => "10",
        counter_direction      => "increment",
        nest_step              => "1,1",
        nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
        nest_enabled           => "0,0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_9_handle = $HashRef->{'multivalue_handle'};
    
my $multivalue_10_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "0",
        counter_step           => "1",
        counter_direction      => "decrement",
        nest_step              => "1,1",
        nest_owner             => "$deviceGroup_1_handle,$topology_1_handle",
        nest_enabled           => "0,0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_10_handle = $HashRef->{'multivalue_handle'};

print "Creating multivalue pattern for BGP network group on Port 2\n";
my $multivalue_11_status = ixiangpf::multivalue_config ({
        pattern                => "counter",
        counter_start          => "1234",
        counter_step           => "1",
        counter_direction      => "increment",
        nest_step              => "1,0",
        nest_owner             => "$deviceGroup_2_handle,$topology_2_handle",
        nest_enabled           => "0,1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_11_handle = $HashRef->{'multivalue_handle'};
    
# Creating BGP Network Group
print "Creating BGP Network Group on Port 1\n";
my $network_group_2_status = ixiangpf::emulation_bgp_route_config ({
        handle                                   => "$networkGroup_1_handle",
        mode                                     => "create",
        protocol_route_name                      => "{BGP IP Route Range 1}",
        active                                   => "1",
        ipv4_unicast_nlri                        => "1",
        prefix                                   => "205.1.0.1",
        label_step                               => "1",
        override_peer_as_set_mode                => "0",
        label_start                              => "$multivalue_6_handle",
        enable_add_path                          => "1",
        add_path_id                              => "$multivalue_7_handle",
        advertise_as_bgp_3107                    => "1",
        label_end                                => "$multivalue_8_handle",
        enable_aigp                              => "1",
        no_of_tlvs                               => "2",
        aigp_type                                => "aigptlv aigptlv",
        aigp_value                               => "$multivalue_9_handle $multivalue_10_handle",
    });
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_2_handle = $HashRef->{'network_group_handle'};
my $ipv4PrefixPools_3_handle = $HashRef->{'ipv4_prefix_pools_handle'};

print "Creating BGP Network Group on Port 2\n";
my $network_group_4_status = ixiangpf::emulation_bgp_route_config ({
        handle                                   => "$networkGroup_3_handle",
        mode                                     => "create",
        protocol_route_name                      => "{BGP IP Route Range 2}",
        active                                   => "1",
        ipv4_unicast_nlri                        => "1",
        prefix                                   => "206.1.0.1",
        label_step                               => "1",
        label_start                              => "16",
        enable_add_path                          => "1",
        add_path_id                              => "$multivalue_11_handle",
        advertise_as_bgp_3107                    => "1",
        label_end                                => "1048575",
        enable_aigp                              => "0",
        no_of_tlvs                               => "1",
        aigp_type                                => "aigptlv",
        aigp_value                               => "0",
    });
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = $HashRef->{'log'};
    print "Error: $error";
    return "FAILED - $error";
}
my $networkGroup_4_handle = $HashRef->{'network_group_handle'};
my $ipv4PrefixPools_4_handle = $HashRef->{'ipv4_prefix_pools_handle'};

############################################################################
# Start BGP protocol                                                       #
############################################################################
print "Starting BGP on Topology 1 & Topology 2\n";
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
print "Waiting for 45 seconds\n";
sleep(45);

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
print "Fetching BGP aggregated statistics on Port 1\n";
my $protostats = ixiangpf::emulation_bgp_info({
    handle => $bgpIpv4Peer_1_handle, 
    mode   => 'stats'}); 
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

print "Fetching BGP aggregated statistics on Port 2\n";
$protostats = ixiangpf::emulation_bgp_info({
    handle => $bgpIpv4Peer_2_handle,
    mode   => 'stats'});
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

################################################################################
# Enabling the IPv4 Filter for BGP Learned Information                         #
################################################################################
print "Enabling the IPv4 Learned Information for BGP\n";
my $bgp_1_status = ixiangpf::emulation_bgp_config ({
    handle                               => "$bgpIpv4Peer_1_handle",
    mode                                 => 'modify',
    ipv4_filter_unicast_nlri             => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

my $bgp_2_status = ixiangpf::emulation_bgp_config ({
    handle                               => "$bgpIpv4Peer_2_handle",
    mode                                 => 'modify',
    ipv4_filter_unicast_nlri             => "1",
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
# Retrieve Learned Info                                                    #
############################################################################
print "Fetching BGP IPv4 MPLS LearnedInfo on Port 1\n";
my $bgpLearnedInfo = ixiangpf::emulation_bgp_info({
    handle => $bgpIpv4Peer_1_handle,
    mode => 'learned_info'});
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

print "Fetching BGP IPv4 MPLS LearnedInfo on Port 2\n";
$bgpLearnedInfo = ixiangpf::emulation_bgp_info({
    handle => $bgpIpv4Peer_2_handle,
    mode => 'learned_info'});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error\n";
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
# Configure L2-L3 traffic                                                  #
############################################################################
print "Configure L2-L3 traffic\n";
# Configure L2-L3 IPv4 Traffic

$_result_ = ixiangpf::traffic_config ({
    mode                    =>        'create',
    traffic_generator       =>        'ixnetwork_540',
    endpointset_count       =>        '1',
    emulation_src_handle    =>        [[$networkGroup_3_handle]],
    emulation_dst_handle    =>        [[$networkGroup_1_handle]],
    name                    =>        'IPv4-Traffic',
    circuit_endpoint_type   =>        'ipv4',
    rate_pps                =>        '1000',
    track_by                =>        'sourceDestEndpointPair0 trackingenabled0 mplsMplsLabelValue0 mplsFlowDescriptor0 ipv4DestIp0 ipv4SourceIp0',
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
