################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    15/01/2015 - Sumeer Kumar - created sample                                #
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
#    This script intends to demonstrate how to use NGPF IPTVv6 HLP API.        #
#                                                                              #
#    1. It will create one MLD Host topology and one IPv6 topology.            #
#    2. Configure IPTV on MLD host.                                            #
#    3. Start all protocols.                                                   #
#    4. Retrieve protocol statistics.                                          #
#    5. Configure L2-L3 traffic.                                               #
#    6. Start the L2-L3 traffic.                                               #
#    7. Stat IPTV.                                                             #  
#    8. Retrieve L2-L3 traffic stats.                                          #
#    9. Make on the fly changes of IPTV attributes                             #	
#   10. Retrieve protocol statistics.                                          #
#   11. Stop IPTV.                                                             #
#   12. Stop L2-L3 traffic.                                                    #
#   13. Stop all protocols.                                                    #
#                                                                              #
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
    topology_name      => "{MLD Topology 1}",
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
    device_group_name            => "{MLD HOST}",
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
    topology_name      => "{IPv6 Topology 2}",
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

# Creating IPv6 Stack on top of Ethernet Stack for the first Device Group                                 
print "Creating IPv6 Stack on top of Ethernet Stack for the first Device Group\n";     
my $ipv6_1_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv6 1}",
    protocol_handle                   => "$ethernet_1_handle",
    ipv6_multiplier                   => "1",
    ipv6_resolve_gateway              => "1",
    ipv6_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step      => "00.00.00.00.00.00",
    ipv6_gateway                      => "20:0:0:0:0:0:0:1",
    ipv6_gateway_step                 => "::0",
    ipv6_intf_addr                    => "20:0:0:0:0:0:0:2",
    ipv6_intf_addr_step               => "::0",
    ipv6_prefix_length                => "64",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv6_1_handle = $HashRef->{'ipv6_handle'};

