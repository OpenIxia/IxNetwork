################################################################################
# $Revision: 0.1															   #
# $Author:   Vijay Anantha Murthy											   #
#																			   #
#    Copyright © by IXIA													   #
#    1997 - 2012                                                               #
#    All Rights Reserved.													   #
#																			   #
#    Revision Log: 															   #
#    10-06-2012		Initial version		 0.1                                   #
#    																		   #
#																			   #
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
#    This sample creates BGP peers and routes, and sends traffic over it       #
#    using ixnetwork traffic_generator.                                        #
#                                                                              #
#    It uses two Ixia ports. BGP peers and routes are configured on both       #
#    ports.  Streams are generated using ixnetwork traffic_generator           #
#    Traffic statistics are collected for each flow.                           #
#                                                                              #
################################################################################
# Source all libraries in the beginning
use warnings;
use strict;
use bignum;
use Carp;

# use lib where the HLPAPI files are located
# This can be moved to .pl files in the JT framework
# It is typically: 
# "/volume/labtools/ixia/<version_number>/lib/library/common/ixia_hl_lib-<version>"
# For Ex:
# use lib "/volume/labtools/ixia/6.30.850.7/lib";
# use lib "/volume/labtools/ixia/6.30.850.7/lib/library/common/ixia_hl_lib-6.30";
use lib "/home/vmurthy/hlpapi/ixos/ixos6.30.850.7/lib";
use lib "/home/vmurthy/hlpapi/ixos/ixos6.30.850.7/lib/library/common/ixia_hl_lib-6.30";
use ixiahlt;
use ixiaixn;

# Declare the Chassis IP address and the Ports that will be used
my $test_name      = "IxNetwork_BGP4_neighbors_b2b_traffic";
my $chassisIP      = "10.64.99.12";
my @port_list      = ("1/9", "1/10");
my $ixNetTclServer = "10.64.99.7";
my $user           = "ixiaHlpapiUser";

# Declare BGP related config options
my $num_of_bgp_neighbors = 10;
my $num_of_prefix        = 1;
my $prefix_ce1           = "55.0.0.1";
my $prefix_ce2           = "70.0.0.1";

# Initialize values for HLPAPI scripts
my $_result_               = '';
my @status_keys            = ();
my %status_keys            = ();
my $port_handle            = '';
my $vport_list             = '';
my $vport_protocols_handle = '';
my $status                 = '';
my @_handles_              = ();
my @return_interfaces      = ();
my @return_router          = ();
my @portHandleList         = ();
my $key                    = '';
my $value                  = '';

# Subroutine to add ip addresses. Can be used for increment
# args Ip_Address, Increment_Step
# returns sum of Ip_Address and Increment_Step
# No Error handling yet
# 
# Handles only IPv4 address format
#
# Ex: Ip_Address     = "10.10.10.1"
#     Increment_Step = "1.0.0.0"
#     Summation      = "11.10.10.1"  
sub ip_addr_incr {
    my ($set_addr, $add_addr) = @_;
    my @set_array = ();
    my @add_array = ();
    my @new_addr  = ();

    @add_array = split /[.]+/, $add_addr;
    @set_array = split /[.]+/, $set_addr;

    for (my $i = 0 ; $i <= @set_array - 1; $i++) {
        $new_addr[$i] = $set_array[$i] + $add_array[$i];
        $set_addr = join ".", @new_addr;
    }
    return $set_addr;
}

# Subroutine to print all key value pairs of Traffic Stats
sub display_all_values {
    my @status_keys = @_;
    foreach my $key (@status_keys) {
        print ("\nINFO: Key value is $key\n\n");
        foreach my $i (ixiahlt::status_item($key)) {
            print ("\nINFO : iValue is $i\n\n");
}}}

sub catch_error {
    if (ixiahlt::status_item('status') != 1) {
        print ("\n#################################################### \n");
        print ("ERROR: \n$test_name : ". ixiahlt::status_item('status'));
        print ("\n#################################################### \n");
        die ("ERROR: \n$test_name : Please check values and the port handles!!!");
}}

#######################################################################
# Connects to the IxNetwork Tcl Server, Tcl Server, and the chassis.  #
# Takes ownership of the ports.                                       #
# Notes: 														      #
# IxNetwork Tcl Server must be running on a client PC; 				  #
# Tcl Server must be running on a client PC;                          #
#######################################################################
$_result_ = ixiahlt::connect({
    reset                => 1,
    device               => $chassisIP ,
    port_list            => \@port_list,
    ixnetwork_tcl_server => $ixNetTclServer ,
    tcl_server           => $chassisIP ,
    break_locks          => 1,
    username             => $user,
    guard_rail           => "statistics",
});
&catch_error();
    
