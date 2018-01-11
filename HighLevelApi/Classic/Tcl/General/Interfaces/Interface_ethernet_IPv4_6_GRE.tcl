################################################################################
# Version 1.1    $Revision: 2 $
# $Author: Radu Antonescu $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    7-06-2003 Radu Antonescu
#    7-27-2003 Matei-Eugen Vasile
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
#    This sample configures 3 interfaces on an Ethernet port, each with a      #
#    single GRE interface attached.                                            #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################

package req Ixia
set test_name [info script]

set chassisIP 10.205.19.96
set port_list [list 2/1]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                \
        -device    $chassisIP \
        -port_list $port_list \
        -username  ixiaApiUser]

if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [::ixia::get_port_list_from_connect $connect_status $chassisIP \
        $port_list]

########################################
# Configure interface in the test      #
#                                      #
# IPv6                                 #
########################################
set interface_status [::ixia::interface_config      \
        -port_handle                $port_handle    \
        -autonegotiation            1               \
        -duplex                     auto            \
        -speed                      auto            \
        -gre_ip_addr                176.13.221.67   \
        -ipv6_intf_addr             1::3            \
        -ipv6_prefix_length         64              \
        -gre_dst_ip_addr            141:85::99:1    \
        -gre_key_enable             1               \
        -gre_key_in                 100             \
        -gre_key_out                200             \
        ]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

########################################
# Configure interface in the test      #
#                                      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config                                  \
        -port_handle                [list   $port_handle    $port_handle    ]   \
        -autonegotiation            [list   1               1               ]   \
        -duplex                     [list   auto            auto            ]   \
        -speed                      [list   auto            auto            ]   \
        -intf_ip_addr               [list   192.168.1.2     192.168.2.2     ]   \
        -gateway                    [list   192.168.1.1     192.168.2.1     ]   \
        -netmask                    [list   255.255.255.0   255.255.255.0   ]   \
        -gre_ipv6_addr              [list   12:13::15       131:231:45::12  ]   \
        -gre_dst_ip_addr            [list   172.16.0.1      144.12.65.34    ]   \
        -gre_key_enable             [list   1               0               ]   \
        -gre_checksum_enable        [list   1                               ]   \
        -gre_key_in                 [list   110             1               ]   \
        -gre_key_out                [list   210             1               ]   \
        ]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
