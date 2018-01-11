#-------------------------------------------------------------------------------
# PROCEDURE  : verifyLacpLearnedInfo
# PURPOSE    :
# PARAMETERS : portList -
#              stat - {name value} Stat list to verify
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc verifyLacpLearnedInfo {linkProtoId checkLinkLearntInfoList \
                            {ckeckNumLAGsList {}}} {
    set isError 1

    # Request LearnedInfo
    set retVal [ixNet exec refreshLacpPortLearnedInfo $linkProtoId]

    set isComplete false
    set count 0
    while {$isComplete != true} {
        flush stdout
        set isComplete \
            [ixNet getAttr $linkProtoId -isLacpPortLearnedInfoRefreshed]

        puts "isComplete = $isComplete"
        after 5000
        incr count
        if {$count > 10} {
            puts "Could not retrieve learnt info on LACP link :\
                 <$linkProtoId> , ... timeout"
            return ""
        }
    }

    # Get Learned Info List
    set learnedInfoList [ixNet getList $linkProtoId learnedInfo]
    if {[llength $learnedInfoList] == 0} {
        log "No LACP learnt info present  ... "
        return $isError
    }
    log "[llength $learnedInfoList] LACP learnt info present... "

    foreach {db expectedCheckList} $checkLinkLearntInfoList {
        # Loop through expected list & search in learntinfo list
        set numInfoInCheckList 0
        set isFound 0
        foreach checkList $expectedCheckList {
            #puts "db $db --- checkList $checkList ... "
            foreach $db $checkList {
                incr numInfoInCheckList
                log " -----------------------------"
                log "Browsing LACP learntinfo list ..."
                foreach learntInfo $learnedInfoList {
                    set misMatch 0
                    foreach attr $db {
                        set attrVal [set [set attr]]
                        #puts "[ixNet help $learntInfo]"
                        log "$attr >> [ixNet getAttr $learntInfo -$attr]"
                        if {[matchAttributeValue $learntInfo $attr $attrVal] \
                             == 1} {
                             set misMatch 1
                             break
                        }
                    }

                    if {$misMatch == 0} {
                        # Reached here -> all field match found in learnt info
                        log "Expected learntinfo present in LACP learntinfo"
                        log " ----------------------------- "
                        incr isFound
                        break
                    }
                }
            } ;# learntInfo $learnedInfoList
        } ;# checkList $expectedCheckList

        log "Among all $numInfoInCheckList info $isFound are \
             present in LACP Learnt Info List"
        if {$numInfoInCheckList != $isFound} {
            return $isError
        }
    }

    set isError 0
    return $isError
}


