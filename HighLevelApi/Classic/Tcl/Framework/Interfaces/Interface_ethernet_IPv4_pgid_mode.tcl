################################################################################
# Version 1.1    $Revision: 2 $
# Author: Radu Antonescu
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    9-21-2003 Matei-Eugen Vasile
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
#    This sample configures an IPv4 VLAN Ethernet interface with pgid_mode.    #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET26
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 2/1 2/2 2/3 2/4]

################################################################################
# Connect to the chassis, reset to factory defaults and take ownership         #
################################################################################
set connect_status [::ixia::connect   \
        -reset                      \
        -device     $chassisIP      \
        -port_list  $port_list      \
        -username   ixiaApiUser     \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle_list [::ixia::get_port_list_from_connect $connect_status \
        $chassisIP $port_list]
        
set port_0 [lindex $port_handle_list 0]
set port_1 [lindex $port_handle_list 1]
set port_2 [lindex $port_handle_list 2]
set port_3 [lindex $port_handle_list 3]

################################################################################
# Configure interface in the test IPv4                                         #
################################################################################
set interface_status [::ixia::interface_config                                \
        -port_handle                $port_0             $port_1             \
        -intf_ip_addr               12.1.3.2            12.1.3.3            \
        -gateway                    12.1.3.1            12.1.3.1            \
        -netmask                    255.255.255.0       255.255.255.0       \
        -autonegotiation            1                   1                   \
        -src_mac_addr               0000.0005.0001      0000.0005.0002      \
        -op_mode                    normal              normal              \
        -pgid_mode                  split               split               \
        -pgid_split1_offset_from    start_of_frame      start_of_frame      \
        -pgid_split1_offset         52                  54                  \
        -pgid_split1_width          2                   4                   \
        -pgid_split1_mask           0xFFFF              0xFFFFFFFF          \
        -pgid_split2_offset_from    start_of_frame      start_of_frame      \
        -pgid_split2_offset         56                  58                  \
        -pgid_split2_width          3                   4                   \
        -pgid_split2_mask           0xFFFFFF            0xFFFFFFFF          \
        -pgid_split3_offset_from    start_of_frame      start_of_frame      \
        -pgid_split3_offset         60                  62                  \
        -pgid_split3_width          4                   4                   \
        -pgid_split3_mask           0xFFFFFFFF          0xFFFFFFFF          \
        -port_rx_mode               wide_packet_group   wide_packet_group   \
        -vlan                       $true               $true               \
        -vlan_id                    100                 100                 \
        -vlan_user_priority         7                   7                   \
        -duplex                     auto                auto                \
        -speed                      ether1000           ether1000           \
        -intf_mode                  ethernet            ethernet            \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
set intf_handle_list [keylget interface_status interface_handle]

set interface_status [::ixia::interface_config        \
        -port_handle            $port_2             \
        -intf_ip_addr           12.1.3.4            \
        -gateway                12.1.3.1            \
        -netmask                255.255.255.0       \
        -autonegotiation        1                   \
        -src_mac_addr           0000.0005.0001      \
        -op_mode                normal              \
        -pgid_mode              dscp                \
        -port_rx_mode           wide_packet_group   \
        -vlan                   $true               \
        -vlan_id                100                 \
        -vlan_user_priority     7                   \
        -duplex                 auto                \
        -speed                  ether1000           \
        -intf_mode              ethernet            \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
lappend intf_handle_list [keylget interface_status interface_handle]

set interface_status [::ixia::interface_config        \
        -port_handle            $port_3             \
        -intf_ip_addr           12.1.3.5            \
        -gateway                12.1.3.1            \
        -netmask                255.255.255.0       \
        -autonegotiation        1                   \
        -src_mac_addr           0000.0005.0001      \
        -op_mode                normal              \
        -port_rx_mode           wide_packet_group   \
        -vlan                   $true               \
        -vlan_id                100                 \
        -vlan_user_priority     7                   \
        -duplex                 auto                \
        -speed                  ether1000           \
        -intf_mode              ethernet            \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
lappend intf_handle_list [keylget interface_status interface_handle]

return "SUCCESS - $test_name - [clock format [clock seconds]]"
