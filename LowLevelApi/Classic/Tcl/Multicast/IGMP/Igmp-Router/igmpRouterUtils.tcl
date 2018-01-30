package req IxTclNetwork

proc sleep {sec} {
    set sec [expr $sec * 1000]
    after $sec
}



proc checkAllIGMPStats { portList stat } {
    set sessFoundFlag 0
    set userViewList [ixNet getList [ixNet getRoot]/statistics userStatView]
    foreach view $userViewList {
        ixNet remove $view
        ixNet commit
    }

    set userStatView [SetupUserStats $portList "IGMPQuerier" "*"]
    set timeout 20
    set doneList $portList

    array set statToVerify $stat
    set statNames [array names statToVerify]

    set returnFlag 1
    #Checking the stats.."
    set contFlag 0
    foreach eachStat $statNames {
        while {$timeout > 0} {
            GetStatValue "UserStatView IGMPQuerier" "$eachStat" statValueArray1
            if {[lindex [array get statValueArray1] 1] >= $statToVerify($eachStat)} {
                PrintArray statValueArray1
                puts "For stat $eachStat expected is $statToVerify($eachStat)"
                puts "obtained: [lindex [array get statValueArray1] 1] "
            } else {
                PrintArray statValueArray1
                puts "For stat $eachStat expected is $statToVerify($eachStat)"
                puts "obtained: [lindex [array get statValueArray1] 1] --> MIS Match"
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
        puts "Error in establishing sessions... Check the configuration"
        return 1
    }

    if {$returnFlag == 1} {
        return 0
    } else {
        return 1
    }
    after 2000
}


proc getIgmpLearnedInfo {igmpRtr} {
    set isComplete false
    set count 0
    set protocolName igmp

    # Request LearnedInfo
    set retVal [ixNet exec refreshLearnedInfo $igmpRtr]

    while {$isComplete != true} {
        flush stdout
        set isComplete [ixNet getAttr $igmpRtr -isRefreshComplete]
        puts "isComplete = $isComplete"
        after 5000
        incr count
        if {$count > 4} {
            puts "Could not retrieve learnt info on \
                 $protocolName querier : $protocolName Router, ... timeout"
            return ""
        }
    }

    set learntList [ixNet getList $igmpRtr learnedGroupInfo]
    return $learntList
}

#--------------------------------------------------------------------------------
# The proc below returns all the entries of a particular group in learned info
# database, It queries the database for a max of QI time, if it does not get
# the required enty it returns ""
#--------------------------------------------------------------------------------

proc retrieveLearnedInfoDetailsByGroup {igmpRtr grp {waitTime 125}} {

    set retInfo ""
    set startTime [clock seconds]

    while {1} {
        after 5000;#keep polling every 5 sec.

        set curTime [clock seconds]
        if {[expr $curTime-$startTime] <= $waitTime} {
            #Check if one QI period has passed
            set learnedList [getIgmpLearnedInfo $igmpRtr]

            puts "Learned Info : <$learnedList>"
            if {[llength $learnedList] > 0} {
                #Learned Info Database is not empty
                foreach linfo $learnedList {

                    #Traverse the database
                    set grpAddr [::ixNet getAttribute $linfo -groupAddress]

                    if {$grpAddr == $grp} {
                        # Entry found for $grp, keep adding all entries
                        # for $grp in a list
                        lappend retInfo "\
                            grpAddr   [ixNet getAttr $linfo -groupAddress]      \
                            grpMode   [ixNet getAttr $linfo -filterMode]        \
                            srcAddr   [ixNet getAttr $linfo -sourceAddress]     \
                            compMode  [ixNet getAttr $linfo -compatibilityMode] \
                            grpTimer  [ixNet getAttr $linfo -groupTimer]        \
                            srcTimer  [ixNet getAttr $linfo -sourceTimer]       \
                            compTimer [ixNet getAttr $linfo -compatibilityTimer]"
                    }
                }

                if {$retInfo != ""} {
                    #Entry found for group $grp, quit the search
                    puts "retInfo is set to : <$retInfo>"
                    return $retInfo
                }

            } else {
                puts "No entry exists, check again ...."
            }
        } else {;#One QI has passed, now quit the search with NULL
            return $retInfo
        }
    } ;# end while (1)
}


#--------------------------------------------------------------------------------
# The proc below keeps on querying the learned info database for
# waiTime (default QI time) and returns the entire learned info
# database, if nothing is found it returns ""
#--------------------------------------------------------------------------------
proc retrieveLearnedInfoDetails {igmpRtr {waitTime 125}} {

    set retInfo ""
    set startTime [clock seconds]
    while {1} {
        after 5000;#keep polling every 5 sec.
        set curTime [clock seconds]
        if {[expr $curTime-$startTime] <= $waitTime} {
            # Check if one QI period has passed
            set learnedList [getIgmpLearnedInfo $igmpRtr]
            puts "Learned Info : <$learnedList>"
            if {[llength $learnedList] > 0} {;#List is not empty
                return $learnedList
            } else {
                puts "No entry exists, check again ...."
            }
        } else {
           puts "Waited for QI interval, no entry found, returning back ..."
           return $retInfo
        }
    }
}


#--------------------------------------------------------------------------------
# THe proc below finds out the value of a particular param from linfo
#--------------------------------------------------------------------------------
proc getParamFromLearnedInfo {linfo param} {
    puts "Learned Info list : <$linfo>"
    set index [lsearch $linfo $param]
    if {$index != -1} {
        set retval [lindex $linfo [incr index]]
        puts "$param : <$retval>"
    } else {
        puts "$param : No such param exists"
        return -1
    }
    return $retval
}


########################################################################################
# Procedure: ixTclNet::SetupUserStats
#
# Description: Sets up user stats view for the requested stat list and start monitoring.
#
# Arguments: realPortList      - A list of real ports in the format of or wildcards
#            sourceType        - Stat source type. That can be obtained from doc or catalog API
#            statNameList      - Stat name list. They can be obtained from doc or catalog API.
#                                It can be '*'. Then all stats for the selected sourceType available
#                                in the catalog would be added.
#
#
#
# Returns: The objRef of created userStatView.
########################################################################################


proc SetupUserStats { realPortList sourceType statNameList} {

    set userStatViewObjRef ""

    set viewCaptionString "UserStatView $sourceType"
    #Create filterValues for the realPortList
    set filterValueList {}

    foreach realPort $realPortList {
        scan [join $realPort] "%s %d %d" hostname card_id port_id
        lappend filterValueList "$hostname/Card$card_id/Port$port_id"
        puts  "$hostname/Card$card_id/Port$port_id"
    }
    puts "filterValueList $filterValueList"

    #Verify filters
    set catalogList [ixNet getList [ixNet getRoot]/statistics catalog]
    puts "Catalog List is $catalogList"
    set i 1
    foreach catalog $catalogList {
        #log "catalog$i $catalog"
        if {[ixNet getAttribute $catalog -sourceType] == $sourceType} {
            set catalogSourceType $catalog
            break
        }
    }
    set validFilterValueList {}
    set filterList [ixNet getList $catalogSourceType filter]
    foreach filterItem $filterList {
        if {[ixNet getAttribute $filterItem -name] == "Port"} {
            set validFilterValueList [ixNet getAttribute $filterItem -filterValueList]
            break
        }
    }
    if {[llength $validFilterValueList] == 0} {
        logMsg "Error: There is no filter for the selected sourceType in the catalog"
        error "Error: There is no filter for the selected sourceType in the catalog"
        return $userStatViewObjRef
    }

    #If the statName list is in form of wild card get all stats name for
    #for the sourceType from catalog.

    if {$statNameList == "*"} {

        #At this moment getFilterList is not working for C# publishers
        #So I loop through of each catalog to find selected sourceType.
        set catalogSourceType ""
        set catalogList [ixNet getList [ixNet getRoot]/statistics catalog]
        foreach catalog $catalogList {
            #puts "This is the compare [ixNet getAttribute $catalog -sourceType] and $sourceType"
            if {[ixNet getAttribute $catalog -sourceType] == $sourceType} {
                set catalogSourceType $catalog
                break
            }
        }
        set statNameList {}
        set statList [ixNet getList $catalogSourceType stat]
        foreach statItem $statList {
            lappend statNameList [ixNet getAttribute $statItem -name]
        }
    }

    #Create userStatView
    #First search whether we have already added a userStatView for that sourceType.

    set existFlag false
    set userStatViewList [ixNet getList [ixNet getRoot]/statistics userStatView]
    foreach userView $userStatViewList {

        if {[ixNet getAttribute $userView -viewCaption] == $viewCaptionString} {
            set userStatViewObjRef $userView
            set existFlag true
            break
        }

    }

    if {$existFlag == "true"} {
        ixNet setAttribute $userStatViewObjRef -enabled false
        ixNet commit
    } else {
        set userStatViewObjRef [ixNet add  [ixNet getRoot]/statistics userStatView]
        ixNet commit
        ixNet setAttribute $userStatViewObjRef -viewCaption "UserStatView $sourceType"
        ixNet commit
        set userStatViewObjRef [ixNet remapId $userStatViewObjRef]
    }
    foreach statName $statNameList {
        set stat [ixNet add $userStatViewObjRef stat]
        ixNet setAttribute $stat -statName $statName
        ixNet setAttribute $stat -sourceType $sourceType
        #ixNet setAttribute $stat -aggregationType kNone
        ixNet setAttribute $stat -aggregationType none
        ixNet setAttribute $stat -filterValueList $filterValueList
        ixNet setAttribute $stat -filterName "Port"
        ixNet commit
    }

    ixNet setAttribute $userStatViewObjRef -enabled true
    ixNet commit
    return $userStatViewObjRef
}



########################################################################################
# Procedure: ixTclNet::GetStatValue
#
# Description: Collects current values for the selected statName.
#
# Arguments:
#            sourceType        - Stat source type. That can be obtained from doc or catalog API
#            statName          - Stat name list. They can be obtained from doc or catalog API.
#
#
#
# Returns: Returns the stat values for the configured filters in an array. In the form of
#           StatValueArray($ip,cardId,portId)
########################################################################################


proc GetStatValue {viewCaption statName StatValueArray} {

    upvar $StatValueArray statValueArray
    set statViewList [ixNet getList [ixNet getRoot]/statistics statViewBrowser]
    set statViewObjRef ""
    #puts "$statViewList"
    foreach statView $statViewList {
        if {[ixNet getAttribute $statView -name] == $viewCaption} {
            if {[ixNet getAttribute $statView -enabled] == "false"} {
                ixNet setAttribute $statView -enabled true
                ixNet commit
            }
            set statViewObjRef $statView
            break
        }
    }

    if {[info exists statValueArray]} {
        unset statValueArray
    }

    if {$statViewObjRef == ""} {
        logMsg "Error in getting stat View $viewCaption"
        error "Error in getting stat View $viewCaption"
    }
    after 1000
    set pageNumber 1
    set totalPages [ixNet getAttribute $statViewObjRef -totalPages]
    set currentPage [ixNet getAttribute $statViewObjRef -currentPageNumber]
    set localTotalPages $totalPages

     if {$totalPages > 0 && $currentPage != $pageNumber} {
         ixNet setAttribute $statViewObjRef -currentPageNumber $pageNumber
         ixNet commit
    }

    set continueFlag "true"
    set timeout 5
    while {$continueFlag == "true"} {
        if {[ixNet getAttribute $statViewObjRef -isReady] == true} {
            set rowList [ixNet getList $statViewObjRef row]
            foreach row $rowList {
                set cellList [ixNet getList $row cell]
                foreach cell $cellList {
                    #puts "This is the cell $cell"
                    #puts "Compared values are [ixNet getAttribute $cell -catalogStatName] and $statName"
                    if {[ixNet getAttribute $cell -catalogStatName] == $statName} {

                        set rowName [ixNet getAttribute $cell -rowName]
                        set statValue [ixNet getAttribute $cell -statValue]
                        set splitString [split $rowName /]
                        set hostName [lindex $splitString 0]
                        set card     [string trimleft [lindex $splitString 1] "Card"]
                        set port     [string trimleft [lindex $splitString 2] "Port"]
                        set card [string trimleft $card 0]
                        set port [string trimleft $port 0]
                        set statValueArray($hostName,$card,$port) $statValue
                    }
                }
            }

            set currentPage [ixNet getAttribute $statViewObjRef -currentPageNumber]
            if {$totalPages > 0 && $currentPage < $localTotalPages} {
                incr totalPages -1

                incr pageNumber
                ixNet setAttribute $statViewObjRef -currentPageNumber $pageNumber
                ixNet commit
            } else {
                set continueFlag false
            }
        } else {
            if {$timeout ==0} {
                set continueFlag false
            } else {
                after 1000
                incr timeout -1
            }
        }
    }
    return 0
}


proc PrintArray { StatValueArray} {
     upvar $StatValueArray statValueArray

     foreach {key value} [array get statValueArray] {
        set mystring [format "%-60s = %s" $key $value]
        logMsg $mystring
     }
}



