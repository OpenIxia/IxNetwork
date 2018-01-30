#############################################################################
# Common procs to be used for set & get attr
#############################################################################

#------------------------------------------------------------------------------
# PROCEDURE    : removePortList
# PURPOSR      : To clean up all the virtual ports from the IxNetwork GUI
# INPUT        : The list of virtual ports to be removed
# OUTPUT       : Removes all the virtual ports from the IxNetwork GUI
# RETURN VALUE : void
#------------------------------------------------------------------------------
proc removePortList {portList} {
    set len [llength $portList]
    set i 0
    while { $i < $len } {
        set port [lindex $portList $i]
        ixNet remove $port
        ixNet commit
        incr i
    }
}


#------------------------------------------------------------------------------
# PROCEDURE    : ixNetCleanUp
# PURPOSR      : Cleaning up, stop all protocols if running, close alnalyzer
#                tabs if open, stop test configuration etc.
# INPUT        : void
# OUTPUT       : Cleans up all configurations from IxNetwork GUI
# RETURN VALUE : void
# ASSUMPTION   : we are in the "connected" with the IxNetwork GUI
#------------------------------------------------------------------------------
proc ixNetCleanUp {} {

    # if protocols are not stopped handle it from here
    catch {ixNet exec stopAllProtocols}

    # Clean all tabs
    catch {ixNet exec closeAllTabs}

    # Stop integrated if running
    catch {
         #stop test configuration if it is running
         catch {ixNet exec stopTestConfiguration}

         while { [regexp [ixNet getAtt [ixNet getRoot]/testConfiguration \
               -testRunning] true ] } {
               after 20000
          }
    };  # stopp !!!!

    # Remove port
    ixTclNet::UnassignPorts [ixNet getList [::ixNet getRoot] vport]
    removePortList [ixNet getList [::ixNet getRoot] vport]

    # clean
    catch {ixNet execute newConfig}
}


#------------------------------------------------------------------------------
# PROCEDURE    : getPortList
# PURPOSR      : connecting to IxNetworl client
# INPUT        : [list $chassis1 $card1 $port1 $client1 $tcpPort1] and
#                [list $chassis2 $card2 $port2 $client2 $tcpPort2]
# OUTPUT       : Connects to IxNetwork Tcl server and chassis
# RETURN VALUE : list of virtual ports
#------------------------------------------------------------------------------
proc getPortList {portData1 portData2} {

    # get port info 1
    set chassisIp1 [lindex $portData1 0]
    set card1      [lindex $portData1 1]
    set port1      [lindex $portData1 2]
    set hostName1  [lindex $portData1 3]
    set tcpPort1   [lindex $portData1 4]

    # get port info 2
    set chassisIp2 [lindex $portData2 0]
    set card2      [lindex $portData2 1]
    set port2      [lindex $portData2 2]
    set hostName2  [lindex $portData2 3]
    set tcpPort2   [lindex $portData2 4]

    set portList [list [list $chassisIp1 $card1 $port1] \
                       [list $chassisIp2 $card2 $port2] ]

    if {[catch {ixNet connect $hostName1 -port $tcpPort1} result]} {
        puts "error in connect: $result"
        set iter 1
        while {$iter <= 3} {
            after 1000
            if {[catch {ixNet connect $hostName1 -port $tcpPort1} \
                result]} {
                puts "error on connect retry $iter: $result"
            } else {
                puts "successful connect on retry $iter"
                break
            }
            incr iter
        }
    }

    # after connecting cleaning up the network
    ixNetCleanUp

    ixTclNet::AssignPorts $portList
    set vPortList [ixNet getList [::ixNet getRoot] vport]
    return $vPortList
}

proc matchAttributeValue {object attr expectedVal} {
     set noMatch 1
     set val [ixNet getAtt $object -$attr]
     #puts "\t (-$attr)$val : $expectedVal (expected)"
     if {[string tolower $val] != [string tolower $expectedVal]} {
          #puts "\t -$attr : $val (expected $expectedVal) ---> No Match"
          return $noMatch
     }
     set noMatch 0
     return $noMatch
}

