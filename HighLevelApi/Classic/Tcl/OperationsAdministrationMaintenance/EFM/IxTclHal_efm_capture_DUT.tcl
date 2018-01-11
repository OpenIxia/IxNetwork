################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mircea Hasegan $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    7-17-2008 Mircea Hasegan
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
#    This sample configures Ethernet OAM on the Ixia port.                     #
#    Ixia port is connected to Cisco 7200 Router.                              #
#    Traffic with bad CRC is sent from the Ixia Port.                          #
#    EFM is started on the Ixia port and statistics are collected.             #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# DUT configuration:                                                           #
#
#     configure terminal
#      interface gigabitEthernet 0/2
#       no shutdown
#       ethernet oam
#       ethernet oam mode active
#       ethernet oam link-monitor supported
#       ethernet oam link-monitor on
#      exit
#     end
#  
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list 7/3
set sess_count 20

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

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username  ixiaApiUser      ]
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

puts "Ixia port handles are $port_handle "

set interface_status [::ixia::interface_config \
        -port_handle      $port_0     \
        -mode             config               \
        -speed            auto                 \
        -duplex           auto                 \
        -phy_mode         copper               \
        -autonegotiation  1                    \
        -port_rx_mode     capture              ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

##################################################
# Remove all streams, including Ethernet OAMPDUs #
##################################################

set traffic_status [ixia::traffic_config \
        -mode        reset               \
        -port_handle $port_0             ]

if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

###########################################
# Configure first stream on the IpV4 port #
###########################################

puts "\nConfiguring Ethernet OAM and traffic streams"
set traffic_status [ixia::traffic_config         \
        -mode         create                     \
        -port_handle  $port_0                    \
        -l3_protocol  ipv4                       \
        -l3_length    64                         \
        -rate_percent 100                        \
        -mac_dst_mode discovery                  \
        -fcs          1                          \
        -fcs_type     bad_CRC                    ]
if {[keylget traffic_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

#######################################################
# Configure Ethernet OAM port and Information  OAMPDU #
#######################################################

set efm_status [::ixia::emulation_efm_config    \
        -port_handle $port_0                    \
        -link_events                            \
        -variable_retrieval                     \
        -size                           1500    \
    ]
if {[keylget efm_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget efm_status log]"
    return
}

set information_stream_id           [keylget efm_status information_oampdu_id]

#################################
# Reset Ethernet OAM statistics #
#################################

puts "\nReseting Ethernet OAM statistics"
set stat_status [::ixia::emulation_efm_stat \
        -port_handle $port_0           \
        -action      reset                   ]
if {[keylget stat_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stat_status log]"
    return
}

######################
# Start Ethernet OAM #
######################

puts "\nStarting Ethernet OAM"
set control_status [::ixia::emulation_efm_control \
        -port_handle $port_0                      \
        -action      start                        ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return
}

####################################
#  Configure triggers and filters  #
####################################

set config_status [::ixia::packet_config_buffers \
	-port_handle  $port_0              	         \
	-capture_mode continuous                     \
	]
if {[keylget config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget config_status log]"
}

#########################
# Start capture on port #
#########################

puts "Starting capture.."

set start_status [::ixia::packet_control \
       -port_handle $port_0              \
	   -action      start		         \
	]
if {[keylget start_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget start_status log]"
    return
}

puts "Capturing...."

#################
# Start Traffic #
#################

puts "\nStarting Traffic"
set traffic_start_status [ixia::traffic_control	\
        -port_handle $port_0                  \
        -action      run                        ]
if {[keylget traffic_start_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_start_status log]"
    return
}

after 10000

################
# Stop Traffic #
################

puts "\nStopping Traffic"
set traffic_start_status [ixia::traffic_control	\
        -port_handle $port_0                  \
        -action      stop                        ]
if {[keylget traffic_start_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_start_status log]"
    return
}

#########################
# Stop capture on port  #
#########################

puts "Stopping capture..."

set stop_status [::ixia::packet_control  \
       -port_handle $port_0              \
	   -action      stop		         \
	]
if {[keylget stop_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget stop_status log]"
}


##############################################################
# Get and print Ethernet OAM statistics while OAM is running #
##############################################################

set stat_status2 [::ixia::emulation_efm_stat \
        -port_handle $port_0                 \
        -action      get                     ]
if {[keylget stat_status2 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stat_status2 log]"
    return
}
printStats $stat_status2

if {[keylget stat_status2 statistics.oam_mode] != "Active"} {
    puts "FAIL - $test_name - OAM Mode error.\nExpected: Active\
            \nActual: [keylget stat_status2 statistics.oam_mode]"
    return
}
if {[keylget stat_status2 statistics.link_events_enabled] != "Supported"} {
    puts "FAIL - $test_name - Link Events error.\nExpected: Supported\
            \nActual: [keylget stat_status2 statistics.link_events_enabled]"
    return
}

######################
# Stop Ethernet OAM  #
######################

puts "\nStopping Ethernet OAM"
set control_status [::ixia::emulation_efm_control \
        -port_handle $port_handle           \
        -action      stop                   ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
