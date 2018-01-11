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
#    It configures two IPv4 Ethernet interfaces and configures Ethernet OAM.   #
#    One Information OAMPDU is on the TX port.                                 #
#    One Event Notification OAM with 4 TLV (Error Frame, Error Frame Period,   #
#    Error Frame Summary and Error Symbol Period) is added on the TX port.     #
#    Three non-EFM traffic streams are added.                                  #
#    The OAMPDU percent rates are modified.                                    #
#    Traffic and Ethernet OAM are started and statistics are gathered.         #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET50.                                      #
#                                                                              #
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
set port_list               [list 2/1 2/2]

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
        statistics.alarms.errored_symbol_period_events   "Error Symbol Period TLV Count"
        statistics.alarms.errored_frame_events           "Error Frame TLV Count"
        statistics.alarms.errored_frame_period_events    "Error Frame Period TLV Count"
        statistics.alarms.errored_frame_seconds_summary_events "Error Frame Seconds Summary TLV Count"
    }
    
    puts "Statistics for Port Handle [keylget keyedList port_handle]:"
    foreach {statKey statName} $statsList {
        puts "\t[format {%-45s%-25s} $statName [keylget keyedList $statKey]]"
    }
    puts "\n\n"
}
########
# IpV4 #
########
set ipV4_port_list    "$port_0        $port_1"
set ipV4_ixia_list    "1.1.1.2        1.1.1.1"
set ipV4_gateway_list "1.1.1.1        1.1.1.2"
set ipV4_netmask_list "255.255.255.0  255.255.255.0"
set ipV4_mac_list     "0000.debb.0001 0000.debb.0002"
set ipV4_version_list "4              4"
set ipV4_autoneg_list "1              1"
set ipV4_duplex_list  "full           full"
set ipV4_speed_list   "ether100       ether100"
set ipV4_port_rx_mode "packet_group   capture" 

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    $ipV4_ixia_list     \
        -gateway         $ipV4_gateway_list  \
        -netmask         $ipV4_netmask_list  \
        -autonegotiation $ipV4_autoneg_list  \
        -duplex          $ipV4_duplex_list   \
        -src_mac_addr    $ipV4_mac_list      \
        -speed           $ipV4_speed_list    \
        -port_rx_mode    $ipV4_port_rx_mode  ]