# Creating IPv6 Stack on top of Ethernet Stack for the second Device Group 
print "Creating IPv6 2 stack on ethernet 2 stack for the second Device Group\n";
my $ipv6_2_status = ixiangpf::interface_config ({
    protocol_name                     => "{IPv6 2}",
    protocol_handle                   => "$ethernet_2_handle",
    ipv6_multiplier                   => "1",
    ipv6_resolve_gateway              => "1",
    ipv6_manual_gateway_mac           => "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step      => "00.00.00.00.00.00",
    ipv6_gateway                      => "20:0:0:0:0:0:0:2",
    ipv6_gateway_step                 => "::0",
    ipv6_intf_addr                    => "20:0:0:0:0:0:0:1",
    ipv6_intf_addr_step               => "::0",
    ipv6_prefix_length                => "64",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ipv6_2_handle = $HashRef->{'ipv6_handle'};

################################################################################
# Other protocol configurations                                                # 
################################################################################

# This will create MLD v2 Host Stack with IPTV enabled on top of IPv6 stack having zap behavior as zap and view, zapping type as multicast to leave and zap direction as down.
    
print "Creating MLD Host Stack on top of IPv6 1 stack\n";
my $mld_host_1_status = ixiangpf::emulation_mld_config ({
    mode                                 => "create",
    handle                               => "$ipv6_1_handle",
    mld_version                          => "v2",
    name                                 => "{MLD Host 1}",
    enable_iptv                          => "1",
    iptv_name                            => "{IPTV 1}",
    stb_leave_join_delay                 => "3000",
    join_latency_threshold               => "10000",
    leave_latency_threshold              => "10000",
    zap_behavior                         => "zapandview",
    zap_direction                        => "down",
    zap_interval                         => "10000",
    num_channel_changes_before_view      => "1",
    view_duration                        => "10000",
    zap_interval_type                    => "multicasttoleave",
    log_failure_timestamps               => "0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $mldHost_1_handle = $HashRef->{'mld_host_handle'};
my $mld_host_iptv_handle = $HashRef->{'mld_host_iptv_handle'};

# Creating MLD Group Ranges 
print "Creating MLD Group Ranges\n";
my $mld_mcast_i_pv6_group_list_1_status = ixiangpf::emulation_multicast_group_config ({
    mode               => "create",
    ip_addr_start      => "ff0a:0:0:0:0:0:0:1",
    ip_addr_step       => "0:0:0:0:0:0:0:0",
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
my $mldMcastIPv6GroupList_1_handle = $HashRef->{'multicast_group_handle'};

# Creating MLD Source Ranges 
print "Creating MLD Source Ranges\n";
my $mld_ucast_i_pv6_source_list_1_status = ixiangpf::emulation_multicast_source_config ({
    mode               => "create",
    ip_addr_start      => "20:0:0:0:0:0:0:1",
    ip_addr_step       => "0:0:0:0:0:0:0:0",
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
my $mldUcastIPv6SourceList_1_handle = $HashRef->{'multicast_source_handle'};

# Creating MLD Group and Source Ranges in MLD Host stack
print "Creating MLD Group and Source Ranges in MLD Host stack\n";
$mld_host_1_status = ixiangpf::emulation_mld_group_config ({
    mode                    => "create",
    g_filter_mode           => "include",
    group_pool_handle       => "$mldMcastIPv6GroupList_1_handle",
    no_of_grp_ranges        => "1",
    no_of_src_ranges        => "1",
    session_handle          => "$mldHost_1_handle",
    source_pool_handle      => "$mldUcastIPv6SourceList_1_handle",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
    
# Configuring inter stb delay and rate control for MLD Host global settings
print "Configuring inter stb delay and rate control for MLD host\n";
my $mld_host_2_status = ixiangpf::emulation_mld_config ({
    mode                          => "create",
    handle                        => "/globals",
    global_settings_enable        => "1",
    no_of_reports_per_second      => "500",
    interval_in_ms                => "1000",
    inter_stb_start_delay         => "0",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Waiting 5 seconds before starting protocol(s) ...\n";
sleep(5);

############################################################################
# Start MLD protocol                                                       #      
############################################################################
print "Starting MLD on topology1\n";
my $run_status = ixiangpf::emulation_mld_control({
   handle => $mldHost_1_handle,
   mode   => 'start',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}

print "Starting IPv6 on topology2\n";
$run_status = ixiangpf::test_control({
   handle => $ipv6_2_handle,
   action => 'start_protocol',
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
print "Fetching MLD aggregated statistics\n";
my $protostats = ixiangpf::emulation_mld_info({
    handle => $deviceGroup_1_handle,
    type   => 'host',
    mode   => 'aggregate'
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
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv6, Destination->Multicast group                #
# 2. Type      : Multicast IPv6 traffic                                    #
# 3. Flow Group: On IPv6 Destination Address                               #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : IPv6 Destination Address                                  #	
############################################################################
print "Configuring L2-L3 traffic\n";
$_result_ = ixiangpf::traffic_config({
    mode                                        => 'create',
    traffic_generator                           => 'ixnetwork_540',
    endpointset_count                           => 1,
    emulation_src_handle                        => $ipv6_2_handle,
    emulation_dst_handle                        => $mldMcastIPv6GroupList_1_handle,
    emulation_multicast_dst_handle              => 'ff0a:0:0:0:0:0:0:1/0:0:0:0:0:0:0:0/1',
    emulation_multicast_dst_handle_type         => 'none',
    emulation_multicast_rcvr_handle             => $mldMcastIPv6GroupList_1_handle,
    emulation_multicast_rcvr_port_index         => 0,
    emulation_multicast_rcvr_host_index         => 0,
    emulation_multicast_rcvr_mcast_index        => 0,
    name                                        => 'TI0-Traffic_Item_1',
    circuit_endpoint_type                       => 'ipv6',
    transmit_distribution                       => 'ipv6DestIp0',                             
    rate_pps                                    => 1000,                                    
    frame_size                                  => 512,
    track_by                                    => 'trackingenabled0 ipv6DestIp0'
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
$_result_ = ixiangpf::traffic_control({
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
# Starting IPTV                                                            #
############################################################################
print "Starting IPTV...\n";
my $iptvStart = ixiangpf::emulation_mld_control({
    handle => $mld_host_iptv_handle,
    mode   => 'start',
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
sleep(10);

############################################################################
# Retrieve L2-L3 traffic stats                                             #
############################################################################
print "Retrieving L2-L3 traffic stats\n";
$protostats = ixiangpf::traffic_stats({
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
@status_keys = ixiangpf::status_item_keys();
 foreach (@status_keys) {
    my $my_key = $_;
    my $allStats = ixiangpf::status_item($my_key);
    print "==================================================================\n";
    print "\n$my_key: $allStats\n\n";
    print "==================================================================\n";
 }
    
############################################################################
# Making on the fly changes for zapDirection, zapIntervalType, zapInterval,#
# numChannelChangesBeforeView and viewDuration in IPTV tab of MLD host     # 
############################################################################
print "Making on the fly chnages for zapDirection, zapIntervalType, zapInterval,
numChannelChangesBeforeView and viewDuration\n";
$mld_host_1_status = ixiangpf::emulation_mld_config ({
    handle                               => $mldHost_1_handle,
    mode                                 => "modify",
    zap_direction                        => "up",
    zap_interval_type                    => "leavetoleave",
    zap_interval                         => "30000",
    num_channel_changes_before_view      => "4",
    view_duration                        => "40000",
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
   handle => $ipv6_1_handle,
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
# Retrieve protocol statistics after doing on the fly changes              #
############################################################################
print "Fetching MLD aggregated statistics\n";
$protostats = ixiangpf::emulation_mld_info({
    handle => $deviceGroup_1_handle,
    type   => 'host',
    mode   => 'aggregate'
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
# Stopping IPTV                                                            #
############################################################################
print "Stopping IPTV\n";
my $iptvStop = ixiangpf::emulation_mld_control({
    handle => $mld_host_iptv_handle,
    mode   => 'stop',
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
