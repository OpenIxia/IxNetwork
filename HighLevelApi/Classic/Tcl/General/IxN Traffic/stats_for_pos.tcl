lappend auto_path {c:\perforce\hltapi\main}
set env(IXIA_VERSION) HLTSET51
package require Ixia


set test_name               [info script]

set chassisIP               10.205.16.32
set port_list               [list 3/1 3/2]

set pgid_mode          outer_vlan_id_6
#set pgid_mode          split            ;# CHOICES custom dscp ipv6TC mplsExp split 
                                                   ;# CHOICES outer_vlan_priority outer_vlan_id_4
                                                   ;# CHOICES outer_vlan_id_6 outer_vlan_id_8
                                                   ;# CHOICES outer_vlan_id_10 outer_vlan_id_12
                                                   ;# CHOICES inner_vlan_priority inner_vlan_id_4
                                                   ;# CHOICES inner_vlan_id_6 inner_vlan_id_8
                                                   ;# CHOICES inner_vlan_id_10 inner_vlan_id_12
                                                   ;# CHOICES tos_precedence ipv6TC_bits_0_2
                                                   ;# CHOICES ipv6TC_bits_0_5
set pgid_encap         "VccMuxBridgedEthernetNoFCS"             ;# CHOICES LLCRoutedCLIP 
                                                   ;# CHOICES LLCPPPoA
                                                   ;# CHOICES LLCBridgedEthernetFCS
                                                   ;# CHOICES LLCBridgedEthernetNoFCS 
                                                   ;# CHOICES VccMuxPPPoA 
                                                   ;# CHOICES VccMuxIPV4Routed 
                                                   ;# CHOICES VccMuxBridgedEthernetFCS
                                                   ;# CHOICES VccMuxBridgedEthernetNoFCS
set pgid_split1_offset 58                         ;# NUMERIC
set pgid_split1_width  2                           ;# RANGE 0-4

set ::ixia::debug      0

