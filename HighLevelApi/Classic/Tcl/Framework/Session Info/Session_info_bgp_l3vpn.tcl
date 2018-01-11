################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LBose $
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
package require Ixia

# Declare the Chassis IP address and the Ports that will be used
set chassis_ip 10.206.27.55
set port_list [list]
set tcl_server 10.206.27.55
set ixnetwork_tcl_server 192.168.4.6

# Setting the absolute path for the IxNetwork configuration file.
set test_name  [info script]
set test_name_folder [file dirname $test_name]
set ixn_cfg [file join $test_name_folder session_info_bgp_l3vpn.ixncfg]

# Connect to the chassis, and load the configuration on ports using the 
# given IxNetwork configuration file. Also instruct not to load the 
# session resumes keys during connect.
set rval [ixia::connect                                 \
        -config_file            $ixn_cfg                \
        -ixnetwork_tcl_server   $ixnetwork_tcl_server   \
        -tcl_server             $tcl_server             \
        -session_resume_keys    0                       \
    ]
if {[keylget rval status] != $::SUCCESS} {
    error "connect failed: [keylget rval log]"
}

# Retrieve the session handles using the session_info and filter for bpg.
set rval [ixia::session_info                                        \
    -mode                           get_session_keys                \
    -session_keys_include_filter    {                               \
                                        connect.vport_list          \
                                        emulation_bgp_config        \
                                        emulation_bgp_route_config  \
                                    }                               \
]
if {[keylget rval status] != $::SUCCESS} {
    error "session_info failed: [keylget rval log]"
}

#Get the First VPort from the VPort List
set vport_0 [lindex [keylget rval vport_list] 0]


#Get the First BGP Session handle
set BGP_Session_Handle [lindex [keylget rval $vport_0.emulation_bgp_config.handles] 0]


# Disable the BGP configuration using the retrieved BGP session Handle.
set bgp_config_status [::ixia::emulation_bgp_config     \
        -mode          disable                          \
        -port_handle   $vport_0                         \
        -handle        $BGP_Session_Handle              \
    ]
if {[keylget bgp_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - $vport_0 BGP neighbors configuration failed. -\
            [keylget bgp_config_status log]"
    return 0
}

puts "SUCCESS - [clock format [clock seconds] -format {%D %X}]"
