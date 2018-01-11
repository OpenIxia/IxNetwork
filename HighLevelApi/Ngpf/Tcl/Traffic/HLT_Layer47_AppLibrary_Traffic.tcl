################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    01/20/2014 - Andrei Parvu - created sample                                #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#   The script below walks through the workflow of an AppLibrary end to end    #	
#	test, using the below steps:											   #	
#		1. Connection to the chassis, IxNetwork Tcl Server 					   #
#		2. Topology configuration											   #
#		3. Configure trafficItem 1 for Layer 4-7 AppLibrary Profile			   #	
#		4. Configure trafficItem 2 for Layer 4-7 AppLibrary Profile			   #
#		5. Start protocols													   #	
#		6. Apply and run AppLibrary traffic									   #
#		7. Drill down per IP addresses during traffic run					   #
#		8. Stop Traffic.													   #	
#																			   #	
#                                                                              #
################################################################################

################################################################################
# Utils																		   #	
################################################################################

# Importing packages to be used in the script
package require Ixia

################################################################################
# Connection to the chassis, IxNetwork Tcl Server                 			   #
################################################################################

# Setting chassis connection parameters
set chassis_ip					{10.205.23.34}
set tcl_server					{10.205.23.34}
set ixnetwork_tcl_server		{localhost:8449}
set port_list					[list 2/5 2/6 2/7 2/8]
set vport_name_list				{{{{Ethernet - 001}} {{Ethernet - 002}} {{Ethernet - 003}} {{Ethernet - 004}}}}

# Connecting to the chassis
set connect_status [::ixiangpf::connect							\
    -reset 							1							\
    -device							$chassis_ip					\
    -port_list						$port_list					\
    -ixnetwork_tcl_server			$ixnetwork_tcl_server		\
    -tcl_server						$tcl_server					\
]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

# Creating port handles to be used further on in the script
set port_1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]
set port_3 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 2]]
set port_4 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 3]]
set port_handle [list $port_1 $port_2 $port_3 $port_4] 

################################################################################
# Configure Topology 1, Device Group 1                                         # 
################################################################################

# Creating the first topology
set topology_1_status [::ixiangpf::topology_config					\
        -topology_name      {Topology 1}                            \
        -port_handle        $port_1								    \
    ]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_1_status log]"
    return 0
}
set topology_1_handle [keylget topology_1_status topology_handle]
  
# Creating a device group for the first topology  
set device_group_1_status [::ixiangpf::topology_config		\
        -topology_handle			$topology_1_handle      \
        -device_group_name			{Device Group 1}        \
        -device_group_multiplier	45	                    \
        -device_group_enabled		1                       \
    ]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_1_status log]"
    return 0
}
set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

################################################################################
# Configure protocol interfaces for first topology                             # 
################################################################################ 

# Creating the multivalue object which will be used to address the topology at Layer 2 
set multivalue_1_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          00.11.01.00.00.01       \
        -counter_step           00.00.00.00.00.01       \
        -counter_direction      increment               \
        -nest_step              00.00.01.00.00.00       \
        -nest_owner             $topology_1_handle      \
        -nest_enabled           1                       \
    ]
if {[keylget multivalue_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_1_status log]"
    return 0
}
set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]

# Configuring Layer 2 for the first topology
set ethernet_1_status [::ixiangpf::interface_config 			 \
        -protocol_name                {Ethernet 1}               \
        -protocol_handle              $deviceGroup_1_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 $multivalue_1_handle       \
        -vlan                         0                          \
        -vlan_id                      1                          \
        -vlan_id_step                 0                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
    ]
if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_1_status log]"
    return 0
}
set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

# Creating more multivalue objects that will be used to addres the topology at Layer 3
set multivalue_2_status [::ixiangpf::multivalue_config  \
        -pattern                counter                 \
        -counter_start          100.1.0.1               \
        -counter_step           0.0.0.1                 \
        -counter_direction      increment               \
        -nest_step              0.1.0.0                 \
        -nest_owner             $topology_1_handle      \
        -nest_enabled           1                       \
    ]
if {[keylget multivalue_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_2_status log]"
    return 0
}
set multivalue_2_handle [keylget multivalue_2_status multivalue_handle]
    
	
set multivalue_3_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          101.1.0.1               \
        -counter_step           255.255.255.255         \
        -counter_direction      decrement               \
        -nest_step              0.0.0.1                 \
        -nest_owner             $topology_1_handle      \
        -nest_enabled           0                       \
    ]
