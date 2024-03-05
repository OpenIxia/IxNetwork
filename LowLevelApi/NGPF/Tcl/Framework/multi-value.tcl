#!/bin/sh
# the next line restarts using tclsh \
exec tclsh "$0" "$@"

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
#    This script intends to demonstrate how to use the multivalue patterns for #
#    the next gen protocols                                                    #
# Module:                                                                      #
#    The sample was tested on 2 back-to-back XMVDC16 ports                     #
################################################################################

puts "Load ixNetwork Tcl API package"
package require IxTclNetwork

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.200.115.201                          ;# IP Address of the IxNetwork Tcl Server
    set ixTclPort   8018                                    ;# Port number of the IxNetwork Tcl Server
    set ports       {{10.200.113.3 2 1} {10.200.113.3 2 2}} ;# Chassis-Slot port details {{ChassisIP Slot Port}...}
}

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.0 –setAttribute strict

puts "Create a new config"
ixNet exec newConfig

puts "Add 2 vport"
ixNet add [ixNet getRoot] vport -name testVport1
ixNet add [ixNet getRoot] vport -name testVport2
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 [lindex $vPorts 0]
set vport2 [lindex $vPorts 1]


puts "Add 1 Topologies"
ixNet add [ixNet getRoot] topology -name testTpg
ixNet commit
set topology [ixNet getList [ixNet getRoot] topology] 


puts "Add 1 device groups with multipliers (number of sessions) as 10"
ixNet add $topology deviceGroup -name testDg -multiplier 10
ixNet commit
set dev [ixNet getList $topology deviceGroup]

puts "Add MAC"
ixNet add $dev ethernet -name testEth
ixNet commit
set mac [ixNet getList $dev ethernet]
puts "Enabled vlan"
ixNet setAttr $mac -vlanCount 1
ixNet setAttr $mac -useVlans true
ixNet setA [ixNet getA $mac -enableVlans]/singleValue -value True
ixNet commit

set vlan [ixNet getList $mac vlan]
set vlanId [ixNet getAttribute $vlan -vlanId]


#singleValue

set multiVal [ixNet add $vlanId "singleValue"]
ixNet setMultiAttribute $multiVal \
-value 100
ixNet commit

#counter

set multiVal [ixNet add $vlanId "counter"]
ixNet setMultiAttribute $multiVal \
	-step 1 \
	-start 1 \
	-direction increment
ixNet commit

#counter

set multiVal [ixNet add $vlanId "counter"]
ixNet setMultiAttribute $multiVal \
	-step 1 \
	-start 1 \
	-direction decrement
ixNet commit

set multiVal [ixNet add $vlanId "random"]
ixNet commit

#repeatableRandom

set multiVal [ixNet add $vlanId "repeatableRandom"]
ixNet setMultiAttribute $multiVal \
	-mask 4095 \
	-count 4000000 \
	-seed 1 \
	-fixed 0
ixNet commit

#customDistributed

set multiVal [ixNet add $vlanId "customDistributed"]
ixNet setMultiAttribute $multiVal \
	-mode perPort \
	-algorithm percentage \
	-values [list [list 1 50] [list 2 50]]
ixNet commit

#custom

set multiVal [ixNet add $vlanId "custom"]
ixNet setMultiAttribute $multiVal \
	-step 1 \
	-start 1
ixNet commit
set multiVal [lindex [ixNet remapIds $multiVal] 0]

set multiVal2 [ixNet add $multiVal "increment"]
ixNet setMultiAttribute $multiVal2 \
	-count 3 \
	-value 1
ixNet commit

#valueList

set multiVal [ixNet add $vlanId "valueList"]
ixNet setMultiAttribute $multiVal \
	-values [list 1 2 3 4 5 6 7 8 9 10]
ixNet commit

#CSV
#amusing the file is present at the desktop of the client with user 8028 and named scaleStack

set multiVal [ixNet add $vlanId "valueList"]
ixNet exec import $multiVal [ixNet readFrom {C:/Users/8028/Desktop/scaleStack.csv}] "csv" 2
ixNet commit

puts "Add IPv4"
ixNet add $mac ipv4 -name testip
ixNet commit
set ip [ixNet getList $mac ipv4]
set ipP1Items [ixNet getList $ip/port:1 item]
set ipP2Items [ixNet getList $ip/port:2 item]


puts "Add both vports to the topology"
ixNet setAttr $topology -vports "$vport1 $vport2"
ixNet commit

puts " "
puts "Setting multi values counter values for ipv4 addresses with increment direction"
set ip_mul [ixNet getAtt $ip -address]
ixNet  setMultiAttr $ip_mul/counter -start 22.1.1.1 -step 0.0.1.2 -direction increment
ixNet commit

foreach ipItems [list $ipP1Items $ipP2Items] {
    foreach item $ipItems {
        puts "IP Address of $item = [ixNet getAtt $item -address]"
    }
}

puts " "
puts "Setting multi values counter values for ipv4 addresses with nest value"
ixNet  setMultiAttr $ip_mul/counter -start 33.1.1.1 -step 0.0.1.2 -direction increment
ixNet  setMultiAttr $ip_mul/nest:1 -step 0.99.1.2 -enabled True
ixNet commit

foreach ipItems [list $ipP1Items $ipP2Items] {
    foreach item $ipItems {
        puts "IP Address of $item = [ixNet getAtt $item -address]"
    }
}

puts " "
puts "Setting multi values counter value for ipv4 addresses with decrement direction"
ixNet  setMultiAttr $ip_mul/counter -start 22.22.22.22 -step 0.0.1.2 -direction decrement
ixNet commit
foreach ipItems [list $ipP1Items $ipP2Items] {
    foreach item $ipItems {
        puts "IP Address of $item = [ixNet getAtt $item -address]"
    }
}

puts " "
puts "Setting multi values custom values for ipv4 and nest value"
ixNet setMultiAtt $ip_mul/custom -start 22.1.1.100 \
                                 -step 0.0.0.20 \
				 -incrementCount 3 \
				 -incrementValue 0.0.0.3
ixNet  setMultiAttr $ip_mul/nest:1 -step 0.0.1.50 -enabled True
ixNet commit
foreach ipItems [list $ipP1Items $ipP2Items] {
    foreach item $ipItems {
        puts "IP Address of $item = [ixNet getAtt $item -address]"
    }
}

puts " "
puts "Setting multivalue overlay pattern for ipv4"
puts "IP Address of 3rd Item before Overlay: [ixNet getAtt [lindex $ipP1Items 2] -address]"
ixNet add $ip_mul overlay -index 3 -value "100.2.5.7"
ixNet commit
puts "IP Address of 3rd Item after Overlay: [ixNet getAtt [lindex $ipP1Items 2] -address]"


#subset

set networkGroup [ixNet add $dev networkGroup]
set ipv4PrePool [ixNet add $networkGroup ipv4PrefixPools]
ixNet commit
set networkAddress [ixNet getA $ipv4PrePool -networkAddress]
set ipv4Address [ixNet getA $ip -address]
set multiVal [ixNet add $networkAddress "subset"]
ixNet setMultiAttribute $multiVal \
	-autoScale True \
	-count 1 \
	-offset 0 \
	-roundRobin "port" \
	-shift 0 \
	-source $ipv4Address \
	-step 1
ixNet commit



puts "TEST END"

puts ""
puts ""
puts "For more info please refer to the user manual or the built-in help"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/item"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/item]"
