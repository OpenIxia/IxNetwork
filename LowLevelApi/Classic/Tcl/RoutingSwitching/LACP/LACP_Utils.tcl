#========================== GLOBAL VARIABLES USED =============================
global lacpGlobalParams
set lacpGlobalParams(pktCaptureDurLong) 120
set lacpGlobalParams(pktCaptureDurShort) 10
set lacpGlobalParams(ixNetOk) "::ixNet::OK"
set lacpGlobalParams(TRUE) "true"
set lacpGlobalParams(FALSE) "false"
set lacpGlobalParams(runningState) "started"
set lacpGlobalParams(runningState1) "stopped"
set lacpGlobalParams(pktCaptureDurLongInMilisec) 120000
set lacpGlobalParams(pktCaptureDurShortInMilisec) 10000
set lacpGlobalParams(actorByteNo) 32
set lacpGlobalParams(partnerByteNo) 52
set lacpGlobalParams(collectionBit) 5
set lacpGlobalParams(distributionBit) 6
set lacpGlobalParams(maskForDistributionBit) 32
set lacpGlobalParams(maskForCollectionBit) 16
set lacpGlobalParams(markerFreqTime) 15
set lacpGlobalParams(markerFreqTimeInMilisec) 15000
set lacpGlobalParams(activityBit) 1
set lacpGlobalParams(maskForActivityBit) 1
set lacpGlobalParams(timeoutBit) 2
set lacpGlobalParams(maskForTimeoutBit) 2
set lacpGlobalParams(aggregationBit) 3
set lacpGlobalParams(maskForAggregationBit) 4
set lacpGlobalParams(syncBit) 4
set lacpGlobalParams(maskForSyncBit) 8
set lacpGlobalParams(devideValue) 1000000000
set lacpGlobalParams(shortTimeoutLowerlimit) 2
set lacpGlobalParams(shortTimeoutUpperlimit) 3
set lacpGlobalParams(longTimeoutLowerlimit) 89
set lacpGlobalParams(longTimeoutUpperlimit) 90
set lacpGlobalParams(longTimeOutValue) 90
set lacpGlobalParams(oneMinDelay) 60
set lacpGlobalParams(oneMinDelayInMilisec) 60000
#=================================================================================
proc startStatelessTraffic {} {

    set root [ixNet getRoot]
    set trafficWizard $root/traffic/wizard
    set traffic $root/traffic

    if {[catch {set trafficItem [ixNet getList $traffic trafficItem]} error]} {
        puts "Error Getting the configured traffic $error"
        return 1
    }

    set genTraffic ""
    puts "Generating traffic items..."

    catch {set genTraffic [ixNet setAtt [ixNet getRoot]/traffic \
           -refreshLearnedInfoBeforeApply  True]} error
    if {$genTraffic != "::ixNet::OK"} {
        puts "Not able to set the generate the traffic: $error"
        return 1
    }
    ixNet commit
    after 10000
    puts "Traffic generation done!!"

    set appTraffic ""
    puts "Applying the stateless traffic..."
    catch {set appTraffic [::ixNet exec apply $traffic]} error
    if {$appTraffic != "::ixNet::OK"} {
        puts "Not able to apply the traffic: $error"
        return 1
    }
    puts "Traffic applied successfully !!"

    set startTraffic ""
    puts "Starting the stateless traffic"
    catch {set startTraffic [::ixNet exec start $traffic]} error
    if {$startTraffic != "::ixNet::OK"} {
        puts "Not able to start the traffic: $error"
        return 1
    }
    puts "Traffic started successfully"

    return 0
}

proc stopStatelessTraffic {} {
    set root [ixNet getRoot]
    set trafficWizard $root/traffic/wizard
    set traffic $root/traffic

    if {[catch {set trafficItem [ixNet getList $traffic trafficItem]} error]} {
        puts "Error Getting the configured traffic $error"
        return 1
    }

    set stopTraffic ""
    puts "Stopping the stateless traffic"
    catch {set stopTraffic [::ixNet exec stop $traffic]} error
    if {$stopTraffic != "::ixNet::OK"} {
        puts "Not able to stop the traffic: $error"
        return 1
    }
    puts "Traffic stopped successfully"

    return 0

}

################################################################################
# STATISTICS VERIFICATION
################################################################################

