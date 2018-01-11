################################################################################
# Version 1.0    $Revision: 1 $
# $Author: MHasegan $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    11-22-2008 Mircea Hasegan
#
# Description:
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
#    This sample uses all modes accepted by -mode argument for                 #
#    ::ixia::emulation_rsvp_config procedure.                                  #
#        -create 10 RSVP neighbor pairs                                        #
#        -deletes last RSVP neighbor                                           #
#        -modify 9 RSVP neighbors                                              #
#        -diable the first four neighbors                                      #
#        -enable the first two neighbors                                       #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a STXS4 module.                                  #
#                                                                              #
################################################################################

package require Ixia

set test_name               [info script]

################################################################################
# START - Connect to the chassis
################################################################################
set chassis_ip              sylvester
set port_list               [list 2/3]

# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                        \
        -reset                                                             \
        -device               $chassis_ip                                  \
        -port_list            $port_list                                   \
        -break_locks          1                                            \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
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
    incr i
}

################################################################################
# END - Connect to the chassis
################################################################################

set interface_status [::ixia::interface_config                             \
        -port_handle      $port_0                                          \
        -mode             config                                           \
        -intf_mode        ethernet                                         \
        -autonegotiation  1                                                \
        -speed            ether100                                         \
        -duplex           auto                                             \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Create 10 RSVP routers
################################################################################
puts "\nCreate 10 RSVP routers"

set rsvp_config_status [::ixia::emulation_rsvp_config                \
        -mode                            create                      \
        -count                           10                          \
        -intf_ip_addr                    1.1.1.1                     \
        -intf_ip_addr_step               0.0.1.0                     \
        -intf_prefix_length              24                          \
        -ip_version                      4                           \
        -mac_address_init                1101.2233.0001              \
        -mac_address_step                0000.0000.0001              \
        -neighbor_intf_ip_addr           111.111.111.1               \
        -neighbor_intf_ip_addr_step      0.0.1.0                     \
        -port_handle                     $port_0                     \
        -vlan                            0                           \
        -actual_restart_time             15000                       \
        -egress_label_mode               exnull                      \
        -graceful_restart                1                           \
        -graceful_restart_recovery_time  33333                       \
        -graceful_restart_restart_time   5555                        \
        -graceful_restart_start_time     33333                       \
        -graceful_restart_up_time        33333                       \
        -graceful_restarts_count         3                           \
        -max_label_value                 5000                        \
        -min_label_value                 4000                        \
        -path_state_refresh_timeout      33333                       \
        -path_state_timeout_count        5                           \
        -hello_tlvs                      "22,1,aa:22,2,bb"           \
        -reset                                                       \
    ]

if {[keylget rsvp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_config_status log]"
}

set rsvpHandleList [keylget rsvp_config_status handles]
foreach rsvpRouter $rsvpHandleList {
    puts "RSVP Router $rsvpRouter Interface Handle:"
    foreach routerInterface [keylget rsvp_config_status router_interface_handle.$rsvpRouter] {
        puts "\t$routerInterface\n"
    }
}

################################################################################
# Delete an RSVP router
################################################################################
puts "\nDelete an RSVP router"

set rsvp_config_status [::ixia::emulation_rsvp_config                           \
        -mode                            delete                                 \
        -handle                          [lindex $rsvpHandleList end]           \
    ]
if {[keylget rsvp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_config_status log]"
}

# Remove the handle from the handle list
set rsvpHandleList [lreplace $rsvpHandleList end end]


################################################################################
# Modify all RSVP routers
################################################################################
puts "\nModify all RSVP routers"

set intf_ip_addr               [list 7.7.7.7  7.7.8.7  7.7.9.7  7.7.10.7 \
                                     7.7.11.7 7.7.12.7 7.7.13.7 7.7.14.7 \
                                     7.7.15.7                            ]
set neighbor_intf_ip_addr      [list 7.7.7.1  7.7.8.1  7.7.9.1  7.7.10.1 \
                                     7.7.11.1 7.7.12.1 7.7.13.1 7.7.14.1 \
                                     7.7.15.1                            ]
set hello_tlvs                 [list 22,1,11:22,2,22 23,1,33:23,2,44 \
                                     24,1,55:24,2,66 25,1,77:25,2,88 \
                                     26,1,99:26,2,aa 27,1,bb:27,2,cc \
                                     28,1,dd:28,2,ee 29,1,ff:29,2,ff \
                                     30,1,00:30,2,11                 ]
set record_route               [list 1 0 1 0 1 0 1 0 1]
set refresh_reduction          [list 0 1 0 1 0 1 0 1 0]

set rsvp_config_status [::ixia::emulation_rsvp_config           \
        -mode                            modify                 \
        -handle                          $rsvpHandleList        \
        -intf_ip_addr                    $intf_ip_addr          \
        -intf_prefix_length              24                     \
        -ip_version                      4                      \
        -neighbor_intf_ip_addr           $neighbor_intf_ip_addr \
        -enable_bgp_over_lsp             0                      \
        -graceful_restart                0                      \
        -hello_interval                  55                     \
        -hello_msgs                      1                      \
        -hello_retry_count               5                      \
        -hello_tlvs                      $hello_tlvs            \
        -record_route                    $record_route          \
        -refresh_interval                33                     \
        -refresh_reduction               $refresh_reduction     \
    ]
if {[keylget rsvp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_config_status log]"
}


################################################################################
# Disable first four routers
################################################################################
puts "\nDisable first four routers"

set rsvp_config_status [::ixia::emulation_rsvp_config                           \
        -mode                            disable                                \
        -handle                          [lrange $rsvpHandleList 0 3]           \
    ]
if {[keylget rsvp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_config_status log]"
}

################################################################################
# Enable first two routers
################################################################################
puts "\nEnable first two routers"

set rsvp_config_status [::ixia::emulation_rsvp_config                           \
        -mode                            enable                                 \
        -handle                          [lrange $rsvpHandleList 0 1]           \
    ]
if {[keylget rsvp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_config_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
