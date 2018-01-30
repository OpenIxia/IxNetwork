#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            # 
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    10/05/2016 - Anit Ghosal - created sample                                 #
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
#    This script intends to demonstrate how to use NGPF ISIS Link Protection-  #
#    SRLG - TCL API                                                            #
#                                                                              #
#    1. It will create 2 ISIS topologies, topology1 will have a simulated      #
#       topology Linear behind Device Group1 and Mesh behind Device Group2     #
#    2. Enable Shared Risk Link Group(SRLG) in ISIS Emulated                   #
#       Router in both Device Group.                                           # 
#    3. Give SRLG count 2 with value 5 and 6 for ISIS Emulated router          #
#       Router in both Device Group.                                           #
#    4. Give SRLG count 1 with value 10 for all ISIS simulated routers         #
#       Router behind Device Group1 & with value 15 for all ISIS simulated     #
#       routers Router behind Device Group2 .                                  #
#    5. Enable Link Protection in ISIS Emulated Router in both Device Group    #
#    6. Give Link Protection type Of Extra traffic,Unprotected and Dedicated   # 
#       :true for emulated Router in both device group.                        #
#    7. Give Link Protection type Of Dedicated 1:1 and shared:true for all     #
#       simulated Router behind  both device group.                            #
#    8. Start protocol.                                                        #
#    9. Retrieve protocol statistics.                                          #
#    10. On the fly uncheck "Enable SRLG"  emulated router in Device group2 &  #
#        check  "Enable SRLG" for all simulated Routers behind device group1   #
#    11. On the fly do change on Link type i.e  make enhanced:true and         #
#       unprotected:false for emulated router in Device group1 & disable"Enable# 
#       Link Protection" for first 2 simulated Routers behind device group2    #
#                                                                              #
#    12. Stop all protocols.                                                   #
#                                                                              #
# Ixia Softwares:                                                              #
#    IxOS      8.01 EA                                                         #
#    IxNetwork 8.01 EA                                                         #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your set-up
namespace eval ::ixia {
    set ixTclServer 10.216.24.34
    set ixTclPort   8888
    set ports       {{10.216.108.99 10  5} { 10.216.108.99  10  6}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.01\
   -setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure ISIS as per the description
#  give above
################################################################################ 
# Adding Virtual ports
puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

# Adding topologies
puts "Adding 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet add [ixNet getRoot] topology -vports $vportRx
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

# Adding Device Groups
puts "Adding 2 device groups"
ixNet add $topo1 deviceGroup
ixNet add $topo2 deviceGroup
ixNet commit

set t1devices [ixNet getList $topo1 deviceGroup]
set t2devices [ixNet getList $topo2 deviceGroup]

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]

puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $t1dev1 -multiplier 1
ixNet setAttr $t2dev1 -multiplier 1
ixNet commit

# Adding Ethernet
puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]
set mac2 [ixNet getList $t2dev1 ethernet]

puts "Configuring the mac addresses"
ixNet setMultiAttr [ixNet getAttr $mac1 -mac]/counter\
        -direction  increment                        \
        -start      {18:03:73:C7:6C:B1}              \
        -step       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
        -value      {18:03:73:C7:6C:01}
ixNet commit


# Adding IPv4 Stack
puts "Add ipv4 over Ethernet stack"
ixNet add $mac1 ipv4
ixNet add $mac2 ipv4
ixNet commit

set ip1 [ixNet getList $mac1 ipv4]
set ip2 [ixNet getList $mac2 ipv4]

set mvAdd1 [ixNet getAttr $ip1 -address]
set mvAdd2 [ixNet getAttr $ip2 -address]
set mvGw1  [ixNet getAttr $ip1 -gatewayIp]
set mvGw2  [ixNet getAttr $ip2 -gatewayIp]

puts "Configuring ipv4 addresses"
ixNet setAttr $mvAdd1/singleValue -value "100.0.0.1"
ixNet setAttr $mvAdd2/singleValue -value "100.0.0.2"
ixNet setAttr $mvGw1/singleValue  -value "100.0.0.2"
ixNet setAttr $mvGw2/singleValue  -value "100.0.0.1"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit


