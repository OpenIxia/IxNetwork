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
#    This sample performes various operations. It creates RIPv1, RIPv2 and     #
#    RIPng routers on three different ports. It adds route ranges to the       #
#    routers. It modifies routers and route ranges, deletes routers and        #
#    route ranges. It deisables, enables, starts and stops routers. It         #
#    advertises and withdraws route ranges.
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
        -count                       5             \
        -intf_ip_addr                11.0.0.100    \
        -intf_prefix_length          24            \
        -update_interval             50            \
        -update_interval_offset      5             \
        -update_mode                 no_horizon    \
        -mac_address_init            0000.0000.0001]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}
set ripv1_routers [keylget rip_status handle]
set ripv1_route_ranges [list ]
set i 15
# Creates 2 route ranges for each router => a total of 6 route ranges
foreach ripv1_router $ripv1_routers {
    # Create first route range
    set rip_status [::ixia::emulation_rip_route_config   \
            -handle                      $ripv1_router \
            -mode                        create        \
            -reset                                     \
            -num_prefixes                5             \
            -prefix_start                $i.0.0.0      \
            -prefix_length               8             \
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
            -prefix_start                1$i.1$i.0.0              \
            -prefix_length               16                       \
            -metric                      2                        \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend ripv1_route_ranges [keylget rip_status route_handle]
    incr i 10
}

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
        -intf_ip_addr                12.0.0.100     \
        -intf_prefix_length          24             \
        -update_interval             50             \
        -update_interval_offset      5              \
        -update_mode                 no_horizon     \
        -authentication_mode         text           \
        -password                    abcde          \
        -send_type                   broadcast_v2   \
        -receive_type                v1_v2          \
        -count                       5              \
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
            -prefix_start                $i.0.0.0      \
            -prefix_length               8             \
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
            [mpexpr 10 + $i].[mpexpr 10 + $i].0.0      \
            -prefix_length               16            \
            -metric                      2             \
            -route_tag                   100           \
            -next_hop                    12.0.0.[mpexpr 10 + $i] \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend ripv2_route_ranges [keylget rip_status route_handle]
    incr i 20
}

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
        -intf_ip_addr                30:30:30:30:0:0:0:1    \
        -intf_ip_addr_step           0:0:0:1:0:0:0:0        \
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
        -count                       5             \
        -mac_address_init            0000.0000.0007]
if {[keylget ripng_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ripng_status log]"
}

set ripng_routers [keylget ripng_status handle]

set ripng_route_ranges [list ]
set i 5

