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
#    This sample creates DHCP DHCP Server on a port and modifies some of its   #
#    parameters.                                                               #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET51.                                      #
#                                                                              #
################################################################################
set env(IXIA_VERSION) HLTSET51

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
# General script variables
################################################################################
set test_name                                   [info script]


################################################################################
# Connect to the chassis
################################################################################
puts "Start connecting to chassis ..."
update idletasks
set var_list [list chassis_ip port_list break_locks tcl_server ixnetwork_tcl_server]

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

foreach item $var_list {catch {unset $item}}
puts "End connecting to chassis ..."
update idletasks

################################################################################
# Interface configuration - L1
################################################################################
set interface_status [::ixia::interface_config                             \
        -port_handle      $port_0                                          \
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

################################################################################
# DHCP Server configuration
################################################################################
puts "Start dhcp server configuration ..."
update idletasks
set dhcp_server_config_status [::ixia::emulation_dhcp_server_config            \
        -mode                                        create                    \
        -port_handle                                 $port_0                   \
        -count                                       3                         \
        -encapsulation                               ETHERNET_II               \
        -local_mac                                   0000.0001.0001            \
        -local_mac_step                              0000.0000.0001            \
        -local_mac_outer_step                        0000.0001.0000            \
        -local_mtu                                   1500                      \
        -qinq_incr_mode                              both                      \
        -vlan_id                                     100                       \
        -vlan_id_count                               1                         \
        -vlan_id_count_inner                         1                         \
        -vlan_id_inner                               10                        \
        -vlan_id_repeat                              1                         \
        -vlan_id_repeat_inner                        1                         \
        -vlan_id_step                                1                         \
        -vlan_id_step_inner                          1                         \
        -vlan_user_priority                          0                         \
        -vlan_user_priority_inner                    0                         \
        -ip_version                                  4                         \
        -ip_address                                  10.10.0.1                 \
        -ip_repeat                                   1                         \
        -ip_step                                     0.0.1.0                   \
        -ip_gateway                                  10.10.0.2                 \
        -ip_gateway_step                             0.1.0.0                   \
        -ip_prefix_length                            16                        \
        -ip_prefix_step                              0.0.1.0                   \
        -ipaddress_count                             1000                      \
        -ipaddress_pool                              10.10.1.1                 \
        -ipaddress_pool_step                         0.1.0.0                   \
        -ip_dns1                                     ""                        \
        -ip_dns1_step                                0.1.0.0                   \
        -ip_dns2                                     ""                        \
        -ip_dns2_step                                0.1.0.0                   \
        -lease_time                                  86400                     \
        -lease_time_max                              864000                    \
        -ping_check                                  0                         \
        -ping_timeout                                1                         \
        -single_address_pool                         0                         \
        ]
if {[keylget dhcp_server_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dhcp_server_config_status log]"
    return
}
set dhcp_server_handles [keylget dhcp_server_config_status handle.dhcp_handle]
puts "Ixia dhcp_server handles are: "
update idletasks
foreach dhcp_server_handle $dhcp_server_handles {
    puts $dhcp_server_handle
    update idletasks
}

################################################################################
# DHCP Server modification
################################################################################
puts "Start dhcp server modification ..."
update idletasks
set dhcp_server_config_status [::ixia::emulation_dhcp_server_config            \
        -mode                                        modify                    \
        -handle                                      [lindex $dhcp_server_handles 0] \
        -local_mac                                   0000.00aa.00bb            \
        -vlan_id                                     200                       \
        ]
if {[keylget dhcp_server_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dhcp_server_config_status log]"
    return
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