puts "Add ipv6 over Ethernet stack"
ixNet add $mac1 ipv6
ixNet add $mac2 ipv6
ixNet commit

set ip3 [ixNet getList $mac1 ipv6]
set ip4 [ixNet getList $mac2 ipv6]

set mvAdd1 [ixNet getAttr $ip3 -address]
set mvAdd2 [ixNet getAttr $ip4 -address]
set mvGw1  [ixNet getAttr $ip3 -gatewayIp]
set mvGw2  [ixNet getAttr $ip4 -gatewayIp]

puts "Configuring ipv4 addresses"
ixNet setAttr $mvAdd1/singleValue -value "2000:0:0:1:0:0:0:2"
ixNet setAttr $mvAdd2/singleValue -value "2000:0:0:1:0:0:0:1"
ixNet setAttr $mvGw1/singleValue  -value "2000:0:0:1:0:0:0:1"
ixNet setAttr $mvGw2/singleValue  -value "2000:0:0:1:0:0:0:2"

ixNet setAttr [ixNet getAttr $ip3 -prefix]/singleValue -value 64
ixNet setAttr [ixNet getAttr $ip4 -prefix]/singleValue -value 64


# Adding ISIS over Ethernet stack
puts "Adding ISIS over Ethernet stacks"
ixNet add $mac1 isisL3
ixNet add $mac2 isisL3
ixNet commit

set isisL3_1 [ixNet getList $mac1 isisL3]
set isisL3_2 [ixNet getList $mac2 isisL3]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "ISIS Topology 1"
ixNet setAttr $topo2  -name "ISIS Topology 2"

ixNet setAttr $t1dev1 -name "ISIS Topology 1 Router"
ixNet setAttr $t2dev1 -name "ISIS Topology 2 Router"
ixNet commit

set isisL3Router1_1 [ixNet getList $t1dev1 isisL3Router]
set isisL3Router2_1 [ixNet getList $t2dev1 isisL3Router]

# Enable host name in ISIS routers
puts "Enabling Host name in Emulated ISIS Routers"
set isisL3Router1 [ixNet getList [ixNet getList $topo1 deviceGroup] isisL3Router]
set enableHostName1 [ixNet getAttr $isisL3Router1 -enableHostName]
ixNet setAttr $enableHostName1/singleValue -value True
ixNet commit
set configureHostName1 [ixNet getAttr $isisL3Router1 -hostName]
ixNet setAttr $configureHostName1/singleValue -value "isisL3Router1"
ixNet commit

set isisL3Router2 [ixNet getList [ixNet getList $topo2 deviceGroup] isisL3Router]
set enableHostName2 [ixNet getAttr $isisL3Router2 -enableHostName]
ixNet setAttr $enableHostName2/singleValue -value True
ixNet commit
set configureHostName2 [ixNet getAttr $isisL3Router2 -hostName]
ixNet setAttr $configureHostName2/singleValue -value "isisL3Router2"
ixNet commit

puts "Making the NetworkType to Point to Point in the first ISIS router in Device Group 1 "
set networkTypeMultiValue1 [ixNet getAttr $isisL3_1 -networkType]
ixNet setAttr $networkTypeMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue1/singleValue -value pointpoint

puts "Making the NetworkType to Point to Point in the Second ISIS router in Device Group 2"
set networkTypeMultiValue2 [ixNet getAttr $isisL3_2 -networkType]
ixNet setAttr $networkTypeMultiValue2 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue2/singleValue -value pointpoint

# Disable Discard Learned LSP
puts "Disabling the Discard Learned Info CheckBox"

set isisL3RouterDiscardLearnedLSP1 [ ixNet getAttr [ixNet getList [ixNet getList $topo1 deviceGroup] isisL3Router] -discardLSPs]
set isisL3RouterDiscardLearnedLSP2 [ ixNet getAttr [ixNet getList [ixNet getList $topo2 deviceGroup] isisL3Router] -discardLSPs]

