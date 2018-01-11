#------------------------------------------------------------------------------
# Name          : test.2.1.112.6vpe.ospf.traffic.tcl
# Author        : Magesh Manavalan
# Purpose   : Checking 6VPE Traffic Item
# Topology  : Configure 6VPE ( 3 PE port + 1 CE port ) with 3 P Router with
#           3 Emulated PE and 5 unique VRF. Use OSPF & RSVP at PE side
#           and OSPFv3  at CE side .Send PE to CE and CE to PE Traffic.
# Steps         :
#         1. Configuring IXIA Ports using scriptgen file
#         2. Verifying the Traffic Item configuration in IXNetwork Client
#         3. Starting the Protocols
#         4. Applying the Traffic
#         5. Verifying the Traffic Item configuration in Chassis(IXExplore)
#         6. Starting the Traffic
#         7. Stopping the Traffic
#         8. Verify the Traffic Statistics in IXNetwork Client
#         9. Stopping the Protocols
#         10. Cleaning the IXIA ports
# ScriptGen used: No
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

# 2.1.112 Test Case Coverage
set ::TestPart0 1; # Protocol Stats Verification
set ::TestPart1 0; # GUI Verification NA
set ::TestPart2 1; # Traffic Configuration Verification
set ::TestPart3 1; # Traffic Stats Verification

proc checkDetailTrafficConfiguration {} {
    set error 1
    #Getting the Traffic Item object hierarchy details
    set traffic [ixNet getRoot]/traffic
    set trafficItem [lindex [ixNet getList $traffic trafficItem] 0]
    set configElementList [ixNet getList $trafficItem configElement]
    set configElement [lindex $configElementList 0]
    set frameRate [ixNet getList $configElement frameRate]
    set framePayload [ixNet getList $configElement framePayload]
    set frameRateDist [ixNet getList $configElement frameRateDistribution]
    set frameSize [ixNet getList $configElement frameSize]

    log "Checking Traffic Item parameters..."
    set trafficitem_values_1 {biDirectional false mergeDestinations false\
    routeMesh oneToOne srcDestMesh oneToOne}

    if {[checkAttributeValue $trafficItem $trafficitem_values_1] == 1} {
        return $error
    }

    if {[checkAttributeValue $trafficItem/tracking \
    {trackBy "trackingenabled0 mplsMplsLabelValue0 mplsMplsLabelValue1"}] == 1} {
        return $error
    }

    log "Checking Frame Payload parameters..."
    if {[checkAttributeValue $framePayload {type incrementByte \
                                            customPattern {} \
                                            customRepeat True}] == 1} {
        return $error
    }

    log "Checking Frame Size parameters..."
    if {[checkAttributeValue $frameSize {type increment \
                                         incrementFrom 200 incrementTo 1518}] == 1} {
        return $error
    }

    log "Checking High Level Stream parameters..."
    if {[checkHighLevelSteamCountForAllTrafficItem 1 {0 1}] == 1} {
        return $error
    }

    set error 0
    return $error
}

proc checkChassiTrafficConfiguration {chassis card port} {

    set error 1

    if {[ixExplorerConnectChassis $chassis $card $port] != 0} {
        log "FAILURE : Error in initializing/logging in chassis"
        return $error
    }

    set chassisId [chassis cget -id]

    #Getting the Frames object hierarchy details
    if {[stream get $chassisId $card $port 1] != 0} {
    log "FAILURE : Error in getting stream data from chassi for port $port"
        return $error
    }

    if {[ipV6 get $chassisId $card $port] != 0} {
    log "FAILURE : Error in getting IPV6 data from chassi for port $port"
        return $error
    }

    log "Checking Stream 1 Values for port $port"
    if {[ixExplorerCheckAttributeValue stream {frameSizeMIN 200\
         frameSizeMAX 1518 patternType 0}] == 1} {
        return $error
    }

    log "Checking Stream 1 IPV6 Values for port $port"
    if {[ixExplorerCheckAttributeValue ipV6 {sourceAddr 30:0:0:0:0:0:0:1 \
    destAddr 33:0:0:0:0:0:0:1}] == 1} {
        return $error
    }

    if {[ixExplorerDisconnectChassis $chassis] != 0} {
        log "FAILURE : Error in disconnecting in chassis"
        return $error
    }

    set error 0
    return $error
}

