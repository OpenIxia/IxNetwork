################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    01/19/2015 - Sumeer Kumar - created sample                                #
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
#    This script intends to demonstrate how to use NGPF IGMP HLP API.          #
#                                                                              #
#    1. It will create two topologies, one having two IGMP Hosts and other     #
#       having one IGMP Querier.                                               #
#    2. Start IGMP protocol.                                                   #
#    3. Retreive protocol statistics.                                          #
#    4. Retrieve learned info.                                                 #
#    5. Configure L2-L3 traffic.                                               #
#    6. Start L2/L3 protocol.                                                  #
#    7. Retreive  L2/L3 protocol statistics.                                   #
#    8. Make Making on the fly changes for IGMP Group and Source Ranges        #
#    9. Make Making on the fly changes for IGMP Querier                        #
#   10. Retreive protocol statistics.                                          #
#   11. Stop protocol and L2/L3 traffic.                                       #
#   12. Stop all protocols.                                                    #
#                                                                              #
#Ixia Software:                                                                #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
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
my @chassis             = ('10.205.28.170');
my $tcl_server          = '10.205.28.170';
my @port_list           = ([ '1/7', '1/8' ]);
my $ixNetwork_client    = '10.205.28.41:8981';

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
    topology_name      => "{IGMP Host Topology}",
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
    device_group_name            => "{IGMP Host Device Group}",
    device_group_multiplier      => "2",
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
    topology_name      => "{IGMP Querier Topology}",
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
    device_group_name            => "{IGMP Querier Device Group}",
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

# Creating multivalue for ethernet
print "Creating multivalue pattern for ethernet\n";
my $multivalue_1_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "18.03.73.c7.6c.b1",
    counter_step           => "00.00.00.00.00.01",
    counter_direction      => "increment",
    nest_step              => "00.00.01.00.00.00",
    nest_owner             => "$topology_1_handle",
    nest_enabled           => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_1_handle = $HashRef->{'multivalue_handle'};