if {[keylget interface_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}

##################################################
# Remove all streams, including Ethernet OAMPDUs #
##################################################

set traffic_status [ixia::traffic_config \
        -mode        reset               \
        -port_handle $port_0             ]

if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

set traffic_status [ixia::traffic_config \
        -mode        reset               \
	    -port_handle $port_1             ]

if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

###########################################
# Configure first stream on the IpV4 port #
###########################################

puts "\nConfiguring Ethernet OAM and traffic streams"
set traffic_status [ixia::traffic_config         \
        -mode         create                     \
        -port_handle  $port_0                    \
        -l3_protocol  ipv4                       \
        -ip_src_addr  [lindex $ipV4_ixia_list 0] \
        -ip_dst_addr  [lindex $ipV4_ixia_list 1] \
        -l3_length    46                         \
        -rate_percent 0.5                        \
        -mac_dst_mode discovery                  \
        -mac_src      [lindex $ipV4_mac_list 0]  ]
if {[keylget traffic_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

##########################################################################
# Configure Ethernet OAM port, Information and Event Notification OAMPDU #
##########################################################################

set efm_status [::ixia::emulation_efm_config       \
        -api_used                       ixprotocol \
        -port_handle                    $port_0    \
        -link_events                               \
        -oam_mode                       active     \
        -variable_retrieval                        \
        -error_frame_count              5          \
        -error_frame_period_count       6          \
        -error_frame_period_threshold   66         \
        -error_frame_period_window      660        \
        -error_frame_threshold          55         \
        -error_frame_window             550        \
        -error_frame_summary_count      7          \
        -error_frame_summary_threshold  77         \
        -error_frame_summary_window     770        \
        -error_symbol_period_count      8          \
        -error_symbol_period_threshold  88         \
        -error_symbol_period_window     880        \
        -mac_local     [lindex $ipV4_mac_list 0]   \
        -size                           1518       \
    ]
if {[keylget efm_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget efm_status log]"
    return 0
}

set information_stream_id           [keylget efm_status information_oampdu_id]
set event_notification_stream_id    [keylget efm_status event_notification_oampdu_id]

set efm_status [::ixia::emulation_efm_config       \
        -api_used                       ixprotocol \
        -port_handle                    $port_1    \
        -link_events                               \
        -oam_mode                       passive    \
        -variable_retrieval                        \
        -error_frame_count              5          \
        -error_frame_period_count       6          \
        -error_frame_period_threshold   66         \
        -error_frame_period_window      660        \
        -error_frame_threshold          55         \
        -error_frame_window             550        \
        -error_frame_summary_count      7          \
        -error_frame_summary_threshold  77         \
        -error_frame_summary_window     770        \
        -error_symbol_period_count      8          \
        -error_symbol_period_threshold  88         \
        -error_symbol_period_window     880        \
        -mac_local     [lindex $ipV4_mac_list 1]   \
        -size                           1518       \
    ]
if {[keylget efm_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget efm_status log]"
    return 0
}

# Configure second stream on the IpV4 port
set traffic_status [ixia::traffic_config         \
        -mode         create                     \
        -port_handle  $port_0                    \
        -l3_protocol  ipv4                       \
        -ip_src_addr  [lindex $ipV4_ixia_list 0] \
        -ip_dst_addr  [lindex $ipV4_ixia_list 1] \
        -l3_length    54                         \
        -rate_percent 0.5                        \
        -mac_dst_mode discovery                  \
        -mac_src      [lindex $ipV4_mac_list 0]  ]
if {[keylget traffic_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

# Configure third stream on the IpV4 port
set traffic_status [ixia::traffic_config         \
        -mode         create                     \
        -port_handle  $port_0                    \
        -l3_protocol  ipv4                       \
        -ip_src_addr  [lindex $ipV4_ixia_list 0] \
        -ip_dst_addr  [lindex $ipV4_ixia_list 1] \
        -l3_length    65                         \
        -rate_percent 0.5                        \
        -mac_dst_mode discovery                  \
        -mac_src      [lindex $ipV4_mac_list 0]  ]
if {[keylget traffic_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

# Modify traffic rate for the Information OAMPDU to 10%
set traffic_status [ixia::traffic_config         \
        -mode         modify                     \
        -port_handle  $port_0                    \
        -stream_id    $information_stream_id     \
        -rate_percent 0.1                        ]
if {[keylget traffic_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

# Modify traffic rate for the Information OAMPDU to 10%
set traffic_status [ixia::traffic_config         \
        -mode         modify                     \
        -port_handle  $port_0                    \
        -stream_id    $event_notification_stream_id     \
        -rate_percent 0.1                        ]
if {[keylget traffic_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

#################################
# Reset Ethernet OAM statistics #
#################################

puts "\nReseting Ethernet OAM statistics"
set stat_status [::ixia::emulation_efm_stat \
        -api_used    ixprotocol             \
        -port_handle $port_0                \
        -action      reset                  \
        ]
if {[keylget stat_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stat_status log]"
    return 0
}

set stat_status [::ixia::emulation_efm_stat \
        -api_used    ixprotocol             \
        -port_handle $port_1                \
        -action      reset                  \
        ]
if {[keylget stat_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stat_status log]"
    return 0
}

######################
# Start Ethernet OAM #
######################

puts "\nStarting Ethernet OAM"
set control_status [::ixia::emulation_efm_control \
        -api_used    ixprotocol                   \
        -port_handle $port_handle                 \
        -action      start                        \
        ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}

####################################
#  Configure triggers and filters  #
####################################

set config_status [::ixia::packet_config_buffers \
	-port_handle  $port_1              	         \
	-capture_mode continuous                     \
	]
if {[keylget config_status status] != $::SUCCESS} {
    return 0 "FAIL - $test_name - [keylget config_status log]"
}

#########################
# Start capture on port #
#########################

puts "Starting capture.."

set start_status [::ixia::packet_control \
        -port_handle $port_1             \
        -action      start		         \
	   ]
if {[keylget start_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget start_status log]"
    return 0
}

puts "Capturing...."

#################
# Start Traffic #
#################

puts "\nStarting Traffic"
set traffic_start_status [ixia::traffic_control	\
        -port_handle $port_0                    \
        -action      run                        ]
if {[keylget traffic_start_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_start_status log]"
    return 0
}

################
# Stop Traffic #
################

puts "\nStopping Traffic"
set traffic_start_status [ixia::traffic_control	\
        -port_handle $port_0                  \
        -action      stop                        ]
if {[keylget traffic_start_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_start_status log]"
    return 0
}

#########################
# Stop capture on port  #
#########################

puts "Stopping capture..."

set stop_status [::ixia::packet_control  \
       -port_handle $port_1              \
	   -action      stop		         \
	]
if {[keylget stop_status status] != $::SUCCESS} {
    return 0 "FAIL - $test_name - [keylget stop_status log]"
}

#########################################
# Get and print Ethernet OAM statistics #
#########################################

set retry_count 10
for {set retry_iteration 0} {$retry_iteration < $retry_count} {incr retry_iteration} {
    puts "\nRetry iteration $retry_iteration - port $port_1"
    set pass_break 1
    set stat_status2 [::ixia::emulation_efm_stat \
            -api_used    ixprotocol              \
            -port_handle $port_0                 \
            -action      get                     ]
    if {[keylget stat_status2 status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget stat_status2 log]"
        return 0
    }
    printStats $stat_status2
    
    if {[keylget stat_status2 statistics.oam_mode] != "passive"} {
        set errMsg "FAIL - $test_name - OAM Mode error.\nExpected: passive\
                \nActual:[keylget stat_status2 statistics.oam_mode]"
        set pass_break 0
    }
    if {[keylget stat_status2 statistics.link_events_enabled] != "Supported"} {
        set errMsg "FAIL - $test_name - Link Events error.\nExpected: Supported\
                \nActual:[keylget stat_status2 statistics.link_events_enabled]"
        set pass_break 0
    }
    if {[keylget stat_status2 statistics.variable_retrieval_enabled] != "Supported"} {
        set errMsg "FAIL - $test_name - Variable Retrieval error.\nExpected: Supported\
                \nActual:[keylget stat_status2 statistics.variable_retrieval_enabled]"
        set pass_break 0
    }
    
    if {$pass_break} {
        break
    }
    after 5000
}

if {!$pass_break} {
    puts $errMsg
    return 0
}

######################
# Stop Ethernet OAM  #
######################

puts "\nStopping Ethernet OAM"
set control_status [::ixia::emulation_efm_control \
        -api_used    ixprotocol             \
        -port_handle $port_handle           \
        -action      stop                   ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
