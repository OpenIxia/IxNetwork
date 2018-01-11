################################################################################
# $Revision: 0.1                                                               #
# $Author:  Vijay Anantha Murthy                                               #
#                                                                              #
#    Copyright  1997 - 2012 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    21-11-2012 Initial Version     0.1                                        #
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
#                                                     #
# This sample creates two RSVP neighbors on two       #
# different ports. One is onfigured as Ingress LSR    #
# the other as Egress LSR. Then the emulated          #
# neighbors are started and tunnel info is displayed. #
#                                                     #
#######################################################
# Source all libraries in the beginning
use warnings;
use strict;
use bignum;
use Carp;

# use lib where the HLPAPI files are located
# This can be moved to .pl files in the JT framework
# It is typically: "/volume/labtools/ixia/<version_number>/lib/library/common/ixia_hl_lib-<version>"
# For Ex:
# use lib "/volume/labtools/ixia/6.30.850.7/lib";
# use lib "/volume/labtools/ixia/6.30.850.7/lib/library/common/ixia_hl_lib-6.30";
use lib "/home/vmurthy/hlpapi/ixos/ixos6.30.850.7/lib";
use lib "/home/vmurthy/hlpapi/ixos/ixos6.30.850.7/lib/library/common/ixia_hl_lib-6.30";
use ixiahlt;
use ixiaixn;

# Declare the Chassis IP address and the Ports that will be used
my $test_name      = "IxNetwork_RSVP_tunnel_info";
my $chassisIP      = "10.64.99.12";
my @port_list      = ("1/9", "1/10");
my $ixNetTclServer = "10.64.99.7";
my $user           = "ixiaHlpapiUser";

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

sub catch_error {
    if (ixiahlt::status_item('status') != 1) {
        print ("n#################################################### n");
        print ("ERROR: n$test_name : ". ixiahlt::status_item('status'));
        print ("n#################################################### n");
        die ("ERROR: n$test_name : Please check values and the port handles!!!");
}}

#######################################################
# Connects to the IxNetwork Tcl Server,               #
# Tcl Server, and the chassis.                        #
# Takes ownership of the ports.                       #
# Notes:                                              #
# IxNetwork Tcl Server must be running on a client PC #
# Tcl Server must be running on a client PC           #
# When using P2NO HLTSET, for loading the             #
# IxTclNetwork package please                         #
# provide .ixnetwork_tcl_server parameter             #
# to ::ixia::connect                                  #
#######################################################
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

#######################################################
# Configure layer 1 port settings (speed)             #
#######################################################
my $speed           = "auto";
my $autonegotiation = 1;
my $duplex          = "auto";
my $phy_mode        = "copper";

$_result_ = ixiahlt::interface_config({
    mode        => 'config',
    port_handle => \@portHandleList,
    intf_mode   => 'ethernet',
    speed       => $speed,
    duplex      => $duplex,
    phy_mode    => $phy_mode,
});
&catch_error();

#######################################################
#  Configure a RSVP neighbor on ingress_port          #
#######################################################
$_result_ = ixiahlt::emulation_rsvp_config ({
	mode                       => 'create',
	reset                      => 1,
	port_handle                => $portHandleList[0],
	count                      => 1,
	refresh_reduction          => 0,
	reliable_delivery          => 0,
	bundle_msgs                => 0,
	hello_msgs                 => 1,
	hello_interval             => 200,
	hello_retry_count          => 4,
	refresh_interval           => 200,
	srefresh_interval          => 300,
	egress_label_mode          => 'nextlabel',
	path_state_refresh_timeout => 77,
	path_state_timeout_count   => 5,
	record_route               => 1,
	resv_confirm               => 1,
	resv_state_timeout_count   => 5,
	resv_state_refresh_timeout => 5,
	min_label_value            => 20,
	max_label_value            => 30,
	vlan                       => 1,
	vlan_id                    => 300,
	vlan_id_mode               => 'fixed',
	vlan_id_step               => 2,
	mac_address_init           => '0000.0000.0001',
	intf_prefix_length         => 24,
	ip_version                 => 4,
	intf_ip_addr               => '3.3.3.100',
	intf_ip_addr_step          => '0.0.1.0',
	neighbor_intf_ip_addr      => '3.3.3.1',
	neighbor_intf_ip_addr_step => '0.0.1.0',
});
&catch_error();

my @rsvp_ingress_handle_list = ixiahlt::status_item("handles");
my $ingress_handle = $rsvp_ingress_handle_list[0];

#######################################################
#  Configure a RSVP neighbor on egress_port           #
#######################################################
$_result_ = ixiahlt::emulation_rsvp_config ({
	mode                       => 'create',
	reset                      => 1,
	port_handle                => $portHandleList[1],
	count                      => 1,
	refresh_reduction          => 0,
	reliable_delivery          => 0,
	bundle_msgs                => 0,
	hello_msgs                 => 1,
	hello_interval             => 200,
	hello_retry_count          => 4,
	refresh_interval           => 200,
	srefresh_interval          => 300,
	egress_label_mode          => 'nextlabel',
	path_state_refresh_timeout => 77,
	path_state_timeout_count   => 5,
	record_route               => 1,
	resv_confirm               => 1,
	resv_state_timeout_count   => 5,
	resv_state_refresh_timeout => 5,
	min_label_value            => 20,
	max_label_value            => 30,
	vlan                       => 1,
	vlan_id                    => 300,
	vlan_id_mode               => 'fixed',
	vlan_id_step               => 2,
	mac_address_init           => '0000.0000.0002',
	intf_prefix_length         => 24,
	ip_version                 => 4,
	intf_ip_addr               => '3.3.3.1',
	intf_ip_addr_step          => '0.0.1.0',
	neighbor_intf_ip_addr      => '3.3.3.100',
	neighbor_intf_ip_addr_step => '0.0.1.0',
});
&catch_error();

