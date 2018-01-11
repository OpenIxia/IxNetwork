################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-20-2007 Mchakravarthy - created sample
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
#   This sample resumes session by loading IxNetwork Config and runs the 	   #
#   traffic and validates the stats									           #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
# General script variables
################################################################################
set test_name                                   [info script]
set cfgError									0
set chassis_ip									10.205.16.54
set port_list									[list 2/5 2/6]
set break_locks									1
set tcl_server									127.0.0.1
set ixnetwork_tcl_server						127.0.0.1
set port_count									2
set detailed_logging							0
set interactive									1
set test_name_folder							[file dirname $test_name]
set ixn_cfg										[file join $test_name_folder test.09.ixncfg]
################################################################################
# START - Connect to the chassis
################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect

puts "Resume session using $ixn_cfg on  ixnetwork tcl server $ixnetwork_tcl_server ..."
update idletasks

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect                                            \
            -mode                 connect                                      \
            -config_file          $ixn_cfg                                     \
            -device               $chassis_ip                                  \
            -port_list            $port_list                                   \
            -tcl_server           $tcl_server                                  \
            -ixnetwork_tcl_server $ixnetwork_tcl_server                        \
            -break_locks          $break_locks                                 \
            -interactive          $interactive                                 \
            ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

# Getting the port handles
set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
            temp_port]} {
        lappend port_handle $temp_port
    }
}
set port_0 [lindex $port_handle 0]
set port_1 [lindex $port_handle 1]

puts "Ixia port handles are: $port_0, $port_1"
update idletasks

################################################################################
# Getting Handles
################################################################################
set traffic_handles [keylget connect_status traffic_config]
set traffic_item_1 [keylget connect_status [lindex $traffic_handles 0].traffic_config.traffic_item]
set traffic_item_2 [keylget connect_status [lindex $traffic_handles 1].traffic_config.traffic_item]

################################################################################
# Start traffic
################################################################################
puts "Starting traffic..."
set traffic_status [::ixia::traffic_control    \
        -action              run               \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

puts "Running traffic for 5 seconds ..."
update idletasks

after 5000

################################################################################
# FD Show Egress Flows
################################################################################
set tracking_value 7
set flow_traffic_status [::ixia::traffic_stats                                          \
        -mode                           user_defined_stats                              \
        -traffic_generator              ixnetwork_540                                   \
        -uds_type                       l23_traffic_flow_detective                      \
        -uds_action                     get_stats                                       \
        -uds_tracking_filter            "Ethernet:Outer VLAN ID (4 bits) at offset 124" \
        -uds_tracking_filter_count      1                                               \
        -uds_l23tfd_tracking_operator   is_equal                                        \
        -uds_l23tfd_tracking_value      $tracking_value                                 \
        -uds_l23tfd_show_egress_flows   1                                               \
        ]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return 0
}


################################################################################
# Stop traffic
################################################################################
puts "Stopping traffic ..."
set traffic_status [::ixia::traffic_control   \
        -action             stop              \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

# Check if Outer VLAN Priority statistic exists

set check_param "Ethernet:Outer VLAN Priority (3 bits) at offset 112"
if {[catch {keylget flow_traffic_status 1.$check_param} catch_err]} {
    puts "FAIL - $test_name - The \"$check_param\" key does not exist"
    return 0
}

# Check if Outer VLAN ID statistic exists, and if Outer VLAN ID is 7 for every flow

set check_param "Ethernet:Outer VLAN ID (4 bits) at offset 124"
foreach item [keylkeys flow_traffic_status] {
    # Check if the key is a number or not
    if {[string is double -strict $item]} {
        if {[catch {keylget flow_traffic_status ${item}.${check_param}} catch_err]} {
            puts "FAIL - $test_name - The \"$check_param\" key does not exist"
            return 0
        } elseif {$catch_err!=$tracking_value} {
            puts "FAIL - $test_name - The flow $item has the statistic \"$check_param\" \
                    with a value of $catch_err, and it should be $tracking_value"
            return 0
        }
    }
}

################################################################################
# Print Stats
################################################################################

puts [::ixia::keylprint flow_traffic_status]

update idletasks

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
