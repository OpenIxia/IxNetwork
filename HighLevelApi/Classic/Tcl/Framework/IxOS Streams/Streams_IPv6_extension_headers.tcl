#################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-08-2006 LRaicea
#    14-02-2008 RAntonescu - Add router solicitation check 
#
#################################################################################

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
#    This sample creates an IPv6 stream with extension headers.                #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#    The sample was tested with HLTSET26.                                      #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 127.0.0.1
set port_list [list 1/1]

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
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
}

set port_0 [keylget connect_status port_handle.$chassisIP.$port_list]


################################################################################
# Configure interface in the test
################################################################################
set interface_status [::ixia::interface_config \
        -mode               config             \
        -port_handle        $port_0            \
        -ipv6_intf_addr     1:2:3:0:0:0:0:100  \
        -ipv6_prefix_length 64                 \
        -src_mac_addr       0123.0123.0123     \
        -autonegotiation    1                  \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

################################################################################
# Set hop by hop extension key vars
################################################################################
set hopt_1 ""
keylset hopt_1 type   padn
keylset hopt_1 length 4
keylset hopt_1 value  11.11.11.11

set hopt_2  ""
keylset hopt_2 type     jumbo
keylset hopt_2 length   4
keylset hopt_2 payload  5

set hopt_3 ""
keylset hopt_3 type   padn
keylset hopt_3 length 6
keylset hopt_3 value  22.22.22.22.22.22

set hopt_4  ""
keylset hopt_4 type        router_alert
keylset hopt_4 length      2
keylset hopt_4 alert_type  mld

set hopt_5 ""
keylset hopt_5 type   padn
keylset hopt_5 length 2
keylset hopt_5 value  00.00

set hopt_6 ""
keylset hopt_6 type   pad1

set hopt_7 ""
keylset hopt_7 type   padn
keylset hopt_7 length 5
keylset hopt_7 value  33.33.33.33.33

set hopt_8  ""
keylset hopt_8 type        router_alert
keylset hopt_8 length      3
keylset hopt_8 alert_type  rsvp

set hopt_9 ""
keylset hopt_9 type   padn
keylset hopt_9 length 5
keylset hopt_9 value  44.44.44.44.44

set hopt_10 ""
keylset hopt_10 type   padn
keylset hopt_10 length 2
keylset hopt_10 value  88.88

set hopt_11 ""
keylset hopt_11 type   padn
keylset hopt_11 length 1
keylset hopt_11 value  00


set hopt_12 ""
keylset hopt_12 type       binding_update
keylset hopt_12 length     10
keylset hopt_12 ack        1
keylset hopt_12 home       1
keylset hopt_12 router     1
keylset hopt_12 duplicate  1
keylset hopt_12 map        1
keylset hopt_12 bicast     1
keylset hopt_12 prefix_len 5
keylset hopt_12 seq_num    5
keylset hopt_12 life_time  5

set hopt_13 ""
keylset hopt_13 type   padn
keylset hopt_13 length 4
keylset hopt_13 value  30.45.45.45

set hopt_14 ""
keylset hopt_14 type       binding_ack
keylset hopt_14 length     13
keylset hopt_14 seq_num    40
keylset hopt_14 life_time  4
keylset hopt_14 status     4
keylset hopt_14 refresh    4

set hopt_15 ""
keylset hopt_15 type   padn
keylset hopt_15 length 4
keylset hopt_15 value  44.44.44.44

set hopt_16 ""
keylset hopt_16 type   padn
keylset hopt_16 length 3
keylset hopt_16 value  00.00.00

set hopt_17 ""
keylset hopt_17 type   padn
keylset hopt_17 length 4
keylset hopt_17 value  22.22.22.16

set hopt_18 ""
keylset hopt_18 type       binding_req
keylset hopt_18 length     9

set hopt_19 ""
keylset hopt_19 type   padn
keylset hopt_19 length 4
keylset hopt_19 value  00.00.00.00

set hopt_20 ""
keylset hopt_20 type        mipv6_unique_id_sub
keylset hopt_20 length      24
keylset hopt_20 sub_unique  89

set hopt_21 ""
keylset hopt_21 type   padn
keylset hopt_21 length 2
keylset hopt_21 value  10.13

set hopt_22 ""
keylset hopt_22 type     mipv6_alternative_coa_sub
keylset hopt_22 length   20
keylset hopt_22 address  1414:1414:1414:1414:1414:1414:0:5


set hopt_23 ""
keylset hopt_23 type   padn
keylset hopt_23 length 4
keylset hopt_23 value  00.00.00.00

set hopt_options ""
for {set i 1} {$i < 24} {incr i} {
    if {[info exists hopt_$i]} {
        lappend hopt_options [set hopt_$i]
    }
}

set ropt_node_list [list                        \
        7777:7777:7777:7777:7777:7777:7777:7777 \
        8888:8888:8888:8888:8888:8888:8888:8888 ]

set aopt_payload [join [list \
        44 44 44 44 44 44 44 44 44 44 44 44 44 44 \
        44 44 44 44 44 44 44 44 44 44 44 44 44 44 ] "."]


set ipv6_next_header        [list \
        routing         destination fragment authentication hop_by_hop   ]

set ipv6_routing_node_list  [list \
        $ropt_node_list N/A         N/A      N/A            N/A          ]

set ipv6_routing_res        [list \
        88.88.88.88     N/A         N/A      N/A            N/A          ]

set ipv6_frag_offset        [list \
        N/A             N/A         345      N/A            N/A          ]

set ipv6_frag_more          [list \
        N/A             N/A         0        N/A            N/A          ]

set ipv6_frag_id            [list \
        N/A             N/A         345      N/A            N/A          ]

set ipv6_frag_res_2bit      [list \
        N/A             N/A         1        N/A            N/A          ]

set ipv6_frag_res_8bit      [list \
        N/A             N/A         121      N/A            N/A          ]

set ipv6_auth_payload_len   [list \
        N/A             N/A         N/A      8              N/A          ]

set ipv6_auth_spi           [list \
        N/A             N/A         N/A      1212           N/A          ]

set ipv6_auth_seq_num       [list \
        N/A             N/A         N/A      3434           N/A          ]

set ipv6_auth_string        [list \
        N/A             N/A         N/A      $aopt_payload  N/A          ]

set ipv6_hop_by_hop_options [list \
        N/A             N/A         N/A      N/A            $hopt_options]

################################################################################
# Configure the IPv6 stream
################################################################################
set traffic_status [::ixia::traffic_config                \
        -mode                    create                   \
        -port_handle             $port_0          	      \
        -name                    "hltapi IpV6"            \
        -l4_protocol             tcp                      \
        -tcp_src_port            1230                     \
        -tcp_dst_port            4560                     \
        -l3_protocol             ipv6                     \
        -ipv6_traffic_class      3                        \
        -ipv6_src_addr           1:2:3:0:0:0:0:100        \
        -ipv6_src_mode           fixed                    \
        -ipv6_dst_addr           4:5:6:0:0:0:0:100        \
        -ipv6_dst_mode           fixed                    \
        -rate_percent            50                       \
        -length_mode             auto                     \
        -mac_dst_mode            discovery                \
        -ipv6_extension_header   $ipv6_next_header        \
        -ipv6_routing_node_list  $ipv6_routing_node_list  \
        -ipv6_routing_res        $ipv6_routing_res        \
        -ipv6_frag_offset        $ipv6_frag_offset        \
        -ipv6_frag_more_flag     $ipv6_frag_more          \
        -ipv6_frag_id            $ipv6_frag_id            \
        -ipv6_frag_res_2bit      $ipv6_frag_res_2bit      \
        -ipv6_frag_res_8bit      $ipv6_frag_res_8bit      \
        -ipv6_auth_payload_len   $ipv6_auth_payload_len   \
        -ipv6_auth_spi           $ipv6_auth_spi           \
        -ipv6_auth_seq_num       $ipv6_auth_seq_num       \
        -ipv6_auth_string        $ipv6_auth_string        \
        -ipv6_hop_by_hop_options $ipv6_hop_by_hop_options \
        ]

if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

# A router solicitation is sent. Because there is no DUT configured in the test
# there will be no response
if {0} {
    set interface_status [::ixia::interface_config  \
            -port_handle     $port_0    		    \
            -arp_send_req    1                      ]
    if {[keylget interface_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget interface_status log]"
        return
    }
    if {[catch {set failed_arp [keylget interface_status \
            $port_0.router_solicitation_success]}] || $failed_arp == 0} {
        set returnLog "FAIL - $test_name - arp send request failed. "
        if {![catch {set intf_list [keylget interface_status $port_0.arp_ipv6_interfaces_failed]}]} {
            append returnLog "Router Solicitation failed on interfaces: $intf_list."
        }
        puts $returnLog
        return
    }
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return
