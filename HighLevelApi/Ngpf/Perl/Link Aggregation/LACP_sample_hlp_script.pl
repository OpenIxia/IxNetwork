################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright 1997 - 2015 by IXIA                                             #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    06/04/2015 - Sumit Deb - created sample                                   #
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
#    This script intends to demonstrate how to use NGPF LACP API.              #
#    Script uses four ports to demonstrate LAG properties                      #
#                                                                              #
#    1. It will create 2 LACP topologies, each having two ports which are      #
#       LAG members. It will then modify the Lag Id for both the LAG systems   #
#    2. Start the LACP protocol.                                               #
#    3. Retrieve protocol statistics and LACP per port statistics              #
#    4. Perform Simulate Link Down on port1 in System1-LACP-LHS                #
#    5. Retrieve protocol statistics and LACP per port statistics              #
#    6. Perform Simulate Link Up on port1 in System1-LACP-LHS                  #
#    7. Retrieve protocol statistics and LACP per port statistics              #
#    8. Stop All protocols                                                     #
#   Ixia Software:                                                             #
#    IxOS      6.90EA                                                          #
#    IxNetwork 7.50EA                                                          #
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
use lib $ENV{'PERL_HL_LIB_PATH'};
use ixiahlt {IXIA_VERSION => $ENV{'IXIA_VERSION'},
    TclAutoPath  => [$ENV{'PERL_IXOS_LIB_PATH'}, $ENV{'PERL_IXNET_LIB_PATH'}]};
#use ixiangpf;
use ixiahltgenerated;
use ixiangpf;

use warnings;
use strict;
use bignum;
use Carp;

# Using a hash reference for the HLP procedures
# (since they return values in form of hashes)
our $HashRef = {};
# Using a common variable to retain the status of each command
our $command_status = '';

my $_result_ = '';
my $_control_status_ = '';
my $_dhcp_stats_ = '';
my @status_keys = ();

################################################################################
# Connection to the chassis, IxNetwork Tcl Server                              #
################################################################################
my @chassis          = ('10.205.28.173');
my $tcl_server       = '10.205.28.173';
my @port_list        = (['1/1', '1/2', '1/3', '1/4']);
my $ixNetwork_client = '10.205.28.41:5555';