# Creates three route ranges for each router => a total of 9 routes
foreach ripng_router $ripng_routers {
    # Create first route range
    set rip_status [::ixia::emulation_rip_route_config                       \
            -handle                      $ripng_router                     \
            -mode                        create                            \
            -reset                                                         \
            -num_prefixes                2                                 \
            -prefix_start                1$i:10:0:0:0:0:0:0                \
            -prefix_length               32                                \
            -prefix_step                 0:1000:0:0:0:0:0:0                \
            -metric                      2                                 \
            -next_hop                    FE80:0:0:0:$i:$i:$i:$i            \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend ripng_route_ranges [keylget rip_status route_handle]
    # Create second route range
    set rip_status [::ixia::emulation_rip_route_config                       \
            -handle                      $ripng_router                     \
            -mode                        create                            \
            -num_prefixes                2                                 \
            -prefix_start                2$i:2$i:20:0:0:0:0:0              \
            -prefix_length               48                                \
            -metric                      2                                 \
            -route_tag                   100                               \
            -next_hop                    FE81:0:0:0:$i:$i:$i:$i            \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend ripng_route_ranges [keylget rip_status route_handle]
    
    # Create third route range
    set rip_status [::ixia::emulation_rip_route_config                       \
            -handle                      $ripng_router                     \
            -mode                        create                            \
            -num_prefixes                2                                 \
            -prefix_start                4$i:4$i:4$i:40:0:0:0:0            \
            -prefix_length               64                                \
            -metric                      2                                 \
            -route_tag                   100                               \
            -next_hop                    FE82:0:0:0:$i:$i:$i:$i            \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend ripng_route_ranges [keylget rip_status route_handle]
    
    incr i
}


set rip_all_routers [concat \
        $ripv1_routers \
        $ripv2_routers \
        $ripng_routers ]

set rip_all_routes [concat  \
        $ripv1_route_ranges \
        $ripv2_route_ranges \
        $ripng_route_ranges ]

# Modify all sessions
set rip_status [::ixia::emulation_rip_config            \
        -mode                        modify           \
        -handle                      $rip_all_routers \
        -update_interval             29               \
        -update_interval_offset      2                \
        -update_mode                 poison_reverse   \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

# Modify all routes
set rip_status [::ixia::emulation_rip_route_config      \
        -mode                        modify           \
        -route_handle                $rip_all_routes  \
        -metric                      1                \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

# Delete sessions
set rip_status [::ixia::emulation_rip_config            \
        -mode                        delete           \
        -handle                      [list            \
        [lindex $ripv1_routers 2]                     \
        [lindex $ripv2_routers 2]                     \
        [lindex $ripng_routers 2]]                    \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

# Remove deleted routers from the lists
set ripv1_routers [lreplace $ripv1_routers 2 2]
set ripv2_routers [lreplace $ripv2_routers 2 2]
set ripng_routers [lreplace $ripng_routers 2 2]

# Remove corresponding route from the lists
set ripv1_route_ranges [lreplace $ripv1_route_ranges 4 5]
set ripv2_route_ranges [lreplace $ripv2_route_ranges 4 5]
set ripng_route_ranges [lreplace $ripng_route_ranges 6 8]

# Disable sessions
set rip_status [::ixia::emulation_rip_config            \
        -mode                        disable          \
        -handle                      [concat          \
        [lrange $ripv1_routers 1 2]                   \
        [lrange $ripv2_routers 1 2]                   \
        [lrange $ripng_routers 1 2]]                  \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

# Start protocols on ports
set rip_status [::ixia::emulation_rip_control  \
        -mode           start                \
        -port_handle    [list $port_handle1  \
        $port_handle2                        \
        $port_handle3]                       \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

# Stop protocols on ports
set rip_status [::ixia::emulation_rip_control  \
        -mode           stop                 \
        -port_handle    [list $port_handle1  \
        $port_handle2                        \
        $port_handle3]                       \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

# Enable sessions and start protocols 
set rip_status [::ixia::emulation_rip_control           \
        -mode                        start            \
        -handle                      [concat          \
        [lrange $ripv1_routers 1 2]                   \
        [lrange $ripv2_routers 1 2]                   \
        [lrange $ripng_routers 1 2]]                  \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

# Stop protocols on ports
set rip_status [::ixia::emulation_rip_control  \
        -mode           stop                 \
        -port_handle    [list $port_handle1  \
        $port_handle2                        \
        $port_handle3]                       \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

# Modify router - this modification will not affect the router
# because authentication is only valid for RIPv2
set rip_status [::ixia::emulation_rip_config      \
        -mode                  modify           \
        -handle                [lindex $ripv1_routers 2]  \
        -authentication_mode   text             \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

# Delete route ranges
set rip_status [::ixia::emulation_rip_route_config   \
        -route_handle  [list             \
        [lindex $ripv1_route_ranges 5]   \
        [lindex $ripv1_route_ranges 7]   \
        [lindex $ripv2_route_ranges 5]   \
        [lindex $ripv2_route_ranges 7]   \
        [lindex $ripng_route_ranges 8]   \
        [lindex $ripng_route_ranges 11]] \
        -mode          delete            \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

# Remove corresponding routes from the lists
set ripv1_route_ranges [lreplace $ripv1_route_ranges 5 5]
set ripv1_route_ranges [lreplace $ripv1_route_ranges 6 6]
set ripv2_route_ranges [lreplace $ripv2_route_ranges 5 5]
set ripv2_route_ranges [lreplace $ripv2_route_ranges 6 6]
set ripng_route_ranges [lreplace $ripng_route_ranges 8 8]
set ripng_route_ranges [lreplace $ripng_route_ranges 10 10]

# Create another route range
set rip_status [::ixia::emulation_rip_route_config                       \
        -handle                      [lindex $ripng_routers end]       \
        -mode                        create                            \
        -num_prefixes                5                                 \
        -prefix_start                50:50:59:50:0:0:0:0               \
        -prefix_length               64                                \
        -metric                      2                                 \
        -route_tag                   100                               \
        -next_hop                    FE83:0:0:0:1:1:1:1                \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}
set ripng_route_ranges [concat $ripng_route_ranges \
        [keylget rip_status route_handle]]
        
# Withdraw route ranges
set rip_status [::ixia::emulation_rip_control  -withdraw \
        [lrange $ripng_route_ranges 1 5]]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

# Start protocols on port
set rip_status [::ixia::emulation_rip_control  \
        -mode           start                \
        -port_handle    $port_handle3        \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}


# Advertise route ranges
set rip_status [::ixia::emulation_rip_control  -advertise \
        [lrange $ripng_route_ranges 1 5]]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}
 
# Stop protocols on port
set rip_status [::ixia::emulation_rip_control  \
        -mode           stop                 \
        -port_handle    $port_handle3        \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