ixNet setAttr $isisL3RouterDiscardLearnedLSP1 -pattern singleValue -clearOverlays False
ixNet setAttr $isisL3RouterDiscardLearnedLSP1/singleValue -value False
ixNet setAttr $isisL3RouterDiscardLearnedLSP2 -pattern singleValue -clearOverlays False
ixNet setAttr $isisL3RouterDiscardLearnedLSP2/singleValue -value False



set networkGoup1 [ ixNet add $t1devices networkGroup ]
ixNet commit
set networkTopology1 [ixNet add $networkGoup1  networkTopology  ]
ixNet commit
set lineartopo [ixNet add $networkTopology1 netTopologyLinear ]
ixNet commit

set networkGoup2 [ ixNet add $t2devices networkGroup ]
ixNet commit
set networkTopology2 [ixNet add $networkGoup2  networkTopology  ]
ixNet commit
set lineartopo2 [ixNet add $networkTopology2 netTopologyMesh ]
ixNet commit



ixNet setAttr $networkGoup1 -multiplier 3
ixNet commit

ixNet setAttr $networkGoup2 -multiplier 1
ixNet commit

ixNet setAttr $networkGoup1 -name "ISIS_Linear Topology 1 "
ixNet commit

ixNet setAttr $networkGoup2 -name "ISIS_Linear Topology 2"
ixNet commit


###############################################################################
# 2. Enable SRLG in Both emulated Router 
###############################################################################

puts "Enabling SRLG in emulated router in both device group "
puts "***************************************************"
set enablesrlg [ixNet getAttr $isisL3_1 -enableSRLG]
set s3 [ixNet add $enablesrlg singleValue]
ixNet setAttr $s3 -value True
ixNet commit

set enablesrlg1 [ixNet getAttr $isisL3_2 -enableSRLG]
set s31 [ixNet add $enablesrlg1 singleValue]
ixNet setAttr $s31 -value True
ixNet commit


##########################################################################################################
# 3. Give SRLG count to 2 and SRLG value to 5 and 6 for ISIS Emulated  Router in both Device Group      
##########################################################################################################       

puts "Setting SRLG count to 2 and SRLG Value to 5 and 6 in emulated router in both Device Group "
puts "***************************************************"

ixNet setAttr  $isisL3_1 -srlgCount 2
ixNet commit

set list [lindex [ixNet getList  $isisL3_1 srlgValueList] 0]
set multi [ixNet getAttr $list -srlgValue ]
set sss [ixNet add $multi singleValue ]
ixNet setAttr $sss -value  5
ixNet commit


set list1 [lindex [ixNet getList $isisL3_1 srlgValueList] 1]
set multi1 [ixNet getAttr $list1 -srlgValue ]
set sss1 [ixNet add $multi1 singleValue ]
ixNet setAttr $sss1 -value  6
ixNet commit

ixNet setAttr  $isisL3_2 -srlgCount 2
ixNet commit

set list2 [lindex [ixNet getList  $isisL3_2 srlgValueList] 0]
set multi2 [ixNet getAttr $list2 -srlgValue ]
set sss2 [ixNet add $multi2 singleValue ]
ixNet setAttr $sss2 -value  5
ixNet commit


set list14 [lindex [ixNet getList $isisL3_2 srlgValueList] 1]
set multi14 [ixNet getAttr $list14 -srlgValue ]
set sss1 [ixNet add $multi14 singleValue ]
ixNet setAttr $sss1 -value  6
ixNet commit

#############################################################################################
# 4.Setting SRLG Value for both Simulated router as described above
#############################################################################################

puts "Setting SRLG value to 10 for Simulated routers behind Device Group1 "
puts "**********************************************"

set s [lindex [ixNet getList $t1devices networkGroup ] 0 ]
set ntt [ixNet add $s networkTopology]
set sintr [ixNet add $ntt simInterface ]
set ps [ixNet add $sintr  isisL3PseudoInterface ]
ixNet commit

set e [ixNet getAttr $ps -enableSRLG ]
set single [ixNet add $e singleValue ]
ixNet setAttr $single -value true
ixNet commit

set list1 [lindex [ixNet getList $ps srlgValueList] 0]
set multi1 [ixNet getAttr $list1 -srlgValue ]
set sss1 [ixNet add $multi1 singleValue ]
ixNet setAttr $sss1 -value  10
ixNet commit

