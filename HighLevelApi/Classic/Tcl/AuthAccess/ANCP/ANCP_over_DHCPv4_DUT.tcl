################################################################################
# Version 1.0    $Revision: 1 $
# $Author: MHasegan $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-18-2006 MHasegan
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
#    This sample configures one ancp sessions and then starts 15 dhcp sessions ##                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10/100/1000 STXS4-256Mb module.                #
#                                                                              #
################################################################################


#DUT CONFIGURATOIN
#conf t
#
#no ip dhcp pool ancp_scalability
#ip dhcp pool ancp_scalability
#   network 175.71.0.0 255.255.0.0
#   default-router 175.71.0.1
#   lease 3
#
#no ipv6 dhcp pool ancp_scalability
#ipv6 dhcp pool ancp_scalability
# prefix-delegation pool ancp_scalability lifetime infinite infinite
#
#no bba-group pppoe monprofileipv4_1
#bba-group pppoe monprofileipv4_1
# virtual-template 3
# sessions per-vc limit 4000
# sessions per-mac limit 65530
# sessions per-vlan limit 65530 inner 65530
#
#no interface GigabitEthernet7/0/0.1
#interface GigabitEthernet7/0/0.1
# encapsulation dot1Q 71 second-dot1q 701
# ip address 175.71.0.1 255.255.0.0
# pppoe enable group monprofileipv4_1
# ipv6 address 2002:175:71:0:1::1/64
# ipv6 enable
# ipv6 ospf 2 area 0
# ipv6 dhcp server ancp_scalability
#
#!
#no interface GigabitEthernet7/0/0.2
#interface GigabitEthernet7/0/0.2
# encapsulation dot1Q 72 second-dot1q 702
# ip address 175.72.0.1 255.255.0.0
# pppoe enable group monprofileipv4_1
# ancp enable
# !
# ipv6 address 2002:175:72:0:1::1/64
#
#
#no interface Virtual-Template3
#interface Virtual-Template3
# ip unnumbered Loopback1
# peer default ip address pool monpoolipv4_1
# peer default ipv6 pool monpoolipv6_1
# ppp authentication pap
#
#no ip local pool monpoolipv4_1
#ip local pool monpoolipv4_1 137.1.1.1 137.1.11.250
#no ipv6 local pool monpoolipv6_1
#ipv6 local pool monpoolipv6_1 2002:ABCD::/48 64
#
#end
#
#tclsh
#
#conf t
#
#for { set i 0 } { $i<=253 } { incr i } {
#    set an [expr 1+$i]    ;# the AN variable
#    for { set y 1 } { $y<=100 } { incr y } {
#	set id [expr $i*100+$y]    ;# the client-ID variable
#	set anip [expr 1+$an]    ;# the access node ip variable
#	set dslid [expr 100000+$id]    ;# the dsl ID variable
#
#	"no ancp neighbor name AN_$an id 175.72.0.$anip"
#	"ancp neighbor name AN_$an id 175.72.0.$anip"
#	"dot1q 72 second-dot1q 702 interface Gi7/0/0.2 client-ID DL$dslid"
#    }
#}
# 
#for { set i 254 } { $i<=319 } { incr i } {
#    set an [expr 1+$i]    ;# the AN variable
#    for { set y 1 } { $y<=100 } { incr y } {
#	set id [expr $i*100+$y]    ;# the client-ID variable
#	set anip [expr $an-255]    ;# the access node ip variable
#	set dslid [expr 100000+$id]    ;# the dsl ID variable
#
#	"no ancp neighbor name AN_$an id 175.72.1.$anip"
#	"ancp neighbor name AN_$an id 175.72.1.$anip"
#	"dot1q 72 second-dot1q 702 interface Gi7/0/0.2 client-ID DL$dslid"
#    }
#}







package require Ixia
set ::ixia::debug 1
set test_name [info script]

set chassis_ip 10.205.17.97
set port_list [list 1/5]

# Connect to the chassis.
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                         \
        -reset                                              \
        -ixnetwork_tcl_server   localhost                   \
        -device                 $chassis_ip                 \
        -port_list              $port_list                  \
        -username               ixiaApiUser                 ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}
set port_handle [keylget connect_status port_handle.$chassis_ip.$port_list]

# Configure physical port attributes
set interface_status [::ixia::interface_config \
        -port_handle       $port_handle        \
        -intf_mode          ethernet           \
        -phy_mode           copper             \
        -autonegotiation    1                  \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}



################################################################################
# START - DHCP Configuration                                                   #
################################################################################

#############################################
# DHCP GENERAL PARAMS                       #
#############################################

set port_handle                    $port_handle    ;# REGEXP ^[0-9]+/[0-9]+/[0-9]+$
set mode                           create     ;# CHOICES create modify reset DEFAULT create
set version                        ixnetwork  ;# CHOICES ixtclhal ixaccess ixnetwork DEFAULT ixtclhal
set reset                          0          ;# FLAG
set no_write                       0          ;# FLAG