if {[keylget multivalue_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_3_status log]"
    return 0
}
set multivalue_3_handle [keylget multivalue_3_status multivalue_handle]

# Setting the gateway for the topology
set ipv4_1_status [::ixiangpf::interface_config \
        -protocol_name                {IPv4 1}                  \
        -protocol_handle              $ethernet_1_handle        \
        -ipv4_resolve_gateway         1                         \
        -ipv4_manual_gateway_mac      00.00.00.00.00.01         \
        -gateway                      $multivalue_3_handle      \
        -intf_ip_addr                 $multivalue_2_handle      \
        -netmask                      255.255.255.0             \
    ]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_1_status log]"
    return 0
}
set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]

################################################################################
# Configure Topology 2, Device Group 2                                         # 
################################################################################      
   
set topology_2_status [::ixiangpf::topology_config \
        -topology_name      {Topology 2}                            \
        -port_handle        $port_2							        \
    ]
if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_2_status log]"
    return 0
}
set topology_2_handle [keylget topology_2_status topology_handle]

    
set device_group_2_status [::ixiangpf::topology_config        \
        -topology_handle              $topology_2_handle      \
        -device_group_name            {Device Group 2}        \
        -device_group_multiplier      45	                  \
        -device_group_enabled         1                       \
    ]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_status log]"
    return 0
}
set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]
    
###############################################################################################################################
# Configure protocol interfaces for second topology - same intermediary steps as for first topology                           # 
############################################################################################################################### 
	
set multivalue_4_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          00.12.01.00.00.01       \
        -counter_step           00.00.00.00.00.01       \
        -counter_direction      increment               \
        -nest_step              00.00.01.00.00.00       \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
if {[keylget multivalue_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_4_status log]"
    return 0
}
set multivalue_4_handle [keylget multivalue_4_status multivalue_handle]


set ethernet_2_status [::ixiangpf::interface_config \
        -protocol_name                {Ethernet 2}               \
        -protocol_handle              $deviceGroup_2_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 $multivalue_4_handle       \
        -vlan                         0                          \
        -vlan_id                      1                          \
        -vlan_id_step                 0                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
    ]
if {[keylget ethernet_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_2_status log]"
    return 0
}
set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]


set multivalue_5_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          101.1.0.1               \
        -counter_step           0.0.0.1                 \
        -counter_direction      increment               \
        -nest_step              0.1.0.0                 \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
if {[keylget multivalue_5_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_5_status log]"
    return 0
}
set multivalue_5_handle [keylget multivalue_5_status multivalue_handle]


set multivalue_6_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          100.1.0.1               \
        -counter_step           255.255.255.255         \
        -counter_direction      decrement               \
        -nest_step              0.0.0.1                 \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           0                       \
    ]
if {[keylget multivalue_6_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_6_status log]"
    return 0
}
set multivalue_6_handle [keylget multivalue_6_status multivalue_handle]


set ipv4_2_status [::ixiangpf::interface_config \
        -protocol_name                {IPv4 2}                  \
        -protocol_handle              $ethernet_2_handle        \
        -ipv4_resolve_gateway         1                         \
        -ipv4_manual_gateway_mac      00.00.00.00.00.01         \
        -gateway                      $multivalue_6_handle      \
        -intf_ip_addr                 $multivalue_5_handle      \
        -netmask                      255.255.255.0             \
    ]
if {[keylget ipv4_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_2_status log]"
    return 0
}
set ipv4_2_handle [keylget ipv4_2_status ipv4_handle]
  
################################################################################
# Configure Topology 3, Device Group 3                                         # 
################################################################################
  
set topology_3_status [::ixiangpf::topology_config 				  \
        -topology_name      {Topology 3}                          \
        -port_handle        $port_3								  \
    ]
if {[keylget topology_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_3_status log]"
    return 0
}
set topology_3_handle [keylget topology_3_status topology_handle]

    
set device_group_3_status [::ixiangpf::topology_config		  \
        -topology_handle              $topology_3_handle      \
        -device_group_name            {Device Group3}         \
        -device_group_multiplier      45                      \
        -device_group_enabled         1                       \
    ]
