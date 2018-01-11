################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Stefan Popi $
#
#    Copyright © 1997 - 2011 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    32-09-2011 Stefan Popi
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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample configures l1 parameters for 40/100Gig card types.            #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on IxNetwork virtual ports                          #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 127.0.0.1
set ixnetwork_tcl_server 127.0.0.1
set port_nr 4

# Connect to the chassis, reset to factory defaults and take ownership

set ret_val [::ixia::connect                            \
        -vport_count            $port_nr                \
        -ixnetwork_tcl_server   $ixnetwork_tcl_server   \
        -reset                                          ]
if {[keylget ret_val status] != $::SUCCESS} {
    puts "FAILURE - [keylget ret_val log]"
    return 0
}


set vport_list  [keylget ret_val vport_list]
set port_type   [list ethernet ethernet ethernet ethernet]
set tcs         [list internal_ppm_adj internal_ppm_adj internal external]
set ppm_adjust  [list 10 20 30 40]
set vport_speed [list ether40Gig ether100Gig ether40000lan ether100000lan]

########################################
# Configure l1 properties in the test  #
########################################

foreach vport_handle $vport_list port_type $port_type tcs $tcs ppm $ppm_adjust speed $vport_speed {
    set ret_val [::ixia::interface_config             \
            -port_handle            $vport_handle     \
            -intf_mode              $port_type        \
            -transmit_clock_source  $tcs              \
            -internal_ppm_adjust    $ppm              \
            -speed                  $speed            ]
    if {[keylget ret_val status] != $::SUCCESS} {
        puts "FAILURE - interface_config - $port_type - [keylget ret_val log]"
        return 0
    }
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
