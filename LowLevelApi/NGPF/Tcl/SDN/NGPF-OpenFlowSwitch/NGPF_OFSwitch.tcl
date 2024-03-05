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

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF OF Switch API          #
#    It will create one OF Switch topology , it will start the emulation       #       
#    and then it will retrieve and display few statistics .                    #
#    It will send learned info trigger  for specified match crteria            #
################################################################################


################################################################################
#edit this variables values to match your setup#
################################################################################
namespace eval ::py {
    set ixTclServer 10.214.101.141
    set ixTclPort   8999
    set ports       {{12.0.1.253 5 1} { 12.0.1.253 5 2}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::py::ixTclServer -port $::py::ixTclPort -version 8.20\
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
::ixTclNet::AssignPorts $py::ports {} $vPorts force

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
ixNet setAttr $topo1  -name "OF Switch"
ixNet commit

set OFSwitch [ixNet add $ip1 openFlowSwitch]
ixNet commit

set topology [lindex [ixNet getList $root topology] 0]
set deviceGroup [lindex [ixNet getList $topology deviceGroup] 0]
set ethernet [lindex [ixNet getList $deviceGroup ethernet] 0]
set ipv4 [lindex [ixNet getList $ethernet ipv4] 0]
set openFlowSwitch1 [lindex [ixNet getList $ipv4 openFlowSwitch] 0]

puts "Set Number of OF Switch Channel to 1"
set NumChannels [ixNet getAttribute $openFlowSwitch1 -numberOfChannels]
ixNet setAttr $openFlowSwitch1 -numberOfChannels 1
ixNet commit
set openFlowChannel [ixNet getL $openFlowSwitch1 OFSwitchChannel ]
puts "Set Number of auxilary Channel to 1" 
set NumAuxChannel [ixNet getA $openFlowChannel -auxConnectionsPerChannel]
ixNet setAttr $openFlowChannel -auxConnectionsPerChannel 1
ixNet commit
set OfSwitchAuxChannel [ixNet getL $openFlowChannel auxiliaryConnectionList]
puts "Set auxilary Channel Connection Type to UDP" 
set mvAux [ixNet getA $OfSwitchAuxChannel -connectionType]
ixNet setAttr $mvAux/singleValue -value udp
ixNet commit
set OfSwitchAuxConnectionType [ixNet getA $mvAux -values]

puts "Set auxilary Channel ID to 1" 
set mvAuxID [ixNet getA $OfSwitchAuxChannel -auxId ]
ixNet setAttr $mvAuxID/singleValue -value 1
ixNet commit
set OfSwitchAuxId [ixNet getA $mvAuxID -values]

puts "Set auxilary Channel UDP port Number to 6000" 
set mvUdp [ixNet getA $OfSwitchAuxChannel -uDPSrcPortNum]
ixNet setAttr $mvUdp/singleValue -value 6000
ixNet commit
set OfSwitchAuxUdpPortNum [ixNet getA $mvUdp -values]
puts "Set Number of OF Switch Table"
ixNet setAttr $openFlowSwitch1 -numberOfTableRanges 1
ixNet commit
set NumSwTable [ixNet getAttribute $openFlowSwitch1 -numberOfTableRanges]

puts "Set Number of OF Switch Table ID"
ixNet setAttr $openFlowSwitch1 -numberOfTableRanges 1
ixNet commit
set swTableList [ixNet getL $openFlowSwitch1 switchTablesList]
set mvSwTableList [ixNet getA $swTableList -tableId]
ixNet setA $mvSwTableList/singleValue -value 50
ixNet commit
set swTableId [ixNet getA $mvSwTableList -values]

################################################################################
#Setting FlowState Table mod in switch
################################################################################
set oFSwitchLearnedInfoConfig [ixNet add $openFlowSwitch1 oFSwitchLearnedInfoConfig]
puts "set Table ID Custom for Switch Flow Learned Info "
ixNet setA $oFSwitchLearnedInfoConfig -flowStatTableIdMode tableIdCustom
ixNet commit
set flowStatTableIdMode [ixNet getA $oFSwitchLearnedInfoConfig -flowStatTableIdMode]
     

################################################################################
# Start protocol and check statistics                                          #
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
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

puts "Verifying OpenFlow Switch per port stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"OF Switch Per Port"/page}
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
#######################################################################################
# On the fly section  Enabling and Disabling Switch , Switch Channel and Switch port #  
#######################################################################################

puts " Disable switch on the Fly"
set switchMv [ixNet getA $openFlowSwitch1 -active]
ixNet setA $switchMv/singleValue -value true
ixNet commit
set switchDisable [ixNet getA $switchMv -values]
puts " Enable switch on the Fly"
set switchMv [ixNet getA $openFlowSwitch1 -active]
ixNet setA $switchMv/singleValue -value false
ixNet commit
set switchEnable [ixNet getA $switchMv -values]
puts " Disable switch Channel on the Fly"
set OFSwitchChannel [ixNet getL $openFlowSwitch1 OFSwitchChannel]
set ofMultiValue [ixNet getAttr $OFSwitchChannel -active ]
ixNet setA $ofMultiValue/singleValue -value false
ixNet commit
set switchChannelDis [ixNet getA $ofMultiValue -values]
puts " Enable switch channel on the Fly"
set OFSwitchChannel [ixNet getL $openFlowSwitch1 OFSwitchChannel]
set ofMultiValue [ixNet getAttr $OFSwitchChannel -active ]
ixNet setA $ofMultiValue/singleValue -value true
ixNet commit
set switchChannelEn [ixNet getA $ofMultiValue -values]
puts " Disable switch port on the Fly"
set ofSwitchPorts [ixNet getL $openFlowSwitch1 ofSwitchPorts]
set ofMultiValue [ixNet getAttr $ofSwitchPorts -active ]
ixNet setA $ofMultiValue/singleValue -value false
ixNet commit
set switchPortDis [ixNet getA $ofMultiValue -values]
puts " Enable switch port on the Fly"
set ofSwitchPorts [ixNet getL $openFlowSwitch1 ofSwitchPorts]
set ofMultiValue [ixNet getAttr $ofSwitchPorts -active ]
ixNet setA $ofMultiValue/singleValue -value true
ixNet commit
set switchPortEn [ixNet getA $ofMultiValue -values]
puts "Apply the changes on the fly"
set globals [ixNet getRoot]/globals
set topology $globals/topology
ixNet exec applyOnTheFly $topology
puts "Change Mac address on the fly"
set OFSwitchChannel [ixNet getL $openFlowSwitch1 OFSwitchChannel]
set ofMultiValueMac [ixNet getA $ofSwitchPorts -etherAddr]
ixNet setA $ofMultiValueMac/singleValue -value 00:00:00:10:10:10
ixNet commit
set oFportMacAddress [ixNet getA $ofMultiValueMac -values] 
puts "Change Port number on the fly"
set OFSwitchChannel [ixNet getL $openFlowSwitch1 OFSwitchChannel]
set oFMvPortNumber [ixNet getA $ofSwitchPorts -portNumber]
ixNet setA $oFMvPortNumber /singleValue -value 5
ixNet commit
set oFportNumber [ixNet getA $oFMvPortNumber  -values] 


###############################################################################
# print Switch learned info                                                   #
###############################################################################
ixNet exec getOFChannelLearnedInfo $openFlowSwitch1 1
after 5000
puts "Getting Basic Switch Learned info!!!!!!!"
set learnedInfoList [ixNet getL $openFlowSwitch1 learnedInfo]
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
puts "Getting Detailed Switch Learned info!!!!!!!"
set learnedInfoList [ixNet getL $openFlowSwitch1 learnedInfo]
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

puts " "
puts "For more info please refer to the user manual or the built-in help"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1/ipv4:1/openFlowSwitch:1"
puts "[ixNet help ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1/ipv4:1/openFlowSwitch:1]"
puts " "
puts "[ixNet help [ixNet getRoot]/traffic]"
after 15000

puts "Stopping all protocols"
ixNet exec stopAllProtocols
puts "*********************************************************************END*************************************************************************"