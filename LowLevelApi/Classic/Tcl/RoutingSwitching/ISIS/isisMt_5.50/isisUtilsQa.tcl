#-------------------------------------------------------------------------------
# PROCEDURE  : checkAllIsisStats
# PURPOSE    :
# PARAMETERS : portList -
#              stat - {name value} Stat list to verify
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc checkAllIsisStats {portLists stat {exactMatch 0}} {
    return [checkAllProtocolStats $portLists "ISIS" $stat $exactMatch]
}


#-------------------------------------------------------------------------------
# PROCEDURE  : checkISISLearnedInfo
# PURPOSE    :
# PARAMETERS : router    - ISIS router object
#              checkList - The list of expected info to be checked in \
#                          learntInfoList
#              filterList - The filter for leart info display
#                   filterIpv4MulticastTlvs         Bool
#                   filterIpv6MulticastTlvs         Bool
#                   filterLearnedIpv4Prefixes       Bool
#                   filterLearnedIpv6Prefixes       Bool
#                   filterLearnedRbridges           Bool
#                   filterMacMulticastTlvs          Bool
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#-------------------------------------------------------------------------------

proc checkISISLearnedInfo {router checkLearntInfoList {filterList {}}} {

    set isError 1

    # Below veriable is for debug log only
    array set filterListArray $filterList
    log "Setting ISIS Learnt Info filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $router $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }
    after 2000

    # Refresh ISIS learnt Info
    set status [ixNet exec refreshLearnedInformation $router]
    after 10000
    set status [ixNet exec refreshLearnedInformation $router]

    if {[string first "::ixNet::OK" $status] == -1} {
        log "Failed to refresh ISIS Learnt info..."
        return $isError
    }
    after 30000
    log "ISIS learnt info refreshed ..."

    # Get ALL Learned Info List
    set routerLearnedInfoList [ixNet getList $router learnedInformation]
    log "Lenght of ALL Leant Info List :: [llength $routerLearnedInfoList]"

    foreach {leartInfoType db expectedCheckList} $checkLearntInfoList {
        # Get Learned Info List
        catch {ixNet help $routerLearnedInfoList} result
        puts $result

        set learnedInfoList [ixNet getList $routerLearnedInfoList $leartInfoType]
        puts "---------------> $learnedInfoList"

        if {[llength $learnedInfoList] == 0} {
            log "No ISIS learnt info present for $leartInfoType ... "
            return $isError
        }
        log "[llength $learnedInfoList] ISIS learnt info present for \
             $leartInfoType"

        # Loop through expected list & search in learntinfo list
        set numInfoInCheckList 0
        set isFound 0
        foreach checkList $expectedCheckList {
            foreach $db $checkList {
                incr numInfoInCheckList
                log " -----------------------------"
                log "Browsing ISIS $leartInfoType learntinfo list ..."
                foreach learntInfo $learnedInfoList {
                    set misMatch 0
                    foreach attr $db {
                        set attrVal [set [set attr]]
                        #log "$attr >> [ixNet getAttr $learntInfo -$attr]"
                        if {($attr == "age") || ($attr == "sequenceNumber")} {
                            log "$attr :: [ixNet getAttr $learntInfo -$attr] \
                               (expected $attrVal) - Not going for exact Match"
                            continue
                        }
                        if {[matchAttributeValue $learntInfo $attr $attrVal] \
                             == 1} {
                             set misMatch 1
                             break
                        }
                    }
                    if {$misMatch == 0} {
                        # Reached here -> all field match found in learnt info
                        log "Expected learntinfo present in ISIS $leartInfoType \
                             learntinfo list ..."
                        log " ----------------------------- "
                        incr isFound
                        break
                    }
                }
            }
        }
        log "Among all $numInfoInCheckList info $isFound are present \
             in ISIS $leartInfoType Learnt Info List"
        if {$numInfoInCheckList != $isFound} {
            return $isError
        }
    }
    set isError 0
    return $isError
}
