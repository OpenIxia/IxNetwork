################################################################################
# Version 1.0    $Revision: 1 $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    04-8-2005  T.Kong - comply with HLTAPI V4.0 spec
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
#    This sample performs various operations . Creats two PIM routers,         #
#    modifies, enables, disables and deletes the routers.                      #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM100TXS8 module.                              #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 127.0.0.1
set port_list [list 10/1 10/2]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username  ixiaApiUser      ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
            temp_port]} {
        lappend port_handle $temp_port
    }
}

##############################################################################
# Configure interface in the test      
# IPv4                                 
##############################################################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle          \
        -autonegotiation 1                     \
        -duplex          full                  \
        -speed           ether100              ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set port1_handle [lindex $port_handle 0]
set port2_handle [lindex $port_handle 1]

##############################################################################
#  Configure a PIM neighbor 
##############################################################################
set pim_config_status [::ixia::emulation_pim_config    \
        -mode                   create                  \
        -reset                                          \
        -port_handle            $port1_handle           \
        -count                  2                       \
        -ip_version             4                       \
        -intf_ip_addr           3.3.3.100               \
        -intf_ip_addr_step      0.0.1.0                 \
        -intf_ip_prefix_length     24                   \
        -router_id              11.0.0.1                \
        -router_id_step         0.0.0.1                 \
        -neighbor_intf_ip_addr  22.0.0.1                \
        -dr_priority            10                      \
        -bidir_capable          0                       \
        -hello_interval         30                      \
        -hello_holdtime         40                      \
        -join_prune_interval    50                      \
        -join_prune_holdtime    60                      \
        -prune_delay_enable     1                       \
        -prune_delay            600                     \
        -override_interval      700                     \
        -vlan                   1                       \
        -vlan_id                300                     \
        -vlan_id_mode           increment               \
        -vlan_id_step           2                       \
        -vlan_user_priority     7                       \
        -mac_address_init       0000.0000.0001          \
        -gateway_intf_ip_addr       3.3.3.1             \
        -gateway_intf_ip_addr_step  0.0.1.0             \
        -prune_delay_tbit       1                       \
        -send_generation_id     1                       \
        -generation_id_mode     random                  \
        -writeFlag              write                   ]
if {[keylget pim_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pim_config_status log]"
}
set port1_session_handle [lindex [keylget pim_config_status handle] 0]

set pim_config_status [::ixia::emulation_multicast_source_config \
        -mode               create      \
        -num_sources        1           \
        -ip_addr_start      101.0.0.1   \
        -ip_addr_step       0.0.0.1     \
        -ip_prefix_len      24          \
        ]
if {[keylget pim_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pim_config_status log]"
}

set source_pool_handle [keylget pim_config_status handle]

set pim_config_status [::ixia::emulation_multicast_group_config \
        -mode               create      \
        -num_groups         1           \
        -ip_addr_start      225.0.0.1   \
        -ip_addr_step       0.0.0.1     \
        -ip_prefix_len      24          \
        ]

if {[keylget pim_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pim_config_status log]"
}

set group_pool_handle [keylget pim_config_status handle]

set pim_config_status [::ixia::emulation_pim_group_config   \
        -mode                   create                      \
        -session_handle         $port1_session_handle       \
        -group_pool_handle      $group_pool_handle          \
        -source_pool_handle     $source_pool_handle         \
        -rp_ip_addr             44.0.0.1                    \
        -group_pool_mode        send                        \
        -join_prune_aggregation_factor 10                   \
        -wildcard_group                 1                   \
        -s_g_rpt_group                  0                   \
        -rate_control                   1                   \
        -interval                       100                 \
        -join_prune_per_interval        99                  \
        -register_per_interval          101                 \
        -register_stop_per_interval     102                 \
        -flap_interval                  999                 \
        -spt_switchover                 0                   \
        -source_group_mapping           one_to_one          \
        -switch_over_interval           200                 \
        ]

if {[keylget pim_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pim_config_status log]"
}

set port1_group_member_handle [lindex [keylget pim_config_status handle] 0]


set pim_config_status [::ixia::emulation_pim_group_config   \
        -mode                   create                      \
        -session_handle         $port1_session_handle       \
        -group_pool_handle      $group_pool_handle          \
        -source_pool_handle     $source_pool_handle         \
        -rp_ip_addr             33.0.0.1                    \
        -group_pool_mode        register                    \
        -register_tx_iteration_gap     100                  \
        -register_udp_destination_port  44                  \
        -register_udp_source_port       55                  \
        -register_triggered_sg          0                   \
        ]

if {[keylget pim_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pim_config_status log]"
}

set port1_group_member_handle2 [lindex [keylget pim_config_status handle] 0]



##############################################################
#  Modify PIM config
##############################################################
set pim_config_status [::ixia::emulation_pim_config    \
        -mode                   modify                  \
        -port_handle            $port1_handle           \
        -handle                 $port1_session_handle   \
        -count                  2                       \
        -ip_version             4                       \
        -dr_priority            100                     \
        -bidir_capable          0                       \
        -hello_interval         300                     \
        -hello_holdtime         400                     \
        -join_prune_interval    500                     \
        -join_prune_holdtime    600                     \
        -prune_delay_enable     1                       \
        -prune_delay            699                     \
        -override_interval      799                     \
        -prune_delay_tbit       0                       \
        -send_generation_id     0                       \
        -generation_id_mode     random                  \
        -writeFlag              write                   ]
if {[keylget pim_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pim_config_status log]"
}


##############################################################
#  Disable PIM config
##############################################################
set pim_config_status [::ixia::emulation_pim_config     \
        -mode                   disable                 \
        -port_handle            $port1_handle           \
        -handle                 $port1_session_handle   \
        -writeFlag              nowrite                 ]
if {[keylget pim_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pim_config_status log]"
}


##############################################################
#  Enable PIM config
##############################################################
set pim_config_status [::ixia::emulation_pim_config     \
        -mode                   enable                 \
        -port_handle            $port1_handle           \
        -handle                 $port1_session_handle   \
        -writeFlag              nowrite                 ]
if {[keylget pim_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pim_config_status log]"
}


##############################################################
#  Disable All PIM config
##############################################################
set pim_config_status [::ixia::emulation_pim_config     \
        -mode                   disable_all             \
        -port_handle            $port1_handle           \
        -writeFlag              nowrite                 ]
if {[keylget pim_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pim_config_status log]"
}

##############################################################
#  Enable All PIM config
##############################################################
set pim_config_status [::ixia::emulation_pim_config     \
        -mode                   enable_all              \
        -port_handle            $port1_handle           \
        -writeFlag              nowrite                 ]
if {[keylget pim_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pim_config_status log]"
}


##############################################################
#  Delete PIM config
##############################################################
set pim_config_status [::ixia::emulation_pim_config     \
        -mode                   delete                  \
        -port_handle            $port1_handle           \
        -handle                 $port1_session_handle   \
        -writeFlag              nowrite                 ]
if {[keylget pim_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pim_config_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
