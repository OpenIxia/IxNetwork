#!/usr/bin/tclsh
################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################


################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia Keysight and #
# have     																	   #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia Keysight and/or by the user and/or by a third party)] shall at  #
# all times 																   #
# remain the property of Ixia Keysight.                                        #
#                                                                              #
# Ixia Keysight does not warrant (i) that the functions contained in the script#
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND Ixia Keysight#
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL Ixia Keysight BE LIABLE FOR ANY DAMAGES RESULTING FROM OR  #
# ARISING   																   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF Ixia Keysight HAS BEEN ADVISED OF THE          #
# POSSIBILITY OF  SUCH DAMAGES IN ADVANCE.                                     #
# Ixia Keysight will not be required to provide any software maintenance or    #
# support services of any kind (e.g. any error corrections) in connection with #
# script or any part thereof. The user acknowledges that although Ixia Keysight# 
# may     																	   #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia Keysight to  #
# provide any additional maintenance or support services.                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    Script  will create following:                                            #
#    1. Create PPPoX Client                                                    #
#    2.	Setting DSL type in DSL line Attribute.                                #
#    3. Setting CUSTOM TLV in DSL Line Attribute..	     					   #
#  	 4. Setting 01 Access-Loop-Circuit-ID	   	   							   #
#	 5. Setting PON-Access-Line-Attributes                             		   #
#                                                                              #
################################################################################

#edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.64.169
    set ixTclPort   8876
    set ports       {{10.39.65.151 9 1} {10.39.65.151 9 2}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.50

puts "Creating a new config"
ixNet exec newConfig

puts "Adding 2 vports"
ixNet add 				[ixNet getRoot] vport
ixNet add 				[ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 				[lindex $vPorts 0]
set vport2 				[lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force
after 5000

puts "*********************************************************************"
puts "Create  topology with PPPoX client and PPPoX Client"
puts "*********************************************************************"
puts "Adding 2 topologies"
ixNet add 	[ixNet getRoot] topology -vports $vport1
ixNet add 	[ixNet getRoot] topology -vports $vport2
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 				[lindex $topologies 0]
set topo2 				[lindex $topologies 1]

puts "Adding 2 device groups, one for the client, \
	  multiplier is set to 1 and one for the server, multiplier is set to 1"
ixNet add $topo1 deviceGroup -multiplier 10
ixNet add $topo2 deviceGroup -multiplier 1
ixNet commit

set t1dev1 				[ixNet getList $topo1 deviceGroup]
set t2dev1 				[ixNet getList $topo2 deviceGroup]

# naming the topologies and the device groups
ixNet setAttr $topo1  -name "PPP Topology-1"
ixNet setAttr $topo2  -name "PPP Topology-2"
ixNet setAttr $t1dev1 -name "Clients"
ixNet setAttr $t2dev1 -name "Servers"
ixNet commit

puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit
set mac1 				[ixNet getList $t1dev1 ethernet]
set mac2 				[ixNet getList $t2dev1 ethernet]


puts "Adding PPP Server and Client stack"
set ppp_client 			[ixNet add $mac1 pppoxclient]
set ppp_server 			[ixNet add $mac2 pppoxserver]
ixNet commit

puts "Setting PPP Server Sessions Count to 1"
ixNet setA $ppp_server -sessionsCount 10

set root 				[ixNet getRoot]
set topo 				[ixNet getL $root topology ]
set device_group 		[ixNet getL [lindex $topo 0] deviceGroup]
set eth 				[ixNet getL $device_group ethernet]
set pppox_client 		[ixNet getL $eth pppoxclient]
puts "Setting ponTypeTlv to GPON "
set pon_tlv 			[ixNet getAttribute $pppox_client -ponTypeTlv]
set single_val 			[ixNet add $pon_tlv "singleValue"]
ixNet setMultiAttribute $single_val -value gpon
ixNet commit

set tlv_profile 		[ixNet getL $pppox_client tlvProfile]
set device_group_server [ixNet getL [lindex $topo 1] deviceGroup]
set eth_server 			[ixNet getL $device_group_server ethernet]
set pppox_server 		[ixNet getL $eth_server pppoxserver]

puts  "Get global templates"
set global_config 		[lindex [ixNet getList $root globals] 0]
set global_top 			[lindex [ixNet getList $global_config topology] 0]
set global_ppp 			[lindex [ixNet getList $global_top pppoxclient] 0]
set global_tlv_editor 	[lindex [ixNet getList $global_ppp tlvEditor] 0]
set global_template 	[lindex [ixNet getList [lindex [ixNet getList $global_tlv_editor defaults] 0] template] 0]


puts "***********************************************************************"
puts "				Setting DSL type in DSL line Attribute..				 "
puts "***********************************************************************"

# This part is doing following:
# 1. Create DSL line Attribute TLV
# 2. It will search for sub tlv and put the object in req_tlv variable
# 3. Fetch required type TLV handle which corresponds to particular index value in sub tlv value handle list
# 4. Enable  DSL type sub tlv by enabling tlv_is_enabled parameter
# 5. Set value field for subtlv to 123

set dsl			 			{DSL-Line-Attributes}

puts "Configure $dsl tlv"
# Get DSL Line attribute TLV from many default templates
set dsl_line_attribute 	[ixNet getFilteredList $global_template tlv -name $dsl]
ixNet commit

# Copy DSL Line attribute TLV template to tlv profile
puts "dsl_line_attribute : $dsl_line_attribute"
set dsl_line_attribute_tlv  [ixNet -strip execute copyTlv $tlv_profile $dsl_line_attribute]
ixNet commit

puts "dsl_line_attribute_tlv: $dsl_line_attribute_tlv"
set parent_tlv_value 	 	[ixNet getL $dsl_line_attribute_tlv value]
set parent_tlv_object 	 	[ixNet getL $parent_tlv_value object]

#Searching for [84] Minimum-Net-Data-Rate-Downstream tlv and put the object in req_tlv variable
set req_tlv ""
set tlv_name ""
foreach obj $parent_tlv_object {
	set dsl_tlv 	{[84] Minimum-Net-Data-Rate-Downstream}
	if { [ixNet getA $obj -name] eq $dsl_tlv } {
		set tlv_name [ixNet getA $obj -name]
		set req_tlv $obj
	}
}
set sub_tlv 				[ixNet getL $req_tlv subTlv]

# Enable sub tlv
ixNet setMultiAttribute $sub_tlv \
	-isEnabled true
ixNet commit

puts "\n\n Change the type for tlv name $req_tlv to value 456 \n\n"

# Get sub-tlv value
set dsl_type_tlv_value 		[ixNet getL $sub_tlv value]

# Get Sub-tlv value object
set dsl_type_tlv_obj 		[ixNet getL $dsl_type_tlv_value object]

# Get Sub-Tlv field value
set dsl_type_field 			[ixNet getL $dsl_type_tlv_obj field]
set dsl_type_tlv_field_value [ixNet getAttr $dsl_type_field -value]
set dsl_counter_value 		[ixNet add $dsl_type_tlv_field_value "counter"]

# Modify field value for sub-tlv
ixNet setMultiAttribute  $dsl_counter_value \
	-step 01 \
	-start 456 \
	-direction increment
ixNet commit

puts "***********************************************************************"
puts "				Setting CUSTOM TLV in DSL Line Attribute..				 "
puts "***********************************************************************"
# This part is doing following:
# 1. It will search for Custom Sub Tlv in  DSL Line Attribute and put the object in req_tlv variable
# 2. Fetch required custom TLV handle which corresponds to particular index value in sub tlv value handle list
# 3. Enable Custom sub tlv by enabling tlv_is_enabled parameter
# 4. Set value field for custom_sub_tlv to 123
# 5. Fetch custom tlv type handle
# 6. Fetching custom tlv type field handle


#Searching for [00] Custom TLV  and put the object in req_tlv variable
set req_tlv ""
set tlv_name ""
foreach obj $parent_tlv_object {
	set dsl_tlv {[00] Custom TLV}
	if { [ixNet getA $obj -name] eq $dsl_tlv } {
		set tlv_name [ixNet getA $obj -name]
		set req_tlv $obj
	}
}

set sub_tlv [ixNet getL $req_tlv subTlv]
# Enable sub tlv
ixNet setMultiAttribute $sub_tlv \
	-isEnabled true
ixNet commit

# Get sub-tlv type field value
set tlv_val 			[ixNet getL $sub_tlv type]
# Get Sub-tlv type field object
set tlv_obj_val 		[ixNet getL $tlv_val object]
# Get Sub-Tlv type field 
set obj_field_val 		[ixNet getL $tlv_obj_val field]
set obj_value 			[ixNet getA $obj_field_val -value]
set obj_counter 		[ixNet add $obj_value "counter"]

# Modify field value for sub-tlv type
puts "\n\n Change the type for tlv name $req_tlv to value aa \n\n"
ixNet setMultiAttribute $obj_counter \
	-step 01 \
	-start aa \
	-direction increment
ixNet commit

puts "Change the type for $req_tlv to value aabbccdd"
# Get sub-tlv value
set tlv_val 			[ixNet getL $sub_tlv value]
# Get Sub-tlv value object
set tlv_obj_val 		[ixNet getL $tlv_val object]
# Get Sub-Tlv value field 
set obj_field_val 		[ixNet getL $tlv_obj_val field]
set obj_value 			[ixNet getA $obj_field_val -value]
set obj_counter 		[ixNet add $obj_value "counter"]

# Modify field value for sub-tlv value
ixNet setMultiAttribute $obj_counter \
	-step 01 \
	-start aabbccdd \
	-direction increment
ixNet commit


puts "***************************************************"
puts "				Setting 01 Access-Loop-Circuit-ID..	 "
puts "***************************************************"
set access_loop			 			{[01] Access-Loop-Circuit-ID}
puts "Configure $access_loop tlv"

# Get Access-Loop-Circuit-ID TLV from many default templates
set access_loop_circuit [ixNet getFilteredList $global_template tlv -name $access_loop]
ixNet commit

# Copy Access-Loop-Circuit-ID TLV template to tlv profile
set access_loop_tlv		 		[ixNet -strip execute copyTlv $tlv_profile $access_loop_circuit]
ixNet commit
# Get tlv value
set access_loop_tlv_value 			[ixNet getL $access_loop_tlv value]
# Get tlv value object
set access_loop_tlv_object 			[ixNet getL $access_loop_tlv_value object]
# Get Tlv field value
set access_loop_tlv_field 			[ixNet getL $access_loop_tlv_object field]
set access_loop_tlv_field_value 	[ixNet getAttr $access_loop_tlv_field -value]
ixNet setMultiAttribute $access_loop_tlv_field_value -clearOverlays false
ixNet commit
set access_loop_single_value [ixNet add $access_loop_tlv_field_value "singleValue"]

puts "access_loop_single_value : $access_loop_single_value"
puts "\n\n Change the value for tlv name $access_loop to  circuit1 \n\n"
ixNet setMultiAttribute $access_loop_single_value \
	-value circuit1
ixNet commit

puts "******************************************************"
puts "			Setting PON-Access-Line-Attributes"
puts "******************************************************"
# This part is doing following:
# 1. Create PON-Access-Line-Attributes TLV
# 2. It will search for [96] sub tlv  and put the object in req_tlv variable
# 3. Fetch required  [96] type TLV handle which corresponds to particular index value in sub tlv value handle list
# 4. Enable [96] type sub tlv by enabling tlv_is_enabled parameter
# 5. Set value field for [96] subtlv to 123345

set pon_attribute			 	{PON-Access-Line-Attributes}
puts "Configure $pon_attribute tlv"
set pon_attribute_data 			[ixNet getFilteredList $global_template tlv -name $pon_attribute]
ixNet commit
set pon_attribute_tlv 		 		[ixNet -strip execute copyTlv $tlv_profile $pon_attribute_data]
ixNet commit
set parent_tlv_value 			[ixNet getL $pon_attribute_tlv value]
set parent_tlv_object 			[ixNet getL $parent_tlv_value object]

#Searching for [96] ONT/ONU-Assured-Data-Rate-Upstream tlv and put the object in req_tlv variable
set req_tlv ""
set tlv_name ""
foreach obj $parent_tlv_object {
	set pon_tlv 	{[96] ONT/ONU-Assured-Data-Rate-Upstream}
	if { [ixNet getA $obj -name] eq $pon_tlv } {
		set tlv_name [ixNet getA $obj -name]
		set req_tlv $obj
	}
}

set sub_tlv 				[ixNet getL $req_tlv subTlv]
ixNet setMultiAttribute $sub_tlv \
	-isEnabled true
ixNet commit

puts "\n\n Change the type for tlv name $req_tlv to value 4561 \n\n"
set ont_onu_tlv_value 		[ixNet getL $sub_tlv value]
set ont_onu_tlv_obj 		[ixNet getL $ont_onu_tlv_value object]
set ont_onu_field 			[ixNet getL $ont_onu_tlv_obj field]
set ont_onu_tlv_field_value [ixNet getAttr $ont_onu_field -value]
set ont_onu_counter_value 		[ixNet add $ont_onu_tlv_field_value "counter"]
ixNet setMultiAttribute  $ont_onu_counter_value \
	-step 01 \
	-start 4561 \
	-direction increment
ixNet commit


puts "Starting PPP Server"
ixNet exec start $pppox_server
puts "Wait 5 sec"
after 5000

puts "Starting PPP Clients"
ixNet exec start $pppox_client

puts "Wait 20 seconds"
after 20000

puts "Stopping the clients"
ixNet exec stop $t1dev1

puts "Stopping the servers"
ixNet exec stop $t2dev1
after 10000

puts "Unassigning ports..."
ixTclNet::UnassignPorts
puts "Done... Ports are unassigned..."
puts ""

puts "Cleaning up IxNetwork..."
ixNet exec newConfig
ixNet disconnect

puts "Done... IxNetwork session is disconnected..."
puts ""
puts "!!! TEST DONE !!!"

return 0