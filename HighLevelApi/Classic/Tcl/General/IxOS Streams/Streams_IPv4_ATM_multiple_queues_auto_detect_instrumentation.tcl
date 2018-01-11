################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    02-08-2008 LRaicea - Created lists of parameters for interface_config
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
#    This sample configures an ATM interface and creates streams.              #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM622MR module.                                #
#    The sample was tested with HLTSET26.                                      #
#                                                                              #
################################################################################

set env(IXIA_VERSION) HLTSET26

package require Ixia

set test_name [info script]

set chassisIP 10.205.19.228
set port_list [list 3/1]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect                                         \
        -reset                                                              \
        -device                             $chassisIP                      \
        -port_list                          $port_list                      \
        -username                           ixiaApiUser                     \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
}
set port_0 [keylget connect_status port_handle.$chassisIP.$port_list]

################################################################################
# Configure interface in the test 
################################################################################
set port_handle_list                    ""
set intf_mode_list                      ""
set intf_ip_addr_list                   ""
set gateway_list                        ""
set netmask_list                        ""
set src_mac_addr_list                   ""
set atm_enable_coset_list               ""
set atm_enable_pattern_matching_list    ""
set atm_filler_cell_list                ""
set atm_interface_type_list             ""
set atm_packet_decode_mode_list         ""
set atm_reassembly_timeout_list         ""

for {set i 1} {$i <= 2} {incr i} {
    lappend port_handle_list                    $port_0
    lappend intf_mode_list                      atm
    lappend intf_ip_addr_list                   12.1.$i.2
    lappend gateway_list                        12.1.$i.1
    lappend netmask_list                        255.255.255.0
    lappend src_mac_addr_list                   0000.debb.00[format "%02x" $i]
    lappend atm_enable_coset_list               0
    lappend atm_enable_pattern_matching_list    0
    lappend atm_filler_cell_list                idle
    lappend atm_interface_type_list             nni
    lappend atm_packet_decode_mode_list         cell
    lappend atm_reassembly_timeout_list         5
}

set interface_status [::ixia::interface_config                              \
        -port_handle                    $port_handle_list                   \
        -intf_mode                      $intf_mode_list                     \
        -intf_ip_addr                   $intf_ip_addr_list                  \
        -gateway                        $gateway_list                       \
        -netmask                        $netmask_list                       \
        -src_mac_addr                   $src_mac_addr_list                  \
        -atm_enable_coset               $atm_enable_coset_list              \
        -atm_enable_pattern_matching    $atm_enable_pattern_matching_list   \
        -atm_filler_cell                $atm_filler_cell_list               \
        -atm_interface_type             $atm_interface_type_list            \
        -atm_packet_decode_mode         $atm_packet_decode_mode_list        \
        -atm_reassembly_timeout         $atm_reassembly_timeout_list        \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}
################################################################################
# Clear all streams
################################################################################
set traffic_status [::ixia::traffic_config                                  \
        -mode                               reset                           \
        -port_handle                        $port_0                         \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}
################################################################################
# Configure stream 1
################################################################################
set traffic_status [::ixia::traffic_config                                  \
        -mode                               create                          \
        -port_handle                        $port_0                         \
        -l3_protocol                        ipv4                            \
        -ip_src_addr                        12.1.1.1                        \
        -ip_dst_addr                        12.1.1.2                        \
        -rate_percent                       5                               \
        -l2_encap                           atm_vc_mux_802.3snap            \
        -mac_dst_mode                       discovery                       \
        -mac_src                            0000.debb.0001                  \
        -length_mode                        auto                            \
        -enable_auto_detect_instrumentation 1                               \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}
################################################################################
# Configure stream 2
################################################################################
set traffic_status [::ixia::traffic_config                                  \
        -mode                               create                          \
        -port_handle                        $port_0                         \
        -multiple_queues                    1                               \
        -l3_protocol                        ipv4                            \
        -ip_src_addr                        12.1.2.1                        \
        -ip_dst_addr                        12.1.2.2                        \
        -rate_percent                       5                               \
        -l2_encap                           atm_vc_mux_802.3snap            \
        -mac_dst_mode                       discovery                       \
        -mac_src                            0000.debb.0002                  \
        -length_mode                        auto                            \
        -enable_auto_detect_instrumentation 1                               \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return
