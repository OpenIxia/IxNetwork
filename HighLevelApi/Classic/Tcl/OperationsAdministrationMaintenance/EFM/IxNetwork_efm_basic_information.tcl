################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mircea Hasegan $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    7-17-2008 Mircea Hasegan
#    3-17-2009 Adrian Iliesiu
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
#    This sample creates a BACK-TO-BACK setup.                                 #
#                                                                              #
#    It configures two IPv4 Ethernet interfaces and configures Ethernet OAM    #
#    adding one Information OAMPDU on each port.                               #
#    Ethernet OAM is started and statistics are gathered.                      #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 1/1 1/2]

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

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect                         \
        -reset                                              \
        -ixnetwork_tcl_server   localhost                   \
        -device                 $chassisIP                  \
        -port_list              $port_list                  \
        -username               ixiaApiUser                 ]
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

puts "Ixia port handles are $port_handle "

########################################
# L1 configurations                    #
########################################
set interface_status [::ixia::interface_config \
        -port_handle      $port_0     \
        -mode             config               \
        -speed            auto                 \
        -duplex           auto                 \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

set interface_status [::ixia::interface_config \
        -port_handle      $port_1     \
        -mode             config               \
        -speed            auto                 \
        -duplex           auto                 \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

######################################################
# Configure Ethernet OAM port and Information OAMPDU #
######################################################

puts "\nConfiguring Ethernet OAM"
set efm_status [::ixia::emulation_efm_config    \
        -port_handle $port_0                    \
        -oam_mode    active                     \
        -link_events                            \
        -variable_retrieval                     \
    ]
if {[keylget efm_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget efm_status log]"
    return
}

set efm_status [::ixia::emulation_efm_config    \
        -port_handle $port_1                    \
        -oam_mode    passive                    \
        -link_events                            \
        -variable_retrieval                     \
        ]
if {[keylget efm_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget efm_status log]"
    return
}

######################
# Start Ethernet OAM #
######################

puts "\nStarting Ethernet OAM"
set control_status [::ixia::emulation_efm_control \
        -port_handle $port_handle           \
        -action      start                  ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return
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
            -port_handle $port_0           \
            -action      get                    ]
    if {[keylget stat_status1 status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget stat_status1 log]"
        return
    }
    
    printStats $stat_status1
    
    if {[keylget stat_status1 statistics.oam_mode] != "Passive"} {
        set errMsg "FAIL - $test_name - OAM Mode error.\nExpected: Passive\
                \nActual:[keylget stat_status1 statistics.oam_mode]"
        set pass_break 0
    }
    if {[keylget stat_status1 statistics.link_events_enabled] != "Supported"} {
        set errMsg "FAIL - $test_name - Link Events error.\nExpected: Supported\
                \nActual:[keylget stat_status1 statistics.link_events_enabled]"
        set pass_break 0
    }
    if {[keylget stat_status1 statistics.variable_retrieval_enabled] != "Supported"} {
        set errMsg "FAIL - $test_name - Variable Retrieval error.\nExpected: Supported\
                \nActual:[keylget stat_status1 statistics.variable_retrieval_enabled]"
        set pass_break 0
    }
    
    if {$pass_break} {
        break
    }
}

if {!$pass_break} {
    puts $errMsg
    return
}

set retry_count 5
for {set retry_iteration 0} {$retry_iteration < $retry_count} {incr retry_iteration} {
    puts "\nRetry iteration $retry_iteration - port $port_1"
    set pass_break 1
    set stat_status2 [::ixia::emulation_efm_stat \
            -port_handle $port_1           \
            -action      get                    ]
    if {[keylget stat_status2 status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget stat_status2 log]"
        return
    }
    printStats $stat_status2
    
    if {[keylget stat_status2 statistics.oam_mode] != "Active"} {
        set errMsg "FAIL - $test_name - OAM Mode error.\nExpected: Active\
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

}

if {!$pass_break} {
    puts $errMsg
    return
}

########################
# Start Sending OAMPDU #
########################

puts "\nStarting Traffic"
set traffic_start_status [ixia::emulation_efm_control	\
        -port_handle $port_handle               \
        -action      start_event                        ]
if {[keylget traffic_start_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_start_status log]"
    return
}

after 10000

########################
# Stop Sending OAMPDU  #
########################

puts "\Stopping Traffic"
set traffic_stop_status [ixia::emulation_efm_control	\
        -port_handle $port_handle               \
        -action      stop_event                       ]
if {[keylget traffic_stop_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_stop_status log]"
    return
}

##############################################################
# Get and print Ethernet OAM statistics after OAM stopped    #
##############################################################

set stat_status1 [::ixia::emulation_efm_stat \
        -port_handle $port_0           \
        -action      get                    ]
if {[keylget stat_status1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stat_status1 log]"
    return
}

printStats $stat_status1

if {[keylget stat_status1 statistics.oampdu_count.information_rx] <= 0} {
    puts "FAIL - $test_name - EOAM Information PDUs Received count is 0."
    return
}

set stat_status2 [::ixia::emulation_efm_stat \
        -port_handle $port_1           \
        -action      get                    ]
if {[keylget stat_status2 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stat_status2 log]"
    return
}
printStats $stat_status2

if {[keylget stat_status2 statistics.oampdu_count.information_rx] <= 0} {
    puts "FAIL - $test_name - EOAM Information PDUs Received count is 0."
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
