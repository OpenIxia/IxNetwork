################################################################################
# Version 1.0
# $Author: Laura - Adriana Savu$
#
#    Copyright © 1997 - 2014 by IXIA
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
#   This sample create one l23 Traffic Item and one l47 traffic Item.          #
#   It regenerates, applies,starts, and stops traffic                          #
################################################################################


###############################################################################
# Package require Ixia
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
#  chassis, card, port configuration                                           #
################################################################################
set chassis_ip              10.215.180.121
set port_list               [list 2/1 2/2 2/3 2/4]
set break_locks             1
set tcl_server              10.215.180.121
set ixnetwork_tcl_server    localhost
set test_name               [info script]

###############################################################################################
# START - Connect to the chassis                                                              #
# Connect to the IxNetwork Tcl Server & chassis, reset to factory defaults and take ownership #
###############################################################################################
puts "Connecting to chassis"
set connect_status [::ixia::connect                                        \
        -reset                                                             \
        -device               $chassis_ip                                  \
        -port_list            $port_list                                   \
        -break_locks          $break_locks                                 \
        -ixnetwork_tcl_server $ixnetwork_tcl_server                        \
]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}
set i 0
foreach port $port_handle {
    set port_$i $port
    puts $port 
    incr i
}

##########################################################
# Create topologies, device groups and interfaces        #
##########################################################
puts "Creating topologies"
set topology_status [::ixiangpf::topology_config                        \
    -port_handle                [list $port_handle1]                    \
    -device_group_multiplier    10                                      \
    ]
if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}
set topology_handle1 [keylget topology_status topology_handle]
set device_group_handle1 [keylget topology_status device_group_handle]

set topology_status [::ixiangpf::topology_config                        \
    -port_handle                [list $port_handle2]                    \
    -device_group_multiplier    10                                      \
    ]
if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}
set topology_handle2 [keylget topology_status topology_handle]
set device_group_handle2 [keylget topology_status device_group_handle]

set topology_status [::ixiangpf::topology_config                        \
    -port_handle                [list $port_handle3]                    \
    -device_group_multiplier    1                                       \
    ]
if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}
set topology_handle3 [keylget topology_status topology_handle]
set device_group_handle3 [keylget topology_status device_group_handle]

set topology_status [::ixiangpf::topology_config                        \
    -port_handle                [list $port_handle4]                    \
    -device_group_multiplier    1                                       \
    ]
if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}
set topology_handle4 [keylget topology_status topology_handle]
set device_group_handle4 [keylget topology_status device_group_handle]

puts "Creating interfaces"
set interface_status [::ixiangpf::interface_config           \
    -protocol_handle              $device_group_handle1      \
    -src_mac_addr                 00.dd.cc.bb.00.01          \
    -src_mac_addr_step            00.00.00.00.00.01          \
    -gateway                      120.120.1.2                \
    -gateway_step                 0.0.1.0                    \
    -intf_ip_addr                 120.120.1.1                \
    -intf_ip_addr_step            0.0.1.0                    \
]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}
set ethernet_handle1 [keylget interface_status ethernet_handle]
set ip_handle1 [keylget interface_status ipv4_handle]

set interface_status [::ixiangpf::interface_config           \
    -protocol_handle              $device_group_handle2      \
    -src_mac_addr                 00.dd.cc.aa.00.01          \
    -src_mac_addr_step            00.00.00.00.00.01          \
    -gateway                      120.120.1.1                \
    -gateway_step                 0.0.1.0                    \
    -intf_ip_addr                 120.120.1.2                \
    -intf_ip_addr_step            0.0.1.0                    \
]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}
set ethernet_handle2 [keylget interface_status ethernet_handle]
set ip_handle2 [keylget interface_status ipv4_handle]

set interface_status [::ixiangpf::interface_config           \
    -protocol_handle              $device_group_handle3      \
    -src_mac_addr                 00.dd.bb.aa.00.01          \
    -src_mac_addr_step            00.00.00.00.00.01          \
    -gateway                      130.130.1.2                \
    -gateway_step                 0.0.1.0                    \
    -intf_ip_addr                 130.130.1.1                \
    -intf_ip_addr_step            0.0.1.0                    \
]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}
set ethernet_handle3 [keylget interface_status ethernet_handle]
set ip_handle3 [keylget interface_status ipv4_handle]