if {[keylget device_group_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_3_status log]"
    return 0
}
set deviceGroup_3_handle [keylget device_group_3_status device_group_handle]

################################################################################
# Configure protocol interfaces for the third topology                             # 
################################################################################ 

set multivalue_7_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          00.13.01.00.00.01       \
        -counter_step           00.00.00.00.00.01       \
        -counter_direction      increment               \
        -nest_step              00.00.01.00.00.00       \
        -nest_owner             $topology_3_handle      \
        -nest_enabled           1                       \
    ] 
	
if {[keylget multivalue_7_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_7_status log]"
    return 0
}	
set multivalue_7_handle [keylget multivalue_7_status multivalue_handle]


set ethernet_3_status [::ixiangpf::interface_config 			 \
        -protocol_name                {Ethernet 3}               \
        -protocol_handle              $deviceGroup_3_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 $multivalue_7_handle       \
        -vlan                         0                          \
        -vlan_id                      1                          \
        -vlan_id_step                 0                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
    ]
if {[keylget ethernet_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_3_status log]"
    return 0
}
set ethernet_3_handle [keylget ethernet_3_status ethernet_handle]

    
set multivalue_8_status [::ixiangpf::multivalue_config  \
        -pattern                counter                 \
        -counter_start          3000:0:0:1:0:0:0:2      \
        -counter_step           0:0:0:1:0:0:0:0         \
        -counter_direction      increment               \
        -nest_step              0:0:0:1:0:0:0:0         \
        -nest_owner             $topology_3_handle      \
        -nest_enabled           1                       \
    ]
if {[keylget multivalue_8_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_8_status log]"
    return 0
}
set multivalue_8_handle [keylget multivalue_8_status multivalue_handle]
    
set multivalue_9_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          3000:0:1:1:0:0:0:2      \
        -counter_step           0:0:0:1:0:0:0:0         \
        -counter_direction      increment               \
        -nest_step              0:0:0:1:0:0:0:0         \
        -nest_owner             $topology_3_handle      \
        -nest_enabled           1                       \
    ]
if {[keylget multivalue_9_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_9_status log]"
    return 0
}
set multivalue_9_handle [keylget multivalue_9_status multivalue_handle]
   
   
set ipv6_3_status [::ixiangpf::interface_config 					 \
        -protocol_name                     {IPv6 3}                  \
        -protocol_handle                   $ethernet_3_handle        \
        -ipv6_multiplier                   1                         \
        -ipv6_resolve_gateway              1                         \
        -ipv6_manual_gateway_mac           00.00.00.00.00.01         \
        -ipv6_manual_gateway_mac_step      00.00.00.00.00.00         \
        -ipv6_gateway                      $multivalue_9_handle      \
        -ipv6_gateway_step                 ::0                       \
        -ipv6_intf_addr                    $multivalue_8_handle      \
        -ipv6_intf_addr_step               ::0                       \
        -ipv6_prefix_length                64                        \
    ]
if {[keylget ipv6_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv6_3_status log]"
    return 0
}
set ipv6_3_handle [keylget ipv6_3_status ipv6_handle]

################################################################################
# Configure Topology 4, Device Group 4                                         # 
################################################################################

set topology_4_status [::ixiangpf::topology_config 				  \
        -topology_name      {Topology 4}                          \
        -port_handle        $port_4								  \
    ]
if {[keylget topology_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_4_status log]"
    return 0
}
set topology_4_handle [keylget topology_4_status topology_handle]
    
	
set device_group_4_status [::ixiangpf::topology_config		  \
        -topology_handle              $topology_4_handle      \
        -device_group_name            {Device Group4}         \
        -device_group_multiplier      45                      \
        -device_group_enabled         1                       \
    ]
if {[keylget device_group_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_4_status log]"
    return 0
}
set deviceGroup_4_handle [keylget device_group_4_status device_group_handle]

################################################################################
# Configure protocol interfaces for the fourth topology                        # 
################################################################################   
  
set multivalue_10_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          00.14.01.00.00.01       \
        -counter_step           00.00.00.00.00.01       \
        -counter_direction      increment               \
        -nest_step              00.00.01.00.00.00       \
        -nest_owner             $topology_4_handle      \
        -nest_enabled           1                       \
    ]
