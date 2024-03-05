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

# ##############################################################################
# Description:                                                                 #
# This script will demonstrate Bonded GRE as per RFC 8157                      #
#     Script  will do following:                                               #
#    1. Load the config bonded_gre_sample_script.ixncfg                        #
#        Config has following:                                                 #
#        a. Config having HAAP side simulation pre configured                  #
#        b. Client side Bonded GRE will be configured in this sample           #
#    2.  Create Bonded GRE topology                                            #
#    3.  Create Link TLV {[77] Link Type]}                                     #
#        and custom TLV {[xx] Bonded GRE Custom TLV}                           #
#        These TLV 's are not mandatory to create                              #
#    4.  Start Protocol in following order as start all protocol not supported #
#        a. Start LTE Bonded GRE device group                                  #
#        b. Start DSL Bonded GRE device group                                  #
#        c. Start HAAP GRE   												   #
#		 d. Simulate control traffic after starting device group mentioned in  #
#			steps from (a to c) for LTE and DSL setup Accept message so that   #
#			Bonded GRE to come up.                                             #
#        d. Start HAAP DHCP server                                             #
#        e. Start Home Gateway dhcp client                                     #
#    5. Create data traffic between HomeGateway DHCP Client to DHCP IPv4 Server#
#    6. Send Active Hello Notify packet from HAAP to Home Gateway.             #
#    7. Send right click actions like stop hello, resume hello, overflowLte    #
#    8. Check following session info state:                                    #
#       a. Bonded Gateway Session Info                                         #
#       b. Home Gateway Session Info 										   #
#	 9. Send LTE tear down control traffic from HAAP to HG  	               #
#    10. Stop and start Bonded GRE LTE after tear down                         #
#    11. Send Tear Down from Home Gateway to HAAP with error code 11           #
#    12. Check     Stats                                                       #
#    13. Stop Protocols                                                        #
#    14.Disable Tlv                                                            #
# Module:                                                                      #
#    The sample was tested on a 10GE LSM  module.                              #
#                                                                              #
# ##############################################################################

