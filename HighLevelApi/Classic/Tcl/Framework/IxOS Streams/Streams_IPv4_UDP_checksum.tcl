################################################################################
# Version 1.0    $Revision: 1 $
# $Author: RAntonescu $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    
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
#    This sample configures an IPv4 UDP stream which have a                    #
#    custom UDP checksum. It also configure transmit port with -ignore_link    #
#    which let traffic to run even if port link is down.                       #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET26                                       #
#                                                                              #
################################################################################
set env(IXIA_VERSION) HLTSET26
package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 3/3 3/4]

################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
################################################################################
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username  ixiaApiUser      \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [::ixia::get_port_list_from_connect $connect_status $chassisIP\
        $port_list]
set port_0 [lindex $port_handle 0]
set port_1 [lindex $port_handle 1]

################################################################################
# Configure interfaces in the test
################################################################################
set interface_status [::ixia::interface_config           \
        -port_handle     $port_0          $port_1        \
        -intf_ip_addr    12.1.3.2         12.1.3.1       \
        -netmask         255.255.255.0    255.255.255.0  \
        -autonegotiation 1                1              \
        -ignore_link     1                0              \
        -op_mode         normal           sim_disconnect \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Delete all the streams first
################################################################################
set traffic_status [::ixia::traffic_config  \
        -mode        reset                  \
        -port_handle $port_0                \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Configure the streams on the first IpV4 port
################################################################################
set traffic_status [::ixia::traffic_config  \
        -mode         create                \
        -port_handle  $port_0               \
        -name         "hltapi UDP"          \
        -l3_protocol  ipv4                  \
        -l4_protocol  udp                   \
        -udp_src_port 123                   \
        -udp_dst_port 4004                  \
        -udp_checksum 1                     \
        -udp_checksum_value 0x1234          \
        -enable_time_stamp  0               \
        -ip_src_addr  12.1.3.2              \
        -ip_dst_addr  12.1.3.1              \
        -l3_length    100                   \
        -rate_percent 50                    \
        -mac_dst_mode discovery             \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Start traffic on first port
################################################################################
set traffic_status [::ixia::traffic_control \
        -port_handle $port_0                \
        -action run                         \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