if {[keylget multivalue_10_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_10_status log]"
    return 0
}
set multivalue_10_handle [keylget multivalue_10_status multivalue_handle]
    
	
set ethernet_4_status [::ixiangpf::interface_config 			 \
        -protocol_name                {Ethernet 4}               \
        -protocol_handle              $deviceGroup_4_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 $multivalue_10_handle      \
        -vlan                         0                          \
        -vlan_id                      1                          \
        -vlan_id_step                 0                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
    ]
if {[keylget ethernet_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_4_status log]"
    return 0
}
set ethernet_4_handle [keylget ethernet_4_status ethernet_handle]

    
set multivalue_11_status [::ixiangpf::multivalue_config  \
        -pattern                counter                 \
        -counter_start          3000:0:1:1:0:0:0:2      \
        -counter_step           0:0:0:1:0:0:0:0         \
        -counter_direction      increment               \
        -nest_step              0:0:0:1:0:0:0:0         \
        -nest_owner             $topology_4_handle      \
        -nest_enabled           1                       \
    ]
if {[keylget multivalue_11_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_11_status log]"
    return 0
}
set multivalue_11_handle [keylget multivalue_11_status multivalue_handle]
   
   
set multivalue_12_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          3000:0:0:1:0:0:0:2      \
        -counter_step           0:0:0:1:0:0:0:0         \
        -counter_direction      increment               \
        -nest_step              0:0:0:1:0:0:0:0         \
        -nest_owner             $topology_4_handle      \
        -nest_enabled           1                       \
    ]
if {[keylget multivalue_12_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_12_status log]"
    return 0
}
set multivalue_12_handle [keylget multivalue_12_status multivalue_handle]
   
   
set ipv6_4_status [::ixiangpf::interface_config 					 \
        -protocol_name                     {IPv6 4}                  \
        -protocol_handle                   $ethernet_4_handle        \
        -ipv6_multiplier                   1                         \
        -ipv6_resolve_gateway              1                         \
        -ipv6_manual_gateway_mac           00.00.00.00.00.01         \
        -ipv6_manual_gateway_mac_step      00.00.00.00.00.00         \
        -ipv6_gateway                      $multivalue_12_handle      \
        -ipv6_gateway_step                 ::0                       \
        -ipv6_intf_addr                    $multivalue_11_handle      \
        -ipv6_intf_addr_step               ::0                       \
        -ipv6_prefix_length                64                        \
    ]
if {[keylget ipv6_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv6_4_status log]"
    return 0
}
set ipv6_4_handle [keylget ipv6_4_status ipv6_handle]


 
####################################################
##Configure traffic for all configuration elements##

##########################################################
# Configure trafficItem 1 for Layer 4-7 AppLibrary Profile
##########################################################

# Creating the list of flows that will be added in the first Traffic Item

set flows1 {
IRC_Login_Auth_Failure \
IRC_Private_Chat \
iSCSI_Read_and_Write \
iTunes_Desktop_App_Store \
iTunes_Mobile_App_Store \
Jabber_Chat \
Laposte_Webmail_1307 \
LinkedIn \
Linkedin_1301 \
LPD \
}

# Using the configuration command to set the parameters and create the first traffic item
# One can set the below parameters to any other valid values and fine tune the traffic item setup

set traffic_item_1_status [::ixiangpf::traffic_l47_config																  \
        -mode                        create																				  \
        -name                        Traffic_Item_1																		  \
        -circuit_endpoint_type       ipv4_application_traffic															  \
        -emulation_src_handle        $topology_1_handle																	  \
        -emulation_dst_handle        $topology_2_handle																	  \
        -objective_type              users																				  \
        -objective_value             100																				  \
        -objective_distribution      apply_full_objective_to_each_port													  \
        -enable_per_ip_stats         1																					  \
        -flows                       $flows1																			  \
    ]
if {[keylget traffic_item_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_item_1_status log]"
    return 0
}

# Also, other modes and attributes can be found in HLAPI documentation	
	
##########################################################
# Configure trafficItem 2 for Layer 4-7 AppLibrary Profile
##########################################################

# Creating the list of flows that will be added in the first Traffic Item

