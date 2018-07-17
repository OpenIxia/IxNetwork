#################################################################################
# Version 1    $Revision: #1 $
# $Author: cm $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-23-2013 Mchakravarthy - created sample
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
#    This sample loads ixnetwork config file with ELMI protocol configured on  #
#    ports and starts ELMI protocol and stops  protocol successfully           #
#    Evc status learned info is also retreived                                 #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################

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
my $test_name              = "ELMI_Protocol_Evc_Status_Learned_Info";
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
my @uniHandleList          = ();

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
# Retreive elmi config UNI handles
################################################################################

my $uni_handle_0 = ixiahlt::status_item("$port_0.emulation_elmi_config.uni_handles");
my $uni_handle_1 = ixiahlt::status_item("$port_1.emulation_elmi_config.uni_handles");
push(@uniHandleList, $uni_handle_0, $uni_handle_1);
print ("\nUNI handles are @uniHandleList ...\n");

################################################################################
# Start ELMI Protocol - Default Start
################################################################################

$_result_ = ixiahlt::emulation_elmi_control ( {
    port_handle            => \@portHandleList,
});

&catch_error();

sleep($wait_time);

################################################################################
# ELMI Protocol EVC status learned info
################################################################################

$_result_ = ixiahlt::emulation_elmi_info ( {
    handle            => \@uniHandleList,
    mode              => 'evc_status_learned_info',
});

&catch_error();

################################################################################
# Retreiving ELMI Protocol evc status learned info for one evcLearnedStatus
# from the available evcLearnedStatus list
################################################################################
my @evc_learned_status_list = ();
my @evc_learned_status_list = ixiahlt::status_item_keys("$port_0.$uni_handle_0");
my $evc_learned_status_0    = $evc_learned_status_list[0];

my $format = "%-40s %-s %-10s\n";
my @stat_list = ixiahlt::status_item_keys("$port_0.$uni_handle_0.$evc_learned_status_0");
print ("\n\nELMI evc learned status for Port: $port_0 EVC Learned Status: $evc_learned_status_0\n");
foreach my $stat (@stat_list) {
    my $stat_value = ixiahlt::status_item("$port_0.$uni_handle_0.$evc_learned_status_0.$stat");        
     printf $format, $stat, "=", $stat_value;
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