proc Action {portData1 portData2} {

    #Initializing return value
    set PASSED 0
    set FAILED 1

    #Get the first port info
    set chassisIp1 [getChassisIp $portData1]
    set card1 [getCardNumber $portData1]
    set port1 [getPortNumber $portData1]

    #Get the second port info
    set chassisIp2 [getChassisIp $portData2]
    set card2 [getCardNumber $portData2]
    set port2 [getPortNumber $portData2]

    #Version Number (IxNetwork Major version No i.e. 5.40)
    set version "5.40"

    #Connecting to the chassis
    set connection_Result [connectToClient $portData1 $portData2 $version]
    log "Connection Result: $connection_Result"
    if {[string equal $connection_Result "::ixNet::OK"] != 1} {
        log "FAILURE : connection to client unsuccessful"
        ixNetCleanUp
        return $FAILED
    }
    log "connectToClient Successful"

    #Cleaning up all the existing configurations from client
    log "!!!cleaning up the client!!!"
    ixNetCleanUp

    # Configure the Ixia ports
    log "!!!Now we configure the Ixia port!!!"
    if {[ixNet exec loadConfig [ixNet readFrom \
        $::pwd/config.2.1.112.6vpe.ospf.rsvp.traffic.ixncfg]] != "::ixNet::OK"} {
        log "FAILURE : Failed to load config file"
        ixNetCleanUp
        return $FAILED
    }
    log "Configuration of the ports Successful"

    #Getting the virtual port list
    log "!!!Getting virtual ports !!!"
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
    log "Virtual ports are = $vPorts"

    #Getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
        [list $chassisIp2 $card2 $port2] ]

    #Assign virtual ports to real ports
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

    #Following code checks whether ports came up after assigning real ports.
    #If not then explicit connect is used
    set vport1_state [ixNet getAttribute $vPort1 -isAvailable]
    if {$vport1_state != "true"} {
    if {[::ixNet exec connectPort $vPort1] != "::ixNet::OK"} {
            log "FAILURE : Unable to connect the real ports1 to virtual ports1"
            ixNetCleanUp
            return $FAILED
        }
    log "Sleeping for 10 seconds for physical ports 1 to come up"
    after 10000
    }
    set vport2_state [ixNet getAttribute $vPort2 -isAvailable]
    if {$vport2_state != "true"} {
    if {[::ixNet exec connectPort $vPort2] != "::ixNet::OK"} {
            log "FAILURE : Unable to connect the real ports2 to virtual ports2"
            ixNetCleanUp
            return $FAILED
        }
    log "Sleeping for 10 seconds for physical ports 2 to come up"
    after 10000
    }

    #Starting all the configured protocol
    log "!!!Starting all the configured protocol!!!"
    set ret [ixNet exec startAllProtocols]
    if {$ret != "::ixNet::OK"} {
    log "FAILURE : Couldn't start the Protocol Operation"
        ixNetCleanUp
        return $FAILED
    }
    log "Sleeping for 60 seconds to start the configured protocols"
    after 60000

    if {$::TestPart0 == 1} {

        log "Verify Protocol Stats ....."

    set BGPStatsList {"Established State Count" 9 \
                          "Sess. Configured" 9 \
                          "Sess. Up" 9}
        set OSPFStatsList {"Sess. Configured" 3 \
                          "Full State Count" 3 \
                          "Full Nbrs." 3}
        set RSVPStatsList {"Egress LSPs Up" 9 \
                          "Ingress LSPs Configured" 9 \
                          "Ingress LSPs Up" 9 \
              "Up State Count" 9}


        set portList [list [list $chassisIp1 $card1 $port1] [list $chassisIp2 $card2 $port2]]
        if {[checkAllProtocolStats $portList "BGP Aggregated Statistics" $BGPStatsList]} {
            log "FAILURE : BGP Protocol stats are not matching"
            ixNetCleanUp
            return $FAILED
        }
        log "BGP Protocol stats are matching"

    set portList [list [list $chassisIp1 $card1 $port1] [list $chassisIp2 $card2 $port2]]
        if {[checkAllProtocolStats $portList "OSPF Aggregated Statistics" $OSPFStatsList]} {
            log "FAILURE : OSPF Protocol stats are not matching"
            ixNetCleanUp
            return $FAILED
        }
        log "OSPF Protocol stats are matching"

    set portList [list [list $chassisIp1 $card1 $port1] [list $chassisIp2 $card2 $port2]]
        if {[checkAllProtocolStats $portList "RSVP Aggregated Statistics" $RSVPStatsList]} {
            log "FAILURE : RSVP Protocol stats are not matching"
            ixNetCleanUp
            return $FAILED
        }
        log "RSVP Protocol stats are matching"
    }

    #Getting the handle for traffic item
    set root [ixNet getRoot]
    set traffic $root/traffic

    #Applying the configured traffic item to respective ports
    log "!!!Applying the traffic !!!"
    if {[generateApplyTraffic] == 1} {
    log "FAILURE : Not able to apply the traffic.."
        ixNetCleanUp
        return $FAILED
    }

    #Checking the configured traffic item in IXNetwork Client and Chassis(IXExplore)
    if {$::TestPart2 == 1} {
    log "Verifying Traffic configuration in IXNetwork Client..."
    if {[checkDetailTrafficConfiguration] == 1} {
        log "FAILURE : Traffic Item Configuration checking in IXNetwork Client failed"
        for {set count $start_count} {$count <= $end_count} {incr count} {
        ResetDut [set DutInterface${count}Data] $count
        }
         ixNetCleanUp
         return $FAILED
    }
    log "Traffic configuration check in IXNetwork Client successful..."

    log "!!!Checking Frames Details in IXNetwork Chassis(IXExplore) !!!"
    if {[checkChassiTrafficConfiguration $chassisIp1 $card1 $port1] == 1} {
        log "FAILURE : Frame Value checking in Chassis failed"
        ixNetCleanUp
        return $FAILED
    } else {
        log "Frame Value checking in Chassis Passed"
    }
    }

    #Starting configured traffic item
    if {[startTraffic $traffic]} {
    log "FAILURE : Start Traffic Failed"
    ixNetCleanUp
    return $FAILED
    }
    log "Sleeping for 120 seconds to start the traffic"
    after 120000

    #Stoping configured traffic item
    if {[stopTraffic $traffic]} {
    log "FAILURE : Stopping Traffic Failed"
    ixNetCleanUp
    return $FAILED
    }

    # Traffic Statistics Checking
    if {$::TestPart3 == 1} {
    log "Check Traffic Item Statistics..."
    if {[checkAllTrafficStats "Traffic Item Statistics"] == 1} {
        log "FAILURE : Not able to retrieve statistics values for Traffic Item Statistics"
        ixNetCleanUp
        return $FAILED
    }

    log "Check Flow Statistics..."
    if {[checkAllTrafficStats "Flow Statistics"] == 1} {
        log "FAILURE : Not able to retrieve statistics values for Flow Statistics"
        ixNetCleanUp
        return $FAILED
    }

    log "Check Data Plane Port Statistics"
    set txPortList [subst {{[ixNet getAttr $vPort1 -name]}}]
        set rxPortList [subst {{[ixNet getAttr $vPort2 -name]}}]
    if {[checkAllPortTrafficStats "Data Plane Port Statistics" $txPortList\
         $rxPortList] } {
        log "FAILURE : Not able to retrieve statistics values for Data plane traffic"
        ixNetCleanUp
        return $FAILED
    }
    }

    #Stoping all the configured protocol
    log "!!!Stopping All Protocol Operation!!!"
    set ret [ixNet exec stopAllProtocols]
    if {$ret != "::ixNet::OK"} {
    log "FAILURE : Couldn't stop the Protocol Operation"
        ixNetCleanUp
        return $FAILED
    }

    #Unassigning all the ports and removing the same
    ixNetCleanUp

    return $PASSED
}

#------------------------------------------------------------------------------#
# Execute the Action procedure defined above                                   #
#------------------------------------------------------------------------------#
Execute_Action