#############################################
# DHCP PROTOCOL CONFIG                      #
#############################################

set accept_partial_config          0          ;# CHOICES 0 1 DEFAULT 0
set lease_time                     3600       ;# RANGE 0-65535 DEFAULT 3600
set max_dhcp_msg_size              576        ;# RANGE 0-65535 DEFAULT 576
set msg_timeout                    4          ;# NUMERIC DEFAULT 4
set outstanding_releases_count     500        ;# RANGE 1-100000 DEFAULT 500
set outstanding_session_count      50         ;# NUMERIC DEFAULT 50
set release_rate                   50         ;# RANGE 1-100000 DEFAULT 50
set release_rate_increment         50         ;# RANGE 1-100000 DEFAULT 50
set request_rate                   10         ;# RANGE 1-100000 DEFAULT 10
set request_rate_increment         50         ;# RANGE 1-100000 DEFAULT 50
set retry_count                    3          ;# RANGE 1-100 DEFAULT 3
set server_port                    67         ;# RANGE 0-65535 DEFAULT 67
set wait_for_completion            0          ;# CHOICES 0 1 DEFAULT 0
set dhcp6_echo_ia_info             0          ;# CHOICES 0 1 DEFAULT 0
set dhcp6_reb_max_rt               600        ;# RANGE 1-10000 DEFAULT 600
set dhcp6_reb_timeout              10         ;# RANGE 1-100 DEFAULT 10
set dhcp6_rel_max_rc               5          ;# RANGE 1-100 DEFAULT 5
set dhcp6_rel_timeout              1          ;# RANGE 1-100 DEFAULT 1
set dhcp6_ren_max_rt               600        ;# RANGE 1-10000 DEFAULT 600
set dhcp6_ren_timeout              10         ;# RANGE 1-100 DEFAULT 10
set dhcp6_req_max_rc               5          ;# RANGE 1-100 DEFAULT 5
set dhcp6_req_max_rt               30         ;# RANGE 1-10000 DEFAULT 30
set dhcp6_req_timeout              1          ;# RANGE 1-100 DEFAULT 1
set dhcp6_sol_max_rc               3          ;# RANGE 1-100 DEFAULT 3
set dhcp6_sol_max_rt               120        ;# RANGE 1-10000 DEFAULT 120
set dhcp6_sol_timeout              1          ;# RANGE 1-100 DEFAULT 1
set msg_timeout_factor             2          ;# RANGE 1-100 DEFAULT 2
set override_global_setup_rate     1          ;# CHOICES 0 1 DEFAULT 1
set override_global_teardown_rate  1          ;# CHOICES 0 1 DEFAULT 1
set release_rate_max               500        ;# RANGE 1-100000 DEFAULT 500
set request_rate_max               50         ;# RANGE 1-100000 DEFAULT 50


#############################################
# IXIA EMULATION DHCP CONFIG FUNCTION     #
#############################################

set dhcp_config_status_0 [::ixia::emulation_dhcp_config             \
    -port_handle                   $port_handle                   \
    -mode                          $mode                          \
    -version                       $version                       \
    -no_write                      $no_write                      \
    -reset                         $reset                         \
    -accept_partial_config         $accept_partial_config         \
    -lease_time                    $lease_time                    \
    -max_dhcp_msg_size             $max_dhcp_msg_size             \
    -msg_timeout                   $msg_timeout                   \
    -outstanding_releases_count    $outstanding_releases_count    \
    -outstanding_session_count     $outstanding_session_count     \
    -release_rate                  $release_rate                  \
    -release_rate_increment        $release_rate_increment        \
    -request_rate                  $request_rate                  \
    -request_rate_increment        $request_rate_increment        \
    -retry_count                   $retry_count                   \
    -server_port                   $server_port                   \
    -wait_for_completion           $wait_for_completion           \
    -dhcp6_echo_ia_info            $dhcp6_echo_ia_info            \
    -dhcp6_reb_max_rt              $dhcp6_reb_max_rt              \
    -dhcp6_reb_timeout             $dhcp6_reb_timeout             \
    -dhcp6_rel_max_rc              $dhcp6_rel_max_rc              \
    -dhcp6_rel_timeout             $dhcp6_rel_timeout             \
    -dhcp6_ren_max_rt              $dhcp6_ren_max_rt              \
    -dhcp6_ren_timeout             $dhcp6_ren_timeout             \
    -dhcp6_req_max_rc              $dhcp6_req_max_rc              \
    -dhcp6_req_max_rt              $dhcp6_req_max_rt              \
    -dhcp6_req_timeout             $dhcp6_req_timeout             \
    -dhcp6_sol_max_rc              $dhcp6_sol_max_rc              \
    -dhcp6_sol_max_rt              $dhcp6_sol_max_rt              \
    -dhcp6_sol_timeout             $dhcp6_sol_timeout             \
    -msg_timeout_factor            $msg_timeout_factor            \
    -override_global_setup_rate    $override_global_setup_rate    \
    -override_global_teardown_rate $override_global_teardown_rate \
    -release_rate_max              $release_rate_max              \
    -request_rate_max              $request_rate_max              \
    ] 

