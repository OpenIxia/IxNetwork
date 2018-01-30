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
    puts "Frames Received: $RxFrame Frames Transmitted: $TxFrame (considering 15% tolerence $minRxFrame)"
    if {$RxFrame < $minRxFrame} {
        puts "Frames Received is less than Frames Transmitted (considering 15% tolerence)"
        return $flag
    }

    set flag 0
    return $flag
}