print "Connecting to chassis and client\n";
$_result_ = ixiangpf::connect({
    reset                => 1,
    device               => @chassis,
    port_list            => @port_list,
    ixnetwork_tcl_server => $ixNetwork_client,
    tcl_server           => $tcl_server,
    break_locks          => 1,
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

#  Creating a topology on 1st and 3rd port
print "Adding topology 1 on port 1 and port 3 \n";
my $topology_1_status = ixiangpf::topology_config ({
    topology_name => "{LAG1-LHS}",
    port_handle   => "$port_handles_list[0] $port_handles_list[2]",
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
    topology_handle         => "$topology_1_handle",
    device_group_name       => "{SYSTEM1-LACP-LHS}",
    device_group_multiplier => "1",
    device_group_enabled    => "1",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $deviceGroup_1_handle = $HashRef->{'device_group_handle'};


# Creating a topology on 2nd and 4th port
print "\nAdding topology 2 on port 2 and port 4\n";
my $topology_2_status = ixiangpf::topology_config ({
    topology_name => "{LAG1-RHS}",
    port_handle   => "$port_handles_list[1] $port_handles_list[3]",
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
    topology_handle         => "$topology_2_handle",
    device_group_name       => "{SYSTEM1-LACP-RHS}",
    device_group_multiplier => "1",
    device_group_enabled    => "1",
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
#  Configure LACP                                              #
################################################################################

# Creating ethernet stack for the first Device Group
print "Creating ethernet stack for the first Device Group\n";
my $ethernet_1_status = ixiangpf::interface_config ({
    protocol_name     => "{Ethernet 1}",
    protocol_handle   => "$deviceGroup_1_handle",
    mtu               => "1500",
    src_mac_addr      => "00.11.01.00.00.01",
    src_mac_addr_step => "00.00.01.00.00.00",
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
    protocol_name     => "{Ethernet 2}",
    protocol_handle   => "$deviceGroup_2_handle",
    mtu               => "1500",
    src_mac_addr      => "00.12.01.00.00.01",
    src_mac_addr_step => "00.00.01.00.00.00",
});
$HashRef = ixiangpf::get_result_hash();
$command_status = $HashRef->{'status'};
if ($command_status != $ixiangpf::SUCCESS) {
    my $error = ixiangpf::status_item('log');
    print "Error: $error";
    return "FAILED - $error";
}
my $ethernet_2_handle = $HashRef->{'ethernet_handle'};

# Creating LACP on top of Ethernet Stack for the first Device Group with actor key 00:00:00:00:06:66
print "\nCreating LACP on top of Ethernet Stack for the first Device Group with actor key 00:00:00:00:06:66\n";
    my $multivalue_1_status = ixiangpf::multivalue_config ({
        pattern                 => "counter",
        counter_start           => "00:00:00:00:00:01",
        counter_step            => "00:00:00:00:00:00",
        counter_direction       => "increment",
        nest_step               => "00:00:00:00:00:01",
        nest_owner              => "$topology_1_handle",
        nest_enabled            => "0",
        overlay_value           => "00:00:00:00:06:66,00:00:00:00:06:66",
        overlay_value_step      => "00:00:00:00:06:66,00:00:00:00:06:66",
        overlay_index           => "1,2",
        overlay_index_step      => "0,0",
        overlay_count           => "1,1",
    });
    if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    @status_keys = ixiangpf::status_item_keys();
    my $multivalue_1_handle = ixiangpf::status_item('multivalue_handle');
    
# Configuring SYSTEM1-lacp-LHS with Actor Key, System Id and flags
print ("Configuring SYSTEM1-lacp-LHS with Actor Key, System Id and flags\n");
    my $lacp_1_status = ixiangpf::emulation_lacp_link_config ({
        mode                                   => "create",
        handle                                 => "$ethernet_1_handle",
        active                                 => "1",
        session_type                           => "lacp",
        actor_key                              => "1",
        actor_port_num                         => "1",
        actor_key_step                         => "0",
        actor_port_num_step                    => "0",
        actor_port_pri                         => "1",
        actor_port_pri_step                    => "0",
        actor_system_id                        => "$multivalue_1_handle",
        administrative_key                     => "1",
        collecting_flag                        => "1",
        distributing_flag                      => "1",
        sync_flag                              => "1",
        aggregation_flag                       => "1",
    });
    if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    @status_keys = ixiangpf::status_item_keys();
    my $lacp_1_handle = ixiangpf::status_item('lacp_handle');
# Creating LACP on top of Ethernet Stack for the second Device Group with actor key 00:00:00:00:07:77 
print "\nCreating LACP on top of Ethernet Stack for the second Device Group with actor key 00:00:00:00:07:77\n";
      my $multivalue_2_status = ixiangpf::multivalue_config ({
        pattern                 => "counter",
        counter_start           => "00:00:00:00:00:02",
        counter_step            => "00:00:00:00:00:00",
        counter_direction       => "increment",
        nest_step               => "00:00:00:00:00:01",
        nest_owner              => "$topology_2_handle",
        nest_enabled            => "0",
        overlay_value           => "00:00:00:00:07:77,00:00:00:00:07:77",
        overlay_value_step      => "00:00:00:00:07:77,00:00:00:00:07:77",
        overlay_index           => "1,2",
        overlay_index_step      => "0,0",
        overlay_count           => "1,1",
    });
    if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    @status_keys = ixiangpf::status_item_keys();
    my $multivalue_2_handle = ixiangpf::status_item('multivalue_handle');

# Configuring SYSTEM1-lacp-LHS with Actor Key, System Id and flags
print ("Configuring SYSTEM1-lacp-LHS with Actor Key, System Id and flags\n");
    my $lacp_2_status = ixiangpf::emulation_lacp_link_config ({
        mode                                   => "create",
        handle                                 => "$ethernet_2_handle",
        active                                 => "1",
        session_type                           => "lacp",
        actor_key                              => "1",
        actor_port_num                         => "1",
        actor_key_step                         => "0",
        actor_port_num_step                    => "0",
        actor_port_pri                         => "1",
        actor_port_pri_step                    => "0",
        actor_system_id                        => "$multivalue_2_handle",
        administrative_key                     => "1",
        collecting_flag                        => "1",
        distributing_flag                      => "1",
        sync_flag                              => "1",
        aggregation_flag                       => "1",
    });
    if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
    }
    @status_keys = ixiangpf::status_item_keys();
    my $lacp_2_handle = ixiangpf::status_item('lacp_handle');

print "Waiting 5 seconds before starting protocol(s) ...\n";
sleep(5);

################################################################################
# Start protocol                                                               #
################################################################################
print "\nStarting StaticLAG on both topologies\n";
ixiahlt::test_control({action => 'start_all_protocols'});
print "Waiting for 30 seconds\n";
sleep(30);

################################################################################
# Get LACP learned_info stats                                                  #
################################################################################
print "\nFetching SYSTEM1-LACP-LHS learned_info\n\n";
my $learned_info = ixiangpf::emulation_lacp_info({
    handle => $lacp_1_handle,
    mode   => "global_learned_info",
    session_type => "lacp",
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
    my $allLi = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "=================================================================\n";
}
################################################################################
# Get LACP per-port stats                                                      #
################################################################################
print "\nFetching SYSTEM1-LACP-RHS per port stats \n\n";
my $stats_info = ixiangpf::emulation_lacp_info({
    handle => $lacp_2_handle,
    mode   => "per_port",
    session_type => "lacp",
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
    my $allLi = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "=================================================================\n";
}

sleep(5);
################################################################################
# Disable Synchronization flag on port1 in System1-LACP-LHS                    #
################################################################################
print("\n\nDisable Synchronization flag on port1 in System1-LACP-LHS\n");
my  $lag_port1Sync_status = ixiangpf::emulation_lacp_link_config({
    handle                   => $lacp_1_handle,
    mode                     => "modify",
    sync_flag                => "0",
    session_type             => "lacp",
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

################################################################################
# Get LACP learned_info stats                                                  #
################################################################################
print "\nFetching SYSTEM1-LACP-LHS learned_info\n\n";
my $learned_info = ixiangpf::emulation_lacp_info({
    handle => $lacp_1_handle,
    mode   => "global_learned_info",
    session_type => "lacp",
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
    my $allLi = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "=================================================================\n";
}
################################################################################
# Get LACP per-port   stats                                          #
################################################################################
print "\nFetching SYSTEM1-LACP-RHS per port stats \n\n";
my $stats_info = ixiangpf::emulation_lacp_info({
    handle => $lacp_2_handle,
    mode   => "per_port",
    session_type => "lacp",
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
    my $allLi = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "=================================================================\n";
}

sleep(5);

################################################################################
# Re-enable Synchronization flag on port1 in System1-LACP-LHS                  #
################################################################################
print("\n\nDisable Synchronization flag on port1 in System1-LACP-LHS\n");
my  $lag_port1Sync_status = ixiangpf::emulation_lacp_link_config({
    handle                   => $lacp_1_handle,
    mode                     => "modify",
    sync_flag                => "1",
    session_type             => "lacp",
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

################################################################################
# Get LACP learned_info stats                                                  #
################################################################################
print "\nFetching SYSTEM1-LACP-LHS learned_info\n\n";
my $learned_info = ixiangpf::emulation_lacp_info({
    handle => $lacp_1_handle,
    mode   => "global_learned_info",
    session_type => "lacp",
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
    my $allLi = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "=================================================================\n";
}
################################################################################
# Get LACP per-port stats                                                      #
################################################################################
print "\nFetching SYSTEM1-LACP-RHS per port stats \n\n";
my $stats_info = ixiangpf::emulation_lacp_info({
    handle => $lacp_2_handle,
    mode   => "per_port",
    session_type => "lacp",
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
    my $allVal = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allVal\n\n";
    print "=================================================================\n";
}
sleep(5);

################################################################################
# Perform Simulate Link Down on port1 in System1-LACP-LHS                      #
################################################################################
print("\n\nPerform Simulate Link Down on port1 in System1-LACP-LHS\n ");

my $result => ixiangpf::interface_config({
    port_handle     =>  $port_handles_list[0],
    op_mode     => "sim_disconnect",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
}
sleep(5);

################################################################################
# Get LACP learned_info stats                                                  #
################################################################################
print "\nFetching SYSTEM1-LACP-LHS learned_info\n\n";
my $learned_info = ixiangpf::emulation_lacp_info({
    handle => $lacp_1_handle,
    mode   => "global_learned_info",
    session_type => "lacp",
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
    my $allLi = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "=================================================================\n";
}
################################################################################
# Get LACP per-port   stats                                                    #
################################################################################
print "\nFetching SYSTEM1-LACP-RHS per port stats \n\n";
my $stats_info = ixiangpf::emulation_lacp_info({
    handle => $lacp_2_handle,
    mode   => "per_port",
    session_type => "lacp",
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
    my $allVal = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allVal\n\n";
    print "=================================================================\n";
}
sleep(5);
################################################################################
# Perform Simulate Link Up on port1 in System1-LACP-LHS                        #
################################################################################
print("\n\nPerform Simulate Link Up on port1 in System1-LACP-LHS\n ");

my $result => ixiangpf::interface_config({
    port_handle     =>  $port_handles_list[0],
    op_mode     => "normal",
});
if (ixiangpf::status_item('status') != $ixiangpf::SUCCESS) {
        handle_error();
}
sleep(5);

################################################################################
# Get LACP learned_info   stats                                                #
################################################################################
print "\nFetching SYSTEM1-LACP-LHS learned_info\n\n";
my $learned_info = ixiangpf::emulation_lacp_info({
    handle => $lacp_1_handle,
    mode   => "global_learned_info",
    session_type => "lacp",
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
    my $allLi = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allLi\n\n";
    print "=================================================================\n";
}
################################################################################
# Get LACP per-port stats                                                      #
################################################################################
print "\nFetching SYSTEM1-LACP-RHS per port stats \n\n";
my $stats_info = ixiangpf::emulation_lacp_info({
    handle => $lacp_2_handle,
    mode   => "per_port",
    session_type => "lacp",
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
    my $allVal = ixiangpf::status_item($my_key);
    print "=================================================================\n";
    print "\n$my_key: $allVal\n\n";
    print "=================================================================\n";
}
sleep(5);

###############################################################################
# Stop all protocols                                                          #
###############################################################################
print "Stopping all protocol(s) ...\n";
my $stop_status = ixiangpf::test_control({
    action      => "stop_all_protocols",
});

sleep(5);

print "!!! Test Script Ends !!!\n";