if {[keylget dhcp_config_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dhcp_config_status_0 log]"
    return 0
}

set dhcp_handles_0 [keylget dhcp_config_status_0 handle]
puts "Ixia dhcp handles are: "
update idletasks

set dhcp_list_0 ""

foreach dhcp_handle $dhcp_handles_0 {
    lappend dhcp_list_0 $dhcp_handle
    puts $dhcp_handle
    update idletasks
}



puts "End dhcp configuration ..."
update idletasks


#################################################
#                                               #
#          PORT 0                               #
#                                               #
#################################################



#############################################
# DHCP GROUP GENERAL PARAMS                 #
#############################################

set handle                                        $dhcp_handles_0  ;# ANY
set mode                                          create           ;# CHOICES create modify reset DEFAULT create
set version                                       ixnetwork        ;# CHOICES ixtclhal ixaccess ixnetwork DEFAULT ixtclhal
set target_subport                                0                ;# RANGE 0-3 DEFAULT 0
set no_write                                      0                ;# FLAG


#############################################
# DHCP GROUP INTERFACE PARAMS               #
#############################################



set encap                                         ethernet_ii_qinq      ;# CHOICES ethernet_ii ethernet_ii_vlan ethernet_ii_qinq vc_mux llcsnap DEFAULT ethernet_ii
set num_sessions                                  15               ;# RANGE 1-65536
set qinq_incr_mode                                both             ;# RANGE 1-3 DEFAULT 1
set vlan_id                                       701              ;# RANGE 0-4095 DEFAULT 4094
set vlan_id_count                                 1                ;# RANGE 0-4095 DEFAULT 4094
set vlan_id_outer                                 71               ;# NUMERIC
set vlan_id_outer_count                           1                ;# RANGE 1-4094
set vlan_id_outer_step                            1                ;# RANGE 1-4094
set vlan_id_step                                  1                ;# RANGE 0-4095
set vlan_id_outer_increment_step                  1                ;# RANGE 0-4093
set vlan_id_outer_priority                        1                ;# RANGE 0-7 DEFAULT 0
set vlan_user_priority                            1                ;# RANGE 0-7 DEFAULT 0
set sessions_per_vc                               1                ;# RANGE 1-65535
set pvc_incr_mode                                 vci              ;# CHOICES vci vpi
set vci                                           20               ;# RANGE 0-65535
set vci_count                                     21               ;# RANGE 0-65535
set vci_step                                      8                ;# NUMERIC
set vpi                                           32               ;# RANGE 0-255
set vpi_count                                     6                ;# RANGE 0-255
set vpi_step                                      4                ;# NUMERIC


#############################################
# DHCP GROUP PROTOCOL CONFIG                #
#############################################

