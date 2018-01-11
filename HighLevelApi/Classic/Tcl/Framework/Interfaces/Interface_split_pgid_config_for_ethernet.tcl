
#source {D:\TC_AUTOMATION\TC_Regression_Setup.tcl}
# source "C:\\Program Files\\Ixia\\hltapi\\$::cfg::hltapi_version\\TclScripts\\bin\\hlt_init.tcl"

lappend auto_path {c:\perforce\hltapi\main}
namespace eval cfg {}
set ::cfg::chassis_index 4
set ::cfg::card_type     stxs4
set ::cfg::setup_type    b2b                       ;# CHOICES b2b dut
set ::cfg::num_ports     2
set ::cfg::l1_intf_mode  ethernet                  ;# CHOICES atm 
                                                   ;# CHOICES ethernet (for 10/100/1000 Ethernet cards and 10GE cards)
                                                   ;# CHOICES pos_hdlc pos_ppp frame_relay1490 frame_relay2427 frame_relay_cisco srp srp_cisco rpr gfp (for POS cards)

set ::cfg::l1_speed      auto                      ;# CHOICES ether10 ether100 ether1000 auto DEFAULT ether100 (for 10/100/1000 Ethernet cards)
                                                   ;# CHOICES ether10000lan ether10000wan (for 10GE cards)
                                                   ;# CHOICES oc3 oc12 oc48 oc192 DEFAULT oc12 (for ATM and POS cards)
set ::ixia::debug 0

set env(IXIA_VERSION) HLTSET51
if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

# global debug_file
# set debug_file [info script]_[clock seconds].log
# puts "debug_file == $debug_file"
# if {[info commands ::realIxNet] == [list]} {
#     rename ixNet realIxNet
# }
# 
# 
# 
# proc ::ixNet args {
#     global debug_file
#     set fid [open $debug_file "a+"]
#     puts $fid "ixNet $args"
#     close $fid
#     set retval [uplevel 1 ::realIxNet $args]
#     return $retval
# }


################################################################################
# General script variables
################################################################################
set test_name               [info script]

################################################################################
# START - Connect to the chassis
################################################################################
set var_list [list chassis_ip port_list break_locks tcl_server ixnetwork_tcl_server]

set chassis_ip              10.205.16.32
set port_list               [list 2/3 2/4]
set break_locks             1
set tcl_server              10.205.16.32
set ixnetwork_tcl_server    localhost


if {[info exists tcl_server] && [info exists ixnetwork_tcl_server]} {
    set connect_status [::ixia::connect                                        \
            -reset                                                             \
            -device               $chassis_ip                                  \
            -port_list            $port_list                                   \
            -break_locks          $break_locks                                 \
            -tcl_server           $tcl_server                                  \
            -ixnetwork_tcl_server $ixnetwork_tcl_server                        \
            ]
} elseif {[info exists tcl_server]} {
    set connect_status [::ixia::connect                                        \
            -reset                                                             \
            -device               $chassis_ip                                  \
            -port_list            $port_list                                   \
            -break_locks          $break_locks                                 \
            -tcl_server           $tcl_server                                  \
            ]
} elseif {[info exists ixnetwork_tcl_server]} {
    set connect_status [::ixia::connect                                        \
            -reset                                                             \
            -device               $chassis_ip                                  \
            -port_list            $port_list                                   \
            -break_locks          $break_locks                                 \
            -ixnetwork_tcl_server $ixnetwork_tcl_server                        \
            ]
} else {
    set connect_status [::ixia::connect                                        \
            -reset                                                             \
            -device               $chassis_ip                                  \
            -port_list            $port_list                                   \
            -break_locks          $break_locks                                 \
            ]
}
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

foreach item $var_list {catch {unset $item}}
################################################################################
# END - Connect to the chassis
################################################################################

puts "Connect to the chassis complete."

################################################################################
# START - Interface configuration - L1
################################################################################
puts "Start interface configuration L1 ..."
update idletasks
set var_list [list intf_cfg_port_handle intf_mode speed autonegotiation duplex  \
                   phy_mode clocksource]

set intf_cfg_port_handle      $port_handle
set intf_mode                 $::cfg::l1_intf_mode ;# CHOICES atm 
                                                   ;# CHOICES ethernet (for 10/100/1000 Ethernet cards and 10GE cards)
                                                   ;# CHOICES pos_hdlc pos_ppp frame_relay1490 frame_relay2427 frame_relay_cisco srp srp_cisco rpr gfp (for POS cards)
