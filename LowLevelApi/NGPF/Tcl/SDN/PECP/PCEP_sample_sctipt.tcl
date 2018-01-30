#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/10/2014 - Abhijit Dhar - created sample                                #
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
#    This script intends to demonstrate how to use NGPF PCEP API.              #
#      1. Configures a PCE on the topology1 and a PCC on topology2. The PCE    #
#         channel has one LSP with two ERO in it. The PCC has one "Expected    #
#         PCE initiated LSP" configured in it. The "Symbolic Path Name" of the #
#         LSP in the PCE channel is same as that of "Expected PCE initiated    #
#         LSP" in the PCC. Also source end of the PCE initiated LSP at the PCE #
#         end is matching with that of "Expected PCE Initiated LSP" at the     #
#         PCC end.                                                             #
#      2. Stats PCC and PCE.                                                   #
#      3. Verify statistics from "Protocols Summary" view                      #
#      4. Fetch PCC learned information                                        #
#      5. Configure L2/L3 traffic - source end is the topology2 (PCC) and      #
#         destinaton end is topology1                                          #
#      6. Apply and start L2/L3 traffic.                                       #
#      7. Verify L2/L3 traffic statistics.                                     #
#      8. Stop traffic.                                                        #
#      9. Change the MPLS Label value in ERO1 of LSP1 at the PCE end in        #
#         topology1.                                                           #      
#     10. Wait for a few seconds and verify learned info                       #
#     11. Apply L2/L3 traffic.                                                 #
#     12. Verify traffic L2/L3 statistics.                                     #
#     13. Stop traiic.                                                         #
#     14. Stop all protocols.                                                  # 
# Ixia Softwares:                                                              #
#    IxOS      8.00 EA                                                         #
#    IxNetwork 8.00 EA                                                         #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.216.108.113
    set ixTclPort   8027
    set ports       {{10.216.108.104 4 1} {10.216.108.104 4 2}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.00\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure PCEP as per the description     #
#    give above                                                                # 
################################################################################ 
puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

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

set t1devices [ixNet getList $topo1 deviceGroup]
set t2devices [ixNet getList $topo2 deviceGroup]

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]

puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $t1dev1 -multiplier 1
ixNet setAttr $t2dev1 -multiplier 1
ixNet commit

puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]
set mac2 [ixNet getList $t2dev1 ethernet]

puts "Configuring the mac addresses"
ixNet setAttr [ixNet getAttr $mac1 -mac]/singleValue\
      -value       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
      -value       {18:03:73:C7:6C:01}
ixNet commit

puts "Add ipv4"
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
ixNet setAttr $mvAdd1/singleValue -value "20.20.20.2"
ixNet setAttr $mvAdd2/singleValue -value "20.20.20.1"
ixNet setAttr $mvGw1/singleValue  -value "20.20.20.1"
ixNet setAttr $mvGw2/singleValue  -value "20.20.20.2"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

puts "Adding a PCE object on the Topology 1"
set pce [ixNet add $ip1 pce]
ixNet commit
set pce [lindex [ixNet remapIds $pce] 0]

puts "Adding a PCC group on the top of PCE"
set pccGroup [ixNet add $pce pccGroup]
ixNet commit
set pccGroup [lindex [ixNet remapIds $pccGroup] 0]

# Adding PCC
puts "Adding a PCC object on the Topology 2"
set pcc [ixNet add $ip2 pcc]
ixNet commit
set pcc [lindex [ixNet remapIds $pcc] 0]

# configured expectedInitiatedLspsForTraffic 
ixNet setAttr $pcc -expectedInitiatedLspsForTraffic 1
ixNet commit

# Set pcc group multiplier to 1
ixNet setAttr $pccGroup -multiplier 1
ixNet commit

# Set PCC group's  "PCC IPv4 Address" field  to 20.20.20.1
set pccIpv4AddressMv [ixNet getAttr $pccGroup -pccIpv4Address]
ixNet setAttr $pccIpv4AddressMv/singleValue -value "20.20.20.1"
ixNet commit

################################################################################
# Set  pceInitiateLspParameters                                                #
# 1. IP version                -- ipv4                                         #
# 2. IPv4 source endpoint      -- 2.0.0.1                                      #
# 3. IPv4 destination endpoint -- 3.0.0.1                                      #
################################################################################
set ipVerisionMv [ixNet getAttr $pccGroup/pceInitiateLspParameters\
    -ipVersion]
ixNet setAttr $ipVerisionMv/singleValue ipv4
ixNet commit

set Ipv4SrcEndpointsMv [ixNet getAttr $pccGroup/pceInitiateLspParameters\
    -srcEndPointIpv4] 
ixNet setAttr $Ipv4SrcEndpointsMv/singleValue -value 2.0.0.1

set Ipv4DestEndpointsMv [ixNet getAttr $pccGroup/pceInitiateLspParameters\
    -destEndPointIpv4]
ixNet setAttr $Ipv4DestEndpointsMv/singleValue -value 3.0.0.1
ixNet commit

# Set  pceInitiateLspParameters
# 1. Include srp
set Ipv4SrpEndpointsMv [ixNet getAttr $pccGroup/pceInitiateLspParameters\
    -includeSrp]
