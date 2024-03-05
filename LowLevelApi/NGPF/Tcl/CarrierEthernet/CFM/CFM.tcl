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

#################################################################################
#                                                                               #
# Description:                                                                  #
#    This script intends to demonstrate how to use NGPF CFM TCL API.            #
#    About Topology:                                                            #
#      Hub & Spoke topology is configured on 2 Ixia Ports. Each Hub & Spoke     #
#    topology consists of one emulated CFM MP (hub) and 3 simulated CFM MPs     #
#    (spoke).                                                                   #
#    Script Flow:                                                               #
#       Step 1. Configuration of protocols.                                     #
#            i.   Adding CFM emulated MP(emulated device group.)                #
#            ii.  Adding CFM Simulated Topology behind Emulated Device Group.   #
#            iii. Configuring simulated topology type as Hub & Spoke using      #
#                 CFM Network Group Wizard.                                     #
#            iv.  Changing Simulated topology connector to CFM stack.           #
#            v.   Configuring MD level and MA parameters in Simulated topology  #
#                 using CFM Network Group wizard.                               #
#            vi.  Execute configMDLevels command after setting required MD level#
#                 parameters.                                                   #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Statistics display                                    #
#        Step 4. Learned Info display   (Continuity Check messages,             #
#                Loopback messages and Link Trace mesages)                      #
#        Step 5. On The Fly(OTF) change of protocol parameter.                  #
#                (OTF Stop CCM in emulated MP and Apply changes on the fly.)    #
#        Step 6. Again statistics display to see OTF changes took place         #
#        Step 7. Configuration L2-L3 Traffic                                    #
#        Step 8. Apply and Start of L2-L3 traffic                               #
#        Step 9. Display of L2-L3  traffic Stats                                #
#        Step 10.Stop of L2-L3 traffic                                          #
#        Step 11.Stop of all protocols                                          #
#                                                                               #
#################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.50.134
    set ixTclPort   8039
    set ports       {{10.39.43.154  3  9} { 10.39.43.154 3  10}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Disconnecting if any already connected"
ixNet disconnect $::ixia::ixTclServer

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 9.10\
    setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

#################################################################################
# Step 1> protocol configuration section
#################################################################################
puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

# Creating topology and device group
puts "Adding 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet add [ixNet getRoot] topology -vports $vportRx
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

puts "Adding 2 device groups"
ixNet add $topo1 deviceGroup
ixNet add $topo2 deviceGroup
ixNet commit

set t1deviceGroup [ixNet getList $topo1 deviceGroup]
set t2deviceGroup [ixNet getList $topo2 deviceGroup]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "CFM Topology 1"
ixNet setAttr $topo2  -name "CFM Topology 2"

set deviceGroup1 [lindex $t1deviceGroup 0]
set deviceGroup2 [lindex $t2deviceGroup 0]

ixNet setAttr $deviceGroup1 -name "Emulated MP 1"
ixNet setAttr $deviceGroup2 -name "Emulated MP 2"
ixNet commit
puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $deviceGroup1 -multiplier 1
ixNet setAttr $deviceGroup2 -multiplier 1
ixNet commit

#  Adding ethernet stack and configuring MAC
puts "Adding ethernet/mac endpoints"
ixNet add $deviceGroup1 ethernet
ixNet add $deviceGroup2 ethernet
ixNet commit

set ethernet1 [ixNet getList $deviceGroup1 ethernet]
set ethernet2 [ixNet getList $deviceGroup2 ethernet]

puts "Configuring the mac addresses"
ixNet setMultiAttr [ixNet getAttr $ethernet1 -mac]/counter\
        -direction  increment                        \
        -start      {22:22:22:22:22:22}              \
        -step       {00:00:00:00:01:00}

ixNet setAttr [ixNet getAttr $ethernet2 -mac]/singleValue\
        -value      {44:44:44:44:44:44}
ixNet commit

#  Adding CFM protocol stack and configuring it
puts "\n\nAdding CFM emulated MP over Ethernet stack\n"
ixNet add $ethernet1 cfmBridge
ixNet add $ethernet2 cfmBridge
ixNet commit

set cfmBridge1 [ixNet getList $ethernet1 cfmBridge]
set cfmBridge2 [ixNet getList $ethernet2 cfmBridge]
set cfmMp1 [ixNet getList $cfmBridge1 cfmMp]
set cfmMp2 [ixNet getList $cfmBridge2 cfmMp]

# Adding CFM Simulated Topology behind Emulated Device Group
puts "\n\nAdding CFM Simulated Topology\n"
set addNetworkGroup1 [ixNet add $deviceGroup1 networkGroup]
set addNetworkGroup2 [ixNet add $deviceGroup2 networkGroup]
ixNet commit

set remapId1 [lindex [ixNet remapIds $addNetworkGroup1] 0]
set addNetworkTopology1 [ixNet add $addNetworkGroup1 networkTopology]

set remapId2 [lindex [ixNet remapIds $addNetworkGroup2] 0]
set addNetworkTopology2 [ixNet add $addNetworkGroup2 networkTopology]

ixNet commit


# Configuring simulated topology type as Hub & Spoke using CFM Network Group Wizard
puts "\n\nConfiguring simulated topology type as Hub & Spoke using CFM Network Group Wizard\n"
set remapId1 [lindex [ixNet remapIds $addNetworkTopology1] 0]
set addHubnSpoke1 [ixNet add $addNetworkTopology1 "netTopologyHubNSpoke"]

set remapId2 [lindex [ixNet remapIds $addNetworkTopology2] 0]
set addHubnSpoke2 [ixNet add $addNetworkTopology2 "netTopologyHubNSpoke"]

ixNet setMultiAttr $addHubnSpoke1 -enableLevel2Spokes false -includeEntryPoint true
ixNet setMultiAttr $addHubnSpoke2 -enableLevel2Spokes false -includeEntryPoint true
ixNet commit

set networkGroup1 [ixNet getList $deviceGroup1 networkGroup]
ixNet setAttr $networkGroup1 -name "Simulated Topology 1"
set networkGroup2 [ixNet getList $deviceGroup2 networkGroup]
ixNet setAttr $networkGroup2 -name "Simulated Topology 2"

set networkTopology1 [ixNet getList $networkGroup1 networkTopology]
set simRouterBridge1 [ixNet getList $networkTopology1 simRouterBridge]
set networkTopology2 [ixNet getList $networkGroup2 networkTopology]
set simRouterBridge2 [ixNet getList $networkTopology2 simRouterBridge]

# Changing Simulated topology connector to CFM stack
puts "\n\nChanging Simulated topology connector to CFM stack\n"

set addconnector1 [ixNet add $simRouterBridge1  connector]
ixNet setMultiAttribute $addconnector1  -connectedTo $cfmBridge1
ixNet commit

set addconnector2 [ixNet add $simRouterBridge2  connector]
ixNet setMultiAttribute $addconnector2  -connectedTo $cfmBridge2
ixNet commit

# Configuring MD level and MA parameters from Simulated topology from CFM Network Group wizard
puts "\n\nConfiguring MD level and MA parameters for Simulated topology 1 using\
      CFM Network Group wizard\n"
set cfmSimulatedTopology1 [ixNet getList $networkTopology1 cfmSimulatedTopology]
set configMANames1 [ixNet getList $cfmSimulatedTopology1 configMANamesParams]
ixNet setMultiAttribute $configMANames1 -maName "MA-12"
ixNet commit
ixNet exec configMANames $configMANames1


set configMDLevels1 [ixNet getList $cfmSimulatedTopology1 configMDLevelsParams]
ixNet setMultiAttribute $configMDLevels1 -numMDLevels 2 -mdLevel1 "1"\
-mdNameFormat1 "mdNameFormatDomainNameBasedStr" -mdName1 "MD-1" -mdLevel2 "2"\
-mdNameFormat2 "mdNameFormatCharacterStr" -mdName2 "MD-2"

ixNet commit
ixNet execute configMDLevels $configMDLevels1


puts "\n\nConfiguring MD level and MA name parameters for Simulated topology\
      2 using CFM Network Group wizard\n"
set cfmSimulatedTopology2 [ixNet getList $networkTopology2 cfmSimulatedTopology]
set configMANames2 [ixNet getList $cfmSimulatedTopology2 configMANamesParams]
ixNet setMultiAttribute $configMANames2 -maName "MA-12"
ixNet commit
ixNet exec configMANames $configMANames2


set configMDLevels2 [ixNet getList $cfmSimulatedTopology2 configMDLevelsParams]
ixNet setMultiAttribute $configMDLevels2 -numMDLevels 2 -mdLevel1 "1"\
-mdNameFormat1 "mdNameFormatDomainNameBasedStr" -mdName1 "MD-1" -mdLevel2 "2"\
-mdNameFormat2 "mdNameFormatCharacterStr" -mdName2 "MD-2"

ixNet commit


# Execute configMDLevels command after setting required MD level parameters 
# (To created simultaed topology with paramters configured above)

ixNet execute configMDLevels $configMDLevels2

################################################################################
# Step 2> Start of protocol.
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up\n"
ixNet exec startAllProtocols
after 30000

################################################################################
# Step 3> Retrieve protocol statistics.
################################################################################
puts "Verifying Protocol Summary stats\n"
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
puts "************************************************************"

puts "Verifying CFM Per Port stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"CFM Per Port"/page}
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
puts "************************************************************"

###############################################################################
# Step 4> Retrieve protocol learned info
# Note: Blank columns in learned information are shown as '{ }' in output
###############################################################################
puts "Fetch CCM, Loopback  and Link Trace learned info... \n"

ixNet exec getCfmCcmLearnedInformation $cfmMp1 1 
after 1000
set linfo [ixNet getList $cfmBridge1 learnedInfo]
set columns [ixNet getAttribute $linfo -columns]
set values [ixNet getAttribute $linfo -values]
puts "CCM learned info"
puts "***************************************************"
puts $columns
foreach v $values {
    puts $v
}
puts "***************************************************"


ixNet exec getCfmLoopbackDbLearnedInformation $cfmMp1 1
after 1000
set linfo [lindex [ixNet getList $cfmBridge1 learnedInfo] 1]
set columns [ixNet getAttribute $linfo -columns]
set values [ixNet getAttribute $linfo -values]
puts "Loopback learned info"
puts "***************************************************"
puts $columns
foreach v $values {
    puts $v
}
puts "***************************************************"


ixNet exec getCfmLinkTraceDbLearnedInformation $cfmMp1 1
after 1000
set linfo [lindex [ixNet getList $cfmBridge1 learnedInfo] 2]
set columns [ixNet getAttribute $linfo -columns]
set values [ixNet getAttribute $linfo -values]
puts "Link Trace learned info"
puts "***************************************************"
puts $columns
foreach v $values {
        puts $v
}
puts "***************************************************"

################################################################################
# Step 5> OTF Stop CCM in emulated MP and Apply changes on the fly.
################################################################################
puts "OTF stop  CCM for root(emualated) MP in topology 2 from right-click action\n"
ixNet execute stopCcmEmulated $cfmMp2
puts "Wait for 10 seconds before checking stats ...\n"
after 10000

################################################################################
# Step 6> Retrieve protocol statistics after OTF Stopping CCM in emulated MP
################################################################################
puts "Verifying CFM Per Port stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"CFM Per Port"/page}
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
puts "************************************************************"

################################################################################
# Step 7> Configure L2-L3 traffic.
################################################################################
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1  \
    -name {Ethernet Traffic}          \
    -roundRobinPacketOrdering false    \
    -trafficType ethernetVlan
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $ethernet1]
set destination  [list $ethernet2]

