#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2016 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    07/07/2016 - Sarabjeet Kaur - created sample                              #
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
#    This script intends to demonstrate how to use NGPF OF Controller API      #
#    It will create one OF Controller topology , it will start the emulation   #       
#    and then it will retrieve and display few statistics .                    #
#    It will send learned info trigger  for specified match crteria            #
# Ixia Software:                                                               #
#    IxOS      8.10 EA                                                         #
#    IxNetwork 8.10 EA                                                         #
#                                                                              #
################################################################################

################################################################################
#Procedure for Adding Match Criteria & Instruction Action Example : adding match# 
#criteria as IPv4, Ethernet #
################################################################################

proc enableMatchesInstructions { flowProfile requiredMatchCriteriaList requiredInstruction requiredAction } {
    set preDefinedTemplate [ixNet add ::ixNet::OBJ-/globals/topology/openFlowController/flowSetTemplate predefined ]
    set flowTemplates [ixNet add $preDefinedTemplate flowTemplate]
    ixNet commit
    after 2000
    set matchActionList [ixNet getList $flowTemplates matchAction]
    puts "matchActionList= $matchActionList " 
    foreach matchAction $matchActionList {
        if { [regexp {Blank Template} [ixNet getA $matchAction -name] ] } {
            ixNet exec addFromTemplate $flowProfile $matchAction
            ixNet commit
            after 2000
            break
        }
    }
    set flowProfileMatchAction   [ixNet getList $flowProfile matchAction]
    puts " flowProfileMatchAction = $flowProfileMatchAction "
    set flowProfilematchCriteria [ixNet getList $flowProfileMatchAction matchCriteria]
    puts " flowProfilematchCriteria = $flowProfilematchCriteria "
    set matchCriteriaList        [ixNet getList $flowProfilematchCriteria matchCriteria]
    puts " matchCriteriaList = $matchCriteriaList "
    foreach requiredMatchCriteria $requiredMatchCriteriaList {
        foreach matchCriteria $matchCriteriaList {
            if { [string match $requiredMatchCriteria [ixNet getA $matchCriteria -name] ] } {
                ixNet setA $matchCriteria -isEnabled true
                ixNet commit
                after 2000
                if { [string match "Ethernet" [ixNet getA $matchCriteria -name] ] } {
                    puts "Enabling Ethernet match Criteria !!!"
                    set ethernetmatchCriteria [ixNet getList $matchCriteria matchCriteria]
                    foreach ethernetValue $ethernetmatchCriteria {
                        if {[string match "Ethernet Source" [ixNet getA $ethernetValue -name] ]} {
                           ixNet setAttr $ethernetValue -isEnabled true
                           ixNet commit
                           set EthernetFields [ixNet getList $ethernetValue field]
                           set value [lindex $EthernetFields 0]
                           set valueMulti [ixNet getAttr $value -value]
                           set EthernetCounterVal [ixNet add $valueMulti "singleValue"]
                           ixNet setMultiAttribute $EthernetCounterVal -value "11:0:0:0:0:0"
                           ixNet commit
                           set mask [lindex $EthernetFields 1]
                           set maskMulti [ixNet getAttr $mask -value]
                           set EthernetMaskVal [ixNet add $maskMulti "singleValue"]                        
                           ixNet setMultiAttribute $EthernetMaskVal -value "ff:ff:ff:ff:ff:fe"
                           ixNet commit
                        } else {
                           ixNet setAttr $ethernetValue -isEnabled true
                           ixNet commit
                           set EthernetDestFields [ixNet getList $ethernetValue field]
                           set value [lindex $EthernetDestFields 0]
                           set valueMulti [ixNet getAttr $value -value]
                           set EthernetCounterVal [ixNet add $valueMulti "singleValue"]
                           ixNet setMultiAttribute $EthernetCounterVal -value "12:0:0:0:0:0"
                           ixNet commit
                           set mask [lindex $EthernetDestFields 1]
                           set maskMulti [ixNet getAttr $mask -value]
                           set EthernetMaskVal [ixNet add $maskMulti "singleValue"]                        
                           ixNet setMultiAttribute $EthernetMaskVal -value "ff:ff:ff:ff:ff:ff"
                           ixNet commit                                                                                        
                        }
                        
                    }
                }
                if { [string match $requiredMatchCriteria [ixNet getA $matchCriteria -name] ] } {
                ixNet setA $matchCriteria -isEnabled true
                ixNet commit
                after 2000
                if { [string match "IP" [ixNet getA $matchCriteria -name] ] } {
                    puts "Enabling IP match Criteria !!!"
                    set IPmatchCriteria [ixNet getList $matchCriteria matchCriteria]
                    set Ipv4matchCriteria [lindex $IPmatchCriteria 0] 
                    set IPv4List [ixNet getL $Ipv4matchCriteria matchCriteria]
                    foreach Ipv4Value $IPv4List {
                        if {[string match "IPv4 Source" [ixNet getA $Ipv4Value -name] ]} {
                           ixNet setAttr $Ipv4Value -isEnabled true
                           ixNet commit
                           set IPv4Fields [ixNet getList $Ipv4Value field]
                           set value [lindex $IPv4Fields 0]
                           set valueMulti [ixNet getAttr $value -value]
                           set IPCounterVal [ixNet add $valueMulti "singleValue"]
                           ixNet setMultiAttribute $IPCounterVal -value "4.4.4.4"
                           ixNet commit
                           set mask [lindex $IPv4Fields 1]
                           set maskMulti [ixNet getAttr $mask -value]
                           set IPMaskVal [ixNet add $maskMulti "singleValue"]                        
                           ixNet setMultiAttribute $IPMaskVal -value "255.255.255.255"
                           ixNet commit
                        } else {
                           ixNet setAttr $Ipv4Value -isEnabled true
                           ixNet commit
                           set IPv4DestFields [ixNet getList $Ipv4Value field]
                           set value [lindex $IPv4DestFields 0]
                           set valueMulti [ixNet getAttr $value -value]
                           set Ipv4CounterVal [ixNet add $valueMulti "singleValue"]
                           ixNet setMultiAttribute $Ipv4CounterVal -value "7.7.7.7"
                           ixNet commit
                           set mask [lindex $IPv4DestFields 1]
                           set maskMulti [ixNet getAttr $mask -value]
                           set IPv4MaskVal [ixNet add $maskMulti "singleValue"]                        
                           ixNet setMultiAttribute $IPv4MaskVal -value "255.255.255.255"
                           ixNet commit                                                                                        
                        }
                        
                    }
                }
              set fieldList [ixNet getList $matchCriteria field]                
              foreach field $fieldList {
                  if { [string match "Ethernet Type" [ixNet getA $field -name] ] } {
                    puts "Enabling Eternet Type match Criteria !!!"
                    ixNet setA $field -isEnabled true
                    ixNet commit
                    set EtherTypeMultiVal [ixNet getAttr $field -value]
                    ixNet setAttr $EtherTypeMultiVal/singleValue -value 88E7
                    ixNet commit
                    }
             }             
             break
            }
        }
    }
    }
    set flowProfileMatchAction [ixNet getList $flowProfile matchAction]
    set flowProfileInstruction [ixNet getList $flowProfileMatchAction instructions]    
    puts " Adding instruction"    
    ixNet exec addInstruction $flowProfileInstruction $requiredInstruction
    ixNet commit
    after 3000
    set flowProfileInstructionAdded [ixNet getList $flowProfileInstruction instruction]
    puts $flowProfileInstructionAdded
    puts "adding 2 Action"
    puts $requiredAction
    foreach action $requiredAction {
                ixNet exec addAction $flowProfileInstructionAdded $action
                ixNet commit
                after 2000
        
    }
    after 5000 
    # adding value in actions
    set actionsAdded [ixNet getList $flowProfileInstructionAdded actions]
    set actions [lindex $actionsAdded 0]
    set actionList [ixNet getList $actions action]
    puts $actionList
 
    foreach action $actionList {
        if {[string match "Set Ethernet Source" [ixNet getA $action -name] ]} {
             puts "action is Set Ethernet Source"
            set val "4:6:0:0:0:0"
        } else {
             puts "action is Set Ethernet Destination"
             set val "7:7:4:8:1:7"
        } 
        set field [ixNet getList $action field ]
        set actionValue [ixNet getAttr $field -value]
        ixNet setAttr $actionValue/singleValue -value $val
        ixNet commit
        after 2000
    }

}