set dhcp6_range_duid_enterprise_id                10               ;# NUMERIC DEFAULT 10
set dhcp6_range_duid_type                         duid_llt         ;# CHOICES duid_llt duid_en duid_ll DEFAULT duid_llt
set dhcp6_range_duid_vendor_id                    10               ;# NUMERIC DEFAULT 10
set dhcp6_range_duid_vendor_id_increment          1                ;# NUMERIC DEFAULT 1
set dhcp6_range_ia_id                             10               ;# NUMERIC DEFAULT 10
set dhcp6_range_ia_id_increment                   1                ;# NUMERIC DEFAULT 1
set dhcp6_range_ia_t1                             302400           ;# NUMERIC DEFAULT 302400
set dhcp6_range_ia_t2                             483840           ;# NUMERIC DEFAULT 483840
set dhcp6_range_ia_type                           iana             ;# CHOICES iana iata iapd DEFAULT iana
set dhcp6_range_param_request_list                2                ;# ANY
set dhcp_range_ip_type                            ipv4             ;# CHOICES ipv4 ipv6 DEFAULT ipv4
set dhcp_range_param_request_list                 2                ;# RANGE 2-24
set dhcp_range_relay6_hosts_per_opt_interface_id  1                ;# RANGE 1-100 DEFAULT 1
set dhcp_range_relay6_opt_interface_id            "id-\[001-900\]" ;# ANY DEFAULT "id-\[001-900\]"
set dhcp_range_relay6_use_opt_interface_id        0                ;# CHOICES 0 1 DEFAULT 0
set dhcp_range_relay_address_increment            0.0.0.1          ;# IP DEFAULT 0.0.0.1
set dhcp_range_relay_circuit_id                   CIRCUITID-p      ;# ANY DEFAULT CIRCUITID-p
set dhcp_range_relay_count                        1                ;# RANGE 1-1000000 DEFAULT 1
set dhcp_range_relay_destination                  20.0.0.1         ;# IP DEFAULT 20.0.0.1
set dhcp_range_relay_first_address                20.0.0.100       ;# IP DEFAULT 20.0.0.100
set dhcp_range_relay_first_vlan_id                1                ;# RANGE 1-4094 DEFAULT 1
set dhcp_range_relay_gateway                      20.0.0.1         ;# IP DEFAULT 20.0.0.1
set dhcp_range_relay_hosts_per_circuit_id         1                ;# RANGE 1-100 DEFAULT 1
set dhcp_range_relay_hosts_per_remote_id          1                ;# RANGE 1-100 DEFAULT 1
set dhcp_range_relay_override_vlan_settings       0                ;# CHOICES 0 1 DEFAULT 0
set dhcp_range_relay_remote_id                    REMOTEID-I       ;# ANY DEFAULT REMOTEID-I
set dhcp_range_relay_subnet                       24               ;# RANGE 1-128 DEFAULT 24
set dhcp_range_relay_use_circuit_id               0                ;# CHOICES 0 1 DEFAULT 0
set dhcp_range_relay_use_remote_id                0                ;# CHOICES 0 1 DEFAULT 0
set dhcp_range_relay_use_suboption6               0                ;# CHOICES 0 1 DEFAULT 0
set dhcp_range_relay_vlan_count                   1                ;# RANGE 1-4094 DEFAULT 1
set dhcp_range_relay_vlan_increment               1                ;# RANGE 0-4093 DEFAULT 1
set dhcp_range_renew_timer                        0                ;# NUMERIC DEFAULT 0
set dhcp_range_server_address                     10.0.0.1         ;# IP DEFAULT 10.0.0.1
set dhcp_range_suboption6_address_subnet          24               ;# RANGE 1-32 DEFAULT 24
set dhcp_range_suboption6_first_address           20.1.1.100       ;# IP DEFAULT 20.1.1.100
set dhcp_range_use_first_server                   1                ;# CHOICES 0 1 DEFAULT 1
set dhcp_range_use_relay_agent                    0                ;# CHOICES 0 1 DEFAULT 0
set dhcp_range_use_trusted_network_element        0                ;# CHOICES 0 1 DEFAULT 0
set mac_mtu                                       1500             ;# RANGE 500-9500 DEFAULT 1500
set server_id                                     7.7.7.7          ;# IP
set use_vendor_id                                 0                ;# CHOICES 0 1 DEFAULT 0
set vendor_id                                     Ixia             ;# ANY DEFAULT Ixia


#############################################
# IXIA EMULATION DHCP GROUP CONFIG FUNCTION #
#############################################


set dhcp_group_config_status_0 [::ixia::emulation_dhcp_group_config                               \
    -handle                                       $handle                                       \
    -mode                                         $mode                                         \
    -version                                      $version                                      \
    -target_subport                               $target_subport                               \
    -no_write                                     $no_write                                     \
    -encap                                        $encap                                        \
    -num_sessions                                 $num_sessions                                 \
    -qinq_incr_mode                               $qinq_incr_mode                               \
    -vlan_id                                      $vlan_id                                      \
    -vlan_id_count                                $vlan_id_count                                \
    -vlan_id_outer                                $vlan_id_outer                                \
    -vlan_id_outer_count                          $vlan_id_outer_count                          \
    -vlan_id_outer_step                           $vlan_id_outer_step                           \
    -vlan_id_step                                 $vlan_id_step                                 \
    -vlan_id_outer_increment_step                 $vlan_id_outer_increment_step                 \
    -vlan_id_outer_priority                       $vlan_id_outer_priority                       \
    -vlan_user_priority                           $vlan_user_priority                           \
    -dhcp6_range_duid_enterprise_id               $dhcp6_range_duid_enterprise_id               \
    -dhcp6_range_duid_type                        $dhcp6_range_duid_type                        \
    -dhcp6_range_duid_vendor_id                   $dhcp6_range_duid_vendor_id                   \
    -dhcp6_range_duid_vendor_id_increment         $dhcp6_range_duid_vendor_id_increment         \
    -dhcp6_range_ia_id                            $dhcp6_range_ia_id                            \
    -dhcp6_range_ia_id_increment                  $dhcp6_range_ia_id_increment                  \
    -dhcp6_range_ia_t1                            $dhcp6_range_ia_t1                            \
    -dhcp6_range_ia_t2                            $dhcp6_range_ia_t2                            \
    -dhcp6_range_ia_type                          $dhcp6_range_ia_type                          \
    -dhcp6_range_param_request_list               $dhcp6_range_param_request_list               \
    -dhcp_range_ip_type                           $dhcp_range_ip_type                           \
    -dhcp_range_param_request_list                $dhcp_range_param_request_list                \
    -dhcp_range_relay6_hosts_per_opt_interface_id $dhcp_range_relay6_hosts_per_opt_interface_id \
    -dhcp_range_relay6_opt_interface_id           $dhcp_range_relay6_opt_interface_id           \
    -dhcp_range_relay6_use_opt_interface_id       $dhcp_range_relay6_use_opt_interface_id       \
    -dhcp_range_relay_address_increment           $dhcp_range_relay_address_increment           \
    -dhcp_range_relay_circuit_id                  $dhcp_range_relay_circuit_id                  \
    -dhcp_range_relay_count                       $dhcp_range_relay_count                       \
    -dhcp_range_relay_destination                 $dhcp_range_relay_destination                 \
    -dhcp_range_relay_first_address               $dhcp_range_relay_first_address               \
    -dhcp_range_relay_first_vlan_id               $dhcp_range_relay_first_vlan_id               \
    -dhcp_range_relay_gateway                     $dhcp_range_relay_gateway                     \
    -dhcp_range_relay_hosts_per_circuit_id        $dhcp_range_relay_hosts_per_circuit_id        \
    -dhcp_range_relay_hosts_per_remote_id         $dhcp_range_relay_hosts_per_remote_id         \
    -dhcp_range_relay_override_vlan_settings      $dhcp_range_relay_override_vlan_settings      \
    -dhcp_range_relay_remote_id                   $dhcp_range_relay_remote_id                   \
    -dhcp_range_relay_subnet                      $dhcp_range_relay_subnet                      \
    -dhcp_range_relay_use_circuit_id              $dhcp_range_relay_use_circuit_id              \
    -dhcp_range_relay_use_remote_id               $dhcp_range_relay_use_remote_id               \
    -dhcp_range_relay_use_suboption6              $dhcp_range_relay_use_suboption6              \
    -dhcp_range_relay_vlan_count                  $dhcp_range_relay_vlan_count                  \
    -dhcp_range_relay_vlan_increment              $dhcp_range_relay_vlan_increment              \
    -dhcp_range_renew_timer                       $dhcp_range_renew_timer                       \
    -dhcp_range_server_address                    $dhcp_range_server_address                    \
    -dhcp_range_suboption6_address_subnet         $dhcp_range_suboption6_address_subnet         \
    -dhcp_range_suboption6_first_address          $dhcp_range_suboption6_first_address          \
    -dhcp_range_use_first_server                  $dhcp_range_use_first_server                  \
    -dhcp_range_use_relay_agent                   $dhcp_range_use_relay_agent                   \
    -dhcp_range_use_trusted_network_element       $dhcp_range_use_trusted_network_element       \
    -mac_mtu                                      $mac_mtu                                      \
    -server_id                                    $server_id                                    \
    -use_vendor_id                                $use_vendor_id                                \
    -vendor_id                                    $vendor_id                                    \
    ]

