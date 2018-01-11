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
#   This sample configures FCoE on ther ports and validates the stats          #
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
set chassis_ip									10.205.16.54
set port_list									[list 1/1 1/2]
set break_locks									1
set tcl_server									127.0.0.1
set port_count									2
set ixnetwork_tcl_server						localhost
set cfgErrors									0
set interactive									1

set flogi_name									FLOGI-NAME
set fdisc_name									FDISC-NAME
set vnport_flogi_name							N_PORT-FLOGI
set vnport_fdisc_name							N_PORT-FDISC
set fdisc_number								255

################################################################################
# START - Connect to the chassis
################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect

################################################################################
#========================== CONNECT TO PORT ON CHASSIS ========================#
################################################################################

puts "Connect chassis ..."
set connect_status [::ixia::connect                     \
        -reset                                          \
        -device                 $chassis_ip             \
        -port_list              $port_list              \
        -mode                   connect                 \
        -break_locks            $break_locks            \
        -interactive            $interactive            \
        -ixnetwork_tcl_server   $ixnetwork_tcl_server   ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

################################################################################
#==================== ASSIGN PORT HANDLE FOR CLIENT AND FPORT==================#
################################################################################

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}
set fc_client_port_handle [lindex $port_handle 0]
set fc_fport_port_handle [lindex $port_handle 1]

################################################################################
#================================ ADD FPORT ===================================#
################################################################################

puts "Adding F-PORT ..."
set fc_fport_add [::ixia::fc_fport_config       \
        -mode           add                     \
        -port_handle    $fc_fport_port_handle   ]
if {[keylget fc_fport_add status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget fc_fport_add log]"
    return 0
}
set fc_fport_handle [keylget fc_fport_add handle]

################################################################################
#========================== ADD CLIENT ========================================#
################################################################################

puts "Adding client ..."
set fc_client_add [::ixia::fc_client_config             \
        -mode                   add                     \
        -fdisc_enabled          1                       \
        -port_handle            $fc_client_port_handle  \
        -flogi_plogi_enabled    1                       \
        -fdisc_plogi_enabled    1                       \
        -fdisc_name             $fdisc_name             \
        -flogi_name             $flogi_name             \
]
if {[keylget fc_client_add status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget fc_client_add log]"
    return 0
}
set fc_client_handle [keylget fc_client_add handle]

################################################################################
#========================== ADD VNPORT ========================================#
################################################################################

puts "Adding vnport ..."
set fc_fport_vnport_add [::ixia::fc_fport_vnport_config \
        -mode           add                             \
        -handle         $fc_fport_handle                \
        -count          [expr $fdisc_number + 1]
]
if {[keylget fc_fport_vnport_add status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget fc_fport_vnport_add log]"
    return 0
}
set fc_fport_vnport_handle [keylget fc_fport_vnport_add handle]

################################################################################
#========================== ADD VNPORT FOR FLOGI ==============================#
################################################################################

set fc_fport_vnport_flogi_add [::ixia::fc_fport_vnport_config   \
        -mode               add                                 \
        -handle             $fc_fport_handle                    \
        -name               $vnport_flogi_name                  \
        -simulated          1                                   \
        -plogi_enable       1                                   \
        -plogi_target_name  $flogi_name                         \
        -count              1                                   ]
if {[keylget fc_fport_vnport_flogi_add status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget fc_fport_vnport_flogi_add log]"
    return 0
}
set fc_fport_vnport_flogi_handle [keylget fc_fport_vnport_flogi_add handle]

################################################################################
#========================== ADD VNPORT FOR FDISC===============================#
################################################################################

set fc_fport_vnport_fdisc_add [::ixia::fc_fport_vnport_config   \
        -mode               add                                 \
        -handle             $fc_fport_handle                    \
        -name               $vnport_fdisc_name                  \
        -simulated          1                                   \
        -plogi_enable       1                                   \
        -plogi_target_name  $fdisc_name                         \
        -count              $fdisc_number                       \
]
if {[keylget fc_fport_vnport_fdisc_add status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget fc_fport_vnport_fdisc_add log]"
    return 0
}
set fc_fport_vnport_fdisc_handle [keylget fc_fport_vnport_fdisc_add handle]

################################################################################
#========================= CONFIG CLIENT TO PLOGI TO FPORT ====================#
################################################################################

puts "Config client ..."
set fc_client_modify [::ixia::fc_client_config -mode modify -handle $fc_client_handle   \
        -fdisc_count             $fdisc_number                                          \
        -flogi_plogi_target_name $vnport_flogi_name                                     \
        -fdisc_plogi_target_name $vnport_fdisc_name                                     \
                     ]
if {[keylget fc_client_modify status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget fc_client_modify log]"
    return 0
}
################################################################################
#===================== START F-PORT and CLIENT-PORT IN ASYNC MODE==============#
################################################################################

