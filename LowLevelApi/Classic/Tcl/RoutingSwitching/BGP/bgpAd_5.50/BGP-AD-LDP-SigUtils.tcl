#-------------------------------------------------------------------------------
# PROCEDURE  : checkBGPLearnedInfo
# PURPOSE    :
# PARAMETERS : neighborRange    - BGP neighborRange object
#              checkLearntInfoList - The list of expected info
#              filterList - The filter for leart info display
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#-------------------------------------------------------------------------------
proc checkBGPLearnedInfo {neighborRange checkLearntInfoList {filterList {}}} {
    set isError 1

    # set filter following filterlist
    array set filterListArray $filterList
    log "Setting BGP Learnt Info filter ... \n [parray filterListArray]"
    set learnedFilter $neighborRange/learnedFilter
    set capabilities $learnedFilter/capabilities
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $capabilities $attr [list $attrVal y]] \
             == 1} {
            return $isError
        }
    }
    after 2000

    log "Refreshing for learnt information on BGP neighbor: $neighborRange\n"
    set a [ixNet exec refreshLearnedInfo $neighborRange]

    set count 0
    set isComplete false
    while {$isComplete != true} {
        set isComplete [ixNet getAttr $neighborRange -isLearnedInfoRefreshed]
        log "isComplete = $isComplete"
        after 1000
        incr count
        if {$count > 40} {
            log "Could not retrieve learnt info on bgp neighbor: \
                $neighborRange, timeout"
            break
        }
    }
    log "BGP Learnt Info refreshed for BGP Neighbor : $neighborRange !!!"

    # Get ALL Learned Info List
    set learnedInformation $neighborRange/learnedInformation

    foreach {learntInfoType db expectedCheckList} $checkLearntInfoList {
        # Get Learned Info List
        set learnedInfoList [ixNet getList $learnedInformation $learntInfoType]
        if {[llength $learnedInfoList] == 0} {
            log "No BGP learnt info present for $learntInfoType !!!"
            return $isError
        }

        log "[llength $learnedInfoList] BGP learnt info present for \
            $learntInfoType !!!"

        # Loop through expected list & search in learntinfo list
        set numInfoInCheckList 0
        set isFound 0
        foreach checkList $expectedCheckList {
            foreach $db $checkList {
                incr numInfoInCheckList
                log " -----------------------------"
                log "Browsing BGP $learntInfoType learntinfo list ..."
                foreach learntInfo $learnedInfoList {
                    set misMatch 0
                    foreach attr $db {
                        set attrVal [set [set attr]]
                        if {[matchAttributeValue $learntInfo $attr $attrVal] \
                             == 1} {
                             set misMatch 1
                             break
                        }
                    }

                    if {$misMatch == 0} {
                        # Reached here -> all field match found in learnt info
                        log "Expected learntinfo present in BGP \
                            $learntInfoType learntinfo list !!!"
                        log " ----------------------------- "
                        incr isFound
                        break
                    }
                }
            }
        }

        log "Among all $numInfoInCheckList info $isFound are present in BGP \
             $learntInfoType Learnt Info List"

        if {$numInfoInCheckList != $isFound} {
            return $isError
        }
    }

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : checkLDP_BgpAdVplsLearnedInfo
# PURPOSE    :
# PARAMETERS : router    - LDP router object
#              checkLearntInfoList - The list of expected info
#              filterList - The filter for leart info display
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#-------------------------------------------------------------------------------