if {[keylget dhcp_group_config_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dhcp_group_config_status_0 log]"
    return 0
}

set dhcp_group_handles_0 [keylget dhcp_group_config_status_0 handle]
puts "Ixia dhcp_group_config handles are: "
update idletasks

set dhcp_group_list_0 ""

foreach dhcp_group_handle $dhcp_group_handles_0 {
    lappend dhcp_group_list_0 $dhcp_group_handle
    puts $dhcp_group_handle
    update idletasks
}



puts "End dhcp group configuration ..."
update idletasks





################################################################################
# START - ANCP configuration - First port
################################################################################
puts "Start ANCP configuration ..."
update idletasks

################################################################################
# ANCP - GENERAL
################################################################################
set device_count                                   10                                 ;# NUMERIC DEFAULT 1
set handle                                         $dhcp_group_handles_0                         ;# ANY 
set mode                                           create                             ;# CHOICES create modify delete enable disable enable_all disable_all DEFAULT create
set ancp_cfg_port_handle                           $port_handle                            ;# ANY 

################################################################################
# ANCP - GLOBAL and PORT
################################################################################
set ancp_standard                                  ietf-ancp-protocol2                ;# Only the default value is supported - CHOICES ietf-ancp-protocol2 gsmp-l2control-config2 DEFAULT ietf-ancp-protocol2
set events_per_interval                            10                                 ;# RANGE 1-300 DEFAULT 10
set global_port_down_rate                          50                                 ;# RANGE 1-300 DEFAULT 50
set global_port_up_rate                            10                                 ;# RANGE 1-300 DEFAULT 10
set global_resync_rate                             50                                 ;# RANGE 1-300 DEFAULT 50
set gsmp_standard                                  gsmp-v3-base                       ;# Only the default value is supported - CHOICES RFC-3292 gsmp-v3-base DEFAULT gsmp-v3-base
set interval                                       1                                  ;# RANGE 1-100 DEFAULT 1
set line_config                                    0                                  ;# Only the default value is supported - CHOICES 0 1 DEFAULT 0
set port_down_rate                                 50                                 ;# RANGE 1-300 DEFAULT 50
set port_resync_rate                               50                                 ;# RANGE 1-300 DEFAULT 50
set port_up_rate                                   50                                 ;# RANGE 1-300 DEFAULT 50
set port_override_globals                          1                                  ;# CHOICES 0 1 DEFAULT 1
set topology_discovery                             1                                  ;# CHOICES 0 1 DEFAULT 1

