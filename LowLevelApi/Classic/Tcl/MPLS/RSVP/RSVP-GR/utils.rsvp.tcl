################################################################################
#File Name  :utils.rsvp.tcl
#Author     :Animesh Roy
#Reviwer    :Suvendu Mazumder
#Purpose    :Utility file for RSVP-GR Automation
#procs      :
#           1.arrange
#           2.checkAllRSVPStats_DefaultView
#           3.checkAllRSVPStats_Userview
#           4.checkAttributeValue
#           5.disableIPv4interface
#           6.getAssignedLabelCount
#           7.getAssignedLabelInfo
#           8.getReceivedLabelCount
#           9.getReceivedLabelInfo 
#           10.matchAttributeValue
#           11.setAndCheckAttributeValue
#           12.verifyCapturedPackets
# 
#Topology   :B2B
#################################################################################

#################################################################################
# LOGGING
# Procedure  : log
# Description: Formatting log printing
# Argument(s):
#              str -  String to be printed.
#
#################################################################################
proc log {str} {
    puts "ixia: $str"
}


################################################################################
# PROC NAME :getAssignedLabelInfo
# ARGUMENT  :
#              1. neighborPair on a particular port
#              2. List of the learnt info to be checked
# DESCRIPTION: Check the assigned label info on a particular neighborPair 
#              according to value that is supplied
# RETURN     : Returns 0 if success else return 1
################################################################################
proc getAssignedLabelInfo {neighborpair CheckLearnedLabelList} {
    set isError 1
    set ref [ixNet exec refreshAssignedLabelInfo $neighborpair]

    log "Refreshing for Learnt Assigned label for Downstream Router \
         neighborpair : $neighborpair...\n"

    set count 0
    set isComplete false
    while {$isComplete != true} {
        set isComplete [ixNet getAttr $neighborpair -isAssignedInfoRefreshed]
        log "isComplete --> $isComplete"
        after 1000
        incr count
        if {$count > 50} {
            log "Failed to retrieve assigned label for Downstream Router \
                 neighborpair: $neighborpair, timeout"
            return $isError
        }
    }

    log "Assigned label for downstream Router neighborpair \
         information refreshed ..."

    # Get Assigned Label Learned Info List
    set receivedLearnedInfoList [ixNet getList $neighborpair assignedLabel]
     
    if {[llength $receivedLearnedInfoList] == 0} {
        log "No Receive Label learnt info present ... "
        return $isError
    }
    
    # Loop through expected list & search in learntinfo list
    set i 0
    foreach labelInfo $receivedLearnedInfoList {
        incr i
        set isFound 0
        set mismatch 0
        log "Browsing Assigned Label learnt Info list (entry $i)..."
        log "------------------------------------------"
        foreach {attr attrVal} $CheckLearnedLabelList {
            #log "Expected val for $attr is $attrVal"
            if {[matchAttributeValue $labelInfo $attr $attrVal] == 1} {
                # Handle not exactMatch cases hare ....
                incr mismatch
                break
            } else {
                # Reached here -> field match found in learnt info
                incr isFound
            }
        }
        
        if {($isFound != 0) && ($mismatch == 0)} {
            log "Among all $isFound info are present in Assigned \
                 Label Learnt Info List"
            set isError 0
            return $isError
        }
    }
    log "All infos not present in Assigned Label Learnt Info List"
    return $isError
}


###############################################################################
# STATS VERIFICATION
# Procedure:checkAllRSVPStats_DefaultView
# Description:Check all RSVP Aggregated stats
#   Argument(s):
#       portLIst -  Ports on which the sessions has to be checked.
#       statList -  List of Stats to be checked.
#
###############################################################################
proc checkAllRSVPStats_DefaultView { portdata stat } {
    set statViewList [ixNet getList [ixNet getRoot]/statistics statViewBrowser]
    array set statToVerify $stat
    set statNames [array names statToVerify]
    set portData [lindex $portdata 0]
    set chassisIvPort1 [lindex $portData 0]
    set card1 [lindex $portData 1]
    set port1 [lindex $portData 2]
    set statView [concat ::ixNet::OBJ-/statistics/statViewBrowser:"RSVP Aggregated Statistics"]
    
    if {[ixNet getAttribute $statView -enabled] == "false"} {
        ixNet setAttribute $statView -enabled true
        ixNet commit
    }

    set statViewObjRef $statView

    set continueFlag "true"
    set timeout 5

    while {$continueFlag == "true"} {
        if {[ixNet getAttribute $statViewObjRef -isReady] == true} {
            set rowList [ixNet getList $statViewObjRef row]
            foreach row $rowList {
                set cellList [ixNet getList $row cell]
                foreach cell $cellList {
                    set statName [ixNet getAttribute $cell -catalogStatName]
                    set rowName [ixNet getAttribute $cell -rowName]
                    set statValue [ixNet getAttribute $cell -statValue]
                    set splitString [split $rowName /]
                    set hostName [lindex $splitString 0]
                    set card [string trimleft [lindex $splitString 1] "Card"]
                    set port [string trimleft [lindex $splitString 2] "Port"]
                    set card [string trimleft $card 0]
                    set port [string trimleft $port 0]
                    set statValueArray($hostName,$card,$port,$statName) $statValue
                }
           }
           break

        } else {
            if {$timeout ==0} {
                set continueFlag false
            } else {
                after 1000
                incr timeout -1
            }
        }
    } ;# end while {$continueFlag == "true"}

    foreach stat $statNames {
        if {$statValueArray($chassisIvPort1,$card1,$port1,$stat) \
             == $statToVerify($stat)} {
            log "statValueArray($chassisIvPort1,$card1,$port1,$stat)\
                 ---EXPECTED:$statToVerify($stat)"
            log "OBTAINED:$statValueArray($chassisIvPort1,$card1,$port1,$stat)\
                 ---Matched"
        } else {
            log "statValueArray($chassisIvPort1,$card1,$port1,$stat)\
                    ---EXPECTED:$statToVerify($stat)"
            log "OBTAINED:$statValueArray($chassisIvPort1,$card1,$port1,$stat)\
                 ---Mismatched"
            return 1
       }
    }
    return 0
}

proc ixNetCleanUp {} { ixNet exec newConfig}
#############################################################################
# Common procs to be used for set & get attr
#############################################################################
proc matchAttributeValue {object attr expectedVal} {
    set noMatch 1
    set val [ixNet getAtt $object -$attr]
    #log "\t (-$attr)$val : expected: $expectedVal"
    if {[string tolower $val] != [string tolower $expectedVal]} {
        log "\t -$attr : $val (expected $expectedVal) ---> No Match"
        return $noMatch
    }
    log "\t -$attr : $val (expected $expectedVal) ---> Match"
    set noMatch 0
    return $noMatch
}    
