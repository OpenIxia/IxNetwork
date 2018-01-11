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
#    This sample creates one traffic item, modifies the frame ordering to the   #
# following values : flow_group_setup, rfc2889, peak_loading, and runs traffic #
#                                                                              #
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
# Create interfaces                                      #
##########################################################
puts "Creating interfaces"
set intf_status [::ixia::interface_config                                                               \
        -port_handle        [list $port_0 $port_2 $port_1 $port_3]                                      \
        -intf_ip_addr       [list 172.16.0.1 172.16.0.3 172.16.0.2 172.16.0.4]                          \
        -gateway            [list 172.16.0.2 172.16.0.4 172.16.0.1 172.16.0.3]                          \
        -netmask            [list 255.255.255.0 255.255.255.0 255.255.255.0 255.255.255.0]              \
        -src_mac_addr       [list 0000.00f5.0001  0000.0012.0002 0000.0012.0003 0000.0012.0004]         \
        -autonegotiation    1                                                                           \
        -speed              ether1000                                                                   \
]
if {[keylget intf_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget intf_status log]"
    return 0
}

set interface_handles [keylget intf_status interface_handle]

#####################################################
# Create traffic item                               #
#####################################################
puts "Creating traffic item"
set traffic_status [::ixia::traffic_config                              \
    -mode                   create                                      \
    -traffic_generator      ixnetwork                                   \
    -emulation_src_handle   [lrange $interface_handles 0 1]             \
    -emulation_dst_handle   [lrange $interface_handles 2 3]             \
    -track_by               endpoint_pair                               \
    -src_dest_mesh          fully                                       \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

set traffic_item_handle [keylget traffic_status traffic_item]
set stream_id [keylget traffic_status stream_id]


#####################################################
# Setting Frame Ordering to Flow Group Setup        #
#####################################################
puts "Modifying frame ordering to flow_group_setup"
set traffic_status [::ixia::traffic_config          \
    -mode                   modify                  \
    -stream_id              $stream_id              \
    -global_frame_ordering  flow_group_setup        \

]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

#####################################################
# Setting Frame Ordering to Peak Loading            #
#####################################################

puts "Modifying frame ordering to peak_loading"
set traffic_status [::ixia::traffic_config          \
    -mode                   modify                  \
    -stream_id              $stream_id              \
    -global_frame_ordering  peak_loading            \

]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

#####################################################
# Setting Frame Ordering to RFC2889                 #
#####################################################
puts "Modifying frame ordering to rfc2889"
set traffic_status [::ixia::traffic_config          \
    -mode                   modify                  \
    -stream_id              $stream_id              \
    -global_frame_ordering  rfc2889                 \

]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}


puts "Starting traffic"
set traffic_status [::ixia::traffic_control     \
    -action             run                     \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

after 20000

puts "Stopping traffic"
set traffic_status [::ixia::traffic_control     \
    -action             stop                    \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}


return 1