proc checkAttributeValue {object arr} {
    set isError 1
    array set expectProp $arr
    #parray expectProp
    foreach attr [array names expectProp] {
       set attVal [ixNet getAttr $object -$attr]
       set val $expectProp($attr)
       #puts "\t attVal = $attVal (-$attr) expectProp = $val"
       if {[string tolower $attVal] != [string tolower $val]} {
           #puts "\t -$attr : $attVal (expected $val) --> did not match!"
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
    #puts "Verifying  $attr ..."
    foreach attrVal [array names expectProp] {
        set retVal $expectProp($attrVal)
        catch {ixNet setAttr $object -$attr $attrVal}
        ixNet commit
        set retAttrVal [ixNet getAttr $object -$attr]
        #puts "\t $attr = $retAttrVal ($attrVal :: $retVal)"
        if {(([string tolower $retAttrVal] != [string tolower $attrVal]) && ($retVal == "y")) || \
            (([string tolower $retAttrVal] == [string tolower $attrVal]) && ($retVal == "n"))} {
            #puts "\t $attr = $retAttrVal ($attrVal :: $retVal) --> Unexpected"
            return $isError
        }
    }
    set isError 0
    return $isError
}

proc getCciInmSec {cci} {
    if {$cci == "100msec"} {
        return 100
    }
    if {$cci == "10min"} {
        return 600000
    }
    if {$cci == "10msec"} {
        return 10
    }
    if {$cci == "10sec"} {
        return 10000
    }
    if {$cci == "1min"} {
        return 60000
    }
    if {$cci == "3.33msec"} {
        return 4
    }
    if {$cci == "1sec"} {
        return 1000
    }
    return -1
}

#############################################################################
# Common procs to be used for set & get attr
#############################################################################
proc matchAttributeValue {object attr expectedVal} {
     set noMatch 1
     set val [ixNet getAtt $object -$attr]
     #puts "\t (-$attr)$val : $expectedVal (expected)"
     if {[string tolower $val] != [string tolower $expectedVal]} {
          puts "\t -$attr : $val (expected $expectedVal) ---> No Match"
          return $noMatch
     }
     set noMatch 0
     puts "\t -$attr : $val (expected $expectedVal) --->Match"
    return $noMatch
}

proc checkAttributeValue {object arr} {
    set isError 1
    array set expectProp $arr
    #parray expectProp
    foreach attr [array names expectProp] {
       set attVal [ixNet getAttr $object -$attr]
       set val $expectProp($attr)
       #puts "\t attVal = $attVal (-$attr) expectProp = $val"
       if {[string tolower $attVal] != [string tolower $val]} {
           puts "\t -$attr : $attVal (expected $val) --> did not match!"
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
    puts "Verifying  $attr ..."
    foreach attrVal [array names expectProp] {
        set retVal $expectProp($attrVal)
        catch {ixNet setAttribute $object -$attr $attrVal}
        ixNet commit
        set retAttrVal [ixNet getAttr $object -$attr]
        puts "\t $attr = $retAttrVal ($attrVal :: $retVal)"
        if {(([string tolower $retAttrVal] != [string tolower $attrVal]) && \
            ($retVal == "y"))                                            || \
            (([string tolower $retAttrVal] == [string tolower $attrVal]) && \
            ($retVal == "n"))} {
            puts "\t $attr = $retAttrVal ($attrVal :: $retVal) --> Unexpected"
            return $isError
        }
    }
    set isError 0
    return $isError
}

proc getCciInmSec {cci} {
    if {$cci == "100msec"} {
        return 100
    }
    if {$cci == "10min"} {
        return 600000
    }
    if {$cci == "10msec"} {
        return 10
    }
    if {$cci == "10sec"} {
        return 10000
    }
    if {$cci == "1min"} {
        return 60000
    }
    if {$cci == "3.33msec"} {
        return 4
    }
    if {$cci == "1sec"} {
        return 1000
    }
    return -1
}

#############################################################################
# PBT operations
#############################################################################

#-------------------------------------------------------------------------------
# PROCEDURE  : enableDisablePbtTrunk
# PURPOSE    : Enable/Disable Pbt Trunk following specification
# PARAMETERS :
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc enableDisablePbtTrunk {bridge en_disen conditionList} {
    set isError 1
    set trunkList [ixNet getList $bridge trunk]
    set numTrunks [llength $trunkList]
    for {set x 0} {$x < $numTrunks} {incr x} {
        set trunk [lindex $trunkList $x]
        if {[checkAttributeValue $trunk $conditionList] == 0} {
            # enable/disable the trunk
            if {[setAndCheckAttributeValue $trunk "enabled" \
                    [list $en_disen y]] == 1} {
                return $isError
            }
            set isError 0
            return $isError
        }
    }
    return $isError
}

#-------------------------------------------------------------------------------
# PROCEDURE  : getCciForPbtTrunk
# PURPOSE    : returns configured CCI for Pbt Trunk following specification
# PARAMETERS :
# RETURN     : string - configured CCI
#-------------------------------------------------------------------------------
proc getCciForPbtTrunk {bridge conditionList} {
    set cci 0
    set trunkList [ixNet getList $bridge trunk]
    set numTrunks [llength $trunkList]
    for {set x 0} {$x < $numTrunks} {incr x} {
        set trunk [lindex $trunkList $x]
        if {[checkAttributeValue $trunk $conditionList] == 0} {
            set cci [getCciInmSec [ixNet getAttr $trunk -cciInterval]]
            return $cci
        }
    }
    return $cci
}

#-------------------------------------------------------------------------------
# PROCEDURE  : checkPbtDelayLearnedInfo
# PURPOSE    :
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkPbtDelayLearnedInfo {bridge filterList checkList {timeout 5000}} {
    set isError 1

    # Below veriable is for debug puts only
    array set filterListArray $filterList
    puts "Setting Pbt Delay filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $bridge $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }

    # set userLearnedInfoTimeOut
    if {[setAndCheckAttributeValue $bridge "userLearnedInfoTimeOut" \
        [list $timeout y]] == 1} {
        return $isError
    }

    after 5000

    # Refresh Pbt LB learnt Info
    set status [ixNet exec startDelayMeasurement $bridge]

    set count 0
    set maxCount [expr [expr $timeout / 1000] + 10] ;# timeout + 10 sec
    set isComplete false
    puts "Retrieving Pbt Delay info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPbbTeDelayLearnedInfoRefreshed]
        puts "isComplete ---> $isComplete"
        after 1000
        incr count
        if { $count > $maxCount } {
            puts "Failed to retrieve Pbt Delay info, \
                  [ixNet getAttr $bridge -pbbTeDelayLearnedErrorString]"
            return $isError
        }
    }
    puts "Pbt Delay info refreshed ..."

    # Check Pbt Delay pkt sent
    if {[matchAttributeValue $bridge "isPbbTeDelayLearnedPacketSent" "True"] == 1} {
        puts "No Pbt Delay pkt sent, [ixNet getAttr $bridge \
              -pbbTeDelayLearnedErrorString]"
        return $isError
    }
    puts "PbbTe Delay pkt sent ... "

    set delayInfo      [lindex [ixNet getList $bridge pbbTeDelayLearnedInfo] 0]
    set delayInSec     [ixNet getAttr $delayInfo -valueInSec]
    set delayInNanoSec [ixNet getAttr $delayInfo -valueInNanoSec]
    
    puts "Pbt LB Learned ConfigMep ? :                         \
         [ixNet getAttr $bridge -isPbbTeDelayLearnedConfigMep] \
         (valueInSec : $delayInSec, valueInNanoSec : $delayInNanoSec)"

    # CheckList Map (reference only veriable)
    set checkListMap {isPbbTeDelayLearnedConfigMep \
                       tolerence                   \
                       valueInSec                  \
                       valueInNanoSec}

    set configMep [lindex $checkList 0]
    if {[matchAttributeValue $bridge "isPbbTeDelayLearnedConfigMep" $configMep] == 1} {
         return $isError
    }

    # Check case with unconfigured MEP
    if {[string tolower $configMep] == "false"} {
        if {($delayInSec != 0) || ($delayInNanoSec != 0)} {
            return $isError
        }
        set isError 0
        return $isError
    } else {
        if {($delayInSec != 0) && ($delayInNanoSec != 0)} {
            return $isError
        }
        set isError 0
        return $isError
    }

    # Now only configured MEP case left
    set matchTol [lindex $checkList 1]
    if {($matchTol > 100) || ($matchTol < -1)} {
         # Wrong user input, setting it to -1
         set matchTol -1
    }
    # Match tolerence -1, Just check for delay > 0 no specific value
    if {($matchTol == -1) && ($delayInSec == 0) && ($delayInNanoSec == 0)} {
        return $isError
    }
    # Match tolerence <0 - 100>
    if {($matchTol >= 0) && ($matchTol <= 100)} {
        set expectedDelayInSec [lindex $checkList 2]
        
        set min [expr $expectedDelayInSec - [expr \
                [expr double($matchTol) / 100] * $expectedDelayInSec]]
        
        set max [expr $expectedDelayInSec + [expr \
                [expr double($matchTol) / 100] * $expectedDelayInSec]]

        puts "expectedDelayInSec : $expectedDelayInSec , delayInSec : $delayInSec"
        if {($delayInSec < $min) || ($delayInSec > $max)} {
            return $isError
        }

        set expectedDelayInNanoSec [lindex $checkList 3]
        set min [expr $expectedDelayInNanoSec - [expr \
                [expr double($matchTol) / 100] * $expectedDelayInNanoSec]]
                
        set max [expr $expectedDelayInNanoSec + [expr \
                [expr double($matchTol) / 100] * $expectedDelayInNanoSec]]

        puts "< $min - $max >"
        puts "expectedDelayInNanoSec : $expectedDelayInNanoSec , \
              delayInNanoSec : $delayInNanoSec]"
        
        if {($delayInNanoSec < $min) || ($delayInNanoSec > $max)} {
            return $isError
        }
    }
    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : checkPbtLbLearnedInfo
# PURPOSE    :
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in
#                          learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkPbtLbLearnedInfo {bridge filterList checkList {configMep "true"} \
                {transactionId 0} {timeout 5000} } {

    set isError 1

    # Below veriable is for debug puts only
    array set filterListArray $filterList
    puts "Setting Pbt LB filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $bridge $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }

    # set userLearnedInfoTimeOut
    if {[setAndCheckAttributeValue $bridge "userLearnedInfoTimeOut" \
        [list $timeout y]] == 1} {
        return $isError
    }

    # Check case with unconfigured MEP
    if {([string tolower $configMep] == "false") && ($transactionId != 0)} {
        if {[setAndCheckAttributeValue $bridge "userTransactionId" \
            [list $transactionId y]] == 1} {
            return $isError
        }
    }
    after 5000

    # Refresh Pbt LB learnt Info
    set status [ixNet exec startLoopback $bridge]

    set count 0
    set maxCount [expr [expr $timeout / 1000] + 10] ;# timeout + 10 sec
    set isComplete false
    puts "Retrieving Pbt LB learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPbbTeLbLearnedInfoRefreshed]
        puts "isComplete ---> $isComplete"
        after 1000
        
        incr count
        if { $count > $maxCount } {
            puts "Failed to retrieve Pbt LB learnt info, \
                  [ixNet getAttr $bridge -pbbTeLbLearnedErrorString]"
            return $isError
        }
    }
    puts "Pbt Lb learnt info refreshed ..."

    # Attr list to match
    set db {bVlan         \
            mdLevel       \
            srcMacAddress \
            dstMacAddress \
            reachability}

    # Check Pbt LB pkt sent
    if {[matchAttributeValue $bridge "isPbbTeLbLearnedPacketSent" "True"] == 1} {
        puts "No Pbt LB pkt sent, [ixNet getAttr \
             $bridge -pbbTeLbLearnedErrorString]"
        return $isError
    }

    set lbLearnedInfoList [ixNet getList $bridge pbbTeLbLearnedInfo]

    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0
    foreach $db $checkList {
        incr numInfoInCheckList
        foreach lbInfo $lbLearnedInfoList {
            set misMatch 0
            foreach attr $db {
                set attrVal [set [set attr]]
                if {[matchAttributeValue $lbInfo $attr $attrVal] == 1} {
                     set misMatch 1
                     break
                }
            } ;# end foreach attr $db
            
            if {$misMatch == 0} {
                # Check case with unconfigured MEP
                if {([string tolower $configMep] == "false") && ($transactionId != 0)} {
                    if {[matchAttributeValue $lbInfo "transactionId" $transactionId] == 1} {
                        continue
                    }
                }
                puts "Pbt LB Learned ConfigMep ? : \
                     [ixNet getAttr $bridge -isPbbTeLbLearnedConfigMep] \
                     (reachability : [ixNet getAttr $lbInfo -reachability], \
                     rtt : [ixNet getAttr $lbInfo -rtt])"
                # Reached here -> all field match found in learnt info
                incr isFound
                break
            }
        } ;# end foreach lbInfo $lbLearnedInfoList
    } ;# foreach $db $checkList
    
    puts "Among all $numInfoInCheckList info $isFound are \
          present in PBT LB Learnt Info List"
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}

#-------------------------------------------------------------------------------
# PROCEDURE  : checkCfmPbtCcmLearnedInfo
# PURPOSE    :
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in
#                          learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkCfmPbtCcmLearnedInfo {bridge checkCcmList} {

    set isError 1
    set status [ixNet exec refreshCcmLearnedInfo $bridge]

    set count 0
    set isComplete false
    puts "Retrieving Pbt Ccm learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPbbTeCcmLearnedInfoRefreshed]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 60 } {
            puts "Failed to retrieve Pbt Ccm learnt info ..."
            return $isError
        }
    }

    puts "Pbt Ccm learnt info refreshed ..."

    # PBT CCM Db
    set db {bVlan                  \
            remoteMacAddress       \
            srcMacAddress          \
            shortMaNameFormat      \
            shortMaName            \
            remoteMepId            \
            srcMepId               \
            mdLevel                \
            mdNameFormat           \
            mdName                 \
            receivedRdi            \
            receivedPortTlvDefect  \
            receivedIfaceTlvDefect \
            errCcmDefect           \
            rmepCcmDefect          \
            outOfSequenceCcmCount  \
            cciInterval            \
            errCcmDefectCount      \
            portTlvDefectCount     \
            ifaceTlvDefectCount    \
            remoteMepDefectCount }

    # Get CCM Learned Info List
    set ccmLearnedInfoList [ixNet getList $bridge pbbTeCcmLearnedInfo]
    puts " length of ccmLearnedInfoList [llength $ccmLearnedInfoList]"
    if {[llength $ccmLearnedInfoList] == 0} {
        puts "No CCM learnt info present in database ... "
        return $isError
    }
    
    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0
    foreach checkList $checkCcmList {
        foreach $db $checkList {
            incr numInfoInCheckList
            puts " -----------------------------"
            puts "Browsing CCM learntinfo list ..."
            foreach ccmInfo $ccmLearnedInfoList {
                set misMatch 0
                foreach attr $db {
                    set attrVal [set [set attr]]
                    if {[matchAttributeValue $ccmInfo $attr $attrVal] == 1} {
                        set misMatch 1
                        break
                    }
                }

                if {$misMatch == 0} {
                    # Reached here -> all field match found in learnt info
                    puts "Expected learntinfo present in CCM learntinfo list "
                    puts " ----------------------------- "
                    incr isFound
                    break
                }
            }
        }
    }

    puts "Among all $numInfoInCheckList info $isFound are \
          present in CCM Learnt Info List"
    
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}

