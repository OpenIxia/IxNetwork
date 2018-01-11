################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mircea Hasegan $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    02-23-2009 Mircea Hasegan
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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample creates a Tree topology on an Ixia Port.                      #
#    Topology graphic representation is too big to include in sample. Please   #
#    see topology_tree_example.jpg in the Samples directory under OAM          #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################

set env(IXIA_VERSION) HLTSET47
package require Ixia

set test_name [info script]

set chassisIP 10.205.19.231
set port_list [list 2/3]


# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                 \
        -reset                                      \
        -ixnetwork_tcl_server       localhost       \
        -device                     $chassisIP      \
        -port_list                  $port_list      \
        -username                   ixiaApiUser     ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set port_0 [lindex $port_handle 0]

puts "Ixia port handles are $port_handle "

set interface_status [::ixia::interface_config \
        -port_handle      $port_0     \
        -mode             config               \
        -speed            auto                 \
        -duplex           auto                 \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}


set oam_topology_status [::ixia::emulation_oam_config_topology                  \
         -mode                        reset                                     \
         -port_handle                 $port_0                                   \
    ]
if {[keylget oam_topology_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget oam_topology_status log]"
}

# Create 2 bridges with multiple levels Tree topology
# 2 bridges; 0 mips; 2 meps; md_level 4; domain_level 7; vlans

set bridge_id    ff:ff:ff:aa:bb:00
set bridge_count 2
set mac_local    00:00:00:10:00:0A
set md_level     4
set domain_level level7
set mep_id       1
set mep_count    2
set vlan_id      10
set vlan_id_step 10

set oam_topology_status [::ixia::emulation_oam_config_topology                  \
         -mode                        create                                    \
         -port_handle                 $port_0                                   \
         -count                       $bridge_count                             \
         -bridge_id                   $bridge_id                                \
         -encap                       ethernet_ii                               \
         -mac_local                   $mac_local                                \
         -mac_local_incr_mode         increment                                 \
         -continuity_check                                                      \
         -fault_alarm_signal                                                    \
         -domain_level                $domain_level                             \
         -md_level                    $md_level                                 \
         -short_ma_name_format        char_str                                  \
         -short_ma_name_wildcard      1                                         \
         -short_ma_name_value         hltapi?                                   \
         -short_ma_name_step          1                                         \
         -short_ma_name_wc_start      0                                         \
         -short_ma_name_length        9                                         \
         -mip_count                   0                                         \
         -mep_count                   $mep_count                                \
         -mep_id                      $mep_id                                   \
         -mep_id_incr_mode            increment                                 \
         -vlan_id                     10                                        \
         -vlan_id_step                10                                        \
    ]
if {[keylget oam_topology_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget oam_topology_status log]"
}


return "SUCCESS - $test_name - [clock format [clock seconds]]"