set e [ixNet getAttr $ps -enableSRLG ]
set single [ixNet add $e singleValue ]
ixNet setAttr $single -value false
ixNet commit

puts "Setting SRLG value to 15 for Simulated routers behind Device Group2 "
puts "**********************************************"

set s1 [lindex [ixNet getList $t2devices networkGroup ] 0 ]
set ntt1 [ixNet add $s1 networkTopology]
set sintr1 [ixNet add $ntt1 simInterface ]
set ps1 [ixNet add $sintr1  isisL3PseudoInterface ]
ixNet commit



set list11 [lindex [ixNet getList $ps1 srlgValueList] 0]
set multi11 [ixNet getAttr $list11 -srlgValue ]
set sss11 [ixNet add $multi11 singleValue ]
ixNet setAttr $sss11 -value  15
ixNet commit


#############################################################################################
# 5. Enable Link Protection in Emulated Router in Both Device Group
#############################################################################################

puts "Enable Link Protection For Device Group 2 Emulated Router1"
puts "***************************************************"

set enable  [ixNet getAttr $isisL3_1 -enableLinkProtection]
set s [ixNet add $enable singleValue]
ixNet setAttr $s -value True
ixNet commit



puts "Enable Link Protection For Device Group 2 Emulated Router1"
puts "**********************************************"

set enable1  [ixNet getAttr $isisL3_2 -enableLinkProtection]
set s11 [ixNet add $enable1 singleValue]
ixNet setAttr $s11 -value True
ixNet commit

##############################################################################################
# 6.Setting Link Protection type as Described above For Emulated Router
##############################################################################################


puts "Enable Extratraffic ----- unprotected ----- dedicatedoneplusone  For emulated Router1 "
puts "**********************************************"


set extratraffic [ixNet getAttr $isisL3_1 -extraTraffic ]
set s1 [ixNet add $extratraffic singleValue]
ixNet setAttr $s1 -value True
ixNet commit



set unprotected [ixNet getAttr $isisL3_1 -unprotected ]
set s2 [ixNet add $unprotected singleValue]
ixNet setAttr $s2 -value True
ixNet commit


set dedicated [ixNet getAttr $isisL3_1  -dedicatedOnePlusOne ]
set s6 [ixNet add $dedicated singleValue]
ixNet setAttr $s6 -value True
ixNet commit


puts "Enable Extratraffic ----- unprotected ----- dedicatedoneplusone  For emulated Router2"
puts "**********************************************"

set extratraffic1 [ixNet getAttr $isisL3_2 -extraTraffic ]
set s12 [ixNet add $extratraffic1 singleValue]
ixNet setAttr $s12 -value True
ixNet commit



set unprotected1 [ixNet getAttr $isisL3_2 -unprotected ]
set s21 [ixNet add $unprotected1 singleValue]
ixNet setAttr $s21 -value True
ixNet commit


set dedicated1 [ixNet getAttr $isisL3_2  -dedicatedOnePlusOne ]
set s61 [ixNet add $dedicated1 singleValue]
ixNet setAttr $s61 -value True
ixNet commit



################################################################################
# 7. Setting Link Protection Type For Simulated Router as Described above
################################################################################

puts "Enable Link Protection For Simulated Routers Behind Device Group1 "
puts "**********************************************"

#Enable some enable link protection on st router
set e [ixNet getAttr $ps  -enableLinkProtection ]
set op12 [ixNet add $e singleValue ]
ixNet setAttr $op12 -value True
ixNet commit

puts "Making DedicatedonePlusOne And Shared Link Protection Type to True  "
puts "**********************************************"

#Make true to DedicatedonePlusOne field
set dedicatedoneplusone [ixNet getAttr $ps -dedicatedOnePlusOne ]
set sin1 [ixNet add $dedicatedoneplusone singleValue]
ixNet setAttr $sin1 -value true
ixNet commit

#Make true to Shared field
set shared [ixNet getAttr $ps -shared ]
set sin12 [ixNet add $shared singleValue]
ixNet setAttr $sin12 -value true
ixNet commit