################################################################################
# STATISTICS VERIFICATION
################################################################################
#-------------------------------------------------------------------------------
# PROCEDURE  : checkAllCfmStats
# PURPOSE    :
# PARAMETERS : portList -
#              stat - {name value} Stat list to verify
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkAllCfmStats {portList stat {exactMatch 0}} {
    set sessFoundFlag 0
    set userViewList [ixNet getList [ixNet getRoot]/statistics userStatView]
    foreach view $userViewList {
        ixNet remove $view
        ixNet commit
    }

    set userStatView [SetupUserStats $portList "CFM" "*"]
    set timeout 20
    set doneList $portList

    array set statToVerify $stat
    set statNames [array names statToVerify]


    set returnFlag 1
    #Checking the stats.."
    set contFlag 0
    puts [format "%-32s %10s\t%10s" "STAT NAME" "EXPECTED" "OBTAINED"]

    foreach eachStat $statNames {
        GetStatValue "UserStatView CFM" "$eachStat" statValueArray1
        if {[lindex [array get statValueArray1] 1] >= $statToVerify($eachStat)} {
            PrintArray statValueArray1
            puts [format "%-32s %10d\t%10d" $eachStat $statToVerify($eachStat) \
                 [lindex [array get statValueArray1] 1]]
            if {($exactMatch == 1) && [lindex [array get statValueArray1] 1] != \
                $statToVerify($eachStat)} {
                return 1
            }
        } else {
            PrintArray statValueArray1
            puts [format "%-32s %10d\t%10d --> MIS Match" $eachStat \
                 $statToVerify($eachStat) [lindex [array get statValueArray1] 1]]
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

    if {$returnFlag == 1} {
        return 0
    } else {
        return 1
    }
    after 2000
}

#-------------------------------------------------------------------------------
# PROCEDURE  : checkAllProtocolStats
# PURPOSE    :
# PARAMETERS : portList -
#              stat - {name value} Stat list to verify
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkAllProtocolStats {portList protocol stat {exactMatch 0}} {
    set sessFoundFlag 0
    set userViewList [ixNet getList [ixNet getRoot]/statistics userStatView]
    foreach view $userViewList {
        ixNet remove $view
        ixNet commit
    }

    set userStatView [SetupUserStats $portList $protocol "*"]
    set timeout 20
    set doneList $portList

    array set statToVerify $stat
    set statNames [array names statToVerify]


    set returnFlag 1
    #Checking the stats.."
    set contFlag 0
    puts "eachStat $statNames"
    foreach eachStat $statNames {
        GetStatValue "UserStatView $protocol" "$eachStat" statValueArray1
        if {[lindex [array get statValueArray1] 1] >= $statToVerify($eachStat)} {
            PrintArray statValueArray1
            puts [format "%-32s %10d\t%10d" $eachStat $statToVerify($eachStat) \
                 [lindex [array get statValueArray1] 1]]
            if {($exactMatch == 1) && [lindex [array get statValueArray1] 1] != \
                        $statToVerify($eachStat)} {
                return 1
            }
       } else {
            PrintArray statValueArray1
            puts [format "%-32s %10d\t%10d --> MIS Match" $eachStat \
                 $statToVerify($eachStat) [lindex [array get statValueArray1] 1]]
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
            
            if {[llength $doneList] == 0} {
                set contFlag 1
                break
            } else {
                incr timeout -1
                after 1000
            }
        } ;# foreach portItem $doneList
    } ;# foreach eachStat $statNames

    if {$contFlag == 0} {
        logMsg "Error... Check the configuration"
        return 1
    }

    if {$returnFlag == 1} {
        return 0
    } else {
        return 1
    }
    after 2000
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
        puts "Failed to close existing analyser tabs "
    }
    after 2000

    #Start the capture
    puts "Start Capturing packets"
    if {[catch {ixNet exec startCapture} err] == 1} {
        puts "Failed to start packet capture "
        return $FAILED
    }
    puts "Enable and Start Capture Complete Successfully"
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

    puts "Initilizing thorugh IxTclHal...."
    ixInitialize $chassis
    chassis get  $chassis
    set chassisId [chassis cget -id]

    port get $chassisId $card $port
    set loginName [port cget -owner]
    ixLogin $loginName
    puts "Logging in using the $loginName"

    # Retrive captured packets
    captureBuffer get $chassisId $card $port

    set numCapturedPkts [captureBuffer cget -numFrames]
    puts "Captured $numCapturedPkts pkts (expected: $expPktCnt)"
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
            puts "Obtained: [lrange $capframe $startIndex $endIndex] \
                  Expected: $expectedVal"
            
            if {[lrange $capframe $startIndex $endIndex] != $expectedVal} {
                set mismatch 1
                puts "Obtained: [lrange $capframe $startIndex $endIndex] \
                      Expected: $expectedVal ---> No Match"
                break
            }
        }
        if {$mismatch == 0} {
            puts "All Field Patterns Matched !!!"
            set isError 0
            return $isError
        }
    }

    if {$mismatch == 1} {
        puts "Not all Field Patterns Matched !!!"
        return $isError
    }
}

