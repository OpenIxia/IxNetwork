#################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-23-2013 Mchakravarthy - created sample
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
#    This sample loads ixnetwork config file with ELMI protocol configured on  #
#    ports and retreives all the handles using session resume                  #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
# General script variables
################################################################################
set test_name               [info script]
set test_name_folder        [file dirname $test_name]
set ixn_cfg                 [file join $test_name_folder ELMI_b2b.ixncfg]

################################################################################
# START - Connect to the chassis
################################################################################
puts "Starting - $test_name - [clock format [clock seconds]]"
puts "Start connecting to chassis ..."

set tcl_server              127.0.0.1
set ixnetwork_tcl_server    127.0.0.1
set chassis_ip              10.206.27.55
set port_list               [list 8/1 8/2]

set connect_status [ixia::connect                               \
        -mode                           connect                 \
        -config_file                    $ixn_cfg                \
        -ixnetwork_tcl_server           $ixnetwork_tcl_server   \
        -tcl_server                     $tcl_server             ]

        
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_handle [list]

foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set i 0
puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port
    incr i
}

puts "Connect to the chassis complete."
################################################################################
# END - Connect to the chassis
################################################################################

################################################################################
# Retreive elmi config handles using session info
################################################################################

set rval_1 [ixia::session_info                                      \
        -mode                           get_session_keys            \
        -session_keys_include_filter    {emulation_elmi_config}     \
        -port_handle                    $port_0                     ]
        
if {[keylget rval_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget rval_1 log]"
    return 0
}

set uni_handles_0 [keylget rval_1 $port_0.emulation_elmi_config.uni_handles]
puts "Port: $port_0 - UNI Handle                - $uni_handles_0"
        
set rval_2 [ixia::session_info                                      \
        -mode                           get_session_keys            \
        -session_keys_include_filter    {emulation_elmi_config}     \
        -port_handle                    $port_1                     ]
        
if {[keylget rval_2 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget rval_2 log]"
    return 0
}

set uni_handles_1               [keylget rval_2 $port_1.emulation_elmi_config.uni_handles]
set evc_handles_1               [lsort [keylget rval_2 $port_1.emulation_elmi_config.evc_handles]]
set uni_status_handles_1        [keylget rval_2 $port_1.emulation_elmi_config.uni_status_handles]
set bw_profile_handles_1        [lsort [keylget rval_2 $port_1.emulation_elmi_config.bw_profile_handles]]
set ce_vlan_id_range_handles_1  [lsort [keylget rval_2 $port_1.emulation_elmi_config.ce_vlan_id_range_handles]]

puts "Port: $port_1 - UNI Handle                - $uni_handles_1"
puts "Port: $port_1 - EVC Handles               - $evc_handles_1"
puts "Port: $port_1 - UNI Status Handles        - $uni_status_handles_1"
puts "Port: $port_1 - BW Profile Handles        - $bw_profile_handles_1"
puts "Port: $port_1 - CE Vlan Id Range Handles  - $ce_vlan_id_range_handles_1"
############################### SUCCESS or FAILURE #############################

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1