@status_keys = ixiahlt::status_item_keys();
$port_handle = ixiahlt::status_item('port_handle');
$vport_list = ixiahlt::status_item('vport_list');
$vport_protocols_handle = ixiahlt::status_item('vport_protocols_handle');
$status = ixiahlt::status_item('status');

# Assign portHandleList with port handles values
foreach my $port (@port_list) {
    $port_handle = ixiahlt::status_item("port_handle.$chassisIP.$port");
    push(@portHandleList, $port_handle);
}
print ("INFO: Port Handle List ".@portHandleList."\n");

#################################################
# Configure layer 1 port settings (speed)       #
#################################################
my $speed           = "auto";		# CHOICES ether10 ether100 ether1000 auto DEFAULT ether100 (for 10/100/1000 Ethernet cards)
my $autonegotiation = 1;		# CHOICES 0 1 DEFAULT 1
my $duplex          = "auto";		# CHOICES half full auto DEFAULT full
my $phy_mode        = "copper";		# CHOICES copper fiber DEFAULT copper

$_result_ = ixiahlt::interface_config({
    mode        => 'config',
    port_handle => \@portHandleList,
    intf_mode   => 'ethernet',
    speed       => $speed,
    duplex      => $duplex,
    phy_mode    => $phy_mode,
});
&catch_error();

##################################################
# Configure multiple BGP Peers with count option #
##################################################
$_result_ = ixiahlt::emulation_bgp_config({
    port_handle      => $portHandleList[0],
    mode             => "reset",
    ip_version       => "4",
    local_ip_addr    => "192.1.1.2",
    remote_ip_addr   => "192.1.1.1",
    local_addr_step  => "0.0.1.0",
    remote_addr_step => "0.0.1.0",
    vlan_id          => 2,
    vlan_id_step     => 1,
    count            => $num_of_bgp_neighbors,
    neighbor_type    => "internal",
    local_as         => 200,
    local_as_step    => 1,       
    local_as_mode    => "increment"
});
&catch_error();

# Get the emulation BGP config return values
@status_keys = ixiahlt::status_item_keys();
$status      = ixiahlt::status_item('status');
my @ce_bgp_neighbor_handle_list = ixiahlt::status_item('handles');
print ("INFO: BGP Handles: @ce_bgp_neighbor_handle_list\n\n");

foreach my $bgp_neighbor_handle (@ce_bgp_neighbor_handle_list){
    #############################################
    # Clear BGP Stats					        #
    #############################################
    $_result_ = ixiahlt::emulation_bgp_info ({
        mode    => 'clear_stats',
        handle => $bgp_neighbor_handle
    });
    &catch_error();

    #############################################
    # Configure BGP routes on each BGP peer     #
    #############################################
    $_result_ = ixiahlt::emulation_bgp_route_config({
        mode	 	    => "add",                    
        handle	 	    => $bgp_neighbor_handle,  
        prefix	 	    => $prefix_ce1,             
        prefix_step	    => 1,                       
        netmask	 	    => "255.255.255.0",           
        num_routes	    => $num_of_prefix,          
        ip_version	    => "4",                       
        origin_route_enable => 1,                       
        origin	 	    => "igp"	
    }); 
    &catch_error();
    $prefix_ce1 = &ip_addr_incr($prefix_ce1, "0.1.0.0");
}

########################################################################
## Configure multiple BGP Peers and BGP routes on the second Ixia port #
########################################################################
$_result_ = ixiahlt::emulation_bgp_config({
    port_handle      => $portHandleList[1],
    mode             => "reset",
    ip_version       => "4",
    local_ip_addr    => "192.1.1.1",
    remote_ip_addr   => "192.1.1.2",
    local_addr_step  => "0.0.1.0",
    remote_addr_step => "0.0.1.0",
    vlan_id          => 2,
    vlan_id_step     => 1,
    count            => $num_of_bgp_neighbors,
    neighbor_type    => "internal",
    local_as         => 200,
    local_as_step    => 1,       
    local_as_mode    => "increment"
});
&catch_error();

# Get the emulation BGP config return values
@status_keys = ixiahlt::status_item_keys();
$status      = ixiahlt::status_item('status');
my @pe_bgp_neighbor_handle_list = ixiahlt::status_item('handles');
print ("INFO: BGP Handles: @pe_bgp_neighbor_handle_list\n\n");

