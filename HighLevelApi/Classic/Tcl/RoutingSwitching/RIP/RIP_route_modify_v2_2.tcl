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
#    This sample creates three RIPv2 routers and adds two route ranges to      #
#    each router. Then it modifies all route ranges.                           #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM100TXS8 module.                              #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 127.0.0.1
set port_list 10/1

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
        -duplex          full                \
        -speed           ether100            ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

###################################################
#  Configure interfaces and create RIPv2 sessions #
###################################################
set rip_status [::ixia::emulation_rip_config          \
        -port_handle                 $port_handle   \
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
        -mac_address_init            0000.0000.0001 ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}

set rip_routers [keylget rip_status handle]

set rip_route_ranges [list ]
set i 20
foreach rip_router $rip_routers {
    # Create first route range
    set rip_status [::ixia::emulation_rip_route_config   \
            -handle                      $rip_router   \
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
    lappend rip_route_ranges [keylget rip_status route_handle]
    # Create second route range
    set rip_status [::ixia::emulation_rip_route_config               \
            -handle                      $rip_router               \
            -mode                        create                    \
            -num_prefixes                5                         \
            -prefix_start                [mpexpr $i + 10].10.0.0   \
            -prefix_length               16                        \
            -metric                      2                         \
            -route_tag                   100                       \
            -next_hop                    12.0.0.[mpexpr $i + 10]   \
            ]
    if {[keylget rip_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget rip_status log]"
    }
    lappend rip_route_ranges [keylget rip_status route_handle]
    incr i 20
}

# Modify route ranges

set rip_status [::ixia::emulation_rip_route_config        \
        -route_handle                $rip_route_ranges  \
        -mode                        modify             \
        -num_prefixes                10                 \
        -metric                      1                  \
        -route_tag                   25                 \
        -prefix_length               16                 \
        ]
if {[keylget rip_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rip_status log]"
}
return "SUCCESS - $test_name - [clock format [clock seconds]]"

