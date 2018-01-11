
################################################################################
# Version 1.0    $Revision: #1 $
# $Author: cm $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-17-2013 LBose - Initial Version
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
#    This sample configures two ports in IxNetwork, configures a traffic item  #
#    and modify the traffic item for repeatable and non-repeatable random macs.#
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
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
my $test_name              = "NextGenTraffic_random_mac";
my $chassis_ip             = "10.206.27.55";
my $tcl_server             = "10.206.27.55";
my @port_list              = ("10/1", "10/2");
my $ixnetwork_tcl_server   = "10.206.26.196";

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
my @status_keys            = ();
my %status_keys            = ();
my @portHandleList         = ();
my @ethStackList           = ();
my $eth_stack              = '';
# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
$_result_ = ixiahlt::connect ( {
    reset                  => 1,
    device                 => $chassis_ip,
    port_list              => \@port_list,
    ixnetwork_tcl_server   => $ixnetwork_tcl_server,
    tcl_server             => $tcl_server,
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

my $port_src_handle = $portHandleList[0];
my $port_dst_handle = $portHandleList[1];

print ("Ixia port handles are $port_handle ...\n");
print ("End connecting to chassis ...\n");
print ("Configure interfaces ...\n");

################################################################################
# Configure Protocol Interfaces on both ports                                  #
################################################################################
$_result_ = ixiahlt::interface_config  ( {
    mode                   => 'config',    
    port_handle            => $port_src_handle,    
    tx_gap_control_mode    => 'average',    
    transmit_mode          => 'advanced',    
    port_rx_mode           => 'packet_group',    
    data_integrity         => 1,    
    intf_mode              => 'ethernet',    
    speed                  => 'ether1000',    
    duplex                 => 'full',    
    autonegotiation        => 1,    
    phy_mode               => 'copper',    
});
&catch_error();



$_result_ = ixiahlt::interface_config  ( {
    mode                   => 'config',    
    port_handle            => $port_dst_handle,    
    tx_gap_control_mode    => 'average',    
    transmit_mode          => 'advanced',    
    port_rx_mode           => 'packet_group',
    data_integrity         => 1,    
    intf_mode              => 'ethernet',
    speed                  => 'ether1000',    
    duplex                 => 'full',    
    autonegotiation        => 1,    
    phy_mode               => 'copper',    
});
&catch_error();


################################################################################
# Configure Traffic on ports                                                   #
################################################################################

print ("Reset traffic ...\n");
$_result_ = ixiahlt::traffic_control  ( {
    action                      => 'reset',    
    traffic_generator           => 'ixnetwork_540',    
    latency_bins                => 'enabled',    
    latency_control             => 'store_and_forward',    
});
&catch_error();

print ("Configure traffic ...\n");
$_result_ = ixiahlt::traffic_config  ( {
    mode                                        => 'create',
    traffic_generator                           => 'ixnetwork_540',
    endpointset_count                           => 1,
    emulation_src_handle                        => $port_src_handle,
    emulation_dst_handle                        => $port_dst_handle,
    global_dest_mac_retry_count                 => 1,
    global_dest_mac_retry_delay                 => 5,
    enable_data_integrity                       => 1,
    global_enable_dest_mac_retry                => 1,
    global_enable_min_frame_size                => 0,
    global_enable_staggered_transmit            => 0,
    global_enable_stream_ordering               => 0,
    global_stream_control                       => 'continuous',
    global_stream_control_iterations            => 1,
    global_large_error_threshhold               => 2,
    global_enable_mac_change_on_fly             => 0,
    global_max_traffic_generation_queries       => 500,
    global_mpls_label_learning_timeout          => 30,
    global_refresh_learned_info_before_apply    => 0,
    global_use_tx_rx_sync                       => 1,
    global_wait_time                            => 1,
    global_display_mpls_current_label_value     => 0,
    frame_sequencing                            => 'disable',
    frame_sequencing_mode                       => 'rx_threshold',
    src_dest_mesh                               => 'one_to_one',
    route_mesh                                  => 'one_to_one',
    bidirectional                               => 0,
    allow_self_destined                         => 0,
    enable_dynamic_mpls_labels                  => 0,
    hosts_per_net                               => 1,
    name                                        => 'Traffic_Item_1',
    source_filter                               => 'all',
    destination_filter                          => 'all',
    merge_destinations                          => 0,
    circuit_type                                => 'raw',
    pending_operations_timeout                  => 30,
});
&catch_error();


my $current_config_element  = ixiahlt::status_item("traffic_item");
@ethStackList = ixiahlt::status_item("$current_config_element.headers");
$eth_stack = $ethStackList[0];

$_result_ = ixiahlt::traffic_config  ( {
    mode                            => 'modify',
    traffic_generator               => 'ixnetwork_540',
    stream_id                       => $current_config_element,
    preamble_size_mode              => 'auto',
    preamble_custom_size            => 8,
    data_pattern                    => '',
    data_pattern_mode               => 'incr_byte',
    enforce_min_gap                 => 0,
    rate_percent                    => 10,
    frame_rate_distribution_port    => 'apply_to_all',
    frame_rate_distribution_stream  => 'split_evenly',
    frame_size                      => 64,
    length_mode                     => 'fixed',
    tx_mode                         => 'advanced',
    transmit_mode                   => 'continuous',
    pkts_per_burst                  => 1,
    tx_delay                        => 0,
    tx_delay_unit                   => 'bytes',
    number_of_packets_per_stream    => 1,
    loop_count                      => 1,
    min_gap_bytes                   => 12,
});
&catch_error();

my $dst_seed_hlt  =  7;
my $dst_bits_hlt  =  '00:00:00:00:00:40';
my $dst_mask_hlt  =  'ff:ff:ff:ff:ff:35';
my $dst_count_hlt =  8;
my $src_seed_hlt  =  5;
my $src_bits_hlt  =  '00:00:00:00:00:10';
my $src_mask_hlt  =  'ff:ff:ff:ff:ff:25';
my $src_count_hlt =  6;

print ("Set repeatable random mac ...\n");
################################################################################
# Configure Traffic Item with repeatbale random mac                            #
################################################################################
$_result_ = ixiahlt::traffic_config  ( {
    mode               => 'modify',
    traffic_generator  => 'ixnetwork_540',
    stream_id          => $eth_stack,
    l2_encap           => 'ethernet_ii',
    mac_dst_mode       => 'repeatable_random',
    mac_dst            => $dst_bits_hlt,
    mac_dst_count      => $dst_count_hlt,
    mac_dst_seed       => $dst_seed_hlt,
    mac_dst_mask       => $dst_mask_hlt,
    mac_dst_tracking   => 0,
    mac_src_mode       => 'repeatable_random',
    mac_src            => $src_bits_hlt,
    mac_src_count      => $src_count_hlt,
    mac_src_seed       => $src_seed_hlt,
    mac_src_mask       => $src_mask_hlt,
    mac_src_tracking   => 0,
    track_by           => 'none',
    egress_tracking    => 'none',
});
&catch_error();

print  ("Set non repeatable random mac ...\n");
################################################################################
# Configure Traffic Item with non-repeatbale random mac                        #
################################################################################
$_result_ = ixiahlt::traffic_config  ( {
    mode               => 'modify',    
    traffic_generator  => 'ixnetwork_540',    
    stream_id          => $eth_stack,    
    l2_encap           => 'ethernet_ii',    
    mac_dst_mode       => 'random',    
    mac_src_mode       => 'random',    
});
&catch_error();

print ("\n\n$test_name : TEST COMPLETED SUCCESSFULLY!\n");