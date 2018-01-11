#################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    04-11-2013 Mchakravarthy - created sample
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
#    This sample connects to IxNetwork Tcl Server and loads the IxNetwork      #
#    config file with traffic configured.                                      #
#    The stats is calculated using mode aggregate and with measure mode        #
#    instantaneous and cumulative                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################
################################################################################
# Loaading Ixia package                                                        #
################################################################################

# Loading Ixia package

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}
################################################################################
# General script variables
################################################################################
set chassis_ip              {10.206.27.55}
set port_list               [list 8/1 8/2]
set tcl_server              localhost
set ixnetwork_tcl_server    localhost
set test_name               [info script]
set test_name_folder        [file dirname $test_name]
set ixn_cfg                 [file join $test_name_folder check_aggregate.ixncfg]
puts "ixn_cfg: $ixn_cfg"

################################################################################
# START - Connect to the chassis and Load IxNetwork config
################################################################################

set res [ixia::connect                              \
    -config_file $ixn_cfg                           \
    -ixnetwork_tcl_server $ixnetwork_tcl_server     \
    -tcl_server $tcl_server                         \
    -device $chassis_ip                             \
    -master_device $chassis_ip                      \
    -port_list $port_list                           \
]
if {[keylget res status] != $::SUCCESS} {
    error "connect failed: $res"
}

set ti_list [list]
foreach ti_name [keylget res traffic_config] {
    lappend ti_list [keylget res ${ti_name}.traffic_config.traffic_item]
}

set vport_list [keylget res vport_list]
set vp0 [lindex $vport_list 0]
set vp1 [lindex $vport_list 1]
after 10000
################################################################################
# START Traffic
################################################################################

set frame_rate [ixNet getA ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/frameRate -rate]
set frame_rate2 [expr $frame_rate*2]
set frame_rate8 [expr $frame_rate*8]

set res [ixia::test_control -action start_all_protocols]
if {[keylget res status] != $::SUCCESS} {
    error "test_control failed: $res"
}

set res [ixia::traffic_control          \
    -action run                         \
    -instantaneous_stats_enable 1       \
    -traffic_generator ixnetwork_540    \
    -handle $ti_list                    \
]
if {[keylget res status] != $::SUCCESS} {
    error "traffic_control run failed: $res"
}

set wait 10
puts "waiting for ${wait}s"
after [expr 1000 * $wait]

################################################################################
# Collect traffic stats
################################################################################

for {set try 0} {$try < 30} {incr try} {
    set res_instantaneous [ixia::traffic_stats  \
        -mode aggregate                         \
        -measure_mode instantaneous             \
    ]
    if {[keylget res_instantaneous status] != $::SUCCESS} {
        error "traffic_stats run failed: $res"
    }
    if {![keylget res_instantaneous waiting_for_stats]} {
        break
    }
    after 1000
}

for {set try 0} {$try < 30} {incr try} {
    set res_cumulative [ixia::traffic_stats     \
        -mode aggregate                         \
        -measure_mode cumulative                \
    ]
    if {[keylget res_cumulative status] != $::SUCCESS} {
        error "traffic_stats run failed: $res"
    }
    if {![keylget res_cumulative waiting_for_stats]} {
        break
    }
    after 1000
}

################################################################################
# Stop the traffic
################################################################################

set res [ixia::traffic_control          \
    -action stop                        \
    -traffic_generator ixnetwork_540    \
    -max_wait_timer 120	
    -handle $ti_list                    \
]
if {[keylget res status] != $::SUCCESS} {
    error "traffic_control stop failed: $res"
}

puts "SUCCESS - [clock format [clock seconds] -format {%D %X}]"
return 1
