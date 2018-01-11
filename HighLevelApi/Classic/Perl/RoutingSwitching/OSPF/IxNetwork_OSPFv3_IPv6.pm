################################################################################
# $Revision: 0.1                                                               #
# $Author: Vijay Anantha Murthy                                                #
#                                                                              #
#    Copyright © by IXIA                                                       #
#    1997 - 2012                                                               #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    11-08-2012      Initial Version 0.1                                       #
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

#######################################################
#                                                     #
# Description:                                        #
#    It uses two Ixia ports and configures            #
#    OSPFv3 and run traffic                           #
#                                                     #
#######################################################

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
my $ERROR                  = '';
my $ERRNO                  = '';
sub display_all_values {
    my @status_keys = ixiahlt::status_item_keys();
    foreach my $key (@status_keys) {
        print ("\nINFO: Key value is $key\n\n");
        foreach my $i (ixiahlt::status_item($key)) {
            print ("\nINFO : iValue is $i\n\n");
}}}

# Subroutine ip_iptobin
# Purpose           : Transform an IP address into a bit string
# Params            : IP address, IP version
# Returns           : bit string on success, undef otherwise
sub ip_iptobin {
    my ($ip, $ipversion) = @_;

    # v4 -> return 32-bit array
    if ($ipversion == 4) {
        return unpack('B32', pack('C4C4C4C4', split(/\./, $ip)));
    }

    # Strip ':'
    $ip =~ s/://g;

    # Check size
    unless (length($ip) == 32) {
        $ERROR = "Bad IP address $ip";
        $ERRNO = 102;
        return;
    }

    # v6 -> return 128-bit array
    return unpack('B128', pack('H32', $ip));
}

# Subroutine ip_bintoip
# Purpose           : Transform a bit string into an IP address
# Params            : bit string, IP version
# Returns           : IP address on success, undef otherwise
sub ip_bintoip {
    my ($binip, $ip_version) = @_;

    # Define normal size for address
    my $len = ip_iplengths($ip_version);
    if ($len < length($binip)) {
        $ERROR = "Invalid IP length for binary IP $binip\n";
        $ERRNO = 189;
        return;
    }

    # Prepend 0s if address is less than normal size
    $binip = '0' x ($len - length($binip)) . $binip;

    # IPv4
    if ($ip_version == 4) {
        return join '.', unpack('C4C4C4C4', pack('B32', $binip));
    }

    # IPv6
    return join(':', unpack('H4H4H4H4H4H4H4H4', pack('B128', $binip)));
}

# Subroutine ip_expand_address
# Purpose           : Expand an address from compact notation
# Params            : IP address, IP version
# Returns           : expanded IP address or undef on failure
sub ip_expand_address {
    my ($ip, $ip_version) = @_;

    unless ($ip_version) {
        $ERROR = "Cannot determine IP version for $ip";
        $ERRNO = 101;
        return;
    }

    # v4 : add .0 for missing quads
    if ($ip_version == 4) {
        my @quads = split /\./, $ip;

        my @clean_quads = (0, 0, 0, 0);

        foreach my $q (reverse @quads) {
            unshift(@clean_quads, $q + 1 - 1);
        }

        return (join '.', @clean_quads[ 0 .. 3 ]);
    }

    # Keep track of ::
    $ip =~ s/::/:!:/;

    # IP as an array
    my @ip = split /:/, $ip;

    # Number of octets
    my $num = scalar(@ip);
    foreach (0 .. (scalar(@ip) - 1)) {

        # Embedded IPv4
        if ($ip[$_] =~ /\./) {

            # Expand Ipv4 address
            # Convert into binary
            # Convert into hex
            # Keep the last two octets

            $ip[$_] =
              substr(
                ip_bintoip(ip_iptobin(ip_expand_address($ip[$_], 4), 4), 6),
                -9);

            # Has an error occured here ?
            return unless (defined($ip[$_]));

            # $num++ because we now have one more octet:
            # IPv4 address becomes two octets
            $num++;
            next;
        }
        # Add missing trailing 0s
        $ip[$_] = ('0' x (4 - length($ip[$_]))) . $ip[$_];
    }

    # Now deal with '::' ('000!')
    foreach (0 .. (scalar(@ip) - 1)) {

        # Find the pattern
        next unless ($ip[$_] eq '000!');

        # @empty is the IP address 0
        my @empty = map { $_ = '0' x 4 } (0 .. 7);

        # Replace :: with $num '0000' octets
        $ip[$_] = join ':', @empty[ 0 .. 8 - $num ];
        last;
    }

    return (lc(join ':', @ip));
}