ixNet setAttr $Ipv4SrpEndpointsMv/singleValue -value True
ixNet commit

################################################################################
# Set  pceInitiateLspParameters                                                #
# a. Include srp                                                               #
# b. Include symbolic pathname TLV                                             #
# c. Symbolic path name                                                        #
################################################################################
set includeLspMv [ixNet getAttr $pccGroup/pceInitiateLspParameters\
    -includeLsp]
ixNet setAttr $includeLspMv/singleValue -value True

set includeSymbolicPathMv [ixNet getAttr $pccGroup/pceInitiateLspParameters\
    -includeSymbolicPathNameTlv]
ixNet setAttr $includeSymbolicPathMv/singleValue True    
    
set symbolicPathNameMv [ixNet getAttr $pccGroup/pceInitiateLspParameters\
    -symbolicPathName]
ixNet setAttr $symbolicPathNameMv/singleValue -value "IXIA_SAMPLE_LSP_1"
ixNet commit

# Add 2 EROs
ixNet setMultiAttribute $pccGroup/pceInitiateLspParameters \
    -numberOfEroSubObjects 2                               \
    -name  {Initiated LSP Parameters}
ixNet commit

################################################################################
# Set the properties of ERO1                                                   #
# a. Active                                                                    # 
# b. Sid Type                                                                  #
# c. MPLS Label                                                                #
# d. TC                                                                        #
# e. TTL                                                                       #
# f. NAI Type                                                                  #
################################################################################
set ero1ActiveMv [ixNet getAttribute\
    $pccGroup/pceInitiateLspParameters/pcepEroSubObjectsList:1\
    -active]
ixNet setAttr $ero1ActiveMv/singleValue -value True

set ero1SidTypeMv [ixNet getAttribute\
    $pccGroup/pceInitiateLspParameters/pcepEroSubObjectsList:1\
    -sidType]
ixNet setAttr $ero1SidTypeMv/singleValue -value mplslabel32bit

set ero1MplsLabelMv [ixNet getAttribute\
    $pccGroup/pceInitiateLspParameters/pcepEroSubObjectsList:1\
    -mplsLabel]
ixNet setAttr $ero1MplsLabelMv/singleValue -value 1111

set ero1TcMv [ixNet getAttribute\
    $pccGroup/pceInitiateLspParameters/pcepEroSubObjectsList:1\
    -tc]
ixNet setAttr $ero1TcMv/singleValue -value 1 

set ero1TtlMv [ixNet getAttribute\
    $pccGroup/pceInitiateLspParameters/pcepEroSubObjectsList:1\
    -ttl]
ixNet setAttr $ero1TtlMv/singleValue -value 125

set ero1NaiTypeMv [ixNet getAttribute\
    $pccGroup/pceInitiateLspParameters/pcepEroSubObjectsList:1\
    -naiType]
ixNet setAttr $ero1NaiTypeMv/singleValue -value notapplicable
ixNet commit

################################################################################
# Set the properties of ERO2                                                   #
# a. Active                                                                    #
# b. Sid Type                                                                  #
# c. MPLS Label                                                                #
# d. TC                                                                        #
# e. TTL                                                                       #
# f. NAI Type                                                                  #
################################################################################
set ero2ActiveMv [ixNet getAttribute\
    $pccGroup/pceInitiateLspParameters/pcepEroSubObjectsList:2\
    -active]
ixNet setAttr $ero2ActiveMv/singleValue -value True

set ero2SidTypeMv [ixNet getAttribute\
    $pccGroup/pceInitiateLspParameters/pcepEroSubObjectsList:2\
    -sidType]
ixNet setAttr $ero2SidTypeMv/singleValue -value mplslabel32bit

set ero2MplsLabelMv [ixNet getAttribute\
    $pccGroup/pceInitiateLspParameters/pcepEroSubObjectsList:2\
    -mplsLabel]
ixNet setAttr $ero2MplsLabelMv/singleValue -value 5555

set ero2TcMv [ixNet getAttribute\
    $pccGroup/pceInitiateLspParameters/pcepEroSubObjectsList:2\
    -tc]
ixNet setAttr $ero2TcMv/singleValue -value 0

set ero2TtlMv [ixNet getAttribute\
    $pccGroup/pceInitiateLspParameters/pcepEroSubObjectsList:2\
    -ttl]
ixNet setAttr $ero2TtlMv/singleValue -value 100

set ero2NaiTypeMv [ixNet getAttribute\
    $pccGroup/pceInitiateLspParameters/pcepEroSubObjectsList:2\
    -naiType]
ixNet setAttr $ero2NaiTypeMv/singleValue -value notapplicable
ixNet commit

# Set PCC's  "PCE IPv4 Address" field  to 20.20.20.20
set pceIpv4AddressMv [ixNet getAttr $pcc -pceIpv4Address]
ixNet setAttr $pceIpv4AddressMv/singleValue -value "20.20.20.2"
ixNet commit

# Add one expectedInitiatedLspList
ixNet setMultiAttribute $pcc/expectedInitiatedLspList \
    -maxExpectedSegmentCount  1                       \
    -name {Expected PCE Initiated LSP 1}
