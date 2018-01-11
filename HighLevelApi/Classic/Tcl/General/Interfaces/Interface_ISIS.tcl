################################################################################
# Version 1.0    $Revision: 1 $
#
#    Copyright © 1997 - 2006 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    3-13-2006 : M. Githens
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
#    This sample creates 10 ISIS routers.  The key piece of this script is to  #
#    show how to use the interface_handle key from interface_config in a call  #
#    to the emulation_isis_config.                                             #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM100TXS4 module.                              #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 127.0.0.1
set port_list [list 1/1]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                    \
        -device    $chassisIP     \
        -port_list $port_list     \
        -username  ixiaApiUser    ]
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

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle          \
        -autonegotiation 1                     \
        -duplex          auto                  \
        -speed           auto                  ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set intf_handles ""

set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    22.1.1.2       \
        -gateway         22.1.1.1       \
        -netmask         255.255.255.0  \
        -src_mac_addr    0000.0005.0001 \
        -vlan            $false         ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
lappend intf_handles [keylget interface_status interface_handle]

set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    22.1.2.2       \
        -gateway         22.1.2.1       \
        -netmask         255.255.255.0  \
        -src_mac_addr    0000.0005.0002 \
        -vlan            $false         ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
lappend intf_handles [keylget interface_status interface_handle]

set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    22.1.3.2       \
        -gateway         22.1.3.1       \
        -netmask         255.255.255.0  \
        -src_mac_addr    0000.0005.0003 \
        -vlan            $false         ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
lappend intf_handles [keylget interface_status interface_handle]

set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    22.1.4.2       \
        -gateway         22.1.4.1       \
        -netmask         255.255.255.0  \
        -src_mac_addr    0000.0005.0004 \
        -vlan            $false         ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
lappend intf_handles [keylget interface_status interface_handle]

set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    22.1.5.2       \
        -gateway         22.1.5.1       \
        -netmask         255.255.255.0  \
        -src_mac_addr    0000.0005.0005 \
        -vlan            $false         ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
lappend intf_handles [keylget interface_status interface_handle]

set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    22.1.6.2       \
        -gateway         22.1.6.1       \
        -netmask         255.255.255.0  \
        -src_mac_addr    0000.0005.0006 \
        -vlan            $false         ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
lappend intf_handles [keylget interface_status interface_handle]

set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    22.1.7.2       \
        -gateway         22.1.7.1       \
        -netmask         255.255.255.0  \
        -src_mac_addr    0000.0005.0007 \
        -vlan            $false         ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
lappend intf_handles [keylget interface_status interface_handle]

set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    22.1.8.2       \
        -gateway         22.1.8.1       \
        -netmask         255.255.255.0  \
        -src_mac_addr    0000.0005.0008 \
        -vlan            $false         ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
lappend intf_handles [keylget interface_status interface_handle]

set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    22.1.9.2       \
        -gateway         22.1.9.1       \
        -netmask         255.255.255.0  \
        -src_mac_addr    0000.0005.0009 \
        -vlan            $false         ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
lappend intf_handles [keylget interface_status interface_handle]

set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    22.1.10.2       \
        -gateway         22.1.10.1       \
        -netmask         255.255.255.0  \
        -src_mac_addr    0000.0005.000A \
        -vlan            $false         ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
lappend intf_handles [keylget interface_status interface_handle]

set tx_port [lindex $port_handle 0]
#####################################################
# Configure 10 ISIS L1L2 neighbors interface 1/10/1 #
#####################################################
set isis_router_status [::ixia::emulation_isis_config  \
        -mode                           create         \
        -reset                                         \
        -port_handle                    $tx_port       \
        -interface_handle               $intf_handles  \
        -intf_ip_addr                   22.1.1.2       \
        -gateway_ip_addr                22.1.1.1       \
        -intf_ip_prefix_length          24             \
        -mac_address_init               0000.0000.0001 \
        -count                          10             \
        -wide_metrics                   1              \
        -discard_lsp                    1              \
        -attach_bit                     1              \
        -partition_repair               1              \
        -overloaded                     1              \
        -lsp_refresh_interval           888            \
        -lsp_life_time                  777            \
        -max_packet_size                1492           \
        -intf_metric                    0              \
        -routing_level                  L1L2           \
        -te_enable                      1              \
        -te_max_bw                      10             \
        -te_max_resv_bw                 20             \
        -te_unresv_bw_priority0         10             \
        -te_unresv_bw_priority2         20             \
        -te_unresv_bw_priority3         30             \
        -te_unresv_bw_priority4         40             \
        -te_unresv_bw_priority5         50             \
        -te_unresv_bw_priority6         60             \
        -te_unresv_bw_priority7         70             \
        -te_metric                      10]
if {[keylget isis_router_status status] != $::SUCCESS} {
    return "FAIL - [keylget isis_router_status log]"
}

######################
# START ISIS         #
######################
set isis_emulation_status [::ixia::emulation_isis_control \
        -port_handle $tx_port                             \
        -mode        start                                ]
if {[keylget isis_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_emulation_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
