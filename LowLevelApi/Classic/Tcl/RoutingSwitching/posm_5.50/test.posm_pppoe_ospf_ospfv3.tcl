source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#------------------------------------------------------------------------------
# Name           : test.posm_pppoe_ospf_ospfv3.tcl
# Author         : Sanchari Roy
# Purpose        : L3 Traffic over PoSM Functinality
#                  Configure OSPFv2/v3 over PPPOE
#                : Configure Traffic
# Verify         : Verify the protocol stats and traffic stats are proper
# Topology       : Back To Back
# ixncfg used    : Yes
# Scriptgen used : No
#------------------------------------------------------------------------------
proc Action {portData1 portData2} {
    source $::pwd/utils.tcl

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
    set tclPublisherVersion "5.50"
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
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
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

    set ethernet1 [lindex [ixNet getList $vPort1/protocolStack ethernet] 0]
    set ppp1 [lindex [ixNet getList $ethernet1 pppoxEndpoint] 0]

    set ethernet2 [lindex [ixNet getList $vPort2/protocolStack ethernet] 0]
    set ppp2 [lindex [ixNet getList $ethernet2 pppoxEndpoint] 0]

    log "Start PPPoE on first client port & then server port"

    ixNet exec start $ppp1
    after 30000

    if {([ixNet exec start $ppp2] != "::ixNet::OK")} {
        log "Failed to start PPPoE successfully on second port..."
        ixNetCleanUp
        return $FAILED
    }
    log "Waiting for 60 Sec..."
    after 60000

    log "Verifying PPPoE protocols stats..."
    set pppStatsPort1 {"Sessions Initiated" 2 \
                       "Sessions Succeeded" 2}

    set pppStatsPort2 {"Sessions Initiated" 2 \
                       "Sessions Succeeded" 2}

    if {[checkAllProtocolStats [list [list $chassisIp1 $card1 $port1]] \
            "PPP General Statistics" $pppStatsPort1]} {
        log "Failure: Did not get the expected value for the all stats"
        ixNetCleanUp
        return $FAILED
    }

    if {[checkAllProtocolStats [list [list $chassisIp2 $card2 $port2]] \
            "PPP General Statistics" $pppStatsPort2]} {
        log "Failure: Did not get the expected value for the all stats"
        ixNetCleanUp
        return $FAILED
    }
    log "PPPoE (v4&v6) Up and Running.."

    log "Wait for 30 second before starting Protocols on top of SM interfaces"
    after 30000

    log "Start Protocols on top of SM interfaces..."

    log "Starting protocol ospf ..."
    if {([ixNet exec start $vPort1/protocols/ospf] != "::ixNet::OK") || \
        ([ixNet exec start $vPort2/protocols/ospf] != "::ixNet::OK")} {
        log "Failed to start protocol ospf ..."
        ixNetCleanUp
        return $FAILED
    }

    after 5000

    log "Starting protocol ospfV3 ..."
    if {([ixNet exec start $vPort1/protocols/ospfV3] != "::ixNet::OK") || \
        ([ixNet exec start $vPort2/protocols/ospfV3] != "::ixNet::OK")} {
        log "Failed to start protocol ospfV3 ..."
        ixNetCleanUp
        return $FAILED
    }

    log "All Protocols started successfully.."

    log "Wait for 60 second before verifying Stats..."
    after 60000

    log "Verify Protocol Stats ....."
    # Verify OSPF Stats...
    set OSPFStatsList {"Sess. Configured" 1 \
                       "Full Nbrs." 1}

    if {[checkAllProtocolStats [list [list $chassisIp2 $card2 $port2]] \
         "OSPF Aggregated Statistics" $OSPFStatsList]} {
        log "OSPF Protocol stats are not matching..."
        ixNetCleanUp
        return $FAILED
    }
    log "OSPF Protocol stats are matching for both ports"

    if {[checkAllProtocolStats [list [list $chassisIp2 $card2 $port2]] \
        "OSPFv3 Aggregated Statistics" $OSPFStatsList]} {
        log "OSPFv3 Protocol stats are not matching..."
        ixNetCleanUp
        return $FAILED
    }
    log "OSPFv3 Protocol stats are matching for both ports"


    # Generate and Apply Traffic & Check number of Flows Generated..
    log "Generating and Applying Traffic"
    if {[generateApplyTraffic]} {
        log "Failed to Generate & Apply traffic successfully"
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic Generated & Applied Successfully..."

    log "Starting the Traffic.."
    if {[startTraffic [ixNet getRoot]/traffic]} {
        log "Failed to Start Traffic Successfully..."
        ixNetCleanUp
        return $FAILED
    }

    log "Running Traffic for 60 seconds..."
    after 60000

    #Verifying traffic item statistics
    log "Check Traffic Item Statistics..."
    if {[checkAllTrafficStats "Traffic Item Statistics"] == 1} {
        log "FAILURE : Not able to retrieve statistics values for \
             Traffic Item Statistics"
        ixNetCleanUp
        return $FAILED
    }

    log "Check Flow Statistics..."
    if {[checkAllTrafficStats "Flow Statistics"] == 1} {
        log "FAILURE : Not able to retrieve statistics values for \
             Flow Statistics"
        ixNetCleanUp
        return $FAILED
    }

    log "Stopping the Traffic.."
    if {[stopTraffic [ixNet getRoot]/traffic]} {
        log "Failed to Stop Traffic successfully..."
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic Stopped"

    #--------------------------------------------------------------------------#
    # Stop all protocols                                                       #
    #--------------------------------------------------------------------------#
    if {[catch {ixNet exec stopAllProtocols}]} {
       log "Error in starting all protocols"
       ixNetCleanUp
       return $FAILED
    }

    # Cleanup
    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