########################################################################################
#                UTIL FOR MAC RANGE CONFIGURATION
########################################################################################
proc getNextMacAddress {lastMacAddressUsed {incrStep 1} {maxBytePosToIncrement 1}} {
    set splitAnMacAddress [split $lastMacAddressUsed ":"]
    for {set i 0} {$i < 6} {incr i} {
        set position [expr $i +1]
        set MacDigit$position [format "%i" 0x[lindex $splitAnMacAddress $i]]
    }

    set posToIncr -1
    incr MacDigit6 +$incrStep
    if {$MacDigit6 > 255} {
        set MacDigit6 $incrStep
        for {set j 5} {$j >= $maxBytePosToIncrement } {incr j -1} {
            set MacDigit [set MacDigit$j]
            if {$MacDigit < 255} {
                set posToIncr $j
                incr MacDigit
                set MacDigit$j $MacDigit
                break
            } else {
                set MacDigit$j 0
            }
        }
    } else {
        set posToIncr 6
    }

    if {$posToIncr == -1} {
        error "Crossing the configurable MAC range Limit from this Harness. \
              Reduce configuration & Try !!!"
    }

    for {set j 1} {$j <= 6} {incr j} {
        set MacDigit [set MacDigit$j]
        set MacDigit$j [format "%0.2x" $MacDigit]
    }
    lappend macAddr $MacDigit1:$MacDigit2:$MacDigit3:$MacDigit4:$MacDigit5:$MacDigit6
    return $macAddr
}


