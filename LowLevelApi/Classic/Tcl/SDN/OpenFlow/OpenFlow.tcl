#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2012 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    06/24/2013 - XYZ - created sample                            #
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
#    This script will do the following:                                        #
#    1. Configure OpenFlow v1.3.1 session to DUT                               #
#    2. configure table 0 containing 2 flow ranges of 1 flow each.             #
#    3. flow configuration :                                                   #
#       Flow1 - match - in Port, src MAC, dst MAC, eth type, src IP, dst IP    #
#       Flow1 - instruction/action - apply, set dst mac, output                #
#       Flow2 - match - src MAC, eth type, mpls label                          #
#       Flow2 - instruction/action - apply, set mpls label, output             #
#    4. bring up openflow connection with DUT and check statistics             #
#    5. Send flow stat learned info trigger. Check learned info.               #
# Setup :                                                                      #
#    Ixia controller IP 4.1.1.1 connected to OpenFlow switch (DUT) IP 4.1.1.2  #
# Module:                                                                      #
#    The sample was tested on an XYZ module.                                   #
# Software:                                                                    #
#    OS        Linux Fedora Core 12 (32 bit)                                   #
#    IxOS      6.50 EA (6.50.950.4)                                            #
#    IxNetwork 7.11  EA (7.11.840.24)                                          #
#                                                                              #
################################################################################



package req IxTclNetwork

set client 10.205.28.12
set chassis 10.205.28.82
set card  2
set port_controller 5
set clientPort 8920

#-------------------------------------------------------------------------------
# PURPOSE : To define stats retrival operations.
# AUTHOR  : Sumeer Kumar
#-------------------------------------------------------------------------------

#------------------------------------------------------------------------------#
# NAMESPACE : statsOperation                                                   #
# PURPOSE   : performs stats retrival operations                               #
#------------------------------------------------------------------------------#
namespace eval statsOperation {
    variable snapShotData
    variable pageSize
    variable pageNum 
    #--------------------------------------------------------------------------#
    # PURPOSE    : to get the caption from the stat view object                #
    # ASSUMPTION : for internal use in this name space                         #
    #--------------------------------------------------------------------------#
    proc getCaption {statViewName} {
        return "\"[ixNet getAttr $statViewName -name]\""
    }

    #--------------------------------------------------------------------------#
    # PURPOSE    : set the page size of a given stat view                      #
    #--------------------------------------------------------------------------#
    proc pageSize {size} {
        variable pageSize
        set pageSize $size
    } 

    #--------------------------------------------------------------------------#
    # PURPOSE    : gett the given page from a given stat view                  #
    #--------------------------------------------------------------------------#
    proc pageNumber {page} {
        variable pageNum
        set pageNum page
    }

    #--------------------------------------------------------------------------#
    #  PURPOSE    : get desired stat values from raw snapshot data object      #
    #--------------------------------------------------------------------------#
    proc getStatFromSnapshotData {vport statName} {
        variable snapShotData
        if {[info exists snapShotData] == 0} {
             puts "Error in getting snapshot of stats for $statName"
             return -1
        }

        # parsing vport
        set chassisCardPortList [split [ixNet getAttr $vport -assignedTo] ":"]
        set chassis  [lindex $chassisCardPortList 0]
        set card Card[format "%0.2d" [lindex $chassisCardPortList 1]]
        set port Port[format "%0.2d" [lindex $chassisCardPortList 2]]
        set myCardPort "$chassis/$card/$port"
        
        set connectionList [lindex $snapShotData 1]
        set statNameList   [lindex $snapShotData 2]
        set statRowList    [lindex $snapShotData 3]
        set myStatRowIndex [lsearch $connectionList $myCardPort]
        if {$myStatRowIndex < 0} {
            puts "Error: Chassis/Card/Port in not in snapshot data"
            return 0
        }

        set myStatRow [lindex $statRowList $myStatRowIndex]
        set myStatName $statName
        set myStatIndex 0
        foreach statName $statNameList {
            if {$statName == $myStatName} {
                puts "Matching stat viewer found"
                break
            }
            incr myStatIndex
        }

        if {$myStatIndex == [llength $statNameList]} {
            puts "ERROR stat name $myStatName not in stat name list !"
            puts "---- Available stat name list are -----------------"
            foreach statN $statNameList {
                puts "$statN"
            }
            puts "---------------------------------------------------"
            return 0
        }

        set retval [lindex $myStatRow $myStatIndex]
        if {($retval == "") || ([string is space $retval] == 1)} {
           return 0
        }
        return $retval
    }

