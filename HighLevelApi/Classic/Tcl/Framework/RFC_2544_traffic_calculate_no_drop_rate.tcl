################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Enache Adrian $
#
#    Copyright © 1997 - 2011 by IXIA
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
#    This sample configures 2 back to back ports and a traffic item between    #
#    them. Then runs the NDR procedure to get the real available bandwidth.    #
#    Note: running this test b2b, most of the times it will reach 100% NDR     #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10/100/1000 STX4-256MB module.                 #
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

set env(IXIA_VERSION) HLTSET105
package require Ixia

#set ixia::debug 3
set test_name [info script]

set chassisIP sylvester
set port_list {2/3 2/4}

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                          \
        -device    $chassisIP           \
        -port_list $port_list           \
        -username  ixiaApiUser          \
        -ixnetwork_tcl_server localhost \
        -tcl_server $chassisIP          ]
        
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle1 [keylget connect_status port_handle.$chassisIP.[lindex $port_list 0]]
set port_handle2 [keylget connect_status port_handle.$chassisIP.[lindex $port_list 1]]

########################################
# Configure interfaces in the test     #
########################################
set interface_status [::ixia::interface_config \
        -mode config                         \
        -port_handle     $port_handle1       \
        -autonegotiation 1                   \
        -duplex          full                \
        -speed           ether100            \
        -vlan 0                              \
        -l23_config_type protocol_interface  \
        -gateway 8.0.0.2                     \
        -intf_ip_addr 8.0.0.1                \
        -netmask 255.255.255.0               \
        -arp_on_linkup 1                     \
        -ns_on_linkup 1                      \
        -single_ns_per_gateway 1             \
        -single_arp_per_gateway 1            ]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set interface_status [::ixia::interface_config \
        -mode config                         \
        -port_handle     $port_handle2       \
        -autonegotiation 1                   \
        -duplex          full                \
        -speed           ether100            \
        -vlan 0                              \
        -l23_config_type protocol_interface  \
        -gateway 8.0.0.1                     \
        -intf_ip_addr 8.0.0.2                \
        -netmask 255.255.255.0               \
        -arp_on_linkup 1                     \
        -ns_on_linkup 1                      \
        -single_ns_per_gateway 1             \
        -single_arp_per_gateway 1            ]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}


########################################
# Configure the traffic item needed    #
########################################

set ret [::ixia::traffic_config  \
    -mode create                                                        \
    -traffic_generator ixnetwork_540                                    \
    -endpointset_count 1                                                \
    -emulation_src_handle [list [list ::ixNet::OBJ-/vport:1/protocols]] \
    -emulation_dst_handle [list [list ::ixNet::OBJ-/vport:2/protocols]] \
    -global_dest_mac_retry_count 1                                      \
    -global_dest_mac_retry_delay 5                                      \
    -enable_data_integrity 1                                            \
    -frame_sequencing disable                                           \
    -frame_sequencing_mode rx_threshold                                 \
    -src_dest_mesh one_to_one                                           \
    -route_mesh fully                                                   \
    -bidirectional 0                                                    \
    -allow_self_destined 0                                              \
    -enable_dynamic_mpls_labels 0                                       \
    -hosts_per_net 1                                                    \
    -name Traffic_Item_1                                                \
    -source_filter all                                                  \
    -destination_filter all                                             \
    -circuit_endpoint_type ipv4                                         \
    -egress_tracking none                                               \
    -track_by {traffic_item endpoint_pair}                              ]

if {[keylget ret status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
    
set stream_id [keylget ret stream_id]

########################################
# Run the NDR procedure                #
########################################

set ret [ixia::get_nodrop_rate \
    -stream_id $stream_id         \
    -max_rate 80000               \
    -tx_port_handle $port_handle1 \
    -rx_port_handle $port_handle2 \
    -stream_mode even             ]
    
puts "Results from NDR..."

show_stats $ret

puts "SUCCESS - [info script] - [clock format [clock seconds]]"
return 1

