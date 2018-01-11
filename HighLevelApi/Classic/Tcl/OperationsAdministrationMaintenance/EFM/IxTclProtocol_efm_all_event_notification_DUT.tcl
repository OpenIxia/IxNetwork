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
#    This sample configures Ethernet OAM on the Ixia port.                     #
#    Ixia port is connected to Cisco 7200 Router.                              #
#    EFM is started on the Ixia port and statistics are collected.             #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET50.                                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# DUT configuration:                                                           #
# 
# configure terminal
# 
# default interface GigabitEthernet0/2
# 
# interface GigabitEthernet0/2
#   no shutdown
#   ethernet oam
#   ethernet oam mode active
#   ethernet oam link-monitor supported
#   ethernet oam link-monitor on
#   ethernet oam link-monitor frame window 600
#   ethernet oam link-monitor frame threshold high 3
#   ethernet oam link-monitor receive-crc window 300
#   ethernet oam link-monitor receive-crc threshold high 12
#   ip address 192.168.1.1 255.255.255.0
#  exit
# end
################################################################################


set env(IXIA_VERSION) HLTSET50
if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}
################################################################################
# General script variables
################################################################################
set test_name               [info script]


################################################################################
# Connect to the chassis
################################################################################
puts "Start connecting to chassis ..."
update idletasks

set chassis_ip              10.205.17.50
set port_list               [list 2/1]

