source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#------------------------------------------------------------------------------
# Name           : test.9.1_IsisPortLevelRateControl.tcl
# Author         : Jayasri Dhar
# Purpose        : Automate ISIS PORT Rate Control Functionality
#                  Rate Control Interval (ms) & LSPs per Interval Functionality
#
# Topology       : 1. Add 2 B2B ports and Configure IS-IS.
#                  2. Configure 1 Route Range with 1000 Routes per range
#                     and (20 * 20) Network Ranges.
#                  3. Configure Rate Control Interval = 1000 ms and
#                     LSPs per Interval = 10 at first.
#                  4. Enable the packet capture and run IS-IS.
#                  5. Wait for 20 secs after the protocol is started and Stop
#                     the packet capture.
#                  6. Perform ALL verification steps listed below
#                  7. Start Capture & Disable/Enable the Route Range & Network
#                     Range simultaneously.
#                  8. Stop Capture Stop Protocol
#                  9. Perform ALL verification steps listed below
#                 10. Configure LSPs per Interval = 20 and repeat step 4 - 9
# Verification   : 1. Verify from stat viewer that the IS-IS sessions are UP
#                     with Rate Control configured.
#                  2. For each set of values and for each verification step
#                     verify
#                     the Rate Control Interval & LSPs per Interval through
#                     packet capture.
#                  3. Verify that the No. of LSPs send MUST NOT exceed the
#                     configured
#                     value within the Rate Control Interval configured.
#                     In the packet capture, consider the timestamp (T0) of
#                     first LSP found as starting timestamp and then add the
#                     configured "Rate Control Interval" value to that
#                     timestamp. Let the resultant timestamp be a value T1.
#                     Verify that no more LSPs than the configured
#                     "LSPs per Interval" have been transmitted within the
#                     time period (T1 - T0).
#                  4. Verify the value of the new stat field
#                     "Rate Control Blocked Sending LSP/MGROUP" is being
#                     populated (i.e. value greater than 0)
# Config Format  : ixncfg used
#------------------------------------------------------------------------------
proc Action {portData1 portData2} {
    source $::pwd/rateControlUtils.tcl

    # initialize return value
    set FAILED 1
    set PASSED 0

    # Get real card1/port1 from portData
    set chassisIp1 [getChassisIp  $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    # Get real card2/port2 from portData
    set chassisIp2 [getChassisIp  $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    # Hostname, where IxNetwork TCL-Server client runs
    set tclPublisherVersion "5.40"
    set hostName [lindex [getHostName $portData1] 0]
    set connection_Result [connectToClient $portData1 $portData2 \
            $tclPublisherVersion]

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
    if  {[ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]] != \
        "::ixNet::OK"} {
        log "Loading IxNetwork config file : Failed "
        ixNetCleanUp
        return $FAILED
    }
    log "Loading IxNetwork config file : Passed"

    # getting the real port list
     set realPortsList [list [list $chassisIp1 $card1 $port1] \
             [list $chassisIp2 $card2 $port2]]

    # Assign real ports to virtual ports
    log "getting virtual ports ...."
    set vPorts      [ixNet getList [ixNet getRoot] vport]
    set vPort1      [lindex $vPorts 0]
    set vPort2      [lindex $vPorts 1]
    log "Virtual ports are = $vPorts"

    # Assign virtual ports to real ports
    log "Assign virtual ports to real ports ..."
    set force true
    set status      [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    log "Assigned: $status"
    if {[string equal [lindex $status 0]  $vPort1] != 1 || \
        [string equal [lindex $status 1]  $vPort2] != 1} {
        ixNetCleanUp
        return $FAILED
    }
    ixTclNet::CheckLinkState $vPorts doneList
    after 2000

    # Enable & Start Capture
    log "Enable & Start Capture..."
    if {[enableCaptureMode $vPorts] == 1} {
        log "Failed to enable capture..."
        ixNetCleanUp
        return $FAILED
    }

    ixNet exec startCapture


    # Repeat twice - once for lspMgroupPdusPerInterval = 10
    # and once for lspMgroupPdusPerInterval = 20
    foreach lspMgroupPdusPerInterval {10 20} {

        # Start Protocols
        log "Starting protocol ISIS (Level 1)..."
        if {([ixNet exec start $vPort1/protocols/isis] != "::ixNet::OK") || \
            ([ixNet exec start $vPort2/protocols/isis] != "::ixNet::OK")} {
            log "Failed to start protocol ISIS (Level 1)..."
            ixNetCleanUp
            return $FAILED
        }

        log "Protocol started"
        log "Waiting for 60 Sec for protocol Sessions to be up"

        after 60000

        ixNet exec stopCapture

        # Verify Starts
        log "Verifying ISIS (Level 1) protocol stats ..."
        set ISISStatsList {"L1 Sess. Configured"                     1 \
                           "L1 Sess. Up"                             1 \
                           "L1 Full State Count"                     1 \
                           "L1 Neighbors"                            1 \
                           "Rate Control Blocked Sending LSP/MGROUP" 1}

        set portList [list [list $chassisIp1 $card1 $port1] \
                           [list $chassisIp2 $card2 $port2]]

        if {[checkAllProtocolStats $portList "ISIS Aggregated Statistics" \
                  $ISISStatsList]} {
            log "Did not get the expected ISIS protocol stats value..."
            ixNetCleanUp
            return $FAILED
        }
        log "Got expected ISIS protocol stats values..."

        set rateControlInterval 1000 ; # in ms
        if {$lspMgroupPdusPerInterval == 20} {
            if {[setAndCheckAttributeValue $vPort1/protocols/isis \
                "lspMgroupPdusPerInterval" {"20" y}] == 1} {
                log "Failed to set lspMgroupPdusPerInterval!!!"
                ixNetCleanUp
                return $FAILED
            }

            if {[setAndCheckAttributeValue $vPort2/protocols/isis \
                "lspMgroupPdusPerInterval" {"20" y}] == 1} {
                log "Failed to set lspMgroupPdusPerInterval!!!"
                ixNetCleanUp
                return $FAILED
            }
        }

        log "Retriving ISIS Rate Control Port Level Attribute \
             values as configured"

        set expectProp  [subst {rateControlInterval $rateControlInterval \
                            lspMgroupPdusPerInterval $lspMgroupPdusPerInterval}]

        if {[checkAttributeValue $vPort1/protocols/isis $expectProp] == 1} {
            log "ISIS Rate Control Port Level Attribute values \
                 not per configuration..."
            ixNetCleanUp
            return $FAILED
        }

        # Verify ISIS LSP's in captured packet
        log "Checking for ISIS (Level 1) LSPs in Captured Pkt..."
        set lspMatchFieldList {17 17 "83" \
                               21 21 "12" }

        set rateList [subst {$lspMgroupPdusPerInterval \
                            [expr $rateControlInterval/1000]}]

        set expectedPktCount [expr $lspMgroupPdusPerInterval * 5]

        if {[checkRateControlThroughCapture $chassisIp1 $card1 $port1 \
                 $lspMatchFieldList $expectedPktCount $rateList] == 1} {
            log "ISIS LSP Rate is not per configuration!!!"
            ixNetCleanUp
            return $FAILED
        }

        # Stop Protocols
        log "Stopping protocol ISIS (Level 1)..."
        if {([ixNet exec stop $vPort1/protocols/isis] != "::ixNet::OK") || \
            ([ixNet exec stop $vPort2/protocols/isis] != "::ixNet::OK")} {
            log "Failed to stop protocol ISIS (Level 1)..."
            ixNetCleanUp
            return $FAILED
        }

        # Verify ISIS LSP's in captured packet
        log "Checking for ISIS (Level 1) LSPs in Captured Pkt..."
        if {[checkRateControlThroughCapture $chassisIp1 $card1 $port1 \
                 $lspMatchFieldList $expectedPktCount $rateList] == 1} {
            log "ISIS LSP Rate is not per configuration!!!"
            ixNetCleanUp
            return $FAILED
        }
    }

    # Cleanup
    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action

