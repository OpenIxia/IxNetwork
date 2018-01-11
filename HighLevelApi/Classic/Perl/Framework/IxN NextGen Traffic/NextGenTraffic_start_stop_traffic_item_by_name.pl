################################################################################
# Version 1.0    $Revision: #1 $
# $Author: cm $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#
# Description:
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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample configures two ports in IxNetwork, configures a traffic item  #
#    and performs a packet_stats procedure call in order to get the first data #
#    frame.                                                                    #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10/100/1000 STX4-256MB module.                 #
#                                                                              #
################################################################################

# Source all libraries in the beginning
use warnings;
use strict;
use bignum;
use Carp;

# use lib where the HLPAPI files are located
# It is typically: "C:/Program Files/Ixia/hltapi/<version_number>/TclScripts/lib/hltapi/library/common/ixia_hl_lib-<version>"
# For Ex:
# use lib "C:/Program Files/Ixia/hltapi/4.70.0.213/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.10";
use lib "C:/Program Files/Ixia/hltapi/4.70.0.213/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.10";

use ixiahlt;
use ixiaixn;

# Declare the Chassis IP address and the Ports that will be used
my $test_name              = "NextGenTraffic_start_stop_traffic_item_by_name";
my $chassisIP              = "10.206.27.55";
my $tcl_server             = "10.206.27.55";
my $ixnetwork_tcl_server   = "10.206.26.196";
my @port_list              = ("10/1", "10/2");

################################################################################
# Function to catch the errors and print it on the screen             .        #
################################################################################
sub catch_error {
    if (ixiahlt::status_item('status') != 1) {
        print ("n#################################################### n");
        print ("ERROR: n$test_name : ". ixiahlt::status_item('status'));
        print ("n#################################################### n");
        die ("ERROR: n$test_name : Please check values and the port handles!!!");
    }
}

# Initialize values for HLPAPI scripts
my $_result_               = '';
my $status                 = '';
my $port_handle            = '';
my @portHandleList         = ();
my @trafficItemList        = ();
my @status_keys            = ();
my %status_keys            = ();

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
$_result_ = ixiahlt::connect( {
    reset                => 1,
    device               => $chassisIP,
    port_list            => \@port_list,
    ixnetwork_tcl_server => $ixnetwork_tcl_server ,
    tcl_server           => $tcl_server ,
});
&catch_error();

@status_keys = ixiahlt::status_item_keys();
$port_handle = ixiahlt::status_item('port_handle');
$status = ixiahlt::status_item('status');

# Assign portHandleList with port handles values
foreach my $port (@port_list) {
    $port_handle = ixiahlt::status_item("port_handle.$chassisIP.$port");
    push(@portHandleList, $port_handle);
}

my $port_src_handle = $portHandleList[0];
my $port_dst_handle = $portHandleList[1];

print ("Ixia port handles are $port_handle ...\n");

################################################################################
# Configure Protocol Interfaces on both ports                                  #
################################################################################
$_result_ = ixiahlt::interface_config ( {
    mode                   => 'config',    
    port_handle            => $port_src_handle,    
    transmit_clock_source  => 'external',    
    internal_ppm_adjust    => 0,    
    data_integrity         => 1,    
    intf_mode              => 'ethernet',    
    speed                  => 'ether100',    
    duplex                 => 'full',    
    autonegotiation        => 1,    
    phy_mode               => 'copper',    
    transmit_mode          => 'advanced',    
    port_rx_mode           => 'capture_and_measure',    
    tx_gap_control_mode    => 'fixed',    
});
&catch_error();

$_result_ = ixiahlt::interface_config ( {
    mode                   => 'config',    
    port_handle            => $port_dst_handle,    
    transmit_clock_source  => 'external',    
    internal_ppm_adjust    => 0,    
    data_integrity         => 1,    
    intf_mode              => 'ethernet',    
    speed                  => 'ether100',    
    duplex                 => 'full',    
    autonegotiation        => 1,    
    phy_mode               => 'copper',    
    transmit_mode          => 'advanced',    
    port_rx_mode           => 'capture_and_measure',    
    tx_gap_control_mode    => 'fixed',    
});
&catch_error();

$_result_ = ixiahlt::interface_config ( {
    mode                       => 'modify',    
    port_handle                => $port_src_handle,    
    vlan                       => 0,    
    l23_config_type            => 'protocol_interface',    
    mtu                        => 1500,    
    gateway                    => '20.0.0.1',    
    intf_ip_addr               => '20.0.0.2',    
    netmask                    => '255.255.255.0',    
    check_opposite_ip_version  => 0,    
    src_mac_addr               => '0000.0107.4232',    
    arp_on_linkup              => 0,    
    ns_on_linkup               => 0,    
    single_arp_per_gateway     => 1,    
    single_ns_per_gateway      => 1,    
});
&catch_error();

$_result_ = ixiahlt::interface_config ( {
    mode                       => 'modify',    
    port_handle                => $port_dst_handle,    
    vlan                       => 0,    
    l23_config_type            => 'protocol_interface',    
    mtu                        => 1500,    
    gateway                    => '20.0.0.2',    
    intf_ip_addr               => '20.0.0.1',    
    netmask                    => '255.255.255.0',    
    check_opposite_ip_version  => 0,    
    src_mac_addr               => '0000.0107.4233',    
    arp_on_linkup              => 0,    
    ns_on_linkup               => 0,    
    single_arp_per_gateway     => 1,    
    single_ns_per_gateway      => 1,    
});
&catch_error();

