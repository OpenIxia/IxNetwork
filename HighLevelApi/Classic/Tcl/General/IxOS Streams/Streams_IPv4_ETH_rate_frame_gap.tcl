################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mirce Hasegan $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10-19-2007 Mircea Hasegan
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
#    This sample creates IPv4 streams on a port using -rate_frame_gap          #
#    parameter.                                                                #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET26.                                      #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 3/1]

# Connect to the chassis,reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username  ixiaApiUser      ]
if {[keylget connect_status status] != $SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [keylget connect_status port_handle.$chassisIP.$port_list]

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config  \
        -port_handle     $port_handle           \
        -intf_ip_addr    12.1.3.2               \
        -gateway         12.1.3.1               \
        -netmask         255.255.255.0          \
        -autonegotiation 0                      \
        -src_mac_addr    0000.0005.0001         \
        -transmit_mode   stream                 ]
if {[keylget interface_status status] != $SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}


# Delete all the streams first
set traffic_status [::ixia::traffic_config \
        -mode        reset                 \
        -port_handle $port_handle          ]
if {[keylget traffic_status status] != $SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

# Configure stream 1 with -rate_frame_gap 0
set traffic_status [::ixia::traffic_config \
        -mode         create               \
        -port_handle  $port_handle         \
        -rate_frame_gap 0                  \
        -l3_protocol  ipv4                 \
        -ip_src_addr  12.1.1.1             \
        -ip_dst_addr  12.1.1.2             \
        -l3_length    100                  \
        -mac_dst_mode discovery            \
        -mac_src      0000.0005.0001       \
        -inter_burst_gap    20             \
        -inter_stream_gap   15             \
        -burst_loop_count   5              \
        ]
if {[keylget traffic_status status] != $SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

# Configure stream 2 with -rate_frame_gap 100
set traffic_status [::ixia::traffic_config \
        -mode         create               \
        -port_handle  $port_handle         \
        -rate_frame_gap 100                \
        -l3_protocol  ipv4                 \
        -ip_src_addr  12.1.1.1             \
        -ip_dst_addr  12.1.1.2             \
        -l3_length    100                  \
        -mac_dst_mode discovery            \
        -mac_src      0000.0005.0001       ]
if {[keylget traffic_status status] != $SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

# Configure stream 3 with -rate_frame_gap 70
set traffic_status [::ixia::traffic_config \
        -mode         create               \
        -port_handle  $port_handle         \
        -rate_frame_gap 70                 \
        -l3_protocol  ipv4                 \
        -ip_src_addr  12.1.1.1             \
        -ip_dst_addr  12.1.1.2             \
        -l3_length    100                  \
        -mac_dst_mode discovery            \
        -mac_src      0000.0005.0001       ]
if {[keylget traffic_status status] != $SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}
set streamId [keylget traffic_status stream_id]

# Modify stream 3 with -rate_frame_gap 50
set traffic_status [::ixia::traffic_config \
        -mode         modify               \
        -port_handle  $port_handle         \
        -stream_id    $streamId            \
        -rate_frame_gap  50                ]
if {[keylget traffic_status status] != $SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
