# Source all libraries in the beginning
use warnings;
use strict;
use bignum;
use Carp;
use Cwd 'abs_path';

# use lib where the HLPAPI files are located
# It is typically: "C:/Program Files/Ixia/hltapi/<version_number>/TclScripts/lib/hltapi/library/common/ixia_hl_lib-<version>"
# For Ex:
# use lib "C:/Program Files/Ixia/hltapi/4.70.0.213/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.10";
use lib "C:/Program Files/Ixia/hltapi/4.80.0.4/TclScripts/lib/hltapi/library/common/ixia_hl_lib-7.10";

use ixiahlt;
use ixiaixn;

# Declare the Chassis IP address and the Ports that will be used
my $test_name              = "ELMI_Protocol_Aggregated_Statistics";
my $chassis_ip             = "10.206.27.55";
my $tcl_server             = "127.0.0.1";
my @port_list              = ("8/1", "8/2");
my $ixnetwork_tcl_server   = "127.0.0.1";
my $wait_time              = 5;
my $test_dir_path          = abs_path();
my $ixn_cfg                = join('/', "$test_dir_path", "ELMI_b2b.ixncfg");

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

################################################################################
# START - Connect to the chassis
################################################################################

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect

$_result_ = ixiahlt::connect ( {
    mode                   => "connect",
    ixnetwork_tcl_server   => $ixnetwork_tcl_server,
    tcl_server             => $tcl_server,
    config_file            => "$ixn_cfg",
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

my $port_0 = $portHandleList[0];
my $port_1 = $portHandleList[1];

print ("\nIxia port handles are @portHandleList ...\n");
print ("End connecting to chassis ...\n");

################################################################################
# END - Connect to the chassis
################################################################################

################################################################################
# Start ELMI Protocol - Default Start
################################################################################

$_result_ = ixiahlt::emulation_elmi_control ( {
    port_handle            => \@portHandleList,
});

&catch_error();

sleep($wait_time);

################################################################################
# ELMI Protocol Aggregated Statistics
################################################################################

$_result_ = ixiahlt::emulation_elmi_info ( {
    port_handle            => \@portHandleList,
});

&catch_error();

my $format = "%-40s %-s %-10s\n";

foreach my $port (@portHandleList) {
    my @stat_list = ixiahlt::status_item_keys("$port.aggregate");
    print ("\n\nELMI Aggregated Stats for Port: $port\n");
    foreach my $stat (@stat_list) {
        my $stat_value = ixiahlt::status_item("$port.aggregate.$stat");        
         printf $format, $stat, "=", $stat_value;
    }
}

################################################################################
# Stop ELMI Protocol
################################################################################

$_result_ = ixiahlt::emulation_elmi_control ( {
    port_handle            => \@portHandleList,
    mode                   => 'stop'
});

&catch_error();

print ("\n\n$test_name : TEST COMPLETED SUCCESSFULLY!\n");
