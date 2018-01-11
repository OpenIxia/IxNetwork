################################################################################
# Version 1.0    $Revision: 1 $
# $Author: cnicutar $
#
#    Copyright © 1997 - 2009 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#
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
#    This sample creates BGP peers and routes, and sends traffic over it       #
#    using ixnetwork_540 traffic_generator and tracking by qos.                #
#                                                                              #
#    It uses two Ixia ports. BGP peers and routes are configured on both       #
#    ports.  Streams are generated using ixnetwork_540 traffic_generator       #
#    Traffic statistics are collected for each flow.                           #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 2/3 2/4]

########
# IpV4 #
########
set ipV4_autoneg_list  "1                    1"
set ipV4_duplex_list   "auto                 auto"
set ipV4_speed_list    "auto                 auto"
set ipV4_ixia_list     "172.16.32.1          172.16.32.2"
set ipV4_gateway_list  "172.16.32.2          172.16.32.1"
set ipV4_netmask_list  "255.255.255.0        255.255.255.0"
set ipV6_intf_addr     "2001::1              2001::2"
set ipv6_prefix_length "64                   64"


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


set port_array [keylget connect_status port_handle.$chassisIP]

set port_0 [keylget port_array [lindex $port_list 0]]
set port_1 [keylget port_array [lindex $port_list 1]]

set port_handle [list $port_0 $port_1]

set interface_status [::ixia::interface_config \
        -port_handle        $port_handle        \
        -autonegotiation    $ipV4_autoneg_list  \
        -duplex             $ipV4_duplex_list   \
        -speed              $ipV4_speed_list    \
        -intf_ip_addr       $ipV4_ixia_list     \
        -gateway            $ipV4_gateway_list  \
        -netmask            $ipV4_netmask_list  \
        -ipv6_intf_addr     $ipV6_intf_addr     \
        -ipv6_prefix_length $ipv6_prefix_length \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set interface_handles [keylget interface_status interface_handle]

set traffic_status  [::ixia::traffic_config                             \
        -traffic_generator              ixnetwork_540                   \
        -mode                           create                          \
        -circuit_endpoint_type          ipv4                            \
        -emulation_src_handle           [lindex $interface_handles 0]   \
        -emulation_dst_handle           [lindex $interface_handles 1]   \
        -length_mode                    imix                            \
        -frame_size_imix                "1:150 1:200 1:256 1:512"         \
        -ipv6_src_addr                  2001::1                         \
        -ipv6_dst_addr                  2001::2                         \
        -track_by                       traffic_item                    \
    ]

if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}


set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

after 10000


################################################################################
# Stop the traffic                                                             #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork_540                               \
]

if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

set traffic_status [::ixia::traffic_stats    \
        -mode                   traffic_item             \
        -traffic_generator      ixnetwork_540            \
]

if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

set traffic_items [keylget traffic_status traffic_item]
set traffic_items [keylkeys traffic_items]

foreach traffic_item $traffic_items {
    puts "***** Traffic item: $traffic_item"
    puts [format "%20s %s" "Total packets: "\
    [keylget traffic_status traffic_item.$traffic_item.rx.total_pkts]]    
    puts [format "%20s %s" "Lost packets: "\
    [keylget traffic_status traffic_item.$traffic_item.rx.loss_pkts]]
    puts [format "%20s %s" "Total packet bytes: "\
    [keylget traffic_status traffic_item.$traffic_item.rx.total_pkt_bytes]]
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1