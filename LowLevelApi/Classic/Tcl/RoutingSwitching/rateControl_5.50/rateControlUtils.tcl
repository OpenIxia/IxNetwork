###############################################################################
# General Procs using IxTclHal                                                #
###############################################################################

#------------------------------------------------------------------------------
# PROCEDURE  : ixExplorerCheckAttributeValue
# PURPOSE    : To check the IxExplorer Attributes
# PARAMETERS : object, array of attr and expectedVal
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#------------------------------------------------------------------------------
proc ixExplorerCheckAttributeValue {object arr} {
    set isError 1
    array set expectProp $arr
    #parray expectProp

    foreach attr [array names expectProp] {
       set attVal [$object cget -$attr]
       set val $expectProp($attr)

       puts "\t attVal = $attVal (-$attr) expectProp = $val"
       if {[string tolower $attVal] != [string tolower $val]} {
           puts "\t -$attr : $attVal (expected $val) --> did not match!"
           return $isError
       }
    }

    set isError 0
    return $isError
}

#------------------------------------------------------------------------------
# PROCEDURE  : connectChassis
# PURPOSE    : To connect to the Chassis and reserve ports
# PARAMETERS : chassisIp, card and port
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#------------------------------------------------------------------------------
proc ixExplorerConnectChassis {chassisIp card port} {

    set error 1

    if {[ixInitialize $chassisIp]} {
        puts "Could not connect to Chassis $chassisIp !!!"
        return $error
    }
    puts "Connect to the Chassis $chassisIp successfully !!!"

    chassis get $chassisIp
    set chassisId [chassis cget -id]
    port get $chassisId $card $port
    set loginName [port cget -owner]

    if {[ixLogin $loginName]} {
        puts "Could not login in the Chassis $chassisIp !!!"
        return $error
    }
    puts "Log in successfully with user: $loginName !!!"

    if {[chassis refresh $chassisId]} {
        puts "Could not refresh Chassis $chassisIp"
        return $error
    }
    puts "Refreshed the Chassis $chassisIp !!!"

    set error 0
    return $error
}


#------------------------------------------------------------------------------
# PROCEDURE  : disconnectChassis
# PURPOSE    : Disconnect from the Chassis
# PARAMETERS : chassisIp
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#------------------------------------------------------------------------------
proc ixExplorerDisconnectChassis {chassisIp} {

   set error 1

   if {[ixDisconnectFromChassis $chassisIp]} {
      puts "Could not disconnect from Chassis $chassisIp"
      return $error
   }
   puts "Successfully disconnected from the Chassis $chassisIp !!!"

   set error 0
   return $error
}


proc  rebootPortOnTheChassis {chIp card port} {
    set result -1
    if [catch {set result [ixInitialize $chIp] } err] {
        logSummary [format "%-14s : %-53s : %-7s" "Error" "" "$err"]
        return $result
    }

    if {!$result} {
        set ch [chassis cget -id]
        ixClearOwnership [list [list $ch $card $port]] force
        portCpu reset $ch $card $port
        port setFactoryDefaults $ch $card $port
        port write $ch $card $port
        #portCpu reset $ch $card $port
        after 2000
    }

    return $result
}

###############################################################################
# PACKET STRUCTURE VERIFICATION                                               #
###############################################################################

#------------------------------------------------------------------------------
# PROCEDURE  : verifyCapturedPackets
# PURPOSE    : Verifying expected field value in Captured Packets
# PARAMETERS : chassis -
#              card -
#              port -
#              matchFieldList - list of {startIndex endIndex expectedVal}
#              expPktCnt - {default value 1}
#              packetLengthList - expected packet length (length will be
#              matched). If one has to match between max size and min size
#              this should be [list $min $max]
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#------------------------------------------------------------------------------
proc verifyCapturedPackets {chassis card port matchFieldList {expPktCnt 1} \
         {packetLengthList {}}} {

    set isError 1

    puts "Initializing through IxTclHal...."
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
        ixExplorerDisconnectChassis $chassis
        return $isError
    }

    set isLengthToBeMatched [llength $packetLengthList]
    captureBuffer get $chassisId $card $port 1 $numCapturedPkts
    for {set f 1} {$f <= $numCapturedPkts} {incr f} {

        after 50
        set a [captureBuffer getframe $f]
        after 50

        set capframe  [captureBuffer cget -frame]
        set frameSize [captureBuffer cget -length]

        set mismatch     0
        set sizeMismatch 0

        if {$isLengthToBeMatched} {
            set expectedMinPktLength [lindex $packetLengthList 0]
            set expectedMaxPktLength [lindex $packetLengthList end]
            if {($frameSize >= $expectedMinPktLength) && \
                ($frameSize <= $expectedMaxPktLength)} {
                set sizeMismatch 0
             } else {
                set sizeMismatch 1
             }
        }


        if {$sizeMismatch == 0} {
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
        } ;# endif sizeMismatch

         if {$mismatch == 0} {
            puts "All Field Patterns Matched !!!"
            set isError 0
            ixExplorerDisconnectChassis $chassis
            return $isError
        }
    } ;# end of swarching in buffer

    if {$mismatch == 1} {
        puts "Not all Field Patterns Matched !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }
}


