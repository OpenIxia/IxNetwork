#################################################################################
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
#   This sample configures interface and modifies the VLAN values in the       #
#       configured interface                                                   #
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
set cfgError                                    0
set chassis_ip                                  10.205.16.54
set port_list                                   [list 2/5]
set ixnetwork_tcl_server                        127.0.0.1
set port_count                                  1
################################################################################
# START - Connect to the chassis
################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect

puts "Starting - $test_name - [clock format [clock seconds]]"
puts "Start connecting to chassis ..."

set connect_status [::ixia::connect                                            \
            -reset                                                             \
            -device               $chassis_ip                                  \
            -port_list            $port_list                                   \
            -break_locks          $break_locks                                 \
            -tcl_server           $tcl_server                                  \
            -ixnetwork_tcl_server $ixnetwork_tcl_server                        \
            -interactive          1                                            \
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
    incr i
}
puts "End connecting to chassis ..."

################################################################################
# END - Connect to the chassis
################################################################################
    
################################################################################
# START - Configure Interface 
################################################################################
    
set _result_ [::ixia::interface_config                          \
    -mode                                config                 \
    -port_handle                         $port_0                \
    -transmit_mode                       advanced               \
    -port_rx_mode                        packet_group           \
    -tx_gap_control_mode                 average                \
    -transmit_clock_source               external               \
    -internal_ppm_adjust                 0                      \
    -additional_fcoe_stat_2              fcoe_invalid_frames    \
    -enable_data_center_shared_stats     0                      \
    -data_integrity                      1                      \
    -additional_fcoe_stat_1              fcoe_invalid_delimiter \
    -intf_mode                           ethernet               \
    -speed                               ether100               \
    -duplex                              full                   \
    -autonegotiation                     1                      \
    -phy_mode                            copper                 \
]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
    return 0
}

################################################################################
# END - Configure Interface 
################################################################################

################################################################################
# START - Modify Interface 
################################################################################
 
set _result_ [::ixia::interface_config                      \
    -mode                               modify              \
    -port_handle                        $port_0             \
    -gateway                            8.0.0.2             \
    -intf_ip_addr                       8.0.0.1             \
    -intf_ip_addr_step                  0.0.1.0             \
    -netmask                            255.255.255.0       \
    -check_opposite_ip_version          0                   \
    -src_mac_addr                       0000.04f0.c442      \
    -single_ns_per_gateway              1                   \
    -single_arp_per_gateway             1                   \
    -arp_on_linkup                      1                   \
    -ns_on_linkup                       1                   \
    -mtu                                1500                \
    -connected_count                    10                  \
    -vlan                               1                   \
    -vlan_id                            1                   \
    -vlan_user_priority                 6,7                 \
    -vlan_id_inner                      11                  \
    -vlan_id_step                       3                   \
    -vlan_id_count                      2                   \
    -vlan_id_inner_step                 13                  \
    -vlan_id_inner_count                14                  \
    -vlan_protocol_id                   0x88A8              \
    -l23_config_type                    protocol_interface  \
]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
    return 0
}

################################################################################
# END - Modify Interface 
################################################################################

################################################################################
# START - Modify Interface 
################################################################################    
    
set _result_ [::ixia::interface_config                  \
    -mode                           modify              \
    -port_handle                    $port_0             \
    -connected_count                1                   \
    -intf_ip_addr                   10.10.0.1           \
    -intf_ip_addr_step              0.0.0.1             \
    -gateway                        0.0.0.0             \
    -gateway_step                   0.0.0.0             \
    -netmask                        255.255.0.0         \
    -gateway_incr_mode              every_subnet        \
    -mss                            1460                \
    -l23_config_type                static_endpoint     \
    -vlan                           1                   \
    -qinq_incr_mode                 both                \
    -vlan_id                        1                   \
    -vlan_id_step                   3                   \
    -vlan_id_count                  4                   \
    -addresses_per_vlan             12,2                \
    -vlan_user_priority             7,6                 \
    -vlan_id_mode                   increment           \
    -vlan_id_inner_mode             increment           \
    -vlan_id_inner_step             13                  \
    -vlan_id_inner_count            14                  \
    -vlan_id_inner                  11                  \
    -mtu                            1500                \
    -src_mac_addr                   000a.0a00.0100      \
    -src_mac_addr_step              0000.0000.0001      \
]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
    return 0
}

################################################################################
# END - Modify Interface 
################################################################################

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1

