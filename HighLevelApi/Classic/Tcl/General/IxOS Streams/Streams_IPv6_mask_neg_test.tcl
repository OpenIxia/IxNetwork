################################################################################
# Version 1    $Revision: 0 $
# $Author: RAntonescu $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log: 
#       02-08-2008 RAntonescu - created sample
#    
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
#    This sample creates a stream for each combination of ipv6 source type,    #
#    ipv6 destination type, ipv6 increment mode, and some custom masks.        #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET26.                                      #
#                                                                              #
################################################################################
package req Ixia

set chassis_name sylvester
set port_list 3/1

set test_name [info script]

################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
################################################################################
set connect_status [ixia::connect   \
        -device     $chassis_name   \
        -port_list  $port_list      \
        -reset                      \
        -username   ixiaApiUser     \
        ]
if {[keylget connect_status status] == $::FAILURE} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
}

set port_handle [keylget connect_status port_handle.$chassis_name.$port_list]

################################################################################
# Configure interface in the test
################################################################################
set interface_status [ixia::interface_config    \
        -port_handle $port_handle               \
        -ipv6_intf_addr 2500::1                 \
        -intf_ip_addr 123.1.1.2                 \
        ]
if {[keylget interface_status status] == $::FAILURE} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

################################################################################
# Specified range not supported for current mode
################################################################################
set traffic_status  [ixia::traffic_config                           \
         -mode                      create                          \
         -port_handle               $port_handle                    \
         -l3_protocol               ipv6                            \
         -ipv6_src_addr             0::01:FE                        \
         -ipv6_src_mode             incr_host                       \
         -ipv6_src_mask             64                              \
         -ipv6_src_count            3                               \
         -ipv6_src_step             0000:0000:0000:0001::0          \
         -ipv6_dst_step             1000::                          \
         -ipv6_dst_addr             2006::1                         \
         -ipv6_dst_mode             increment                       \
         -ipv6_dst_count            3                               \
         -l3_length                 512                             \
         -rate_bps                  100                             \
         -mac_dst_mode              discovery                       \
         -vlan_id_mode              increment                       \
         -vlan_id                   100                             \
         -vlan_id_count             3                               \
         -vlan_id_step              2                               \
         -signature_offset          100                             \
         -enable_pgid               0                               \
]
if {[keylget traffic_status status] == $::SUCCESS} {
    puts "FAIL - $test_name - traffic_config did not returned error for\
            unsupported mask."
    return
}

################################################################################
# Specify mode with invalid increment mode for specified ipv6
################################################################################
set traffic_status  [ixia::traffic_config                           \
         -mode                      create                          \
         -port_handle               $port_handle                    \
         -l3_protocol               ipv6                            \
         -ipv6_dst_addr             400::                           \
         -ipv6_dst_mode             incr_intf_id                    \
         -ipv6_dst_count            3                               \
         -ipv6_src_mode             decrement                       \
         -l3_length                 512                             \
         -rate_bps                  100                             \
         -mac_dst_mode              discovery                       \
         -vlan_id_mode              increment                       \
         -vlan_id                   100                             \
         -vlan_id_count             3                               \
         -vlan_id_step              2                               \
         -signature_offset          100                             \
         -enable_pgid               0                               \
]
if {[keylget traffic_status status] == $::SUCCESS} {
    puts "FAIL - $test_name - Traffic config did not returned error for\
            invalid increment mode."
    return
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
