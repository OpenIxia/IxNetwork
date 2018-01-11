################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Eduard Tutescu $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#
# Description:
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
#    This sample configures two ports in IxNetwork and retrieve the ports      #
#    owner, type and name through the device_info procedure call               #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10/100/1000 STX4-256MB module.                 #
#                                                                              #
################################################################################

package require Ixia

proc keylprint {keylist {space ""}} {
    upvar $keylist kl
    set result ""
    foreach key [keylkeys kl] {
    set value [keylget kl $key]
    if {[catch {keylkeys value}]} {
        append result "$space$key: $value\n"
    } else {
        set newspace "$space "
        append result "$space$key:\n[keylprint value $newspace]"
    }
    }
    return $result
}

set test_name [info script]

set chassis_ip [list 10.205.16.98]
set port_list [list 7/1 7/2]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                    \
        -device    $chassis_ip     \
        -port_list $port_list     \
        -username  ixiaApiUser    \
        -ixnetwork_tcl_server localhost \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set i 0
foreach port $port_list {
    set port_${i} [keylget connect_status port_handle.$chassis_ip.$port]
    incr i
}
set port_list_info [list $port_0 $port_1]

# Getting information about the specified ports
set device_stat [::ixia::device_info                \
        -ports             $port_list_info         \
        -port_handle        $port_list_info         \
        ]
if {[keylget device_stat status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget device_stat log]"
}

puts [keylprint device_stat]

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1