###########################################################################################
###                         PROCs for Periodic OAM
###########################################################################################
#-------------------------------------------------------------------------------
# PROCEDURE  : checkPbbtePeriodicOAMLTLearnedInfo
# PURPOSE    : Verifying pbbte Periodic OAM LT Learned Info
# PARAMETERS :
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkPbbtePeriodicOAMLTLearnedInfo {bridge checkList} {
    set isError 1

    if {[setAndCheckAttributeValue $bridge "userPeriodicOamType" \
         {"linkTrace" y}] == 1} {
         return $isError
    }

    # Refresh PBBTE Periodic OAM LT learnt Info
    ixNet exec updatePeriodicOamLearnedInfo $bridge

    set count 0
    set isComplete false
    puts "Retrieving Pbbte Periodic OAM Lt learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPeriodicOamLearnedInfoRefreshed]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 60 } {
            puts "Failed to retrieve Pbbte Periodic OAM Lt learnt info, \
                [ixNet getAttr $bridge -isPeriodicOamLearnedInfoRefreshed]"
            return $isError
        }
    }
    puts "Pbbte Periodic OAM Lt learnt info refreshed ..."

    # Return if no verification needed, we did passed empty match list
    if {$checkList == ""} {
        puts "returning as no verification needed..."
        set isError 0
        return $isError
    }

    # CFM LT Db
    set db {averageHopCount    \
            bVlan              \
            completeReplyCount \
            dstMacAddress      \
            ltmSentCount       \
            mdLevel            \
            noReplyCount       \
            partialReplyCount  \
            recentHopCount     \
            recentHops         \
            recentReplyStatus  \
            srcMacAddress}

    # Get LT Learned Info List
    after 5000
    set ltLearnedInfoList [ixNet getList $bridge \
            pbbTePeriodicOamLtLearnedInfo]

    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0

    foreach val $checkList {
        foreach $db $val {
            incr numInfoInCheckList
            puts " -----------------------------"
            puts "Browsing Cfm Lt learntinfo list ..."
            foreach ltInfo $ltLearnedInfoList {
                set misMatch 0
                foreach attr $db {
                    set attrVal [set [set attr]]
                    if {[matchAttributeValue $ltInfo $attr $attrVal] == 1} {
                         set misMatch 1
                         break
                    }
                }

                if {$misMatch == 0} {
                    # Reached here -> all field match found in learnt info
                    puts "Expected learntinfo present in PBBTE Link Trace \
                         learntinfo list ..."
                    puts " ----------------------------- "
                    incr isFound
                    break
                }
            }
        }
    }

    puts "Among all $numInfoInCheckList info $isFound are present in \
            Link Trace Learnt Info List"
    
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : checkPbbtePeriodicOAMLBLearnedInfo
# PURPOSE    : Verifying pbbte Periodic OAM LB Learned Info
# PARAMETERS :
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc checkPbbtePeriodicOAMLBLearnedInfo {bridge checkList} {
    set isError 1

    if {[setAndCheckAttributeValue $bridge "userPeriodicOamType" \
        {"loopback" y}] == 1} {
        return $isError
    }

    # Refresh PBBTE Periodic OAM LT learnt Info
    ixNet exec updatePeriodicOamLearnedInfo $bridge

    set count 0
    set isComplete false
    puts "Retrieving Pbbte Periodic OAM Lb learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPeriodicOamLearnedInfoRefreshed]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 60 } {
            puts "Failed to retrieve Pbbte Periodic OAM Lb learnt info, \
                 [ixNet getAttr $bridge -isPeriodicOamLearnedInfoRefreshed]"
            return $isError
        }
    }
    puts "Pbbte Periodic OAM Lb learnt info refreshed ..."

    # Return if no verification needed, we did passed empty match list
    if {$checkList == ""} {
        puts "returning as no verification needed..."
        set isError 0
        return $isError
    }

    # CFM LB Db
    set db {bVlan              \
            dstMacAddress      \
            lbmSentCount       \
            mdLevel            \
            noReplyCount       \
            recentReachability \
            srcMacAddress}

    # Get LB Learned Info List
    after 5000
    set lbLearnedInfoList [ixNet getList $bridge \
            pbbTePeriodicOamLbLearnedInfo]

    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0

    foreach val $checkList {
        foreach $db $val {
            incr numInfoInCheckList
            puts " -----------------------------"
            puts "Browsing PBBTE Lb learntinfo list ..."
            foreach lbInfo $lbLearnedInfoList {
                set misMatch 0
                foreach attr $db {
                    set attrVal [set [set attr]]
                    if {[matchAttributeValue $lbInfo $attr $attrVal] == 1} {
                         set misMatch 1
                         break
                    }
                }
                if {$misMatch == 0} {
                    puts "averageRtt: [ixNet getAttr $lbInfo -averageRtt] \
                        recentRtt: [ixNet getAttr $lbInfo -recentRtt]"
                    # Reached here -> all field match found in learnt info
                    puts "Expected learntinfo present in PBBTE Link Trace \
                          learntinfo list ..."
                    puts " ----------------------------- "
                    incr isFound
                    break
                }
            }
        }
    }

    puts "Among all $numInfoInCheckList info $isFound are present in Link \
          Trace Learnt Info List"
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : checkPbbtePeriodicOAMDMLearnedInfo
# PURPOSE    : Verifying pbbte Periodic OAM DM Learned Info
# PARAMETERS :
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkPbbtePeriodicOAMDMLearnedInfo {bridge checkList} {
    set isError 1

    if {[setAndCheckAttributeValue $bridge "userPeriodicOamType" \
            {"delayMeasurement" y}] == 1} {
        return $isError
    }

    # Refresh PBBTE Periodic OAM DM learnt Info
    ixNet exec updatePeriodicOamLearnedInfo $bridge

    set count 0
    set isComplete false
    puts "Retrieving Pbbte Periodic OAM Dm learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPeriodicOamLearnedInfoRefreshed]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 60 } {
            puts "Failed to retrieve Pbbte Periodic OAM Dm learnt info, \
                [ixNet getAttr $bridge -isPeriodicOamLearnedInfoRefreshed]"
            return $isError
        }
    }
    puts "Pbbte Periodic OAM Dm learnt info refreshed ..."

    # Return if no verification needed, we did passed empty match list
    if {$checkList == ""} {
        puts "returning as no verification needed..."
        set isError 0
        return $isError
    }

    # CFM DM Db
    set db {bVlan         \
            dmmCountSent  \
            dstMacAddress \
            mdLevel       \
            noReplyCount  \
            srcMacAddress}


    # Get DM Learned Info List
    after 5000
    set dmLearnedInfoList [ixNet getList $bridge pbbTePeriodicOamDmLearnedInfo]

    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0

    foreach val $checkList {
        foreach $db $val {
            incr numInfoInCheckList
            puts " -----------------------------"
            puts "Browsing Cfm Dm learntinfo list ..."
            foreach dmInfo $dmLearnedInfoList {
                set misMatch 0
                foreach attr $db {
                    set attrVal [set [set attr]]
                    if {[matchAttributeValue $dmInfo $attr $attrVal] == 1} {
                         set misMatch 1
                         break
                    }
                }
                if {$misMatch == 0} {
                    puts "averageDelaySec: [ixNet getAttr $dmInfo -averageDelaySec]        \
                         averageDelayNanoSec: [ixNet getAttr $dmInfo -averageDelayNanoSec] \
                        recentDelaySec: [ixNet getAttr $dmInfo -recentDelaySec]            \
                        recentDelayNanoSec: [ixNet getAttr $dmInfo -recentDelayNanoSec] "

                    if {([ixNet getAttr $dmInfo -averageDelaySec] == 0 &&     \
                        [ixNet getAttr $dmInfo -averageDelayNanoSec] == 0) || \
                        ([ixNet getAttr $dmInfo -recentDelaySec] == 0 &&      \
                        [ixNet getAttr $dmInfo -recentDelayNanoSec] == 0)} {
                        puts "Delay should be a non zero value..."
                        return $isError
                    }
                    # Reached here -> all field match found in learnt info
                    puts "Expected learntinfo present in CFM Link Trace learntinfo list ..."
                    puts " ----------------------------- "
                    incr isFound
                    break
                }
            }
        }
    }
    puts "Among all $numInfoInCheckList info $isFound are present in DM Learnt Info List"
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}