#-------------------------------------------------------------------------------
# PROCEDURE  : checkAllLacpStats
# PURPOSE    :
# PARAMETERS : portList -
#              stat - {name value} Stat list to verify
#Author      :Darshan T
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkAllLacpStats {portList stat {exactMatch 0}} {
    set sessFoundFlag 0
    set userViewList [ixNet getList [ixNet getRoot]/statistics userStatView]
    foreach view $userViewList {
        ixNet remove $view
        ixNet commit
    }

    set userStatView [SetupUserStats $portList "LACP" "*"]
    set timeout 20
    set doneList $portList

    array set statToVerify $stat
    set statNames [array names statToVerify]

    set returnFlag 1

    #Checking the stats.."
    set contFlag 0
    #puts [format "%-32s %10s\t%10s" "STAT NAME" "EXPECTED" "OBTAINED"]
    foreach eachStat $statNames {
        while {$timeout > 0} {
            GetStatValue "UserStatView LACP" "$eachStat" statValueArray1
            if {[lindex [array get statValueArray1] 1] >= $statToVerify($eachStat)} {
                PrintArray statValueArray1
                if {($exactMatch == 1) && [lindex [array get statValueArray1] 1] != \
                     $statToVerify($eachStat)} {
                    return 1
                }
            } else {
                PrintArray statValueArray1
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
        } ;# end while (timeout > 0)
    }


    if {$contFlag == 0} {
        logMsg "Error... Check the configuration"
        return 1
    }

    if {$returnFlag == 1} {
        return 0
    } else {
        return 1
    }
}

################################################################################
# Enable and Start capture on ports.
################################################################################

#-------------------------------------------------------------------------------
# PROCEDURE  : enableAndStartCapture
# PURPOSE    : Enable and Start capture on given ports in argument.
# PARAMETERS : vPort1-Vitrual port on which we have to start capture.
#              args-List of other ports on which we wan to start capture.
#Author      :Darshan T
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail.
#-------------------------------------------------------------------------------
proc enableAndStartCapture {vPort1 args} {
    puts "The argument is <$vPort1> and <$args>............"
    # initialize return value
    set PASSED 0
    set FAILED 1

    ixNet setAttribute $vPort1 -rxMode capture
    ixNet setAttribute $vPort1/capture -softwareEnabled true
    ixNet setAttribute $vPort1/capture -hardwareEnabled true
    after 2000
    ixNet commit
    
    after 2000
    foreach vPorts $args {
        ixNet setAttribute $vPorts -rxMode capture
        ixNet setAttribute $vPorts/capture -softwareEnabled true
        ixNet setAttribute $vPorts/capture -hardwareEnabled true
        ixNet commit
        after 2000
    }

    # capture cleanup
    if {[catch {ixNet exec closeAllTabs} err] == 1} {
        puts "Failed to close existing analyser tabs "
    }

    #Start the capture
    puts "Start Capturing packets"

    ixNet commit
    after 5000
    
    if {[catch {ixNet exec startCapture} err] == 1} {
        puts "Failed to start packet capture "
        ixNetCleanUp
        return $FAILED
    }

    puts "Enable and Start Capture Complete Successfully"
    return $PASSED
}


################################################################################
# Start Protocol on ports.
################################################################################
#-------------------------------------------------------------------------------
# PROCEDURE  : startLacpOnPorts
# PURPOSE    : Start LACP protocol on given object of LACP protocol in argument.
# PARAMETERS : proto-Lacp protocol object on which we want to start protocol.
#              args-List of other protocol objects on which we wan to start
#                   protcol.
#Author      :Darshan T
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc startLacpOnPorts {proto args} {
    # initialize return value
    set PASSED 0
    set FAILED 1

    puts "---------------The for first Port is <$proto>"
    if {[catch {ixNet exec start $proto} err] == 1} {
        puts "Failed to Start LACP "
        return $FAILED
    }

    foreach proto1 $args {
        puts "The for Port is <$proto1>"
        if {[catch {ixNet exec start $proto1} err] == 1} {
            puts "Failed to Start LACP "
            return $FAILED
        }
    }

    puts "LACP Protocol started successfully"
    return $PASSED
}


################################################################################
# Stop Protocol on ports.
################################################################################
#-------------------------------------------------------------------------------
# PROCEDURE  : stopLacpOnPorts
# PURPOSE    : Stop LACP protocol on given object of LACP protocol in argument.
# PARAMETERS : proto-Lacp protocol object on which we want to start protocol.
#              args-List of other protocol objects on which we wan to start
#                   protcol.
#Author      :Darshan T
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc stopLacpOnPorts {proto args} {
    # initialize return value
    set PASSED 0
    set FAILED 1

    puts "Stop LACP Protocol"

    if {[catch {ixNet exec stop $proto} err] == 1} {
        puts "Failed to Stop LACP "
        return $FAILED
    }

    foreach proto1 $args {
        if {[catch {ixNet exec stop $proto1} err] == 1} {
            puts "Failed to Stop LACP "
            return $FAILED
        }
    }

    return $PASSED
}

################################################################################
# Start Protocol on ports.
################################################################################
#-------------------------------------------------------------------------------
# PROCEDURE  : verifyMarkerCapture
# PURPOSE    : Enable and Start capture on given ports in argument.
# PARAMETERS : chassisId -
#              cardNo -
#              portNo -
#              markerType - Type of marker packet (0-Request,1-Responce)
#              count - No of packet to verify
#              time - time interval between two packet.
#Author      :Darshan T
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc verifyMarkerCapture {chassisId cardNo portNo markerType expTimeDiff \
         {expPktCnt 1}} {

    # initialize return value
    set PASSED 0
    set FAILED 1

    if {$markerType == 0} {
        puts "Verifying Marker Request frame structure"
        set matchFieldList {0 5 "01 80 C2 00 00 02" \
                            14 14 "02" \
                            16 16 "01"}

    } elseif {$markerType == 1} {
        puts "Verifying Marker Respond frame structure"
        set matchFieldList {0 5 "01 80 C2 00 00 02" \
                            14 14 "02" \
                            16 16 "02"}
    } else {
        puts "Invalid Marker Packet type is given"
        return $FAILED
    }

    if {[verifyCapturedPackets $chassisId $cardNo $portNo $matchFieldList \
             $expTimeDiff $expPktCnt]==1} {

        puts "Error In Marker packet Verification"
        return $FAILED
    }

    puts "Verification Of Marker PDU Complete Successfully"
    return $PASSED
}

################################################################################
# Verify both actor and partner state on same port.
################################################################################
#-------------------------------------------------------------------------------
# PROCEDURE  : verifyActorPartnerStates
# PURPOSE    : Verify States as per gievn information.
# PARAMETERS :
#              Chassis:
#              card:
#              Port:
#              args: Args contains the all information from which bytes we verify
#                    which bit for actor and partner.
#Author      :DarshanT
# RETURN     : List of bytes or 1 on fail
#-------------------------------------------------------------------------------
proc verifyActorPartnerStates {chassis card port args} {
    set PASSED 0
    set FAILED 1
    
    puts "Initilizing thorugh IxTclHal...."
    ixInitialize $chassis
    chassis get $chassis
    set chassisId [chassis cget -id]
    set count 0

    port get $chassisId $card $port
    puts "$chassisId $card $port------------------"
    set loginName [port cget -owner]
    ixLogin $loginName
    puts "Logging in using the $loginName"

    # Retrive captured packets
    captureBuffer get $chassisId $card $port
    set numCapturedPkts [captureBuffer cget -numFrames]
    puts "No of capture Packets <$numCapturedPkts>............."
    if {$numCapturedPkts < 1} {
        return $FAILED
    }

    captureBuffer get $chassisId $card $port 1 $numCapturedPkts

    for {set f 1} {$f <= $numCapturedPkts} {incr f} {
        after 50
        captureBuffer getframe $f
        after 50
        set capFrame [captureBuffer cget -frame]
        puts "TimeStamp of frame$f :  [captureBuffer cget -timestamp]"

        foreach dataList $args {
            set mismatch 0
            set getBytes "0x[lindex $capFrame [lindex $dataList 0]]"
            puts "the byte no is <[lindex $dataList 0]>"

            puts "Get Byte is <$getBytes> and frame is :---- $capFrame"

            set intByte  [format %d $getBytes]
            set bitNo    [lindex $dataList 1]
            set expValue [lindex $dataList 2]

            puts "Integer Value is -------<$intByte>"

            if {$bitNo == 1} {
                puts "the anding result---------<[expr $intByte & 1]> and expected \
                      Value is <$expValue>"
                if {[expr $intByte & 1] != $expValue} {
                    puts "For LACP Activity Expected bit is <$expValue> but actual \
                          value is <[expr $intByte & 1]>"
                    return $FAILED
                }
            } elseif {$bitNo == 2} {
                puts "the anding result---------<[expr $intByte & 2]> \
                      and expected Value is <$expValue>"
                if {[expr $intByte & 2] != $expValue} {
                    puts "For LACP Time Out Expected bit is <$expValue> but actual \
                          value is <[expr $intByte & 2]>"
                    return $FAILED
                }
            } elseif {$bitNo == 3} {
                puts "the anding result---------<[expr $intByte & 4]> and \
                      expected Value is <$expValue>"
                if {[expr $intByte & 4] != $expValue} {
                    puts "For LACP Aggregation  Expected bit is <$expValue> \
                          but actual value is <[expr $intByte & 4]>"
                    return $FAILED
                }
            } elseif {$bitNo == 4} {
                puts "the anding result---------<[expr $intByte & 8]> and expected \
                      Value is <$expValue>"
                if {[expr $intByte & 8] != $expValue} {
                    puts "For LACP Synchronization Expected bit is <$expValue> but \
                          actual value is <[expr $intByte & 8]>"
                    return $FAILED
                }
            } elseif {$bitNo == 5} {
                if {[expr $intByte & 16] != $expValue} {
                    puts "For LACP Collection Expected bit is <$expValue> but \
                          actual value is <[expr $intByte & 16]>"
                    return $FAILED
                }
            } elseif {$bitNo == 6} {
                if {[expr $intByte & 32] != $expValue} {
                    puts "For LACP Distribution Expected bit is <$expValue> but \
                          actual value is <[expr $intByte & 32]>"
                    return $FAILED
                }
            } elseif {$bitNo == 7} {
                if {[expr $intByte & 64] != $expValue} {
                    puts "For LACP Default Expected bit is <$expValue> but actual \
                          value is <[expr $intByte & 64]>"
                    return $FAILED
                }
            } elseif {$bitNo == 8} {
                if {[expr $intByte & 128] != $expValue} {
                    puts "For LACP Expired Expected bit is <$expValue> but actual \
                          value is <[expr $intByte & 128]>"
                    return $FAILED
                }
            } else {
                puts "Wrong input given for States Verification...."
                return $FAILED
            }
        }
    }
    return $PASSED
}

################################################################################
# Verify given given link attribute value with actual value.
################################################################################
#-------------------------------------------------------------------------------
# PROCEDURE  : checkLacpLinkAttribut
# PURPOSE    : Verify given given link attribute value with actual value.
# PARAMETERS :
#             linkObj : Object of link
#             mainDataList: List of attribute of link and its expected values
#Author      :DarshanT
# RETURN     :FAILED - 1
#             PASSED - 0
#-------------------------------------------------------------------------------
proc checkLacpLinkAttribut {linkObj mainDataList} {
    set count  0
    set PASSED 0
    set FAILED 1

    set attributList [lindex $mainDataList 0]
    set setValueList [lindex $mainDataList 1]

    foreach singleAttribut $attributList {
       if {[string tolower [ixNet getAttr $linkObj -$singleAttribut]] != \
            [string tolower [lindex $setValueList $count]]} {
            puts "Error to get <[lindex $setValueList $count]> for \
                  $singleAttribut Attribute"
            return $FAILED
        }
        incr count
    }

    if {$count == 0} {
        puts "Given Data is not proper...."
        return $FAILED
    }

    puts "All the attribute set properly...."
    return $PASSED
}


################################################################################
# Set the particualr value given for the particualr attribute for given link obj.
################################################################################
#-------------------------------------------------------------------------------
# PROCEDURE  : setLacpLinkAttribut
# PURPOSE    : Set the particualr value given for the particualr attribute for
#              given link obj.
# PARAMETERS :
#             linkObj : Object of link
#             mainDataList: List of attribute of link and its expected values to
#                           set.
#Author      :DarshanT
# RETURN     :FAILED - 1
#             PASSED - 0
#-------------------------------------------------------------------------------
proc setLacpLinkAttribut {linkObj mainDataList} {
    set count  0
    set PASSED 0
    set FAILED 1

    set attributList [lindex $mainDataList 0]
    set setValueList [lindex $mainDataList 1]

    foreach singleAttribut $attributList {
        if {[catch {ixNet setAttr $linkObj -$singleAttribut \
                        [lindex $setValueList $count]} err] == 1} {
            puts "Failed to set <[lindex $setValueList $count]> \
                  for $singleAttribut Attribute"
            return $FAILED
        }

        if {[catch {ixNet commit} err] == 1} {

            puts "Failed to Commit the changes"
            return $FAILED
        }

        if {[string tolower [ixNet getAttr $linkObj -$singleAttribut]] != \
            [string tolower [lindex $setValueList $count]]} {
            puts "Error to set <[lindex $setValueList $count]> for \
                 $singleAttribut Attribute"
            return $FAILED
        }
        incr count
    }

    if {$count == 0} {
        puts "NULL list provided"
        return $FAILED
    }

    puts "All the attribute set properly...."
    return $PASSED
}

################################################################################
# PACKET STRUCTURE VERIFICATION
################################################################################

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
proc verifyCapturedPackets {chassis card port matchFieldList expTimeDiff \
     {expPktCnt 1}} {

    set isError 1
    set PASSED  0
    set FAILED  1
    
    puts "Initilizing thorugh IxTclHal...."
    ixInitialize $chassis
    chassis get $chassis
    set chassisId [chassis cget -id]

    set count 0

    set curTime 0
    set prevTime 0

    port get $chassisId $card $port

    puts "$chassisId $card $port------------------"
    set loginName [port cget -owner]
    ixLogin $loginName
    puts "Logging in using the $loginName"

    # Retrive captured packets
    captureBuffer get $chassisId $card $port
    set numCapturedPkts [captureBuffer cget -numFrames]
    puts "Captured $numCapturedPkts pkts (expected: $expPktCnt)"
    if {$numCapturedPkts < $expPktCnt} {
        puts "No of captured packet is <$numCapturedPkts> \
              Less than expected packet count <$expPktCnt>"
        return $FAILED
    }
    captureBuffer get $chassisId $card $port 1 $numCapturedPkts
    for {set f 1} {$f <= $numCapturedPkts} {incr f} {
        after 50
        captureBuffer getframe $f
        after 50
        set capFrame [captureBuffer cget -frame]
        puts "TimeStamp of frame$f :  [captureBuffer cget -timestamp]"

        set mismatch 0
        foreach {startIndex endIndex expectedVal} $matchFieldList {
            puts "Obtained Pattern: [lrange $capFrame $startIndex $endIndex] \
                    Expected Pattern: $expectedVal"
            if {[string tolower [lrange $capFrame $startIndex $endIndex]] != \
                [string tolower $expectedVal]} {
                set mismatch 1
                puts "Obtained: [lrange $capFrame $startIndex $endIndex] \
                      Expected: $expectedVal ---> No Match"
                break
            }
        }
        if {$mismatch == 0} {
            puts "------$capFrame"
            puts "All Field Patterns Matched !!!"
            set isError 0
            incr count

            set prevTime $curTime
            set curTime [captureBuffer cget -timestamp]

            if {$prevTime != 0 && $expTimeDiff != 0} {
                set obsTimeDiff [expr [expr $curTime - $prevTime]/1000000000]
                if { $obsTimeDiff != $expTimeDiff} {
                    puts "Time diff between two PDUs is not proper, \
                          expTimeDiff/obsTimeDiff : <$expTimeDiff>/<$obsTimeDiff>"
                    return $FAILED
                }
            }
        }
    }
    
    if {$expPktCnt != 1 && $count < $expPktCnt} {
        puts "Not able to get min. no. of packest expected : \
              minexpPktCount/rcvdPktCont : <$expPktCnt>/<$count>"
        return $FAILED
    }

    puts "Packet Verification Complete Successfully"
    return $PASSED
}


proc verifyCapture {chassis card port pattern {expPktCnt 1}} {
    
    set isError 1
    set PASSED  0
    set FAILED  1
    
    puts "Initilizing thorugh IxTclHal...."
    ixInitialize $chassis
    chassis get $chassis
    set chassisId [chassis cget -id]

    set count    0
    set curTime  0
    set prevTime 0

    port get $chassisId $card $port

    puts "$chassisId $card $port------------------"
    set loginName [port cget -owner]
    ixLogin $loginName
    puts "Logging in using the $loginName"

    # Retrive captured packets
    captureBuffer get $chassisId $card $port
    set numCapturedPkts [captureBuffer cget -numFrames]
    puts "Captured $numCapturedPkts pkts (expected: $expPktCnt)"
    if {$numCapturedPkts < $expPktCnt} {
        return $FAILED
    }
    captureBuffer get $chassisId $card $port 1 $numCapturedPkts
    for {set f 1} {$f <= $numCapturedPkts} {incr f} {
        after 50
        captureBuffer getframe $f
        after 50
        set capFrame [captureBuffer cget -frame]
        puts "TimeStamp of frame$f :  [captureBuffer cget -timestamp]"

        set mismatch 0
        foreach {startIndex endIndex expectedVal} $pattern {
            puts "Obtained Pattern: [lrange $capFrame $startIndex $endIndex] \
                  Expected Pattern: $expectedVal"
            
            if {[lrange $capFrame $startIndex $endIndex] != $expectedVal} {
                set mismatch 1
                puts "Obtained: [lrange $capFrame $startIndex $endIndex] \
                        Expected: $expectedVal ---> No Match"
                break
            }
        }
        
        if {$mismatch == 0} {
            puts "------$capFrame"
            puts "All Field Patterns Matched !!!"
            set isError 0
            incr count
        }
    }

    puts "Packet Verification Complete Successfully"
    return $PASSED
}

################################################################################
#This Packet return time value for particular packet and checking for packets.
################################################################################
#-------------------------------------------------------------------------------
# PROCEDURE  : getTimeValueOfLacpPacket
# PURPOSE    : This Packet return time value for particular packet and
#              checking for packets.
# PARAMETERS : chassis -
#              card -
#              port -
#              choice - 1(For this choice return time value for last LACPDU)
#                       2(Return time value for first packet where expiry bit
#                         set in acot and sync bit 0 in partner)
#                       3(Checking for first LACP packet in which expiry bit set)
#                       4(Return time stamp for first packet where the defaluted
#                         bit is set)
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc getTimeValueOfLacpPacket {chassis card port choice} {

    set PASSED 0
    set FAILED 1
    
    puts "Initilizing thorugh IxTclHal...."
    ixInitialize $chassis
    chassis get $chassis
    set chassisId [chassis cget -id]

    set count           0
    set curTime         0
    set prevTime        0
    set packetTimeStamp 0
    port get $chassisId $card $port

    puts "$chassisId $card $port------------------"
    set loginName [port cget -owner]
    ixLogin $loginName
    puts "Logging in using the $loginName"

    # Retrive captured packets
    captureBuffer get $chassisId $card $port
    set numCapturedPkts [captureBuffer cget -numFrames]

    if {$numCapturedPkts < 1} {
        puts "No of packet is less than 1..."
        return $FAILED
    }

    captureBuffer get $chassisId $card $port 1 $numCapturedPkts
    set matchFieldList {0 5 "01 80 C2 00 00 02" \
                        12 13 "88 09" \
                        14 14 "01" \
                        15 15 "01" \
                        16 16 "01" \
                        17 17 "14" \
                        33 35 "00 00 00" \
                        36 36 "02" \
                        37 37 "14" \
                        53 55 "00 00 00" \
                        56 56 "03" \
                        57 57 "10"}

    if {$choice == 1} {
        
        for {set f 1} {$f <= $numCapturedPkts} {incr f} {
            after 50
            captureBuffer getframe $f
            after 50
            set capFrame [captureBuffer cget -frame]
            foreach {startIndex endIndex expectedVal} $matchFieldList {
                puts "Obtained Pattern: [lrange $capFrame $startIndex $endIndex] \
                      Expected Pattern: $expectedVal"
                
                if {[lrange $capFrame $startIndex $endIndex] != $expectedVal} {
                    set mismatch 1
                    puts "Obtained: [lrange $capFrame $startIndex $endIndex] \
                          Expected: $expectedVal ---> No Match"
                    break
                } else {

                    set packetTimeStamp [captureBuffer cget -timestamp]
                }
            }
        } ;# end for {set f 1} {$f <= $numCapturedPkts} {incr f}
        
    } elseif {$choice == 2} {
        
        for {set f 3} {$f <= $numCapturedPkts} {incr f} {
            after 50
            captureBuffer getframe $f
            after 50
            set capFrame [captureBuffer cget -frame]

            set getBytes "0x[lindex $capFrame 32]"
            set getBytes1 "0x[lindex $capFrame 52]"

            puts "Get Byte is <$getBytes> and <$getBytes1> \
                  frame is :---- $capFrame"

            set intByte [format %d $getBytes]
            set intByte1 [format %d $getBytes1]

            if {[expr $intByte & 128] == 128 && [expr $intByte1 & 8] == 0} {

                set packetTimeStamp [captureBuffer cget -timestamp]
                break
            }
        } ;# for {set f 3} {$f <= $numCapturedPkts} {incr f}

    } elseif {$choice == 3} {
        set f 1
        after 50
        
        captureBuffer getframe $f
        after 50
        
        set capFrame [captureBuffer cget -frame]

        set getBytes "0x[lindex $capFrame 32]"
        puts "Get Byte is <$getBytes> and frame is :---- $capFrame"

        set intByte [format %d $getBytes]
        if {[expr $intByte & 128] != 128} {
            set packetTimeStamp [captureBuffer cget -timestamp]
            return $FAILED
        }

        for {set f 5} {$f <= $numCapturedPkts} {incr f} {
            after 50
            captureBuffer getframe $f
            after 50
            set capFrame [captureBuffer cget -frame]

            set getBytes "0x[lindex $capFrame 32]"

            puts "Get Byte is <$getBytes> and frame is :---- $capFrame"

            set intByte [format %d $getBytes]

            if {[expr $intByte & 128] == 128} {

                set packetTimeStamp [captureBuffer cget -timestamp]
                return $FAILED
            }

            puts "The no of capture packet is <$numCapturedPkts>=<$f>..........."
        } ;# end {set f 5} {$f <= $numCapturedPkts} {incr f}
        return $PASSED
        
    } elseif {$choice == 4} {
        for {set f 3} {$f <= $numCapturedPkts} {incr f} {
            after 50
            captureBuffer getframe $f
            after 50
            set capFrame [captureBuffer cget -frame]

            set getBytes "0x[lindex $capFrame 32]"

            puts "Get Byte is <$getBytes> frame is :---- $capFrame"

            set intByte [format %d $getBytes]

            if {[expr $intByte & 64] == 64} {

                set packetTimeStamp [captureBuffer cget -timestamp]
                break
            }
        }
    } else {
        puts "Wrong Optiong given..."
        return $FAILED
    }
    return $packetTimeStamp
}

################################################################################
#  LACP Procs 
################################################################################
proc getLacpLearnedInfo {linkProtoId} {
    set isComplete false
    set count 0
    set protocolName lacp

    # Request LearnedInfo
    set retVal [ixNet exec refreshLacpPortLearnedInfo $linkProtoId]

    while {$isComplete != true} {
        flush stdout
        set isComplete [ixNet getAttr $linkProtoId -isLacpPortLearnedInfoRefreshed]
        puts "isComplete = $isComplete"
        after 5000
        incr count
        if {$count > 4} {
            puts "Could not retrieve learnt info on \
                 $protocolName link : <$linkProtoId> , ... timeout"
            return ""
        }
    }

    set learntList [ixNet getList $linkProtoId learnedInfo]
    return $learntList
}


proc retrieveLacpLearnedInfoPerLink {linkProtoId {waitTime 60}} {
    set retInfo ""
    set learntinfo [getLacpLearnedInfo $linkProtoId]
    puts "Learned Info : <$learntinfo>"
    if {[llength $learntinfo] > 0} {;#Learned Info Database is not empty
        lappend retInfo "actorCollectingFlag [::ixNet getAttribute $learntinfo -actorCollectingFlag] \
                     actorDefaultedFlag [::ixNet getAttribute $learntinfo -actorDefaultedFlag] \
                     actorDistributingFlag [::ixNet getAttribute $learntinfo -actorDistributingFlag] \
                     actorExpiredFlag [::ixNet getAttribute $learntinfo -actorExpiredFlag] \
                     actorLacpActivity [::ixNet getAttribute $learntinfo -actorLacpActivity] \
                     actorLacpTimeout [::ixNet getAttribute $learntinfo -actorLacpTimeout] \
                     actorLinkAggregationStatus [::ixNet getAttribute $learntinfo -actorLinkAggregationStatus] \
                     actorOperationalKey [::ixNet getAttribute $learntinfo -actorOperationalKey] \
                     actorPortNumber [::ixNet getAttribute $learntinfo -actorPortNumber] \
                     actorPortPriority [::ixNet getAttribute $learntinfo -actorPortPriority] \
                     actorSyncFlag [::ixNet getAttribute $learntinfo -actorSyncFlag] \
                     actorSystemId [::ixNet getAttribute $learntinfo -actorSystemId] \
                     actorSystemPriority [::ixNet getAttribute $learntinfo -actorSystemPriority] \
                     enabledAggregation [::ixNet getAttribute $learntinfo -enabledAggregation] \
                     partnerCollectingFlag [::ixNet getAttribute $learntinfo -partnerCollectingFlag] \
                     partnerCollectorMaxDelay [::ixNet getAttribute $learntinfo -partnerCollectorMaxDelay] \
                     partnerDefaultedFlag [::ixNet getAttribute $learntinfo -partnerDefaultedFlag] \
                     partnerDistributingFlag [::ixNet getAttribute $learntinfo -partnerDistributingFlag] \
                     partnerExpiredFlag [::ixNet getAttribute $learntinfo -partnerExpiredFlag] \
                     partnerLacpActivity [::ixNet getAttribute $learntinfo -partnerLacpActivity] \
                     partnerLacpTimeout [::ixNet getAttribute $learntinfo -partnerLacpTimeout] \
                     partnerLinkAggregationStatus [::ixNet getAttribute $learntinfo -partnerLinkAggregationStatus] \
                     partnerOperationalKey [::ixNet getAttribute $learntinfo -partnerOperationalKey] \
                     partnerPortNumber [::ixNet getAttribute $learntinfo -partnerPortNumber] \
                     partnerPortPriority [::ixNet getAttribute $learntinfo -partnerPortPriority] \
                     partnerSyncFlag [::ixNet getAttribute $learntinfo -partnerSyncFlag] \
                     partnerSystemId [::ixNet getAttribute $learntinfo -partnerSystemId] \
                     partnerSystemPriority [::ixNet getAttribute $learntinfo -partnerSystemPriority]"
          puts "Returning with learnt Info : \n<$retInfo>\n"
          return $retInfo
    } else {
        puts "No entry exists, check again ...."
        return $retInfo
    }
}

proc getParamFromLearnedInfo {linfo param} {
    puts "Learned Info list : <$linfo>"
    set linfo [lindex $linfo 0]
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

#-----------------------------------------------------------------------------
# PROCEDURE     : clearAll
# PURPOSE       : do all clean up steps in this proc before return
#-----------------------------------------------------------------------------
proc clearAll { {DutInterfaceDataList NULL} } {
    set flag 0
    if [catch {stopAllProtocols} err ] {
        puts "Error: During stop prototcol: $err"
        set flag 1
    }

    puts "Cleaning up client..."
    if [catch {ixNetCleanUp} err] {
        puts "Error: During clean up: $err"
        set flag 1
    }
    puts "Clean up done .."

    if {$DutInterfaceDataList != "NULL"} {
        for {set i 1} {$i <= [llength $DutInterfaceDataList]} {incr i} {
            set DutInterfaceData [lindex $DutInterfaceDataList [expr $i - 1]]
            if [ResetDut $DutInterfaceData $i] {
                set flag 1
            }
        }
    }
    return $flag
}


#-----------------------------------------------------------------------------
# PROCEDURE     : ResetDut
# PURPOSE       : dump content of dut clean up file on DUT
#-----------------------------------------------------------------------------
proc ResetDut {interfaceData number} {
    set flag 0
    set type             [getDutMake $interfaceData]
    set dutIp            [getDutIp $interfaceData]
    set dutConfigScript  [getDutConfigScriptName $type $number]
    set dutInterfaceName [getDutInterfaceName $interfaceData]

    if [configureDut $interfaceData $dutConfigScript] {
        puts "Error resetting DUT $dutIp $dutInterfaceName"
        set flag 1
        return $flag
    }
    return $flag
}

#-----------------------------------------------------------------------------
# PROCEDURE     : clearAll
# PURPOSE       : do all clean up steps in this proc before return
#-----------------------------------------------------------------------------
proc clearAll { {DutInterfaceDataList NULL} } {
    set flag 0
    if [catch {stopAllProtocols} err ] {
        puts "Error: During stop prototcol: $err"
        set flag 1
    }

    puts "Cleaning up client..."
    if [catch {ixNetCleanUp} err] {
        puts "Error: During clean up: $err"
        set flag 1
    }
    puts "Clean up done .."


    if {$DutInterfaceDataList != "NULL"} {
        for {set i 1} {$i <= [llength $DutInterfaceDataList]} {incr i} {
            set DutInterfaceData [lindex $DutInterfaceDataList [expr $i - 1]]
            if [ResetDut $DutInterfaceData $i] {
                set flag 1
            }
        }
    }
    return $flag
}


#-----------------------------------------------------------------------------
# PROCEDURE     : ResetDut
# PURPOSE       : dump content of dut clean up file on DUT
#-----------------------------------------------------------------------------
proc ResetDut {interfaceData number} {

    set flag 0
    set type             [getDutMake $interfaceData]
    set dutIp            [getDutIp $interfaceData]
    set dutConfigScript  [getDutConfigScriptName $type $number]
    set dutInterfaceName [getDutInterfaceName $interfaceData]

    if [configureDut $interfaceData $dutConfigScript] {
        puts "Error resetting DUT $dutIp $dutInterfaceName"
        set flag 1
        return $flag
    }
    return $flag
}


proc verifyCapturedPacketsTimeDiff {chassis card port matchFieldList mintime \
          maxtime {expPktCnt 1} {expPktCnt1 1} } {
    
    ixInitialize $chassis
    chassis get $chassis
    set chassisId [chassis cget -id]
    port get $chassisId $card $port
    puts "Getting the ownership details..."
    set loginName [port cget -owner]
    puts "Logging in using the $loginName"
    ixLogin $loginName

    set isError  1
    set PASSED   0
    set FAILED   1
    set count    0
    set count1   0
    set curTime  0
    set prevTime 0

    # Retrive captured packets
    captureBuffer get $chassisId $card $port
    set numCapturedPkts [captureBuffer cget -numFrames]
    puts "Captured $numCapturedPkts pkts (expected: $expPktCnt)"
    if {$numCapturedPkts < $expPktCnt} {
        return $FAILED
    }
    captureBuffer get $chassisId $card $port 1 $numCapturedPkts
    for {set f 1} {$f <= $numCapturedPkts} {incr f} {
        after 50
        captureBuffer getframe $f
        after 50
        set capFrame [captureBuffer cget -frame]
        puts "TimeStamp of frame$f :  [captureBuffer cget -timestamp]"

        set mismatch 0
        foreach {startIndex endIndex expectedVal} $matchFieldList {
            puts "Obtained Pattern: [lrange $capFrame $startIndex $endIndex] \
                  Expected Pattern: $expectedVal"
            if {[lrange $capFrame $startIndex $endIndex] != $expectedVal} {
                set mismatch 1
                puts "Obtained: [lrange $capFrame $startIndex $endIndex] \
                      Expected: $expectedVal ---> No Match"
                break
            }
        }

        if {$mismatch == 0} {
            puts "All Field Patterns Matched !!!"
            set isError 0
            incr count

            set prevTime $curTime
            set curTime [captureBuffer cget -timestamp]
            
            if {$prevTime != 0} {
                set obsTimeDiff [expr double ([expr $curTime.0 - $prevTime.0])]
                set timeDiff [expr $obsTimeDiff/1000000000]
                
                puts "time diff $timeDiff"
                if {$timeDiff < $mintime || $timeDiff > $maxtime} {
                    puts "Time diff between two PDUs is not with in range.....$timeDiff.."
                } else {
                    puts "Time diff between LACPDU with in range ......$timeDiff.."
                    incr count1
                }
            }
        }
        if {$count != $expPktCnt && $expPktCnt != 1} {
            puts "Not able to get expected no of packet : expPktCount/rcvdPktCont :\
                 <$expPktCnt>/<$count>"
            return $FAILED
        }
    }
    
    puts "count with time diff is: $count1"
    if {$expPktCnt1 > $count1 &&  $expPktCnt1 != 1} {
        puts "Not able to get expected no of packets with timediff : \
             expPktCount/rcvdPktCount : <$expPktCnt1>/<$count1>"
        return $FAILED
    }
    puts " packets with timediff : expPktCount/rcvdPktCount : \
         <$expPktCnt1>/<$count1>"
    puts "Packet Verification Complete Successfully"
    return $PASSED
}

proc verifyTimestamp {chassis card port choise} {
    ixInitialize  $chassis
    chassis get   $chassis
    set chassisId [chassis cget -id]
    port get      $chassisId $card $port
    
    puts "Getting the ownership details..."
    set loginName [port cget -owner]
    puts "Logging in using the $loginName"
    ixLogin $loginName

    set count           0
    set PASSED          0
    set FAILED          1
    set curTime         0
    set prevTime        0
    set packetTimeStamp 0
    port get $chassisId $card $port

    puts "$chassisId $card $port------------------"

    # Retrive captured packets
    captureBuffer get $chassisId $card $port
    set numCapturedPkts [captureBuffer cget -numFrames]

    if {$numCapturedPkts < 1} {
                puts "No of packet is less than 1..."
        return $FAILED
    }

    captureBuffer get $chassisId $card $port 1 $numCapturedPkts
    set matchFieldList {0 5 "01 80 C2 00 00 02" \
                        12 13 "88 09" \
                        14 14 "01" \
                        15 15 "01" \
                        16 16 "01" \
                        17 17 "14" \
                        33 35 "00 00 00" \
                        36 36 "02" \
                        37 37 "14" \
                        53 55 "00 00 00" \
                        56 56 "03" \
                        57 57 "10"}
    if {$choise == 1} {
        for {set f 1} {$f <= $numCapturedPkts} {incr f} {
            after 50
            captureBuffer getframe $f
            after 50
            
            set capFrame [captureBuffer cget -frame]
            foreach {startIndex endIndex expectedVal} $matchFieldList {
                puts "Obtained Pattern: [lrange $capFrame $startIndex $endIndex] \
                      Expected Pattern: $expectedVal"
                if {[lrange $capFrame $startIndex $endIndex] != $expectedVal} {
                    set mismatch 1
                    puts "Obtained: [lrange $capFrame $startIndex $endIndex] \
                        Expected: $expectedVal ---> No Match"
                    break
                } else {
                     set packetTimeStamp [captureBuffer cget -timestamp]
                }
            }
        }
    } elseif {$choise == 2} {
        for {set f 3} {$f <= $numCapturedPkts} {incr f} {
            after 50
            captureBuffer getframe $f
            after 50
            set capFrame [captureBuffer cget -frame]

            set getBytes "0x[lindex $capFrame 32]"
            set getBytes1 "0x[lindex $capFrame 52]"

            puts "Get Byte is <$getBytes> and <$getBytes1> frame is :---- $capFrame"

            set intByte [format %d $getBytes]
            set intByte1 [format %d $getBytes1]

            if {[expr $intByte & 128] == 128 && [expr $intByte1 & 8] == 0 && \
                [expr $intByte1 & 2] == 0} {
                set packetTimeStamp [captureBuffer cget -timestamp]
                break
            }
        }
     }  elseif {$choise == 3} {
        for {set f 3} {$f <= $numCapturedPkts} {incr f} {
            after 50
            captureBuffer getframe $f
            after 50
            set capFrame [captureBuffer cget -frame]

            set getBytes  "0x[lindex $capFrame 32]"
            set getBytes1 "0x[lindex $capFrame 52]"
            puts "Get Byte is <$getBytes> frame is :---- $capFrame"

            set intByte [format %d $getBytes]
            set intByte1 [format %d $getBytes1]

            if {[expr $intByte & 64] == 64 && [expr $intByte1 & 1] == 0  && \
                [expr $intByte1 & 2] == 0 && [expr $intByte1 & 4] == 0   && \
                [expr $intByte1 & 8] == 8 && [expr $intByte1 & 16] == 16 && \
                [expr $intByte1 & 32] == 0 && [expr $intByte1 & 64] == 0 && \
                [expr $intByte1 & 128] == 128} {
                set packetTimeStamp [captureBuffer cget -timestamp]
                break
            }
        }
    } else {
        puts "Wrong Optiong given..."
        return $FAILED
    }
    return $packetTimeStamp
}

