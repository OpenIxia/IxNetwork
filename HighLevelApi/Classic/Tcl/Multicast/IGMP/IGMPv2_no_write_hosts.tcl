#################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-20-2007 Mchakravarthy - created sample
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
#   This sample Configures IGMP groups and uses IGMP no write option     	   #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
# General script variables
################################################################################
set test_name                                   [info script]
set cfgError									0
set chassis_ip									10.205.16.54
set port_list									[list 2/5]
set ixnetwork_tcl_server						127.0.0.1
set port_count									1
################################################################################
# START - Connect to the chassis
################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect

set connect_status [::ixia::connect                     \
        -reset                                          \
        -device               $chassis_ip               \
        -ixnetwork_tcl_server $ixnetwork_tcl_server     \
        -port_list            $port_list                \
        -username             spopi                     \
        -interactive          1                         \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}
set port_handle [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]


############################################################
# Configure port properites like speed and autonegogiation #
############################################################
set interface_status [::ixia::interface_config          \
        -port_handle                    $port_handle    \
        -autonegotiation                1               \
        -duplex                         full            \
        -speed                          auto            \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

############################################################
# Configuring Interface 								   #
############################################################

set interface_status [::ixia::interface_config   \
        -port_handle        $port_handle         \
        -autonegotiation    1                    \
        -duplex             full                 \
        -speed              auto                 \
        -connected_count    3                    \
        -intf_ip_addr       130.0.0.2            \
        -intf_ip_addr_step  0.1.0.0              \
        -gateway            130.0.0.1            \
        -gateway_step       0.1.0.0              \
        -netmask            255.255.255.0        \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
set int_handles [keylget interface_status interface_handle]
set handle_1 [lindex $int_handles 0]
set handle_2 [lindex $int_handles 1]
set handle_3 [lindex $int_handles 2]


############################################################
# Configuring IGMP on the port   						   #
############################################################
set igmp_status [::ixia::emulation_igmp_config          \
        -port_handle                    $port_handle    \
        -mode                           create          \
        -msg_interval                   0               \
        -igmp_version                   v2              \
        -ip_router_alert                0               \
        -general_query                  0               \
        -group_query                    0               \
        -count                          1               \
        -intf_ip_addr                   130.0.0.2       \
        -neighbor_intf_ip_addr          130.0.0.1       \
        -intf_prefix_len                24              \
        -no_write                                       \
        ]
if {[keylget igmp_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmp_status log]"
}
set session_handle_1 [keylget igmp_status handle]

############################################################
# Create a new IGMP host using interface handle			   #
############################################################

set igmp_status [::ixia::emulation_igmp_config          \
        -port_handle                    $port_handle    \
        -mode                           create          \
        -interface_handle               $handle_2       \
        -msg_interval                   0               \
        -igmp_version                   v2              \
        -ip_router_alert                0               \
        -general_query                  0               \
        -group_query                    0               \
        -no_write                                       \
        ]
if {[keylget igmp_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmp_status log]"
}
set session_handle_2 [keylget igmp_status handle]

############################################################
# Create a new host, by matching the protocol interface IP #	
############################################################

set igmp_status [::ixia::emulation_igmp_config          \
        -port_handle                    $port_handle    \
        -mode                           create          \
        -msg_interval                   0               \
        -igmp_version                   v2              \
        -ip_router_alert                0               \
        -general_query                  0               \
        -group_query                    0               \
        -count                          1               \
        -intf_ip_addr                   150.0.0.2       \
        -neighbor_intf_ip_addr          150.0.0.1       \
        -intf_prefix_len                24              \
        -no_write                                       \
        ]
if {[keylget igmp_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmp_status log]"
}
set session_handle_3 [keylget igmp_status handle]

set igmp_status [::ixia::emulation_igmp_config          \
        -port_handle                    $port_handle    \
        -mode                           create          \
        -msg_interval                   0               \
        -igmp_version                   v2              \
        -ip_router_alert                0               \
        -general_query                  0               \
        -group_query                    0               \
        -count                          10              \
        -intf_ip_addr                   20.0.0.2        \
        -intf_ip_addr_step              10.0.0.0        \
        -neighbor_intf_ip_addr          20.0.0.1        \
        -neighbor_intf_ip_addr_step     10.0.0.0        \
        -intf_prefix_len                24              \
        -no_write                                       \
        ]
if {[keylget igmp_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmp_status log]"
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