ixNet setMultiAttribute $endpointSet1           \
        -name                  "EndpointSet-1"  \
        -multicastDestinations [list]           \
        -scalableSources       [list]           \
        -multicastReceivers    [list]           \
        -scalableDestinations  [list]           \
        -ngpfFilters           [list]           \
        -trafficGroups         [list]           \
        -sources               $source          \
        -destinations          $destination        
ixNet commit
set endpointSet1 [lindex [ixNet remapIds $endpointSet1] 0]
ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy        [list ethernetIiSourceaddress0 trackingenabled0 ethernetIiDestinationaddress0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]
ixNet commit

###############################################################################
# Step 8> Apply and start L2/L3 traffic.
###############################################################################
puts "applying traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000
puts "starting traffic"
ixNet exec start [ixNet getRoot]/traffic

puts "let traffic run for 120 second"
after 12000
###############################################################################
# Step 9> Retrieve L2/L3 traffic item statistics.
###############################################################################
puts "Verifying all the L2-L3 traffic stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Flow Statistics"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -34 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

#################################################################################
# Step 10> Stop L2/L3 traffic.
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

###############################################################################
# Step 11> Stop of protocol.
################################################################################
puts "Stopping protocols and waiting for 60 seconds for protocols to stop\n"
ixNet exec stopAllProtocols
after 60000

puts "!!! Test Script Ends !!!"