################################################################################
# ANCP - Access Loop
################################################################################
set access_aggregation                             0                                  ;# CHOICES 0 1 DEFAULT 0
set access_aggregation_dsl_inner_vlan              1                                  ;# RANGE 1-4094 DEFAULT 1
set access_aggregation_dsl_inner_vlan_type         actual_dsl_subscriber_vlan         ;# CHOICES actual_dsl_subscriber_vlan custom DEFAULT actual_dsl_subscriber_vlan
set access_aggregation_dsl_outer_vlan              1                                  ;# RANGE 1-4094 DEFAULT 1
set access_aggregation_dsl_outer_vlan_type         actual_dsl_subscriber_vlan         ;# CHOICES actual_dsl_subscriber_vlan custom DEFAULT actual_dsl_subscriber_vlan

################################################################################
# ANCP - NAS
################################################################################
set keep_alive                                     10000                              ;# RANGE 1000-25000 DEFAULT 10000
set keep_alive_retries                             3                                  ;# RANGE 1-10 DEFAULT 3
set sut_ip_addr                                    175.72.0.1                         ;# IPV4 DEFAULT 20.20.0.1
set sut_service_port                               6068                               ;# RANGE 1-65535 DEFAULT 6068

################################################################################
# ANCP - DSL DISTRIBUTION
################################################################################
set distribution_alg_percentage                    0                                  ;# RANGE 0-100 DEFAULT 0

################################################################################
# ANCP - ACCESS NODE IP
################################################################################
set gateway_incr_mode                              every_subnet                       ;# CHOICES every_subnet every_interface DEFAULT every_subnet
set gateway_ip_addr                                175.72.0.1                         ;# IPV4 DEFAULT 0.0.0.0
set gateway_ip_prefix_len                          16                                 ;# RANGE 0-32 DEFAULT 16
set gateway_ip_step                                0.0.0.1                            ;# IPV4 DEFAULT 0.0.0.0
set intf_ip_addr                                   175.72.0.12                        ;# IPV4 DEFAULT 10.10.10.2
set intf_ip_prefix_len                             16                                 ;# RANGE 0-32 DEFAULT 16
set intf_ip_step                                   0.0.0.1                            ;# IPV4 DEFAULT 0.0.0.1
set local_mss                                      1460                               ;# RANGE 28-9460 DEFAULT 1460

################################################################################
# ANCP - ACCESS NODE MAC
################################################################################
set encap_type                                     ETHERNETII                         ;# CHOICES ETHERNETII SAF SNAP DEFAULT ETHERNETII
set local_mac_addr                                 000a.0abc.0200                     ;# MAC DEFAULT 000a.0a00.0200
set local_mac_step                                 0000.0000.0001                     ;# MAC DEFAULT 0000.0000.0001
set local_mac_addr_auto                            0                                  ;# CHOICES 0 1 DEFAULT 1
set local_mtu                                      1500                               ;# RANGE 500-9500 DEFAULT 1500

################################################################################
# ANCP - ACCESS NODE VLAN
################################################################################
set qinq_incr_mode                                 both                               ;# CHOICES inner outer both DEFAULT both
set vlan_id                                        72                                 ;# RANGE 0-4095 DEFAULT 1
set vlan_id_count                                  1                                  ;# RANGE 0-4095 DEFAULT 1
set vlan_id_count_inner                            1                                  ;# RANGE 0-4095 DEFAULT 1
set vlan_id_inner                                  702                                ;# RANGE 0-4095 DEFAULT 1
set vlan_id_repeat                                 1                                  ;# NUMERIC DEFAULT 1
set vlan_id_repeat_inner                           1                                  ;# NUMERIC DEFAULT 1
set vlan_id_step                                   1                                  ;# RANGE 0-4095 DEFAULT 1
set vlan_id_step_inner                             1                                  ;# RANGE 0-4095 DEFAULT 1
set vlan_user_priority                             1                                  ;# RANGE 0-7 DEFAULT 0
set vlan_user_priority_inner                       1                                  ;# RANGE 0-7 DEFAULT 0

################################################################################
# ANCP - ACCESS NODE PVC
################################################################################
set pvc_incr_mode                                  both                               ;# CHOICES vci vpi both DEFAULT both
set vci                                            32                                  ;# RANGE 32-65535 DEFAULT 32
set vci_count                                      4063                               ;# RANGE 1-65504 DEFAULT 4063
set vci_repeat                                     1                                  ;# RANGE 1-65535 DEFAULT 1
set vci_step                                       1                                  ;# RANGE 0-65503 DEFAULT 1
set vpi                                            0                                  ;# RANGE 0-255 DEFAULT 0
set vpi_count                                      1                                  ;# RANGE 1-256 DEFAULT 1
set vpi_repeat                                     1                                  ;# RANGE 1-65535 DEFAULT 1
set vpi_step                                       1                                  ;# RANGE 0-255 DEFAULT 1

