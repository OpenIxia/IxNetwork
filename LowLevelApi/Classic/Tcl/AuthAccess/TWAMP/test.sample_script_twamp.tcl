#------------------------------------------------------------------------------
# Name          : test.sample_script_twamp.tcl
# Author        : Indranil Acharya
# Purpose       : To check TWAMP Statistics (Per Session /Per Range and Global)
# Code Flow     : 1. Configure IXIA Ports
#                 2. Start TWAMP
#                 3. Verify TWAMP Protocol Stats
#                 4. Verify Per Session/Range Stats
#                 5. Stop TWAMP
#                 6. Clean IXIA Ports
# Test Setup    : B2B
# ixncfg used   : Yes (config.sample_script_twamp.ixncfg)
# Scriptgen used: No
#------------------------------------------------------------------------------

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

proc Action {portData1 portData2} {
    # Initialize return value
    set FAILED 1
    set PASSED 0

    # Source the Utility Files
    set isError [catch {source $::pwd/twampTrafficUtils.tcl
                        source $::pwd/twampUtils.tcl} errorMsg]
    if {$isError} {
        log "Error in sourcing the file $errorMsg"
        ixNetCleanUp
        return $FAILED
    }

    # Get port info 1
    set chassisIp1 [lindex $portData1 0]
    set card1      [lindex $portData1 1]
    set port1      [lindex $portData1 2]
    set client1    [lindex $portData1 3]
    set tcpPort1   [lindex $portData1 4]

    # Get port info 2
    set chassisIp2 [lindex $portData2 0]
    set card2      [lindex $portData2 1]
    set port2      [lindex $portData2 2]
    set client2    [lindex $portData2 3]
    set tcpPort2   [lindex $portData2 4]

    set version "5.40"

    # Connect to IxNetwork TCL-Server/Client
    if {$client1 == $client2} {
        log "Connecting to client $client1"
        if {[ixNet connect $client1 -port $tcpPort1 -version $version] != \
            "::ixNet::OK" } {
            log "Unable to connect to IxNetwork Tcl Server !!!"
            ixNetCleanUp
            return $FAILED
        }
    } else {
        log "Use the same client !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Connection to the Client successful !!!"

    # Clean up all the existing configurations from client
    log "Cleaning up the client"
    ixNetCleanUp
    log "Executing from [pwd]"

    # Load config file
    set configFileName "config.sample_script_twamp.ixncfg"
    if  {[ixNet exec loadConfig [ixNet readFrom \
        "$::pwd/$configFileName"]] != "::ixNet::OK"} {
        log "Loading IxNetwork config file : Failed "
        ixNetCleanUp
        return $FAILED
    }

    # Get the virtual port list
    log "getting virtual ports ...."
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
    log "Virtual ports are = $vPorts"

    # Get the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1]\
                            [list $chassisIp2 $card2 $port2] ]

    # Assign virtual ports to real ports
    log "Assign virtual ports to real ports ..."
    set force true
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    ixNet commit
    log "Assigned: $status"

    if {[string equal [lindex $status 0] $vPort1] != 1 || \
        [string equal [lindex $status 1] $vPort2] != 1} {
        ixNetCleanUp
        return $FAILED
    }
    ixTclNet::CheckLinkState $vPorts doneList

    log "Waiting for 10 sec before starting ..."
    after 10000

    # Start TWAMP on both ports
    set ethernet1   [lindex [ixNet getList $vPort1/protocolStack ethernet] 0]
    set ipEndpoint1 [lindex [ixNet getList $ethernet1 ipEndpoint] 0]

    set ethernet2   [lindex [ixNet getList $vPort2/protocolStack ethernet] 0]
    set ipEndpoint2 [lindex [ixNet getList $ethernet2 ipEndpoint] 0]

    log "Starting TWAMP on the ports"
    if {[ixNet exec start $ipEndpoint2] != "::ixNet::OK"} {
        log "Unable to start TWAMP at 2nd Port"
        ixNetCleanUp
        return $FAILED
    }
    log "TWAMP started at 2nd Port successfully"
    after 5000

    if {[ixNet exec start $ipEndpoint1] != "::ixNet::OK"} {
        log "Unable to start TWAMP at 1st Port"
        ixNetCleanUp
        return $FAILED
    }
    log "TWAMP started at 1st Port successfully"


    log "Waiting for 20 Sec..."
    after 20000

    # TWAMP Stats Verification
    set completeStats {"TWAMP Server Control" {"Sessions Initiated" 7 \
                                               "Sessions Succeeded" 7 \
                                               "Sessions Failed" 0 \
                                               "Active Sessions" 7 \
                                               "Initiated Sessions Rate" 0 \
                                               "Successful Sessions Rate" 0 \
                                               "Failed Sessions Rate" 0 } \
                       "TWAMP Server Test"    {"Initiated Sessions" 7 \
                                               "Successful Sessions" 7 \
                                               "Failed Sessions" 0 \
                                               "Active Sessions" 0 \
                                               "Initiated Sessions Rate" 0 \
                                               "Successful Sessions Rate" 0 \
                                               "Failed Sessions Rate" 0 } \
                       "TWAMP Server Data"    {"Datagram Tx" 70 \
                                               "Datagram Rx" 70 \
                                               "Datagram Unexpected" 0 \
                                               "Data Streams Initiated" 7 \
                                               "Data Streams Successful" 7 \
                                               "Data Streams Failed" 0 } \
                       "TWAMP Control"        {"Sessions Initiated" 7 \
                                               "Sessions Succeeded" 7 \
                                               "Sessions Failed" 0 \
                                               "Active Sessions" 7 \
                                               "Initiated Sessions Rate" 0 \
                                               "Successful Sessions Rate" 0 \
                                               "Failed Sessions Rate" 0 } \
                       "TWAMP Test"           {"Initiated Sessions" 7 \
                                               "Successful Sessions" 7 \
                                               "Failed Sessions" 0 \
                                               "Active Sessions" 0 \
                                               "Initiated Sessions Rate" 0 \
                                               "Successful Sessions Rate" 0 \
                                               "Failed Sessions Rate" 0 } \
                       "TWAMP Data"           {"Datagram Tx" 70 \
                                               "Datagram Rx" 70 \
                                               "Datagram Lost" 0 \
                                               "Datagram Unexpected" 0 \
                                               "Data Streams Initiated" 7 \
                                               "Data Streams Successful" 7 \
                                               "Data Streams Failed" 0 } \
        }

    foreach {captionView completeStat} $completeStats {
        if {[checkAllTwampStats $captionView $completeStat 1] == 1} {
            log "Failure: Did not get the expected value for the stats"
            ixNetCleanUp
            return $FAILED
        }
        log "$captionView: Got the expected value for all the stats"
    }
    # Verifying Per Session Stats
    log "Verifying Per Session Stats ....."


    set expectedPerSessionStat {"1 1 0 0 10 10 0 1 1 0 0 1000 0" \
                                "1 1 0 0 10 10 0 1 1 0 1 1000 0" \
                                "1 1 0 0 10 10 0 1 1 0 2 1000 0" \
                                "1 1 0 0 10 10 0 1 1 0 3 1000 0" \
                                "1 1 0 0 10 10 0 1 1 0 4 1000 0"}
    if {[designL23TrafficPerSession perSession $expectedPerSessionStat] == 1} {
        log "Fail: The Per session stats are not correct"
        ixNetCleanUp
        return $FAILED
    }
    log "Pass: The Per session stats are correct"

    # Verify Per Range Stats
    log "Verifying Per Range Stats ....."
    set expectedPerRangeStat {"0 5 5 0 5 5 5 0 0 50 50 0 0 5 5 0"}
    if {[designL23TrafficPerSession perRange $expectedPerRangeStat] == 1} {
        log "Fail: The Per Range stats are not correct"
        ixNetCleanUp
        return $FAILED
    }
    log "Pass: The Per Range stats are correct"

    # Stop TWAMP
    log "Stopping TWAMP on the both ports"

    if {[ixNet exec stop $ipEndpoint1] != "::ixNet::OK"} {
        log "Unable to stop TWAMP at 1st Port"
        ixNetCleanUp
        return $FAILED
    }
    log "TWAMP stopped at 1st Port successfully"

    if {[ixNet exec stop $ipEndpoint2] != "::ixNet::OK"} {
        log "Unable to stop TWAMP at 2nd Port"
        ixNetCleanUp
        return $FAILED
    }
    log "TWAMP stopped at 2nd Port successfully"

    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
