################################################################################
# Version 1.0    $Revision: 2 $
# $Author: Lavinia Raicea $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    26/5-2005 Lavinia Raicea
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
#    This sample creates RIPv1, RIPv2 and RIPng routers. It adds route ranges  #
#    to each router. Then it deletes some of the route ranges.                 #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM100TXS8 module.                              #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 127.0.0.1
set port_list1 10/1
set port_list2 10/2
set port_list3 10/3

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect \
        -reset                    \
        -device    $chassisIP     \
        -port_list $port_list1    \
        -username  ixiaApiUser    ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle1 [keylget connect_status port_handle.$chassisIP.$port_list1]

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle1       \
        -autonegotiation 1                   \
        -duplex          full                \
        -speed           ether100            ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
####################################################
#  Configure interfaces and create RIP v1 sessions #
####################################################
set rip_status [::ixia::emulation_rip_config         \
        -port_handle                 $port_handle1 \
        -mode                        create        \
        -session_type                ripv1         \
        -reset                                     \
        -count                       3             \
        -intf_ip_addr                11.1.0.2      \
        -intf_ip_addr_step           0.1.0.0       \
        -neighbor_intf_ip_addr       11.1.0.1      \
        -intf_prefix_length          24            \
        -update_interval             50            \
        -update_interval_offset      5             \
        -update_mode                 no_horizon    \
        -vlan_id                     10            \
        -vlan_id_step                10            \
        -mac_address_init            0000.0000.0001]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}
