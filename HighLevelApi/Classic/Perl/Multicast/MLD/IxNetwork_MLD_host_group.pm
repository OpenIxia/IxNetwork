################################################################################
# $Revision: 0.1                                                               #
# $Author:   Vijay Anantha Murthy                                              #
#                                                                              #
#    Copyright  1997 - 2012 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    17-10-2012 Initial Version 0.1                                            #
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

#############################################################################
#                                                                           #
# Description:                                                              #
#   This sample creates 10 MLD v2 hosts and a pool of two multicast groups  #
#   then adds the groups in the pool to each MLD hosts.                     #
#                                                                           #
#############################################################################
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
my $test_name      = "IxNetwork_MLD_host_group";
my $chassisIP      = "10.64.99.12";
my @port_list      = ("1/9", "1/10");
my $ixNetTclServer = "10.64.99.7";
my $user           = "ixiaHlpapiUser";

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
    $set_addr;
}

# Subroutine to print all key value pairs of Traffic Stats
my $ERROR                  = '';
my $ERRNO                  = '';
sub display_all_values {
    my @status_keys = @_;
    foreach my $key (@status_keys) {
        print ("\nINFO: Key value is $key\n\n");
        foreach my $i (ixiahlt::status_item($key)) {
            print ("\nINFO : iValue is $i\n\n");
        }
    }
}

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
    }
}

#######################################################
# Result:                                             #
#                                                     #
# my $ipv6_result =                                   #
# &add_ipv6("2000:0001:0002:0003:0004:0005:0006:0007",# 
# "0001:0000:0000:0000:0000:0000:0000:0001");         #
# INFO: Sum IP Address in ipv6 format                 #
# 2001:0001:0002:0003:0004:0005:0006:0008             #
#                                                     #
#######################################################
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

###########################################################
# Connects to the IxNetwork Tcl Server, 				  #
# Tcl Server, and the chassis.                            #
# Takes ownership of the ports.                           #
# Notes:                                                  #
# IxNetwork Tcl Server must be running on a client PC;    #
# Tcl Server must be running on a client PC;              #
# When using P2NO HLTSET, for loading the IxTclNetwork    #
# package please provide .ixnetwork_tcl_server parameter  #
# to ::ixia::connect                                      #
###########################################################
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

print ("INFO: After connect to IxNetwork TCL Server, connect status keys are [".@status_keys."]\n");

# Assign portHandleList with port handles values

foreach my $port (@port_list) {
    $port_handle = ixiahlt::status_item("port_handle.$chassisIP.$port");
    push(@portHandleList, $port_handle);
}

print ("INFO: Port Handle List ".@portHandleList."\n");

my $port_tx = $portHandleList[0];
my $port_rx = $portHandleList[1];
my $port_count = scalar (@portHandleList);
my $intf_count  = 5;
my $host_count  = 10;
my $group_count = 2;
my $src_ip_address          = &ip_expand_address("2000::1", 6);
my $src_ip_address_step     = &ip_expand_address("0:1::", 6);
my $host_ip_address         = &ip_expand_address("3000::1", 6);
my $host_ip_address_step    = &ip_expand_address("0:1::", 6);
my $group_range_ip_address  = &ip_expand_address("FF07::1", 6);
my $group_range_step        = &ip_expand_address("0::1:0", 6);
my $group_range_host_step   = &ip_expand_address("0::1", 6);

######################################################
# Configure 10 MLD hosts, MLD version 2              #
######################################################
$_result_ = ixiahlt::emulation_mld_config({
    mode              => 'create',
    port_handle       => $portHandleList[0],
    mld_version       => 'v2',
    count             => $host_count,
    intf_ip_addr      => $host_ip_address,
    intf_prefix_len   => '64',
    msg_interval      => '10',
    max_groups_per_pkts => '5',
    unsolicited_report_interval => '30',
    general_query     => '1',
    group_query       => '1',
    max_response_control => '1',
    max_response_time => '0',
    ip_router_alert   => '1',
    suppress_report   => '1',
    mac_address_init  => '0000.0000.0001',
    reset             => 1,
});
&catch_error();
my @mld_host_handle_list = ixiahlt::status_item('handle');

######################################################
#  For each MLD host, configure a group ranges       #
######################################################
my @group_range_handle_list; 
my $mcast_group_handle;
my $mld_host_handle; 
my $group_range_ip_address_temp = $group_range_ip_address;

$_result_ = ixiahlt::emulation_multicast_group_config ({
    mode            => 'create',
    num_groups      => $group_count,
    ip_addr_start   => $group_range_ip_address_temp,
    ip_addr_step    => $group_range_step,
    ip_prefix_len   => '64',
});
&catch_error();

$mcast_group_handle = ixiahlt::status_item('handle');
foreach (@mld_host_handle_list) {
    $_result_ = ixiahlt::emulation_mld_group_config ({
        mode                => 'create',
        session_handle      => $_,
        group_pool_handle   => $mcast_group_handle,
    });
    &catch_error();
}
 
######################################################
# Start MLD                                          #
######################################################
$_result_ = ixiahlt::emulation_mld_control({
    mode        => 'start',
    port_handle => $portHandleList[1],
});
&catch_error();

#######################################################
# Clean up the session:                               #
# Disconnects from  IxNetwork Tcl server,             #
# Tcl server, and Chassis.                            #
# Clears the ownership from a list of ports.          #
#######################################################
$_result_ = ixiahlt::cleanup_session ({
    port_handle => \@portHandleList,
    reset       => 1
});

print ("\n\n$test_name : TEST COMPLETED SUCCESSFULLY!\n");