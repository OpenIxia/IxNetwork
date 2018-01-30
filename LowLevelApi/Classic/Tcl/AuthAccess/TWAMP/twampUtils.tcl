#############################################################################
# Common procs to be used for set & get attr
#############################################################################

proc matchAttributeValue {object attr expectedVal} {
     set noMatch 1
     set val [ixNet getAtt $object -$attr]
     #log "\t (-$attr)$val : $expectedVal (expected)"
     if {[string tolower $val] != [string tolower $expectedVal]} {
          log "\t -$attr : $val (expected $expectedVal) ---> No Match"
          return $noMatch
     }
     set noMatch 0
     log "\t -$attr : $val (expected $expectedVal) --->Match"
    return $noMatch
}

proc checkAttributeValue {object arr} {
    set isError 1
    array set expectProp $arr
    #parray expectProp
    foreach attr [array names expectProp] {
       set attVal [ixNet getAttr $object -$attr]
       set val $expectProp($attr)
       #log "\t attVal = $attVal (-$attr) expectProp = $val"
       if {[string tolower $attVal] != [string tolower $val]} {
           log "\t -$attr : $attVal (expected $val) --> did not match!"
           return $isError
       }
    }
    set isError 0
    return $isError
}

proc setAndCheckAttributeValue {object attr arr} {
    set isError 1
    array set expectProp $arr
    #parray expectProp
    log "Verifying  $attr ..."
    foreach attrVal [array names expectProp] {
        set retVal $expectProp($attrVal)
        catch {ixNet setAttribute $object -$attr $attrVal}
        catch {ixNet commit}
        set retAttrVal [ixNet getAttr $object -$attr]
        log "\t $attr = $retAttrVal ($attrVal :: $retVal)"
        if {(([string tolower $retAttrVal] != [string tolower $attrVal]) && ($retVal == "y")) || \
            (([string tolower $retAttrVal] == [string tolower $attrVal]) && ($retVal == "n"))} {
            log "\t $attr = $retAttrVal ($attrVal :: $retVal) --> Unexpected"
            return $isError
        }
    }
    set isError 0
    return $isError
}


proc addObjectInConfig {parentObj objName objConfigList} {
    set isError 1

    set prevLength [llength [ixNet getList $parentObj $objName]]

    set newObject [ixNet add $parentObj $objName]
    ixNet commit
    foreach {attr attrVal} $objConfigList {
        ixNet setAttr $newObject -$attr $attrVal
    }
    ixNet commit
    set newObject [lindex [ixNet remapIds $newObject] 0]

    set curLength [llength [ixNet getList $parentObj $objName]]
    log "Prev #$objName = $prevLength ~ Current #$objName = $curLength"
    if {$curLength <= $prevLength} {
        return $isError
    }
    set isError 0
    return $isError
}

proc removeObjectInConfig {parentObj objName objMatchList} {
    set isError 1

    set gotTheObjToRemove 0
    set getObjList [ixNet getList $parentObj $objName]
    set prevLength [llength $getObjList]
    foreach getObject $getObjList {
        if {[checkAttributeValue $getObject $objMatchList] == 0} {
            log "Got the $objName in configuration to remove.."
            set gotTheObjToRemove 1
            break
        }
    }

    if {$gotTheObjToRemove == 1} {
        ixNet remove $getObject
        ixNet commit
    } else {
        log "No mathing $objName found in configuration..."
        return $isError
    }

    set curLength [llength [ixNet getList $parentObj $objName]]
    log "Prev #$objName = $prevLength ~ Current #$objName = $curLength"
    if {$curLength >= $prevLength} {
        return $isError
    }
    set isError 0
    return $isError
}


################################################################################
# STATISTICS VERIFICATION
################################################################################

#-------------------------------------------------------------------------------
# PROCEDURE  : checkAllTwampStats
# PURPOSE    :
# PARAMETERS : portList -
#              stat - {name value} Stat list to verify
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkAllTwampStats {viewCaption stat {exactMatch 0}} {
    set isError 1
    set statValue 0
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
    after 1000

    set timeout 10
    while {$timeout > 0} {
        if {[ixNet getAttribute $statViewObjRef -isReady] == true} {
            break
        }
        log "Error: Data is not available."
        after 1000
        incr timeout -1
    }

    if {[ixNet getAttribute $statViewObjRef -isReady] != true} {
        log "Error: Data is not available."
        return $isError
    }

    log "Verifying stats under * $viewCaption *"
    array set statToVerify $stat
    set statNames [array names statToVerify]
    foreach statName $statNames {
        set rowList [ixNet getList $statViewObjRef row]
        foreach row $rowList {
            set cellList [ixNet getList $row cell]
            foreach cell $cellList {
                if {[ixNet getAttribute $cell -catalogStatName] == $statName} {
                    set statValue [ixNet getAttribute $cell -statValue]
                    break
                }
            }
        }
        log "\t $statName Expected: $statToVerify($statName) (Obtained: $statValue)"
        if {$statValue >= $statToVerify($statName)} {
            if {($exactMatch == 1) && ($statValue > $statToVerify($statName))} {
                log "--> MIS Match"
                return $isError
            }
        } else {
            log "--> MIS Match"
            return $isError
        }
    }
    set isError 0
    return $isError
}