set connect_status [::ixia::connect                                        \
        -reset                                                             \
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
# START - Interface configuration
################################################################################
puts "Start interface configuration ..."
update idletasks

set interface_status [::ixia::interface_config                         \
        -port_handle            $port_0                                \
        -mode                   config                                 \
        -intf_mode              ethernet                               \
        -autonegotiation        1                                      \
        -speed                  auto                                   \
        -duplex                 auto                                   \
        -src_mac_addr           00aa.00bb.cc01                         \
        -intf_ip_addr           192.168.1.100                          \
        -gateway                192.168.1.1                            \
        -netmask                255.255.255.0                          \
        -ipv6_intf_addr         100::2                                 \
        -ipv6_prefix_length     64                                     \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}
        
lappend interface_handles_$port_0 [keylget interface_status interface_handle]
puts "End interface configuration  ..."
update idletasks

################################################################################
# Additional procedures
################################################################################
proc printStats {keyedList} {
    set statsList {
        statistics.mac_remote                            "Remote MAC Address"
        statistics.oam_mode                              "OAM Mode"
        statistics.unidir_enabled                        "Unidirectional Support"
        statistics.remote_loopback_enabled               "Loopback Support"
        statistics.link_events_enabled                   "Link Events Support"
        statistics.variable_retrieval_enabled            "Variable Retrieval Support"
        statistics.oampdu_size                           "Max OAM PDU size"
        statistics.oampdu_count.information_tx           "EOAM Information PDUs Sent"
        statistics.oampdu_count.information_rx           "EOAM Information PDUs Received"
        statistics.oampdu_count.event_notification_rx    "EOAM Event Notification PDUs Received"
        statistics.oampdu_count.loopback_control_rx      "EOAM Loopback Control PDUs Received"
        statistics.oampdu_count.organization_rx          "EOAM Organization PDUs Received"
        statistics.oampdu_count.variable_request_rx      "EOAM Variable Request PDUs Received"
        statistics.oampdu_count.variable_response_rx     "EOAM Variable Response PDUs Received"
        statistics.oampdu_count.unsupported_rx           "EOAM Unsupported PDUs Received"
        statistics.oampdu_count.total_rx                 "EOAM Total PDUs Received"
        statistics.oui_value                             "OUI"
        statistics.vsi_value                             "Vendor Specific Information"
    }
    
    puts "Statistics for Port Handle [keylget keyedList port_handle]:"
    foreach {statKey statName} $statsList {
        puts "\t[format {%-45s%-25s} $statName [keylget keyedList $statKey]]"
    }
    puts "\n\n"
}

################################################################################
# START - EFM configuration
################################################################################
puts "Start EFM configuration ..."
update idletasks

set efm_config_status [::ixia::emulation_efm_config                            \
        -api_used                                ixprotocol                    \
        -port_handle                             $port_0                       \
        -error_frame_period_threshold            30                            \
        -error_frame_period_window               300                           \
        -error_frame_summary_threshold           30                            \
        -error_frame_summary_window              300                           \
        -error_frame_threshold                   40                            \
        -error_frame_window                      400                           \
        -error_symbol_period_threshold           50                            \
        -error_symbol_period_window              500                           \
        -oam_mode                                passive                       \
        -oui_value                               00aabb                        \
        -size                                    256                           \
        -vsi_value                               00aabbcc                      \
        -disable_information_pdu_tx              0                             \
        -disable_non_information_pdu_tx          0                             \
        -enable_loopback_response                1                             \
        -enable_variable_response                1                             \
        -event_interval                          1                             \
        -error_frame_count                       40                            \
        -error_frame_period_count                30                            \
        -error_frame_summary_count               30                            \
        -error_symbol_period_count               50                            \
        -information_pdu_rate                    1                             \
        -link_event_tx_mode                      periodic                      \
        -local_lost_link_timer                   5                             \
        -loopback_cmd                            enable_oam_remote_loopback    \
        -loopback_timeout                        10                            \
        -supports_remote_loopback                0                             \
        -supports_unidir_mode                    0                             \
        -variable_response_timeout               1                             \
        -link_events                             1                             \
        -variable_retrieval                      0                             \
        -os_oampdu_data_oui                      0x000000                      \
        ]
if {[keylget efm_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget efm_config_status log]"
    return 0
}

######################
# Start Ethernet OAM #
######################

puts "\nStarting Ethernet OAM"
set control_status [::ixia::emulation_efm_control \
        -api_used    ixprotocol             \
        -port_handle $port_0                \
        -action      start                  \
        ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}

##############################################################
# Get and print Ethernet OAM statistics while OAM is running #
##############################################################
set retry_count 5
for {set retry_iteration 0} {$retry_iteration < $retry_count} {incr retry_iteration} {
    after 5000
    puts "\nRetry iteration $retry_iteration - port $port_0"
    set pass_break 1
    set stat_status1 [::ixia::emulation_efm_stat \
            -api_used    ixprotocol              \
            -port_handle $port_0                 \
            -action      get                     \
            ]
    if {[keylget stat_status1 status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget stat_status1 log]"
        return 0
    }
    
    printStats $stat_status1
    
    if {[keylget stat_status1 statistics.oam_mode] != "active"} {
        set errMsg "FAIL - $test_name - OAM Mode error.\nExpected: active\
                \nActual:[keylget stat_status1 statistics.oam_mode]"
        set pass_break 0
    }
    if {[keylget stat_status1 statistics.link_events_enabled] != "Supported"} {
        set errMsg "FAIL - $test_name - Link Events error.\nExpected: Supported\
                \nActual:[keylget stat_status1 statistics.link_events_enabled]"
        set pass_break 0
    }
    if {[keylget stat_status1 statistics.variable_retrieval_enabled] != "Not Supported"} {
        set errMsg "FAIL - $test_name - Variable Retrieval error.\nExpected: Not Supported\
                \nActual:[keylget stat_status1 statistics.variable_retrieval_enabled]"
        set pass_break 0
    }
    
    if {$pass_break} {
        break
    }
}

if {!$pass_break} {
    puts $errMsg
    return 0
}

##############################################################
# EFM was negotiated with DUT. Send Link Events.             #
##############################################################

puts "\nSend Ethernet OAM Event Notifications."
set control_status [::ixia::emulation_efm_control \
        -api_used    ixprotocol                   \
        -port_handle $port_0                      \
        -action      start_event                  \
        ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}


after 50000

puts "\nStop Send Ethernet OAM Event Notifications."
set control_status [::ixia::emulation_efm_control \
        -api_used    ixprotocol                   \
        -port_handle $port_0                      \
        -action      stop_event                   \
        ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}

##############################################################
# Check if event notificatoins were sent.                    #
##############################################################
set stat_status1 [::ixia::emulation_efm_stat \
            -api_used    ixprotocol          \
            -port_handle $port_0             \
            -action      get                 \
            ]
if {[keylget stat_status1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stat_status1 log]"
    return 0
}

set stats_check_list {
    statistics.oampdu_count.event_notification_tx              "Event Notifications sent"
    statistics.alarms.errored_symbol_period_events_tx          "Errored Symbol Period Event Running Total Tx"
    statistics.alarms.errored_symbol_period_errors_tx          "Errored Symbol Period Error Running Total Tx"
    statistics.alarms.errored_frame_events_tx                  "Errored Frame Event Running Total Tx"
    statistics.alarms.errored_frame_errors_tx                  "Errored Frame Error Running Total Tx"
    statistics.alarms.errored_frame_period_events_tx           "Errored Frame Period Event Running Total Tx"
    statistics.alarms.errored_frame_period_errors_tx           "Errored Frame Period Error Running Total Tx"
    statistics.alarms.errored_frame_seconds_summary_events_tx  "Errored Frame SS Event Running Total Tx"
    statistics.alarms.errored_frame_seconds_summary_errors_tx  "Errored Frame SS Error Running Total Tx"
}

foreach {stat_key stat_desc} $stats_check_list {
    if {[keylget stat_status1 $stat_key] == 0} {
        puts "FAIL - $test_name - OAM $stat_key error.\n\
                $stat_desc is 0."
        return 0
    }
}

######################
# Stop Ethernet OAM  #
######################

puts "\nStopping Ethernet OAM"
set control_status [::ixia::emulation_efm_control \
        -api_used    ixprotocol                   \
        -port_handle $port_0                      \
        -action      stop                         \
        ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}


puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
