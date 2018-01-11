#################################################################################
# Version 1.0    $Revision: 1 $
# $Author: T. Kong $
#
# $Workfile: OSPFv2_Lsa_reset.tcl $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample creates an OSPFv2 router and removes all User LSA under it.   #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM100TXS8 module.                              #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 127.0.0.1
set port_list [list 10/1 10/2]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect \
        -device    $chassisIP \
        -port_list $port_list \
        -username  ixiaApiUser]

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

set port_tx [lindex $port_handle 0]
set port_rx [lindex $port_handle 1]

########################################
# Configure interface in the test      #
#                                      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle \
        -autonegotiation 1            \
        -duplex          auto         \
        -speed           ether1000]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}


#################################################
#                                               #
#  Configure n OSPFv2 neighbors                 #
#                                               #
#################################################

set ospf_neighbor_status [::ixia::emulation_ospf_config \
        -port_handle                $port_tx         \
        -reset                                       \
        -session_type               ospfv2           \
        -mode                       create           \
        -count                      1                \
        -mac_address_init           1000.0000.0001   \
        -intf_ip_addr               100.1.1.1        \
        -intf_ip_addr_step          0.0.1.0          \
        -router_id                  1.1.1.1          \
        -router_id_step             0.0.1.0          \
        -neighbor_intf_ip_addr      100.1.1.2        \
        -neighbor_intf_ip_addr_step 0.0.1.0          \
        -neighbor_router_id         11.11.11.11      \
        -neighbor_router_id_step    0.0.1.0          \
        -loopback_ip_addr           1.1.1.1          \
        -loopback_ip_addr_step      1.1.1.1          \
        -vlan                       1                \
        -vlan_id                    1000             \
        -vlan_id_mode               fixed            \
        -vlan_id_step               5                \
        -area_id                    0.0.0.1          \
        -area_id_step               0.0.0.1          \
        -area_type                  external-capable \
        -authentication_mode        null             \
        -dead_interval              222              \
        -hello_interval             333              \
        -interface_cost             55               \
        -lsa_discard_mode           1                \
        -mtu                        670              \
        -network_type               broadcast        \
        -option_bits                "0x02"]

if {[keylget ospf_neighbor_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_neighbor_status log]"
}

# Extract the OSPF router handle
set ospf_handle_list [keylget ospf_neighbor_status handle]

#################################################
#                                               #
#  Mode is Reset                                #
#                                               #
#################################################

set ospf_handle [lindex $ospf_handle_list 0]
set ospf_lsa_status [::ixia::emulation_ospf_lsa_config    \
        -mode           reset   \
        -handle         $ospf_handle]

if {[keylget ospf_lsa_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_lsa_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