    #--------------------------------------------------------------------------#
    #  PURPOSE    : get tx/rx stat values from raw snapshot data object        #
    #--------------------------------------------------------------------------#
    proc getTrafficStatFromSnapshotData {trafficItem statName} {
        variable snapShotData
        if {[info exists snapShotData] == 0} {
             puts "Error in getting snapshot of stats for $statName" 
             return -1
        }

        set myCardPort $trafficItem

        # parsing snapShot data
        set connectionList [lindex $snapShotData 1]
        set statNameList   [lindex $snapShotData 2]
        set statRowList    [lindex $snapShotData 3]
        set myStatRowIndex [lsearch $connectionList $myCardPort]
        if {$myStatRowIndex < 0} {
            puts "Error:  myCardPort in not in snapshot data"
            return 0
        }

        set myStatRow [lindex $statRowList $myStatRowIndex]
        # puts "myStatRow == $myStatRow"
        set myStatName $statName
        set myStatIndex 0
        foreach statName $statNameList {
            if {$statName == $myStatName} {
                break
            }
            incr myStatIndex
        }

        if {$myStatIndex == [llength $statNameList]} {
            puts "ERROR stat name $myStatName not in stat name list !"
            return 0
        }

        set retval [lindex $myStatRow $myStatIndex]
        if {($retval == "") || ([string is space $retval] == 1)} {
           return 0
        }
        return $retval
    }

    #--------------------------------------------------------------------------#
    #  PURPOSE    : get raw snapshot data object from ixNetwork stat viewer    #
    #--------------------------------------------------------------------------#
    proc getSnapShotData {viewCaption} {
        variable snapShotData
        variable pageSize
        variable pageNum

        set statsViewList [ixNet getList [ixNet getRoot]/statistics\
            statViewBrowser]
        set indexOfStatView 0
        foreach statView $statsViewList {
           set statViewCaption [getCaption $statView]
       puts "stat view name = $statView statViewCaption = $statViewCaption\
                 viewCaptionPassed = $viewCaption"
           if {[string tolower $statViewCaption] ==\
               [string tolower $viewCaption]} {
               break
           }
           incr indexOfStatView
        }

        if {$indexOfStatView == [llength $statsViewList]} {
           puts "--------- Availabls stats views --------------"
           foreach statview $statsViewList {
                puts "[getCaption $statview]"
           }
           puts "----------------------------------------------" 
           return {}
        }

        set myStatView [lindex $statsViewList $indexOfStatView]
        if {[info exists pageSize] == 1} {
            catch {ixNet help $myStatView} msg
            puts $msg
            puts "ixNet setAttr $myStatView -pageSize $pageSize"
            ixNet setAttr $myStatView -pageSize $pageSize
            ixNet commit
        }

        if {[info exists pageNum] == 1} {
            ixNet setAttr $myStatView -currentPageNumber $pageNum
            ixNet commit
        } else {
            ixNet setAttr $myStatView -currentPageNumber 1
            ixNet commit
        }

        catch {ixNet help $myStatView} data
        set isError [catch {set snapShotData\
            [ixNet getAttr $myStatView -snapshotData]}]
        if {$isError} {
            puts "Error: $::errorInfo"
        }
    }

    #--------------------------------------------------------------------------#
    # PURPOSE : Print the content of the snapshot data                         #
    #           May be used for debugging                                      #
    #--------------------------------------------------------------------------#                    
    proc printSnapShotData {} {
        variable snapShotData
        if {[info exists snapShotData]} {
            puts $snapShotData
        }
    }