# add ipv6 addresses
sub add_ipv6 {
    my ($addr_ipv6, $incr_ipv6) = @_;

    # Expand Ipv6 Addresses
    #$addr_ipv6 = &ip_expand_address($addr_ipv6, 6);
    #$incr_ipv6 = &ip_expand_address($incr_ipv6, 6);

    # Replace ':' with nothing
    $addr_ipv6 =~ s/://g;
    $incr_ipv6 =~ s/://g;

    # Convert the IPv6 string to 128 bit binary format
    my $addr_ipv6_bin = unpack('B128', pack('H32', $addr_ipv6));
    my $incr_ipv6_bin = unpack('B128', pack('H32', $incr_ipv6));

    # Convert 128 Bit binary format to IPv6 format; Not required but
    # mentioned for completeness purposes
    my $addr_ipv6_join = join(':', unpack('H4H4H4H4H4H4H4H4', pack('B128', $addr_ipv6_bin)));
    my $incr_ipv6_join = join(':', unpack('H4H4H4H4H4H4H4H4', pack('B128', $incr_ipv6_bin)));
    my $b  = $addr_ipv6_bin;
    my $e = $incr_ipv6_bin;

    # Check IP length
    unless (length($b) eq length($e)) {
        $ERROR = "IP addresses of different length\n";
        $ERRNO = 130;
        return;
    }

    # Reverse the two IPs
    $b = scalar(reverse $b);
    $e = scalar(reverse $e);
    my ($carry, $result, $c) = (0);

    # Foreach bit (reversed)
    for (0 .. length($b) - 1) {

        # add the two bits plus the carry
        $c     = substr($b, $_, 1) + substr($e, $_, 1) + $carry;
        $carry = 0;
        # sum = 0 => $c = 0, $carry = 0
        # sum = 1 => $c = 1, $carry = 0
        # sum = 2 => $c = 0, $carry = 1
        # sum = 3 => $c = 1, $carry = 1

        if ($c > 1) {
            $c -= 2;
            $carry = 1;
        }
        $result .= $c;
    }
    # Reverse result
    my $ipv6_result = join(':', unpack('H4H4H4H4H4H4H4H4', pack('B128', scalar(reverse($result)))));
    return $ipv6_result;
}

sub catch_error {
    if (ixiahlt::status_item('status') != 1) {
        print ("\n#################################################### \n");
        print ("ERROR: \n$test_name : ". ixiahlt::status_item('status'));
        print ("\n#################################################### \n");
        die ("ERROR: \n$test_name : Please check values and the port handles!!!");
}}

#################################################
# Source all libraries in the beginning         #
#################################################
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
my $test_name      = "IxNetwork_IPv6_OSPF";
my $chassisIP      = "10.64.99.12";
my @port_list      = ("1/9", "1/10");
my $ixNetTclServer = "10.64.99.7";
my $user           = "ixiaHlpapiUser";

# Declare all variables
my $_result_               = '';
my @status_keys            = ();
my %status_keys            = ();
my $port_handle            = '';
my $vport_list             = '';
my $vport_protocols_handle = '';
my $status                 = '';
my @_handles_              = ();
my @portHandleList         = ();
my $key                    = '';
my $value                  = '';
my $index                  = '';

#######################################################################
# Connects to the IxNetwork Tcl Server, Tcl Server, and the chassis.  #
# Takes ownership of the ports.                                       #
# Notes:                                                              #
# IxNetwork Tcl Server must be running on a client PC;                #
# Tcl Server must be running on a client PC;                          #
# When using P2NO HLTSET, for loading the IxTclNetwork package please #
# provide .ixnetwork_tcl_server parameter to ::ixia::connect          #
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

