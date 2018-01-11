################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright ? 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    10/2/2014 - Alexandra Apetroaei - created sample   	                   #
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
# The script creates one Custom TLV and adds it and another predefined TLV     #
# to the configuration.                                                        #
# Start/Stop protocols.                                                        #
# Module:                                                                      #
#    The sample was tested on an FlexAP10G16S module.                          #
# Software:                                                                    #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################


set ports       {{10.205.15.90 11 3} {10.205.15.90 11 4}}

package req IxTclNetwork

puts "Connecting to Ixnetwork..."
ixNet connect ixro-smqa-r-22 -port 8009 -version 7.40

puts "Cleaning up IxNetwork..."
ixNet execute newConfig

# all objects are under root
set root [ixNet getRoot]

puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 [lindex $vPorts 0]
set vport2 [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ports {} $vPorts force

# Rebooting the ports
foreach vp $vPorts {lappend jobs [ixNet -async exec resetPortCpuAndFactoryDefault $vp]}
foreach j $jobs {ixNet isSuccess $j}


after 5000
ixNet execute clearStats

puts "# ######################## Add DHCP DGs ####################################### #"

puts "Adding 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vport1
ixNet add [ixNet getRoot] topology -vports $vport2
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

puts "Adding 2 device groups, one for the client, multiplier is set to 15 and one for the server, multiplier is set to 1"
ixNet add $topo1 deviceGroup -multiplier 1
ixNet add $topo2 deviceGroup -multiplier 15
ixNet commit

set t1dev1 [ixNet getList $topo1 deviceGroup]
set t2dev1 [ixNet getList $topo2 deviceGroup]

# naming the topologies and the device groups
ixNet setAttr $topo1  -name "DHCP Topology-1"
ixNet setAttr $topo2  -name "DHCP Topology-2"
ixNet setAttr $t1dev1 -name "Server"
ixNet setAttr $t2dev1 -name "Client"
ixNet commit

puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]
set mac2 [ixNet getList $t2dev1 ethernet]

puts "Adding DHCPv4 Server "
puts "First we need to add IP layer because DHCP server is stacked on it"
ixNet add $mac1 ipv4
ixNet commit
set dhcpv4S [ixNet add [ixNet getList $mac1 ipv4] dhcpv4server]

puts "Disable the Resolve gateway checkbox for DHCPv4 Server"
set ip [ixNet getList $mac1 ipv4]
ixNet setA [ixNet getA $ip -resolveGateway]/singleValue -value false
ixNet commit

puts "Setting Start Pool Address for DHCPv4 Servers"
ixNet setA [ixNet getA $dhcpv4S/dhcp4ServerSessions -ipAddress]/counter -start 100.1.0.20
ixNet commit

puts "Setting DHCPv4 Server Pool Count to 15"
ixNet setA [ixNet getA $dhcpv4S/dhcp4ServerSessions -poolSize]/singleValue -value 15
ixNet commit

puts "Adding DHCPv4 Client"
ixNet add $mac2 dhcpv4client
ixNet commit

set dhcpServer [ixNet remapIds $dhcpv4S]

set dhcpClient [ixNet getL $mac2 dhcpv4client]

puts "# ######################## End Add DHCP DGs ################################## #"

# ###################### Create a Custom TLV ################################ #
# ###################### Create a Custom TLV ################################ #


puts "# ###################### Create a Custom TLV ################################ #"


puts  "Get global templates"
set global_config [lindex [ixNet getList $root globals] 0]
set global_top [lindex [ixNet getList $global_config topology] 0]
set global_dhcp [lindex [ixNet getList $global_top dhcpv4client] 0]
set global_tlv_editor [lindex [ixNet getList $global_dhcp tlvEditor] 0]
set global_default_template [lindex [ixNet getList [lindex [ixNet getList $global_tlv_editor defaults] 0] template] 0]


puts "Create a custom TLV"

puts "Add a new template"
set new_template [ixNet add $global_tlv_editor template]
ixNet commit

puts "Change the name"
ixNet setAttribute $new_template -name  "Test Template"
ixNet commit

puts "Add a new TLV"
set new_tlv [ixNet add $new_template tlv]
ixNet commit

puts "Change the name"
ixNet setAttribute $new_tlv -name "Test TLV"
ixNet commit

puts "Modify Length"

set new_tlv_length [lindex [ixNet getList $new_tlv length] 0]

puts "Modify Length Attributes"

puts "Set the name"
ixNet setAttribute $new_tlv_length -name "Length"
ixNet commit

puts "Change the Value for Length"
set value_mv [ixNet getAttribute $new_tlv_length -value]
ixNet setAttribute $value_mv -pattern singleValue
ixNet commit

set value_mv_singleValue [lindex [ixNet getList $value_mv singleValue] 0]
ixNet setMultiAttribute $value_mv_singleValue -value 2
ixNet commit

puts "Modify type"

set new_tlv_type [ lindex [ixNet getList $new_tlv type] 0]

puts "Set the name"
ixNet setAttribute $new_tlv_type -name Type
ixNet commit