proc checkLDP_BgpAdVplsLearnedInfo {router checkLearntInfoList} {
    set isError 1

    log "Refreshing for learnt information on LDP Router: $router\n"
    set a [ixNet exec refreshBgpAdVplsLearnedInfo $router]

    set count 0
    set isComplete false
    while {$isComplete != true} {
        set isComplete [ixNet getAttr $router -isBgpAdVplsLearnedInfoRefreshed]
        log "isComplete = $isComplete"
        after 1000
        incr count
        if {$count > 40} {
            log "Could not retrieve LDP Learnt info on LDP Router: \
                 $router, timeout"
            break
        }
    }
    log "LDP Learnt Info refreshed for LDP Router: $router !!!"

    # Get ALL Learned Info List
    foreach {db expectedCheckList} $checkLearntInfoList {
        # Get Learned Info List
        set learnedBgpAdVplsLabelsList [ixNet getList $router \
            learnedBgpAdVplsLabels]

        if {[llength $learnedBgpAdVplsLabelsList] == 0} {
            log "No LDP learnt info present for learnedBgpAdVplsLabels !!!"
            return $isError
        }

        log "[llength $learnedBgpAdVplsLabelsList] LDP learnt info present for \
             learnedBgpAdVplsLabels !!!"

        # Loop through expected list & search in learntinfo list
        set numInfoInCheckList 0
        set isFound 0
        foreach checkList $expectedCheckList {
            foreach $db $checkList {
                incr numInfoInCheckList
                log " -----------------------------"
                log "Browsing LDP learnedBgpAdVplsLabels learntinfo list ..."
                foreach learntInfo $learnedBgpAdVplsLabelsList {
                    set misMatch 0
                    foreach attr $db {
                        set attrVal [set [set attr]]
                        if {[matchAttributeValue $learntInfo $attr $attrVal] \
                             == 1} {
                             set misMatch 1
                             break
                        }
                    }

                    if {$misMatch == 0} {
                        # Reached here -> all field match found in learnt info
                        log "Expected learntinfo present in LDP \
                             learnedBgpAdVplsLabels learntinfo list !!!"
                        log " ----------------------------- "
                        incr isFound
                        break
                    }
                }
            }
        }

        log "Among all $numInfoInCheckList info $isFound are present in LDP \
             learnedBgpAdVplsLabels Learnt Info List"

        if {$numInfoInCheckList != $isFound} {
            return $isError
        }
    }

    set isError 0
    return $isError
}



#-------------------------------------------------------------------------------
# PROCEDURE  : checkLDPLearnedInfo
# PURPOSE    :
# PARAMETERS : interface    - LDP router interface object
#              checkLearntInfoList - The list of expected info
#              filterList - The filter for leart info display
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#-------------------------------------------------------------------------------

proc checkLDPLearnedInfo {interface checkLearntInfoList {filterList {}}} {
    set isError 1

    # set filter following filterlist
    array set filterListArray $filterList
    log "Setting LDP Learnt Info filter ... \n [parray filterListArray]"
    set learnedFilter $interface/learnedFilter
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $learnedFilter $attr \
            [list $attrVal y]] == 1} {
            return $isError
        }
    }
    after 2000

    log "Refreshing for learnt information on LDP interface: $interface\n"
    set a [ixNet exec refreshLearnedInfo $interface]

    set count 0
    set isComplete false
    while {$isComplete != true} {
        set isComplete [ixNet getAttr $interface -isLdpLearnedInfoRefreshed]
        log "isComplete = $isComplete"
        after 1000
        incr count
        if {$count > 40} {
            log "Could not retrieve LDP Learnt info on LDP interface: \
                 $interface, timeout"
            break
        }
    }
    log "LDP Learnt Info refreshed for LDP interface: $interface !!!"

    # Get ALL Learned Info List
    foreach {learntInfoType db expectedCheckList} $checkLearntInfoList {
        # Get Learned Info List
        set learnedInfoList [ixNet getList $interface $learntInfoType]
        if {[llength $learnedInfoList] == 0} {
            log "No LDP learnt info present for $learntInfoType !!!"
            return $isError
        }

        log "[llength $learnedInfoList] LDP learnt info present for \
             $learntInfoType !!!"

        # Loop through expected list & search in learntinfo list
        set numInfoInCheckList 0
        set isFound 0
        foreach checkList $expectedCheckList {
            foreach $db $checkList {
                incr numInfoInCheckList
                log " -----------------------------"
                log "Browsing LDP $learntInfoType learntinfo list ..."
                foreach learntInfo $learnedInfoList {
                    set misMatch 0
                    foreach attr $db {
                        set attrVal [set [set attr]]
                        if {[matchAttributeValue $learntInfo $attr $attrVal] \
                             == 1} {
                             set misMatch 1
                             break
                        }
                    }

                    if {$misMatch == 0} {
                        # Reached here -> all field match found in learnt info
                        log "Expected learntinfo present in LDP \
                             $learntInfoType learntinfo list !!!"
                        log " ----------------------------- "
                        incr isFound
                        break
                    }
                }
            }
        }

        log "Among all $numInfoInCheckList info $isFound are present \
             in LDP $learntInfoType Learnt Info List"

        if {$numInfoInCheckList != $isFound} {
            return $isError
        }
    }

    set isError 0
    return $isError
}