ixNet commit
################################################################################
# Add expected PCC's Expected Initiated LSP traffic end point                  #
# a. Active                                                                    #
# b. Source IP addresses                                                       #
# c. Symbolic path name                                                        #
################################################################################
set pccExpectedLspActiveMv [ixNet getAttribute $pcc/expectedInitiatedLspList\
    -active]
ixNet setAttr $pccExpectedLspActiveMv/singleValue -value True
ixNet commit

set pccExpectedSrcIpAddrMv [ixNet getAttribute $pcc/expectedInitiatedLspList\
    -sourceIpv4Address]
ixNet setAttr $pccExpectedSrcIpAddrMv/singleValue -value "2.0.0.1"
ixNet commit

set pccExpectedSymbolicPathMv [ixNet getAttribute $pcc/expectedInitiatedLspList\
    -symbolicPathName]
ixNet setAttr $pccExpectedSymbolicPathMv/singleValue -value "IXIA_SAMPLE_LSP_1"
ixNet commit
      
################################################################################
# 2. Start PCC and PCE and wait for 60 seconds                                 #
################################################################################
puts "Starting all protocols"
ixNet exec startAllProtocols
after 60000

puts "Checking statistics"
################################################################################
# 3. Retrieve protocol statistics.                                             #
################################################################################
puts "Fetching all Protocol Summary Stats\n"
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

################################################################################
# 4. Retrieve protocol learned info                                            #
################################################################################
set totalNumberOfPcc 1
for {set i 1} {$i <= $totalNumberOfPcc} {incr i} {
    ixNet exec getPccLearnedInfo $pcc $i
}
puts "[string repeat * 60]"
set learnedInfoList [ixNet getList $pcc learnedInfo]
foreach learnedInfo $learnedInfoList {
    set table [ixNet getList $learnedInfo table]
    foreach t $table {
        set colList [ixNet getAttr $t -columns]
        set rowList [ixNet getAttr $t -values]
        foreach valList $rowList {
            set ndx 0  
            foreach val $valList {
                set name  [lindex $colList $ndx]
                set value $val
                set displayString [format "%-30s:\t%s" $name $value]
                puts $displayString
                incr ndx
            }
            puts "[string repeat * 60]"
        }
    }
}

################################################################################
# 5. Configure L2-L3 traffic                                                   #
################################################################################
puts "Configuring L2-L3 Traffic Item"
ixNet setAttr [ixNet getRoot]/traffic -refreshLearnedInfoBeforeApply true
ixNet commit

set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {Traffic Item 1}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv4
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $pcc/expectedInitiatedLspList]
set destination  [list $topo1]

ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"\
    -multicastDestinations [list]\
    -scalableSources       [list]\
    -multicastReceivers    [list]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source\
    -destinations          $destination\    
ixNet commit

ixNet setMultiAttribute $trafficItem1/transmissionDistribution\
    -distributions [list mplsMplsLabelValue0]

ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy        [list trackingenabled0 mplsMplsLabelValue0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]

ixNet commit

###############################################################################
# 6. Apply and start L2/L3 traffic                                            #
###############################################################################
puts "applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

puts "Let traffic run for 1 minute"
after 60000

###############################################################################
# 7. Retrieve L2/L3 traffic item statistics                                   #
###############################################################################
puts "Verifying all the L2-L3 traffic stats\n"
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
puts "***************************************************"

################################################################################
# 8. Stop the L2/L3 traffic                                                    #
################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 9. Change MPLS label valie in the ERO1 of LSP1                               #
################################################################################
ixNet setAtt $ero1MplsLabelMv/singleValue -value 6666
ixNet commit
ixNet exec applyOnTheFly {/globals/topology}
after 5000 

################################################################################
# 10. Retrieve protocol learned info                                           #
################################################################################
set totalNumberOfPcc 1
for {set i 1} {$i <= $totalNumberOfPcc} {incr i} {
    ixNet exec getPccLearnedInfo $pcc $i
}
puts "[string repeat * 60]"
set learnedInfoList [ixNet getList $pcc learnedInfo]
foreach learnedInfo $learnedInfoList {
    set table [ixNet getList $learnedInfo table]
    foreach t $table {
        set colList [ixNet getAttr $t -columns]
        set rowList [ixNet getAttr $t -values]
        foreach valList $rowList {
            set ndx 0  
            foreach val $valList {
                set name  [lindex $colList $ndx]
                set value $val
                set displayString [format "%-30s:\t%s" $name $value]
                puts $displayString
                incr ndx
            }
            puts "[string repeat * 60]"
        }
    }
}

###############################################################################
# 11. Apply and start L2/L3 traffic                                           #
###############################################################################
puts "applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

puts "Let traffic run for 1 minute"
after 60000

###############################################################################
# 12. Retrieve L2/L3 traffic item statistics                                  #
###############################################################################
puts "Verifying all the L2-L3 traffic stats\n"
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
puts "***************************************************"

################################################################################
# 13. Change MPLS label valie in the ERO1 of LSP1                              #
################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 14. Stop all protocols                                                       #
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"