puts "Start session ..."
set control_status [::ixia::fc_control                                      \
        -action         start                                               \
        -action_mode    async                                               \
        -port_handle    [list $fc_fport_port_handle $fc_client_port_handle] ]
if {[keylget control_status status] == $::FAILURE} {
    puts "FAIL. Can not start Client Port"
    return 0
}
################################################################################
#======================== CHECK IS DONE COMMAND ===============================#
################################################################################

set i 0
set list_result [keylget control_status result]
set result_list [lindex $list_result 0]
set result [lindex $result_list 1]
while {$i < 200} {
    set check_control [::ixia::fc_control -action is_done -result $result]
    set log_mess [keylget check_control log]
    if {[keylget log_mess $result] != "false"} {
        after 6500
        puts "Status of Sessions : [keylget log_mess $result]"
        break
    }
    after 1000
    incr i
}
if {[keylget log_mess $result] == "false"} {
    puts "FAIL.The system get hang while starting the session"
    return 0
}

################################################################################
#================================ VERIFY ======================================#
#============================ For Client-Port =================================#
################################################################################

puts "Compare statistics for Client Port"
#Get value using High Level
set client_statistics_verify [::ixia::fc_client_stats   \
        -mode   aggregate                               \
        -handle $fc_client_handle
]
puts "Wait 3 seconds to get aggregate stats for client"
after 3000

set fc_client_aggregate_high(flogi_ls_acc_rx) [keylget client_statistics_verify $fc_client_port_handle.aggregate.flogi_ls_acc_rx]
set fc_client_aggregate_high(fdisc_ls_acc_rx) [keylget client_statistics_verify $fc_client_port_handle.aggregate.fdisc_ls_acc_rx]
set fc_client_aggregate_high(plogi_ls_acc_rx) [keylget client_statistics_verify $fc_client_port_handle.aggregate.plogi_ls_acc_rx]
set fc_client_aggregate_high(sessions_succeeded) [keylget client_statistics_verify $fc_client_port_handle.aggregate.sessions_succeeded]
#Create expected value array
set fc_client_aggregate_expected(flogi_ls_acc_rx) 1
set fc_client_aggregate_expected(fdisc_ls_acc_rx) 255
set fc_client_aggregate_expected(plogi_ls_acc_rx) 256
set fc_client_aggregate_expected(sessions_succeeded) 256
puts "Compare high-level values and expected values"
set cfgErrors [expr $cfgErrors + [::ixia::compare_obj_settings_array fc_client_aggregate_expected fc_client_aggregate_high]]

################################################################################
#============================ For F-Port ======================================#
################################################################################

puts "Compare statistics for F-Port"
#Get value using High Level
set fport_statistics_verify [::ixia::fc_fport_stats \
        -mode   aggregate                           \
        -handle $fc_fport_handle                    ]
puts "Wait 3 seconds to get stats of Fport"
after 3000
set fc_fport_aggregate_high(plogi_ls_acc_rx) [keylget fport_statistics_verify $fc_fport_port_handle.aggregate.plogi_ls_acc_rx]
set fc_fport_aggregate_high(fdisc_ls_acc_tx) [keylget fport_statistics_verify $fc_fport_port_handle.aggregate.fdisc_ls_acc_tx]
set fc_fport_aggregate_high(flogi_ls_acc_tx) [keylget fport_statistics_verify $fc_fport_port_handle.aggregate.flogi_ls_acc_tx]
set fc_fport_aggregate_high(nports_registered) [keylget fport_statistics_verify $fc_fport_port_handle.aggregate.nports_registered]
#Create expected value array
set fc_fport_aggregate_expected(plogi_ls_acc_rx) 256
set fc_fport_aggregate_expected(fdisc_ls_acc_tx) 255
set fc_fport_aggregate_expected(flogi_ls_acc_tx) 1
set fc_fport_aggregate_expected(nports_registered) 256
puts "Compare high-level values and expected values"
set cfgErrors [expr $cfgErrors + [::ixia::compare_obj_settings_array fc_fport_aggregate_expected fc_fport_aggregate_high]]

################################################################################
#===================== STOP F-PORT and CLIENT-PORT IN ASYNC MODE===============#
################################################################################

puts "Stop session ..."
set control_status [::ixia::fc_control                                  \
        -action         stop                                            \
        -action_mode    async                                           \
        -port_handle [list $fc_fport_port_handle $fc_client_port_handle]]
if {[keylget control_status status] == $::FAILURE} {
    puts "FAIL. Can not start Client Port"
    return 0
}

################################################################################
#================================== End Verify ================================#
################################################################################

puts "###############################"
if {$cfgErrors == 0} {
    puts "SUCCESS - $test_name - [clock format [clock seconds]]"
    return 1
} else {
    puts "FAIL - $test_name - [clock format [clock seconds]]"
    return 0
}