foreach my $bgp_neighbor_handle (@pe_bgp_neighbor_handle_list){
    #############################################
    # Clear BGP Stats							#
    #############################################
    $_result_ = ixiahlt::emulation_bgp_info ({
        mode    => 'clear_stats',
        handle => $bgp_neighbor_handle
    });
    &catch_error();

    #############################################
    # Configure BGP routes on each BGP peer		#
    #############################################
    $_result_ = ixiahlt::emulation_bgp_route_config({
        mode	 	    => "add",                    
        handle	 	    => $bgp_neighbor_handle,  
        prefix	 	    => $prefix_ce2,             
        prefix_step	    => 1,                       
        netmask	 	    => "255.255.255.0",           
        num_routes	    => $num_of_prefix,          
        ip_version	    => "4",                       
        origin_route_enable => 1,                       
        origin	 	    => "igp"	
    }); 
    &catch_error();
    $prefix_ce2 = &ip_addr_incr($prefix_ce2, "0.1.0.0");
}

######################################################
## Start the BGP sessions						     #
######################################################
foreach (@portHandleList) {
    $_result_ = ixiahlt::emulation_bgp_control ({
        mode        => "start",
        port_handle => $_
    });
}
&catch_error();
print ("INFO: Sleeping to wait for BGP to come up...\n");
sleep(15);

######################################################
# Get Stats of BGP Sessions						     #
######################################################
foreach my $bgp_neighbor_handle (@pe_bgp_neighbor_handle_list) {
    $_result_ = ixiahlt::emulation_bgp_info ({
        mode    => 'stats',
        handle => $bgp_neighbor_handle
    });
    &catch_error();

    print ("INFO: \n"); 
    @status_keys = ixiahlt::status_item_keys();
    $status = ixiahlt::status_item('status');
    print ("INFO: $status\n\n");
    print ("\n\n########################################\n\n");

    foreach my $val (ixiahlt::status_item('sessions_established')) {
        if ($val eq "10") {
            print ("INFO: BGP session for $bgp_neighbor_handle is UP...\n");
        }
    }

    # Optionally Loop through all the key-value pairs and print them 
    #&display_all_values ( @status_keys );
}

######################################################
# Get BGP Stats									     #
######################################################
foreach my $bgp_neighbor_handle (@ce_bgp_neighbor_handle_list) {
    $_result_ = ixiahlt::emulation_bgp_info ({
        mode    => 'stats',
        handle => $bgp_neighbor_handle
    });
    &catch_error();
    
    print ("INFO: \n"); 
    @status_keys = ixiahlt::status_item_keys();
    $status = ixiahlt::status_item('status');
    print ("INFO: $status\n\n");
    print ("\n\n########################################\n\n");

    foreach my $val (ixiahlt::status_item('sessions_established')) {
        if ($val eq "10") {
            print ("INFO: BGP session for $bgp_neighbor_handle is UP...\n");
        }
    }

    # Optionally Loop through all the key-value pairs and print them 
    #&display_all_values ( @status_keys );
}

my $port_tx = $portHandleList[0];
my $port_rx = $portHandleList[1];
print ("INFO: Tx and Rx ports respectively are: \nTx: $port_tx \nRx: $port_rx\n");

######################################################
# Reset traffic									     #
######################################################
$_result_ = ixiahlt::traffic_config ({
        mode                 =>  "reset",
        port_handle          =>  $port_tx,
});
&catch_error();

#####################################################################
# Configuring Traffic												#
#																	#
# NOTE: You may use the track_by option to  specify the method of 	#	
# tracking the generated traffic									#
# in order to gather traffic statistics								#
#####################################################################
my $stream1 = ixiahlt::traffic_config({
    mode                 => 'create',
    traffic_generator    => 'ixnetwork_540',
    endpointset_count    => 1,
    transmit_mode        => "continuous",
    port_handle          => $port_tx,
    emulation_src_handle => \@ce_bgp_neighbor_handle_list,
    emulation_dst_handle => \@pe_bgp_neighbor_handle_list, 
    name                 => "IPv4_TRAFFIC",
    src_dest_mesh        => "one_to_one", 
    route_mesh           => "one_to_one",
    circuit_type         => "none",     
    circuit_endpoint_type => "ipv4",
    rate_percent         => 10,                                      
    tx_delay             => 10,                                      
    length_mode          => "fixed",                                   
    frame_size           => 512,
    track_by             => "endpoint_pair",
});
&catch_error();
my $tiName1  = ixiahlt::status_item("stream_id");

######################################################
# Clear the Stats on both ports					     #
######################################################
$_result_ = ixiahlt::traffic_control ({
        action               =>  "clear_stats",
        port_handle          =>  \@portHandleList,
});
&catch_error();

