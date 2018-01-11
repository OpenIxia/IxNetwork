################################################################################
# Version 1    $Revision: 0 $
# $Author: RAntonescu $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    02-08-2008 RAntonescu - created sample
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
#    This sample creates a stream for each combination of ipv6 source type,    #
#    ipv6 destination type, ipv6 increment mode, and some custom masks.        #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET26.                                      #
#                                                                              #
################################################################################
package req Ixia

set test_name [info script]

set port_list {3/1}
set chassis_name sylvester

proc getStepFromMask {mask} {
    set mask_value [mpexpr round(pow(2,128-$mask))]
    set bytes [::ixia::val2Bytes $mask_value 16]
    set ipv6_addr ""
    set i 0
    foreach byte $bytes {
        if {[expr $i % 2] == 0 && $i > 0} {
           append ipv6_addr ":"
        }
        append ipv6_addr $byte
        incr i
    }
    return $ipv6_addr
}

# Create an array which have an ipv6 address of each type
array set ipv6_addresses {
    userdef         4000::
    reserverd       0::1
    nsap            200::
    ipx             400::
    global          3000::
    local           FE80::
    site            FEC0::
    mcast           FF0E::
}

# Create an array which returned ipv6 types supported by a specific mode
array set incr_modes [list \
        fixed                       {userdef reserverd nsap ipx global local site mcast} \
        incr_host                   {userdef reserverd nsap ipx} \
        decr_host                   {userdef reserverd nsap ipx} \
        incr_network                {userdef reserverd nsap ipx} \
        decr_network                {userdef reserverd nsap ipx} \
        incr_intf_id                {global local site} \
        decr_intf_id                {global local site} \
        incr_global_top_level       {global} \
        decr_global_top_level       {global} \
        incr_global_next_level      {global} \
        decr_global_next_level      {global} \
        incr_global_site_level      {global} \
        decr_global_site_level      {global} \
        incr_local_site_subnet      {site} \
        decr_local_site_subnet      {site} \
        incr_mcast_group            {mcast} \
        decr_mcast_group            {mcast} \
]

# Create an array which provide a valid mask for a specific increment mode
array set supported_masks {
    fixed                       96
    incr_host                   97
    decr_host                   98
    incr_network                99
    decr_network                100
    incr_intf_id                101
    decr_intf_id                102
    incr_global_top_level       4
    decr_global_top_level       4
    incr_global_next_level      24
    decr_global_next_level      24
    incr_global_site_level      48
    decr_global_site_level      48
    incr_local_site_subnet      48
    decr_local_site_subnet      48
    incr_mcast_group            96
    decr_mcast_group            96
}

################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
################################################################################
set connect_status [ixia::connect   \
        -device     $chassis_name   \
        -port_list  $port_list      \
        -reset                      \
        -username   ixiaApiUser     \
        ]
if {[keylget connect_status status] == $::FAILURE} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
}

set port_handle [keylget connect_status port_handle.$chassis_name.$port_list]

################################################################################
# Configure interface in the test
################################################################################
set interface_status [ixia::interface_config    \
        -port_handle $port_handle               \
        -ipv6_intf_addr 2500::1                 \
        -intf_ip_addr 123.1.1.2                 \
        ]
if {[keylget interface_status status] == $::FAILURE} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}
        
