################################################################################
# Version 1.0    $Revision: #1 $
# $Author: cm $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-20-2013 LBose - Initial Version
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
#    This sample script loads an IxNetwork configuration for bgp L3 VPN and    #
# retrieves the sessions handles using session_info                            #
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
my $test_name              = "Session_info_bgp_l3vpn";
my $chassis_ip             = "10.206.27.55";
my $tcl_server             = "10.206.27.55";
my @port_list              = ();
my @vport_list             = ();
my @session_handles        = ();
my $ixnetwork_tcl_server   = "192.168.4.6";


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

# Connect to the chassis, and load the configuration on ports using the 
# given IxNetwork configuration file. Also instruct not to load the 
# session resumes keys during connect.
$_result_ = ixiahlt::connect ( {
    config_file            => 'session_info_bgp_l3vpn.ixncfg',
    ixnetwork_tcl_server   => $ixnetwork_tcl_server,
    tcl_server             => $tcl_server,
    session_resume_keys    => 0,
});
&catch_error();

my @session_filter = ("connect.vport_list", "emulation_bgp_config", "emulation_bgp_route_config");
# Retrieve the session handles using the session_info and filter for bpg.
$_result_ = ixiahlt::session_info ( {
    mode                          =>   'get_session_keys',    
    session_keys_include_filter   =>  \@session_filter,  
});
&catch_error();

#Get the First VPort from the VPort List
@vport_list = ixiahlt::status_item('vport_list');
my $vport_0 = $vport_list[0];


#Get the First BGP Session handle
@session_handles = ixiahlt::status_item("$vport_0.emulation_bgp_config.handles");
my $BGP_Session_Handle = $session_handles[0];


# Disable the BGP configuration using the retrieved BGP session Handle.
$_result_ = ixiahlt::emulation_bgp_config ( {
    mode          => 'disable',
    port_handle   => $vport_0,
    handle        => $BGP_Session_Handle,
});
&catch_error();

print ("\n\n$test_name : TEST COMPLETED SUCCESSFULLY!\n");
