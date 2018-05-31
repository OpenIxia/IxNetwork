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
# Script to demo Creation of Source and               #
# Multicast groups and retrieve handles               #
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
my $test_name      = "IxNetwork_PIM";
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
        print ("\n#################################################### \n");
        print ("ERROR: \n$test_name : ". ixiahlt::status_item('status'));
        print ("\n#################################################### \n");
        die ("ERROR: \n$test_name : Please check values and the port handles!!!");
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

print ("INFO: Port Handle List ".@portHandleList."\n");
my $port_tx = $portHandleList[0];
my $port_rx = $portHandleList[1];

#######################################################
# Configure layer 1 port settings (speed)             #
#######################################################
my $speed           = "auto";           # CHOICES ether10 ether100 ether1000 auto DEFAULT ether100 (for 10/100/1000 Ethernet cards)
my $autonegotiation = 1;                # CHOICES 0 1 DEFAULT 1
my $duplex          = "auto";           # CHOICES half full auto DEFAULT full
my $phy_mode        = "copper";         # CHOICES copper fiber DEFAULT copper

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
# Configure a PIM neighbor                            #
#######################################################
$_result_ = ixiahlt::emulation_pim_config({
    mode                       =>  "create",
    reset                      =>  1,
    port_handle                => $port_tx,
    count                      => 2,
    ip_version                 => 4,
    intf_ip_addr               => "3.3.3.100",
    intf_ip_addr_step          => "0.0.1.0",
    intf_ip_prefix_length      => 24,
    router_id                  => "11.0.0.1",
    router_id_step             => "0.0.0.1",
    neighbor_intf_ip_addr      => "22.0.0.1",
    dr_priority                => 10,
    bidir_capable              => 0,
    hello_interval             => 30,
    hello_holdtime             => 40,
    join_prune_interval        => 50,
    join_prune_holdtime        => 60,
    prune_delay_enable         => 1,
    prune_delay                => 600,
    override_interval          => 700,
    vlan                       => 1,
    vlan_id                    => 300,
    vlan_id_mode               => "increment",
    vlan_id_step               => 2,
    vlan_user_priority         => 7,
    mac_address_init           => "0000.0000.0001",
    gateway_intf_ip_addr       => "3.3.3.1",
    gateway_intf_ip_addr_step  => "0.0.1.0",
    prune_delay_tbit           => 1,
    send_generation_id         => 1,
    generation_id_mode         => "random",
    writeFlag                  => "nowrite",
});
&catch_error();

@status_keys = ixiahlt::status_item_keys();
my $vals;
foreach (@status_keys) {
    print ("\nINFO Keys are : $_\n");
    $vals = ixiahlt::status_item($_);
    print ("\nINFO Values are $vals\n"); 
}

my @pim_session_handle =  ixiahlt::status_item('handle');
my $pim_session1 = $pim_session_handle[0];
my $pim_session2 = $pim_session_handle[1];

#######################################################
# Configure Multicast Sources                         #
#######################################################
$_result_ =  ixiahlt::emulation_multicast_source_config ({
    mode            => 'create',
    num_sources     => 1,
    ip_addr_start   => '101.0.0.1',
    ip_addr_step    => '0.0.0.1',
    ip_prefix_len   => 24
});
&catch_error();

my $source_pool_handle = ixiahlt::status_item('handle');
print("\nINFO: source pool handle $source_pool_handle\n");

#######################################################
# Configure Multicast Groups                          #
#######################################################
$_result_ =  ixiahlt::emulation_multicast_group_config ({
    mode            => 'create',
    num_groups      => 1,
    ip_addr_start   => '225.0.0.1',
    ip_addr_step    => '0.0.0.1',
    ip_prefix_len   => 24,
});
&catch_error();

my $group_pool_handle = ixiahlt::status_item('handle');
print("\nINFO: group pool handle $group_pool_handle\n");

#######################################################
# Configure PIM Group with Session,                   # 
# Source and Group handles                            #
#######################################################
$_result_ = ixiahlt::emulation_pim_group_config({
    mode                           => 'create',
    session_handle                 =>  $pim_session1,
    group_pool_handle              =>  $group_pool_handle,
    source_pool_handle             =>  $source_pool_handle,
    rp_ip_addr                     => '44.0.0.1',
    group_pool_mode                => 'send',
    join_prune_aggregation_factor  => 10,
    wildcard_group                 => 1,
    s_g_rpt_group                  => 0,
    rate_control                   => 1,
    interval                       => 100,
    join_prune_per_interval        => 99,
    register_per_interval          => 101,
    register_stop_per_interval     => 102,
    flap_interval                  => 999,
    spt_switchover                 => 0,
    source_group_mapping           => 'one_to_one',
    switch_over_interval           => 200,
});
&catch_error();

