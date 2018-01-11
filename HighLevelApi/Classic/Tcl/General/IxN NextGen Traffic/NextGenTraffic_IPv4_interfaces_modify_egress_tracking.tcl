################################################################################
# Version 1.0    $Revision: 1 $
# $Author: E. Tutescu $
#
#    Copyright © 1997 - 2012 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    19-01-2012 E. Tutescu - Created sample
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
#    This sample creates a back-to-back setup using two Ixia ports.            #
#    It configures one IPv4 Ethernet interface on each port and creates/modify #
#    a traffic item with two egress tracking elements.                         #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a XM12 module.                                   #
#                                                                              #
################################################################################
package require Ixia

# Setting session variables
set chassisIp               10.205.16.98
set portList                [list 7/1 7/2]
set ixnetwork_tcl_server    "localhost"
set test_name               [info script]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connection_info [::ixia::connect                                           \
    -device                 $chassisIp                                         \
    -ixnetwork_tcl_server   localhost                                          \
    -port_list              $portList                                          \
    -ixnetwork_tcl_server   $ixnetwork_tcl_server                              \
    -reset                                                                     ]
    
if {[keylget connection_info status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connection_info log]"
}

set tx_port [lindex $portList 0]
set rx_port [lindex $portList 1]
set tx_handle [keylget connection_info port_handle.$chassisIp.$tx_port]
set rx_handle [keylget connection_info port_handle.$chassisIp.$rx_port]

################################################################################
# Configure interfaces in the test                                             #
# IPv4                                                                         #
################################################################################
set tx_ip "20.0.0.1"
set rx_ip "20.0.0.2"

set tx_interface_config [::ixia::interface_config                              \
    -port_handle        $tx_handle                                             \
    -intf_ip_addr       $tx_ip                                                 \
    -gateway            20.0.0.2                                               \
    -netmask            255.255.255.0                                          \
    -src_mac_addr       0000.0000.0001                                         \
    -intf_mode          ethernet                                               \
    -speed              auto                                                   ]
    
if {[keylget tx_interface_config status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget tx_interface_config log]"
}

set rx_interface_config [::ixia::interface_config                              \
    -port_handle        $rx_handle                                             \
    -intf_ip_addr       $rx_ip                                                 \
    -gateway            20.0.0.1                                               \
    -netmask            255.255.255.0                                          \
    -src_mac_addr       0000.0000.0002                                         \
    -intf_mode          ethernet                                               \
    -speed              auto                                                   ]
    
if {[keylget rx_interface_config status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rx_interface_config log]"
}

set tx_intf_handles [keylget tx_interface_config interface_handle]
set rx_intf_handles [keylget rx_interface_config interface_handle]

# Send arp for the configured interfaces
after 3000
set interface_config [::ixia::interface_config                                 \
    -arp_send_req       {1 1}                                                  \
    -port_handle        $tx_handle $rx_handle                                  ]

if {[keylget interface_config status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_config log]"
}

################################################################################
# Configure traffic in the test                                                #
#                                                                              #
################################################################################

# Configure one traffic item with one egressTracking elements
# which is set to custom by field
set traffic_status [::ixia::traffic_config                                     \
    -mode                       create                                         \
    -traffic_generator          ixnetwork_540                                  \
    -transmit_mode              continuous                                     \
    -name                       "HLTAPI_traffic"                               \
    -src_dest_mesh              fully                                          \
    -route_mesh                 fully                                          \
    -emulation_src_handle       $tx_intf_handles                               \
    -emulation_dst_handle       $rx_intf_handles                               \
    -rate_percent               10                                             \
    -egress_tracking            dscp tos_precedence                            \
    -egress_tracking_encap      ethernet ethernet                              \
    -track_by                   ipv4_source_ip                                 \
    -frame_size_max             512                                            ]
    
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

set stream_id [keylget traffic_status stream_id]

# Get the custom field offsets on which egress tracking can be enabled
set traffic_status [::ixia::traffic_config                                     \
    -mode                       get_available_egress_tracking_field_offset     \
    -stream_id                  $stream_id                                     ]

if {[keylget traffic_status status] == $::FAILURE} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

# Modify the custom field offset on which egress tracking is enabled
set offsets [keylget traffic_status available_egress_tracking_field_offset]
set field_offset [lindex $offsets 2]
set traffic_status [::ixia::traffic_config                                     \
    -mode                           modify                                     \
    -stream_id                      $stream_id                                 \
    -egress_tracking                dscp       custom_by_field                 \
    -egress_custom_field_offset     ethernet   $field_offset                   ]
    
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
