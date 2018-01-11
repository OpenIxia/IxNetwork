################################################################################
# Version 1    $Revision: 1 $
# $Author: RAntonescu $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    02-11-2008 RAntonescu - created sample
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
#    This sample configures two interfaces: Ethernet and ATM. For each         #
#    interface, sets a MTU value that is different from the default MTU value. #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 and LM622MR module.                #
#    The sample was tested with HLTSET27 and HLTSET26.                         #
#                                                                              #
################################################################################
package req Ixia

set test_name [info script]

set chassisIP sylvester

# The first port should be an Ethernet port and the second port should be an 
# ATM port
set port_list {3/1 2/1}

################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
################################################################################
set connect_status [::ixia::connect \
        -device     $chassisIP      \
        -port_list  $port_list      \
        -reset                      \
        -username   ixiaApiUser     \
        ]
if {[keylget connect_status status] == $::FAILURE} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
}

array set port_array [join [keylget connect_status port_handle.$chassis_name]]

set port_0 $port_array([lindex $port_list 0])
set port_1 $port_array([lindex $port_list 1])

################################################################################
# Configure interface on ethernet in the test
################################################################################
set interface_status [::ixia::interface_config  \
        -port_handle    $port_0                 \
        -intf_ip_addr   1.1.1.1                 \
        -mtu            576                     \
        ]
if {[keylget interface_status status] == $::FAILURE} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}
        
################################################################################
# Configure interfaceon ATM in the test
################################################################################
set interface_status [::ixia::interface_config         \
        -port_handle         $port_1                   \
        -atm_encapsulation   LLCBridgedEthernetNoFCS   \
        -atm_interface_type  uni                       \
        -intf_mode           atm                       \
        -vpi                 8                         \
        -vci                 36                        \
        -intf_ip_addr        1.1.1.2                   \
        -mtu                 4560                      \
        ]
if {[keylget interface_status status] == $::FAILURE} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return