puts "Enable Link Protection For Simulated Routers Behind Device Group2 "
puts "**********************************************"

#Enable some enable link protection on st router
set e1 [ixNet getAttr $ps1  -enableLinkProtection ]
set op121 [ixNet add $e1 singleValue ]
ixNet setAttr $op121 -value True
ixNet commit

puts "Making DedicatedonePlusOne And Shared Link Protection Type to True  "
puts "**********************************************"

#Make true to DedicatedonePlusOne field
set dedicatedoneplusone1 [ixNet getAttr $ps1 -dedicatedOnePlusOne ]
set sin11 [ixNet add $dedicatedoneplusone1 singleValue]
ixNet setAttr $sin11 -value true
ixNet commit

#Make true to Shared field
set s [ixNet getAttr $ps1 -shared]
set sin1 [ixNet add $s singleValue]
ixNet setAttr $sin1 -value true
ixNet commit




################################################################################
# 8. Start ISIS protocol and wait for 60 seconds
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000


################################################################################
# 9. Retrieve protocol statistics.
################################################################################
puts "Fetching all Protocol Summary Stats\n"
puts "**********************************************"
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
puts "***************************************************\n"



################################################################################
# 10. Do OTF  on Enable SRLG
################################################################################
puts "Do OTF on Device Group2 Emulated router on SRLG to make Deactive "
puts "**********************************************"

set root [ixNet getRoot]
set topologies [ixNet getList $root topology]
set topology1 [lindex $topologies 0]
set topology2 [lindex $topologies 1]
set deviceGroup0 [lindex [ixNet getList $topology2 deviceGroup] 0]
set deviceGroup1 [lindex [ixNet getList $topology2 deviceGroup] 1]
set ethernet12 [lindex [ixNet getList $deviceGroup0 ethernet] 0]
set isisL312 [lindex [ixNet getList $ethernet12 isisL3] 0]
ixNet commit
#Disable Link protection
set en [ixNet getAttr $isisL312 -enableSRLG]
set over1 [ixNet add $en overlay ]
ixNet setAttr $over1 -index 1 -value false
ixNet commit

puts "Do OTF on  Simulated router back of Device Group1 on SRLG to make Active"
puts "**********************************************"

set e1 [ixNet getAttr $ps -enableSRLG ]
set single1 [ixNet add $e1 singleValue ]
ixNet setAttr $single1 -value true
ixNet commit


################################################################################
# 11. Do OTF on Enable Link Protection as Described above
################################################################################

puts "Do OTF on Link type to make unprotected false and enhanced true "
puts "**********************************************"
set root [ixNet getRoot]
set topologies [ixNet getList $root topology]
set topology1 [lindex $topologies 0]
set topology2 [lindex $topologies 1]
set deviceGroup0 [lindex [ixNet getList $topology1 deviceGroup] 0]
set deviceGroup1 [lindex [ixNet getList $topology1 deviceGroup] 1]
set ethernet12 [lindex [ixNet getList $deviceGroup0 ethernet] 0]
set isisL312 [lindex [ixNet getList $ethernet12 isisL3] 0]
ixNet commit

#Make False to unprotected field
set unprotected [ixNet getAttr $isisL312 -unprotected]
set sin1 [ixNet add $unprotected singleValue]
ixNet setAttr $sin1 -value False
ixNet commit

#Make True to Enhanced field
set enhanced [ixNet getAttr $isisL312 -enhanced]
set sin12 [ixNet add $enhanced singleValue]
ixNet setAttr $sin12 -value True
ixNet commit

puts "Disable Link Protection of first two Simulated Roter behind For Device Group2"
puts "***************************************************"
set e1 [ixNet getAttr $ps1  -enableLinkProtection ]
set op121 [ixNet add $e1 overlay]
ixNet setAttr $op121 index 1 -value false
ixNet commit

set en12 [ixNet getAttr $ps1  -enableLinkProtection ]
set ov12 [ixNet add $en12 overlay ]
ixNet setAttr $ov12 -index 2 -value false
ixNet commit



################################################################################
# 12. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"

