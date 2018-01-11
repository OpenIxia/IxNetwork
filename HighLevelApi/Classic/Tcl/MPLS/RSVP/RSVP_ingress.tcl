################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Hasmik $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-19-2004 Hasmik
#    04-1-2005  T.Kong - updated for HLTAPI V4.0 spec
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
#    This sample creates a RSVP neigbor and configures it as Ingress LSR.      #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM100TXS8 module.                              #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 127.0.0.1
set port_list [list 10/1]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username   ixiaApiUser     ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [keylget connect_status port_handle.$chassisIP.$port_list]

##############################################################################
# Configure interface in the test      
# IPv4                                 
##############################################################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle          \
        -autonegotiation 1                     \
        -duplex          full                  \
        -speed           ether100              ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

##############################################################################
#  Configure a RSVP neighbor 
##############################################################################
set rsvp_config_status [::ixia::emulation_rsvp_config   \
        -mode                 create                    \
        -reset                                          \
        -port_handle          $port_handle              \
        -count                2                         \
        -refresh_reduction    1                         \
        -reliable_delivery    1                         \
        -bundle_msgs          0                         \
        -hello_msgs           1                         \
        -hello_interval       200                       \
        -hello_retry_count    4                         \
        -refresh_interval     20                        \
        -srefresh_interval    1000                      \
        -egress_label_mode           imnull             \
        -path_state_refresh_timeout  77                 \
        -path_state_timeout_count    5                  \
        -record_route                1                  \
        -resv_confirm                1                  \
        -resv_state_timeout_count    5                  \
        -resv_state_refresh_timeout  5                  \
        -min_label_value      20                        \
        -max_label_value      30                        \
        -vlan                 1                         \
        -vlan_id              300                       \
        -vlan_id_mode         fixed                     \
        -vlan_id_step         2                         \
        -mac_address_init     0000.0000.0001            \
        -intf_prefix_length   24                        \
        -ip_version           4                         \
        -intf_ip_addr         3.3.3.100                 \
        -intf_ip_addr_step    0.0.1.0                   \
        -neighbor_intf_ip_addr       3.3.3.1            \
        -neighbor_intf_ip_addr_step  0.0.1.0            \
        -writeFlag            nowrite                   ]
if {[keylget rsvp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_config_status log]"
}

set handle [lindex [keylget rsvp_config_status handles] 0]

################################################################################
#  Configure a RSVP Destination Range along with Sender Range
#  handle        - retured from the previous call
#  rsvp_behavior - rsvpIngress
################################################################################

set handleList     [list]
set egress_ip_addr 2.2.2.100
set sender_ip_addr 4.4.4.100
set rro_ipv4_list   {101.0.0.1 202.0.0.1}
set rro_label_list  {11 22}
set rro_ctype_list  {33 44}
set rro_flags_list  {9  12}
set ero_ipv4_list   {33.0.0.1 44.0.0.1}
set ero_as_num_list {33 44}
set ero_flags_list  {9  11}
set ero_pfxlen_list {1 1}
set ero_loose_list  {1  0}

# Add numDests Destination Ranges
set rsvp_tunnel_config_status [::ixia::emulation_rsvp_tunnel_config   \
        -mode                               create          \
        -handle                             $handle         \
        -rsvp_behavior                      rsvpIngress     \
        -count                              3               \
        -egress_ip_addr                     $egress_ip_addr \
        -egress_ip_step                     0.1.0.0         \
        -ingress_ip_addr                    $sender_ip_addr \
        -ingress_ip_step                    0.1.0.0         \
        -ingress_bandwidth                  1000            \
        -sender_tspec_token_bkt_rate        10              \
        -sender_tspec_token_bkt_size        10              \
        -sender_tspec_peak_data_rate        10              \
        -sender_tspec_min_policed_size      5               \
        -sender_tspec_max_pkt_size          580             \
        -session_attr_bw_protect            1               \
        -session_attr_se_style              1               \
        -session_attr_local_protect         1               \
        -session_attr_label_record          0               \
        -session_attr_setup_priority        2               \
        -session_attr_hold_priority         2               \
        -session_attr_resource_affinities   1               \
        -session_attr_ra_include_all        0x11223344      \
        -lsp_id_start                       100             \
        -tunnel_id_start                    5               \
        -tunnel_id_count                    2               \
        -tunnel_id_step                     10              \
        -ero_mode                           loose           \
        -ero_dut_pfxlen                     16              \
        -rro                                1               \
        -rro_list_type                      label           \
        -rro_list_ipv4                      $rro_ipv4_list  \
        -rro_list_label                     $rro_label_list \
        -rro_list_flags                     $rro_flags_list \
        -rro_list_ctype                     $rro_ctype_list \
        -ero                                1               \
        -ero_list_type                      ipv4            \
        -ero_list_loose                     $ero_loose_list \
        -ero_list_ipv4                      $ero_ipv4_list  \
        -ero_list_pfxlen                    $ero_pfxlen_list\
        -ero_list_as_num                    $ero_as_num_list\
        -fast_reroute                       1               \
        -fast_reroute_bandwidth             1000            \
        -fast_reroute_exclude_any           aabbccdd        \
        -fast_reroute_holding_priority      1               \
        -fast_reroute_hop_limit             5               \
        -fast_reroute_setup_priority        7               \
        -one_to_one_backup                  1               \
        -send_detour                        1               \
        -plr_id                             11.0.0.1        \
        -avoid_node_id                      22.0.0.1        \
        -session_attr_name                  MyAttr          \
        -writeFlag                          write           ]

if {[keylget rsvp_tunnel_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tunnel_config_status log]"
}

lappend handleList [keylget rsvp_tunnel_config_status tunnel_handle]

return "SUCCESS - $test_name - [clock format [clock seconds]]"