################################################################################
# Start ANCP Call
################################################################################
set ANCP_config_status [::ixia::emulation_ancp_config                                                   \
        -device_count                                   $device_count                                   \
        -handle                                         $handle                                         \
        -mode                                           $mode                                           \
        -port_handle                                    $ancp_cfg_port_handle                           \
        -ancp_standard                                  $ancp_standard                                  \
        -events_per_interval                            $events_per_interval                            \
        -global_port_down_rate                          $global_port_down_rate                          \
        -global_port_up_rate                            $global_port_up_rate                            \
        -global_resync_rate                             $global_resync_rate                             \
        -gsmp_standard                                  $gsmp_standard                                  \
        -interval                                       $interval                                       \
        -line_config                                    $line_config                                    \
        -port_down_rate                                 $port_down_rate                                 \
        -port_resync_rate                               $port_resync_rate                               \
        -port_up_rate                                   $port_up_rate                                   \
        -port_override_globals                          $port_override_globals                          \
        -topology_discovery                             $topology_discovery                             \
        -access_aggregation                             $access_aggregation                             \
        -access_aggregation_dsl_inner_vlan              $access_aggregation_dsl_inner_vlan              \
        -access_aggregation_dsl_inner_vlan_type         $access_aggregation_dsl_inner_vlan_type         \
        -access_aggregation_dsl_outer_vlan              $access_aggregation_dsl_outer_vlan              \
        -access_aggregation_dsl_outer_vlan_type         $access_aggregation_dsl_outer_vlan_type         \
        -keep_alive                                     $keep_alive                                     \
        -keep_alive_retries                             $keep_alive_retries                             \
        -sut_ip_addr                                    $sut_ip_addr                                    \
        -sut_service_port                               $sut_service_port                               \
        -distribution_alg_percentage                    $distribution_alg_percentage                    \
        -gateway_incr_mode                              $gateway_incr_mode                              \
        -gateway_ip_addr                                $gateway_ip_addr                                \
        -gateway_ip_prefix_len                          $gateway_ip_prefix_len                          \
        -gateway_ip_step                                $gateway_ip_step                                \
        -intf_ip_addr                                   $intf_ip_addr                                   \
        -intf_ip_prefix_len                             $intf_ip_prefix_len                             \
        -intf_ip_step                                   $intf_ip_step                                   \
        -local_mss                                      $local_mss                                      \
        -encap_type                                     $encap_type                                     \
        -local_mac_addr                                 $local_mac_addr                                 \
        -local_mac_step                                 $local_mac_step                                 \
        -local_mac_addr_auto                            $local_mac_addr_auto                            \
        -local_mtu                                      $local_mtu                                      \
        -qinq_incr_mode                                 $qinq_incr_mode                                 \
	-vlan_id                                        $vlan_id                                        \
        -vlan_id_count                                  $vlan_id_count                                  \
        -vlan_id_count_inner                            $vlan_id_count_inner                            \
	-vlan_id_inner                                  $vlan_id_inner                                  \
        -vlan_id_repeat                                 $vlan_id_repeat                                 \
        -vlan_id_repeat_inner                           $vlan_id_repeat_inner                           \
        -vlan_id_step                                   $vlan_id_step                                   \
        -vlan_id_step_inner                             $vlan_id_step_inner                             \
        -vlan_user_priority                             $vlan_user_priority                             \
        -vlan_user_priority_inner                       $vlan_user_priority_inner                       \
        -pvc_incr_mode                                  $pvc_incr_mode                                  \
        -vci                                            $vci                                            \
        -vci_count                                      $vci_count                                      \
        -vci_repeat                                     $vci_repeat                                     \
        -vci_step                                       $vci_step                                       \
        -vpi                                            $vpi                                            \
        -vpi_count                                      $vpi_count                                      \
        -vpi_repeat                                     $vpi_repeat                                     \
        -vpi_step                                       $vpi_step                                       \
        ]
if {[keylget ANCP_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ANCP_config_status log]"
    return
}
set ANCP_handles [keylget ANCP_config_status handle]
puts "Ixia ANCP handles are: "
update idletasks
foreach ANCP_handle $ANCP_handles {
    puts $ANCP_handle
    update idletasks
}
puts "End ANCP configuration ..."
update idletasks

################################################################################
# END - ANCP configuration - First Port
################################################################################


set sbsc_out [::ixia::emulation_ancp_subscriber_lines_config        \
       -mode                               create                   \
       -ancp_client_handle                 $ANCP_handles            \
       -circuit_id                         DL                       \
       -circuit_id_suffix                  116300                   \
       -circuit_id_suffix_repeat           1                        \
       -circuit_id_suffix_step             1                        \
       -actual_rate_downstream             13                       \
       -actual_rate_upstream               14                       \
       -data_link                          ethernet                 \
       -downstream_act_interleaving_delay  22                       \
       -downstream_attainable_rate         23                       \
       -downstream_max_interleaving_delay  54                       \
       -downstream_max_rate                25                       \
       -downstream_min_low_power_rate      26                       \
       -downstream_min_rate                27                       \
       -dsl_type                           vdsl2                    \
       -encap1                             single_tagged_ethernet   \
       -encap2                             aal5_null_wo_fcs         \
       -include_encap                      1                        \
       -remote_id                          50                       \
       -upstream_act_interleaving_delay    76                       \
       -upstream_attainable_rate           88                       \
       -upstream_max_interleaving_delay    99                       \
       -upstream_max_rate                  76                       \
       -upstream_min_low_power_rate        66                       \
       -upstream_min_rate                  55                       \
       -percentage                         100                      \
    ]