################################################################################
# PACKET STRUCTURE VERIFICATION
################################################################################
#-------------------------------------------------------------------------------
# PROCEDURE  : enableAndStartCapture
# PURPOSE    : Enable and Start capture on given ports in argument.
# PARAMETERS : vPorts - List of Vitrual ports on which we have to start capture.
#              args-List of other ports on which we wan to start capture.
#Author      :Darshan T
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail.
#-------------------------------------------------------------------------------


proc enableAndStartCapture {vPorts} {
    # initialize return value
    set PASSED 0
    set FAILED 1

    foreach vPort $vPorts {
        ixNet setAttribute $vPort -rxMode capture
        ixNet setAttribute $vPort/capture -softwareEnabled true
        ixNet setAttribute $vPort/capture -hardwareEnabled true
        ixNet commit
        after 2000
    }

    # capture cleanup
    if {[catch {ixNet exec closeAllTabs} err] == 1} {
        log "Failed to close existing analyser tabs "
    }
    after 2000

    #Start the capture
    log "Start Capturing packets"
    if {[catch {ixNet exec startCapture} err] == 1} {
        log "Failed to start packet capture "
        return $FAILED
    }
    log "Enable and Start Capture Complete Successfully"
    return $PASSED
}

#-------------------------------------------------------------------------------
# PROCEDURE  : verifyCapturedPackets
# PURPOSE    : Verifying expected field value in Captured Packets
# PARAMETERS : chassis -
#              card -
#              port -
#              matchFieldList - list of {startIndex endIndex expectedVal}
#              expPktCnt - {default value 1}
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc verifyCapturedPackets {chassis card port matchFieldList {expPktCnt 1}} {
    set isError 1

    log "Initilizing thorugh IxTclHal...."
    ixInitialize $chassis
    chassis get $chassis
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
    for {set f 1} {$f <= $numCapturedPkts} {incr f} {
        after 50
        set a [captureBuffer getframe $f]
        after 50
        set capframe [captureBuffer cget -frame]
        puts "capframe = $capframe"
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
            set isError 0
            return $isError
        }
    }
    if {$mismatch == 1} {
        log "Not all Field Patterns Matched !!!"
        return $isError
    }
}

#########################################
## Per Session/Per Range Specific Proc ##
#########################################

proc checkVal {attrCap attrVal expVal} {
        set isError 1
        if {$attrVal == $expVal} {
            puts "$attrCap :: val $attrVal <Expected :: val $expVal >  ------Match!!"
        } else {
            puts "$attrCap :: val $attrVal <Expected :: val $expVal >  ------No Match!!"
            return $isError
        }
    }

    proc designL23TrafficPerSession {viewType expectedPerSessionStat} {
    # LAYER23PROTOCOLSTACK
    # create the view
        set isError 1
        set view [ixNet add [ixNet getRoot]statistics view]
        ixNet setAttribute $view -caption "$viewType"
        ixNet setAttribute $view -type layer23ProtocolStack
        ixNet commit
        set view [lindex [ixNet remapIds $view] end]
        # set the filters

        ixNet setAttribute ${view}/layer23ProtocolStackFilter -protocolStackFilterId [list [lindex [ixNet getList ${view} availableProtocolStackFilter] 0]]
        ixNet commit

        # set additional options

        ixNet setAttribute ${view}/layer23ProtocolStackFilter -sortingStatistic [lindex [ixNet getList ${view} statistic] end]
        ixNet setAttribute ${view}/layer23ProtocolStackFilter -sortAscending false
        ixNet setAttribute ${view}/layer23ProtocolStackFilter -numberOfResults 50
        ixNet setAttribute ${view}/layer23ProtocolStackFilter -drilldownType $viewType
        ixNet commit
        # enable the statistics
        foreach {statistic} [ixNet getList $view statistic] {
            puts "Checking Attribute $statistic"
                if {[setAndCheckAttributeValue $statistic enabled [subst {true "y"}]] == 1} {
                return $isError
                }
        }

        # enable the view
        ixNet setAttribute $view -enabled true
        ixNet commit
        # get results
        set rowValuesALL [ixNet getAttribute ${view}/page -rowValues]
        set columnCaptions [ixNet getAttribute ${view}/page -columnCaptions]
        set rowCount [ixNet getAttribute ${view}/page -rowCount]
        set columnCount [ixNet getAttribute ${view}/page -columnCount]
        puts "rowValuesALL :: $rowValuesALL"
        set rowValues [lindex $rowValuesALL 0]
        set expecStatindex 0
        foreach rowValue $rowValues  {
            puts "**********[lindex $rowValue 0]**********"
            set rowVal [lindex $expectedPerSessionStat $expecStatindex]
            set matchStatIndex 0
            for {set capIndex 1} {$capIndex < $columnCount} {} {
                set Val [lindex $rowValue $capIndex]
                set Cap [lindex $columnCaptions $capIndex]
                set match [lindex $rowVal $matchStatIndex]
                    if {$Cap == {Latency [us]}} {
                        if {$Val > $match} {
                            puts "$Cap :: $Val <Expected > $match > ------No Match!!"
                            return $isError
                        } else {
                            puts "$Cap :: $Val <Expected <= $match > ------Match!!"
                        }
                    } else {
                    if {[checkVal $Cap $Val $match] == 1} {
                        return $isError
                    }
                    }
                incr capIndex
                incr matchStatIndex
            }
            incr expecStatindex
        }
    }

###################################
############## END ################
###################################