# Assign portHandleList with port handles values

foreach my $port (@port_list) {
    $port_handle = ixiahlt::status_item("port_handle.$chassisIP.$port");
    push(@portHandleList, $port_handle);
}

my $port_tx                   = $portHandleList[0];
my $port_rx                   = $portHandleList[1];
my $port_count                = scalar (@portHandleList);
my $tx_ip_address             = &ip_expand_address("2001::1", 6);
my $tx_ip_address_step        = &ip_expand_address("0:1::", 6);
my $rx_ip_address             = &ip_expand_address("2001::100", 6);
my $rx_ip_address_step        = &ip_expand_address("0:1::", 6);
my $local_ip_address          = &ip_expand_address("2001::1", 6);
my $local_ip_address_step     = &ip_expand_address("0:1::", 6);
my $router_id_address         = "21.0.0.2";
my $router_id_address_step    = "0.1.0.0";
my $route_range_ip_address    = &ip_expand_address("2000:1000::1", 6);
my $route_range_step          = &ip_expand_address("0:1000::", 6);

######################################################
# Initialize ports                                   #
######################################################
$_result_ = ixiahlt::interface_config ({
    mode            => 'config',
    intf_mode       => 'ethernet',
    autonegotiation => 1,
    speed           => 'auto',
    transmit_mode   => 'advanced',
    port_handle     => $portHandleList[0],
    ipv6_intf_addr => $tx_ip_address,
    ipv6_prefix_length => 64,
    ipv6_gateway => $rx_ip_address,
});
&catch_error();
my $tx_interface_handle = ixiahlt::status_item('interface_handle');

$_result_ = ixiahlt::interface_config ({
    mode            => 'config',
    intf_mode       => 'ethernet',
    autonegotiation => 1,
    speed           => 'auto',
    transmit_mode   => 'advanced',
    port_handle     => $portHandleList[1],
    ipv6_intf_addr => $rx_ip_address,
    ipv6_prefix_length => 64,
    ipv6_gateway => $tx_ip_address,
});
&catch_error();
my $rx_interface_handle = ixiahlt::status_item('interface_handle');

######################################################
# Configure an OSPFv3 emulated router on each port   #
######################################################
my @ospf_router_handle_list; 
my $local_ip_address_temp  =  $local_ip_address;
my $router_id_address_temp =  $router_id_address;
$_result_ = ixiahlt::emulation_ospf_config ({
    mode                => 'create',
    reset               => 1,
    session_type        => 'ospfv3',
    port_handle         => $portHandleList[0],
    router_id           => $router_id_address_temp,
    intf_ip_addr        => $tx_ip_address,
    intf_prefix_length  => 64,
    neighbor_intf_ip_addr => $rx_ip_address,
    count               => 1,
    area_id             => '0.0.0.0',
    area_type           => 'external-capable',
    network_type        => 'broadcast',
    option_bits         => '0x13',
    lsa_discard_mode    => 0,
});
&catch_error();
push(@ospf_router_handle_list, ixiahlt::status_item('handle'));

$router_id_address_temp = &ip_addr_incr($router_id_address, $router_id_address_step);
$_result_ = ixiahlt::emulation_ospf_config ({
    mode                  => 'create',
    reset                 => 1,
    session_type          => 'ospfv3',
    port_handle           => $portHandleList[1],
    router_id             => $router_id_address_temp,
    intf_ip_addr          => $rx_ip_address,
    intf_prefix_length    => 64,
    neighbor_intf_ip_addr => $tx_ip_address,
    count                 => 1,
    area_id               => '0.0.0.0',
    area_type             => 'external-capable',
    network_type          => 'broadcast',
    option_bits           => '0x13',
    lsa_discard_mode      => 0,
});
&catch_error();
push(@ospf_router_handle_list, ixiahlt::status_item('handle'));