################################################################################
#edit this variables values to match your setup#
################################################################################

namespace eval ::ixia {
    set ixTclServer 10.214.101.141
    set ixTclPort   8009
    set ports       {{12.0.1.253 5 9} { 12.0.1.253 5 10}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.10\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# protocol configuration section                                               #
################################################################################ 
puts "Adding 1 vports"
ixNet add [ixNet getRoot] vport
ixNet commit
set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

puts "Adding topology"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet commit
set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
puts "Adding a device group"
ixNet add $topo1 deviceGroup
ixNet commit
set t1devices [ixNet getList $topo1 deviceGroup]
set t1dev1 [lindex $t1devices 0]

puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $t1dev1 -multiplier 1
ixNet commit

puts "Adding ethernet"
set ethernet [ixNet add $t1dev1 ethernet]
ixNet commit

puts "Add ipv4"
ixNet add $ethernet ipv4
ixNet commit

set ip1 [ixNet getList $ethernet ipv4]
set mvAdd1 [ixNet getAttr $ip1 -address]
set mvGw1  [ixNet getAttr $ip1 -gatewayIp]

puts "configuring ipv4 addresses"
ixNet setAttr $mvAdd1/singleValue -value "1.1.1.2"
ixNet setAttr $mvGw1/singleValue  -value "1.1.1.1"
ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet commit

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "OF Controller"
ixNet commit

set OFController [ixNet add $ip1 openFlowController]
ixNet commit

set topology [lindex [ixNet getList $root topology] 0]
set deviceGroup [lindex [ixNet getList $topology deviceGroup] 0]
set ethernet [lindex [ixNet getList $deviceGroup ethernet] 0]
set ipv4 [lindex [ixNet getList $ethernet ipv4] 0]
set openFlowController1 [lindex [ixNet getList $ipv4 openFlowController] 0]

puts "Set Number of OF Controller Channel to 1"
set NumChannels [ixNet getAttribute $openFlowController1 -numberOfChannels]
ixNet setAttr $openFlowController1 -numberOfChannels 1
ixNet commit
set openFlowChannel [ixNet getL $openFlowController1 openFlowChannel]
puts "Set Number of Group Per Channel to 1"        
set groupNum [ixNet getAttribute $openFlowChannel -groupsPerChannel]
ixNet setMultiAttribute $openFlowChannel -groupsPerChannel 1
ixNet commit

puts "Set Number of Meters Per Channel to 1"     
set meterNum [ixNet getAttribute $openFlowChannel -metersPerChannel]
ixNet setMultiAttribute $openFlowChannel -metersPerChannel 1
ixNet commit      

puts "Set Number of FlowSet Per Channel to 1"
set table [ixNet getL $openFlowChannel tables]
ixNet getAttr $table -numberOfFlowSet
ixNet setMultiAttribute $table -numberOfFlowSet 1
ixNet commit  

puts "Set Number of Flows Per Channel to 1"
set flowSet [ixNet getL $table flowSet]
set numFlows [ixNet getAttr $flowSet -numberOfFlows]
set numFlowsValue [ixNet setMultiAttribute $flowSet -numberOfFlows 1]
ixNet commit


################################################################################
#adding match criteria and instruction actions from Proc named enableMatchesInstructions#
################################################################################

set flowProfile [ixNet getL $flowSet flowProfile]
set requiredMatchCriteriaList {"Ethernet" "IP"}
set requiredInstruction {"Apply Actions"}
set requiredAction {"Set Ethernet Source" "Set Ethernet Destination"}
enableMatchesInstructions $flowProfile $requiredMatchCriteriaList $requiredInstruction $requiredAction

################################################################################
# Start protocol and check statistics                                          #
################################################################################
puts "Starting protocols and waiting for 45 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000
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

puts "Verifying OpenFlow Controller per port stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"OpenFlow Controller Per Port"/page}
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
# On the fly section  (Changing Instruction Action for Set Ethernet Source field)                                                         #  
################################################################################
set flowProfileMatchAction [ixNet getList $flowProfile matchAction]
set flowProfileInstruction [ixNet getList $flowProfileMatchAction instructions]    
set flowProfileInstructionAdded [ixNet getList $flowProfileInstruction instruction]
set First_action [lindex $flowProfileInstructionAdded 0]
set actionsAdded [ixNet getList $First_action actions]
set actionList [ixNet getList $actionsAdded action]
set setEthernetSourceaction [lindex $actionList 0]
if {[string match "Set Ethernet Source" [ixNet getA $setEthernetSourceaction -name] ]} {
       puts "Modifying Set Ethernet Source  Value OTF to 76:44:33:2:1:1"
       set val 76:44:33:2:1:1
}
set Ethernetfield [ixNet getList $setEthernetSourceaction field ]
set actionValue [ixNet getAttr $Ethernetfield -value]
ixNet setAttr $actionValue/singleValue -value $val
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
ixNet exec applyOnTheFly $topology

###############################################################################
# print learned info                                                          #
###############################################################################
ixNet exec getOFChannelLearnedInfo $openFlowController1 1
after 5000
puts "Getting Basic Controller Learned info!!!!!!!"
set learnedInfoList [ixNet getL $openFlowController1 learnedInfo]
set learnedInfo [lindex $learnedInfoList end]
set table [lindex [ixNet getList $learnedInfo table] 0]
set learnedInfoColumnsList [ixNet getAttr $table -columns]
set learnedInfoValuesList [ixNet getAttr $table -values]
set row2 [lindex $learnedInfoValuesList 1]

puts "***************************************************"
foreach v $learnedInfoColumnsList {
    puts $v
}
puts "***************************************************"

puts "***************************************************"
foreach v $row2 {
    puts $v
}
puts "***************************************************"
puts "Getting Detailed Controller Learned info!!!!!!!"
set learnedInfoList [ixNet getL $openFlowController1 learnedInfo]
set learnedInfo1 [lindex $learnedInfoList 0]
set table1 [lindex [ixNet getList $learnedInfo1 table] 0]
set learnedInfoColumnsList [ixNet getAttr $table1 -columns]
set learnedInfoValuesList [ixNet getAttr $table1 -values]
set row2 [lindex $learnedInfoValuesList 0]

puts "***************************************************"
foreach v $learnedInfoColumnsList {
    puts $v
}
puts "***************************************************"

puts "***************************************************"
foreach v $row2 {
    puts $v
}
puts "***************************************************"

puts "Set on demand message for flow stat!!!!"
set OfChanneLearnedinfoList [ixNet getL $openFlowController1 ofChannelLearnedInfoList]
set OnDemandMessage [ixNet getAttr $OfChanneLearnedinfoList -onDemandMessages]
set values1 [ixNet getAttr $OnDemandMessage -values]
ixNet setAttribute $OnDemandMessage/singleValue -value flowstat
puts "sending on demand message on the fly for flow stat learned info"
ixNet exec sendOnDemandMessage $OfChanneLearnedinfoList 1


puts " "
puts "For more info please refer to the user manual or the built-in help"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1/ipv4:1/openFlowController:1"
puts "[ixNet help ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1/ipv4:1/openFlowController:1]"
puts " "
puts "[ixNet help [ixNet getRoot]/traffic]"
after 15000

puts "Stopping all protocols"
ixNet exec stopAllProtocols
puts "*********************************************************************END*************************************************************************"