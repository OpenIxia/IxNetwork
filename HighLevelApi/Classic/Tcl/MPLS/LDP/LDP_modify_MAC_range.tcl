################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    03-20-2008 LRaicea - created sample
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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample creates a LDP router and an LDP VC Range.                     #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested using HLTSET29.                                     #
#                                                                              #
################################################################################
package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 2/1]

################################################################################
# Connect to the chassis, reset to factory defaults
################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                            \
        -reset                                                                 \
        -device      $chassisIP                                                \
        -port_list   $port_list                                                \
        -username    ixiaApiUser                                               \
        -break_locks 1                                                         \
        ]
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
################################################################################
# Set L1 configuration
################################################################################
set interface_status [::ixia::interface_config                                 \
        -port_handle     $port_0                                               \
        -autonegotiation 1                                                     \
        -duplex          auto                                                  \
        -speed           auto                                                  \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

################################################################################
# LDP router configuration
################################################################################
set ldp_routers_status [::ixia::emulation_ldp_config                           \
        -mode                           create                                 \
        -port_handle                    $port_0                                \
        -count                          1                                      \
        -intf_ip_addr                   30.30.30.2                             \
        -intf_prefix_length             24                                     \
        -gateway_ip_addr                30.30.30.1                             \
        -loopback_ip_addr               3.3.3.2                                \
        -lsr_id                         3.3.3.2                                \
        -remote_ip_addr                 3.3.3.1                                \
        -label_space                    0                                      \
        -peer_discovery                 targeted_martini                       \
        -hello_interval                 5                                      \
        -hello_hold_time                15                                     \
        -keepalive_interval             10                                     \
        -keepalive_holdtime             30                                     \
        -discard_self_adv_fecs          0                                      \
        -enable_l2vpn_vc_fecs           1                                      \
        -enable_explicit_include_ip_fec 0                                      \
        -enable_remote_connect          1                                      \
        -enable_vc_group_matching       0                                      \
        -targeted_hello_hold_time       45                                     \
        -targeted_hello_interval        15                                     \
        ]

if {[keylget ldp_routers_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ldp_routers_status log]"
    return
}
set ldp_router [keylget ldp_routers_status handle]
    
    
################################################################################
# LDP VC Range configuration
################################################################################
set ldp_route_status [::ixia::emulation_ldp_route_config                       \
        -mode                              create                              \
        -handle                            $ldp_router                         \
        -fec_type                          vc                                  \
        -fec_vc_type                       eth                                 \
        -fec_vc_count                      3                                   \
        -fec_vc_group_id                   1                                   \
        -fec_vc_group_count                1                                   \
        -fec_vc_cbit                       0                                   \
        -fec_vc_id_start                   332                                 \
        -fec_vc_id_step                    1                                   \
        -fec_vc_id_count                   1                                   \
        -fec_vc_intf_mtu_enable            1                                   \
        -fec_vc_intf_mtu                   1500                                \
        -fec_vc_intf_desc                  "ixia_ldp_vc"                       \
        -packing_enable                    0                                   \
        -fec_vc_label_mode                 increment_label                     \
        -fec_vc_label_value_start          332                                 \
        -fec_vc_label_value_step           1                                   \
        -fec_vc_peer_address               3.3.3.1                             \
        -fec_vc_ce_ip_addr                 3.3.3.2                             \
        -fec_vc_mac_range_enable           1                                   \
        -fec_vc_mac_range_count            5                                   \
        -fec_vc_mac_range_repeat_mac       0                                   \
        -fec_vc_mac_range_same_vlan        0                                   \
        -fec_vc_mac_range_vlan_enable      0                                   \
        -fec_vc_mac_range_start            00aa.00bb.00cc                      \
        ]

if {[keylget ldp_route_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ldp_route_status log]"
    return
}
set lsp_vc_range_handles     [keylget ldp_route_status lsp_vc_range_handles]
set lsp_vc_mac_range_handles [keylget ldp_route_status lsp_vc_mac_range_handles]

################################################################################
# LDP VC Range modify
################################################################################
set ldp_route_status [::ixia::emulation_ldp_route_config                       \
        -mode                              modify                              \
        -handle                            $ldp_router                         \
        -lsp_handle                        [lindex $lsp_vc_mac_range_handles 0]\
        -fec_vc_mac_range_start            0011.0022.0033                      \
        ]
if {[keylget ldp_route_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ldp_route_status log]"
    return
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return