###############################################################################
# PROCEDURE  : checkRateControlThroughCapture
# PURPOSE    : returns the timestamp of the captured packets
# PARAMETERS : chassis
#              card
#              port
#              matchFieldList- list of {startIndex endIndex expectedVal}
#              expPktCount- Number of pkts matching matchFieldList
#              rateList- list of {expPktinConfiguredInterval
#                        configuredIntervalinSec}
# RETURN     : (BOOL)  - 0 for Pass ~ 1 for Fail
###############################################################################
proc checkRateControlThroughCapture {chassis card port matchFieldList \
     expPktCount rateList } {
    set isError 1

    # Connecting to the Chassis
    puts "Connecting to the Chassis $chassis ..."
    if {[ixInitialize $chassis]} {
        puts "Could not connect to Chassis $chassis !!!"
        return $isError
    }
    puts "Connected to the Chassis $chassis successfully !!!"

    # Get Chassis ID
    set chassisId [ixGetChassisID $chassis]

    # Login and take ownership
    puts "Login into the Chassis with IxNetwork UserId ..."
    if {[port get $chassisId $card $port]} {
        puts "Could not perform port get !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }
    set loginName [port cget -owner]
    if {[ixLogin $loginName]} {
        puts "Could not login in the Chassis $chassisIp !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }
    puts "Log in successfully with user: $loginName !!!"

    # Retrieve captured packets
    puts "Retrieving captured packets ..."
    if {[capture get $chassisId $card $port]} {
        puts "Could not perform capture get !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }

    if {[catch {set numCapturedPkts [capture cget -nPackets]} err] == 1} {
        puts "Could not perform capture cget: $err !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }
    puts "No. of packets captured: $numCapturedPkts !!!"

    # Get the batch of frames
    if {[captureBuffer get $chassisId $card $port 1 $numCapturedPkts]} {
        puts "Could not perform captureBuffer get !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }

    # Matching the expected packet and retrieving its timestamp
    puts "Retreiving timestamp of matched packets ..."
    set matchedPktCount 0
    for {set f 1} {$f <= $numCapturedPkts} {incr f} {
        if {[captureBuffer getframe $f]} {
            puts "Could not perform captureBuffer getframe $f !!!"
            ixExplorerDisconnectChassis $chassis
            return $isError
        }

        if {[catch {set capframe [captureBuffer cget -frame]} err] == 1} {
            puts "Could not perform captureBuffer cget -frame: $err !!!"
            ixExplorerDisconnectChassis $chassis
            return $isError
        }
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
            incr matchedPktCount

            # Get Time Stamp in nanoseconds
            set timeStamp1 [captureBuffer cget -timestamp]

            array set timeStamp {}
            set timeStamp($matchedPktCount) $timeStamp1
        }
    }


    # Verify Expected no. of matched packets
    if {$matchedPktCount < $expPktCount} {
         puts "Failed: Matched packets=$matchedPktCount; \
              Expected packets=$expPktCount !!!"
         ixExplorerDisconnectChassis $chassis
         return $isError
    }
    puts "Passed: Matched packets=$matchedPktCount; \
          Expected packets=$expPktCount !!!"

    # Verify Rate
    set expPkt_configuredInterval [lindex $rateList 0]
    set configuredInterval [lindex $rateList 1]

    set numSlotsToCheck [expr $expPktCount/$expPkt_configuredInterval]
    set pkt_configuredInterval 0
    set initialPktIndex 1
    set failed 0
    for {set i 1} {$i <= $matchedPktCount} {incr i} {
        set intv [expr ($timeStamp($i) - $timeStamp($initialPktIndex))]
        if { [expr double ($intv)/1000000000] > $configuredInterval } {
            incr numSlotsToCheck -1
            if {($pkt_configuredInterval > $expPkt_configuredInterval) || \
                ($pkt_configuredInterval == 0)} {
                puts "Fail: Actual Pkt Recv = $pkt_configuredInterval \
                      Expected Pkt=$expPkt_configuredInterval \
                      in $configuredInterval sec !!!"
                set failed 1
            } else {
                puts "Pass: Actual Pkt Recv = $pkt_configuredInterval \
                      Expected Pkt=$expPkt_configuredInterval \
                      in $configuredInterval sec !!!"
            }
            incr pkt_configuredInterval
            set initialPktIndex $pkt_configuredInterval
            set pkt_configuredInterval 0
            if {$numSlotsToCheck == 0} {
                if {$failed == 1} {
                    puts "All brusts doesn't have expected Number of Pkts..."
                    ixExplorerDisconnectChassis $chassis
                    return $isError
                }
                puts "All brusts have expected Number of Pkts..."
                break
            }
        }
        incr pkt_configuredInterval
    }

    set isError 0
    ixExplorerDisconnectChassis $chassis
    return $isError
}


###############################################################################
# PROCEDURE  : verifyRateControlThroughCapture
# PURPOSE    : returns the timestamp of the captured packets
# PARAMETERS : chassis
#              card
#              port
#              matchFieldList- list of {startIndex endIndex expectedVal}
#              pktCountList- list of {expPktCount pktCountFlag}
#                   - pktCountFlag can have 3 values:
#                   - exact-Exact pktCount, max- Max pktCount min- Min pktCount
#              rateList- list of {expRate rateFlag tolerance}
#                   - expRate should be mentioned in packets per sec
#                   - rateFlag can have 3 values:
#                           avg-with tolerace limit exact-Exact max-
#                           Max Rate min- Min rate
#                   - tol- Tolerance; Default Value is 10%
# RETURN     : BOOL)    - 0 for Pass ~ 1 for Fail
###############################################################################
proc verifyRateControlThroughCapture {chassis card port matchFieldList
                                      pktCountList rateList } {
    set isError 1

    # Connecting to the Chassis
    puts "Connecting to the Chassis $chassis ..."
    if {[ixInitialize $chassis]} {
        puts "Could not connect to Chassis $chassis !!!"
        return $isError
    }
    puts "Connected to the Chassis $chassis successfully !!!"

    # Get Chassis ID
    set chassisId [ixGetChassisID $chassis]

    # Login and take ownership
    puts "Login into the Chassis with IxNetwork UserId ..."
    if {[port get $chassisId $card $port]} {
        puts "Could not perform port get !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }
    set loginName [port cget -owner]
    if {[ixLogin $loginName]} {
        puts "Could not login in the Chassis $chassisIp !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }
    puts "Log in successfully with user: $loginName !!!"

    # Retrieve captured packets
    puts "Retrieving captured packets ..."
    if {[capture get $chassisId $card $port]} {
        puts "Could not perform capture get !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }

    if {[catch {set numCapturedPkts [capture cget -nPackets]} err] == 1} {
        puts "Could not perform capture cget: $err !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }
    puts "No. of packets captured: $numCapturedPkts !!!"

    # Get the batch of frames
    if {[captureBuffer get $chassisId $card $port 1 $numCapturedPkts]} {
        puts "Could not perform captureBuffer get !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }

    # Matching the expected packet and retrieving its timestamp
    puts "Retreiving timestamp of matched packets ..."
    set matchedPktCount 0
    for {set f 1} {$f <= $numCapturedPkts} {incr f} {
        if {[captureBuffer getframe $f]} {
            puts "Could not perform captureBuffer getframe $f !!!"
            ixExplorerDisconnectChassis $chassis
            return $isError
        }

        if {[catch {set capframe [captureBuffer cget -frame]} err] == 1} {
            puts "Could not perform captureBuffer cget -frame: $err !!!"
            ixExplorerDisconnectChassis $chassis
            return $isError
        }
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
            incr matchedPktCount

            # Get Time Stamp in nanoseconds
            set timeStamp1 [captureBuffer cget -timestamp]

            array set timeStamp {}
            set timeStamp($matchedPktCount) $timeStamp1
        }
    }

    # Verify Expected no. of matched packets
    set expPktCount [lindex $pktCountList 0]
    set pktCountFlag [lindex $pktCountList 1]
    switch $pktCountFlag {
        "exact" {if {$matchedPktCount != $expPktCount} {
                     puts "Failed: Matched packets=$matchedPktCount; \
                           Expected packets=$expPktCount !!!"
                     ixExplorerDisconnectChassis $chassis
                     return $isError
                }}
        "max" {if {$matchedPktCount > $expPktCount} {
                   puts "Failed: Matched packets=$matchedPktCount; \
                         Expected packets=$expPktCount !!!"
                   ixExplorerDisconnectChassis $chassis
                   return $isError
              }}
        "min" {if {$matchedPktCount < $expPktCount} {
                   puts "Failed: Matched packets=$matchedPktCount; \
                        Expected packets=$expPktCount !!!"
                   ixExplorerDisconnectChassis $chassis
                   return $isError
              }}
        default {puts "Wrong Packet Count Flag: $pktCountFlag !!!"
                 ixExplorerDisconnectChassis $chassis
                 return $isError
                }
    }
    puts "Passed: Matched packets=$matchedPktCount; \
          Expected packets=$expPktCount !!!"

    # Verify Rate
    set expRate [lindex $rateList 0]
    set rateFlag [lindex $rateList 1]
    set tol [lindex $rateList 2]
    set minRate $expRate
    set maxRate $expRate
    if {$tol != 0} {
        # Expected Rate Limits
        set minRate [expr ($expRate - ($expRate * $tol)/100)]
        set maxRate [expr ($expRate + ($expRate * $tol)/100)]
    }

    # Actual Time Interval
    puts "1st Pkt TS = $timeStamp(1) ~ \
          $expPktCount th Pkt TS $timeStamp($expPktCount)"
    set actTime [expr ($timeStamp($expPktCount) - $timeStamp(1))]
    # Convert Time Stamp to seconds
    set actTimeInt [expr double ($actTime)/1000000000]
    set actRate [expr double ($expPktCount)/$actTimeInt]

    switch $rateFlag {
        "avg" {if {($actRate < $minRate) || ($actRate > $maxRate)} {
                     puts "Failed: Actual Rate=$actRate; \
                           Expected rate=$expRate packets per sec !!!"
                     ixExplorerDisconnectChassis $chassis
                     return $isError
                }}
        "exact" {if {$actRate != $expRate} {
                     puts "Failed: Actual Rate=$actRate; \
                          Expected rate=$expRate packets per sec !!!"
                     ixExplorerDisconnectChassis $chassis
                     return $isError
                }}
        "max" {if {$actRate > $maxRate} {
                   puts "Failed: Actual Rate=$actRate; \
                         Expected rate=$expRate packets per sec !!!"
                   ixExplorerDisconnectChassis $chassis
                   return $isError
              }}
        "min" {if {$actRate < $minRate} {
                   puts "Failed: Actual Rate=$actRate; \
                         Expected rate=$expRate packets per sec !!!"
                   ixExplorerDisconnectChassis $chassis
                   return $isError
              }}
        default {puts "Wrong Rate Flag: $rateFlag !!!"
                 ixExplorerDisconnectChassis $chassis
                 return $isError
                }
    }
    puts "Passed: Actual Rate=$actRate; Expected rate=$expRate \
          packets per sec !!!"

    set isError 0
    return $isError
}

###############################################################################
# PROCEDURE  : checkInterBurstGapThroughCapture
# PURPOSE    : returns the timestamp of the captured packets
# PARAMETERS : chassis
#              card
#              port
#              matchFieldList- list of {startIndex endIndex expectedVal}
#              expPktCount- Number of pkts matching matchFieldList
#              expValList- list of {expPktinConfiguredInterval
#                          configuredIntervalinSec}
# RETURN     : BOOL)    - 0 for Pass ~ 1 for Fail
###############################################################################
proc checkInterBurstGapThroughCapture {chassis card port matchFieldList \
         expPktCount expValList {exachMatch 0}} {
    set isError 1

    # Connecting to the Chassis
    puts "Connecting to the Chassis $chassis ..."
    if {[ixInitialize $chassis]} {
        puts "Could not connect to Chassis $chassis !!!"
        return $isError
    }
    puts "Connected to the Chassis $chassis successfully !!!"

    # Get Chassis ID
    set chassisId [ixGetChassisID $chassis]

    # Login and take ownership
    puts "Login into the Chassis with IxNetwork UserId ..."
    if {[port get $chassisId $card $port]} {
        puts "Could not perform port get !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }
    set loginName [port cget -owner]
    if {[ixLogin $loginName]} {
        puts "Could not login in the Chassis $chassisIp !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }
    puts "Log in successfully with user: $loginName !!!"

    # Retrieve captured packets
    puts "Retrieving captured packets ..."
    if {[capture get $chassisId $card $port]} {
        puts "Could not perform capture get !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }

    if {[catch {set numCapturedPkts [capture cget -nPackets]} err] == 1} {
        puts "Could not perform capture cget: $err !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }
    puts "No. of packets captured: $numCapturedPkts !!!"

    # Get the batch of frames
    if {[captureBuffer get $chassisId $card $port 1 $numCapturedPkts]} {
        puts "Could not perform captureBuffer get !!!"
        ixExplorerDisconnectChassis $chassis
        return $isError
    }

    # Matching the expected packet and retrieving its timestamp
    puts "Retreiving timestamp of matched packets ..."
    set matchedPktCount 0
    for {set f 1} {$f <= $numCapturedPkts} {incr f} {
        if {[captureBuffer getframe $f]} {
            puts "Could not perform captureBuffer getframe $f !!!"
            ixExplorerDisconnectChassis $chassis
            return $isError
        }

        if {[catch {set capframe [captureBuffer cget -frame]} err] == 1} {
            puts "Could not perform captureBuffer cget -frame: $err !!!"
            ixExplorerDisconnectChassis $chassis
            return $isError
        }
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
            incr matchedPktCount

            # Get Time Stamp in nanoseconds
            set timeStamp1 [captureBuffer cget -timestamp]

            array set timeStamp {}
            set timeStamp($matchedPktCount) $timeStamp1

        }
    }


    # Verify Expected no. of matched packets
    if {$matchedPktCount < $expPktCount} {
         puts "Failed: Matched packets=$matchedPktCount; \
              Expected packets=$expPktCount !!!"
         ixExplorerDisconnectChassis $chassis
         return $isError
    }
    puts "Passed: Matched packets=$matchedPktCount; \
          Expected packets=$expPktCount !!!"

    # Verify Rate
    set expPkt_configuredInterval [lindex $expValList 0]
    set configuredInterval [lindex $expValList 1]

    set numSlotsToCheck [expr $expPktCount/$expPkt_configuredInterval]
    set pkt_configuredInterval 0
    set lastPktIndexOfSlot  $expPkt_configuredInterval
    set firstPktIndexOfNextSlot [expr $lastPktIndexOfSlot + 1]
    set failed 0

    for {set i 1} {$i <= $numSlotsToCheck} {incr i} {
        set intv [expr double ($timeStamp($firstPktIndexOfNextSlot) - \
            $timeStamp($lastPktIndexOfSlot))/1000000000]
        puts "$timeStamp($firstPktIndexOfNextSlot)"
        puts "$timeStamp($lastPktIndexOfSlot)"
        if {$exachMatch == 1} {
            if {($intv > [expr $configuredInterval + 2]) ||  \
                ($intv < $configuredInterval)} {
               puts "Fail: Actual Gap = $intv Expected \
                     Gap =$configuredInterval !!!"
               set failed 1
            } else {
               puts "Pass: Actual Gap = $intv Expected \
                     Gap =$configuredInterval !!!"
            }
        } else {
            if { $intv < $configuredInterval } {
                puts "Fail: Actual Gap = $intv Expected \
                      Gap =$configuredInterval !!!"
                set failed 1
            } else {
                puts "Pass: Actual Gap = \
                     $intv Expected Gap =$configuredInterval !!!"
            }
        }
        incr lastPktIndexOfSlot $expPkt_configuredInterval
        set firstPktIndexOfNextSlot [expr $lastPktIndexOfSlot + 1]
    }

    if {$failed == 1} {
        puts "All inter brust gaps not per configuration..."
        ixExplorerDisconnectChassis $chassis
        return $isError
    }
    puts "All inter burst gaps per configuration..."

    set isError 0
    ixExplorerDisconnectChassis $chassis
    return $isError
}