set i 1
foreach incr_mode [array names incr_modes] {
    foreach ip_addr_type $incr_modes($incr_mode) {
        set ip_addr $ipv6_addresses($ip_addr_type)
        set mask $supported_masks($incr_mode)
        set step [getStepFromMask $mask]
        puts "--------------------------------------------\nstream $i"
        incr i
        puts "ip_addr=$ip_addr"
        puts "mask=$mask"
        puts "step=$step"
        puts "incr_mode=$incr_mode"
        puts "use ip_addr as source"
        ########################################################################
        # Configure streams which have different ipv6_src_xxx parameters
        ########################################################################
        set traffic_status  [ixia::traffic_config                           \
                 -mode                      create                          \
                 -port_handle               $port_handle                    \
                 -l3_protocol               ipv6                            \
                 -ipv6_src_addr             $ip_addr                        \
                 -ipv6_src_mode             $incr_mode                      \
                 -ipv6_src_mask             $mask                           \
                 -ipv6_src_count            10                              \
                 -ipv6_src_step             $step                           \
                 -ipv6_dst_step             1000::                          \
                 -ipv6_dst_addr             2006::1                         \
                 -ipv6_dst_mode             increment                       \
                 -ipv6_dst_count            3                               \
                 -l3_length                 512                             \
                 -rate_bps                  100                             \
                 -mac_dst_mode              discovery                       \
                 -vlan_id_mode              increment                       \
                 -vlan_id                   100                             \
                 -vlan_id_count             3                               \
                 -vlan_id_step              2                               \
                 -signature_offset          100                             \
                 -enable_pgid               0                               \
        ]
        if {[keylget traffic_status status] == $::FAILURE} {
            puts "FAIL - $test_name - [keylget traffic_status log]"
            return
        } 

        puts "stream $i"
        incr i
        puts "use ip_addr as destination"
        ########################################################################
        # Configure streams which have different ipv6_dst_xxx parameters
        ########################################################################
        set traffic_status  [ixia::traffic_config                           \
                 -mode                      create                          \
                 -port_handle               $port_handle                    \
                 -l3_protocol               ipv6                            \
                 -ipv6_dst_addr             $ip_addr                        \
                 -ipv6_dst_mode             $incr_mode                      \
                 -ipv6_dst_mask             $mask                           \
                 -ipv6_dst_step             $step                           \
                 -ipv6_dst_count            3                               \
                 -ipv6_src_addr             FF05::                          \
                 -ipv6_src_mode             decrement                       \
                 -ipv6_src_count            7                               \
                 -l3_length                 512                             \
                 -rate_bps                  100                             \
                 -mac_dst_mode              discovery                       \
                 -vlan_id_mode              increment                       \
                 -vlan_id                   100                             \
                 -vlan_id_count             3                               \
                 -vlan_id_step              2                               \
                 -signature_offset          100                             \
                 -enable_pgid               0                               \
        ]
        if {[keylget traffic_status status] == $::FAILURE} {
            puts "FAIL - $test_name - [keylget traffic_status log]"
            return
        } 
        
        puts "stream $i"
        incr i
        puts "use ip_addr as inner source"
        ########################################################################
        # Configure streams which have different inner_ipv6_src_xxx parameters
        ########################################################################
        set traffic_status  [ixia::traffic_config                           \
                 -mode                      create                          \
                 -port_handle               $port_handle                    \
                 -l3_protocol               ipv4                            \
                 -ip_src_addr               2.2.3.4                         \
                 -ip_src_mode               increment                       \
                 -ip_src_count              9                               \
                 -ip_dst_addr               2.2.3.5                         \
                 -ip_dst_mode               increment                       \
                 -ip_dst_count              3                               \
                 -l3_length                 78                              \
                 -rate_bps                  100                             \
                 -mac_dst_mode              discovery                       \
                 -vlan_id_mode              increment                       \
                 -vlan_id                   100                             \
                 -vlan_id_count             3                               \
                 -vlan_id_step              2                               \
                 -signature_offset          64                              \
                 -l4_protocol               gre                             \
                 -inner_protocol            ipv6                            \
                 -inner_ipv6_dst_addr       FEC0::                          \
                 -inner_ipv6_dst_mode       increment                       \
                 -inner_ipv6_dst_step       0:0:1::0                        \
                 -inner_ipv6_src_addr       $ip_addr                        \
                 -inner_ipv6_src_mode       $incr_mode                      \
                 -inner_ipv6_src_count      10                              \
                 -inner_ipv6_src_mask       $mask                           \
                 -enable_pgid               0                               \
        ]
        if {[keylget traffic_status status] == $::FAILURE} {
            puts "FAIL - $test_name - [keylget traffic_status log]"
            return
        } 

        puts "stream $i"
        incr i
        puts "use ip_addr as inner destination"
        ########################################################################
        # Configure streams which have different inner_ipv6_dst_xxx parameters
        ########################################################################
        set traffic_status  [ixia::traffic_config                           \
                 -mode                      create                          \
                 -port_handle               $port_handle                    \
                 -l3_protocol               ipv4                            \
                 -ip_src_addr               12.2.3.4                        \
                 -ip_src_mode               increment                       \
                 -ip_src_count              3                               \
                 -ip_dst_addr               22.2.3.5                        \
                 -ip_dst_mode               increment                       \
                 -ip_dst_count              2                               \
                 -l3_length                 78                              \
                 -rate_bps                  100                             \
                 -mac_dst_mode              discovery                       \
                 -vlan_id_mode              increment                       \
                 -vlan_id                   100                             \
                 -vlan_id_count             3                               \
                 -vlan_id_step              2                               \
                 -signature_offset          64                              \
                 -l4_protocol               gre                             \
                 -inner_protocol            ipv6                            \
                 -inner_ipv6_src_addr       4000::                          \
                 -inner_ipv6_src_mode       increment                       \
                 -inner_ipv6_src_step       0::1:0:0:0                      \
                 -inner_ipv6_dst_addr       $ip_addr                        \
                 -inner_ipv6_dst_mode       $incr_mode                      \
                 -inner_ipv6_dst_mask       $mask                           \
                 -inner_ipv6_dst_step       $step                           \
                 -inner_ipv6_dst_count      10                              \
                 -enable_pgid               0                               \
        ]
        if {[keylget traffic_status status] == $::FAILURE} {
            puts "FAIL - $test_name - [keylget traffic_status log]"
            return
        } 
    }
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