# CFM
#-------------------------------------------------------------------------------
# PROCEDURE  : checkCfmPeriodicOAMLtLearnedInfo
# PURPOSE    :
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkCfmPeriodicOAMLtLearnedInfo {bridge checkList ltLearnedHopList} {
    set isError 1

    if {[setAndCheckAttributeValue $bridge "userPeriodicOamType" {"linkTrace" y}] == 1} {
        return $isError
    }

    # Refresh CFM Periodic OAM LT learnt Info
    ixNet exec updatePeriodicOamLearnedInfo $bridge

    set count 0
    set isComplete false
    puts "Retrieving CFM Periodic OAM Lt learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPeriodicOamLearnedInfoRefreshed]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 60 } {
            puts "Failed to retrieve Pbbte Periodic OAM Lt learnt info, \
                [ixNet getAttr $bridge -isPeriodicOamLearnedInfoRefreshed]"
            return $isError
        }
    }
    puts "CFM Periodic OAM Lt learnt info refreshed ..."

    # Return if no verification needed, we did passed empty match list
    if {$checkList == ""} {
        puts "returning as no verification needed..."
        set isError 0
        return $isError
    }

    # CFM LT Db
    set db {averageHopCount   \
           cVlan              \
           completeReplyCount \
           dstMacAddress      \
           ltmSentCount       \
           mdLevel            \
           noReplyCount       \
           partialReplyCount  \
           recentHopCount     \
           recentHops         \
           recentReplyStatus  \
           sVlan              \
           srcMacAddress}

    # Get LT Learned Info List
    set ltLearnedInfoList [ixNet getList $bridge periodicOamLtLearnedInfo]

    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0

    foreach val $checkList {
        foreach $db $val {
            incr numInfoInCheckList
            puts " -----------------------------"
            puts "Browsing Cfm Lt learntinfo list ..."
            foreach ltInfo $ltLearnedInfoList {
                set misMatch 0
                foreach attr $db {
                    set attrVal [set [set attr]]
                    if {[matchAttributeValue $ltInfo $attr $attrVal] == 1} {
                         set misMatch 1
                         break
                    }
                }

                if {$misMatch == 0} {
                    set ltHopInfo [ixNet getList $ltInfo ltLearnedHop]
                    if [verifyLtHopInfo $ltHopInfo $ltLearnedHopList] {
                    set misMatch 1
                    continue
                    }
                    # Reached here -> all field match found in learnt info
                    puts "Expected learntinfo present in CFM Link Trace learntinfo list ..."
                    puts " ----------------------------- "
                    incr isFound
                    break
                }
            }
        }
    }
 
    puts "Among all $numInfoInCheckList info $isFound are \
          present in Link Trace Learnt Info List"
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}

