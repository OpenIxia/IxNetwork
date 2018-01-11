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
#    This sample creates PBB bridges with custom TLVs and trunks,              #
#    starts the protocol and retrieves protocol aggregated stats per port.     #
#    The setup used are two ixia port connected back-to-back.                  #
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


################################################################################
# General script variables
################################################################################
set test_name                                   [info script]
set bridge_count                                3
set trunk_count                                 2
set mr_count                                    2
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
# Interface configuration - L1
################################################################################
puts "Start interface configuration L1 ..."
update idletasks

set interface_status [::ixia::interface_config                             \
        -port_handle      $port_handle                                     \
        -mode             config                                           \
        -intf_mode        ethernet                                         \
        -autonegotiation  1                                                \
        -speed            auto                                             \
        -duplex           auto                                             \
        -phy_mode         copper                                           \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}

puts "End interface configuration L1 ..."
update idletasks

################################################################################
# PBB bridge configuration
################################################################################
puts "\n### Start PBB bridge configuration ..."
update idletasks
set port 1
foreach port_h $port_handle {
    foreach {ch ca po} [split $port_h /] {}
    set bridge_id        [format %02x $ch]:[format %02x $ca]:[format %02x $po]:00:AA:01
    set mac_address_init [format %02x $ch]:[format %02x $ca]:[format %02x $po]:BB:00:01
    set pbb_config_status [::ixia::emulation_pbb_config                        \
            -mode                                     create                   \
            -port_handle                              $port_h                  \
            -bridge_id                                $bridge_id               \
            -bridge_id_step                           00:00:00:02:00:00        \
            -count                                    $bridge_count            \
            -enable_optional_tlv_validation           0                        \
            -enable_out_of_sequence_detection         1                        \
            -ether_type                               8902                     \
            -mac_address_init                         $mac_address_init        \
            -mac_address_step                         00:00:00:00:02:00        \
            -receive_ccm                              1                        \
            -send_ccm                                 1                        \
            -vlan_id                                  100                      \
            -vlan_id_step                             2                        \
            -vlan_user_priority                       3                        \
            ]
   if {[keylget pbb_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pbb_config_status log]"
    return 0
    }
    set pbb_handles_$port [keylget pbb_config_status handle]
    puts "Ixia pbb_bridge handles for port $port are: "
    update idletasks
    foreach pbb_handle [set pbb_handles_$port] {
        puts $pbb_handle
        update idletasks
    }
    incr port
}


################################################################################
# PBB trunk configuration
################################################################################
puts "\n### Start PBB trunk configuration ..."
update idletasks
set port 1

set dst_mac_address_list {}
set src_mac_address_list {}

for {set i 1} {$i <= $bridge_count} {incr i} {
    lappend dst_mac_address_list aa:bb:00:00:1$i:01
    lappend src_mac_address_list cc:dd:00:00:1$i:01
}


array set rev_port_mac_address_list [list \
    $port_0,dst dst_mac_address_list \
    $port_0,src src_mac_address_list \
    $port_1,src dst_mac_address_list \
    $port_1,dst src_mac_address_list \
    ]
