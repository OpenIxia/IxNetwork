################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    03-28-2008 MHasegan - created sample
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
#    This sample creates 1 BFD router, with 2 router interfaces having VLAN    #
#    enabled.                                                                  #
#    Each router interface is associated with a directly connected protocol    #
#    interface.                                                                #
#    The BFD router is modified by disabling VLAN (-vlan 0), and vlan will be  #
#    disabled on the connected protocol interfaces.                            #
#    The second call with -mode modify will have a BFD interface as handle and #
#    -vlan 1 (enable VLAN tags). This will enable VLAN on the second protocol  #
#    interface.                                                                #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 2/1]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                         \
        -reset                                              \
        -ixnetwork_tcl_server       localhost               \
        -device                     $chassisIP              \
        -port_list                  $port_list              \
        -username                   ixiaApiUser             \
        ]
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
################################################################################
# Configure interface in the test
################################################################################
set interface_status [::ixia::interface_config              \
        -port_handle                $port_handle            \
        -autonegotiation            1                       \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set port_0 [lindex $port_handle 0]

################################################################################
# Configure BFD router with -vlan 1
################################################################################
set bfd_router_status [::ixia::emulation_bfd_config         \
        -mode                       create                  \
        -reset                                              \
        -port_handle                $port_0                 \
        -count                      1                       \
        -intf_count                 2                       \
        -intf_ip_addr               25.1.1.2                \
        -intf_ip_addr_step          1.0.0.0                 \
        -intf_ip_prefix_length      24                      \
        -intf_gw_ip_addr            25.1.1.1                \
        -intf_gw_ip_addr_step       1.0.0.0                 \
        -vlan                       1                       \
        -vlan_id                    25                      \
        -vlan_id_step               5                       \
        -mac_address_init           0000.0000.0001          \
        -router_id                  25.1.1.2                \
        -router_id_step             1.0.0.0                 \
        -echo_rx_interval           100                     \
        -echo_tx_interval           200                     \
        -enable_demand_mode         1                       \
        ]
if {[keylget bfd_router_status status] != $::SUCCESS} {
    return "FAIL - [keylget bfd_router_status log]"
}
set bfd_router1 [lindex [keylget bfd_router_status router_handles] 0]
set bfd_router_intf2 [lindex [keylget bfd_router_status router_interface_handles.$bfd_router1] 1]

################################################################################
# Modify BFD router with vlan 0 to disable VLAN from both interfaces
################################################################################
set bfd_router_modify_status [::ixia::emulation_bfd_config  \
        -mode                       modify                  \
        -handle                     $bfd_router1            \
        -vlan                       0                       \
        -echo_rx_interval           300                     \
        ]
if {[keylget bfd_router_modify_status status] != $::SUCCESS} {
    return "FAIL - [keylget bfd_router_modify_status log]"
}

################################################################################
# Modify BFD router interface with vlan 1 to enable VLAN on the second interface
# of the router
################################################################################
set bfd_router_modify_status [::ixia::emulation_bfd_config  \
        -mode                       modify                  \
        -handle                     $bfd_router_intf2       \
        -vlan                       1                       \
        -echo_rx_interval           300                     \
        ]
if {[keylget bfd_router_modify_status status] != $::SUCCESS} {
    return "FAIL - [keylget bfd_router_modify_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
