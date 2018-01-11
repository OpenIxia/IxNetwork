#################################################################################
# Version 1.0    $Revision: 2 $
# $Author: Karim $
#
# $Workfile: sample_ixia_hltapi_MLD_host_group_source.tcl $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    4-25-2003 Karim
#    4-25-2005 DRusu
#
# Description:
#
#################################################################################

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
#    This sample creates 10 MLD v2 hosts, a pool of two multicast groups       #
#    and a pool of five multicast sources. Then adds the multicast sources     #
#    in the pool to each multicast group in the group pool and all the groups  #
#    to each MLD hosts. The default include filter mode is applied to          #
#    the sources.                                                              #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM100TXS8 module.                              #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 127.0.0.1
set port_list [list 10/1]

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

#################################################
#  Configure 2 MLD hosts on interface           #
#  MLD Version 2                                #
#################################################
set mld_host_status [::ixia::emulation_mld_config     \
        -mode                        create         \
        -port_handle                 $port_handle   \
        -mld_version                 v2             \
        -count                       10             \
        -intf_ip_addr                30::31         \
        -intf_prefix_len             64             \
        -msg_interval                10             \
        -max_groups_per_pkts         5              \
        -unsolicited_report_interval 30             \
        -general_query               1              \
        -group_query                 1              \
        -max_response_control        1              \
        -max_response_time           0              \
        -ip_router_alert             1              \
        -suppress_report             1              \
        -mac_address_init            0000.0000.0001 \
        -reset                                      ]
if {[keylget mld_host_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget mld_host_status log]"
}

# get the MLD Host handle from keyed list
set mld_host_handle_list [keylget mld_host_status handle]

#####################################################################
#  Configure 2 MLD groups on each MLD hosts  on interface           #
#  MLD Version 2                                                    #
#####################################################################

set mld_group_status ""

# Set multicast group
set multicast_group_status [::ixia::emulation_multicast_group_config \
        -mode          create                                        \
        -num_groups    2                                             \
        -ip_addr_start FF15::1                                       \
        -ip_addr_step  0::1                                          \
        -ip_prefix_len 64                                            ]
if {[keylget multicast_group_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multicast_group_status log]"
}

# Get the multicast group handle from keyed list
set multicast_group_handle [keylget multicast_group_status handle]

# Set multicast sources
set multicast_source_status [::ixia::emulation_multicast_source_config \
        -mode          create                                          \
        -num_sources   5                                               \
        -ip_addr_start 20::21                                          \
        -ip_addr_step  0::1                                            \
        -ip_prefix_len 64                                              ]
if {[keylget multicast_source_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multicast_source_status log]"
}

# Get the multicast source handle from keyed list
set multicast_source_handle [keylget multicast_source_status handle]

#####################################################################
#  Configure 5 MLD sources on each MLD groups for each MLD host     #
#  MLD Version 2                                                    #
#####################################################################
foreach mld_host_handle $mld_host_handle_list {
    
    set single_mld_group_status [::ixia::emulation_mld_group_config \
            -mode               create                            \
            -session_handle     $mld_host_handle                  \
            -group_pool_handle  $multicast_group_handle           \
            -source_pool_handle $multicast_source_handle          ]
    if {[keylget single_mld_group_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget single_mld_group_status log]"
    }
    
    lappend mld_group_status $single_mld_group_status
}

######################
# START MLD          #
######################
set mld_emulation_status [::ixia::emulation_mld_control \
        -mode        start                            \
        -port_handle $port_handle                     ]
if {[keylget mld_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget mld_emulation_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