foreach port_h $port_handle { 
    set bridge_handles [set pbb_handles_$port] 
    set bridge 1
    set dst_mac_address_list_temp [set $rev_port_mac_address_list($port_h,dst)]
    set src_mac_address_list_temp [set $rev_port_mac_address_list($port_h,src)]
    foreach bridge_handle $bridge_handles {
        set pbb_trunk_config_status [::ixia::emulation_pbb_trunk_config        \
                -bridge_handle                             $bridge_handle      \
                -mode                                      create              \
                -count                                     $trunk_count        \
                -dst_mac_address                           [lindex $dst_mac_address_list_temp [expr $bridge - 1]] \
                -src_mac_address                           [lindex $src_mac_address_list_temp [expr $bridge - 1]]  \
                -add_ccm_custom_tlvs                       1                   \
                -add_data_tlv                              1                   \
                -add_interface_status_tlv                  1                   \
                -add_lbm_custom_tlvs                       1                   \
                -add_lbr_custom_tlvs                       1                   \
                -add_ltm_custom_tlvs                       1                   \
                -add_ltr_custom_tlvs                       1                   \
                -add_organization_specific_tlv             1                   \
                -add_port_status_tlv                       1                   \
                -add_sender_id_tlv                         1                   \
                -auto_dm_iteration                         100                 \
                -auto_dm_timeout                           5                   \
                -auto_dm_timer                             30                  \
                -auto_lb_iteration                         200                 \
                -auto_lb_timeout                           5                   \
                -auto_lb_timer                             40                  \
                -auto_lt_iteration                         300                 \
                -auto_lt_timeout                           6                   \
                -auto_lt_timer                             50                  \
                -b_vlan_id                                 100                 \
                -b_vlan_priority                           3                   \
                -b_vlan_tp_id                              9100                \
                -cci_interval                              10msec              \
                -ccm_priority                              1                   \
                -chassis_id                                00:00:00:00:00:11   \
                -chassis_id_length                         6                   \
                -chassis_id_step                           00:00:00:00:00:a1   \
                -chassis_id_sub_type                       chassis_component   \
                -data_tlv_length                           4                   \
                -data_tlv_step                             00:00:00:03         \
                -data_tlv_value                            11:22:33:44         \
                -dmm_priority                              4                   \
                -enable_auto_dm                            1                   \
                -enable_auto_lb                            1                   \
                -enable_auto_lt                            1                   \
                -enable_reverse_bvlan                      1                   \
                -lbm_priority                              2                   \
                -ltm_priority                              7                   \
                -management_address                        a1:a2:a3:a3:a4:a5   \
                -management_address_domain                 4d:61:6e:61:67:65:6d:65:6e:74:20:41:64:64:72:20:44:6f:6d:61:69:6e \
                -management_address_domain_length          22                  \
                -management_address_domain_step            00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:01 \
                -management_address_length                 6                   \
                -md_level_id                               3                   \
                -md_name                                   IxiaUser            \
                -md_name_format                            string              \
                -mep_id                                    ${port}${bridge}0   \
                -mr_count                                  $mr_count           \
                -mr_inner_count                            $mr_count           \
                -mr_enable_vlan                            1                   \
                -mr_i_tagi_sid                             10                  \
                -mr_start_mac_address                      00:00:00:aa:00:01   \
                -mr_mac_inter_range_step                   00:00:00:00:01:50   \
                -mr_mac_inter_trunk_step                   00:00:00:a1:00:00   \
                -mr_mac_step                               00:00:00:00:00:02   \
                -mr_s_vlan_id                              20                  \
                -mr_s_vlan_priority                        5                   \
                -mr_s_vlan_tp_id                           8100                \
                -mr_stacked_vlan_id_step                   12                  \
                -mr_stacked_vlan_inter_trunk_step          15                  \
                -mr_type                                   single              \
                -mr_vlan_id_step                           2                   \
                -mr_vlan_inter_trunk_step                  100                 \
                -organization_specific_tlv_length          5                   \
                -organization_specific_tlv_value           00:00:00:ff:ee      \
                -override_vlan_priority                    1                   \
                -reverse_bvlan_id                          1000                \
                -short_ma_name                             "ixia-user"         \
                -short_ma_name_format                      char_string         \
                -ttl                                       64                  \
                ]
        if {[keylget pbb_trunk_config_status status] != $::SUCCESS} {
            puts "FAIL - $test_name - [keylget pbb_trunk_config_status log]"
            return 0
        }
        set PB $port/$bridge
        set pbb_trunk_handles_$PB [keylget pbb_trunk_config_status trunk_handle]
        puts "Ixia pbb trunk handles for port/bridge $PB are: "
        update idletasks
        foreach pbb_trunk_handle [set pbb_trunk_handles_$PB] {
            puts $pbb_trunk_handle
            update idletasks
        }
        incr bridge
    }
    incr port
}


################################################################################
# PBB custom TLV configuration
################################################################################
puts "\n### Start PBB custom TLV configuration ..."
update idletasks
set port 1
foreach port_h $port_handle { 
    set bridge_handles [set pbb_handles_$port] 
    set bridge 1
    foreach bridge_handle $bridge_handles { 
        set pbb_custom_tlv_config_status [::ixia::emulation_pbb_custom_tlv_config \
                -bridge_handle          $bridge_handle          \
                -mode                   create                  \
                -count                  3                       \
                -include_in_ccm         1                       \
                -include_in_lbm         1                       \
                -include_in_lbr         1                       \
                -include_in_ltm         1                       \
                -include_in_ltr         1                       \
                -length                 3                       \
                -reset                  1                       \
                -type                   70                      \
                -value                  11:22:aa                \
                -value_step             0a:11:00                \
                ]
        if {[keylget pbb_custom_tlv_config_status status] != $::SUCCESS} {
            puts "FAIL - $test_name - [keylget pbb_custom_tlv_config_status log]"
            return 0
        }
        set PB $port/$bridge
        set pbb_custom_tlv_handles_$PB [keylget pbb_custom_tlv_config_status handle]
        puts "Ixia pbb custom tlv handles for port/bridge $PB are: "
        update idletasks
        foreach pbb_custom_tlv_handle [set pbb_custom_tlv_handles_$PB] {
            puts $pbb_custom_tlv_handle
            update idletasks
        }
        incr bridge
    }
    incr port
}

