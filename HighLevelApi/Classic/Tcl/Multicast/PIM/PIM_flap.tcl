################################################################################
# Version 1.0    $Revision: 1 $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10-10-2007
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
#
# Description:
#    This sample configures a setup which shows PIM flapping functionality.
#
#   +---------+          +--------+
#   |Ixia Port|----------|DUT Port|
#   +---------+          +--------+
#      OSPF                 OSPF
#      PIM                  PIM
#
#   DUT configuration:
# ip multicast-routing
# interface loopback 20 
# ip address 24.0.0.1 255.255.255.255
# ip pim sparse-mode
# ip ospf hello-interval 10
# ip ospf dead-interval 40
# exit
# 
# router ospf 21
# router-id 23.255.255.255
# network 24.0.0.1 0.0.0.0 area 0
# network 23.3.3.0 0.0.0.255 area 0
# exit
# 
# ip pim rp-address 24.0.0.1
# 
# interface gigabitEthernet 7/36
# no shutdown
# ip address 23.3.3.1 255.255.255.0
# ip pim sparse-mode
# ip pim query-interval 2
# ip ospf hello-interval 10
# ip ospf dead-interval 40
# end
#
# debug ip pim 225.0.0.0
# term mon
#
# Module:
#    The sample was tested on a LM1000STXS4
#    The sample was tested with HLTSET27
#
################################################################################

set ixia_ip_address 23.3.3.100
set dut_ip_address  23.3.3.1
set rp_address      24.0.0.1
set group_address   225.0.0.0

package require Ixia

set test_name [info script]

set start_time [clock clicks -milliseconds]
set totalTime  0

set chassisIP sylvester
set port_list [list 2/1]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username  ixiaApiUser      ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
            temp_port]} {
        lappend port_handle $temp_port
    }
}
set port_0 [lindex $port_handle 0]
##############################################################################
# Configure interface in the test      
# IPv4                                 
##############################################################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_0               \
        -speed           auto                  \
        -duplex          auto                  \
        -autonegotiation 1                     ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}

set ospf_status [::ixia::emulation_ospf_config        \
        -port_handle                $port_0           \
        -session_type               ospfv2            \
        -intf_ip_addr               $ixia_ip_address  \
        -neighbor_intf_ip_addr      $dut_ip_address   \
        -mode                       create            \
        -count                      1                 \
        -router_id                  0.0.0.1           \
        -area_type                  external-capable  \
        -authentication_mode        null              \
        -dead_interval              40                \
        -hello_interval             10                \
        -network_type               broadcast         \
        -option_bits                "0x02"            ]
if {[keylget ospf_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospf_status log]"
    return
}

set ospf_status [::ixia::emulation_ospf_control \
        -port_handle        $port_handle     \
        -mode               start             ]
if {[keylget ospf_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospf_status log]"
    return 0
}

##############################################################################
#  Configure a PIM neighbor 
##############################################################################
set pim_config_status [::ixia::emulation_pim_config     \
        -mode                   create                  \
        -port_handle            $port_0                 \
        -count                  1                       \
        -ip_version             4                       \
        -intf_ip_addr           $ixia_ip_address        \
        -intf_ip_addr_step      0.0.1.0                 \
        -intf_ip_prefix_length     24                   \
        -router_id              11.0.0.1                \
        -router_id_step         0.0.0.1                 \
        -neighbor_intf_ip_addr  $dut_ip_address         \
        -gateway_intf_ip_addr   $dut_ip_address         \
        -dr_priority            10                      \
        -bidir_capable          0                       \
        -hello_interval         10                      \
        -hello_holdtime         20                      \
        -join_prune_interval    20                      \
        -join_prune_holdtime    30                      \
        -prune_delay_enable     1                       \
        -prune_delay            600                     \
        -override_interval      700                     \
        -prune_delay_tbit       1                       \
        -send_generation_id     1                       \
        -generation_id_mode     random                  ]
if {[keylget pim_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_config_status log]"
    return 0
}
set port1_session_handle [lindex [keylget pim_config_status handle] 0]

set pim_mconfig_status [::ixia::emulation_multicast_group_config \
        -mode               create          \
        -num_groups         1               \
        -ip_addr_start      $group_address  \
        -ip_addr_step       0.0.0.1         \
        -ip_prefix_len      24              \
        ]

if {[keylget pim_mconfig_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_mconfig_status log]"
    return 0
}

set group_pool_handle [keylget pim_mconfig_status handle]

set pim_gr_config_status [::ixia::emulation_pim_group_config\
        -mode                          create               \
        -session_handle                $port1_session_handle\
        -group_pool_handle             $group_pool_handle   \
        -rp_ip_addr                    24.0.0.1             \
        -group_pool_mode               send                 \
        -join_prune_aggregation_factor 10                   \
        -rate_control                   1                   \
        -interval                       100                 \
        -join_prune_per_interval        99                  \
        -register_per_interval          101                 \
        -register_stop_per_interval     102                 \
        -spt_switchover                 0                   \
        -switch_over_interval           200                 \
        ]

if {[keylget pim_gr_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_gr_config_status log]"
    return 0
}

set pim_control_status [::ixia::emulation_pim_control         \
        -mode                           start               \
        -flap                           1                   \
        -flap_interval                  3                   \
        -handle           [keylget pim_config_status handle]]
if {[keylget pim_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_control_status log]"
    return 0
}

set total_time [expr [clock clicks -milliseconds] - $start_time]
puts   "SUCCESS - $total_time - $totalTime"
return 1