#-------------------------------------------------------------------------------
# PROCEDURE  : checkCfmPeriodicOAMLBLearnedInfo
# PURPOSE    : Verifying cfm Periodic OAM LB Learned Info
# PARAMETERS :
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc checkCfmPeriodicOAMLBLearnedInfo {bridge checkList} {

    set isError 1

    if {[setAndCheckAttributeValue $bridge "userPeriodicOamType" \
        {"loopback" y}] == 1} {
        return $isError
    }

    # Refresh CFM Periodic OAM LT learnt Info
    ixNet exec updatePeriodicOamLearnedInfo $bridge

    set count 0
    set isComplete false
    puts "Retrieving CFM Periodic OAM Lt learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPeriodicOamLearnedInfoRefreshed]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 60 } {
            puts "Failed to retrieve CFM Periodic OAM Lt learnt info, \
                [ixNet getAttr $bridge -isPeriodicOamLearnedInfoRefreshed]"
            return $isError
        }
    }
    puts "CFM Periodic OAM Lt learnt info refreshed ..."

    # Return if no verification needed, we did passed empty match list
    if {$checkList == ""} {
        puts "returning as no verification needed..."
        set isError 0
        return $isError
    }

    # CFM LB Db
    set db {cVlan              \
            dstMacAddress      \
            lbmSentCount       \
            mdLevel            \
            noReplyCount       \
            recentReachability \
            sVlan              \
            srcMacAddress }

    # Get LB Learned Info List
    after 5000
    set lbLearnedInfoList [ixNet getList $bridge periodicOamLbLearnedInfo]

    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0

    foreach val $checkList {
        foreach $db $val {
            incr numInfoInCheckList
            puts " -----------------------------"
            puts "Browsing Cfm Lt learntinfo list ..."
            foreach lbInfo $lbLearnedInfoList {
                set misMatch 0
                foreach attr $db {
                    set attrVal [set [set attr]]
                    if {[matchAttributeValue $lbInfo $attr $attrVal] == 1} {
                         set misMatch 1
                         break
                    }
                }
                if {$misMatch == 0} {
                    puts "averageRtt: [ixNet getAttr $lbInfo -averageRtt] \
                        recentRtt: [ixNet getAttr $lbInfo -recentRtt]"
                    # Reached here -> all field match found in learnt info
                    puts "Expected learntinfo present in CFM Link Trace learntinfo list ..."
                    puts " ----------------------------- "
                    incr isFound
                    break
                }
            }
        }
    }

    puts "Among all $numInfoInCheckList info $isFound are present \
        in Link Trace Learnt Info List"
    
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : checkItuPeriodicOAMDMLearnedInfo
# PURPOSE    : Verifying ITU Periodic OAM DM Learned Info
# PARAMETERS :
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkItuPeriodicOAMDMLearnedInfo {bridge checkList} {

    set isError 1

    if {[setAndCheckAttributeValue $bridge "userPeriodicOamType" \
        {"delayMeasurement" y}] == 1} {
        return $isError
    }

    # Refresh CFM Periodic OAM LT learnt Info
    ixNet exec updatePeriodicOamLearnedInfo $bridge

    set count 0
    set isComplete false
    puts "Retrieving ITU Periodic OAM DM learnt info ..."

    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPeriodicOamLearnedInfoRefreshed]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 60 } {
            puts "Failed to retrieve ITU Periodic OAM DM learnt info, \
                [ixNet getAttr $bridge -isPeriodicOamLearnedInfoRefreshed]"
            return $isError
        }
    }
    puts "ITU Periodic OAM DM learnt info refreshed ..."

    # Return if no verification needed, we did passed empty match list
    if {$checkList == ""} {
        puts "returning as no verification needed..."
        set isError 0
        return $isError
    }

    # CFM DM Db
    set db {cVlan         \
            dmmCountSent  \
            dstMacAddress \
            mdLevel       \
            noReplyCount  \
            sVlan         \
            srcMacAddress}

    # Get DM Learned Info List
    after 5000
    set delayLearnedInfoList [ixNet getList $bridge periodicOamDmLearnedInfo]

    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0

    foreach val $checkList {
        foreach $db $val {
            incr numInfoInCheckList
            puts " -----------------------------"
            puts "Browsing Cfm Lt learntinfo list ..."
            foreach dmInfo $delayLearnedInfoList {
                set misMatch 0
                foreach attr $db {
                    set attrVal [set [set attr]]
                    if {[matchAttributeValue $dmInfo $attr $attrVal] == 1} {
                         set misMatch 1
                         break
                    }
                }
                if {$misMatch == 0} {
                    puts "averageDelaySec: [ixNet getAttr $dmInfo -averageDelaySec]       \
                        averageDelayNanoSec: [ixNet getAttr $dmInfo -averageDelayNanoSec] \
                        recentDelaySec: [ixNet getAttr $dmInfo -recentDelaySec]           \
                        recentDelayNanoSec: [ixNet getAttr $dmInfo -recentDelayNanoSec] "

                    if {([ixNet getAttr $dmInfo -averageDelaySec] == 0 &&     \
                         [ixNet getAttr $dmInfo -averageDelayNanoSec] == 0) || \
                        ([ixNet getAttr $dmInfo -recentDelaySec] == 0 &&      \
                         [ixNet getAttr $dmInfo -recentDelayNanoSec] == 0)} {
                        puts "Delay should be a non zero value..."
                        return $isError
                    }

                    # Reached here -> all field match found in learnt info
                    puts "Expected learntinfo present in CFM Link Trace learntinfo list ..."
                    puts " ----------------------------- "
                    incr isFound
                    break
                }
            }
        }
    }
    
    puts "Among all $numInfoInCheckList info $isFound are present in \
         Link Trace Learnt Info List"
    
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : checkPbbteDelayLearnedInfo
# PURPOSE    :
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in
#                          learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkPbbteDelayLearnedInfo {bridge filterList checkList {timeout 5000}} {
    set isError 1

    # Below veriable is for debug puts only
    array set filterListArray $filterList
    puts "Setting Pbt Delay filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $bridge $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }

    # set userLearnedInfoTimeOut
    if {[setAndCheckAttributeValue $bridge "userLearnedInfoTimeOut" \
        [list $timeout y]] == 1} {
        return $isError
    }

    after 5000

    # Refresh Pbt LB learnt Info
    set status [ixNet exec startDelayMeasurement $bridge]

    set count 0
    set maxCount [expr [expr $timeout / 1000] + 10] ;# timeout + 10 sec
    set isComplete false
    puts "Retrieving Pbt Delay info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPbbTeDelayLearnedInfoRefreshed]
        puts "isComplete ---> $isComplete"
        after 1000
        incr count
        if { $count > $maxCount } {
            puts "Failed to retrieve Pbt Delay info, [ixNet getAttr $bridge \
                  -pbbTeDelayLearnedErrorString]"
            return $isError
        }
    }
    puts "Pbt Delay info refreshed ..."

    # Check Pbt Delay pkt sent
    if {[matchAttributeValue $bridge "isPbbTeDelayLearnedPacketSent" "True"] == 1} {
        puts "No Pbt Delay pkt sent, [ixNet getAttr $bridge \
              -pbbTeDelayLearnedErrorString]"
        return $isError
    }
    puts "PbbTe Delay pkt sent ... "

    set delayInfo [ixNet getList $bridge pbbTeDelayLearnedInfo]
    after 5000
    
    set db {bVlan         \
            dstMacAddress \
            mdLevel       \
            srcMacAddress}

   # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0

    foreach val $checkList {
        foreach $db $val {
            incr numInfoInCheckList
            puts " -----------------------------"
            puts "Browsing Cfm Dm learntinfo list ..."
            foreach dmInfo $delayInfo {
                set misMatch 0
                foreach attr $db {
                    set attrVal [set [set attr]]
                    if {[matchAttributeValue $dmInfo $attr $attrVal] == 1} {
                         set misMatch 1
                         break
                    }
                }
                if {$misMatch == 0} {
                    puts "averageDelaySec: [ixNet getAttr $dmInfo -valueInSec] \
                        averageDelayNanoSec: [ixNet getAttr $dmInfo -valueInNanoSec]"
                    
                    if {([ixNet getAttr $dmInfo -valueInSec] == 0 && \
                        [ixNet getAttr $dmInfo -valueInNanoSec] == 0)} {
                        puts "Delay should be a non zero value..."
                        return $isError
                    }
                 # Reached here -> all field match found in learnt info
                    puts "Expected learntinfo present in CFM Link Trace learntinfo list ..."
                    puts " ----------------------------- "
                    incr isFound
                    break
                }
            }
        }
    }
    
    puts "Among all $numInfoInCheckList info $isFound are present \
          in DM Learnt Info List"
    
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : checkItuDelayLearnedInfo
# PURPOSE    : Check ITU Delay Learnt info getting populated correctly
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in
#                          learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkItuDelayLearnedInfo {bridge filterList checkList {timeout 5000}} {

    set isError 1

    # Below veriable is for debug puts only
    array set filterListArray $filterList
    puts "Setting ITU Delay filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $bridge $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }

    # set userLearnedInfoTimeOut
    if {[setAndCheckAttributeValue $bridge "userLearnedInfoTimeOut" [list $timeout y]] == 1} {
        return $isError
    }

    after 5000

    # Refresh Itu Delay learnt Info
    set status [ixNet exec startDelayMeasurement $bridge]

    set count 0
    set maxCount [expr [expr $timeout / 1000] + 10] ;# timeout + 10 sec
    set isComplete false
    puts "Retrieving ITU Delay info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isDelayMeasurementLearnedInfoRefreshed]
        puts "isComplete ---> $isComplete"
        after 1000
        incr count
        if { $count > $maxCount } {
            puts "Failed to retrieve ITU Delay info, \
                  [ixNet getAttr $bridge -delayLearnedErrorString]"
            return $isError
        }
    }

    puts "ITU Delay info refreshed ..."

    # Check Itu Delay pkt sent
    if {[matchAttributeValue $bridge "isDelayLearnedPacketSent" "True"] == 1} {
        puts "No Itu Delay pkt sent, [ixNet getAttr $bridge -delayLearnedErrorString]"
        return $isError
    }
    puts "ITU Delay pkt sent ... "

    set delayInfo [ixNet getList $bridge delayLearnedInfo]
    puts "$delayInfo"
   after 5000
    set db {cVlan         \
            dstMacAddress \
            mdLevel       \
            srcMacAddress \
            sVlan}

   # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0

    foreach val $checkList {
        foreach $db $val {
            incr numInfoInCheckList
            puts " -----------------------------"
            puts "Browsing Cfm Dm learntinfo list ..."
            foreach dmInfo $delayInfo {
                set misMatch 0
                foreach attr $db {
                    set attrVal [set [set attr]]
                    if {[matchAttributeValue $dmInfo $attr $attrVal] == 1} {
                         set misMatch 1
                         break
                    }
                }
                
                if {$misMatch == 0} {
                    puts "averageDelaySec: [ixNet getAttr $dmInfo -valueInSec] \
                        averageDelayNanoSec: [ixNet getAttr $dmInfo -valueInNanoSec]"
                    if {([ixNet getAttr $dmInfo -valueInSec] == 0 && \
                        [ixNet getAttr $dmInfo -valueInNanoSec] == 0)} {
                        puts "Delay should be a non zero value..."
                        return $isError
                    }
                    
                    # Reached here -> all field match found in learnt info
                    puts "Expected learntinfo present in CFM Link Trace learntinfo list ..."
                    puts " ----------------------------- "
                    incr isFound
                    break
                }
            }
        }
    }

    puts "Among all $numInfoInCheckList info $isFound are present in \
          DM Learnt Info List"

    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : pbbTeLtLearnedInfo
