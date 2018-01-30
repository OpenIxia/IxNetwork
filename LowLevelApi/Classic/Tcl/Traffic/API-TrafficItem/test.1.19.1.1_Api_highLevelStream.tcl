#------------------------------------------------------------------------------
# File Name - test.1.10.1.1_Api_highLevelStream.tcl
# Description:
#            1) Load the scriptgen file using Tcl
#            2) Verify the configuration
#            3) Maipulate the attributes and verify its value again what was set
# Topology  - B2B
#-------------------------------------------------------------------------------
# /traffic/trafficItem:1/highLevelStream:1 ::
#     -destinationMacMode
#     -crc
#     -preambleFrameSizeMode
# /traffic/trafficItem:1/highLevelStream:1/framePayload ::
#     -type
#     -customRepeat
# /traffic/trafficItem:1/highLevelStream:1/frameSize ::
#    -fixedSize
#    -incrementFrom
#    -incrementStep
#    -incrementTo
#    -presetDistribution
#    -quadGaussian
#    -randomMax
#    -randomMin
#    -type
#    -weightedPairs
# /traffic/trafficItem:1/highLevelStream:1/frameRate ::
#     -bitRateUnitsType
#     -type
#     -enforceMinimumInterPacketGap
#     -rate
# /traffic/trafficItem:1/highLevelStream:1/transmissionControl ::
#     -interBurstGap
#     -frameCount
#     -interStreamGap
#     -type
#     -iterationCount
#     -minGapBytes
#     -startDelay
#-------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

