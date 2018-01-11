################################################################################
# Version 1.0    $Revision: 1 $
# $Author: RAntonescu $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    12-05-2007 RAntonescu - created sample
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
#    This sample creates five STP bridges and ten emulated LANs to be used by  #
#    the STP bridges.                                                          #
#    Each STP bridge will have three bridge interfaces.                        #
#    The STP bridge interface will be configured as a layer 2 interface with   #
#    stacked VLAN.                                                             #
#    On the first STP bridge, five VLAN objects are being configured.          #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET27.                                      #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]
set ixnetwork_tcl_server 127.0.0.1
set chassisIP 127.0.0.1
set port_list [list 3/3]

################################################################################
# Connect to the chassis,reset to factory defaults and take ownership
################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect 				\
        -reset                      				\
        -ixnetwork_tcl_server $ixnetwork_tcl_server \
        -device    $chassisIP       				\
        -port_list $port_list       				\
        -username  ixiaApiUser      				\
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
}

set port_array [keylget connect_status port_handle.$chassisIP]

set port_0 [keylget port_array [lindex $port_list 0]]

################################################################################
# Configure L1 interface
################################################################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_0               \
        -autonegotiation 1                     \
        -duplex          auto                  \
        -speed           auto                  \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

################################################################################
# Create emulated STP bridges
################################################################################
set stp_status [::ixia::emulation_stp_bridge_config \
        -port_handle              $port_0           \
        -auto_pick_bridge_mac     0                 \
        -auto_pick_port           0                 \
        -bridge_mac               1234.5678.9abc    \
        -bridge_mac_step          0000.0000.0005    \
        -bridge_mode              pvst              \
        -bridge_priority          8192              \
        -cst_root_mac_address     0101.1010.0101    \
        -cst_root_path_cost       100               \
        -cst_root_priority        24576             \
        -cst_vlan_port_priority   16                \
        -count                    5                 \
        -enable_jitter            1                 \
        -forward_delay            1000              \
        -hello_interval           1500              \
        -inter_bdpu_gap           10                \
        -intf_cost                7                 \
        -intf_count               3                 \
        -jitter_percentage        20                \
        -link_type                shared            \
        -mac_address_bridge_step  0000.0001.0000    \
        -mac_address_init         1111.2222.1111    \
        -mac_address_intf_step    0000.1111.0000    \
        -max_age                  12500             \
        -mtu                      576               \
        -port_no                  1                 \
        -port_no_bridge_step      0                 \
        -port_no_intf_step        1                 \
        -port_priority            144               \
        -pvid                     8                 \
        -vlan                     1                 \
        -vlan_id                  5,6,7             \
        -vlan_id_intf_step        0,0,1             \
        -vlan_user_priority       4,1,2             \
        ]
if {[keylget stp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_status log]"
    return
}

set bridge_handle [lindex [keylget stp_status bridge_handles] 0]

################################################################################
# Create VLAN objects on first STP bridge
################################################################################
set stp_status [::ixia::emulation_stp_vlan_config \
        -bridge_handle           $bridge_handle   \
        -count                   4                \
        -mode                    create           \
        -internal_root_path_cost 34               \
        -root_mac_address        0000.0000.0001   \
        -root_mac_address_step   0000.0000.00aa   \
        -root_priority           20480            \
        -vlan_port_priority      22               \
        -vlan_port_priority_step 2                \
        -vlan_id                 2                \
        -vlan_id_step            3                \
        ]
if {[keylget stp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_status log]"
    return
}

# retrieve first handle from VLAN objects
set vlan_handle [lindex [keylget stp_status handle] 0]

################################################################################
# Modify STP bridge
################################################################################
set stp_status [::ixia::emulation_stp_bridge_config \
        -handle             $bridge_handle          \
        -mode               modify                  \
        -bridge_msti_vlan   $vlan_handle            \
        ]
if {[keylget stp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_status log]"
    return
}

################################################################################
# Create an emulated LAN for STP use
################################################################################
set stp_status [::ixia::emulation_stp_lan_config \
        -port_handle     $port_0                 \
        -count           10                      \
        -mac_address     000e.4cd7.c011          \
        -mac_incr_enable 1                       \
        ]
if {[keylget stp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_status log]"
    return
}

################################################################################
# Start STP protocol on specified port
################################################################################
set stp_status [::ixia::emulation_stp_control \
        -port_handle     $port_0              \
        -mode            start                \
        ]
if {[keylget stp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_status log]"
    return
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