    #--------------------------------------------------------------------------#
    # Return the unparsed snapshot data for those who wants to used it for     #
    # their self-defined parsing                                               #
    #--------------------------------------------------------------------------#    
    proc returnRawSnapshotDataObj {} {
        variable snapShotData
        if {[info exists snapShotData]} {
            return $snapShotData
        } else {
            return ""
        }
    } 
}
namespace export statsOperation *

ixNet connect $client -version 7.11 -port $clientPort
ixNet exec newConfig
 
set root [ixNet getRoot]
ixNet commit
set root [lindex [ixNet remapIds $root] 0]

# add vport1
set vport1 [ixNet add $root vport]
ixNet setAttr $vport1 -name {Controller}
ixNet commit
set vport1 [lindex [ixNet remapIds $vport1] 0]


# add interface
set interface [ixNet add $vport1 "interface"]
ixNet setAttribute $interface -enabled true 
ixNet commit
set interface [lindex [ixNet remapIds $interface] 0]

# add ipv4
set ipv4 [ixNet add $interface "ipv4"]
ixNet setMultiAttribute $ipv4 \
            -ip 4.1.1.1 \
            -gateway 4.1.1.2
ixNet commit
set ipv4 [lindex [ixNet remapIds $ipv4] 0]

# enable openFlow
ixNet setMultiAttribute $vport1/protocols/openFlow \
            -enabled true
ixNet commit

# add device and enable version 1.3.1
set device [ixNet add $vport1/protocols/openFlow "device"]
ixNet setMultiAttribute $device \
            -enabled true \
            -enableVersion131 true \
            -enableVersion100 false
ixNet commit
set device [lindex [ixNet remapIds $device] 0]

# add openflow interface
set ofInterface [ixNet add $device "interface"]
ixNet setMultiAttribute $ofInterface \
            -enabled true \
            -protocolInterfaces $interface
ixNet commit
set ofInterface [lindex [ixNet remapIds $ofInterface] 0]

# add ofchannel
set ofChannel [ixNet add $ofInterface "ofChannel"]
ixNet setMultiAttribute $ofChannel \
            -enabled true \
            -remoteIp 4.1.1.2 
ixNet commit
set ofChannel [lindex [ixNet remapIds $ofChannel] 0]

# add controller table
set controllerTables [ixNet add $ofChannel "controllerTables"]
ixNet setAttribute $controllerTables -enabled true
ixNet commit
set controllerTables [lindex [ixNet remapIds $controllerTables] 0]

# add first controller table flow range
set controllerTableFlowRanges1 [ixNet add $controllerTables "controllerTableFlowRanges"]
ixNet setMultiAttribute $controllerTableFlowRanges1 \
            -inPort {startValue = 1,stepValue = 0,repeatCount = 1,wrapCount = 4294967295,incrementMode = increment} \
            -ethernetSource {startValue = 00:01:00:00:00:01,stepValue = 00:00:00:00:00:01,repeatCount = 1,wrapCount = 1000000,incrementMode = increment} \
            -ethernetSourceMask {FF FF FF FF FF FF} \
            -ethernetDestination {startValue = 00:02:00:00:00:01,stepValue = 00:00:00:00:00:01,repeatCount = 1,wrapCount = 1000000,incrementMode = increment} \
            -ethernetDestinationMask {FF FF FF FF FF FF} \
            -ethernetType {startValue = 800,stepValue = 0,repeatCount = 1,wrapCount = 65535,incrementMode = increment} \
            -ipv4Source {startValue = 1.1.1.1/0,stepValue = 0.0.0.1,repeatCount = 1,wrapCount = 1000000,incrementMode = increment} \
            -ipv4SourceMask {255.255.255.255} \
            -ipv4Destination {startValue = 2.1.1.1/0,stepValue = 0.0.0.1,repeatCount = 1,wrapCount = 1000000,incrementMode = increment} \
            -ipv4DestinationMask {255.255.255.255} \
            -enabled true