set flows2 { 
MAX_Bandwidth_HTTP \
Microsoft_Update \
MMS_MM1_WAP_HTTP \
Modbus \
MS_SQL_Create \
MS_SQL_Delete \
MS_SQL_Drop \
MS_SQL_Insert \
MS_SQL_Server \
MS_SQL_Server_Advanced \
}

# Using the configuration command to set the parameters and create the first traffic item
# One can set the below parameters to any other valid values and fine tune the traffic item setup

set traffic_item_2_status [::ixiangpf::traffic_l47_config																  \
        -mode                        create																				  \
        -name                        Traffic_Item_2																		  \
        -circuit_endpoint_type       ipv6_application_traffic															  \
        -emulation_src_handle        $topology_3_handle																	  \
        -emulation_dst_handle        $topology_4_handle																	  \
        -objective_type              users																				  \
        -objective_value             100																				  \
        -objective_distribution      apply_full_objective_to_each_port													  \
        -enable_per_ip_stats         1																					  \
        -flows                       $flows2																			  \
    ]
if {[keylget traffic_item_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_item_2_status log]"
    return 0
}

	
# Also, other modes and attributes can be found in HLAPI documentation

# Setting handles for further usage when calling different modes for traffic config or traffic stats commands
set trafficItem_1_handle [keylget traffic_item_1_status traffic_l47_handle]
set responder_ports_item1 [keylget traffic_item_1_status $trafficItem_1_handle.responder_ports]
set applib_handle_item1 [keylget traffic_item_1_status $trafficItem_1_handle.applib_profile]
set applib_flow_item1 [keylget traffic_item_1_status $trafficItem_1_handle.$applib_handle_item1.applib_flow]
set responder_port_item1 [lindex $responder_ports_item1 0]
	
	
set trafficItem_2_handle [keylget traffic_item_2_status traffic_l47_handle]
set responder_ports_item2 [keylget traffic_item_2_status $trafficItem_2_handle.responder_ports]
set applib_handle_item2 [keylget traffic_item_2_status $trafficItem_2_handle.applib_profile]
set applib_flow_item2 [keylget traffic_item_2_status $trafficItem_2_handle.$applib_handle_item2.applib_flow]
set responder_port_item2 [lindex $responder_ports_item2 0]


####################################################
# Start protocols
####################################################
	 
set _result_ [::ixia::test_control -action start_all_protocols -port_handle $port_handle]
after 10000


################################################################################
# Start traffic                                                                # 
################################################################################

puts "Running traffic"
set run_traffic [::ixiangpf::traffic_control					   	\
        -action				 run 								\
        -traffic_generator  ixnetwork_540 						\
        -type				l47 								\
    ]
if {[keylget run_traffic status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget run_traffic log]"
    return 0
}


###############################################################################
# Performing drill downs on the TCP Statistics views
###############################################################################

# Using the traffic_stats command to execute drill-downs on statistics
# The drill down is made on the TCP statistics views on the first flow in each traffic item

set stats [::ixiangpf::traffic_stats	\
					-mode							L47_traffic_item_tcp			\
					-drill_down_type				per_ports_per_initiator_flows	\
					-drill_down_traffic_item		$trafficItem_1_handle			\
					-drill_down_port				$port_1							\
					-drill_down_flow				[lindex $flows1 0]				\
				] 
if {[keylget stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stats log]"
    return 0
}
after 3000

set stats [::ixiangpf::traffic_stats	\
					-mode							L47_flow_initiator_tcp			\
					-drill_down_type				per_initiator_ports				\
					-drill_down_traffic_item		$trafficItem_2_handle			\
					-drill_down_port				$port_3							\
					-drill_down_flow				[lindex $flows2 1]				\
				] 
if {[keylget stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stats log]"
    return 0
}
after 3000

# There are several other option for the drill-down to be executed. These options can be found in the HLAPI documentation.				

#################################################### 
# Stop traffic
####################################################

puts "Stopping traffic"
set run_traffic [::ixiangpf::traffic_control					   	\
        -action				stop 								\
        -traffic_generator  ixnetwork_540 						\
        -type				l47 								\
    ]
if {[keylget run_traffic status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget run_traffic log]"
    return 0
}
after 15000

#################################################### 
# Test END
####################################################

puts "###################"
puts "Test run is PASSED"
puts "###################"
return 1

##################################################################################################################################################
##################################################################################################################################################

