################################################################################
# Version 1.0    $Revision: 1 $
# Author: Radu Antonescu
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-03-2007 RAntonescu - created sample
#    10-17-2007 LRaicea    - corected indentation and validated returned keys
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
#    This sample creates two IPv4 streams on a port.                           #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 2.5G MSM POS/SPR/RPR module.                   #
#    The sample was tested with HLTSET26.                                      #
#                                                                              #
################################################################################

package require Ixia
set test_name [info script]

set chassisIP sylvester
set port_list [list 1/1 2/1]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username  ixiaApiUser      ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle_list [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
            temp_port]} {
        lappend port_handle_list $temp_port
    }
}

set port_0 [lindex $port_handle_list 0]
set port_1 [lindex $port_handle_list 1]

################################################################################
# Configure interface in the test
################################################################################
set interface_status [::ixia::interface_config                        \
        -port_handle     [list $port_0              $port_1        ]  \
        -intf_mode       [list frame_relay2427      frame_relay2427]  \
        -speed           [list oc48                 oc48           ]  \
        -phy_mode        [list fiber                fiber          ]  \
        -rx_scrambling   [list 0                    0              ]  \
        -tx_scrambling   [list 0                    0              ]  \
        -data_integrity  [list 0                    0              ]  \
        -transmit_mode   [list advanced             advanced       ]  \
        -intf_ip_addr    [list 12.1.3.2             12.1.3.1       ]  \
        -gateway         [list 12.1.3.1             12.1.3.2       ]  \
        -netmask         [list 255.255.255.0        255.255.255.0  ]  \
        -autonegotiation [list 0                    0              ]  \
        -src_mac_addr    [list 0000.0005.0001       0000.0001.0002 ]  ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
################################################################################
# Delete all the streams first
################################################################################
set traffic_status [::ixia::traffic_config \
        -mode        reset                 \
        -port_handle $port_0          ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}
################################################################################
# Configure stream
################################################################################
set traffic_status [::ixia::traffic_config       \
        -mode               create               \
        -port_handle        $port_0              \
        -l3_protocol        ipv4                 \
        -ip_src_addr        12.1.1.1             \
        -ip_dst_addr        12.1.1.2             \
        -rate_percent       50                   \
        -length_mode        fixed                \
        -frame_size         128                  \
        -l2_encap           ietf_framerelay      \
        -enable_time_stamp  0                    \
        -dlci_value         750                  \
        -dlci_count_mode    increment            \
        -dlci_repeat_count  10                   \
        -fecn               1                    \
        -discard_eligible   1                    \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}
################################################################################
# Clear stats 
################################################################################
set stat_control [::ixia::traffic_control   \
        -port_handle        $port_1         \
        -action             clear_stats     ]
if {[keylget stat_control status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stat_control log]"
    return
}
################################################################################
# Start traffic
################################################################################
set traffic_control [::ixia::traffic_control \
        -port_handle        $port_0          \
        -action             run              ]
if {[keylget traffic_control status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_control log]"
    return
}

after 5000
################################################################################
# Stop traffic
################################################################################
set traffic_control [::ixia::traffic_control \
        -port_handle        $port_0          \
        -action             stop             ]
if {[keylget traffic_control status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_control log]"
    return
}
################################################################################
# Retrive statistics
################################################################################
set stat_status [::ixia::traffic_stats \
        -port_handle        $port_1    \
        -mode               aggregate  ]
if {[keylget stat_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stat_status log]"
    return
}
puts "Packets received: [keylget stat_status $port_1.aggregate.rx.pkt_count]"

return "SUCCESS - $test_name - [clock format [clock seconds]]"
