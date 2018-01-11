################################################################################
# Version 1.0    $Revision: 1 $
# $Author: E. Tutescu $
#
#    Copyright © 1997 - 2012 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    24-01-2012 E. Tutescu - Created sample
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
#    This sample creates one connected and one unconnected interface and then  #
# creates a gre interface attached to the unconnected one.                     #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a XM12 module.                                   #
#                                                                              #
################################################################################
package require Ixia

# Setting session variables
set test_name                   [info script]
set chassis_ip                  10.205.16.98
set ixnetwork_tcl_server        localhost
set port_list                   [list 7/3]

set autonegotiation             0
set netmask                     255.255.255.0
set ip                          19.19.19.2
set ipv6                        19::2
set unconnected_ip              19.19.19.3
set unconnected_ipv6            19::3
set ipv6_prefix_length          64
set gateway                     19.19.19.1
set mac                         0000.0000.0001

set intf_mode                   ethernet
set gre_dst_ip_addr             239.1.1.1
set gre_key_enable              0
set gre_checksum_enable         0
set gre_ip_addr                 3.3.3.3
set gre_ip_prefix_length        32

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect                                            \
        -reset                                                                 \
        -device               $chassis_ip                                      \
        -port_list            $port_list                                       \
        -ixnetwork_tcl_server $ixnetwork_tcl_server                            \
        -username             ixiaApiUser                                      \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set i 0
set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
        set port_$i $temp_port
        incr i
    }
}

# Creating a connected interface
set interface_status [::ixia::interface_config                                 \
    -port_handle      $port_0                                                  \
    -intf_mode        ethernet                                                 \
    -netmask          $netmask                                                 \
    -intf_ip_addr     $ip                                                      \
    -ipv6_intf_addr   $ipv6                                                    \
    -ipv6_prefix_length   $ipv6_prefix_length                                  \
    -gateway          $gateway                                                 \
    -src_mac_addr     $mac                                                     \
    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

# Creating an unconnected interface
set interface_status [::ixia::interface_config                                 \
    -port_handle            $port_0                                            \
    -intf_mode              ethernet                                           \
    -netmask                $netmask                                           \
    -intf_ip_addr           $unconnected_ip                                    \
    -ipv6_intf_addr         $unconnected_ipv6                                  \
    -ipv6_prefix_length     $ipv6_prefix_length                                \
    -gateway                $ip                                                \
    -src_mac_addr           $mac                                               \
    -check_gateway_exists   1                                                  \
    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

# Creating a gre interface attached to the existing connected interface
set interface_status [::ixia::interface_config                                 \
    -port_handle            $port_0                                            \
    -intf_ip_addr           $unconnected_ip                                    \
    -gre_dst_ip_addr        $gre_dst_ip_addr                                   \
    -gre_key_enable         $gre_key_enable                                    \
    -gre_key_in             100                                                \
    -gre_key_out            200                                                \
    -gre_checksum_enable    $gre_checksum_enable                               \
    -gre_ip_addr            $gre_ip_addr                                       \
    -src_mac_addr           $mac                                               \
    -gateway                $ip                                                \
    -check_gateway_exists   1                                                  \
    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