#-------------------------------------------------------------------------------
# PROCEDURE : verifyhighLevelStreamMainAttributes
# PURPOSE   : to verify the following attributes
# /traffic/trafficItem:1/highLevelStream:1 ::
#     -destinationMacMode
#     -crc
#     -preambleFrameSizeMode
#-------------------------------------------------------------------------------
proc verifyhighLevelStreamMainAttributes {highLevelStreamMain} {
    set isError 1

    if {[setAndCheckAttributeValue $highLevelStreamMain \
        "destinationMacMode" {"arp" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $highLevelStreamMain \
        "destinationMacMode"  {"manual" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $highLevelStreamMain \
        "destinationMacMode"  {"arp" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $highLevelStreamMain \
        "destinationMacMode" {"manual" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $highLevelStreamMain "crc" \
        {"goodCrc" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $highLevelStreamMain "crc" \
        {"badCrc" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $highLevelStreamMain \
        "preambleFrameSizeMode" {"custom" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $highLevelStreamMain \
        "preambleFrameSizeMode" {"auto" y}] == 1} {
        return $isError
    }

    set isError 0
    return $isError
}


#------------------------------------------------------------------------------
# PROCEDURE : verifyFramePayloadAttributes
# PURPOSE   : to verify the following attributes
# /traffic/trafficItem:1/highLevelStream:1/framePayload ::
#     -type
#     -customRepeat
#------------------------------------------------------------------------------
proc verifyFramePayloadAttributes {framePayload} {
    set isError 1

    if {[setAndCheckAttributeValue $framePayload "customPattern" \
        {"5" y}] == 1} {
         return $isError
    }

    if {[setAndCheckAttributeValue $framePayload "type" \
        {"custom" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $framePayload "type" \
        {"decrementByte" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $framePayload "type" \
        {"decrementWord" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $framePayload "type" \
        {"incrementWord" y}] == 1} {
            return $isError
    }

    if {[setAndCheckAttributeValue $framePayload "type" \
        {"random" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $framePayload "type" \
        {"incrementByte" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $framePayload "customRepeat" \
        {"False" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $framePayload "customRepeat" \
        {"True" y}] == 1} {
        return $isError
    }

    set isError 0
    return $isError
}


#------------------------------------------------------------------------------
# PROCEDURE : verifyFrameSizeAttributes
# PURPOSE   : to verify the following attributes
# /traffic/trafficItem:1/highLevelStream:1/frameSize ::
#    -fixedSize
#    -incrementFrom
#    -incrementStep
#    -incrementTo
#    -presetDistribution
#    -quadGaussian
#    -randomMax
#    -randomMin
#    -type
#    -weightedPairs
#------------------------------------------------------------------------------
proc verifyFrameSizeAttributes {frameSize} {
    set isError 1

    # Set type to "weightedPairs"
    if {[setAndCheckAttributeValue $frameSize "type" \
        {"weightedPairs" y}] == 1} {
        return $isError
    }

    # Set the weightedPairs/weightedPairs values
    if {[setAndCheckAttributeValue $frameSize "weightedPairs" \
        {"50 50" y}] == 1} {
        return $isError
    }

    # Set type to increment
    if {[setAndCheckAttributeValue $frameSize "type" \
        {"increment" y}] == 1} {
        return $isError
    }

    # Set increment/incrementStep
    if {[setAndCheckAttributeValue $frameSize "incrementStep" \
        {"5" y}] == 1} {
        return $isError
    }

    # Set increment/incrementTo
    if {[setAndCheckAttributeValue $frameSize "incrementTo" \
        {"1518" y}] == 1} {
        return $isError
    }

    # Set increment/incrementFrom
    if {[setAndCheckAttributeValue $frameSize "incrementFrom" \
        {"64" y}] == 1} {
        return $isError
    }

    # Set type to fixed
    if {[setAndCheckAttributeValue $frameSize "type" \
        {"fixed" y}] == 1} {
        return $isError
    }

    # Set fixed/fixedSize
    if {[setAndCheckAttributeValue $frameSize "fixedSize" \
        {"100" y}] == 1} {
        return $isError
    }

    # Set type random
    if {[setAndCheckAttributeValue $frameSize "type" \
        {"random" y}] == 1} {
        return $isError
    }

    # set random/randomMax
    if {[setAndCheckAttributeValue $frameSize "randomMax" \
        {"1518" y}] == 1} {
        return $isError
    }

    # random/randomMin
    if {[setAndCheckAttributeValue $frameSize "randomMin" \
        {"512" y}] == 1} {
        return $isError
    }

    # Set type to presetDistribution
    if {[setAndCheckAttributeValue $frameSize "type" \
        {"presetDistribution" y}] == 1} {
        return $isError
    }

    # Set presetDistribution/presetDistribution type
    if {[setAndCheckAttributeValue $frameSize "presetDistribution" \
        {"imix" y}] == 1} {
        return $isError
    }

    # set type to quadGaussian
    if {[setAndCheckAttributeValue $frameSize "type" \
        {"quadGaussian" y}] == 1} {
        return $isError
    }

    # set quadGaussian/quadGaussian values
    set validList1 [list 50.000000   50.000000 1 \
                         51.000000   55.000000 2 \
                         200.000000 100.000000 0 \
                         200.000000 100.000000 0]

    if {[setAndCheckAttributeValue $frameSize "quadGaussian" \
        [list  $validList1 y]] == 1} {
        return $isError
    }

    set isError 0
    return $isError
}


#------------------------------------------------------------------------------
# PROCEDURE : verifyFrameRateAttributes
# PURPOSE   : to verify the following attributes
# /traffic/trafficItem:1/highLevelStream:1/frameRate ::
#     -bitRateUnitsType
#     -type
#     -enforceMinimumInterPacketGap
#     -rate
#------------------------------------------------------------------------------
proc verifyFrameRateAttributes {frameRate} {
    set isError 1

    # Set valid value & verify

    # set bitRateUnits to bytesPerSec
    if {[setAndCheckAttributeValue $frameRate "bitRateUnitsType" \
        {"bytesPerSec" y}] == 1} {
        return $isError
    }

    # set bitRateUnits to kbytesPerSec
    if {[setAndCheckAttributeValue $frameRate "bitRateUnitsType" \
         {"kbytesPerSec" y }] == 1} {
        return $isError
    }

    # set bitRateUnits to mbytesPerSec
    if {[setAndCheckAttributeValue $frameRate "bitRateUnitsType" \
        {"mbytesPerSec" y}] == 1} {
        return $isError
    }

    # set bitRateUnits to bitsPerSec
    if {[setAndCheckAttributeValue $frameRate "bitRateUnitsType" \
        {"bitsPerSec" y}] == 1} {
        return $isError
    }

    # set rate to bitsPerSecond
    if {[setAndCheckAttributeValue $frameRate "type" \
        {"bitsPerSecond" y}] == 1} {
        return $isError
    }

    # set rate to framesPerSecond
    if {[setAndCheckAttributeValue $frameRate "type" \
        {"framesPerSecond" y}] == 1} {
        return $isError
    }

    # set rate to percentLineRate
    if {[setAndCheckAttributeValue $frameRate "type" \
        {"percentLineRate" y}] == 1} {
        return $isError
    }

    # set enforceMinimumInterPacketGap
    if {[setAndCheckAttributeValue $frameRate "enforceMinimumInterPacketGap" \
        {"5" y}] == 1} {
        return $isError
    }

    # set rate value
    if {[setAndCheckAttributeValue $frameRate "rate" \
        {"10.000000" y}] == 1} {
        return $isError
    }

    set isError 0
    return $isError
}


#------------------------------------------------------------------------------
# PROCEDURE : verifyTransmissionControlAttributes
# PURPOSE   : to verify the following attributes
# /traffic/trafficItem:1/highLevelStream:1/transmissionControl ::
#     -interBurstGap
#     -frameCount
#     -interStreamGap
#     -type
#     -iterationCount
#     -minGapBytes
#     -startDelay
#-------------------------------------------------------------------------------
proc verifyTransmissionControlAttributes {transmissionControl} {
    set isError 1

    # set transmissionControl/interBurstGap
    if {[setAndCheckAttributeValue $transmissionControl "interBurstGap" \
        {"5" y}] == 1} {
        return $isError
    }

    # set transmissionControl/frameCount
    if {[setAndCheckAttributeValue $transmissionControl "frameCount" \
        {"100" y}] == 1} {
        return $isError
    }

    # transmissionControl/interStreamGap
    if {[setAndCheckAttributeValue $transmissionControl "interStreamGap" \
        {"100" y}] == 1} {
        return $isError
    }

    # set transmission type auto
    if {[setAndCheckAttributeValue $transmissionControl "type" \
        {"auto" y}] == 1} {
        return $isError
    }

    # set transmission type fixedFrameCount
    if {[setAndCheckAttributeValue $transmissionControl "type" \
        {"fixedFrameCount" y}] == 1} {
        return $isError
    }

    # set transmission type custom
    if {[setAndCheckAttributeValue $transmissionControl "type" \
        {"custom" y}] == 1} {
        return $isError
    }

    # set transmission type continuous
    if {[setAndCheckAttributeValue $transmissionControl "type" \
        {"continuous" y}] == 1} {
        return $isError
    }

    # set transmission type fixedIterationCount
    if {[setAndCheckAttributeValue $transmissionControl "type" \
        {"fixedIterationCount" y }] == 1} {
        return $isError
    }

    # set transmissionControl iterationCount
    if {[setAndCheckAttributeValue $transmissionControl "iterationCount" \
        {"100" y}] == 1} {
        return $isError
    }

    # set transmissionControl minGapBytes
    if {[setAndCheckAttributeValue $transmissionControl "minGapBytes" \
       {"5" y}] == 1} {
        return $isError
    }

    # set transmissionControl startDelay
    if {[setAndCheckAttributeValue $transmissionControl "startDelay" \
       {"5" y}] == 1} {
        return $isError
    }

    # transmissionControl interBurstGapUnits
    if {[setAndCheckAttributeValue $transmissionControl "interBurstGapUnits" \
       {"bytes" y}] == 1} {
        return $isError
    }

    # set transmissionControl startDelayUnits
    if {[setAndCheckAttributeValue $transmissionControl "startDelayUnits" \
       {"nanoseconds" y}] == 1} {
        return $isError
    }

    set isError 0
    return $isError
}


proc Action {portData1 portData2} {

    set FAILED 1
    set PASSED 0

    set ASSIGN_PORT 0

    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    set chassisIp2 [getChassisIp $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    # Hostname, where IxNetwork TCL-Server client runs
    set hostName [lindex [getHostName $portData1] 0]

    # Version Number (IxNetwork Major version No i.e. 5.40)
    set version "5.40"

    # connect to the chassis
    set connection_Result [connectToClient $portData1 $portData2 $version]
    log "Connection Result: $connection_Result"
    if {[string equal $connection_Result "::ixNet::OK"] != 1} {
        log "connection to client unsuccessful"
        return $FAILED
    }
    log "connectToClient Successful"

    # clean up all the existing configurations from client
    log "cleaning up the client"
    ixNetCleanUp
    after 2000

    # load config files
    set configFileName config.[getTestId].ixncfg
    if  {[ixNet exec loadConfig [ixNet readFrom "$::pwd/$configFileName"]] != \
         "::ixNet::OK"} {
        log "Loading IxNetwork config file : Failed "
        ixNetCleanUp
        return $FAILED
    }
    log "Loading IxNetwork config file : Passed"

    if {$ASSIGN_PORT} {
        # getting the real port list
        set realPortsList [list [list $chassisIp1 $card1 $port1] \
                                [list $chassisIp2 $card2 $port2]]

        # Assign real ports to virtual ports
        log "getting virtual ports ...."
        set vPorts [ixNet getList [ixNet getRoot] vport]
        set vPort1 [lindex $vPorts 0]
        set vPort2 [lindex $vPorts 1]
        log "Virtual ports are = $vPorts"

        # Assign virtual ports to real ports
        log "Assign virtual ports to real ports ..."
        set force true
        set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
        log "Assigned: $status"

        if {[string equal [lindex $status 0]  $vPort1] != 1 || \
            [string equal [lindex $status 1]  $vPort2] != 1} {
            ixNetCleanUp
            return $FAILED
        }
        ixTclNet::CheckLinkState $vPorts doneList
    }
    after 100

    #---------------------------------------------------------------------------
    # TRAFFIC GROUP
    #---------------------------------------------------------------------------
    set Root [ixNet getRoot]
    set traffic $Root/traffic

    after 100

    #---------------------------------------------------------------------------
    # CONFIG ELEMENT
    #---------------------------------------------------------------------------
    set trafficItem [ixNet getList $traffic trafficItem]
    set ti1 [lindex $trafficItem 0]

    set highLevelStream [ixNet getList $ti1 highLevelStream]
    set hls1 [lindex $highLevelStream 0]

    if {[verifyhighLevelStreamMainAttributes $hls1] == 1} {
        ixNetCleanUp
        return $FAILED
    }
    log "Config Element Attributes verification successful"

    after 100

    #---------------------------------------------------------------------------
    # FRAME PAYLOAD
    #---------------------------------------------------------------------------
    set framePayload $hls1/framePayload
    if {[verifyFramePayloadAttributes $framePayload] == 1} {
        ixNetCleanUp
        return $FAILED
    }
    log "Frame Payload Attributes verification successful"

    after 100

    #---------------------------------------------------------------------------
    # FRAME RATE
    #---------------------------------------------------------------------------
    set frameRate $hls1/frameRate
    if {[verifyFrameRateAttributes $frameRate] == 1} {
        ixNetCleanUp
        return $FAILED
    }
    log "Frame Payload Attributes verification successful"

    after 100

    #---------------------------------------------------------------------------
    # FRAME SIZE
    #---------------------------------------------------------------------------
    set frameSize $hls1/frameSize
    if {[verifyFrameSizeAttributes $frameSize] == 1} {
        ixNetCleanUp
        return $FAILED
    }
    log "Frame Size Attributes verification successful"

    after 100

    #--------------------------------------------------------------------------
    # TRANSMISSION CONTROL
    #--------------------------------------------------------------------------
    set transmissionControl $hls1/transmissionControl
    if {[verifyTransmissionControlAttributes $transmissionControl] == 1} {
        ixNetCleanUp
        return $FAILED
    }
    log "transmission Control Attributes verification successful"

    ixNetCleanUp
    return $PASSED
}

#------------------------------------------------------------------------------#
# Execute the Action procedure defined above                                   #
#------------------------------------------------------------------------------#
Execute_Action
