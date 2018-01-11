################################################################################
# Version 1.0    $Revision: 1 $
# $Author: L. Raicea $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    06-06-2008 L. Raicea - Created sample
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
#    This sample creates a back-to-back setup using two Ixia ports.            #
#    It configures several IPv4 Ethernet interfaces on each port and generates #
#    traffic between them.                                                     #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a STXS4 module.                                  #
#                                                                              #
################################################################################
package require Ixia


set test_name               [info script]

set chassisIP               sylvester
set port_list               [list 2/1 2/2]

################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                         \
        -reset                                                              \
        -ixnetwork_tcl_server   localhost                                   \
        -device                 $chassisIP                                  \
        -port_list              $port_list                                  \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}
set port_0 [lindex $port_handle 0]
set port_1 [lindex $port_handle 1]
################################################################################
# Configure interfaces
################################################################################
set port_count           [llength $port_list]
set port_handle_list     ""
set intf_ip_addr_list    ""
set gateway_list         ""
set netmask_list         ""
set autonegotiation_list ""
set speed_list           ""
set duplex_list          ""
for {set i 0} {$i < 5} {incr i} {
    lappend port_handle_list     $port_0
    lappend intf_ip_addr_list    20.1.1.[expr 10 + $i]
    lappend gateway_list         20.1.1.[expr 20 + $i]
    lappend netmask_list         255.255.255.0
    lappend autonegotiation_list 1
    lappend speed_list           auto
    lappend duplex_list          auto
}
for {set i 0} {$i < 5} {incr i} {
    lappend port_handle_list     $port_1
    lappend intf_ip_addr_list    20.1.1.[expr 20 + $i]
    lappend gateway_list         20.1.1.[expr 10 + $i]
    lappend netmask_list         255.255.255.0
    lappend autonegotiation_list 1
    lappend speed_list           auto
    lappend duplex_list          auto
}
set intf_status [::ixia::interface_config                                   \
        -port_handle        $port_handle_list                               \
        -intf_ip_addr       $intf_ip_addr_list                              \
        -gateway            $gateway_list                                   \
        -netmask            $netmask_list                                   \
        -autonegotiation    $autonegotiation_list                           \
        -speed              $speed_list                                     \
        -duplex             $duplex_list                                    \
        ]
if {[keylget intf_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget intf_status log]"
    return
}
set interface_handles [keylget intf_status interface_handle]

################################################################################
# Delete all the streams first
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action             reset                                           \
        -traffic_generator  ixnetwork                                       \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

################################################################################
# Create traffic items
################################################################################
set traffic_status [::ixia::traffic_config                                  \
        -mode                   create                                      \
        -traffic_generator      ixnetwork                                   \
        -transmit_mode          continuous                                  \
        -name                   "IPv4_Traffic"                              \
        -src_dest_mesh          fully                                       \
        -route_mesh             fully                                       \
        -circuit_type           none                                        \
        -circuit_endpoint_type  ipv4                                        \
        -emulation_src_handle   [lrange $interface_handles 0 4]             \
        -emulation_dst_handle   [lrange $interface_handles 5 end]           \
        -track_by               endpoint_pair                               \
        -stream_packing         one_stream_per_endpoint_pair                \
        -rate_percent           5                                           \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

################################################################################
# Start the traffic 
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

################################################################################
# Wait for the traffic to be transmitted
################################################################################
after 5000

################################################################################
# Stop the traffic 
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

################################################################################
# Wait for the traffic to stop 
################################################################################
after 15000

################################################################################
# Gather and display per port per flow traffic statistics 
################################################################################
set flow_traffic_status [::ixia::traffic_stats                              \
        -mode                   flow                                        \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return
}
set flow_results [list                                                      \
        "Tx Port"                       tx.port                             \
        "Rx Port"                       rx.port                             \
        "Tx Frames"                     tx.total_pkts                       \
        "Tx Frame Rate"                 tx.total_pkt_rate                   \
        "Rx Frames"                     rx.total_pkts                       \
        "Frames Delta"                  rx.loss_pkts                        \
        "Rx Frame Rate"                 rx.total_pkt_rate                   \
        "Loss %"                        rx.loss_percent                     \
        "Rx Bytes"                      rx.total_pkts_bytes                 \
        "Rx Rate (Bps)"                 rx.total_pkt_byte_rate              \
        "Rx Rate (bps)"                 rx.total_pkt_bit_rate               \
        "Rx Rate (Kbps)"                rx.total_pkt_kbit_rate              \
        "Rx Rate (Mbps)"                rx.total_pkt_mbit_rate              \
        "Avg Latency (ns)"              rx.avg_delay                        \
        "Min Latency (ns)"              rx.min_delay                        \
        "Max Latency (ns)"              rx.max_delay                        \
        "First Timestamp"               rx.first_tstamp                     \
        "Last Timestamp"                rx.last_tstamp                      \
        ]

set flows [keylget flow_traffic_status flow]
foreach flow [keylkeys flows] {
    set flow_key [keylget flow_traffic_status flow.$flow]
    puts "\tFlow $flow"
    foreach {name key} [subst $[subst flow_results]] {
        puts "\t\t$name: [keylget flow_traffic_status flow.$flow.$key]"
    }
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return
