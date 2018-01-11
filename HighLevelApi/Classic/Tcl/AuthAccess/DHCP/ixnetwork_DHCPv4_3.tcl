################################################################################
# Version 1.0    $Revision: 1 $
# $Author: MRidichie $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-18-2006 MRidichie
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
#    This sample configures one dhcp session.                                  #
#    Configures a group for that session using ethernet_ii, and retreives      #
#     statistics.                                                              #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10/100/1000 STXS4-256Mb module.                #
#                                                                              #
################################################################################

################################################################################
#  DUT configuration example:
#        ip dhcp pool ixiaTest
#        network 200.200.141.0 255.255.255.0
#        exit
#        default interface f5/0
#        int f5/0
#        ip address 200.200.141.1 255.255.255.0
#        no shut
#        exit
#        service dhcp
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 10.205.19.121
set port_list [list 1/3]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassisIP      \
        -port_list              $port_list      \
        -username               ixiaApiUser     ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [keylget connect_status port_handle.$chassisIP.$port_list]

################################################################################
# Configure DHCP session
################################################################################
set dhcp_portHandle_status [::ixia::emulation_dhcp_config \
        -mode                        create               \
        -port_handle                 $port_handle         \
        -lease_time                  311                  \
        -max_dhcp_msg_size           1000                 \
        -version                     ixnetwork             \
        -reset                                            \
        -no_write                                         ]
if {[keylget dhcp_portHandle_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dhcp_portHandle_status log]"
}
set sess_handle [keylget dhcp_portHandle_status handle]

################################################################################
# Configure DHCP group
################################################################################
set dhcp_group_status [::ixia::emulation_dhcp_group_config \
        -mode          create                              \
        -mac_addr      00.10.95.22.11.09                   \
        -mac_addr_step 00.00.00.aa.00.00                   \
        -num_sessions  10                                  \
        -handle        $sess_handle                        \
        -encap         ethernet_ii                         \
        -vlan_user_priority 2                              \
        -version       ixnetwork                            ]
if {[keylget dhcp_group_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dhcp_group_status log]"
}


############################################################################
# START DHCP
############################################################################

set control_status_0 [::ixia::emulation_dhcp_control \
        -port_handle $port_handle                         \
        -action            bind                      \
        ]
if {[keylget control_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status_0 log]"
    return 0
}


after 30000

##################################################
#             GET DHCP STATISTICS                #
##################################################
set dhcp_stats_0 [::ixia::emulation_dhcp_stats      \
            -port_handle $port_handle                     \
            -version     ixnetwork                         \
    	]
    if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
        puts "FAIL - $test_name -[keylget dhcp_stats_0 log]"
        return 0
    }
##################################################
#            PRINT DHCP STATISTICS               #
##################################################


proc show_stats var {
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
            if {$key == "status"} {continue}
            set indent [string repeat "    " $level] 
            puts -nonewline $indent 
            if {[catch {keylkeys var $key}]} {
                puts "$key: [keylget var $key]"
                continue
            } else {
                puts $key
                puts "$indent[string repeat "-" [string length $key]]"
            }
            show_stats [keylget var $key]
    }
}

show_stats $dhcp_stats_0 



return "SUCCESS - $test_name - [clock format [clock seconds]]"

