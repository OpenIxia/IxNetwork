proc checkAllRSVPStats { portList stat } {
    set sessFoundFlag 0
    set userViewList [ixNet getList [ixNet getRoot]/statistics userStatView]
    foreach view $userViewList {
        ixNet remove $view
        ixNet commit
    }

    set userStatView [SetupUserStats $portList "RSVP" "*"]
    set timeout 20
    set doneList $portList

    array set statToVerify $stat
    set statNames [array names statToVerify]

    set returnFlag 1
    # Checking the stats.."
    set contFlag 0
    foreach eachStat $statNames {
        while {$timeout > 0} {
            GetStatValue "UserStatView RSVP" "$eachStat" statValueArray1
            if {[lindex [array get statValueArray1] 1] >= $statToVerify($eachStat)} {
                    PrintArray statValueArray1
                    log "For stat $eachStat expected is $statToVerify($eachStat) \
                         obtained: [lindex [array get statValueArray1] 1] "
            } else {
                    PrintArray statValueArray1
                    log "For stat $eachStat expected is $statToVerify($eachStat) \
                         obtained: [lindex [array get statValueArray1] 1] --> MIS Match "
                  set returnFlag 0
                  return 1
            }

            foreach portItem $doneList {
                scan [join [split $portItem]] "%s %s %s" ch card port
                set sessFoundFlag 0
                if {([llength [array get statValueArray1]] > 0)} {
                    if {$statValueArray1($ch,$card,$port) >= 0} {
                        set sessFoundFlag 1
                        set index [lsearch $doneList [list $ch $card $port]]
                        if {$index != -1} {
                            set doneList [lreplace $doneList $index $index]
                        }
                    }
                }
            }

            if {[llength $doneList] == 0} {
                set contFlag 1
                break
            } else {
                incr timeout -1
                after 1000
            }
        }
    }

    if {$contFlag == 0} {
        logMsg "Error in establishing RSVP sessions... Check the configuration"
        return 1
    }
    if {$returnFlag == 1} {
        return 0
    } else {
        return 1
    }
    after 2000
}

proc log {str} {
    puts "ixia: $str"
}

proc ixNetCleanUp {} { ixNet exec newConfig}

##############################################################################
# PROC NAME    : getAssignedLabelInfo
# ARGUMENT     : 1. neighborPair on a particular port
#                2. List of the learnt info to be checked
# DESCRIPTION  : Check the assigned label info on a particular neighborPair
#                according to the value that is supplied
# RETURN       : Returns 0 if success else return 1
##############################################################################
proc getAssignedLabelInfo {neighborpair mainCheckLearnedLabelList {exactMatch 1}} {
    set isError 1
    set ref [ixNet exec refreshAssignedLabelInfo $neighborpair]

    log "Refreshing for Learnt Assigned label for Downstream \
            Router neighborpair : $neighborpair...\n"
    
    set count 0
    set isComplete false
    while {$isComplete != true} {
        set isComplete [ixNet getAttr $neighborpair -isAssignedInfoRefreshed]
        log "isComplete --> $isComplete"
        after 1000
        incr count
        if {$count > 50} {
            log "Failed to retrieve assigned label for Downstream \
                 Router neighborpair: $neighborpair, timeout"
            return $isError
        }
    }
    log "Assigned label for downstream Router neighborpair information refreshed ..."

    # Get Assigned Label Learned Info List
    set assignedLearnedInfoList [ixNet getList $neighborpair assignedLabel]

    if {[llength $assignedLearnedInfoList] == 0} {
        log "No Receive Label learnt info present ... "
        return $isError
    }
    # Loop through expected list & search in learntinfo list
    set i 0

    foreach CheckLearnedLabelList $mainCheckLearnedLabelList {
        set isError 1
        foreach labelInfo $assignedLearnedInfoList {
            incr i
            set isFound  0
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
            }
        }
        if {$isError == 1} {
            log "Not Finding matching with Learned info"
            return $isError
        }
    }

    set isError 0
    log "All infos not present in Assigned Label Learnt Info List"
    return $isError
}


