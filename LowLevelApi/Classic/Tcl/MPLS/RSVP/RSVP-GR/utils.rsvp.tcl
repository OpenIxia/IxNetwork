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
#File Name  :utils.rsvp.tcl
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