ixNet commit
set controllerTableFlowRanges1 [lindex [ixNet remapIds $controllerTableFlowRanges1] 0]

# add instructions
set instruction1 [ixNet add $controllerTableFlowRanges1 "instructions"]
ixNet setAttribute $instruction1 -instructionType applyActions 
ixNet commit
set instruction1 [lindex [ixNet remapIds $instruction1] 0]

# add first action 
set instructionAction11 [ixNet add $instruction1 "instructionActions"]
ixNet setMultiAttribute $instructionAction11 \
            -actionType setEthernetDestination \
            -ethernetDestination 00:04:00:00:00:01
ixNet commit
set instructionAction11 [lindex [ixNet remapIds $instructionAction11] 0]

# add second action
set instructionAction12 [ixNet add $instruction1 "instructionActions"]
ixNet setMultiAttribute $instructionAction12 \
            -actionType output \
            -outputPort 2 \
            -maxByteLength 65535
ixNet commit
set instructionAction12 [lindex [ixNet remapIds $instructionAction12] 0]

# add second controller table flow range
set controllerTableFlowRanges2 [ixNet add $controllerTables "controllerTableFlowRanges"]
ixNet setMultiAttribute $controllerTableFlowRanges2 \
            -inPort {startValue = 1,stepValue = 0,repeatCount = 1,wrapCount = 4294967295,incrementMode = increment} \
            -ethernetSource {startValue = 00:03:00:00:00:01,stepValue = 00:00:00:00:00:01,repeatCount = 1,wrapCount = 1000000,incrementMode = increment} \
            -ethernetSourceMask {FF FF FF FF FF FF} \
            -ethernetType {startValue = 8847,stepValue = 0,repeatCount = 1,wrapCount = 65535,incrementMode = increment} \
            -mplsLabel {startValue = 10,stepValue = 1,repeatCount = 1,wrapCount = 4294967295,incrementMode = increment} \
            -enabled true 
ixNet commit
set controllerTableFlowRanges2 [lindex [ixNet remapIds $controllerTableFlowRanges2] 0]

# add instructions
set instruction2 [ixNet add $controllerTableFlowRanges2 "instructions"]
ixNet setAttribute $instruction2 -instructionType applyActions
ixNet commit
set instruction2 [lindex [ixNet remapIds $instruction2] 0]

# add first action
set instructionAction21 [ixNet add $instruction2 "instructionActions"]
ixNet setMultiAttribute $instructionAction21 \
            -actionType setMplsLabel \
            -mplsLabel 20 
ixNet commit
set instructionAction21 [lindex [ixNet remapIds $instructionAction21] 0]

# add second action
set instructionAction22 [ixNet add $instruction2 "instructionActions"]
ixNet setMultiAttribute $instructionAction22 \
                        -actionType output \
                        -outputPort 2 \
                        -maxByteLength 65535
ixNet commit
set instructionAction22 [lindex [ixNet remapIds $instructionAction22] 0]


set realPortsList [list [list $chassis $card $port_controller]]
set vportList [ixNet getList $root vport]
 if {[catch {ixTclNet::AssignPorts $realPortsList {} $vportList force}]} {
    puts "Not able to assign real ports: $::errorInfo"
    return 1
}
after 5000

puts "starting protocol"
set of $vportList/protocols/openFlow
ixNet exec start $of
puts "wait 30 seconds"
after 30000

