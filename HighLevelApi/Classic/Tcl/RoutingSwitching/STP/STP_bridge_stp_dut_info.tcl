################################################################################
# Version 1.0    $Revision: 1 $
# $Author: RAntonescu $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    12-05-2007 RAntonescu - created sample
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
#     This sample create following topology:                                   #
#     Ixia port(first)        Ixia port(second)                                #
#                                                                              #
#        ---        ---        ---                                             #
#       |sw1|------|DUT|------|sw2|                                            #
#        ---        ---        ---                                             #
#                                                                              #
#       sw1 It is an emulated STP bridge which sends BPDUs (it emulate         #
#           behing it root bridge). It have two interfaces: first should       #
#           be in forwarding and second in backup mode.                        #
#       sw2 It is an emulated STP bridge which receive BPDUs from DUT.         #
#                                                                              #
#  DUT configuration:                                                          #
#       vlan 910                                                               #
#       exit                                                                   #
#       spanning-tree mode pvst                                                #
#       spanning-tree vlan 910 hello-time 1                                    #
#       spanning-tree vlan 910 forward-time 4                                  #
#       spanning-tree vlan 910 max-age 6                                       #
#       interface GigabitEthernet7/34                                          #
#         no ip address                                                        #
#         switchport                                                           #
#         switchport access vlan 910                                           #
#       interface GigabitEthernet7/36                                          #
#         no ip address                                                        #
#         switchport                                                           #
#         switchport access vlan 910                                           #
#                                                                              #
#   DUT debuging command:                                                      #
#       show spanning-tree vlan 910                                            #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET27.                                      #
#                                                                              #
################################################################################
package require Ixia

set test_name [info script]
set ixnetwork_tcl_server 127.0.0.1
set chassisIP sylvester
set port_list [list 3/1 3/2]

################################################################################
# Connect to the chassis,reset to factory defaults and take ownership
################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect 				\
        -reset                      				\
        -ixnetwork_tcl_server $ixnetwork_tcl_server \
        -device    $chassisIP       				\
        -port_list $port_list       				\
        -username  ixiaApiUser      				\
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
}

set port_array [keylget connect_status port_handle.$chassisIP]

set port_0 [keylget port_array [lindex $port_list 0]]
set port_1 [keylget port_array [lindex $port_list 1]]

################################################################################
# Configure L1 interface
################################################################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_0 $port_1       \
        -autonegotiation 1                     \
        -duplex          auto                  \
        -speed           auto                  \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

################################################################################
# Create emulated STP bridges
################################################################################
set stp_status [::ixia::emulation_stp_bridge_config \
        -port_handle        $port_0                 \
        -bridge_mode        rstp                    \
        -count              1                       \
        -intf_count         2                       \
        -mac_address_init   101f.efe2.12b4          \
        -hello_interval     1000                    \
        -forward_delay      4000                    \
        -max_age            6000                    \
        -bridge_mac         0000.1111.ffff          \
        -root_mac           0000.1111.eeee          \
        -link_type          shared                  \
        -root_priority      8192                    \
        ]
if {[keylget stp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_status log]"
    return
}

set bridge_handle [keylget stp_status bridge_handles]
set bridge_interface_handles\
        [keylget stp_status bridge_interface_handles.$bridge_handle]

################################################################################
# Create an emulated LAN for STP use
################################################################################
set stp_status [::ixia::emulation_stp_lan_config \
        -port_handle        $port_0              \
        -count              10                   \
        -mac_address        000e.4cd7.c011       \
        -mac_incr_enable    1                    \
        ]
if {[keylget stp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_status log]"
    return
}
        
################################################################################
# Create emulated STP bridges
################################################################################
set stp_status [::ixia::emulation_stp_bridge_config \
        -port_handle        $port_1                 \
        -bridge_mode        rstp                    \
        -count              1                       \
        -intf_count         1                       \
        -mac_address_init   101f.efff.12b4          \
        -hello_interval     1000                    \
        -forward_delay      4000                    \
        -max_age            6000                    \
        -bridge_mac         0000.1aa1.ffff          \
        -link_type          shared                  \
        ]
if {[keylget stp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_status log]"
    return
}

set bridge_handle2 [keylget stp_status bridge_handles]
set bridge_interface_handles2 [keylget stp_status\
        bridge_interface_handles.$bridge_handle2]

################################################################################
# Create an emulated LAN for STP use
################################################################################
set stp_status [::ixia::emulation_stp_lan_config \
        -port_handle        $port_1              \
        -count              10                   \
        -mac_address        000e.4fd7.c011       \
        -mac_incr_enable    1                    \
        ]
if {[keylget stp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_status log]"
    return
}

################################################################################
# Start STP protocol on speficied port
################################################################################
set stp_status [::ixia::emulation_stp_control \
        -port_handle    $port_0               \
        -mode           start                 \
        ]
if {[keylget stp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_status log]"
    return
}

################################################################################
# Start STP protocol on speficied port
################################################################################
set stp_status [::ixia::emulation_stp_control \
        -port_handle    $port_1               \
        -mode           start                 \
        ]
if {[keylget stp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_status log]"
    return
}

# wait for stp interface to change their states
after 10000

################################################################################
# Retrieve learned information
################################################################################
set stp_info [::ixia::emulation_stp_info \
        -port_handle    $port_1          \
        -mode           learned_info     \
        ]
if {[keylget stp_info status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_info log]"
    return
}

puts "\nLearned info on port $port_1:"

set i 1
foreach stp_intf $bridge_interface_handles2 {
    puts "Interface $i stats:"
    set stat_list [keylget stp_info $port_1.$bridge_handle2.stp_intf.$stp_intf]
    foreach stat_name [keylkeys stat_list] {
        puts "$stat_name: [keylget stat_list $stat_name]"
    }
    incr i
    puts ""
}

################################################################################
# Retrieve aggregate statistics on port which send BPDUs
################################################################################
set stp_info [::ixia::emulation_stp_info \
        -port_handle    $port_0          \
        -mode           aggregate_stats  \
        ]
if {[keylget stp_info status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stp_info log]"
    return
}
puts "Aggregate stats on port $port_0:"
puts "BPDUs Rx: [keylget stp_info $port_0.aggregate.rstp_bpdus_rx]"
puts "BPDUs Tx: [keylget stp_info $port_0.aggregate.rstp_bpdus_tx]"

return "SUCCESS - $test_name - [clock format [clock seconds]]"