######################################################
#  For each OSPFv3 router, configure a route range   #
######################################################
my $route_range_ip_address_temp =  $route_range_ip_address;
for (my $i = 0; $i < $port_count; $i++) {
    $_result_ = ixiahlt::emulation_ospf_topology_route_config ({
        mode                     => 'create',
        handle                   => $ospf_router_handle_list[$i],
        type                     => 'summary_routes',
        summary_prefix_start     => $route_range_ip_address_temp,
        summary_prefix_length    => 45,
        summary_number_of_prefix => 5,
    });
    &catch_error();
    $route_range_ip_address_temp = &add_ipv6($route_range_ip_address_temp, $route_range_step);
}

######################################################
# Clear Stats                                        #
######################################################
$_result_ = ixiahlt::emulation_ospf_info ({
    mode        => 'clear_stats',
    port_handle => \@portHandleList,
});
&catch_error();
 
######################################################
# Start OSPFv3                                       #
######################################################
$_result_ = ixiahlt::emulation_ospf_control ({
    port_handle => \@portHandleList,
    mode        => 'start',
});
&catch_error();

######################################################
# Retrieve Aggregated Stats                          #
######################################################
$_result_ = ixiahlt::emulation_ospf_info ({
     mode        => 'aggregate_stats',
     port_handle => $portHandleList[0],
});
&catch_error();
&display_all_values();

######################################################
# Retrieve Aggregated Stats                          #
######################################################
$_result_ = ixiahlt::emulation_ospf_info ({
     mode        => 'aggregate_stats',
     port_handle => $portHandleList[1],
});
&catch_error();
&display_all_values();

######################################################
# Retrieve Learned Info                              #
######################################################
#$_result_ = ixiahlt::emulation_ospf_info ({
#     mode        => 'learned_info',
#     handle      => $ospf_router_handle_list[1],
#});
#&catch_error();
#&display_all_values();

######################################################
# Wait for the routes to be learned                  #
######################################################
sleep(30);

###################################################################
# Configuring Traffic                                             #
#                                                                 #
# NOTE: You may use the track_by option to  specify the method of #
# tracking the generated traffic                                  #
# in order to gather traffic statistics                           #
###################################################################
my $stream1 = ixiahlt::traffic_config({
    mode                 => 'create',
    traffic_generator    => 'ixnetwork_540',
    endpointset_count    => 1,
    transmit_mode        => "continuous",
    emulation_src_handle => $port_tx,
    emulation_dst_handle => $port_rx,
    name                 => "IPv6_TRAFFIC",
    src_dest_mesh        => "one_to_one",
    route_mesh           => "one_to_one",
    circuit_type         => "none",
    circuit_endpoint_type => "ipv6",
    rate_percent         => 10,
    tx_delay             => 10,
    length_mode          => "fixed",
    frame_size           => 512,
    track_by             => "endpoint_pair",
});
&catch_error();
my $tiName1  = ixiahlt::status_item("stream_id");

######################################################
# Clear the Stats on both ports                      #
######################################################
$_result_ = ixiahlt::traffic_control ({
        action               =>  "clear_stats",
        port_handle          =>  \@portHandleList,
});
&catch_error();

######################################################
# Start the traffic                                  #
######################################################
$_result_ = ixiahlt::traffic_control ({
        action               =>  "run",
});
&catch_error();

######################################################
# Wait for 60 seconds for the traffic to flow!       #
######################################################
print ("INFO: Check now that that traffic is flowing...Let it flow for 1 minute\n");
sleep(60);

######################################################
# Stop the traffic                                   #
#                                                    #
# NOTE: Add the max_wait_timer option in case of     #
# medium to large ixncfg.                            #
# Without it, the script often fails.                #
######################################################
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
# Gather and display aggregate statistics            #
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

######################################################
# Clean up the session:                              #
# Disconnects from                                   #
# IxNetwork Tcl server, Tcl server, and Chassis.     #
# Clears the ownership from a list of ports.         #
######################################################
$_result_ = ixiahlt::cleanup_session ({
    port_handle => \@portHandleList,
    reset       => 1
});

print ("\n\n$test_name : PASSED! \n\nTEST COMPLETED SUCCESSFULLY!\n");