##############################################################################
# PROC NAME  :getReceivedLabelInfo
# ARGUMENT   :
#             1.neighborPair on a particular port
#             2.List of the learnet info to be checked
# DESCRIPTION: Check the received label on a particular neighborPair according
#              to the value that is supplied
# RETURN     : Returns 0 if success else return 1
##############################################################################
proc getReceivedLabelInfo {neighborpair mainCheckLearnedLabelList {exactMatch 1}} {

    set isError 1
    set ref [ixNet exec refreshReceivedLabelInfo $neighborpair]

    log "Refreshing for learnt Received label for upstream Router \
         neighborpair : $neighborpair...\n"
    set count      0
    set isComplete false
    
    while {$isComplete != true} {
        set isComplete [ixNet getAttr $neighborpair -isLearnedInfoRefreshed]
        log "isComplete --> $isComplete"
        after 1000
        incr count
        if {$count > 50} {
            log "Failed to retrieve received label for upstream Router \
                 neighborpair: $neighborpair, timeout"
            return $isError
        }
    }

    log "received label for upstream Router neighborpair \
            information refreshed ..."

    # Get RP Learned Info List
    set receivedLearnedInfoList [ixNet getList $neighborpair receivedLabel]
    if {[llength $receivedLearnedInfoList] == 0} {
        log "No Receive Label learnt info present ... "
        return $isError
    }

    # Loop through expected list & search in learntinfo list
    set i 0
    foreach CheckLearnedLabelList $mainCheckLearnedLabelList {
        set isError 1
        foreach labelInfo $receivedLearnedInfoList {
            incr i
            set isFound  0
            set mismatch 0
            log "Browsing Received Label learnt Info list (entry $i)..."
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
                log "Among all $isFound info are present in Received \
                     Label Learnt Info List"
                set isError 0
            }
        }
        if {$isError == 1} {
            log "Not Finding matching with Learned info"
            return $isError
        }
    }
    
    set isError 0
    log "All infos not present in Received Label Learnt Info List"
    return $isError
}

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


#-------------------------------------------------------------------------------
# PROCEDURE  : verifyCapturedPackets
# PURPOSE    : Verifying expected field value in Captured Packets
# PARAMETERS : chassis -
#              card -
#              port -
#              matchFieldList - list of {startIndex endIndex expectedVal}
#              expPktCnt - {default value 1}
#			   index - {default value 0} returns nth packet of a particular type
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc verifyCapturedPackets {chassis card port matchFieldList {expPktCnt 1} \
     {index 0}} {
        
    set isError 1

    log "Initializing through IxTclHal...."
    ixInitialize  $chassis
    chassis get   $chassis
    set chassisId [chassis cget -id]

    port get $chassisId $card $port
    set loginName [port cget -owner]
    ixLogin $loginName
    log "Logging in using the $loginName"

    # Retrive captured packets
    captureBuffer get $chassisId $card $port
    set numCapturedPkts [captureBuffer cget -numFrames]
    log "Captured $numCapturedPkts pkts (expected: $expPktCnt)"
    if {$numCapturedPkts < $expPktCnt} {
        return $isError
    }

    captureBuffer get $chassisId $card $port 1 $numCapturedPkts
    set cnt 0
    for {set f 1} {$f <= $numCapturedPkts} {incr f} {
        after 50
        captureBuffer getframe $f
        after 50
        set capframe [captureBuffer cget -frame]
        set mismatch 0
        foreach {startIndex endIndex expectedVal} $matchFieldList {
            log "Obtained: [lrange $capframe $startIndex $endIndex] \
                 Expected: $expectedVal"
            if {[lrange $capframe $startIndex $endIndex] != $expectedVal} {
                set mismatch 1
                log "Obtained: [lrange $capframe $startIndex $endIndex] \
                     Expected: $expectedVal ---> No Match"
                break
            }
        }

        if {$mismatch == 0} {
            log "All Field Patterns Matched !!!"
            incr cnt
            log "Matching Packet No. $cnt found"
        }
        # Added to get the particular no packet for particular pattern say
        # I want to get the 3rd hello packet
		# By putting index=3 we can achieve this
		if {($index > 0) && ($index==$cnt)} {
		   log "Specific Packet found"
		   break
		}
    }

    log "This is the number of matched packets $cnt"
    if {($index > 0) && ($cnt != $index)} {
        return $isError
    } else {
        return $capframe
    }
}
