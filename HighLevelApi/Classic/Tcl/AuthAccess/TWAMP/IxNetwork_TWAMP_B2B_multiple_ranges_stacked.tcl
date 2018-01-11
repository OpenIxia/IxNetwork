################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Adrian Iliesiu $
#
#    Copyright © 1997 - 2009 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    3-16-2009 Adrian Iliesiu
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
#    This sample creates a BACK-TO-BACK setup.                                 #
#                                                                              #
#    It configures two IPv4 Ethernet interfaces with stacked VLANS and         #
#    configures TWAMP on each port. TWAMP is started and some statistics       #
#    are gathered.                                                             #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################
package require Ixia

set test_name               [info script]
set twamp_control_sessions  1
set twamp_test_sessions     1
set twamp_server_sessions   1

set chassis_ip              sylvester
set port_list               [list 1/1 1/2]

# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                            \
            -reset                                                             \
            -ixnetwork_tcl_server localhost                                    \
            -device               $chassis_ip                                  \
            -port_list            $port_list                                   \
            -username             ixiaApiUser                                  \ 
            ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
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

################################################################################
# END - Connect to the chassis
################################################################################

puts "Connect to the chassis complete."

################################################################################
# START - Interface configuration - L1
################################################################################
puts "Start interface configuration L1 ..."

foreach port $port_handle {
     set interface_status [::ixia::interface_config                             \
                -port_handle      $port                                         \
                -mode             config                                        \
                -intf_mode        ethernet                                      \
                -autonegotiation  1                                             \
                -speed            ether1000                                     \
                -duplex           auto                                          \
                -phy_mode         copper                                        \
                ]
      if {[keylget interface_status status] != $::SUCCESS} {
          puts "FAIL - $test_name - [keylget interface_status log]"
          return
         }
}

################################################################################
# END - Interface configuration - L1
################################################################################

puts "Layer 1 config complete."

################################################################################
# START - Interface configuration - L2, L3
################################################################################

set interface_config_handle_0_list [list]
set client_ip_list  [list 10.20.0.1 20.20.0.1 30.20.0.1]
set client_gateways [list 10.20.0.2 20.20.0.2 30.20.0.2]
# Configure L23 - IP Endpoint on first port:
      
set chassis                     [format %02x [lindex [split $port_0 "/"] 0]]
set card                        [format %02x [lindex [split $port_0 "/"] 1]]
set port                        [format %02x [lindex [split $port_0 "/"] 2]]

