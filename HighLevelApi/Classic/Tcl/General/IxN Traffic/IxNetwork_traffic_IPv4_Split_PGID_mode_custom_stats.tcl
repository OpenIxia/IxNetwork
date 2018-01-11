################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2009 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-08-2007 LRaicea - created sample
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
#    This sample creates IPv4 interfaces and traffic between them with         #
#    different TOS values. The tracking is done both on source-destination     #
#    pair and on TOS. Egress stats are retrieved by port and by flow.          #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET51.                                      #
#                                                                              #
################################################################################
set env(IXIA_VERSION) HLTSET51

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

set debug_file [info script]_[clock seconds].log
if {[info commands ::realIxNet] == [list]} {
    rename ixNet realIxNet
}

proc ::ixNet args {
    global debug_file
    set fid [open $debug_file "a+"]
    puts $fid "ixNet $args"
    close $fid
    set retval [uplevel 1 ::realIxNet $args]
    return $retval
}


################################################################################
# General script variables
################################################################################
set test_name                                   [info script]


################################################################################
# Connect to the chassis
################################################################################
puts "Start connecting to chassis ..."
update idletasks

set chassis_ip              10.205.17.50
set port_list               [list 2/1 2/2]

# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                        \
        -reset                                                             \
        -ixnetwork_tcl_server localhost                                    \
        -device               $chassis_ip                                  \
        -port_list            $port_list                                   \
        -break_locks          1                                            \
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
puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port
    
    # Initialize per port variables
    set interface_handles_$port ""
    
    incr i
}

puts "End connecting to chassis ..."
update idletasks

################################################################################
# Run for PGID mode split
################################################################################
proc createLogHere { what } {
    set log_path [file dirname [info script]]
    if {[catch {set fid [open "${log_path}/${what}.txt" w]}]} {
        puts "Couldn't create log file."
        return ""
    }
    puts $fid "***** $what *****"
    return $fid
}

set pgid_split1_offset   15
set pgid_split1_width    3
set pgid_mode            split
set logid [createLogHere $pgid_mode]
set num_interfaces       4
set num_tos_values       4
################################################################################
# Configure interfaces
################################################################################
puts "Started configuration of L1-L3 interfaces ..."
update idletasks
set port_count           [llength $port_list]
set port_handle_list     ""
set intf_ip_addr_list    ""
set gateway_list         ""
set netmask_list         ""
set autonegotiation_list ""
set speed_list           ""
set duplex_list          ""
for {set i 0} {$i < $num_interfaces} {incr i} {
    lappend port_handle_list     $port_0
    lappend intf_ip_addr_list    20.1.1.[expr 1   + $i]
    lappend gateway_list         20.1.1.[expr 100 + $i]
    lappend netmask_list         255.255.255.0
    lappend autonegotiation_list 1
    lappend speed_list           auto
    lappend duplex_list          auto
}
for {set i 0} {$i < $num_interfaces} {incr i} {
    lappend port_handle_list     $port_1
    lappend intf_ip_addr_list    20.1.1.[expr 100 + $i]
    lappend gateway_list         20.1.1.[expr 1   + $i]
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
        -pgid_mode          $pgid_mode                                      \
        -pgid_split1_offset $pgid_split1_offset                             \
        -pgid_split1_width  $pgid_split1_width                              \
        ]
if {[keylget intf_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget intf_status log]"
    return 0
}
set interface_handles [keylget intf_status interface_handle]
puts "Finished configuration of L1-L3 interfaces ..."
update idletasks
################################################################################
# Delete all the streams first
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action             reset                                           \
        -traffic_generator  ixnetwork                                       \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

################################################################################
# Create traffic items
################################################################################
puts "Started configuration of traffic items ..."
update idletasks
for {set i 0} {$i < $num_tos_values} {incr i} {
    set traffic_status [::ixia::traffic_config                                  \
            -mode                   create                                      \
            -traffic_generator      ixnetwork                                   \
            -transmit_mode          continuous                                  \
            -name                   "IPv4_Traffic"                              \
            -src_dest_mesh          fully                                       \
            -route_mesh             fully                                       \
            -circuit_type           none                                        \
            -circuit_endpoint_type  ipv4                                        \
            -emulation_src_handle   [lrange $interface_handles 0 [expr $num_interfaces - 1]] \
            -emulation_dst_handle   [lrange $interface_handles $num_interfaces end]          \
            -track_by               endpoint_pair                               \
            -stream_packing         optimal_packing                             \
            -rate_percent           5                                           \
            -qos_type_ixn           tos                                         \
            -qos_value_ixn          $i                                          \
            ]
    if {[keylget traffic_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget traffic_status log]"
        return 0
    }
}
puts "Finished configuration of traffic items ..."
update idletasks
after 2000