# PURPOSE    :
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in
#                          learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc checkPbbTeLtLearnedInfo {bridge filterList checkList ltLearnedHopList \
                {configMep "true"} {transactionId 0} {timeout 5000} {ttl 64}} {

    set isError 1

    # Below veriable is for debug puts only
    array set filterListArray $filterList
    puts "Setting Cfm Lt Advanced filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $bridge $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }

    # set userLearnedInfoTimeOut
    if {[setAndCheckAttributeValue $bridge "userLearnedInfoTimeOut" \
        [list $timeout y]] == 1} {
        return $isError
    }

    # set userTtlInterval
    if {[setAndCheckAttributeValue $bridge "userTtlInterval" [list $ttl y]] == 1} {
        return $isError
    }

    # Check case with unconfigured MEP
    if {([string tolower $configMep] == "false") && ($transactionId != 0)} {
        if {[setAndCheckAttributeValue $bridge "userTransactionId" \
            [list $transactionId y]] == 1} {
            return $isError
        }
    }

    after 5000
    ixNet exec refreshCcmLearnedInfo $bridge
    after 5000

    # Refresh PBBTE LT learnt Info
    set status [ixNet exec startLinkTrace $bridge]

    set count 0
    set isComplete false
    puts "Retrieving Cfm Lt learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isLinkTraceLearnedInfoRefreshed]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 60 } {
            puts "Failed to retrieve Cfm Lt learnt info, \
                  [ixNet getAttr $bridge -ltLearnedErrorString]"
            return $isError
        }
    }
    puts "PBBTE Lt learnt info refreshed ..."

    # Return if no verification needed, we did passed empty match list
    if {$checkList == ""} {
        puts "returning as no verification needed..."
        set isError 0
        return $isError
    }

    # Check CFM LT pkt sent
    if {[matchAttributeValue $bridge "isLtLearnedPacketSent" "True"] == 1} {
        puts "No Cfm Lt pkt sent, [ixNet getAttr $bridge -ltLearnedErrorString]"
        return $isError
    }
    puts "Cfm Link Trace pkt sent ? [ixNet getAttr $bridge -isLtLearnedPacketSent]"

    # CFM LT Db
    set db {bVlan         \
            mdLevel       \
            srcMacAddress \
            dstMacAddress \
            hopCount      \
            replyStatus}

    # Get LT Learned Info List
    set ltLearnedInfoList [ixNet getList $bridge pbbTeLtLearnedInfo]

    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0
    foreach $db $checkList {
        incr numInfoInCheckList
        puts " -----------------------------"
        puts "Browsing Cfm Lt learntinfo list ..."
        foreach ltInfo $ltLearnedInfoList {
            set misMatch 0
            foreach attr $db {
                set attrVal [set [set attr]]
                if {[matchAttributeValue $ltInfo $attr $attrVal] == 1} {
                     set misMatch 1
                     break
                }
            }
            if {$misMatch == 0} {
                # Check Lt Learned HopList
                set ltHopInfo [ixNet getList $ltInfo ltLearnedHop]
                if [verifyLtHopInfo $ltHopInfo $ltLearnedHopList] {
                    set misMatch 1
                    continue
                }
                # Check case with unconfigured MEP
                if {([string tolower $configMep] == "false") && \
                    ($transactionId != 0)} {
                    if {[matchAttributeValue $lbInfo "transactionId" $transactionId] == 1} {
                        continue
                    }
                }
                puts "Cfm Lt Learned ConfigMep ? : [ixNet getAttr $bridge \
                        -isLtLearnedConfigMep] (replyStatus : [ixNet getAttr $ltInfo \
                        -replyStatus], hops : [ixNet getAttr $ltInfo -hops])"

                # Reached here -> all field match found in learnt info
                puts "Expected learntinfo present in CFM Link Trace learntinfo list ..."
                puts " ----------------------------- "
                incr isFound
                break
            }
        }
    }
    
    puts "Among all $numInfoInCheckList info $isFound are present in \
          Link Trace Learnt Info List"
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}