set ripv1_routers [keylget rip_status handle]
set ripv1_route_ranges [list ]
set i 1
# Creates 2 route ranges for each router => a total of 6 route ranges
foreach ripv1_router $ripv1_routers {
    # Create first route range
    set rip_status [::ixia::emulation_rip_route_config   \
            -handle                      $ripv1_router \
            -mode                        create        \
            -reset                                     \
            -num_prefixes                5             \
            -prefix_start                100.$i.0.0    \
            -prefix_length               16            \
            -metric                      2             \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend ripv1_route_ranges [keylget rip_status route_handle]
    # Create second route range
    set rip_status [::ixia::emulation_rip_route_config              \
            -handle                      $ripv1_router            \
            -mode                        create                   \
            -num_prefixes                5                        \
            -prefix_start                200.$i.0.0               \
            -prefix_length               16                       \
            -metric                      2                        \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend ripv1_route_ranges [keylget rip_status route_handle]
    incr i
}

set ripv1_to_be_deleted [list \
        [lindex $ripv1_route_ranges 1] \
        [lindex $ripv1_route_ranges 3] \
        [lindex $ripv1_route_ranges 5] ]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                    \
        -device    $chassisIP     \
        -port_list $port_list2    \
        -username  ixiaApiUser    ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle2 [keylget connect_status port_handle.$chassisIP.$port_list2]

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle2       \
        -autonegotiation 1                   \
        -duplex          full                \
        -speed           ether100            ]
###################################################
#  Configure interfaces and create RIPv2 sessions #
###################################################
set rip_status [::ixia::emulation_rip_config          \
        -port_handle                 $port_handle2  \
        -mode                        create         \
        -reset                                      \
        -intf_ip_addr                12.0.0.2       \
        -neighbor_intf_ip_addr       12.0.0.1       \
        -intf_prefix_length          24             \
        -update_interval             50             \
        -update_interval_offset      5              \
        -update_mode                 poison_reverse \
        -authentication_mode         text           \
        -password                    abcde          \
        -send_type                   broadcast_v2   \
        -receive_type                v1_v2          \
        -count                       3              \
        -mac_address_init            0000.0000.0004 ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

set ripv2_routers [keylget rip_status handle]

set ripv2_route_ranges [list ]
set i 20
foreach ripv2_router $ripv2_routers {
    # Create first route range
    set rip_status [::ixia::emulation_rip_route_config   \
            -handle                      $ripv2_router \
            -mode                        create        \
            -reset                                     \
            -num_prefixes                5             \
            -prefix_start                $i.1.0.0      \
            -prefix_length               16            \
            -metric                      2             \
            -next_hop                    12.0.0.$i     \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend ripv2_route_ranges [keylget rip_status route_handle]
    
    # Create second route range
    set rip_status [::ixia::emulation_rip_route_config   \
            -handle                      $ripv2_router \
            -mode                        create        \
            -num_prefixes                5             \
            -prefix_start                              \
            [mpexpr $i + 10].[mpexpr $i + 10].1.0      \
            -prefix_length               24            \
            -metric                      2             \
            -route_tag                   100           \
            -next_hop                    12.0.0.[mpexpr $i + 50] \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend ripv2_route_ranges [keylget rip_status route_handle]
    incr i 10
}

set ripv2_to_be_deleted [list \
        [lindex $ripv2_route_ranges 1] \
        [lindex $ripv2_route_ranges 3] \
        [lindex $ripv2_route_ranges 5] ]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                    \
        -device    $chassisIP     \
        -port_list $port_list3    \
        -username  ixiaApiUser    ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle3 [keylget connect_status port_handle.$chassisIP.$port_list3]

########################################
# Configure interface in the test      #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle3       \
        -autonegotiation 1                   \
        -duplex          full                \
        -speed           ether100            ]
        
###################################################
#  Configure interfaces and create RIPng sessions #
###################################################

set ripng_status [::ixia::emulation_rip_config       \
        -port_handle                 $port_handle3 \
        -mode                        create        \
        -reset                                     \
        -session_type                ripng         \
        -intf_ip_addr                30:30:30:2:0:0:0:2  \
        -intf_ip_addr_step           0:0:0:1:0:0:0:0     \
        -intf_prefix_length          64            \
        -update_interval             50            \
        -update_interval_offset      5             \
        -update_mode                 no_horizon    \
        -receive_type                store         \
        -interface_metric            2             \
        -time_period                 100           \
        -num_routes_per_period       10            \
        -router_id                   20            \
        -router_id_step              10            \
        -vlan_id                     1500          \
        -vlan_id_step                100           \
        -count                       3             \
        -mac_address_init            0000.0000.0007]
if {[keylget ripng_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ripng_status log]"
}

set ripng_routers [keylget ripng_status handle]

set ripng_route_ranges [list ]
set i 1

# Creates three route ranges for each router => a total of 9 routes
foreach ripng_router $ripng_routers {
    # Create first route range
    set rip_status [::ixia::emulation_rip_route_config              \
            -handle                      $ripng_router            \
            -mode                        create                   \
            -reset                                                \
            -num_prefixes                5                        \
            -prefix_start                1$i:1$i:0:0:0:0:0:0    \
            -prefix_length               32                       \
            -prefix_step                 0:1000:0:0:0:0:0:0       \
            -metric                      2                        \
            -next_hop                    FE80:0:0:0:$i:$i:$i:$i   \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend ripng_route_ranges [keylget rip_status route_handle]
    # Create second route range
    set rip_status [::ixia::emulation_rip_route_config                  \
            -handle                      $ripng_router                \
            -mode                        create                       \
            -num_prefixes                5                            \
            -prefix_start                2$i:2$i:2$i:2$i:0:0:0:0  \
            -prefix_length               64                           \
            -metric                      2                            \
            -route_tag                   100                          \
            -next_hop                    FE81:0:0:0:$i:$i:$i:$i       \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend ripng_route_ranges [keylget rip_status route_handle]
    
    # Create third route range
    set rip_status [::ixia::emulation_rip_route_config              \
            -handle                      $ripng_router            \
            -mode                        create                   \
            -num_prefixes                5                        \
            -prefix_start                4$i:4$i:4$i:0:0:0:0:0    \
            -prefix_length               48                       \
            -metric                      2                        \
            -route_tag                   100                      \
            -next_hop                    FE82:0:0:0:$i:$i:$i:$i   \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend ripng_route_ranges [keylget rip_status route_handle]
    
    incr i
}

set ripng_to_be_deleted [list \
        [lindex $ripng_route_ranges 0] \
        [lindex $ripng_route_ranges 1] \
        [lindex $ripng_route_ranges 3] \
        [lindex $ripng_route_ranges 4] \
        [lindex $ripng_route_ranges 6] \
        [lindex $ripng_route_ranges 7] ]

set rip_routes_to_be_deleted [concat \
        $ripv1_to_be_deleted \
        $ripv2_to_be_deleted \
        $ripng_to_be_deleted ]


# Delete route ranges
set rip_status [::ixia::emulation_rip_route_config                     \
        -route_handle                $rip_routes_to_be_deleted       \
        -mode                        delete                          \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}
return "SUCCESS - $test_name - [clock format [clock seconds]]"
