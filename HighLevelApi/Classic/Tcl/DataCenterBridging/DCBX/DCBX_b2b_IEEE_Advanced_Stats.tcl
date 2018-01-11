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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#                                                                              #
################################################################################


package require Ixia

set test_name [info script]

set chassisIP 10.205.16.65
set port_list [list 3/1 3/2]

set all_dcbx_ranges {}

# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassisIP      \
        -port_list              $port_list      \
        -username               cnicutar        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_array [keylget connect_status port_handle.$chassisIP]

set port0 [keylget port_array [lindex $port_list 0]]
set port1 [keylget port_array [lindex $port_list 1]]


set interface_status [::ixia::interface_config              \
    -mode                               config              \
    -port_handle                        $port0              \
    -data_integrity                     1                   \
    -intf_mode                          ethernet            \
    -speed                              auto                \
    -transmit_mode                      advanced            \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set style "//vport/protocolStack/ethernet/dcbxEndpoint/range"

set dcbx_status [::ixia::dcbxrange_config                   \
    -mode                               create              \
    -parent_handle                      $port0              \
    -style                              $style              \
    -enabled                            True                \
    -name                               DCBX-R3             \
    -chassis_id                         2E:1E:50:1F:00:00   \
    -port_id_sub_type                   0                   \
    -port_id_mac_address                12:EA:1B:36:00:00   \
    -port_id_interface_name             {<interface name>}  \
    -tx_interval                        30                  \
    -hold_time                          4                   \
    -tx_delay                           2                   \
    -dcbx_enable                        True                \
    -fast_init_enable                   True                \
    -oui                                00.1B.21            \
    -dcbx_subtype                       2                   \
    -control_tlv_max_version            255                 \
    -mac_range_count                    1                   \
    -mac_range_increment_by             00:00:00:00:00:01   \
    -mac_range_mac                      54:85:B2:DC:00:00   \
    -mac_range_name                     MAC-R3              \
    -mac_range_mtu                      1500                \
    -mac_range_enabled                  True                \
    -vlan_range_inner_first_id          1                   \
    -vlan_range_inner_increment         1                   \
    -vlan_range_enabled                 False               \
    -vlan_range_unique_count            4094                \
    -vlan_range_name                    VLAN-R3             \
    -vlan_range_increment_step          1                   \
    -vlan_range_priority                1                   \
    -vlan_range_inner_enable            False               \
    -vlan_range_inner_unique_count      4094                \
    -vlan_range_first_id                1                   \
    -vlan_range_increment               1                   \
    -vlan_range_inner_increment_step    1                   \
    -vlan_range_id_incr_mode            2                   \
    -vlan_range_inner_priority          1                   \
]
#Check status
if {[keylget dcbx_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dcbx_status log]"
}
set dcbx_range [keylget dcbx_status handles]
lappend all_dcbx_ranges $dcbx_range

set style //vport/protocolStack/ethernet/dcbxEndpoint/range/dcbxRange
set dcbx_status [::ixia::dcbxtlv_config                                                     \
    -mode                                                           create                  \
    -parent_handle                                                  $dcbx_range             \
    -style                                                          $style                  \
    -enabled                                                        True                    \
    -name                                                           DcbxTlvPgIeee-1         \
    -feature_type                                                   2                       \
    -max_version                                                    255                     \
    -sub_type                                                       0                       \
    -feature_enable                                                 True                    \
    -willing                                                        True                    \
    -error_override                                                 False                   \
    -error                                                          True                    \
    -tlv_settings_dcbx_tlv_pg_ieee_tcs_supported                    8                       \
    -tlv_settings_dcbx_tlv_pg_ieee_priority_group_id_map            {0 1 2 3 4 5 6 7}       \
    -tlv_settings_dcbx_tlv_pg_ieee_priority_group_percentage_map    {70 10 0 0 0 0 0 20}    \
]
if {[keylget dcbx_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dcbx_status log]"
}

set style //vport/protocolStack/ethernet/dcbxEndpoint/range/dcbxRange
set dcbx_status [::ixia::dcbxtlv_config                                         \
    -mode                                           add                         \
    -style                                          $style                      \
    -enabled                                        True                        \
    -name                                           DCBX-IEEE-PFC-TLV-1         \
    -feature_type                                   3                           \
    -max_version                                    255                         \
    -sub_type                                       0                           \
    -feature_enable                                 True                        \
    -willing                                        True                        \
    -error_override                                 False                       \
    -error                                          True                        \
    -tlv_settings_dcbx_tlv_pfc_ieee_tcs_supported   8                           \
    -tlv_settings_dcbx_tlv_pfc_ieee_priority_map    {1 1 0 0 0 0 0 1}           \
]
if {[keylget dcbx_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dcbx_status log]"
}

set dcbx_status [::ixia::dcbxtlv_config                                                         \
    -mode                                                       add                             \
    -style                                                      $style                          \
    -enabled                                                    True                            \
    -name                                                       DCBX-IEEE-Application-TLV-1     \
    -feature_type                                               4                               \
    -max_version                                                255                             \
    -sub_type                                                   0                               \
    -feature_enable                                             True                            \
    -willing                                                    True                            \
    -error_override                                             False                           \
    -error                                                      True                            \
    -tlv_settings_dcbx_tlv_fcoe_ieee_priority_map               {1 1 0 0 0 0 0 1}               \
    -tlv_settings_dcbx_tlv_fcoe_ieee_application_protocol_id    35078                           \
]
if {[keylget dcbx_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dcbx_status log]"
}

set dcbx_status [::ixia::dcbxtlv_config                                                         \
    -mode                                                       add                             \
    -style                                                      $style                          \
    -enabled                                                    False                           \
    -name                                                       DCBX-IEEE-Application-TLV-3     \
    -feature_type                                               4                               \
    -max_version                                                255                             \
    -sub_type                                                   0                               \
    -feature_enable                                             True                            \
    -willing                                                    True                            \
    -error_override                                             False                           \
    -error                                                      True                            \
    -tlv_settings_dcbx_tlv_fcoe_ieee_priority_map               {1 1 0 0 0 0 0 1}               \
    -tlv_settings_dcbx_tlv_fcoe_ieee_application_protocol_id    35092                           \
]
if {[keylget dcbx_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dcbx_status log]"
}

set dcbx_status [::ixia::dcbxtlv_config                                                         \
    -mode                                                       add                             \
    -style                                                      $style                          \
    -enabled                                                    True                            \
    -name                                                       DCBX-IEEE-Custom-TLV-3          \
    -feature_type                                               5                               \
    -max_version                                                255                             \
    -sub_type                                                   0                               \
    -feature_enable                                             True                            \
    -willing                                                    True                            \
    -error_override                                             False                           \
    -error                                                      True                            \
    -tlv_settings_dcbx_tlv_custom_feature_tlv                   {00 99 AA FF}                   \
]
if {[keylget dcbx_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dcbx_status log]"
}


set interface_status [::ixia::interface_config              \
    -mode                               config              \
    -port_handle                        $port1              \
    -data_integrity                     1                   \
    -intf_mode                          ethernet            \
    -speed                              auto                \
    -transmit_mode                      advanced            \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set style //vport/protocolStack/ethernet/dcbxEndpoint/range
set dcbx_status [::ixia::dcbxrange_config                   \
    -mode                               create              \
    -parent_handle                      $port1              \
    -style                              $style              \
    -enabled                            True                \
    -name                               DCBX-R4             \
    -chassis_id                         0E:E7:00:BD:00:00   \
    -port_id_sub_type                   0                   \
    -port_id_mac_address                5C:3D:A3:86:00:00   \
    -port_id_interface_name             {<interface name>}  \
    -tx_interval                        30                  \
    -hold_time                          4                   \
    -tx_delay                           2                   \
    -dcbx_enable                        True                \
    -fast_init_enable                   True                \
    -oui                                00.1B.21            \
    -dcbx_subtype                       2                   \
    -control_tlv_max_version            255                 \
    -mac_range_count                    1                   \
    -mac_range_increment_by             00:00:00:00:00:01   \
    -mac_range_mac                      6C:D8:16:44:00:00   \
    -mac_range_name                     MAC-R4              \
    -mac_range_mtu                      1500                \
    -mac_range_enabled                  True                \
    -vlan_range_inner_first_id          1                   \
    -vlan_range_inner_increment         1                   \
    -vlan_range_enabled                 False               \
    -vlan_range_unique_count            4094                \
    -vlan_range_name                    VLAN-R4             \
    -vlan_range_increment_step          1                   \
    -vlan_range_priority                1                   \
    -vlan_range_inner_enable            False               \
    -vlan_range_inner_unique_count      4094                \
    -vlan_range_first_id                1                   \
    -vlan_range_increment               1                   \
    -vlan_range_inner_increment_step    1                   \
    -vlan_range_id_incr_mode            2                   \
    -vlan_range_inner_priority          1                   \
]
if {[keylget dcbx_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dcbx_status log]"
}

set dcbx_range [keylget dcbx_status handles]
lappend all_dcbx_ranges $dcbx_range

set style //vport/protocolStack/ethernet/dcbxEndpoint/range/dcbxRange

set dcbx_status [::ixia::dcbxtlv_config                                                         \
    -mode create                                                                                \
    -parent_handle                                                  $dcbx_range                 \
    -style                                                          $style                      \
    -enabled                                                        True                        \
    -name                                                           DcbxTlvPgIeee-2             \
    -feature_type                                                   2                           \
    -max_version                                                    255                         \
    -sub_type                                                       0                           \
    -feature_enable                                                 True                        \
    -willing                                                        True                        \
    -error_override                                                 False                       \
    -error                                                          True                        \
    -tlv_settings_dcbx_tlv_pg_ieee_tcs_supported                    8                           \
    -tlv_settings_dcbx_tlv_pg_ieee_priority_group_id_map            {0 1 2 3 4 5 6 7}           \
    -tlv_settings_dcbx_tlv_pg_ieee_priority_group_percentage_map    {70 10 0 0 0 0 0 20}        \
]
if {[keylget dcbx_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dcbx_status log]"
}

set dcbx_status [::ixia::dcbxtlv_config                                                         \
    -mode                                                           add                         \
    -style                                                          $style                      \
    -enabled                                                        True                        \
    -name                                                           DCBX-IEEE-PFC-TLV-2         \
    -feature_type                                                   3                           \
    -max_version                                                    255                         \
    -sub_type                                                       0                           \
    -feature_enable                                                 True                        \
    -willing                                                        True                        \
    -error_override                                                 False                       \
    -error                                                          True                        \
    -tlv_settings_dcbx_tlv_pfc_ieee_tcs_supported                   8                           \
    -tlv_settings_dcbx_tlv_pfc_ieee_priority_map                    {1 1 0 0 0 0 0 1}           \
]
if {[keylget dcbx_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dcbx_status log]"
}


set dcbx_status [::ixia::dcbxtlv_config                                                         \
    -mode                                                           add                         \
    -style                                                          $style                      \
    -enabled                                                        True                        \
    -name                                                           DCBX-IEEE-Application-TLV-2 \
    -feature_type                                                   4                           \
    -max_version                                                    255                         \
    -sub_type                                                       0                           \
    -feature_enable                                                 True                        \
    -willing                                                        True                        \
    -error_override                                                 False                       \
    -error                                                          True                        \
    -tlv_settings_dcbx_tlv_fcoe_ieee_priority_map                   {1 1 0 0 0 0 0 1}           \
    -tlv_settings_dcbx_tlv_fcoe_ieee_application_protocol_id        35078                       \
]
if {[keylget dcbx_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dcbx_status log]"
}


set dcbx_status [::ixia::dcbxtlv_config                                                         \
    -mode                                                           add                         \
    -style                                                          $style                      \
    -enabled                                                        False                       \
    -name                                                           DCBX-IEEE-Application-TLV-4 \
    -feature_type                                                   4                           \
    -max_version                                                    255                         \
    -sub_type                                                       0                           \
    -feature_enable                                                 True                        \
    -willing                                                        True                        \
    -error_override                                                 False                       \
    -error                                                          True                        \
    -tlv_settings_dcbx_tlv_fcoe_ieee_priority_map                   {1 1 0 0 0 0 0 1}           \
    -tlv_settings_dcbx_tlv_fcoe_ieee_application_protocol_id        35092                       \
]
if {[keylget dcbx_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dcbx_status log]"
}


set dcbx_status [::ixia::dcbxtlv_config                                                         \
    -mode                                                           add                         \
    -style                                                          $style                      \
    -enabled                                                        True                        \
    -name                                                           DCBX-IEEE-Custom-TLV-4      \
    -feature_type                                                   5                           \
    -max_version                                                    255                         \
    -sub_type                                                       0                           \
    -feature_enable                                                 True                        \
    -willing                                                        True                        \
    -error_override                                                 False                       \
    -error                                                          True                        \
    -tlv_settings_dcbx_tlv_custom_feature_tlv                       {00 99 AA FF}               \
]
if {[keylget dcbx_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dcbx_status log]"
}



foreach dcbx_range $all_dcbx_ranges {
    set dcbx_status [::ixia::dcbxrange_control      \
    -handle         $dcbx_range                     \
    -action         connect                         \
    ]
    if {[keylget dcbx_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget dcbx_status log]"
    }
}

foreach port_handle [list $port0 $port1] {
    set r [::ixia::dcbxrange_stats                  \
    -mode           aggregate                       \
    -port_handle    $port_handle                    \
    ]
    if {[keylget r status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget r log]"
    }

    foreach {stat} [keylkeys r $port_handle.aggregate.gen] {
        set v [keylget r $port_handle.aggregate.gen.$stat]
        puts stderr [format {%40s = %s} $stat $v]
    }
    puts ""
    update idletasks
}

foreach dcbx_range $all_dcbx_ranges {
    set dcbx_status [::ixia::dcbxrange_control      \
    -handle         $dcbx_range                     \
    -action         disconnect                      \
    ]
    if {[keylget dcbx_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget dcbx_status log]"
    }
}