set speed                     $::cfg::l1_speed     ;# CHOICES ether10 ether100 ether1000 auto DEFAULT ether100 (for 10/100/1000 Ethernet cards)
                                                   ;# CHOICES ether10000lan ether10000wan (for 10GE cards)
                                                   ;# CHOICES oc3 oc12 oc48 oc192 DEFAULT oc12 (for ATM and POS cards)


set pgid_mode          split            ;# CHOICES custom dscp ipv6TC mplsExp split 
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
set pgid_split1_offset 128                         ;# NUMERIC
set pgid_split1_width  4                           ;# RANGE 0-4

#set ::ixia::debug 1
set ::ixia::debug 0

################################################################################
array set traffic_offset_map {
    outer_vlan_priority     "Outer VLAN Priority (3 bits)"
    outer_vlan_id_4         "Outer VLAN ID (4 bits)"
    outer_vlan_id_6         "Outer VLAN ID (6 bits)"
    outer_vlan_id_8         "Outer VLAN ID (8 bits)"
    outer_vlan_id_10        "Outer VLAN ID (10 bits)"
    outer_vlan_id_12        "Outer VLAN ID (12 bits)"
    inner_vlan_priority     "Inner VLAN Priority (3 bits)"
    inner_vlan_id_4         "Inner VLAN ID (4 bits)"
    inner_vlan_id_6         "Inner VLAN ID (6 bits)"
    inner_vlan_id_8         "Inner VLAN ID (8 bits)"
    inner_vlan_id_10        "Inner VLAN ID (10 bits)"
    inner_vlan_id_12        "Inner VLAN ID (12 bits)"
    tos_precedence          "IPv4 TOS Precedence (3 bits)"
    dscp                    "IPv4 DSCP (6 bits)"
    ipv6TC                  "IPv6 Traffic Class (8 bits)"
    ipv6TC_bits_0_2         "IPv6 Traffic Class Bits 0-2 (3 bits)"
    ipv6TC_bits_0_5         "IPv6 Traffic Class Bits 0-5 (6 bits)"
    mplsExp                 "MPLS Exp (3 bits)"
    split                   "Custom"
}
################################################################################
foreach current_traffic_offset [array names traffic_offset_map] {
    set pgid_mode $current_traffic_offset
    puts "======================== PGID mode = $pgid_mode ======================="
    ################################################################################
    # 10/100/1000 Ethernet cards
    ################################################################################
    if {$intf_mode == "ethernet" && [lsearch {ether10 ether100 ether1000 auto} $speed] != -1} {
        set autonegotiation             1                 ;# CHOICES 0 1 DEFAULT 1
        set duplex                      auto              ;# CHOICES half full auto DEFAULT full
        set phy_mode                    copper            ;# CHOICES copper fiber DEFAULT copper
        # set clocksource               internal          ;# NA - CHOICES internal loop external DEFAULT internal
        
        foreach port $intf_cfg_port_handle {
            set interface_status [::ixia::interface_config                             \
                    -port_handle      $port                                            \
                    -mode             config                                           \
                    -intf_mode        $intf_mode                                       \
                    -autonegotiation  $autonegotiation                                 \
                    -speed            $speed                                           \
                    -duplex           $duplex                                          \
                    -phy_mode         $phy_mode                                        \
                    -pgid_mode        $pgid_mode                                       \
                    -pgid_encap       $pgid_encap                                      \
                    -pgid_split1_offset $pgid_split1_offset                            \
                    -pgid_split1_width  $pgid_split1_width                             \
                    ]
            if {[keylget interface_status status] != $::SUCCESS} {
                puts "FAIL - $test_name - [keylget interface_status log]"
                return 0
            }
        }
    }
    ################################################################################
    # 10G Ethernet cards
    ################################################################################
    if {$intf_mode == "ethernet" && [lsearch {ether10000lan ether10000wan} $speed] != -1} {
        # set autonegotiation         1                   ;# NA - CHOICES 0 1 DEFAULT 1
        # set duplex                  auto                ;# NA - CHOICES half full auto DEFAULT full
        # set phy_mode                copper              ;# NA - CHOICES copper fiber DEFAULT copper
        # set clocksource             internal            ;# NA - CHOICES internal loop external DEFAULT internal
        
        foreach port $intf_cfg_port_handle {
            set interface_status [::ixia::interface_config                             \
                    -port_handle      $port                                            \
                    -mode             config                                           \
                    -intf_mode        $intf_mode                                       \
                    -speed            $speed                                           \
                    -pgid_mode        $pgid_mode                                       \
                    -pgid_encap       $pgid_encap                                      \
                    -pgid_split1_offset $pgid_split1_offset                            \
                    -pgid_split1_width  $pgid_split1_width                             \
                    ]
            if {[keylget interface_status status] != $::SUCCESS} {
                puts "FAIL - $test_name - [keylget interface_status log]"
                return 0
            }
        }
    }
    
    #foreach item $var_list { catch {unset $item}}
    puts "End interface configuration L1 ..."
    #update idletasks
    ################################################################################
    # END - Interface configuration - L1
    ################################################################################
    
    puts "Layer 1 config complete."
    
    ################################################################################
    # Testing section BEGINS -------------------------------------------------------
    ################################################################################
    puts "  -------------------------------------------------------------------"
    set flow_measurement_mode [ixNet getA ::ixNet::OBJ-/traffic -flowMeasurementMode]
    if {$flow_measurement_mode == "splitPGID"} {
        puts "  Split PGID mode Active - Ok."
    } else {
        puts "! Flow Measurement Mode is not Split Pgid (it is $flow_measurement_mode)."
        return 0
    }
    set iteration_index 0
    foreach port_identifier [ixNet getL [ixNet getRoot] vport] {
        set traffic_port [lindex [ixNet getL ::ixNet::OBJ-/traffic/splitPgidSettings setting] $iteration_index]
        puts "  ***** Checking for port $port_identifier *****"
        puts "  ***** Traffic entry: $traffic_port *****"
        foreach current_component [ixNet getL $traffic_port component] {
            puts "    *** Component $current_component ***"
            #-----------------------------------------------------------------------
            if {$pgid_mode != "split"} {
                set current_encapsulation [ixNet getAttribute $current_component -encapsulation]
                set match [regexp {::ixNet::OBJ-/traffic/splitPgidSettings/setting/encapsulation:"([a-zA-Z]+)"} $current_encapsulation match_name particle]
                set particle [string tolower $particle]
                if {$particle == $intf_mode} {
                    puts "  Encapsulation - $particle - Ok."
                } else {
                    puts "! Encapsulation is $particle (should be $intf_mode)"
                }
            }
            #-----------------------------------------------------------------------
            set current_pgid_mode [ixNet getAttribute $current_component -predefinedOffset]
            set match [regexp {::ixNet::OBJ-/traffic/splitPgidSettings/setting/predefinedOffset:"([a-zA-Z0-9( )-]+)"} $current_pgid_mode match_name particle]
            set particle [string trim $particle]
            if {![info exists traffic_offset_map($pgid_mode)]} {
                set traffic_offset_map($pgid_mode) "-unknown-" 
            }
            if {$particle == $traffic_offset_map($pgid_mode)} {
                puts "  Pgid mode - $particle - Ok."
            } else {
                puts "! Pgid mode is $particle (should be $traffic_offset_map($pgid_mode))"
            }
            #-----------------------------------------------------------------------
            if {$pgid_mode == "split"} {
                set field_custom_width  [ixNet getAttribute $current_component -customWidth]
                if {$field_custom_width == $pgid_split1_width} {
                    puts "  Pgid custom width - $pgid_split1_width - Ok."
                } else {
                    puts "! Pgid custom width is $field_custom_width (should be $pgid_split1_width)"
                }
                set field_custom_offset [ixNet getAttribute $current_component -customOffset]
                if {$field_custom_offset == $pgid_split1_offset} {
                    puts "  Pgid custom offset - $field_custom_offset - Ok."
                } else {
                    puts "! Pgid custom offset is $field_custom_offset (should be $pgid_split1_offset)"
                }
            }
        }
        puts "  ---------------------------------------------------------------------"
    }
    ################################################################################
    # Testing section ENDS ---------------------------------------------------------
    ################################################################################
    
}
foreach item $var_list { catch {unset $item}}
update idletasks

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