######################################################
# Start the traffic 							     #
######################################################
$_result_ = ixiahlt::traffic_control ({
        action               =>  "run",            
});     
&catch_error();

######################################################
# Wait for 60 seconds for the traffic to flow!	     #
######################################################
print ("INFO: Check now that that traffic is flowing...Let it flow for 1 minute\n");
sleep(60);

#############################################################################
# Stop the traffic															#
#																			#
# NOTE: Add the max_wait_timer option in case of medium to large ixncfg.  	#
# Without it, the script often fails.										#
#############################################################################
$_result_ = ixiahlt::traffic_control ({
        action               =>  "stop",
        max_wait_timer       =>  "60",
});
&catch_error();

######################################################
# Set mode to Traffic Items to display traffic stats #
######################################################
my $ti_traffic_status = ixiahlt::traffic_stats ({
        mode                 =>  "traffic_item",
});
&catch_error();
my @traffic_item_stats = ixiahlt::status_item('traffic_item');

### For Traffic Item
my $tx_frame_rate = ixiahlt::status_item("traffic_item.$tiName1.tx.total_pkt_rate");
my $rx_frame_rate = ixiahlt::status_item("traffic_item.$tiName1.rx.total_pkt_rate");
my $tx_total_pkts = ixiahlt::status_item("traffic_item.$tiName1.tx.total_pkts");
my $rx_total_pkts = ixiahlt::status_item("traffic_item.$tiName1.rx.total_pkts");
print ("INFO: traffic_item.$tiName1.tx.total_pkt_rate $tx_frame_rate\n");
print ("INFO: traffic_item.$tiName1.rx.total_pkt_rate $rx_frame_rate\n");
print ("INFO: traffic_item.$tiName1.tx.total_pkts $tx_total_pkts\n");
print ("INFO: traffic_item.$tiName1.rx.total_pkts $rx_total_pkts\n");

######################################################
# Gather and display aggregate statistics		     #
######################################################
my $aggregated_traffic_status = ixiahlt::traffic_stats ({
        mode                 =>  "all",
        port_handle          =>  \@portHandleList,
});
&catch_error();

my %packet_aggregate_mode = (
"Scheduled Frames Tx."               =>  "aggregate.tx.scheduled_pkt_count.max",
"Frames Tx."                         =>  "aggregate.tx.pkt_count.max",
"Total Frames Tx."                   =>  "aggregate.tx.total_pkts.sum",
"Total Frames Rx."                   =>  "aggregate.rx.total_pkts.sum",
"Bytes Tx."                          =>  "aggregate.tx.pkt_byte_count.sum",
"Bytes Rx."                          =>  "aggregate.rx.pkt_byte_count.sum",
"Data Integrity Frames Rx. Max"      =>  "aggregate.rx.data_int_frames_count.max",
"Data Integrity Frames Rx. Min"      =>  "aggregate.rx.data_int_frames_count.min",
"Data Integrity Errors Max"          =>  "aggregate.rx.data_int_errors_count.max"  ,
"Data Integrity Errors Min"          =>  "aggregate.rx.data_int_errors_count.min"  ,
"Valid Frames Rx."                   =>  "aggregate.rx.pkt_count.max",
"Valid Frames Rx. Rate"              =>  "aggregate.rx.pkt_rate",
"Traffic Item Total Packets Rate Tx" => "traffic_item.$tiName1.tx.total_pkt_rate", 
"Traffic Item Total Packets Rate Rx" => "traffic_item.$tiName1.rx.total_pkt_rate",
"Traffic Item Total packets Tx"      => "traffic_item.$tiName1.tx.total_pkts",
"Traffic Item Total packets Rx"      => "traffic_item.$tiName1.rx.total_pkts",
);

@status_keys = ixiahlt::status_item_keys();
$status = ixiahlt::status_item('status');
print ("\n\n########################################\n\n");
print ("\n @status_keys \n");
print ("\n\n########################################\n\n");
print ("INFO: FINAL STATS\n");
while (my ($k, $v) = each(%packet_aggregate_mode)) {
    $value = (ixiahlt::status_item($v));
    print ("\n\n$k => $value\n");
}

#######################################################
# Clean up the session:								  #
# Disconnects from  IxNetwork Tcl server,             #
# Tcl server, and Chassis. 	                          #
# Clears the ownership from a list of ports.		  #
#######################################################
$_result_ = ixiahlt::cleanup_session ({
    port_handle => \@portHandleList,
    reset       => 1
});
print ("\n\n$test_name : PASSED! \n\nTEST COMPLETED SUCCESSFULLY!\n");