# Creating ethernet stack for the first Device Group 
print "Creating ethernet stack for the first Device Group\n";
my $ethernet_1_status = ixiangpf::interface_config ({
    protocol_name                => "{Ethernet 1}",
    protocol_handle              => "$deviceGroup_1_handle",
    mtu                          => "1500",
    src_mac_addr                 => "$multivalue_1_handle",
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

# Creating multivalue for IPv4                                 
print "Creating multivalue pattern for IPv4\n";
my $multivalue_2_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "20.20.20.2",
    counter_step           => "0.0.0.1",
    counter_direction      => "increment",
    nest_step              => "0.1.0.0",
    nest_owner             => "$topology_1_handle",
    nest_enabled           => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_2_handle = $HashRef->{'multivalue_handle'};

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
    intf_ip_addr                      => "$multivalue_2_handle",
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

# This will create IGMP v3 Host Stack with IPTV disabled on top of IPv4 stack

# Creating IGMP Host Stack on top of IPv4 stack
print "Creating IGMP Host Stack on top of IPv4 stack in first topology\n";    
my $igmp_host_1_status = ixiangpf::emulation_igmp_config ({
    handle                               => "$ipv4_1_handle",
    protocol_name                        => "{IGMP Host}",
    mode                                 => "create",
    filter_mode                          => "include",
    igmp_version                         => "v3",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $igmpHost_1_handle = $HashRef->{'igmp_host_handle'};

# Creating multivalue for group address
print "Creating multivalue pattern for IGMP Host group address\n";
my $multivalue_4_status = ixiangpf::multivalue_config ({
    pattern                => "counter",
    counter_start          => "226.0.0.1",
    counter_step           => "1.0.0.0",
    counter_direction      => "increment",
    nest_step              => "0.1.0.0",
    nest_owner             => "$topology_1_handle",
    nest_enabled           => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $multivalue_3_handle = $HashRef->{'multivalue_handle'};

# Creating IGMP Group Ranges 
print "Creating IGMP Group Ranges\n"; 
my $igmp_mcast_i_pv4_group_list_1_status = ixiangpf::emulation_multicast_group_config ({
    mode               => "create",
    ip_addr_start      => "$multivalue_3_handle",
    ip_addr_step       => "0.0.0.1",
    num_groups         => "1",
    active             => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $igmpMcastIPv4GroupList_1_handle = $HashRef->{'multicast_group_handle'};

# Creating IGMP Source Ranges
print "Creating IGMP Source Ranges\n";      
my $igmp_ucast_i_pv4_source_list_1_status = ixiangpf::emulation_multicast_source_config ({
    mode               => "create",
    ip_addr_start      => "20.20.20.1",
    ip_addr_step       => "0.0.0.1",
    num_sources        => "1",
    active             => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $igmpUcastIPv4SourceList_1_handle = $HashRef->{'multicast_source_handle'};
 
# Creating IGMP Group and Source Ranges in IGMP Host stack
print "Creating IGMP Group and Source Ranges in IGMP Host stack\n";   
$igmp_host_1_status = ixiangpf::emulation_igmp_group_config ({
    mode                    => "create",
    g_filter_mode           => "include",
    group_pool_handle       => "$igmpMcastIPv4GroupList_1_handle",
    no_of_grp_ranges        => "1",
    no_of_src_ranges        => "1",
    session_handle          => "$igmpHost_1_handle",
    source_pool_handle      => "$igmpUcastIPv4SourceList_1_handle",
});
    
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $igmpGroup_1_handle = $HashRef->{'igmp_group_handle'};

# This will create IGMP v3 Querier Stack on top of IPv6 stack

# Creating IGMP Querier Stack on top of IPv4 stack
print "Creating IGMP Querier Stack on top of IPv4 stack in second topology\n";    
my $igmp_querier_1_status = ixiangpf::emulation_igmp_querier_config ({
    mode                                   => "create",
    discard_learned_info                   => "0",
    active                                 => "1",
    general_query_response_interval        => "11000",
    handle                                 => "$ipv4_2_handle",
    igmp_version                           => "v3",
    query_interval                         => "140",
    name                                   => "{IGMP Querier}",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $igmpQuerier_1_handle = $HashRef->{'igmp_querier_handle'};

print "Waiting 05 seconds before starting protocol(s) ...\n";
sleep(5);
    
############################################################################
# Start IGMP protocol                                                      #
############################################################################
print "Starting IGMP Host on topology1\n";
my $run_status = ixiangpf::emulation_igmp_control({
    handle => $igmpHost_1_handle,
    mode   => 'start',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Starting IGMP Querier on topology2\n"; 
$run_status = ixiangpf::emulation_igmp_control({
   handle => $igmpQuerier_1_handle,
   mode   => 'start',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
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
print "Fetching IGMP aggregated statistics\n";
my $protostats = ixiangpf::emulation_igmp_info({
    handle => $deviceGroup_1_handle,
    type   => 'host',
    mode   => 'aggregate',
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

print "Fetching IGMP Querier aggregated statistics\n";
$protostats = ixiangpf::emulation_igmp_info({
    handle => $deviceGroup_2_handle,
    type   => 'querier',
    mode   => 'aggregate',
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
print "Fetching IGMP Querier LearnedInfo\n";
my $igmpLearnedInfo = ixiangpf::emulation_igmp_info({
    handle => $igmpQuerier_1_handle,
    type => 'querier',
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

############################################################################ 
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv4, Destination->Multicast group                #
# 2. Type      : Multicast IPv4 traffic                                    #
# 3. Flow Group: Source Destination Endpoint Pair                          #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : Source Destination Endpoint Pair                          #	
############################################################################
print "Configuring L2-L3 traffic\n";
$_result_ = ixiangpf::traffic_config({
    mode                                => 'create',
    traffic_generator                   => 'ixnetwork_540',
    endpointset_count                   => 1,
    emulation_src_handle                => $topology_2_handle,
    emulation_dst_handle                => '',
    emulation_multicast_dst_handle      => ['226.0.0.1/0.0.0.0/1', '227.0.0.1/0.0.0.0/1'],
    emulation_multicast_dst_handle_type => ['none', 'none'],
    emulation_multicast_rcvr_handle     => [$igmpMcastIPv4GroupList_1_handle, $igmpMcastIPv4GroupList_1_handle],
    emulation_multicast_rcvr_port_index => [0, 0],
    emulation_multicast_rcvr_host_index => [0, 1],
    emulation_multicast_rcvr_mcast_index=> [0, 0],
    name                                => 'TI0-Traffic_Item_1',
    circuit_endpoint_type               => 'ipv4',
    transmit_distribution               => 'srcDestEndpointPair0',                             
    rate_pps                            => 1000,                                    
    frame_size                          => 512,
    track_by                            => 'trackingenabled0 sourceDestEndpointPair0'
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
print "Running Traffic...\n";
$_result_ = ixiangpf::traffic_control({
    action            => 'run',
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
print "Let the traffic run for 20 seconds ...\n";
sleep(20);
    
############################################################################
# Retrieve L2-L3 traffic stats                                             #
############################################################################
print "Retrieving L2-L3 traffic stats\n";
$protostats = ixiangpf::traffic_stats({
    mode              => 'all',
    traffic_generator => 'ixnetwork_540',
    measure_mode      => 'mixed'});
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
# Sending leave using IGMP host group handle                               #
############################################################################
print "Sending leave using IGMP host group handle\n";
my $sendLeaveGlobally = ixiangpf::emulation_igmp_control({
    mode                => 'leave',
    group_member_handle => $igmpGroup_1_handle});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(2);

############################################################################
# Sending join using IGMP host group handle                                #
############################################################################
print "Sending join using IGMP host group handle\n";
my $sendJoinGlobally = ixiangpf::emulation_igmp_control({
    mode                => 'join',
    group_member_handle => $igmpGroup_1_handle});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(2);

################################################################################
# Making on the fly changes for IGMP Group and Source Ranges                   #
################################################################################
print "Making on the fly changes for IGMP Group Ranges\n";
$igmp_host_1_status = ixiangpf::emulation_multicast_group_config ({
    handle        => $igmpMcastIPv4GroupList_1_handle,
    mode          => 'modify',
    ip_addr_start => '230.1.1.1',
    ip_addr_step  => '0.0.0.2',
    num_groups    => '2',
    active        => '1',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Making on the fly changes for IGMP Source Ranges\n";
$igmp_host_1_status = ixiangpf::emulation_multicast_source_config ({
    handle            => $igmpUcastIPv4SourceList_1_handle,
    mode              => 'modify',
    ip_addr_start     => '30.30.30.1',
    ip_addr_step      => '0.0.0.1',
    num_sources       => '5',
    active            => '1',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Making on the fly chnages for IGMP Group and Source Ranges in IGMP Host stack\n";
$igmp_host_1_status = ixiangpf::emulation_igmp_group_config ({
    mode              => 'modify',
    handle            => "$igmpHost_1_handle",
    g_filter_mode     => 'exclude',
    group_pool_handle => "$igmpMcastIPv4GroupList_1_handle",
    no_of_grp_ranges  => '1',
    no_of_src_ranges  => '1',
    session_handle    => "$igmpHost_1_handle",
    source_pool_handle=> "$igmpUcastIPv4SourceList_1_handle",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(5);
 
################################################################################
# Making on the fly changes for IGMP Querier                                   #
################################################################################
print "Making on the fly changes for IGMP Querier\n";
$igmp_querier_1_status = ixiangpf::emulation_igmp_querier_config ({
    mode                            => 'modify',
    handle                  	    => "$igmpQuerier_1_handle",
    general_query_response_interval => '240',
    ip_router_alert                 => '0',
    robustness_variable             => '5',
    startup_query_count             => '5',
    query_interval                  => '180',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(2);

############################################################################
# Applying changes one the fly                                             #
############################################################################
print "Applying changes on the fly\n";    
my $applyChanges = ixiangpf::test_control({
   handle => "$ipv4_1_handle",
   action => 'apply_on_the_fly_changes',});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(5);

############################################################################
# Retrieve protocol statistics after making On The Fly changes             #
############################################################################
print "Fetching IGMP aggregated statistics\n";
$protostats = ixiangpf::emulation_igmp_info({
    handle => $deviceGroup_1_handle,
    type   => 'host',
    mode   => 'aggregate',
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

print "Fetching IGMP Querier aggregated statistics\n";
$protostats = ixiangpf::emulation_igmp_info({
    handle => $deviceGroup_2_handle,
    type   => 'querier',
    mode   => 'aggregate',
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
