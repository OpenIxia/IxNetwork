################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Karim $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    4-25-2003 Karim
#    14-02-2008 RAntonescu - Add router solicitation check 
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
# meet the user’s requirements or (ii) that the script will be without      #
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
#    This sample configures an IPv6 stream.                                    #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET26.                                      #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 127.0.0.1
set port_list [list 10/1]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username  ixiaApiUser      \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
}

set port_0 [keylget connect_status port_handle.$chassisIP.$port_list]

########################################
# Configure interface in the test      #
# IPv6                                 #
########################################
set interface_status [::ixia::interface_config  \
        -port_handle        $port_0             \
        -ipv6_intf_addr     30::31              \
        -ipv6_prefix_length 64                  \
        -autonegotiation    1                   \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################
# Configure the streams on the first IpV4 port #
################################################
set traffic_status [::ixia::traffic_config  \
        -mode                create         \
        -port_handle         $port_0        \
        -name                "hltapi IpV6"  \
        -l3_protocol         ipv6           \
        -ipv6_traffic_class  2              \
        -ipv6_flow_label     55             \
        -ipv6_hop_limit      100            \
        -ipv6_src_addr       30::31         \
        -ipv6_src_mode       "fixed"        \
        -ipv6_dst_addr       55::50         \
        -ipv6_dst_mode       "fixed"        \
        -ipv6_frag_offset    7000           \
        -ipv6_frag_id        123456         \
        -ipv6_frag_more_flag                \
        -l3_length           74             \
        -rate_percent        50             \
        -mac_dst_mode        discovery      \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

# A router solicitation is sent. Because there is no DUT configured in the test
# there will be no response
if {0} {
    set interface_status [::ixia::interface_config  \
            -port_handle     $port_0                \
            -arp_send_req    1                      \
            ]
    if {[keylget interface_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget interface_status log]"
        return
    }
    if {[catch {set failed_arp [keylget interface_status \
            $port_0.router_solicitation_success]}] || $failed_arp == 0} {
        set returnLog "FAIL - $test_name - Router Solicitation send request failed. "
        if {![catch {set intf_list [keylget interface_status \
                $port_0.arp_ipv6_interfaces_failed]}]} {
            append returnLog "ARP failed on interfaces: $intf_list."
        }
        puts $returnLog
        return
    }
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return
