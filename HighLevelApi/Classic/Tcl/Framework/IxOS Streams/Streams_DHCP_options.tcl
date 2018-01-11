################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2006 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    11-08-2006 LRaicea
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
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample creates a DHCP streams on an Ixia port.                       #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM100TXS8 module.                              #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 127.0.0.1
set port_list [list 10/3]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username  ixiaApiUser      ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [keylget connect_status port_handle.$chassisIP.$port_list]


################################################################################
# Configure interface in the test
################################################################################
set interface_status [::ixia::interface_config  \
        -port_handle     $port_handle           \
        -autonegotiation 1                      ]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Delete all the streams first
################################################################################
set traffic_status [::ixia::traffic_config \
        -mode        reset                 \
        -port_handle $port_handle          ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Configure DHCP stream using various DHCP options
################################################################################
set traffic_status [::ixia::traffic_config        \
        -mode                create               \
        -port_handle         $port_handle         \
        -transmit_mode       single_burst         \
        -pkts_per_burst      1                    \
        -length_mode         auto                 \
        -rate_percent        1                    \
        -l3_protocol         ipv4                 \
        -l4_protocol         dhcp                 \
        -dhcp_operation_code reply                \
        -dhcp_hw_type        1                    \
        -dhcp_hw_len         6                    \
        -dhcp_flags          broadcast            \
        -dhcp_your_ip_addr   192.168.18.154       \
        -dhcp_client_hw_addr 01.02.03.04.05.06    \
        -dhcp_server_ip_addr 192.168.18.2         \
        -dhcp_option  {
            dhcp_subnet_mask
            dhcp_gateways
            dhcp_name_server
            dhcp_domain_name
            dhcp_net_bios_scope
            dhcp_param_request_list
        } \
        -dhcp_option_data  {
            255.255.255.0
            192.168.18.254
            192.168.18.2
            ixiacom.com
            cc.ee.22.11.33.ff
            {
                dhcp_subnet_mask
                dhcp_gateways 
                dhcp_domain_name_server 
                dhcp_domain_name
                dhcp_net_bios_name_svr
                dhcp_net_bios_node_type
                dhcp_net_bios_scope
            }
        }]

if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