if {[keylget sbsc_out status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget sbsc_out log]"
    return 0
}


##################################################
#           CLEAR DHCP STATISTICS                #
##################################################


set dhcp_stats_0 [::ixia::emulation_dhcp_stats      \
        -port_handle   $port_handle                      \
        -action        clear                        \
	-version       ixnetwork                    \
	]
if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name -[keylget dhcp_stats_0 log]"
    return 0
}

##################################################
# Start DHCP                                   #
##################################################
set control_status_0 [::ixia::emulation_dhcp_control \
        -port_handle $port_handle                         \
        -action            bind                      \
        ]
if {[keylget control_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status_0 log]"
    return 0
}

##################################################
#             GET DHCP STATISTICS                #
##################################################


#set clients_bound_configured     15                  ;#This value is equal with num_sessions
#set clients_bound_running 0
#set retries                    10
#while {($clients_bound_configured > $clients_bound_running) && $retries} {
    set dhcp_stats_0 [::ixia::emulation_dhcp_stats      \
            -port_handle $port_handle                           \
            -version     ixnetwork                         \
    	]
    if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
        puts "FAIL - $test_name -[keylget dhcp_stats_0 log]"
        return 0
#    }
    
#    set clients_bound_running 0
#        if {[string is integer [keylget dhcp_stats_0 aggregate.currently_bound]] } {
#            incr clients_bound_running [keylget dhcp_stats_0 aggregate.currently_bound]
#        }
#    after 5000
#    incr retries -1
#}
#if {$clients_bound_configured > $clients_bound_running} {
#    puts "FAIL - $test_name - Invalid number of DHCP addresses learned.\
#            Configured: $clients_bound_configured, Reported: $clients_bound_running."
#    return 0
#}

after 5000


##################################################
#           CLEAR ANCP STATISTICS                #
##################################################

#set ancp_stats_0 [::ixia::emulation_ancp_stats      \
#        -port_handle   $port_handle                      \
#	-reset                                      \
#        ]
#if {[keylget ancp_stats_0 status] != $::SUCCESS} {
#    puts "FAIL - $test_name -[keylget ancp_stats_0 log]"
#    return 0
#}

##################################################
#            PRINT ANCP STATISTICS               #
##################################################


proc show_stats var {
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
            if {$key == "status"} {continue}
            set indent [string repeat "    " $level] 
            puts -nonewline $indent 
            if {[catch {keylkeys var $key}]} {
                puts "$key: [keylget var $key]"
                continue
            } else {
                puts $key
                puts "$indent[string repeat "-" [string length $key]]"
            }
            show_stats [keylget var $key]
    }
}

#show_stats $ancp_stats_0



after 5000

puts "starting ANCP protocol"

##################################################
# Start ANCP                                   #
##################################################

set control_status_0 [::ixia::emulation_ancp_control \
        -ancp_handle $ANCP_handle                    \
        -action            enable                    \
	-action_control    start                     \
        ]
if {[keylget control_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status_0 log]"
    return 0
}

after 10000

##################################################
#           GET ANCP STATISTICS                #
##################################################

set ancp_stats_0 [::ixia::emulation_ancp_stats      \
        -port_handle   $port_handle                      \
        ]
if {[keylget ancp_stats_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name -[keylget ancp_stats_0 log]"
    return 0
}

after 5000



puts "These are the statistics after starting the protocol"

puts "####################################################"
show_stats $ancp_stats_0
puts "####################################################"



after 2000

##################################################
# Stop reset ANCP                                #
##################################################

set control_status_0 [::ixia::emulation_ancp_control \
        -ancp_handle $ANCP_handle                    \
        -action            enable                    \
	-action_control    stop                      \
        ]
if {[keylget control_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status_0 log]"
    return 0
}

##################################################
#           GET ANCP STATISTICS                #
##################################################

set ancp_stats_0 [::ixia::emulation_ancp_stats      \
        -port_handle   $port_handle                      \
        ]
if {[keylget ancp_stats_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name -[keylget ancp_stats_0 log]"
    return 0
}


puts "These are the statistics after stoping the protocol"

puts "####################################################"
show_stats $ancp_stats_0
puts "####################################################"


#set cleanup_status [::ixia::cleanup_session -port_handle $port_handle]
#if {[keylget cleanup_status status] != $::SUCCESS} {
#    return "FAIL - $test_name - [keylget cleanup_status log]"
#}

return "SUCCESS - $test_name - [clock format [clock seconds]]"

