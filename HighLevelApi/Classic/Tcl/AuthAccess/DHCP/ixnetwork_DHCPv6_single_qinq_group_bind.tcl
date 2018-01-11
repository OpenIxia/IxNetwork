################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Matei-Eugen Vasile $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    3-16-2007 Matei-Eugen Vasile
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
#    This sample creates a DHCPv6 group, binds it and gathers the DHCPv6       #
#    statistics from the port on which the group was configured. The group is  #
#    configured to use stacked VLANs.                                          #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################

################################################################################
# DUT config:                                                                  #
################################################################################
# conf t                                                                       
#                                                                              
# ipv6 local pool ixa_pool 2001:4::/48 64                                      
#                                                                              
# ipv6 dhcp pool ixaccess                                                      
#     prefix-delegation pool ixa_pool                                          
# exit                                                                         
#                                                                              
# interface f5/0                                                
#     no shutdown                                                             
# !                                                                           
# interface f5/0.80010                                          
#     encapsulation dot1Q 800 second-dot1q 10                                 
#     ipv6 enable                                                             
#     ipv6 dhcp server ixaccess                                               
# !                                                                           
# interface f5/0.80214                                          
#     encapsulation dot1Q 802 second-dot1q 14                                 
#     ipv6 enable                                                             
#     ipv6 dhcp server ixaccess                                               
# !                                                                           
# interface f5/0.80418                                          
#     encapsulation dot1Q 804 second-dot1q 18                                  
#     ipv6 enable                                                              
#     ipv6 dhcp server ixaccess                                                
# exit                                                                         
#                                                                             
# end                                                                         
################################################################################

package require Ixia

set test_name [info script]

set chassis_ip 10.205.19.121
set port_list [list 1/3]

# Connect to the chassis.
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassis_ip     \
        -port_list              $port_list      \
        -username               ixiaApiUser     ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}
set port_handle [keylget connect_status port_handle.$chassis_ip.$port_list]

# Configure physical port attributes
set interface_status [::ixia::interface_config \
        -port_handle       $port_handle        \
        -intf_mode          ethernet           \
        -phy_mode           copper             \
        -autonegotiation    1                  \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

# Create DHCPv6 settings objects.
# NOTE: Cisco supported only IAPD at the time this test script was written.
set dhcp_settings_obj [::ixia::emulation_dhcp_config    \
        -mode           create          \
        -port_handle    $port_handle    \
        -lease_time     300             \
        -reset                          \
	-version        ixnetwork       \
        ]
if {[keylget dhcp_settings_obj status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dhcp_settings_obj log]"
}
set settings_handle [keylget dhcp_settings_obj handle]

# Create DHCPv6 clients croups.
# NOTE:
#   -encap has the default set to "ethernet" 
#   -target_subport has the default set to "0" 
set dhcp_group_obj [::ixia::emulation_dhcp_group_config \
        -mode                       create              \
        -handle                     $settings_handle    \
        -encap                      ethernet_ii_qinq    \
        -mac_addr                   00.00.11.11.22.22   \
        -mac_addr_step              00.00.bb.00.11.00   \
	-dhcp6_range_ia_type        iapd                \
        -num_sessions               6                   \
        -vlan_id                    10                  \
        -vlan_id_step               4                   \
        -vlan_id_count              3                   \
        -vlan_user_priority         0                   \
        -vlan_id_outer              800                 \
        -vlan_id_outer_step         2                   \
        -vlan_id_outer_count        3                   \
	-dhcp_range_ip_type         ipv6                \
        -qinq_incr_mode             both                \
	-version                    ixnetwork           \
	-dhcp_range_param_request_list 2                   \
        ]
if {[keylget dhcp_group_obj status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dhcp_group_obj log]"
}
set group_handle [keylget dhcp_group_obj handle]

# Get IPv6 addresses for the clients emulated on port $port_handle.
set dhcp_port_status [::ixia::emulation_dhcp_control \
        -port_handle    $port_handle    \
        -action         bind            \
        ]       
if {[keylget dhcp_port_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget dhcp_port_status log]"
}



after 30000
##################################################
#             GET DHCP STATISTICS                #
##################################################
set dhcp_stats_0 [::ixia::emulation_dhcp_stats      \
            -port_handle $port_handle                     \
            -version     ixnetwork                         \
    	]
    if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
        puts "FAIL - $test_name -[keylget dhcp_stats_0 log]"
        return 0
    }
##################################################
#            PRINT DHCP STATISTICS               #
##################################################


proc show_stats var {
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
            if {$key == "status"} {continue}
            set indent [string repeat "    " $level] 
            puts -nonewline $indent 
            if {[catch {keylkeys var $key}]} {
                puts "$key: [keylget var $key]"
                continue
            } else {
                puts $key
                puts "$indent[string repeat "-" [string length $key]]"
            }
            show_stats [keylget var $key]
    }
}

show_stats $dhcp_stats_0 



return "SUCCESS - $test_name - [clock format [clock seconds]]"

