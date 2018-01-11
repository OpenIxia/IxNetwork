
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

    #Verify filters
    set catalogList [ixNet getList [ixNet getRoot]/statistics catalog]
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
# Procedure: ixTclNet::BrowseStatView
#
# Description: Browse statView with selected caption and store current values in StatValueArray.
#              
# Arguments: 
#            viewCaption       - View caption.
#                                
#        
#                         
# Returns: returns StatValueArray
########################################################################################


proc BrowseStatView {viewCaption StatValueArray} {
    
    upvar $StatValueArray statValueArray
    set statViewList [ixNet getList [ixNet getRoot]/statistics statViewBrowser]
    set statViewObjRef ""
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
        logMsg "Error in getting $viewCaption"
        error "Error in getting $viewCaption"
    }

    
    set timeout 5
    set pageNumber 1
    set totalPages [ixNet getAttribute $statViewObjRef -totalPages]
    set currentPage [ixNet getAttribute $statViewObjRef -currentPageNumber]

    set localTotalPages $totalPages
    set continueFlag "true"
    if {$totalPages > 0 && $currentPage != $pageNumber} {
         ixNet setAttribute $statViewObjRef -currentPageNumber $pageNumber
         ixNet commit
    }
    
    while {$continueFlag == "true"} {
        if {[ixNet getAttribute $statViewObjRef -isReady] == true} {
            set rowList [ixNet getList $statViewObjRef row]
            foreach row $rowList {
                set cellList [ixNet getList $row cell]
                foreach cell $cellList {
					#puts "This is the cell $cell"
                    set colName [ixNet getAttribute $cell -columnName]
                    set rowName [ixNet getAttribute $cell -rowName]
                    set statValue [ixNet getAttribute $cell -statValue]
                    set statValueArray($rowName,$colName) $statValue
                    #I can store it as statName and sourceType.
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


########################################################################################
# Procedure: GetLabelString
#
# Description: Finds Label string for the specified catalog statName.
#              
# Arguments: 
#            viewObjRef       
#            statName          - Stat name list. They can be obtained from doc or catalog API.
#                                
#        
#                         
# Returns: Returns the stat values for the configured filters in an array. In the form of 
#           StatValueArray($ip,cardId,portId)
########################################################################################


proc GetLabelString {viewObjRef catalogStatName} {

    set labelString ""

    if {[ixNet getAttribute $viewObjRef -enabled] == "false"} {
        ixNet setAttribute $viewObjRef -enabled true
        ixNet commit
    }

    if {[ixNet getAttribute $statViewObjRef -isReady] == true} {
        set rowList [ixNet getList $statViewObjRef row]
        #Get the firs row and search the cells.
        set row [lindex $rowList 0]
        set cellList [ixNet getList $row cell]
        foreach cell $cellList {
            if {[ixNet getAttribute $cell -catalogStatName] == $catalogStatName} {
                set labelString [ixNet getAttribute $cell -labelName]
            }
        }
    }
       
    return $labelString
}


###############################################################################
# Procedure: logger::message
#
# Description: This command is used to write messages to the log.
#              Usage is as follows:
#                  log message <-priority 1> "This is my message"
#
###############################################################################
proc message {args} \
{
    set ioHandle stdout
    set argLen [llength $args]
    set type   logger

    if {[lindex $args 0] == "-nonewline"} {
        set args [lreplace $args 0 0]

        catch {puts -nonewline $ioHandle [join $args " "]}

    } else {
        catch {puts $ioHandle [join $args " "]}
    }

    flush $ioHandle

    # required not only for flushing the stdout, but also to flush anything from the
    # open socket connections  (should probably revisit the socket code later)
    update
}



########################################################################
# Procedure: logMsg
#
# Description: This command wraps the logger command logger message
#
# Arguments: args - a list of valid arguments
#
# Results: Returns 0 for ok and 1 for error.  WARNING: Cannot use TCL_OK
#          and TCL_ERROR at this point.  It was failing on certain unix
#          and linux combinations
########################################################################
proc logMsg {args} \
{
    set retCode 0
    if {[lindex $args 0] == "-nonewline"} {
        set args [lreplace $args 0 0]
        if {[catch {eval message -nonewline $args} err]} {
            set retCode 1
        }
    } else {
        if {[catch {eval message $args} err]} {
            set retCode 1
        }
    }
    return $retCode
}

########################################################################################
# Procedure: GetTrafficStatValue 
#
# Description: Collects current values for the selected statName.
#              
# Arguments: 
#            viewCaption        - view caption.
#            statName          - Stat name list. They can be obtained from doc or catalog API.
#                                
#        
#                         
# Returns: Returns the stat values for the configured filters in an array. In the form of 
#           StatValueArray($rowObjRef)
########################################################################################


proc GetTrafficStatValue {viewCaption statName StatValueArray} {
    
    upvar $StatValueArray statValueArray
    set statViewList [ixNet getList [ixNet getRoot]/statistics statViewBrowser]
    set viewObjRef ""
    foreach statView $statViewList {
        if {[ixNet getAttribute $statView -name] == $viewCaption} {
            if {[ixNet getAttribute $statView -enabled] == "false"} {
                ixNet setAttribute $statView -enabled true
                ixNet commit
            }
            set viewObjRef $statView
            break
        }
    }
   
   
    if {[info exists statValueArray]} {
        unset statValueArray
    } 

    if {$viewObjRef == ""} {
        logMsg "Error in getting view $viewCaption"
        error "Error in getting view $viewCaption"
    }
    after 1000
    set pageNumber 1
    set totalPages [ixNet getAttribute $viewObjRef -totalPages]
    set currentPage [ixNet getAttribute $viewObjRef -currentPageNumber]
    set localTotalPages $totalPages

     if {$totalPages > 0 && $currentPage != $pageNumber} {
         ixNet setAttribute $viewObjRef -currentPageNumber $pageNumber
         ixNet commit
    }

    set timeout 5
    set continueFlag "true"
    while {$continueFlag == "true"} {
        if {[ixNet getAttribute $viewObjRef -isReady] == true} {
            set rowList [ixNet getList $viewObjRef row]
            foreach row $rowList {
                set cellList [ixNet getList $row cell]
                foreach cell $cellList {
                    if {[ixNet getAttribute $cell -catalogStatName] == $statName} {
                        set colName [ixNet getAttribute $cell -columnName]
                        set statValue [ixNet getAttribute $cell -statValue]
                        set statValueArray($row) $statValue
                    }
                }
            }

            set currentPage [ixNet getAttribute $viewObjRef -currentPageNumber]
            if {$totalPages > 0 && $currentPage < $localTotalPages} {
                incr totalPages -1
    
                incr pageNumber
                ixNet setAttribute $viewObjRef -currentPageNumber $pageNumber
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
}     
