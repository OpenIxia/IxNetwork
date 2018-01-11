#
# CFM Traffic Utils to be used in the Traffic test cases
#


################################################################################
# Procedure : generateApplyTraffic
# Purpose   : To Generate and Apply Traffic
# Parameters    : None
# Return    : (Bool) 0 - Applied Traffic 1 - Failed to Apply Traffic
################################################################################
proc generateApplyTraffic {} {

    set flag 1
    set traffic [ixNet getRoot]/traffic
    # Generate Traffic
    set genTraffic [ixNet setAtt $traffic -refreshLearnedInfoBeforeApply  true]
    if {$genTraffic != "::ixNet::OK"} {
        puts "Not able to generate  the traffic.."
        return $flag
    }
    after 10000

    puts "Appling the traffic...."
    set appTraffic [::ixNet exec apply $traffic]
    if {$appTraffic != "::ixNet::OK"} {
        puts "Not able to apply the traffic.."
        return $flag
    }
    after 10000
    set flag 0
    return $flag
}

################################################################################
#Procedure  : startTraffic
#Purpose    : To Start the Traffic
#Parameters     : None
#Return     : (Bool) 0 - Started Traffic Successfully 1 - Failed to Start the Traffic
################################################################################
proc startTraffic {} {
    set flag 1
    set traffic [ixNet getRoot]/traffic
    puts "Starting the traffic..."
    set startTraffic [::ixNet exec start $traffic]
    if {$startTraffic != "::ixNet::OK"} {
        puts "Not able to start the traffic.."
    return $flag
    }
    set flag 0
    return $flag
}

################################################################################
#Procedure  :stopTraffic
#Purpose    : To Stop the Traffic
#Parameters : None
#Return     : (Bool) 0 - Stopped Traffic Successfully 1 - Failed to Stop the Traffic
################################################################################

proc stopTraffic {} {
    set flag 1
    set traffic [ixNet getRoot]/traffic
    puts "Stopping the traffic...."
    set stopTraffic [::ixNet exec stop $traffic]
    if {$stopTraffic != "::ixNet::OK"} {
        puts "Not able to stop the traffic.."
        return $flag
    }
    after 10000

    set flag 0
    return $flag
}

################################################################################
#Procedure  : captureMode
#Purpose    : To change the mode of the Port p2 to Capture Mode
#Parameters : port (port)
#Return     : None
################################################################################

proc captureMode {port} {
    ixNet setAttribute $port -rxMode capture
    ixNet setAttribute $port/capture -hardwareEnabled true
    ixNet commit
    after 5000
}

################################################################################
#Procedure  : measureMode
#Purpose    : To change the mode of the port p2 to measure flow mode
#Parameters : port (port )
#Return     : None
################################################################################

proc measureMode {port} {
    ixNet setAttribute $port -rxMode measure
    ixNet setAttribute $port/capture -hardwareEnabled false
    ixNet commit
    after 5000
}
################################################################################
#Procedure  : TxRxCalculation
#Purpose    : To calculate the Tx - Rx Rate and to check if the Rx rate is equal to expected Rx Rate
#Parameters : TxFrame Value RxFrame Value
#Return     : (Bool) 0 - If the Rx Frame is greater than or equal to delta percentage  the value of Tx Frame
################################################################################

proc TxRxCalculation {TxFrame RxFrame {tolerance 15} } {
    set flag 1
    set minRxFrame [expr ($TxFrame - ($TxFrame * $tolerance)/100)]
    puts "Frames Received: $RxFrame Frames Transmitted: $TxFrame (considering 15%% tolerence $minRxFrame)"
    if {$RxFrame < $minRxFrame} {
        puts "Frames Received is less than Frames Transmitted (considering 15%% tolerence)"
        return $flag
    }

    set flag 0
    return $flag
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

proc verifyCapturedPackets {chassis card port matchFieldList {expPktCnt 1}} {
    set isError 1

    puts "Initilizing thorugh IxTclHal...."
    ixInitialize $chassis
    chassis get $chassis
    set chassisId [chassis cget -id]

    port get $chassisId $card $port
    set putsinName [port cget -owner]
    ixLogin $putsinName
    puts "Logging in using the $putsinName"

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
        captureBuffer getframe $f
        after 50
        set capframe [captureBuffer cget -frame]
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


proc pktFormat {packet} {
    set lenPkt [string length $packet]
    set cntr 00
    puts "=========================================================="
    for {set i 0} {$i <= $lenPkt} {incr i 48} {
    if { $cntr < 100 } {puts -nonewline "00$cntr     "} else {puts -nonewline "0$cntr     "}
        puts -nonewline [string range $packet $i [expr $i+23]]
        puts -nonewline "  "
        puts [string range $packet [expr $i+24] [expr $i+47]]
        set cntr [expr $cntr + 10]
    }
    puts "=========================================================="
}