################################################################################
# Configure Traffic on ports                                                   #
################################################################################
print ("Configure Traffic...\n");

$_result_ = ixiahlt::traffic_control ( {
    action                          => 'reset',
    traffic_generator               => 'ixnetwork_540',
    cpdp_convergence_enable         => 0,
    delay_variation_enable          => 0,
    packet_loss_duration_enable     => 0,
    latency_bins                    => 3,
    latency_values                  => '1.5 3 6.8',
    latency_control                 => 'store_and_forward',
});
&catch_error();

my $ti_src = '::ixNet::OBJ-/vport:1/protocols';
my $ti_dst = '::ixNet::OBJ-/vport:2/protocols';

$_result_ = ixiahlt::traffic_config ( {
    mode                                       => 'create',
    traffic_generator                          => 'ixnetwork_540',
    endpointset_count                          => 1,
    emulation_src_handle                       => $ti_src,
    emulation_dst_handle                       => $ti_dst,
    global_dest_mac_retry_count                => 1,
    global_dest_mac_retry_delay                => 5,
    enable_data_integrity                      => 1,
    global_enable_dest_mac_retry               => 1,
    global_enable_min_frame_size               => 0,
    global_enable_staggered_transmit           => 0,
    global_enable_stream_ordering              => 0,
    global_stream_control                      => 'continuous',
    global_stream_control_iterations           => 1,
    global_large_error_threshhold              => 2,
    global_enable_mac_change_on_fly            => 0,
    global_max_traffic_generation_queries      => 500,
    global_mpls_label_learning_timeout         => 30,
    global_refresh_learned_info_before_apply   => 0,
    global_use_tx_rx_sync                      => 1,
    global_wait_time                           => 1,
    global_display_mpls_current_label_value    => 0,
    frame_sequencing                           => 'disable',
    frame_sequencing_mode                      => 'rx_threshold',
    src_dest_mesh                              => 'one_to_one',
    route_mesh                                 => 'one_to_one',
    bidirectional                              => 0,
    allow_self_destined                        => 0,
    enable_dynamic_mpls_labels                 => 0,
    hosts_per_net                              => 1,
    name                                       => 'Traffic_Item_1',
    source_filter                              => 'all',
    destination_filter                         => 'all',
    merge_destinations                         => 1,
    circuit_endpoint_type                      => 'ipv4',
    egress_tracking                            => 'none',
});
&catch_error();

my $traffic_item = ixiahlt::status_item('stream_id');
push(@trafficItemList, $traffic_item);

$_result_ = ixiahlt::traffic_config ( {
    mode                                       => 'create',
    traffic_generator                          => 'ixnetwork_540',
    endpointset_count                          => 1,
    emulation_src_handle                       => $ti_src,
    emulation_dst_handle                       => $ti_dst,
    global_dest_mac_retry_count                => 1,
    global_dest_mac_retry_delay                => 5,
    enable_data_integrity                      => 1,
    global_enable_dest_mac_retry               => 1,
    global_enable_min_frame_size               => 0,
    global_enable_staggered_transmit           => 0,
    global_enable_stream_ordering              => 0,
    global_stream_control                      => 'continuous',
    global_stream_control_iterations           => 1,
    global_large_error_threshhold              => 2,
    global_enable_mac_change_on_fly            => 0,
    global_max_traffic_generation_queries      => 500,
    global_mpls_label_learning_timeout         => 30,
    global_refresh_learned_info_before_apply   => 0,
    global_use_tx_rx_sync                      => 1,
    global_wait_time                           => 1,
    global_display_mpls_current_label_value    => 0,
    frame_sequencing                           => 'disable',
    frame_sequencing_mode                      => 'rx_threshold',
    src_dest_mesh                              => 'one_to_one',
    route_mesh                                 => 'one_to_one',
    bidirectional                              => 0,
    allow_self_destined                        => 0,
    enable_dynamic_mpls_labels                 => 0,
    hosts_per_net                              => 1,
    name                                       => 'Traffic_Item_2',
    source_filter                              => 'all',
    destination_filter                         => 'all',
    merge_destinations                         => 1,
    circuit_endpoint_type                      => 'ipv4',
    egress_tracking                            => 'none',
});
&catch_error();

my $traffic_item2 = ixiahlt::status_item('stream_id');
push(@trafficItemList, $traffic_item2);

################################################################################
# Start Traffic Item -1 & 2 using the  stream names                            #
################################################################################
$_result_ = ixiahlt::traffic_control ( {
    action  => 'run',    
    handle  => \@trafficItemList,    
});
&catch_error();

sleep (5);

################################################################################
# Stop Traffic Item -1  using the  stream names                                #
################################################################################
$_result_ = ixiahlt::traffic_control ( {
    action  => 'stop',    
    handle  => $traffic_item,    
});
&catch_error();

print ("\n\n$test_name : TEST COMPLETED SUCCESSFULLY!\n");