namespace eval ::ixia {
    set ixTclServer 10.39.65.1
    set ixTclPort   9862
    set ports       {{10.39.64.117 2 5} {10.39.64.117 2 6}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork


# Procedure for enabling traffic item and regenerate
proc traffitem_enable_regenerate {tItemName} {
	set root [ixNet getRoot]
	set traffic [ixNet getL $root traffic]
	set traffic_items [ixNet getL $traffic trafficItem]
	set flag 1
	foreach item $traffic_items {
		set name [ixNet getAttribute $item -name]
		if {$name == $tItemName} {
			ixNet setMultiAttribute $item -enabled true
			ixNet commit
			ixNet execute generate $item
			set flag 0
	return $flag
		
		}
	}
}

# Procedure for disabling traffic item 
proc traffitem_disable {tItemName} {
	set root [ixNet getRoot]
	set traffic [ixNet getL $root traffic]
	set traffic_items [ixNet getL $traffic trafficItem]
	set flag 1
	foreach item $traffic_items {
		set name [ixNet getAttribute $item -name]
		if {$name == $tItemName} {
			ixNet setMultiAttribute $item -enabled false
			ixNet commit
			set flag 0
	return $flag
		
		}
	}
}


puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.50
#ixNet connect 10.39.65.1 -port 9863 -version 8.50

puts "Creating a new config"
ixNet exec newConfig

# Load the Test Config
puts "Loading .ixncfg file ..."
set config_file "bonded_gre_sample_script.ixncfg"
ixNet exec loadConfig [ixNet readFrom $config_file ]

puts "Successfully loaded .ixncfg file !!!"

set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 [lindex $vPorts 0]
set vport2 [lindex $vPorts 1]
set root [ixNet getRoot]
puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

after 5000

puts "*****************************************************"
puts "Create  Home Gateway topology "
puts "*****************************************************"

puts "Adding Home Gateway topology"
set hg_topology [ixNet add $root "topology"]
ixNet setMultiAttribute $hg_topology 				\
	-name "Home Gateway" 							\
	-ports $vport1
ixNet commit

puts "\n .........Adding Bonded GRE LTE............ "

set lte_device [ixNet add $hg_topology "deviceGroup"]
ixNet setMultiAttribute $lte_device 				\
	-multiplier 1 									\
	-name "LTE Device Group"
ixNet commit

puts "\n Add Ethernet to LTE"
set ethernet1 [ixNet add $lte_device "ethernet"]
ixNet commit
set mac [ixNet getAttribute $ethernet1 -mac]
set mac_val [ixNet add $mac "counter"]
ixNet setMultiAttribute $mac_val 					\
	-step 00:00:00:00:00:01 						\
	-start 00:12:01:00:00:01 						\
	-direction increment
ixNet commit


puts "Add ipv4 to LTE device"
ixNet add $ethernet1 ipv4
ixNet commit

set ip1 [ixNet getList $ethernet1 ipv4]
set mvAdd1 [ixNet getAttr $ip1 -address]
set mvGw1  [ixNet getAttr $ip1 -gatewayIp]

puts "configuring ipv4 addresses for LTE device"
ixNet setAttr $mvAdd1/singleValue -value "1.1.1.1"
ixNet setAttr $mvGw1/singleValue  -value "1.1.1.101"
ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet commit

puts "\n Add GREoIPV4 in LTE device "
set greoipv4 [ixNet add $ip1 "greoipv4"]
ixNet setMultiAttribute $greoipv4 					\
	-stackedLayers [list ] 							\
	-name "GREoIPv4\ 2"
ixNet commit

puts "\n Add DHCPv4 Client in LTE device"
set dhcpv4client [ixNet add $greoipv4 "dhcpv4client"]
ixNet setMultiAttribute $dhcpv4client 				\
	-name "DHCPv4\ Client\ 1"
ixNet commit

set dhcpv4client_bgre [ixNet getL $greoipv4 dhcpv4client]
puts "\n Home Gateway DHCPv4 Client handle is : $dhcpv4client_bgre"

set bonded_gre_lte [ixNet add $greoipv4 "bondedGRE"]
ixNet setMultiAttribute $bonded_gre_lte 			\
	-name "LTE Bonded GRE"
ixNet commit
		
puts "\n .........Adding Bonded GRE DSL ............ "		

set dsl_device [ixNet add $hg_topology "deviceGroup"]
ixNet setMultiAttribute $dsl_device 				\
	-multiplier 1 									\
	-name "DSL Device Group"
ixNet commit

puts "\n Add Ethernet to DSL device group"
set ethernet2 [ixNet add $dsl_device "ethernet"]
ixNet commit
set mac [ixNet getAttribute $ethernet2 -mac]
set mac_val [ixNet add $mac "counter"]
ixNet setMultiAttribute $mac_val 					\
	-step 00:00:00:00:00:01 						\
	-start 00:14:01:00:00:01 						\
	-direction increment
ixNet commit

puts "Add ipv4 to DSL device group"
ixNet add $ethernet2 ipv4
ixNet commit

set ip2 [ixNet getList $ethernet2 ipv4]
set mvAdd2 [ixNet getAttr $ip2 -address]
set mvGw2  [ixNet getAttr $ip2 -gatewayIp]

puts "configuring ipv4 addresses for  DSL device group"
ixNet setAttr $mvAdd2/singleValue -value "1.1.1.2"
ixNet setAttr $mvGw2/singleValue  -value "1.1.1.101"
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

puts "\n Add GREoIPV4 for  DSL device group"
set greoipv4_dsl [ixNet add $ip2 "greoipv4"]
ixNet setMultiAttribute $greoipv4_dsl					 \
	-stackedLayers [list ] 								 \
	-name "GREoIPv4\ 2"
ixNet commit

set bonded_gre_dsl [ixNet add $greoipv4_dsl "bondedGRE"]
ixNet setMultiAttribute $bonded_gre_dsl 				\
	-name "DSL Bonded GRE"
ixNet commit
		
puts "\n Modify tunnel type of DSL device group to DSL value"
ixNet setMultiAttribute $bonded_gre_dsl \
	-tunnelType dsl \
	-stackedLayers [list ] \
	-name "DSL\ Bonded\ GRE"
ixNet commit


set haap_topo [lindex [ixNet getList $root topology] 0]
set deviceGroup_haap [lindex [ixNet getList $haap_topo deviceGroup] 0]
set ethernet_haap [lindex [ixNet getList $deviceGroup_haap ethernet] 0]
set ipv4_haap [lindex [ixNet getList $ethernet_haap ipv4] 0]
set greoipv4 [lindex [ixNet getList $ipv4_haap greoipv4] 0]
set dhcpip [lindex [ixNet getList $greoipv4 ipv4] 0]
set dhcpv4server [lindex [ixNet getList $dhcpip dhcpv4server] 0]

puts "\n HAAP DHCPv4 Server handle is : $dhcpv4server"
puts "\n HAAP DHCPv4 Server IP handle is : $dhcpip"
		
puts  "Get global templates"
set global_config 		[lindex [ixNet getList $root globals] 0]
set global_top 			[lindex [ixNet getList $global_config topology] 0]
set global_bgre 		[lindex [ixNet getList $global_top bondedGRE] 0]
set global_tlv_editor 	[lindex [ixNet getList $global_bgre tlvEditor] 0]
set global_template 	[lindex [ixNet getList [lindex [ixNet getList $global_tlv_editor defaults] 0] template] 0]

puts "***************************************************"
puts "			Add Link and custom TLV in LTE "
puts "***************************************************"

puts "1. Creating Link TLV"

set tlv_profile 					[ixNet getL $bonded_gre_lte tlvProfile]
set link_value			 			{[77] Link Type}
puts "Configure $link_value tlv"

# Get Link Type TLV from many default templates
set tlv_list 						[ixNet getFilteredList $global_template tlv -name $link_value]
ixNet commit

# Copy Link Type TLV template to tlv profile
set link_type_tlv		 			[ixNet -strip execute copyTlv $tlv_profile $tlv_list]
ixNet commit


puts "2. Creating custom TLV with Type , Length and Value"
set custom_tlv {[xx] Bonded GRE Custom TLV}

# Get Custom Type TLV from many default templates
set tlv_list 						[ixNet getFilteredList $global_template tlv -name $custom_tlv]
ixNet commit

# Copy Custom Type TLV template to tlv profile
set custom_type_tlv		 			[ixNet -strip execute copyTlv $tlv_profile $tlv_list]
ixNet commit
	

# Get Custom type field value
set tlv_val 			[ixNet getL $custom_type_tlv type]
# Get Custom type field object
set tlv_obj_val 		[ixNet getL $tlv_val object]
# Get Custom type field 
set obj_field_val 		[ixNet getL $tlv_obj_val field]
set obj_value 			[ixNet getA $obj_field_val -value]
set obj_counter 		[ixNet add $obj_value "counter"]

# Modify field value for Custom type
puts "\n\n Change the type for tlv name $custom_tlv to value 12 \n\n"
ixNet setMultiAttribute $obj_counter \
	-step 01 \
	-start 12 \
	-direction increment
ixNet commit
		
puts "Change the value for $custom_tlv to value aabbccdd"
# Get Custom value
set tlv_val 			[ixNet getL $custom_type_tlv value]
# Get Custom value object
set tlv_obj_val 		[ixNet getL $tlv_val object]
# Get Custom value field 
set obj_field_val 		[ixNet getL $tlv_obj_val field]
set obj_value 			[ixNet getA $obj_field_val -value]
set obj_counter 		[ixNet add $obj_value "counter"]

# Modify field value for Custom value
ixNet setMultiAttribute $obj_counter \
	-step 01 \
	-start aabbccdd \
	-direction increment
ixNet commit		

puts "********************************************************"
puts "		Starting protocols "
puts "********************************************************"
puts "\n\n 1. Starting LTE Bonded GRE protocols...\n\n"
ixNet exec start $bonded_gre_lte

puts "\n\n 2. Starting DSL Bonded GRE protocols...\n\n"
ixNet exec start $bonded_gre_dsl

puts "\n\n 3. Starting HAAP GRE...\n\n"
ixNet exec start $greoipv4 

puts "Wait 30 sec"
after 30000

# Apply and start traffic for lte_setup_accept
set traffic [ixNet getList $root traffic]
puts "Making LTE up by sending traffic for LTE setup Accept message"
set lte_setup_accept "LTE setup Accept - All attributes"
traffitem_enable_regenerate $lte_setup_accept
ixNet exec apply $traffic
ixNet exec start $traffic
after 5000

puts "Disable LTE traffic items"
traffitem_disable $lte_setup_accept

# Apply and start traffic for dsl_setup_accept
set dsl_setup_accept "DSL Setup Accept - All attributes"
traffitem_enable_regenerate $dsl_setup_accept
ixNet exec apply $traffic
ixNet exec start $traffic
after 5000

puts "Disable DSL setup accept traffic items"
traffitem_disable $dsl_setup_accept

puts "Check Stats after DSL and LTE comes up"
puts "Verifying all the stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Protocols Summary"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

puts "Verifying BondedGRE Per Port stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"BondedGRE Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "\n\n 4 . Starting HAAP dhcp server....\n\n"  
ixNet exec start $dhcpv4server

puts "\n\n 5 . Starting Home Gateway dhcp client....\n\n"
ixNet exec start $dhcpv4client_bgre

after 5000

puts "Creating Traffic from Home Gateway DHCP client to DHCP Server IPV4"
ixNet add [ixNet getRoot]/traffic trafficItem
ixNet commit
set ti1 [lindex [ixNet getList [ixNet getRoot]/traffic trafficItem] 4]
ixNet setMultiAttribute $ti1 -name  "LTE-DHCP-HG-HAAP"
ixNet commit

ixNet setAttribute $ti1 -trafficType ipv4
ixNet commit

ixNet add $ti1 endpointSet              \
        -sources             $dhcpv4client_bgre    \
        -destinations        $dhcpip    \
        -name                "ep-set1"  \
        -sourceFilter        {}         \
        -destinationFilter   {}
ixNet commit

ixNet setMultiAttribute $ti1/tracking -trackBy [list ethernetIiSourceaddress0 \
											    sourceDestEndpointPair0 	  \
												trackingenabled0 ipv4DestIp0  \
												ipv4SourceIp0 				  \
												ethernetIiDestinationaddress0]
ixNet commit

# Apply and start traffic from Home Gateway DHCP client to DHCP Server IPV4 
ixNet exec apply $traffic
ixNet exec start $traffic
after 5000

puts "Check  BondedGRE Traffic flow stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Flow Statistics"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}

ixNet exec stop $traffic
after 5000

set lte_traffic_home_gateway_haap "LTE-DHCP-HG-HAAP"
puts "Disable traffic from Home Gateway DHCP client to DHCP Server IPV4s"
traffitem_disable $lte_traffic_home_gateway_haap

puts "\n Applying and running traffic for active hello state"
set lte_active_hello "LTE - Notify-active_hello"
traffitem_enable_regenerate $lte_active_hello
ixNet exec apply $traffic
ixNet exec start $traffic
after 5000

puts "Disable traffic active hello"
traffitem_disable $lte_active_hello

puts "********************************************************"
puts "Send right click actions for Overflow lte, Stop Hello and resume hello"
puts "********************************************************"
#Similar command can be used for all right click actions like:
#Diag:Bonding tunnel start, Diag:DSL tunnel start, Diag:LTE tunnel Start, Diag: End Diagnostics
#Switch To DSL tunnel, DSL link failure, LTE link failure

puts "\n Sending Stop hello"
ixNet exec stophello $bonded_gre_lte 1
after 2000
set stop_hello_info [ixNet getAttr $bonded_gre_lte -bSessionInfo]
puts "Bonded GRE info after stop hello is : $stop_hello_info"

puts "\n Sending Resume hello"
ixNet exec resumehello $bonded_gre_lte 1
after 2000
set resume_hello_info [ixNet getAttr $bonded_gre_lte -bSessionInfo]
puts "Bonded GRE info after resume hello is : $resume_hello_info"

puts "\n Sending overflowLte"
ixNet exec overflowLte $bonded_gre_lte 1
after 2000
set overflow_lte [ixNet getAttr $bonded_gre_lte -homeGatewayInfo]
puts "Bonded GRE info after overdlow LTE is : $overflow_lte"


puts "Verifying BondedGRE Per Port stats for overflowLte \n"
set viewPage {::ixNet::OBJ-/statistics/view:"BondedGRE Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "********************************************************"
puts "Send LTE tear down traffic from HAAP to Homegateway"
puts "********************************************************"

puts "Enabling traffic for  LTE tear down with error code 01"
set lte_teardown_error "LTE-Teardowncode01"
traffitem_enable_regenerate $lte_teardown_error
ixNet exec apply $traffic

ixNet exec start $traffic
after 5000

# Get Bonded GRE session Info for tear down
set bgre_session_info [ixNet getAttr $bonded_gre_lte -bSessionInfo]
puts "Bonded GRE session Info for tear down is $bgre_session_info"

# Get Error Code for tear down
set error_code [ixNet getAttr $bonded_gre_lte -errorCode]
puts " \n Error Code for tear down is  : $error_code \n"

puts "\n\n Stop LTE Bonded GRE protocols and start again...\n\n"
ixNet exec stop $bonded_gre_lte
puts "Wait 5 sec"
after 5000

ixNet exec start $bonded_gre_lte
puts "Wait 5 sec"
after 5000

puts "Making LTE up by sending traffic for LTE setup Accept message"
set lte_setup_accept "LTE setup Accept - All attributes"
traffitem_enable_regenerate $lte_setup_accept
ixNet exec apply $traffic
ixNet exec start $traffic
after 5000

puts "********************************************************"
puts "Send LTE tear down traffic from Homegateway to HAAP"
puts "********************************************************"
ixNet exec teardown $bonded_gre_lte 11 1
after 2000
set teardown_info [ixNet getAttr $bonded_gre_lte -bSessionInfo]
puts "Bonded GRE info after Tear down from Homegateway to HAAP is : $teardown_info"


puts "********************************************************"
puts "\n\nStopping Bonded GRE...\n\n"
puts "********************************************************"		  
ixNet exec stopAllProtocols
after 5000

puts "********************************************************"
puts "		Disable Link and custom TLV"
puts "********************************************************"

# Get TLV profile list
set tlv_profile_list [ixNet getL $bonded_gre_lte tlvProfile]

# Disable each tlv by making -isEnabled parameter False
foreach tlv $tlv_profile_list {
	ixNet setAttr $tlv -isEnabled false
	ixNet commit
}

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

return 0