################################################################################
proc createLogHere { what } {
    if {[catch {set fid [open c:/Alfa/HLT/split/Logz/${what}.txt w]}]} {
        puts "Couldn't create log file."
        return ""
    }
    puts $fid "***** $what *****"
    return $fid
}
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
# Run for all pgid modes
################################################################################
# set specific_intf_mode_list {
#     pos_hdlc                    "CISCO HDLC"                            \
#     pos_ppp                     "PPP"                                   \
#     frame_relay2427             "Frame Relay"                           \   -> Probleme !!!
#     frame_relay_cisco           "Cisco Frame Relay"                     \   -> Probleme !!!
# }
set specific_intf_mode_list {
    frame_relay2427             "Frame Relay"                           \
}
################################################################################
set pgid_modes_list {                                                       \
    tos_precedence          "IPv4 TOS Precedence (3 bits)"                  \
    dscp                    "IPv4 DSCP (6 bits)"                            \
    ipv6TC                  "IPv6 Traffic Class (8 bits)"                   \
    ipv6TC_bits_0_2         "IPv6 Traffic Class Bits 0-2 (3 bits)"          \
    ipv6TC_bits_0_5         "IPv6 Traffic Class Bits 0-5 (6 bits)"          \
    mplsExp                 "MPLS Exp (3 bits)"                             \
    split                   "Custom"                                        \
}
################################################################################
foreach {current_intf_mode intf_mode_alias} $specific_intf_mode_list {
    puts "===== Running for Interface Mode: $intf_mode_alias"
    after 2000
    foreach {current_pgid_mode mode_alias} $pgid_modes_list {
        set pgid_mode $current_pgid_mode
        puts "***** Running for PGID mode: $mode_alias"
        set logid [createLogHere "${current_intf_mode}-${pgid_mode}"]
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
        set intf_mode            ""
        for {set i 0} {$i < 5} {incr i} {
            lappend port_handle_list     $port_0
            lappend intf_ip_addr_list    20.1.1.[expr 10 + $i]
            lappend gateway_list         20.1.1.[expr 20 + $i]
            lappend netmask_list         255.255.255.0
            lappend autonegotiation_list 1
            lappend speed_list           oc12
            lappend duplex_list          auto
            lappend intf_mode            $current_intf_mode
        }
        for {set i 0} {$i < 5} {incr i} {
            lappend port_handle_list     $port_1
            lappend intf_ip_addr_list    20.1.1.[expr 20 + $i]
            lappend gateway_list         20.1.1.[expr 10 + $i]
            lappend netmask_list         255.255.255.0
            lappend autonegotiation_list 1
            lappend speed_list           oc12
            lappend duplex_list          auto
            lappend intf_mode            $current_intf_mode
        }
        set intf_status [::ixia::interface_config                                   \
                -port_handle        $port_handle_list                               \
                -intf_mode          $intf_mode                                      \
                -intf_ip_addr       $intf_ip_addr_list                              \
                -gateway            $gateway_list                                   \
                -netmask            $netmask_list                                   \
                -autonegotiation    $autonegotiation_list                           \
                -speed              $speed_list                                     \
                -duplex             $duplex_list                                    \
                -clocksource        internal                                        \
                -pgid_mode          $pgid_mode                                      \
                -pgid_split1_offset $pgid_split1_offset                             \
                -pgid_split1_width  $pgid_split1_width                              \
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
        for {set i 0} {$i < 3} {incr i} {
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
                    -qos_type_ixn           tos                                         \
                    -qos_value_ixn          $i                                           \
                    ]
            if {[keylget traffic_status status] != $::SUCCESS} {
                puts "FAIL - $test_name - [keylget traffic_status log]"
                return
            }
        }
        
        after 2000
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
            return
        }
        
        ################################################################################
        # Wait for the traffic to stop 
        ################################################################################
        after 15000
        
        ################################################################################
        # STATISTICS Egress by PORT                                                    #
        ################################################################################
        set flow_traffic_status [::ixia::traffic_stats                              \
                -mode                   egress_by_port                              \
                -traffic_generator      ixnetwork                                   \
                -port_handle            $port_1
                ]
        if {[keylget flow_traffic_status status] != $::SUCCESS} {
            puts "FAIL - $test_name - [keylget flow_traffic_status log]"
            return
        }
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
        
        set flows [keylget flow_traffic_status egress]
        set number_of_flows [llength [keylkeys flows]]
        puts " ----- Flows = $number_of_flows -----"
        puts $logid " ----- Flows = $number_of_flows -----"
        foreach flow [lsort -dictionary [keylkeys flows]] {
            set flow_key [keylget flow_traffic_status egress.$flow]
            puts "\tFlow $flow"
            puts $logid "\tFlow $flow"
            foreach {name key} [subst $[subst flow_results]] {
                puts "\t\t$name: [keylget flow_traffic_status egress.$flow.$key]"
                puts $logid "\t\t$name: [keylget flow_traffic_status egress.$flow.$key]"
            }
        }
        
        after 1000
        ################################################################################
        # STATISTICS Egress by FLOW                                                    #
        ################################################################################
        set flow_traffic_status [::ixia::traffic_stats                              \
                -mode                   egress_by_flow                              \
                -traffic_generator      ixnetwork                                   \
                -port_handle            $port_1
                ]
        if {[keylget flow_traffic_status status] != $::SUCCESS} {
            puts "FAIL - $test_name - [keylget flow_traffic_status log]"
            return
        }
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
        
        set flows [keylget flow_traffic_status egress]
        set number_of_flows [llength [keylkeys flows]]
        puts " ----- Flows = $number_of_flows -----"
        puts $logid " ----- Flows = $number_of_flows -----"
        foreach flow [lsort -dictionary [keylkeys flows]] {
            set flow_key [keylget flow_traffic_status egress.$flow]
            puts "\tFlow $flow"
            puts $logid "\tFlow $flow"
            foreach {name key} [subst $[subst flow_results]] {
                puts "\t\t$name: [keylget flow_traffic_status egress.$flow.$key]"
                puts $logid "\t\t$name: [keylget flow_traffic_status egress.$flow.$key]"
            }
        }
        close $logid
    }
}
puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1

################################################################################