set new_object [ixNet add $new_tlv_type object]
ixNet commit

set new_field  [ixNet add $new_object field]
ixNet commit

puts "Modify Field Attributes"

puts "Set the name"
ixNet setAttribute $new_field -name Code
ixNet commit

puts "Change the Code for Type"
set value_mv [ixNet getAttribute $new_field -value]
ixNet setAttribute $value_mv -pattern singleValue
ixNet commit
set value_mv_singleValue [lindex [ixNet getList $value_mv singleValue] 0]
ixNet setMultiAttribute $value_mv_singleValue -value 150
ixNet commit

puts "Modify value"
set new_value [lindex [ixNet getList $new_tlv value] 0]

puts "Edit Value Atributes"

puts "Set the name"
ixNet setAttribute $new_value -name value
ixNet commit

puts "Add a container with two fields"
set new_object [ixNet add $new_value object]
set new_container [ixNet add $new_object container]
set new_object_1 [ixNet add $new_container object]
set new_object_2 [ixNet add $new_container object]

set new_field_1 [ixNet add $new_object_1 field]
set new_field_2 [ixNet add $new_object_2 field]
ixNet commit

puts "Modify Field Attributes"

puts "Set the name"
ixNet setAttribute $new_field_1 -name "Field_1"
ixNet commit

puts "Change the Value for Field_1"
set value_mv [ixNet getAttribute $new_field_1 -value]
ixNet setAttribute $value_mv -pattern singleValue
ixNet commit
set value_mv_singleValue [lindex [ixNet getList $value_mv singleValue] 0]
ixNet setMultiAttribute $value_mv_singleValue -value 4
ixNet commit

puts "Set the name"
ixNet setAttribute $new_field_1 -name  "Field_2"
ixNet commit

puts "Change the Value for Field_2"
set value_mv [ixNet getAttribute $new_field_2 -value]
ixNet setAttribute $value_mv -pattern singleValue
ixNet commit
set value_mv_singleValue [lindex [ixNet getList $value_mv singleValue] 0]
ixNet setMultiAttribute $value_mv_singleValue -value 5
ixNet commit

puts "Add a subTlv with two fields"

set new_object [ixNet add $new_value object]
set new_subtlv [ixNet add $new_object subTlv]
ixNet commit

puts "Modify Length"

set new_tlv_length [lindex [ixNet getList $new_subtlv length] 0]

puts "Modify Length Attributes"

puts "Set the name"
ixNet setAttribute $new_tlv_length -name "Length"
ixNet commit

puts "Change the Value for Length"
set value_mv [ixNet getAttribute $new_tlv_length -value]
ixNet setAttribute $value_mv -pattern singleValue
ixNet commit
set value_mv_singleValue [lindex [ixNet getList $value_mv singleValue] 0]
ixNet setMultiAttribute $value_mv_singleValue -value 2
ixNet commit


puts "Modify type"

set new_tlv_type [lindex [ixNet getList $new_subtlv type] 0]

puts "Set the name"
ixNet setAttribute $new_tlv_type -name  "Type"
ixNet commit

set new_object [ixNet add $new_tlv_type object]
ixNet commit

set new_field [ixNet add $new_object field]
ixNet commit

puts "Modify Field Attributes"

puts "Set the name"
ixNet setAttribute $new_field -name "Code"
ixNet commit

puts "Change the Code for Type"
set value_mv [ixNet getAttribute $new_field -value]
ixNet setAttribute $value_mv -pattern singleValue
ixNet commit
set value_mv_singleValue [lindex [ixNet getList $value_mv singleValue] 0]
ixNet setMultiAttribute $value_mv_singleValue -value 1
ixNet commit


puts "Adding the two fields"

set new_value [lindex [ixNet getList $new_subtlv value] 0]

set new_object_1 [ixNet add $new_value object]
set new_object_2 [ixNet add $new_value object]

set new_field_1 [ixNet add $new_object_1 field]
set new_field_2 [ixNet add $new_object_2 field]
ixNet commit

puts "Modify Field Attributes"

puts "Set the name"
ixNet setAttribute $new_field_1 -name "Field_1"
ixNet commit

puts "Change the Value for Field_1"
set value_mv [ixNet getAttribute $new_field_1 -value]
ixNet setAttribute $value_mv -pattern singleValue
ixNet commit
set value_mv_singleValue [lindex [ixNet getList $value_mv singleValue] 0]
ixNet setMultiAttribute $value_mv_singleValue -value 4
ixNet commit

puts "Set the name"
ixNet setAttribute $new_field_2 -name "Field_2"
ixNet commit

puts "Change the Value for Field_2"
set value_mv [ixNet getAttribute $new_field_2 -value]
ixNet setAttribute $value_mv -pattern singleValue
ixNet commit
set value_mv_singleValue [lindex [ixNet getList $value_mv singleValue] 0]
ixNet setMultiAttribute $value_mv_singleValue -value 5
ixNet commit

puts "# ###################### End Create a Custom TLV ################################ #"

# ###################### Add TLVs to DCPv4 Client ############################## #
# ###################### Add TLVs to DCPv4 Client ############################## #

