#################################################################################
# Version 1.0    $Revision: 1 $
# $Author: MHasegan $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    11-13-2006 MHasegan
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
#    This sample configures ATM filters, triggers and counters.                #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on an ATM/POS 622 module.                           #
#                                                                              #
################################################################################
package require Ixia

set test_name [info script]

set chassisIP sylvester

########
# IpV4 #
########

set port_list "3/1"

#################################################################################
#                                START TEST                                     #
#################################################################################

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect  \
        -reset                     \
        -device    $chassisIP      \
        -port_list $port_list      \
        -username  ixiaApiUser     ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set test_port [keylget connect_status \
        port_handle.$chassisIP.[lindex $port_list 0]]

set port_handle [list $test_port]
########################################
# Configure interface in the test      #
# IPv4                                 #
########################################

set session_count 10

for {set id 0} {$id < $session_count} {incr id} {
    set interface_status.${id} [::ixia::interface_config \
            -port_handle      $test_port           \
            -mode             config               \
            -speed            oc3                  \
            -intf_mode        atm                  \
            -tx_c2            13                   \
            -rx_c2            13                   \
            -atm_encapsulation LLCRoutedCLIP       \
            -vpi                 1                 \
            -vci              [expr 32 + $id]      \
            -intf_ip_addr     [format "2.0.0.%d"   \
            [expr 100 + $id]]                      \
            -gateway          2.0.0.1              \
            -netmask          255.255.255.0        \
            ]        
    
    if {[keylget interface_status.${id} status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget interface_status.${id} log]"
    }
}

# ATM specific filters will not be enabled if the next call is not present

set traffic_start_status [::ixia::traffic_stats                 \
    -port_handle                            $test_port       \
    -mode                                   add_atm_stats    \
    -vpi                                    1                 \
    -vci                                    32                 \
    -vci_count                              10               \
    -vci_step                               1                \
    -atm_counter_vpi_type                   fixed             \
    -atm_counter_vci_type                   counter             \
    -atm_counter_vci_mode                   incr             \
    -atm_reassembly_enable_iptcpudp_checksum 0               \
    -atm_reassembly_enable_ip_qos           0                \
    -atm_reassembly_encapsulation           llc_routed_clip  ]

if {[keylget traffic_start_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_start_status log]"
}

set config_status [::ixia::packet_config_buffers \
    -port_handle  $test_port                     \
    -capture_mode trigger                        \
    ]
if {[keylget config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget config_status log]"
}

# The first call can have settings for regular filters and ATM specific
# filters
set filters_status [::ixia::packet_config_filter    \
    -mode               create                      \
    -port_handle        $test_port                  \
    -pattern1           {0C 01 01 64}               \
    -pattern_atm        {AB BA}                     \
    -pattern_mask_atm   {00 00}                     \
    -pattern_offset_atm 26                          \
    -vpi                1                           \
    -vci                32                          \
    -vci_count          5                           \
    -vci_step           1                           \
    ]
if {[keylget filters_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget filters_status log]"
}
# We store the handle of the first 5 pvc filters configured because they are
# needed for ::ixia::packet_config_tirggers
set atm_handle1 [keylget filters_status handle]

# When mode is addAtmFilter only ATM specific filters will be configured
# If regular filter values are provided they will be ignored

set filters_status [::ixia::packet_config_filter    \
    -mode               addAtmFilter                \
    -port_handle        $test_port                  \
    -pattern_atm        {AA BB CC DD}               \
    -pattern_mask_atm   {FF 00 FF FF}               \
    -pattern_offset_atm 10                          \
    -vpi                1                           \
    -vci                37                          \
    -vci_count          3                           \
    -vci_step           1                           \
    ]
if {[keylget filters_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget filters_status log]"
}

set atm_handle2 [keylget filters_status handle]

set filters_status [::ixia::packet_config_filter \
    -mode               addAtmFilter             \
    -port_handle        $test_port               \
    -pattern_atm        {11 22 33 44 55}         \
    -pattern_mask_atm   {FF 00 FF FF 00}         \
    -pattern_offset_atm 10                       \
    -vpi                1                        \
    -vci                40                       \
    -vci_count          2                        \
    -vci_step           1                        \
    ]
if {[keylget filters_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget filters_status log]"
}

set atm_handle3_1 [lindex [keylget filters_status handle] 0]
set atm_handle3_2 [lindex [keylget filters_status handle] 1]

# We assign the patterns set with ::ixia::packet_config_filters
# A handle must be provided. All the pvc patterns from the handle will be
# used in this procedure.
# Here we can configure filters, triggers and counters for both ATM specific
# and general. 

set trigger_status [::ixia::packet_config_triggers \
    -mode                   create                 \
    -port_handle            $test_port             \
    -handle                 $atm_handle1           \
    -uds1                   1                      \
    -capture_trigger        1                      \
    -capture_filter         1                      \
    -capture_filter_pattern pattern1               \
    -uds1_pattern           patternAtm             \
    -capture_trigger_pattern patternAtm            \
    ]

if {[keylget trigger_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget trigger_status log]"
}

# When mode is addAtmTriggers, only the ATM specific configurations will
# be set. Any other configurations will be ignored.
set trigger_status [::ixia::packet_config_triggers \
    -mode                   addAtmTrigger          \
    -port_handle            $test_port             \
    -handle                 $atm_handle2           \
    -uds2                   1                      \
    -capture_filter         1                      \
    -uds2_pattern           patternAtm             \
    -capture_filter_pattern patternAtm             \
    ]

if {[keylget trigger_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget trigger_status log]"
}

set trigger_status [::ixia::packet_config_triggers \
    -mode                   addAtmTrigger          \
    -port_handle            $test_port             \
    -handle                 $atm_handle3_1         \
    -capture_filter         1                      \
    -capture_filter_pattern patternAtm             \
    ]

if {[keylget trigger_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget trigger_status log]"
}

set trigger_status [::ixia::packet_config_triggers \
    -mode           addAtmTrigger      \
    -port_handle    $test_port         \
    -handle         $atm_handle3_2     \
    -uds1            1                 \
    -uds2            1                 \
    -capture_filter  1                 \
    -capture_trigger 1                 \
    -uds1_pattern    patternAtm        \
    -uds2_pattern    patternAtm        \
    -capture_filter_pattern patternAtm \
    -capture_trigger_pattern patternAtm\
    ]

if {[keylget trigger_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget trigger_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"