set interface_status [::ixiangpf::interface_config           \
    -protocol_handle              $device_group_handle4      \
    -src_mac_addr                 00.dd.bb.bb.00.01          \
    -src_mac_addr_step            00.00.00.00.00.01          \
    -gateway                      130.130.1.1                \
    -gateway_step                 0.0.1.0                    \
    -intf_ip_addr                 130.130.1.2                \
    -intf_ip_addr_step            0.0.1.0                    \
]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}
set ethernet_handle4 [keylget interface_status ethernet_handle]
set ip_handle4 [keylget interface_status ipv4_handle]

puts "Starting all protocols"
set start_status [::ixiangpf::test_control  \
    -action         start_all_protocols     \
    ]
if {[keylget start_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget start_status log]"
    return 0
}
after 5000
update idletasks

#####################################################
# Create l23 traffic item                           #
#####################################################
puts "Creating l23 traffic item"
set traffic_status [::ixia::traffic_config                                  \
    -mode                   create                                          \
    -traffic_generator      ixnetwork                                       \
    -emulation_src_handle   $ip_handle1                                     \
    -emulation_dst_handle   $ip_handle2                                     \
    -circuit_endpoint_type  ipv4                                            \
    -track_by               [list dest_ip  source_ip]                       \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}
set traffic_l23_handle [keylget traffic_status traffic_item]

#####################################################
# Create l47 traffic item                           #
#####################################################
puts "Creating l47 traffic item"
set flows {Amazon_EC2_Create_Key_Pair_Flow AOL_Instant_Messenger AOL_Webmail AppleJuice AppLine_Demo_Superflow}
set traffic_status [::ixiangpf::traffic_l47_config          \
    -mode                       create                      \
    -emulation_src_handle       [list $ip_handle3]          \
    -emulation_dst_handle       [list $ip_handle4]          \
    -circuit_endpoint_type      ipv4_application_traffic    \
    -flows                      $flows                      \
    -enable_per_ip_stats        1                           \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}
set traffic_l47_handle [keylget traffic_status traffic_l47_handle]
set applib_handle [keylget traffic_status $traffic_l47_handle.applib_profile]

#####################################################
# Regenerate l23 traffic item                       #
#####################################################
puts "Regenerating l23 traffic item"
set traffic_status [::ixia::traffic_control  \
    -handle         $traffic_l23_handle      \
    -action         regenerate               \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

#####################################################
# Apply l23 traffic item                            #
#####################################################
puts "Applying l23 traffic"
set traffic_status [::ixia::traffic_control  \
    -action         apply                    \
    -type           l23                      \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

#####################################################
# Start l23 traffic item                            #
#####################################################
puts "Starting l23 traffic"
set traffic_status [::ixia::traffic_control  \
    -action         run                      \
    -type           l23                      \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}
after 7000
update idletasks

#####################################################
# Stop l23 traffic item                             #
#####################################################
puts "Stopping l23 traffic"
set traffic_status [::ixia::traffic_control  \
    -action         stop                     \
    -type           l23                      \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}
after 7000
update idletasks

#####################################################
# Apply l47 traffic item                            #
#####################################################
puts "Applying l47 traffic"
set traffic_status [::ixia::traffic_control  \
    -action         apply                    \
    -type           l47                      \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

#####################################################
# Start l47 traffic item                            #
#####################################################
puts "Starting l47 traffic"
set traffic_status [::ixia::traffic_control  \
    -action         run                    \
    -type           l47                      \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}
after 7000
update idletasks

#####################################################
# Stop l47 traffic item                             #
#####################################################
puts "Stopping l47 traffic"
set traffic_status [::ixia::traffic_control  \
    -action         stop                     \
    -type           l47                      \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}
after 7000
update idletasks

return 1