################################################################################
# Start the traffic 
################################################################################
puts "Started traffic ..."
update idletasks
set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

################################################################################
# Wait for the traffic to be transmitted
################################################################################
after 7790

################################################################################
# Stop the traffic 
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

puts "Stopped traffic ..."
update idletasks
################################################################################
# Wait for the traffic to stop 
################################################################################
after 15000
################################################################################
# STATISTICS Egress by PORT                                                    #
################################################################################
puts "Started retrieving stats per port ..."
update idletasks
set flow_traffic_status [::ixia::traffic_stats                              \
        -mode                   egress_by_port                              \
        -traffic_generator      ixnetwork                                   \
        -port_handle            $port_1
        ]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return 0
}
puts "Finished retrieving stats per flow ..."
update idletasks

set flow_results [list                                                  \
            "Rx Frames"                     rx.total_pkts               \
            "Rx Frame Rate"                 rx.total_pkt_rate           \
            "Rx Bytes"                      rx.total_pkts_bytes         \
            "Rx Rate (Bps)"                 rx.total_pkt_byte_rate      \
            "Rx Rate (bps)"                 rx.total_pkt_bit_rate       \
            "Rx Rate (Kbps)"                rx.total_pkt_kbit_rate      \
            "Rx Rate (Mbps)"                rx.total_pkt_mbit_rate      \
            "Cut-Through Avg Latency (ns)"  rx.avg_delay                \
            "Cut-Through Min Latency (ns)"  rx.min_delay                \
            "Cut-Through Max Latency (ns)"  rx.max_delay                \
            "First TimeStamp"               rx.first_tstamp             \
            "Last TimeStamp"                rx.last_tstamp              \
        ]


puts " ----- EGRESS BY PORT -----"
puts $logid " ----- EGRESS BY PORT -----"
set flow 1
while {![catch {set flow_key [keylget flow_traffic_status egress.$flow]}]} {
    puts "\tFlow $flow - [keylget flow_traffic_status egress.$flow.flow_name]"
    puts $logid "\tFlow $flow - [keylget flow_traffic_status egress.$flow.flow_name]"
    foreach {name key} [subst $[subst flow_results]] {
        puts "\t\t$name: [keylget flow_traffic_status egress.$flow.$key]"
        puts $logid "\t\t$name: [keylget flow_traffic_status egress.$flow.$key]"
    }
    incr flow
}

puts " ----- Flows = [expr $flow - 1] -----"
puts $logid " ----- Flows = [expr $flow - 1] -----"

after 10000
#after 1000
################################################################################
# STATISTICS Egress by FLOW                                                    #
################################################################################
puts "Started retrieving stats per flow ..."
update idletasks
set flow_traffic_status [::ixia::traffic_stats                              \
        -mode                   egress_by_flow                              \
        -traffic_generator      ixnetwork                                   \
        -port_handle            $port_1
        ]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return 0
}
puts "Finished retrieving stats per flow ..."
update idletasks
set flow_results [list                                                  \
            "Rx Frames"                     rx.total_pkts               \
            "Rx Frame Rate"                 rx.total_pkt_rate           \
            "Rx Bytes"                      rx.total_pkts_bytes         \
            "Rx Rate (Bps)"                 rx.total_pkt_byte_rate      \
            "Rx Rate (bps)"                 rx.total_pkt_bit_rate       \
            "Rx Rate (Kbps)"                rx.total_pkt_kbit_rate      \
            "Rx Rate (Mbps)"                rx.total_pkt_mbit_rate      \
            "Cut-Through Avg Latency (ns)"  rx.avg_delay                \
            "Cut-Through Min Latency (ns)"  rx.min_delay                \
            "Cut-Through Max Latency (ns)"  rx.max_delay                \
            "First TimeStamp"               rx.first_tstamp             \
            "Last TimeStamp"                rx.last_tstamp              \
        ]
puts " ----- EGRESS BY FLOW -----"
puts $logid " ----- EGRESS BY FLOW -----"
set flow 1
while {![catch {set flow_key [keylget flow_traffic_status egress.$flow]}]} {
    puts "\tFlow $flow - [keylget flow_traffic_status egress.$flow.flow_name] - [keylget flow_traffic_status egress.$flow.flow_print]"
    puts $logid "\tFlow $flow - [keylget flow_traffic_status egress.$flow.flow_name] - [keylget flow_traffic_status egress.$flow.flow_print]"
    foreach {name key} [subst $[subst flow_results]] {
        puts "\t\t$name: [keylget flow_traffic_status egress.$flow.$key]"
        puts $logid "\t\t$name: [keylget flow_traffic_status egress.$flow.$key]"
    }
    incr flow
}

puts " ----- Flows = [expr $flow - 1] -----"
puts $logid " ----- Flows = [expr $flow - 1] -----"

close $logid
puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