set interface_status [::ixia::interface_config                                  \
            -port_handle            [list $port_0 $port_0 $port_0]              \
            -mode                   modify                                      \
            -intf_mode              ethernet                                    \
            -src_mac_addr           00${chassis}.00${card}.${port}01            \
            -intf_ip_addr           $client_ip_list                             \
            -gateway                $client_gateways                            \
            -netmask                255.255.0.0                                 \
            -l23_config_type        static_endpoint                             \
            -vlan                   1                                           \
            -vlan_id                100,300                                     \
            -vlan_id_step           2,1                                         \
            -vlan_user_priority     0,1                                         \
            -addresses_per_vlan     1,1                                         \
            ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

foreach list_element [keylget interface_status interface_handle] {
    lappend interface_config_handle_0_list $list_element
}  

# Configure L23 - IP Endpoint on second port:
set interface_config_handle_1_list [list]
set server_ip_list   [list 10.20.0.2 20.20.0.2 30.20.0.2]
set server_gateways  [list 10.20.0.1 20.20.0.1 30.20.0.1]

set chassis                     [format %02x [lindex [split $port_1 "/"] 0]]
set card                        [format %02x [lindex [split $port_1 "/"] 1]]
set port                        [format %02x [lindex [split $port_1 "/"] 2]]

set interface_status [::ixia::interface_config                                  \
            -port_handle            [list $port_1 $port_1 $port_1]              \
            -mode                   modify                                      \
            -intf_mode              ethernet                                    \
            -src_mac_addr           00${chassis}.00${card}.${port}02            \
            -intf_ip_addr           $server_ip_list                             \
            -gateway                $server_gateways                            \
            -netmask                255.255.0.0                                 \
            -l23_config_type        static_endpoint                             \
            -vlan                   1                                           \
            -vlan_id                100,300                                     \
            -vlan_id_step           2,1                                         \
            -vlan_user_priority     0,1                                         \
            ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

foreach list_element [keylget interface_status interface_handle] {
    lappend interface_config_handle_1_list $list_element
}     

################################################################################
# END - Interface configuration - L2, L3
################################################################################

puts "Interface config complete."

################################################################################
# 1. Start ::ixia::emulation_twamp_config
################################################################################
# Start TWAMP Call

set twamp_port_list [list $port_0 $port_1]
set TWAMP_vport_handles [list]
foreach port_x $twamp_port_list {
    set port_handle                     $port_x              
    set TWAMP_config_status [::ixia::emulation_twamp_config                     \
            -mode                                create                         \
            -port_handle                         $port_handle                   \
            -error_estimate_multiplier           12                             \
            -error_estimate_scale                10                             \
            -global_max_outstanding              32                             \
            -global_setup_rate                   8                              \
            -global_teardown_rate                9                              \
            -port_max_outstanding                34                             \
            -port_override_globals               1                              \
            -port_setup_rate                     7                              \
            -port_teardown_rate                  8                              \
            -session_timeout                     312                            \
            ]
    if {[keylget TWAMP_config_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget TWAMP_config_status log]"
        return
    } else {
        lappend twamp_config_status_list $TWAMP_config_status
    }
    lappend TWAMP_vport_handles [keylget TWAMP_config_status handle]
    puts "Ixia TWAMP handles are: "
    update idletasks
    foreach TWAMP_vport_handle $TWAMP_vport_handles {
        puts $TWAMP_vport_handle
        update idletasks
    }
    puts "Port $port_x complete."
}
# End TWAMP Call   #

################################################################################
# 1. End ::ixia::emulation_twamp_config
################################################################################

puts "::ixia::emulation_twamp_config - Complete"

################################################################################
# 2. START - ::ixia::emulation_twamp_control_range_config
################################################################################
puts "\nStart TWAMP control range configuration ..."

set TWAMP_control_range_handles [list]
set current_index 0
foreach interface_config_handle_0 $interface_config_handle_0_list {
    set current_server_ip [lindex $server_ip_list [expr $current_index]]
    incr current_index
    # Start TWAMP Call
    set TWAMP_control_range_config_status [::ixia::emulation_twamp_control_range_config  \
            -mode                                 create                                 \
            -control_mode                         unauthenticated                        \
            -count                                $twamp_control_sessions                \
            -handle                               $interface_config_handle_0             \
            -key_id                               second_key                             \
            -server_ip                            $current_server_ip                     \
            -server_ip_intra_range_step           0.0.0.0                                \
            -server_port                          862                                    \
            -shared_secret                        slightly_used                          \
            ]
    if {[keylget TWAMP_control_range_config_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget TWAMP_control_range_config_status log]"
        return
    }
    foreach twamp_control_range_returned_handle [keylget TWAMP_control_range_config_status handle] {
        lappend TWAMP_control_range_handles $twamp_control_range_returned_handle
    }
    puts "Ixia TWAMP handles are: "
    update idletasks
    foreach TWAMP_control_handle $TWAMP_control_range_handles {
        puts $TWAMP_control_handle
        update idletasks
    }
    # End TWAMP Call
}

################################################################################
# 2. END - ::ixia::emulation_twamp_control_range_config
################################################################################

puts "::ixia::emulation_twamp_control_range_config - Complete"

################################################################################
# 3. START - ::ixia::emulation_twamp_server_range_config
################################################################################
puts "Start TWAMP server range configuration ..."

set TWAMP_server_range_handles [list]
set current_index 0
foreach interface_config_handle_1 $interface_config_handle_1_list {
    set current_permitted_ip [lindex $client_ip_list [expr $current_index]]
    incr current_index
    # Start TWAMP Call
    set TWAMP_server_range_config_status [::ixia::emulation_twamp_server_range_config    \
            -mode                                    create                              \
            -count                                   $twamp_server_sessions              \
            -handle                                  $interface_config_handle_1          \
            -control_port                            862                                 \
            -iteration_count                         1024                                \
            -key_id                                  second_key                          \
            -enable_access_control                   1                                   \
            -permitted_ip                            $current_permitted_ip               \
            -permitted_ip_intra_range_step           0.0.0.0                             \
            -permitted_pkt_size                      128                                 \
            -permitted_sender_port                   11009                               \
            -permitted_timeout                       1                                   \
            -reflector_port                          12009                               \
            -server_mode                             unauthenticated                     \
            -shared_secret                           slightly_used                       \
            ]
    if {[keylget TWAMP_server_range_config_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget TWAMP_server_range_config_status log]"
        return
    }
    foreach twamp_server_range_returned_handle [keylget TWAMP_server_range_config_status handle] {
        lappend TWAMP_server_range_handles $twamp_server_range_returned_handle
    }
    puts "Ixia TWAMP handles are: "
    update idletasks
    foreach TWAMP_server_handle $TWAMP_server_range_handles {
        puts $TWAMP_server_handle
        update idletasks
    }
    # End TWAMP Call
}

################################################################################
# 3. END - ::ixia::emulation_twamp_server_range_config
################################################################################

puts "::ixia::emulation_twamp_server_range_config - Complete"

################################################################################
# START - TWAMP test range configuration
################################################################################
puts "Start TWAMP test range configuration ..."

set TWAMP_test_range_handles [list]
foreach interface_config_handle_0 $interface_config_handle_0_list {
    set twamp_tst_range [lindex [ixNet getL $interface_config_handle_0 twampTestRange] 0]
    # Start TWAMP Call
    set TWAMP_test_range_config_status [::ixia::emulation_twamp_test_range_config        \
            -handle                                $twamp_tst_range                      \
            -mode                                  modify                                \
            -num_pkts                              50                                    \
            -padding_with_zero                     1                                     \
            -pkt_length                            128                                   \
            -pps                                   25                                    \
            -session_reflector_port                12009                                 \
            -session_reflector_port_step           1                                     \
            -session_sender_port                   11009                                 \
            -session_sender_port_step              1                                     \
            -test_sessions_count                   $twamp_test_sessions                  \
            -timeout                               1                                     \
            -type_p_descriptor                     0                                     \
            ]
    if {[keylget TWAMP_test_range_config_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget TWAMP_test_range_config_status log]"
        return
    }
    foreach twamp_test_range_reference [keylget TWAMP_test_range_config_status handle] {
       lappend TWAMP_test_range_handles $twamp_test_range_reference
    }
    puts "Ixia TWAMP handles are: "
    update idletasks
    foreach TWAMP_handle $TWAMP_test_range_handles {
        puts $TWAMP_handle
        update idletasks
    }
    # End TWAMP Call
}

puts "End TWAMP test range configuration ..."

################################################################################
# END - TWAMP test range configuration
################################################################################

set port_list [list $port_0 $port_1]

set interface_config_handle_zero [lindex $interface_config_handle_0_list 0]
set interface_config_handle_one  [lindex $interface_config_handle_1_list 0]

################################################################################
# Start TWAMP                                                                  #
################################################################################
puts " *** Waiting for the settings to settle down ***"
after 5000
puts " *** Starting TWAMP ***"
set reverse_port_list [list $port_1 $port_0]

foreach port_x $reverse_port_list {
    puts " - Start for port $port_x"
    set twamp_status [::ixia::emulation_twamp_control                           \
            -mode                   start                                       \
            -port_handle            $port_x                                     \
            ]
    if {[keylget twamp_status status] != $::SUCCESS} {
        puts "! Error while starting twamp on port $port_x"
        return
    }
    after 2000
}
after 5000

################################################################################
# Get and display stats...
################################################################################

set stat_list_twamp_control {        
    "Initiated Sessions"                        
            sess_initiated
    "Successful Sessions"
            sess_successful
    "Failed Sessions"
            sess_failed
    "Active Sessions"
            sess_active
    "Initiated Sessions Rate"
            sess_initiated_rate
    "Successful Sessions Rate"
            sess_successful_rate
    "Failed Sessions Rate"
            sess_failed_rate
}
set stat_list_twamp_data {        
   "Datagram Tx"
           datagram_tx
   "Datagram Rx"
           datagram_rx
   "Datagram Lost"
           datagram_lost
   "Datagram Unexpected"
           datagram_unexpected
   "Data Streams Initiated"
           data_streams_initiated
   "Data Streams Successful"
           data_streams_successful
   "Data Streams Failed"
           data_streams_failed
}
set stat_list_twamp_test {        
   "Initiated Sessions"
           sess_initiated
   "Successful Sessions"
           sess_successful
   "Failed Sessions"
           sess_failed
   "Active Sessions"
           sess_active
   "Initiated Sessions Rate"
           sess_initiated_rate
   "Successful Sessions Rate"
           sess_successful_rate
   "Failed Sessions Rate"
           sess_failed_rate
}
     
set twamp_info_status [::ixia::emulation_twamp_info                      \
        -port_handle            $port_0                                  \
        ]
if {[keylget twamp_info_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget twamp_info_status log]"
    return
}

after 500

puts "* Stats for control *"
foreach {proper_name real_name} $stat_list_twamp_control {
    set result [keylget twamp_info_status $real_name]
    puts "$proper_name = $result"
    set control_${real_name} $result
}

puts "* Stats for server *"
foreach stat_result [keylget twamp_info_status $port_0] {
    set lookup [lindex $stat_result 0]
    set result [lindex $stat_result 1]
    foreach {proper_name real_name} $stat_list_twamp_data {
        if {$lookup == $real_name} {
            puts "$proper_name = $result"
            set server_${real_name} $result
            break
        }
    }
}

puts "* Stats for test *"
foreach stat_result [keylget twamp_info_status $port_0] {
    set lookup [lindex $stat_result 0]
    set result [lindex $stat_result 1]
    foreach {proper_name real_name} $stat_list_twamp_test {
        if {$lookup == $real_name} {
            puts "$proper_name = $result"
            set test_${real_name} $result
            break
        }
    }
}
after 1000
################################################################################
# Stop TWAMP                                                                   #
################################################################################
foreach port_x $reverse_port_list {
    puts " - Stop for port $port_x"
    set twamp_status [::ixia::emulation_twamp_control                           \
            -mode                   stop                                        \
            -port_handle            $port_x                                     \
            ]
    if {[keylget twamp_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget twamp_status log]"
        return
    }
}
return "SUCCESS - $test_name - [clock format [clock seconds]]"