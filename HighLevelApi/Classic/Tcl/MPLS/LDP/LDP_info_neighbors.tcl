################################################################################
# Version 1.1    $Revision: 2 $
# $Author: Matei-Eugen Vasile $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    3-29-2007 initial version - Matei-Eugen Vasile
#    5-4-2007 added statistics result display code - Matei-Eugen Vasile
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
#    This sample creates two LDP peer, adds FEC classes to them and gathers    #
#    information regarding the discovered neighbors.                           #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module in a back-to-back configuration.   #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 2/1 2/2]

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

set port_handle1 [keylget connect_status port_handle.$chassisIP.[lindex $port_list 0]]
set port_handle2 [keylget connect_status port_handle.$chassisIP.[lindex $port_list 1]]

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config                \
        -port_handle     [list $port_handle1 $port_handle2] \
        -autonegotiation 1                                  \
        -duplex          full                               \
        -speed           ether100                           \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################
# Configure the first LDP peer #
################################
set ldp_routers_status [::ixia::emulation_ldp_config      \
        -mode                           create          \
        -port_handle                    $port_handle1   \
        -label_adv                      unsolicited     \
        -peer_discovery                 link            \
        -count                          1               \
        -intf_ip_addr                   11.1.1.2        \
        -intf_prefix_length             24              \
        -intf_ip_addr_step              0.0.1.0         \
        -lsr_id                         10.10.10.10     \
        -label_space                    60              \
        -lsr_id_step                    0.0.1.0         \
        -mac_address_init               0000.0000.0001  \
        -enable_l2vpn_vc_fecs           1               \
        -enable_vc_group_matching       1               \
        -gateway_ip_addr                11.1.1.1        \
        -gateway_ip_addr_step           0.0.1.0         \
        -reset                                          \
        -graceful_restart_enable        1               \
        -recovery_time                  66000           \
        -reconnect_time                 90000           \
        ]
if {[keylget ldp_routers_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_routers_status log]"
}

set router_handle_list [keylget ldp_routers_status handle]

set router_handle1 [lindex $router_handle_list 0]

#################################
# Configure the second LDP peer #
#################################
set ldp_routers_status [::ixia::emulation_ldp_config      \
        -mode                           create          \
        -port_handle                    $port_handle2   \
        -label_adv                      unsolicited     \
        -peer_discovery                 link            \
        -count                          1               \
        -intf_ip_addr                   11.1.1.1        \
        -intf_prefix_length             24              \
        -intf_ip_addr_step              0.0.1.0         \
        -lsr_id                         20.20.20.20     \
        -label_space                    60              \
        -lsr_id_step                    0.0.1.0         \
        -mac_address_init               0000.0000.0002  \
        -enable_l2vpn_vc_fecs           1               \
        -enable_vc_group_matching       1               \
        -gateway_ip_addr                11.1.1.2        \
        -gateway_ip_addr_step           0.0.1.0         \
        -reset                                          \
        -graceful_restart_enable        1               \
        -recovery_time                  66000           \
        -reconnect_time                 90000           \
        ]
if {[keylget ldp_routers_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_routers_status log]"
}

set router_handle_list [keylget ldp_routers_status handle]

set router_handle2 [lindex $router_handle_list 0]


###########################################################
# Configure ipv4_prefix fec type routes on the first peer #
###########################################################
set ldp_routers_status [::ixia::emulation_ldp_route_config    \
        -mode                   create                      \
        -handle                 $router_handle1             \
        -fec_type               ipv4_prefix                 \
        -label_msg_type         mapping                     \
        -egress_label_mode      nextlabel                   \
        -num_lsps               3                           \
        -fec_ip_prefix_start    123.0.0.1                   \
        -fec_ip_prefix_length   16                          \
        -packing_enable         1                           \
        -label_value_start      100                         \
]

############################################################
# Configure ipv4_prefix fec type routes on the second peer #
############################################################
set ldp_routers_status [::ixia::emulation_ldp_route_config    \
        -mode                   create                      \
        -handle                 $router_handle2             \
        -fec_type               ipv4_prefix                 \
        -label_msg_type         mapping                     \
        -egress_label_mode      nextlabel                   \
        -num_lsps               5                           \
        -fec_ip_prefix_start    23.0.0.1                    \
        -fec_ip_prefix_length   8                           \
        -packing_enable         1                           \
        -label_value_start      50                          \
]


if {[keylget ldp_routers_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_routers_status log]"
}


################################
# Start the protocol emulation #
################################
set ldp_routers_status [::ixia::emulation_ldp_control \
        -mode start                                 \
        -port_handle $port_handle1                  \
        ]
if {[keylget ldp_routers_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_routers_status log]"
}

set ldp_routers_status [::ixia::emulation_ldp_control \
        -mode start                                 \
        -port_handle $port_handle2                  \
        ]
if {[keylget ldp_routers_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_routers_status log]"
}


###############
# Gather info #
###############
after 10000
set ldp_routers_info [::ixia::emulation_ldp_info  \
        -handle                 $router_handle1 \
        -mode                   neighbors       \
        ]
if {[keylget ldp_routers_info status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_routers_info log]"
}
puts "First router's neighbors:"
set ldp_neighbors [keylget ldp_routers_info neighbors]
foreach neighbor $ldp_neighbors {
    puts "\t$neighbor"
}

set ldp_routers_info [::ixia::emulation_ldp_info  \
        -handle                 $router_handle2 \
        -mode                   neighbors       \
        ]
if {[keylget ldp_routers_info status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ldp_routers_info log]"
}
puts "Second router's neighbors:"
set ldp_neighbors [keylget ldp_routers_info neighbors]
foreach neighbor $ldp_neighbors {
    puts "\t$neighbor"
}


return "SUCCESS - $test_name - [clock format [clock seconds]]"
