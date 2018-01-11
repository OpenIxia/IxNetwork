#------------------------------------------------------------------------------
# Name     : test.6.1.10_bgp_ospf.traffic.tcl
# Author   : Soumen Roy
# Purpose  : Checking imported routes in BGP and verify protocols and traffic
# Steps    : 
#           1. Configuring IXIA Ports using ixncfg file
#           2. Verifying the importing routes in bgp by importing bgp routes in 
#              the first port and verifying learned routed in the second port.
#           3. Starting the Protocols
#           4. Applying the Traffic
#           5. Starting the Traffic
#           6. Stopping the Traffic
#           7. Verify the Traffic Statistics in IXNetwork Client and also verify 
#              Learned info.
#           8. Stopping the Protocols
#           9. Cleaning the IXIA ports
# ScriptGen used: No
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

proc Action {portData1 portData2} {
    
    source $::pwd/BGPRouteImportUtils.tcl

    # Initializing return value
    set PASSED 0
    set FAILED 1

    # Get the first port info
    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]
    
    # Get the second port info
    set chassisIp2 [getChassisIp $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    # Version Number (IxNetwork Major version No i.e. 5.40)
    set version "5.40"

    # Connecting to the chassis
    set connection_Result [connectToClient $portData1 $portData2 $version]
    log "Connection Result: $connection_Result"
    if {[string equal $connection_Result "::ixNet::OK"] != 1} {
        log "connection to client unsuccessful"
        ixNetCleanUp
        return $FAILED
    }
    log "connectToClient Successful"

    # Cleaning up all the existing configurations from client
    log "!!!cleaning up the client!!!"
    ixNetCleanUp

    # Configure the Ixia ports
    set configFileName config.[getTestId].ixncfg
    log "!!!Now we configure the Ixia port!!!"
    if {[ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]] != \
        "::ixNet::OK"} {
        log "Failed to load config file"
        ixNetCleanUp
        return $FAILED
    }
    log "Configuration of the ports Successful"

    # Getting the virtual port list
    log "!!!Getting virtual ports !!!"
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
    log "Virtual ports are = $vPorts"

    # Getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]

    # Assign virtual ports to real ports
    log "!!!Assign virtual ports to real ports!!!"
    set force true
    log "$realPortsList {} $vPorts"
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts $force]
    log "Assigned: $status"
    ixNet commit
    if {[string equal [lindex $status 0] $vPort1] != 1 || \
        [string equal [lindex $status 1] $vPort2] != 1} {
        ixNetCleanUp
        return $FAILED
    }

    # Following code checks whether ports came up after assigning real ports.
    # If not then explicit connect is used
    set vport1_state [ixNet getAttribute $vPort1 -isAvailable]
    if {$vport1_state != "true"} {
        if {[::ixNet exec connectPort $vPort1] != "::ixNet::OK"} {
            log "Unable to connect the real ports1 to virtual ports1"
            ixNetCleanUp
            return $FAILED
        }
        log "Sleeping for 10 seconds for physical ports 1 to come up"
        after 10000
    }

    set vport2_state [ixNet getAttribute $vPort2 -isAvailable]
    if {$vport2_state != "true"} {
        if {[::ixNet exec connectPort $vPort2] != "::ixNet::OK"} {
            log "Unable to connect the real ports2 to virtual ports2"
            ixNetCleanUp
            return $FAILED
        }
        log "Sleeping for 10 seconds for physical ports 2 to come up"
        after 10000
    }

    set bgp1 $vPort1/protocols/bgp
    set bgpNeighbor        [lindex [ixNet getList $bgp1 neighborRange] 0]
    set importRouteOptions [ixNet add $bgpNeighbor routeImportOptions]
    
    # Setting the path of the filename to be imported
    set fileName $::pwd/[getTestId].csv 
   
    # Checking bgp import functionality
    if {[bgpImportFunctionality $importRouteOptions $fileName 1] != 0} {
        log "FAILURE : Could not import routes"
        ixNetCleanUp
        return $FAILED
    } else {
        log "SUCCESS : Successfully imported routes"
    }

    # Applying the opaque route ranges
    set opaqueRouteRange [lindex [ixNet getList $bgpNeighbor \
        opaqueRouteRange] 0]

    ixNet exec applyOpaqueRouteRange $opaqueRouteRange
    log "waiting for 10 seconds"
    after 10000
    log "Retrieving opaque route ranges"

    # check properly applied or not
    set retrieveOpqRtRange [lindex [ixNet getList $bgpNeighbor \
        opaqueRouteRange] 0]
    if {[ixNet getAttribute $retrieveOpqRtRange -status] != "kApplied"} {
        log "FAILURE : Could not apply routes"
        ixNetCleanUp
        return $FAILED
    } else {
        log "SUCCESS : Successfully applied routes"
    }

    # Starting all the configured protocol
    log "!!!Starting all the configured protocol!!!"
    set ret [ixNet exec startAllProtocols]
    if {$ret != "::ixNet::OK"} {
    log "Couldn't start the Protocol Operation"
        ixNetCleanUp
        return $FAILED
    }
    log "Sleeping for 30 seconds to start the configured protocols"
    after 30000

    # Verifying learned info at port 2
    set bgp2 $vPort2/protocols/bgp
    set bgpNeighbor2 [lindex [ixNet getList $bgp2 neighborRange] 0]

    set FinalmatchList1 [list {<65001> 0 1.1.1.1 5.5.5.0} \
            {{<65001> <100 300 50> {80,701,703}} 0 1.1.1.1 12.0.0.0} \
            {{<65001> <100 300> {50} {21889}} 0 1.1.1.1 14.23.112.0} \
            {{<65001> <100 300> {50} {21889}} 0 1.1.1.1 16.23.114.0} \
            {{<65001> <100 300> {50} {21889}} 0 1.1.1.1 17.36.116.0} \
            {{<65001> <100 300> {50} {80,701,703}} 0 1.1.1.1 22.0.0.0} \
            {{<65001> <100 300> {50} {21889}} 0 1.1.1.1 24.23.112.0} \
            {{<65001> <100 300> {50} {21889}} 0 1.1.1.1 25.23.113.0} \
            {{<65001> <100 300> {50} {21889}} 0 1.1.1.1 26.23.114.0} \
            {{<65001> <100 300 50 80 701 703>} 0 1.1.1.1 52.0.0.0} \
            {{<65001> <100 300 50 21889>} 0 1.1.1.1 54.23.112.0} \
            {{<65001> <100 300 50 21889>} 0 1.1.1.1 55.23.113.0} \
            {{<65001> <100 300 50 21889>} 0 1.1.1.1 56.23.114.0} \
            {{<65001> <100 300 50 21889>} 0 1.1.1.1 57.36.116.0} \
            {{<65001> <100 300 50 80 701 703>} 0 1.1.1.1 58.0.0.0} \
            {{<65001> <100 300 50 80 701 703>} 0 1.1.1.1 59.0.0.0} \
            {{<65001> <100 300 50 21889>} 0 1.1.1.1 60.23.112.0} \
            {{<65001> <100 300 50 21889>} 0 1.1.1.1 61.23.113.0} \
            {{<65001> <100 300 50 21889>} 0 1.1.1.1 62.23.114.0}]

    if {[learnedInfoFetchForRouteImport $bgpNeighbor2 $FinalmatchList1] != 1} {
        log "Learned info verification failed for first peer"
        ixNetCleanUp
        return $FAILED
    }
    log "Learned info verification successfull for first peer.."
   
    log "Verify Protocol Stats ....."

    set BGPStatsList {"Established State Count" 1 \
                      "Sess. Configured" 1 \
                      "Sess. Up" 1}

    set OSPFStatsList {"Sess. Configured" 1 \
                       "Full State Count" 1 \
                       "Full Nbrs." 1}

    set portList [list [list $chassisIp1 $card1 $port1] \
                       [list $chassisIp2 $card2 $port2]]

    if {[checkAllProtocolStats $portList "BGP Aggregated Statistics" \
        $BGPStatsList]} {
        log "BGP Protocol stats are not matching"
        ixNetCleanUp
        return $FAILED
    }
    log "BGP Protocol stats are matching"

    set portList [list [list $chassisIp1 $card1 $port1] \
                       [list $chassisIp2 $card2 $port2]]

    if {[checkAllProtocolStats $portList "OSPF Aggregated Statistics" \
        $OSPFStatsList]} {
        log "OSPF Protocol stats are not matching"
        ixNetCleanUp
        return $FAILED
    }
    log "OSPF Protocol stats are matching"

    # Getting the handle for traffic item
    set root [ixNet getRoot]
    set traffic $root/traffic

    # Applying the configured traffic item to respective ports
    log "!!!Applying the traffic !!!"
    if {[generateApplyTraffic] == 1} {
    log "Not able to apply the traffic.."
        ixNetCleanUp
        return $FAILED
    }

    # Starting configured traffic item
    log "!!!Starting the traffic!!!"
    if {[catch {ixNet exec startStatelessTraffic $traffic} errMsg]} {
        log "Start Traffic Failed - $errMsg"
        ixNetCleanUp
        return $FAILED
    }
    log "Sleeping for 120 seconds to start the traffic"
    after 120000

    # Stoping configured traffic item
    log "!!!Stopping the traffic!!!"
    if {[catch {ixNet exec stopStatelessTraffic $traffic} errMsg]} {
        log "Stopping Traffic Failed - $errMsg"
        ixNetCleanUp
        return $FAILED
    }

    # Traffic Statistics Checking
    log "Check Traffic Item Statistics..."
    if {[checkAllTrafficStats "Traffic Item Statistics"] == 1} {
        log "Not able to retrieve Traffic Item Statistics"
        ixNetCleanUp
        return $FAILED
    }

    log "Check Flow Statistics..."
    if {[checkAllTrafficStats "Flow Statistics"] == 1} {
       log "Not able to retrieve statistics values for Flow Statistics"
       ixNetCleanUp
       return $FAILED
    }

    log "Check Data Plane Port Statistics"
    set txPortList [subst {{[ixNet getAttr $vPort1 -name]}}]
    set rxPortList [subst {{[ixNet getAttr $vPort2 -name]}}]
    if {[checkAllPortTrafficStats "Data Plane Port Statistics" $txPortList \
        $rxPortList] } {
        log "Not able to retrieve statistics values for Data plane traffic"
        ixNetCleanUp
        return $FAILED
    }
  
    # Stoping all the configured protocol
    log "!!!Stopping All Protocol Operation!!!"
    set ret [ixNet exec stopAllProtocols]
    if {$ret != "::ixNet::OK"} {
    log "Couldn't stop the Protocol Operation"
        ixNetCleanUp
        return $FAILED
    }
    
    # Unassigning all the ports and removing the same
    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