my @rsvp_egress_handle_list = ixiahlt::status_item("handles");
my $egress_handle = $rsvp_egress_handle_list[0];

#######################################################
#  Configure a RSVP Destination Range along with      #
#  Sender Range                                       #
#  handle        - retured from the previous call     #
#  rsvp_behavior - rsvpIngress                        #
#######################################################
my @handleList;
my $egress_ip_addr = '2.2.2.100';
my $sender_ip_addr = '4.4.4.100';
my @rro_ipv4_list  = ('101.0.0.1', '202.0.0.1');
my @rro_label_list = ('11', '22');
my @rro_ctype_list = ('33', '44');
my @rro_flags_list = ('9',  '12');
my @ero_ipv4_list  = ('33.0.0.1', '44.0.0.1');
my @ero_as_num_list = ('33',  '44');
my @ero_flags_list  = ('9', '11');
my @ero_pfxlen_list = ('1', '1');
my @ero_loose_list  = ('1',  '0');

# RSVP tunnel config for ingress port
$_result_ = ixiahlt::emulation_rsvp_tunnel_config ({
	mode                             =>  'create',
	handle                           =>  $ingress_handle,
	rsvp_behavior                    =>  'rsvpIngress',
	count                            =>  3,
	egress_ip_addr                   =>  $egress_ip_addr,
	egress_ip_step                   =>  '0.1.0.0',
	ingress_ip_addr                  =>  $sender_ip_addr,
	ingress_ip_step                  =>  '0.1.0.0',
	ingress_bandwidth                =>  1000,
	sender_tspec_token_bkt_rate      =>  10,
	sender_tspec_token_bkt_size      =>  10,
	sender_tspec_peak_data_rate      =>  10,
	sender_tspec_min_policed_size    =>  5,
	sender_tspec_max_pkt_size        =>  580,
	session_attr_bw_protect          =>  1,
	session_attr_se_style            =>  1,
	session_attr_local_protect       =>  1,
	session_attr_label_record        =>  0,
	session_attr_setup_priority      =>  2,
	session_attr_hold_priority       =>  2,
	session_attr_resource_affinities =>  1,
	session_attr_ra_include_all      =>  0x11223344,
	lsp_id_start                     =>  100,
	tunnel_id_start                  =>  5,
	tunnel_id_count                  =>  2,
	tunnel_id_step                   =>  10,
	ero_mode                         =>  'loose',
	ero_dut_pfxlen                   =>  16,
	rro                              =>  1,
	rro_list_type                    =>  'label',
	rro_list_ipv4                    =>  \@rro_ipv4_list,
	rro_list_label                   =>  \@rro_label_list,
	rro_list_flags                   =>  \@rro_flags_list,
	rro_list_ctype                   =>  \@rro_ctype_list,
	ero                              =>  1,
	ero_list_type                    =>  'as',
	ero_list_loose                   =>  \@ero_loose_list,
	ero_list_ipv4                    =>  \@ero_ipv4_list,
	ero_list_pfxlen                  =>  \@ero_pfxlen_list,
	ero_list_as_num                  =>  \@ero_as_num_list,
	fast_reroute                     =>  1,
	fast_reroute_bandwidth           =>  1000,
	fast_reroute_exclude_any         =>  'aabbccdd',
	fast_reroute_holding_priority    =>  1,
	fast_reroute_hop_limit           =>  5,
	fast_reroute_setup_priority      =>  7,
	one_to_one_backup                =>  1,
	send_detour                      =>  1,
	plr_id                           =>  '11.0.0.1',
	avoid_node_id                    =>  '22.0.0.1',
	session_attr_name                =>  'MyAttr',
});
&catch_error();

push (@handleList, ixiahlt::status_item("tunnel_handle"));

#######################################################
# Tunnel config for Egress port                       #
#######################################################
$_result_ = ixiahlt::emulation_rsvp_tunnel_config ({
	mode           => 'create',
	handle         => $egress_handle,
	rsvp_behavior  => 'rsvpEgress',
	count          => 3,
	egress_ip_addr => $egress_ip_addr,
	egress_ip_step => '0.1.0.0',
});
&catch_error();

#######################################################
#  Start RSVP Protocol                                #
#######################################################
$_result_ = ixiahlt::emulation_rsvp_control ({
	mode        => 'start',
	port_handle => \@portHandleList,
});
&catch_error();

print ("INFO: Wait for 10 seconds before getting the rsvp tunnelinfo");
sleep(10);

#######################################################
#  Get RSVP Tunnel Info                               #
#######################################################
$_result_ = ixiahlt::emulation_rsvp_tunnel_info ({
	handle      => $ingress_handle,
	port_handle => $portHandleList[0],
});
&catch_error();

my $total_lsp_count = ixiahlt::status_item("total_lsp_count");
my $inbound_lsp_count = ixiahlt::status_item("inbound_lsp_count");
my $outbound_lsp_count = ixiahlt::status_item("outbound_lsp_count");
my $outbound_up_count = ixiahlt::status_item("outbound_up_count");
my $outbound_down_count = ixiahlt::status_item("outbound_down_count");
my $label = ixiahlt::status_item("label");

print ("\n*********************************************\n");
print ("INFO: total_lsp_count         : $total_lsp_count\n");
print ("INFO: inbound_lsp_count       : $inbound_lsp_count\n");
print ("INFO: outbound_lsp_count      : $outbound_lsp_count\n");
print ("INFO: outbound_up_count       : $outbound_up_count\n");
print ("INFO: outbound_down_count     : $outbound_down_count\n");
print ("INFO: label                   : $label\n");
print ("\n*********************************************\n");

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