################################################################################
# Start protocol
################################################################################
puts "\n### Starting PBB-TE protocol"
update idletasks
set protocol_status [::ixia::emulation_pbb_control                         \
        -mode                        start                                 \
        -port_handle                 $port_handle                          \
    ]
if {[keylget protocol_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget protocol_status log]"
        return 0
    }
puts "\nSUCCESS protocol started!"
update idletasks

after 30000

################################################################################
# Collect statistics
################################################################################
puts "\n###Collecting statistics ..."
update idletasks

#########################
#SHOW STATS PROCEDURE   #
#########################
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
            #show_stats [keylget var $key]
    }
}

set pbb_info_status_1 [::ixia::emulation_pbb_info                              \
        -mode                               aggregated_stats                   \
        -port_handle                        $port_0                            \
        ]
        
if {[keylget pbb_info_status_1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pbb_info_status_1 log]"
    return 0
}
puts "\n# Statistics for port $port_0:"
update idletasks
show_stats $pbb_info_status_1

set pbb_info_status_2 [::ixia::emulation_pbb_info                              \
        -mode                               aggregated_stats                   \
        -port_handle                        $port_1                            \
        ]
if {[keylget pbb_info_status_2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pbb_info_status_2 log]"
    return 0
}
puts "\n# Statistics for port $port_1:"
update idletasks
show_stats $pbb_info_status_2


################################################################################
# Statistics pass fail
################################################################################
set cfgErrors    0
set errorMessage ""

set bridges_running    $bridge_count
set bridges_configured $bridge_count
set trunks_running     [expr $bridge_count * $trunk_count]
set trunks_configured  [expr $bridge_count * $trunk_count]
set mas_running        $bridge_count
set mas_configured     $bridge_count

set agg_params {
        bridges_running               
        trunks_running         
        bridges_configured                
        trunks_configured                  
        mas_running                    
        mas_configured         
}
puts "\n### Verifying aggregated statistics on port $port_0"
foreach pair [keylget pbb_info_status_1 $port_0] { 
    set stat_name  [lindex $pair 0] 
    set stat_value [lindex $pair 1]
    foreach hlt_stat $agg_params {
        if {$stat_name == $hlt_stat} {
            set hlt_param_value [set $hlt_stat]
            if {$stat_value != $hlt_param_value} {
                    incr cfgErrors
                    append errorMessage " ! $hlt_stat = $stat_value (should be $hlt_param_value) \n"
                }
            }
       }
}
puts "\n### Verifying protocol statistics on port $port_1"
foreach pair [keylget pbb_info_status_2 $port_1] { 
    set stat_name  [lindex $pair 0] 
    set stat_value [lindex $pair 1]
    puts [format "%30s %30s" $stat_name $stat_value]
    foreach hlt_stat $agg_params {
        if {$stat_name == $hlt_stat} {
            set hlt_param_value [set $hlt_stat]
            if {$stat_value != $hlt_param_value} {
                    incr cfgErrors
                    append errorMessage " ! $hlt_stat = $stat_value (should be $hlt_param_value)\n"
                }
            }
       }
}


################################################################################
# Stop protocol
################################################################################
set protocol_status [::ixia::emulation_pbb_control                             \
            -mode                        stop                                  \
            -port_handle                 $port_handle                          \
        ]
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}
puts "\nSUCCESS protocol stopped!"

################################################################################
# Verify errors
################################################################################
if {$cfgErrors} {
    puts "FAIL - ::ixia::emulation_pbb_info aggregated_stats - There were $cfgErrors configuration errors. \n$errorMessage"
    return 0
} else {
    puts "\n### Aggregated Stats are Ok."
}
puts "\nEnd test ..."
puts "\nSUCCESS - $test_name - [clock format [clock seconds]]"
return 1
