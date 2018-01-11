################################################################################
# Version 1.0    $Revision: 1 $
# $Author: $
#
#    Copyright © 1997 - 2010 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#
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
# Description: Configures FC Fport and FC Client Port, one - one mode, control #
#              in sync mode and get aggregate stats                            #
# This sample was tested with a N HLTSET type.                                 #
#                                                                              #
################################################################################


package require Ixia

set test_name               [info script]
set chassis_ip              10.200.102.13
set port_list               [list 1/3 1/4]
set ixnetwork_tcl_server    localhost
set break_locks             1
set cfgErrors               0
set interactive             1

set flogi_name              FLOGI-NAME
set fdisc_name              FDISC-NAME
set vnport_flogi_name       N_PORT-FLOGI
set vnport_fdisc_name       N_PORT-FDISC
set fdisc_number            1

#========================== CONNECT TO PORT ON CHASSIS ========================#
puts "Connect chassis ..."
set connect_status [::ixia::connect\
        -reset \
        -device $chassis_ip\
        -port_list $port_list\
        -mode connect\
        -break_locks $break_locks\
        -interactive $interactive\
        -ixnetwork_tcl_server $ixnetwork_tcl_server]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}
#==================== ASSIGN PORT HANDLE FOR CLIENT AND FPORT=================#
set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}
set fc_client_port_handle [lindex $port_handle 0]
set fc_fport_port_handle [lindex $port_handle 1]

#================================ ADD FPORT ==================================#
puts "Adding F-PORT ..."
set fc_fport_add [::ixia::fc_fport_config\
        -mode add\
        -port_handle $fc_fport_port_handle]
if {[keylget fc_fport_add status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget fc_fport_add log]"
    return 0
}
set fc_fport_handle [keylget fc_fport_add handle]

#========================== ADD CLIENT =======================================#
puts "Adding client ..."
set fc_client_add [::ixia::fc_client_config\
        -mode add\
        -fdisc_enabled       1\
        -port_handle         $fc_client_port_handle\
        -flogi_plogi_enabled 1\
        -fdisc_plogi_enabled 1\
        -fdisc_name          $fdisc_name\
        -flogi_name          $flogi_name\
]
if {[keylget fc_client_add status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget fc_client_add log]"
    return 0
}
set fc_client_handle [keylget fc_client_add handle]

#========================== ADD VNPORT =======================================#
puts "Adding vnport ..."
set fc_fport_vnport_add [::ixia::fc_fport_vnport_config\
        -mode           add\
        -handle         $fc_fport_handle\
        -count          [expr $fdisc_number + 1]
]
if {[keylget fc_fport_vnport_add status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget fc_fport_vnport_add log]"
    return 0
}
set fc_fport_vnport_handle [keylget fc_fport_vnport_add handle]

#========================== ADD VNPORT FOR FLOGI =============================#
set fc_fport_vnport_flogi_add [::ixia::fc_fport_vnport_config \
        -mode               add \
        -handle             $fc_fport_handle\
        -name               $vnport_flogi_name\
        -simulated          1\
        -plogi_enable       1\
        -plogi_target_name  $flogi_name\
        -count              1]
if {[keylget fc_fport_vnport_flogi_add status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget fc_fport_vnport_flogi_add log]"
    return 0
}
set fc_fport_vnport_flogi_handle [keylget fc_fport_vnport_flogi_add handle]

#========================== ADD VNPORT FOR FDISC==============================#
set fc_fport_vnport_fdisc_add [::ixia::fc_fport_vnport_config\
        -mode               add\
        -handle             $fc_fport_handle\
        -name               $vnport_fdisc_name\
        -simulated          1\
        -plogi_enable       1\
        -plogi_target_name  $fdisc_name\
        -count              $fdisc_number\
]
if {[keylget fc_fport_vnport_fdisc_add status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget fc_fport_vnport_fdisc_add log]"
    return 0
}
set fc_fport_vnport_fdisc_handle [keylget fc_fport_vnport_fdisc_add handle]

#========================= CONFIG CLIENT TO PLOGI TO FPORT ===================#
puts "Config client ..."
set fc_client_modify [::ixia::fc_client_config -mode modify -handle $fc_client_handle\
        -fdisc_count             $fdisc_number\
        -flogi_plogi_target_name $vnport_flogi_name\
        -fdisc_plogi_target_name $vnport_fdisc_name\
                     ]
if {[keylget fc_client_modify status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget fc_client_modify log]"
    return 0
}
#===========================START SESSION IN SYNC MODE=======================#
puts "Start session with sync mode ..."
set control_status [::ixia::fc_control\
        -action start\
        -port_handle [list $fc_fport_port_handle $fc_client_port_handle ]]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}
after 7000
#===============================GET AGGREGATE STATISTICS=======================#
puts "Getting aggregate statistics ..."
set stats_aggregate_fport [::ixia::fc_fport_stats\
        -mode aggregate\
        -port_handle $fc_fport_port_handle]

if {[keylget stats_aggregate_fport status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stats_aggregate_fport log]"
    return 0
}
set stats_aggregate_client [::ixia::fc_client_stats\
        -mode aggregate\
        -port_handle $fc_client_port_handle]

if {[keylget stats_aggregate_client status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stats_aggregate_client log]"
    return 0
}
set flogi_ls_acc_tx_fport [keylget stats_aggregate_fport $fc_fport_port_handle.aggregate.flogi_ls_acc_tx]
set fdisc_ls_acc_tx_fport [keylget stats_aggregate_fport $fc_fport_port_handle.aggregate.fdisc_ls_acc_tx]
set plogi_ls_acc_tx_fport [keylget stats_aggregate_fport $fc_fport_port_handle.aggregate.plogi_ls_acc_tx]
set flogi_ls_acc_rx_client [keylget stats_aggregate_client $fc_client_port_handle.aggregate.flogi_ls_acc_rx]
set fdisc_ls_acc_rx_client [keylget stats_aggregate_client $fc_client_port_handle.aggregate.fdisc_ls_acc_rx]
set plogi_ls_acc_rx_client [keylget stats_aggregate_client $fc_client_port_handle.aggregate.plogi_ls_acc_rx]
puts "fport flogi accept tx : $flogi_ls_acc_tx_fport"
puts "fport fdisc accept tx : $fdisc_ls_acc_tx_fport"
puts "fport plogi accept tx : $plogi_ls_acc_tx_fport"
puts "client flogi accept rx : $flogi_ls_acc_rx_client"
puts "client fdisc accept rx : $fdisc_ls_acc_rx_client"
puts "client plogi accept rx : $plogi_ls_acc_rx_client"

return "SUCCESS - [info script] - [clock format [clock seconds]]"