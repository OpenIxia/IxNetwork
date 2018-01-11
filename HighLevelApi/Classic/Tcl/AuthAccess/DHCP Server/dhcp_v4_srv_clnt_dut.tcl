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
#    This sample creates DHCP Server and the DUT acts like a client.           #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET51.                                      #
#                                                                              #
################################################################################

################################################################################
# 
# DUT config:
#
# configure terminal
# 
# default interface GigabitEthernet0/2
# 
# interface GigabitEthernet0/2
# no ip address
# no shut
# 
# interface GigabitEthernet0/2.200
# encapsulation dot1Q 200 second-dot1q 100
# ip address dhcp
# ip dhcp client hostname hlt200
# no shut
# 
# interface GigabitEthernet0/2.201
# encapsulation dot1Q 201 second-dot1q 101
# ip address dhcp
# ip dhcp client hostname hlt201
# no shut
# 
# interface GigabitEthernet0/2.202
# encapsulation dot1Q 202 second-dot1q 102
# ip address dhcp
# ip dhcp client hostname hlt202
# no shut
#
#
################################################################################
set env(IXIA_VERSION) HLTSET51


if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
# General script variables
################################################################################
set test_name [info script]

################################################################################
# START - Connect to the chassis
################################################################################
puts "Start connecting to chassis ..."
update idletasks

set chassis_ip              10.205.17.50
set port_list               [list 2/1]

# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                        \
        -reset                                                             \
        -ixnetwork_tcl_server localhost                                    \
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
# Interface configuration - L1
################################################################################
puts "Start interface configuration L1 ..."
update idletasks

set interface_status [::ixia::interface_config                             \
        -port_handle      $port_handle                                     \
        -mode             config                                           \
        -intf_mode        ethernet                                         \
        -autonegotiation  1                                                \
        -speed            auto                                             \
        -duplex           auto                                             \
        -phy_mode         copper                                           \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}

puts "End interface configuration L1 ..."
update idletasks

################################################################################
# DHCP Server configuration
################################################################################
puts "Started DHCP Server configuration ..."
update idletasks

################################################################################
# Start DHCP Server Call
################################################################################
set dhcp_server_config_status [::ixia::emulation_dhcp_server_config            \
        -count                                       3                         \
        -encapsulation                               ETHERNET_II               \
        -local_mac                                   5000.0001.0001            \
        -ip_address                                  50.100.0.1                \
        -ip_gateway                                  50.100.0.254              \
        -ip_prefix_length                            16                        \
        -ip_prefix_step                              0.0.1.0                   \
        -ip_repeat                                   1                         \
        -ip_step                                     0.1.0.0                   \
        -ipaddress_count                             1000                      \
        -ipaddress_pool                              50.100.1.1                \
        -lease_time                                  300                       \
        -mode                                        create                    \
        -port_handle                                 $port_0                   \
        -vlan_id                                     200                       \
        -ipaddress_pool_step                         0.1.0.0                   \
        -ip_dns1                                     200.200.222.222           \
        -ip_dns1_step                                0.1.0.0                   \
        -ip_dns2                                     100.100.111.111           \
        -ip_dns2_step                                0.1.0.0                   \
        -ip_gateway_step                             0.1.0.0                   \
        -ip_version                                  4                         \
        -lease_time_max                              3600                      \
        -local_mac_step                              0000.0000.0001            \
        -local_mac_outer_step                        0000.0001.0000            \
        -local_mtu                                   1500                      \
        -qinq_incr_mode                              both                      \
        -ping_check                                  0                         \
        -ping_timeout                                1                         \
        -single_address_pool                         0                         \
        -vlan_id_count                               1                         \
        -vlan_id_count_inner                         1                         \
        -vlan_id_inner                               100                       \
        -vlan_id_repeat                              1                         \
        -vlan_id_repeat_inner                        1                         \
        -vlan_id_step                                1                         \
        -vlan_id_step_inner                          1                         \
        -vlan_user_priority                          0                         \
        -vlan_user_priority_inner                    0                         \
        ]

if {[keylget dhcp_server_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dhcp_server_config_status log]"
    return 0
}
set dhcp_server_handles [keylget dhcp_server_config_status handle.dhcp_handle]
puts "---Ixia DHCP Server handles are:---"
update idletasks
foreach dhcp_server_handle $dhcp_server_handles {
    puts $dhcp_server_handle
    update idletasks
}

################################################################################
# START DHCP
################################################################################
set control_status_1 [::ixia::emulation_dhcp_server_control \
        -port_handle      $port_0                    \
        -action           collect                    \
        ]
if {[keylget control_status_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status_1 log]"
    return 0
}
puts "---DHCP Server activated---"
after 30000
##################################################
#             GET DHCP STATISTICS                #
##################################################
set dhcp_stats_1 [::ixia::emulation_dhcp_server_stats  \
        -port_handle $port_0                    \
        -action      collect                    \
        ]
if {[keylget dhcp_stats_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name -[keylget dhcp_stats_1 log]"
    return 0
}
puts "---DHCP stats collected---"
##################################################
#            PRINT DHCP STATISTICS               #
##################################################
proc show_stats var {
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
            if {$key == "status"} {continue}
            set indent [string repeat "    " $level] 
            puts -nonewline $indent 
            if {[catch {keylkeys var $key}]} {
                puts "$key: [keylget var $key]"
                continue
            } else {
                puts $key
                puts "$indent[string repeat "-" [string length $key]]"
            }
            show_stats [keylget var $key]
    }
}

puts "------------------DHCP Server stats------------------"
show_stats $dhcp_stats_1 

################################################################################
# Clear config
################################################################################
# set clear_return [::ixia::cleanup_session -reset -port_handle $port_handle]
# if {[keylget clear_return status] != $::SUCCESS} {
#     puts "FAIL - $test_name -[keylget clear_return log]"
#     return 0
# }

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1