puts "# ###################### Add TLVs to DCPv4 Client ############################## #"

set dhcpv4_tlvProfile [lindex [ixNet getList $dhcpClient tlvProfile] 0]

puts "Getting default TLV"
set dhcp_default_tlv [lindex [ixNet getList $dhcpv4_tlvProfile defaultTlv] 0]

puts "Adding TLVs to the DHCP client"
set prototype_custom_tlv_1_name "Test TLV"
set prototype_predefined_tlv_1_name  "\[12\] Host Name"

set global_predefined_tlv_1 [ixNet getFilteredList $global_default_template tlv -name $prototype_predefined_tlv_1_name]
set global_predefined_custom_tlv_1 [ixNet getFilteredList $new_template tlv -name $prototype_custom_tlv_1_name]

set predefined_tlv_1 [ixNet -strip execute copyTlv $dhcpv4_tlvProfile $global_predefined_tlv_1]
ixNet commit
set custom_tlv_1 [ixNet -strip execute copyTlv $dhcpv4_tlvProfile $global_predefined_custom_tlv_1]
ixNet commit

#ixNet help $predefined_tlv_1
set messages [ixNet getAttribute $predefined_tlv_1 -availableIncludeInMessages]
set discover [lindex $messages 0]
set request [lindex $messages 1]
set decline [lindex $messages 2]
set release [lindex $messages 3]


puts "# ###################### Configure TLV values ############################## #"

puts "Configure TLV values"

puts "Change the Value for TLV 18"
set predefined_tlv_1_value [lindex [ixNet getList $predefined_tlv_1 value] 0]
set predefined_tlv_1_value_object [lindex [ixNet getList $predefined_tlv_1_value object] 0]
set predefined_tlv_1_value_object_field [lindex [ixNet getList $predefined_tlv_1_value_object field] 0]

set value_mv [ixNet getAttribute $predefined_tlv_1_value_object_field -value]
ixNet setAttribute $value_mv -pattern singleValue
ixNet commit
set value_mv_singleValue [lindex [ixNet getList $value_mv singleValue] 0]
ixNet setMultiAttribute $value_mv_singleValue -value "Custom_Value"
ixNet commit

puts "Enable SubTlv 1 for the Default TLV, Option 55"
set default_tlv_1_value [lindex [ixNet getList $dhcp_default_tlv value] 0]
set default_tlv_1_value_object [lindex [ixNet getList $predefined_tlv_1_value object] 0]
set default_tlv_1_value_object_field [lindex [ixNet getList $predefined_tlv_1_value_object field] 0]
ixNet setAttribute $default_tlv_1_value_object_field -isEnabled true
ixNet commit

puts "Change the Value for one of the fields in the sub Tlv of the custom created TLV"

set custom_tlv_1_value [lindex [ixNet getList $custom_tlv_1 value] 0]
set custom_tlv_1_value_object_1 [lindex [ixNet getList $custom_tlv_1_value object] 1]
set custom_tlv_1_value_object_1_subTlv [lindex [ixNet getList $custom_tlv_1_value_object_1 subTlv] 0]

set subTlv_value [lindex [ixNet getList $custom_tlv_1_value_object_1_subTlv value] 0]
set subTlv_value_object_1 [lindex [ixNet getList $subTlv_value object] 0]
set custom_tlv_1_value_object_1_field [lindex [ixNet getList $subTlv_value_object_1 field] 0]

set value_mv [ixNet getAttribute $custom_tlv_1_value_object_1_field -value]
ixNet setAttribute $value_mv -pattern singleValue
ixNet commit
set value_mv_singleValue [lindex [ixNet getList $value_mv singleValue] 0]
ixNet setMultiAttribute $value_mv_singleValue -value 20
ixNet commit

puts "Set Include in Messages"

ixNet setAttribute $predefined_tlv_1 -includeInMessages [list $discover $request $release]
ixNet setAttribute $dhcp_default_tlv -includeInMessages [list $discover $request $decline]
ixNet setAttribute $custom_tlv_1 -includeInMessages [list $request $release]
ixNet commit

puts "# ################################### Dynamics ############################### #"
#starting topologies

puts "Starting DHCP Servers"
ixNet exec start $dhcpServer
puts "Wait 5 sec"
after 5000

puts "Starting DHCP Clients"
ixNet exec start $dhcpClient

puts "Wait 2 minutes"
after 120000

puts "Printing learned info for DHCPv4 Client"
foreach add [ixNet getA $dhcpClient -discoveredAddresses] {
	puts $add
}

puts "Stopping the clients"
ixNet exec stop $t2dev1
after 5000
puts "Stopping the servers"
ixNet exec stop $t1dev1
after 10000

puts "Unassigning ports..."
ixTclNet::UnassignPorts
puts "Done... Ports are unassigned..."
puts ""

puts "Cleaning up IxNetwork..."
ixNet exec newConfig
ixNet disconnect

puts "Done... IxNetwork session is closed..."
puts ""
puts "!!! TEST DONE !!!"
