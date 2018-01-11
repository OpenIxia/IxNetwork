#################################################################################
# Version 1    $Revision: 1 $
# $Author: RCsutak $
#
#    Copyright © 1997 - 2014 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    08-18-2014 RCsutak - created sample
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
#   This script connects to a star topology chassis chain using the ixiangpf   # 
#   namespace, displays the information retrieved and demonstrates a few key   #
#   retrievals.                                                                # 
#                                                                              #
# Module:                                                                      #
#   The sample was tested on a LSM XMVDC16NG module.                           #
#                                                                              #
################################################################################



if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}
set test_name                   [info script]
set chassis_ip                  [list master_chassis slave_1  slave_2  slave_3 slave_4]
set ixnetwork_tcl_server        localhost
set port_list                   [list [list 4/1] [list] [list] [list 4/1] [list]]
set master_chassis				[list none master_chassis master_chassis master_chassis master_chassis]
set chain_type                  star
set errors                      0
set chain_cables_length         [list 0 3 6 3 6]

     

if {$chain_type == "star"} {

    set connect_status [::ixiangpf::connect		      			 \
            -reset                                           \
            -device                 $chassis_ip              \
            -port_list              $port_list               \
            -ixnetwork_tcl_server   $ixnetwork_tcl_server    \
            -master_device          $master_chassis          \
            -chain_type             $chain_type             \
            -chain_cables_length    $chain_cables_length    \
            ]
               
    if {[keylget connect_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget connect_status log]"
        return 0
    }

    puts "Connected with star topology..."
} else {
    set connect_status [::ixiangpf::connect		      			 \
            -reset                                           \
            -device                 $chassis_ip              \
            -port_list              $port_list               \
            -ixnetwork_tcl_server   $ixnetwork_tcl_server    \
            -tcl_server             $tcl_server              \
            -master_device          $master_chassis           \
    ]
               
    if {[keylget connect_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget connect_status log]"
        return 0
    }

    puts "Connected with daisy topology..."
}

puts "\nPrinting full connection information tree ...\n"
::ixia::keylprint connect_status

set port_1 [keylget connect_status port_handle.[lindex $chassis_ip 0].[lindex $port_list 0]]
set port_2 [keylget connect_status port_handle.[lindex $chassis_ip 3].[lindex $port_list 3]]
set port_handle [list $port_1 $port_2] 
set check_master [keylget connect_status connection.chassis.[lindex $chassis_ip 0].is_master_chassis]
set check_chain_type [keylget connect_status connection.chassis.[lindex $chassis_ip 0].chain_type]

puts "Script ran SUCCESSFULLY!"
return 1
