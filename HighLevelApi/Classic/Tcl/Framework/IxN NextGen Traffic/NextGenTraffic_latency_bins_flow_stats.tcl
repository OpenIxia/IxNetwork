################################################################################
# Version 1.0    $Revision: 1 $
# $Author: cnicutar $
#
#    Copyright © 1997 - 2009 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10-19-2009 cnicutar
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
#    Creates one interface on one  port and three interfaces on the other      #
#    port and then runs ip traffic between the two ports (ip_src_mode increment#
#    + latency_bins + track_by src_mac) and collects flow statistics           #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on an STXS4 module.                                 #
#                                                                              #
################################################################################

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

package require Ixia
set test_name [info script]

set chassisIP sylvester
set port_list [list 3/3 3/4]

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

set interface_status1 [::ixia::interface_config \
        -port_handle        $port_0          \
        -intf_ip_addr       172.16.31.1      \
        -gateway            172.16.31.2      \
        -netmask            255.255.255.0    \
        -autonegotiation    1                \
        -op_mode            normal           \
        -vlan               $true            \
        -vlan_id            100              \
        -vlan_user_priority 7                \
        -duplex             auto             \
        -speed              auto             \
        -intf_mode          ethernet         ]
if {[keylget interface_status1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status1 log]"
}
set intf_h0 [keylget interface_status1 interface_handle]

set interface_status2_1 [::ixia::interface_config \
        -port_handle        $port_1          \
        -intf_ip_addr       172.16.31.2      \
        -gateway            172.16.31.1      \
        -netmask            255.255.255.0    \
        -autonegotiation    1                \
        -op_mode            normal           \
        -vlan               $true            \
        -vlan_id            100              \
        -vlan_user_priority 7                \
        -duplex             auto             \
        -speed              auto             \
        -intf_mode          ethernet         ]
if {[keylget interface_status2_1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status2_1 log]"
}

set intf_h1 [keylget interface_status2_1 interface_handle]

set interface_status2_2 [::ixia::interface_config \
        -port_handle        $port_1          \
        -intf_ip_addr       172.16.31.3      \
        -gateway            172.16.31.1      \
        -netmask            255.255.255.0    \
        -autonegotiation    1                \
        -op_mode            normal           \
        -vlan               $true            \
        -vlan_id            100              \
        -vlan_user_priority 7                \
        -duplex             auto             \
        -speed              auto             \
        -intf_mode          ethernet         ]
if {[keylget interface_status2_2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status2_2 log]"
}


set interface_status2_3 [::ixia::interface_config \
        -port_handle        $port_1          \
        -intf_ip_addr       172.16.31.4      \
        -gateway            172.16.31.1      \
        -netmask            255.255.255.0    \
        -autonegotiation    1                \
        -op_mode            normal           \
        -vlan               $true            \
        -vlan_id            100              \
        -vlan_user_priority 7                \
        -duplex             auto             \
        -speed              auto             \
        -intf_mode          ethernet         ]
if {[keylget interface_status2_3 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status2_3 log]"
}

set traffic_status [::ixia::traffic_config \
            -traffic_generator ixnetwork_540   \
            -circuit_endpoint_type ipv4        \
            -mode         create               \
            -emulation_src_handle  $intf_h0    \
            -emulation_dst_handle  $intf_h1    \
            -l3_protocol           ipv4        \
            -ip_src_addr           172.16.31.1 \
            -ip_src_mode           increment   \
            -ip_src_count          3           \
            -ip_src_step           0.0.0.1     \
            -ip_dst_addr           172.16.31.2 \
            -ip_dst_mode           increment   \
            -ip_dst_count          3           \
            -ip_dst_step           0.0.0.1     \
            -convert_to_raw        1           \
            -latency_bins_enable   1           \
            -latency_bins          4           \
            -latency_values        {1.5 3 6.8} \
            -track_by              src_mac\
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

################################################################################
# The traffic must flow!                                                       #
################################################################################

after 10000

################################################################################
# Gather and display traffic statistics                                        #
################################################################################

set flow_traffic_status [::ixia::traffic_stats                        \
        -mode                   flow                                        \
        -traffic_generator      ixnetwork_540                               \
        ]

if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return 0
}

################################################################################
# Stop the traffic                                                             #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork_540                               \
]

################################################################################
# Wait for the traffic to stop                                                 #
################################################################################

after 10000

if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

show_stats $flow_traffic_status

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1