#--------------------------------------------------------------------------#
# Check statistics                                                         #
#--------------------------------------------------------------------------#
# 1. OF Channel Configured                                                 #
# 2. OF Channel Configured Up                                              #
# 3. OF Channel Learned Up                                                 #
# 4. Hellos Tx                                                             #
# 5. Hellos Rx                                                             # 
# 6. Echo Requests Tx                                                      #
# 7. Echo Replies Rx                                                       #
# 8. Echo Requests Rx                                                      #
# 9. Echo Replies Tx                                                       #
#10. Feature Requests Tx                                                   #
#11. Feature Replies Rx                                                    # 
#--------------------------------------------------------------------------#
set {statValArray(OF Channel Configured)}    [list "1" "=="]
set {statValArray(OF Channel Configured Up)} [list "1" "=="]
set {statValArray(OF Channel Learned Up)}    [list "0" "=="]
set {statValArray(Hellos Tx)}                [list "1" ">="]
set {statValArray(Hellos Rx)}                [list "1" ">="]
set {statValArray(Echo Requests Tx)}         [list "1" ">="]
set {statValArray(Echo Replies Rx)}          [list "1" ">="]
set {statValArray(Echo Requests Rx)}         [list "0" ">="]
set {statValArray(Echo Replies Tx)}          [list "0" ">="]
set {statValArray(Feature Requests Tx)}      [list "1" "=="]
set {statValArray(Feature Replies Rx)}       [list "1" "=="]
set {statValArray(Flow Adds Tx)}             [list "2" "=="]
    
puts "checking statistics"
statsOperation::getSnapShotData {"OpenFlow Controller Aggregated Statistics"}
foreach stat [array names statValArray] {
    puts "retriving stats for $stat"
    set value [lindex $statValArray($stat) 0]
    set comparisonLogic [lindex $statValArray($stat) 1]
    set valObtained [statsOperation::getStatFromSnapshotData $vport1 $stat]
    puts "$stat:valueObtained == $valObtained"
    puts "$stat:valueExpected == $value"
    puts "comparing valueObtained $comparisonLogic valueExpected"

    if "$valObtained $comparisonLogic $value" {
        continue
    } else {
        puts "Stats not proper"
    }
}
unset statValArray
#--------------------------------------------------------------------------#

# Sending Flow stat trigger
puts "Sending trigger for flow stat"
set learnedInfo [ixNet getList $of learnedInformation]
ixNet exec refreshLearnedInformation $learnedInfo
after 10000

ixNet exec clearRecordsForTrigger $learnedInfo
set ofChannelLearnedInfo [ixNet getList $learnedInfo ofChannelLearnedInformation]
ixNet exec addRecordForTrigger $ofChannelLearnedInfo
ixNet setAttr $learnedInfo -enableSendTriggeredFlowStatLearnedInformation true
ixNet commit
after 5000
ixNet exec trigger $learnedInfo
after 10000
puts "Trigger sent"
after 10000

#--------------------------------------------------------------------------#
# Check Flow Stat learned info                           #
#--------------------------------------------------------------------------#
    
puts "Checking Flow Stat Learned Info"
set flowStatLearnedInformation [ixNet getList $learnedInfo flowStatLearnedInformation]
set flowStatLearnedInformationFirst [lindex $flowStatLearnedInformation 0]
if {[ixNet getAttr $flowStatLearnedInformationFirst -ethernetDestination] != "00:02:00:00:00:01" \
    || [ixNet getAttr $flowStatLearnedInformationFirst -ethernetSource] != "00:01:00:00:00:01" \
    || [ixNet getAttr $flowStatLearnedInformationFirst -ethernetType] != "0x800" \
    || [ixNet getAttr $flowStatLearnedInformationFirst -ipv4Destination] != "2.1.1.1/32" \
    || [ixNet getAttr $flowStatLearnedInformationFirst -ipv4Source] != "1.1.1.1/32" \
    || [ixNet getAttr $flowStatLearnedInformationFirst -tableId] != "1"} {
    puts "Flows not learned properly for first flow"
}

set flowStatLearnedInformationLast [lindex $flowStatLearnedInformation end]
if {[ixNet getAttr $flowStatLearnedInformationLast -ethernetSource] != "00:03:00:00:00:01" \
    || [ixNet getAttr $flowStatLearnedInformationLast -ethernetType] != "0x8847" \
    || [ixNet getAttr $flowStatLearnedInformationLast -mplsLabel] != "10"} {
    puts "Flows not learned properly for last flow"
}