my @port_group_member_handle = ixiahlt::status_item('handle');
my $port1_group_member_handle = $port_group_member_handle[0];

######################################################
# Configure RP                                       #
######################################################
$_result_ = ixiahlt::emulation_pim_group_config({
    mode                          => 'create',
    session_handle                => $pim_session1,
    group_pool_handle             => $group_pool_handle,
    source_pool_handle            => $source_pool_handle,
    rp_ip_addr                    => '33.0.0.1',
    group_pool_mode               => 'register',
    register_tx_iteration_gap     => 100,
    register_udp_destination_port => 44,
    register_udp_source_port      => 55,
    register_triggered_sg         => 0,
});
&catch_error();

#######################################################
# Configure PIM                                       #
#######################################################
$_result_ = ixiahlt::emulation_pim_config ({
    mode                      => 'create',
    reset                     => 1,
    port_handle               => $port_rx,
    pim_mode                  => 'sm',
    type                      => 'remote_rp',
    count                     => 2,
    ip_version                => 4,
    intf_ip_addr              => '3.3.3.1',
    intf_ip_addr_step         => '0.0.1.0',
    intf_ip_prefix_length     => 24,
    router_id                 => '12.0.0.1',
    router_id_step            => '0.0.0.1',
    neighbor_intf_ip_addr     => '22.0.0.1',
    dr_priority               => 10,
    bidir_capable             => 0,
    hello_interval            => 30,
    hello_holdtime            => 40,
    join_prune_interval       => 50,
    join_prune_holdtime       => 60,
    prune_delay_enable        => 1,
    prune_delay               => 600,
    override_interval         => 700,
    vlan                      => 1,
    vlan_id                   => 300,
    vlan_id_mode              => 'increment',
    vlan_id_step              => 2,
    vlan_user_priority        => 7,
    mac_address_init          => '0000.0000.0003',
    gateway_intf_ip_addr      => '3.3.3.100',
    gateway_intf_ip_addr_step => '0.0.1.0',
    prune_delay_tbit          => 1,
    send_generation_id        => 1,
    generation_id_mode        => 'random',
    writeFlag                 => 'nowrite',
});
&catch_error();

@port_group_member_handle = ixiahlt::status_item('handle');
my $port2_group_member_handle = $port_group_member_handle[0];

#######################################################
# Start the first PIM router per port.                #
# The second PIM router                               #
# is enabled by default.                              #
#######################################################
$_result_ = ixiahlt::emulation_pim_control ({
    mode           => 'start',
    handle         => $pim_session1,
    flap_interval  => 300,
    flap           => 1,
});
&catch_error();

$_result_ = ixiahlt::emulation_pim_control ({
    mode           => 'start',
    handle         => $pim_session2,
});
&catch_error();

#######################################################
# Stop the first PIM router per port                  #
#######################################################          
$_result_ = ixiahlt::emulation_pim_control ({
    mode           => 'stop',
    handle         => $pim_session1,
    flap_interval  => 200,
    flap           => 0,
});
&catch_error();

$_result_ = ixiahlt::emulation_pim_control ({
    mode           => 'stop',
    handle         => $pim_session2,
});
&catch_error();

#######################################################
# Stop PIM protocol on port_handle                    #
#######################################################
$_result_ = ixiahlt::emulation_pim_control ({
    mode           => 'stop',
    port_handle    => $port_tx,
});
&catch_error();

$_result_ = ixiahlt::emulation_pim_control ({
    mode           => 'stop',
    port_handle    => $port_rx,
});
&catch_error();

#######################################################
# Restart PIM protocol on port_handle                 #
#######################################################
$_result_ = ixiahlt::emulation_pim_control ({
    mode           => 'restart',
    port_handle    => $port_tx,
});
&catch_error();

$_result_ = ixiahlt::emulation_pim_control ({
    mode           => 'restart',
    port_handle    => $port_rx,
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