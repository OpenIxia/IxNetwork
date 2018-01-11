################################################################################
# Version 1.0    $Revision: 2 $
# $Author: Lavinia Raicea $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    5/3-2005 Lavinia Raicea
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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample creates an IGMP v3 host, two pools of five multicast groups   #
#    and two pools of three multicast sources. It adds the multicast groups    #
#    from the first pool to the host. Then it adds the multicast sources from  #
#    both source pools to the multicast groups in the second group pool. These #
#    multicast groups are added to the host.                                   #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM100TXS8 module.                              #
#                                                                              #
################################################################################
set env(IXIA_VERSION) HLTSET26
package require Ixia

set test_name [info script]

set chassisIP 10.205.19.147
set port_list 3/3

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect \
        -reset                    \
        -device    $chassisIP     \
        -port_list $port_list     \
        -username  ixiaApiUser    ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [keylget connect_status port_handle.$chassisIP.$port_list]

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -autonegotiation 1                   \
        -duplex          auto                \
        -speed           ether1000           \
        -arp_send_req    1                   \
        ]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}


##################################################
#  Configure interfaces and create IGMP sessions #
##################################################
set igmp_status [::ixia::emulation_igmp_config      \
        -port_handle                $port_handle  \
        -mode                       create        \
        -reset                                    \
        -msg_interval               1000          \
        -igmp_version               v3            \
        -ip_router_alert            1             \
        -general_query              1             \
        -group_query                1             \
        -unsolicited_report_interval         50   \
        -suppress_report            0             \
        -max_response_control       1             \
        -max_response_time          0             \
        -msg_count_per_interval     2             \
        -enable_packing             1             \
        -max_groups_per_pkts        2             \
        -max_sources_per_group      3             \
        -filter_mode                exclude       \
        -count                      1             \
        -intf_ip_addr               20.0.0.1      \
        -neighbor_intf_ip_addr      20.0.0.2      \
        -intf_prefix_len            24            ]
if {[keylget igmp_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmp_status log]"
}
set session [keylget igmp_status handle]

# Create multicast group pool number 1
set group_status_1 [::ixia::emulation_multicast_group_config \
        -mode create                 \
        -num_groups    1             \
        -ip_addr_start 227.0.1.1     \
        -ip_addr_step  0.0.0.1       \
        -ip_prefix_len 24            ]

if {[keylget group_status_1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget group_status_1 log]"
}
set group1 [keylget group_status_1 handle]

# Create multicast group pool number 2
set group_status_2 [::ixia::emulation_multicast_group_config \
        -mode create                 \
        -num_groups    1             \
        -ip_addr_start 227.1.0.1     \
        -ip_addr_step  0.0.0.1       \
        -ip_prefix_len 24            ]

if {[keylget group_status_2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget group_status_2 log]"
}
set group2 [keylget group_status_2 handle]

# Create multicast source pool number 1
set source_status_1 [::ixia::emulation_multicast_source_config \
        -mode create                 \
        -num_sources    3            \
        -ip_addr_start 25.42.1.1     \
        -ip_addr_step  0.0.1.0       \
        -ip_prefix_len 24            ]

if {[keylget source_status_1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget source_status_1 log]"
}
set source1 [keylget source_status_1 handle]

# Create multicast source pool number 2
set source_status_2 [::ixia::emulation_multicast_source_config \
        -mode create                 \
        -num_sources    3            \
        -ip_addr_start 27.43.1.1     \
        -ip_addr_step  0.0.1.0       \
        -ip_prefix_len 24            ]

if {[keylget source_status_2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget source_status_2 log]"
}
set source2 [keylget source_status_2 handle]

# Create group member for session1 with group_pool_handle group1
set group_member_status_1 [::ixia::emulation_igmp_group_config  \
        -mode               create          \
        -session_handle     $session        \
        -group_pool_handle  $group1         ]
if {[keylget group_member_status_1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget group_member_status_1 log]"
}

# Create group member for session1 with group_pool_handle group2 and
# source handle source1 and source2
set group_member_status_2 [::ixia::emulation_igmp_group_config  \
        -mode               create                  \
        -session_handle     $session                \
        -group_pool_handle  $group2                 \
        -source_pool_handle [list $source1 $source2]]

if {[keylget group_member_status_2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget group_member_status_2 log]"
}

# Modify records/frame
set igmp_status [::ixia::emulation_igmp_config      \
        -port_handle                $port_handle  \
        -handle                     $session      \
        -mode                       modify        \
        -igmp_version               v3            \
        -max_groups_per_pkts        4             \
        -max_sources_per_group      5             ]
if {[keylget igmp_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmp_status log]"
}

::ixia::emulation_igmp_control -port_handle $port_handle -mode start

return "SUCCESS - $test_name - [clock format [clock seconds]]"
