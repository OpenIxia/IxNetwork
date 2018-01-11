################################################################################
# Version 1.2    $Revision: 3 $
# $Author: Lavinia Raicea $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    04/27/2005 Lavinia Raicea
#    07/20/2007 Matei-Eugen Vasile
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
#    This sample creates an IGMP v2 host. It creates a multicast group pool    #
#    and adds it to the host.                                                  #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 10.205.19.96
set port_list 2/1

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                       \
        -reset                                          \
        -device                         $chassisIP      \
        -port_list                      $port_list      \
        -username                       ixiaApiUser     \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}
set port_handle [keylget connect_status port_handle.$chassisIP.$port_list]

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config            \
        -port_handle                    $port_handle    \
        -autonegotiation                1               \
        -duplex                         full            \
        -speed                          ether100        \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

##################################################
#  Configure interfaces and create IGMP sessions #
##################################################
set igmp_status [::ixia::emulation_igmp_config            \
        -port_handle                    $port_handle    \
        -mode                           create          \
        -reset                                          \
        -msg_interval                   167             \
        -igmp_version                   v2              \
        -ip_router_alert                0               \
        -general_query                  0               \
        -group_query                    0               \
        -count                          1               \
        -intf_ip_addr                   100.41.1.2      \
        -neighbor_intf_ip_addr          100.41.1.1      \
        -intf_prefix_len                24              \
        ]
if {[keylget igmp_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmp_status log]"
}
set session [keylget igmp_status handle]

# Create multicast group pool
set mcast [::ixia::emulation_multicast_group_config     \
        -mode create                                    \
        -num_groups                     20              \
        -ip_addr_start                  225.0.1.1       \
        -ip_addr_step                   0.0.0.1         \
        -ip_prefix_len                  24              \
        ]
if {[keylget mcast status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget mcast log]"
}
set group [keylget mcast handle]

# Create IGMP group member by asociating a multicast group pool to a session
set gr_status [::ixia::emulation_igmp_group_config      \
        -mode                           create          \
        -session_handle                 $session        \
        -group_pool_handle              $group          \
        ]

if {[keylget gr_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget gr_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
