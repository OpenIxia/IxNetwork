#-------------------------------------------------------------------------------------
# Name          : test.2.1.154.rawtrafficitem.tcl
# Author        : Magesh Manavalan
# Purpose   : Checking Raw Traffic Item
# Topology  : Configure  raw traffic items with ipv4 and append of different
#           protocol ( MPLS, LDP , RSVP  ) control packets . One TI for each.
#           select Optimal Packing for some  TI and One stream per ep option
#           for remaining TI.Configure Egress Tracking.
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
#--------------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

# 2.1.154 Test Case Coverage
set ::TestPart0 0; # Protocol Stats Verification
set ::TestPart1 0; # GUI Verification NA
set ::TestPart2 1; # Traffic Configuration Verification
set ::TestPart3 1; # Traffic Stats Verification

proc checkDetailTrafficConfiguration {} {
    set error 1
    #Getting the Traffic Item object hierarchy details
    for {set count 0} {$count < 3} {incr count} {
    set traffic [ixNet getRoot]/traffic
    set trafficItem [lindex [ixNet getList $traffic trafficItem] $count]
    set configElementList [ixNet getList $trafficItem configElement]
    set configElement [lindex $configElementList 0]
    set frameRate [ixNet getList $configElement frameRate]
    set framePayload [ixNet getList $configElement framePayload]
    set frameRateDist [ixNet getList $configElement frameRateDistribution]
    set frameSize [ixNet getList $configElement frameSize]

    log "Checking Traffic Item [expr $count + 1] parameters..."
    set trafficitem_values_1 {biDirectional false mergeDestinations false\
    routeMesh oneToOne srcDestMesh oneToOne}

    if {[checkAttributeValue $trafficItem $trafficitem_values_1] == 1} {
        return $error
    }

    if {[checkAttributeValue $trafficItem/tracking \
    {trackBy "trackingenabled0 ethernetIiDestinationaddress0"}] == 1} {
        return $error
    }

    log "Checking Frame Payload parameters..."
    if {[checkAttributeValue $framePayload {type incrementByte \
                                            customPattern {} \
                                            customRepeat True}] == 1} {
        return $error
    }

    log "Checking Frame Size parameters..."
    if {[checkAttributeValue $frameSize {type fixed \
                                         fixedSize 200}] == 1} {
        return $error
    }
    }

    log "Checking High Level Stream parameters..."
    if {[checkHighLevelSteamCountForAllTrafficItem 3 {0 1 1 1 2 1}] == 1} {
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
    set frame_count 3

    for {set count 1} {$count <= $frame_count} {incr count} {
    #Getting the Frames object hierarchy details
    if {[stream get $chassisId $card $port $count] != 0} {
        log "FAILURE : Error in getting stream $count data from chassi for port $port"
        return $error
    }

    if {[ip get $chassisId $card $port] != 0} {
        log "FAILURE : Error in getting IPV4 data from chassi for port $port"
        return $error
    }

    log "Checking Stream $count Values for port $port"
    if {[ixExplorerCheckAttributeValue stream {framesize 200 patternType 0}] == 1} {
        return $error
    }
    log "Checking Stream $count IPV4 Values for port $port"
    if {[ixExplorerCheckAttributeValue ip {sourceIpAddr 1.1.1.1\
         destIpAddr 1.1.1.2}] == 1} {
        return $error
    }
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

    #Configure the Ixia ports
    log "!!!Now we configure the Ixia port!!!"
    if {[ixNet exec loadConfig [ixNet readFrom \
      $::pwd/config.2.1.154.rawtrafficitem.ixncfg]] != "::ixNet::OK"} {
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

    #Getting Neighbor MAC address. This value is set as Destination MAC address
    #in the raw traffic item
    set dis_neighbor1 [ixNet getList $vPort1 discoveredNeighbor]
    set neigh_mac1 [ixNet getAttr $dis_neighbor1 -neighborMac]
    set dis_neighbor2 [ixNet getList $vPort2 discoveredNeighbor]
    set neigh_mac2 [ixNet getAttr $dis_neighbor2 -neighborMac]

    #Getting handle for traffic item list
    set root [ixNet getRoot]
    set traffic $root/traffic
    set trafficItemList [ixNet getList $traffic trafficItem]

    #Traversing each traffic item and setting the destination mac address
    foreach trafficitem $trafficItemList {
    set highlevelstream_list [ixNet getList $trafficitem highLevelStream]
    #Setting Destination MAC, Source IP, Destination IP. Since traffic is bi-Directional,
    #values needs to be changed for each flow group.
    for {set streamcount 0} {$streamcount < 1} {incr streamcount} {
        set stack_list [ixNet getList [lindex $highlevelstream_list $streamcount] stack]
        foreach stack_element $stack_list {
        #Checking for Ethernet MAC Address field and setting the value
        if {[regexp -nocase {Ethernet} $stack_element]} {
            set fields [ixNet getList $stack_element field]
            foreach field $fields {
            if {[regexp -nocase {destinationAddress} $field]} {
                if {$streamcount == 0} {
                if {[ixNet setAttr $field -singleValue $neigh_mac1] != "::ixNet::OK"} {
                    log "FAILURE : Setting Destination MAC Address for Flow Group \
                         [expr $streamcount +1] TI [expr $streamcount +1] Failed"
                    ixNetCleanUp
                }
                }
                if {[ixNet commit] != "::ixNet::OK"} {
                log "FAILURE : Commiting Destination MAC Address for Flow Group \
                     [expr $streamcount +1] TI [expr $streamcount +1] Failed"
                ixNetCleanUp
                }
            }
            }
        } elseif {[regexp -nocase {IPv4} $stack_element]} {
            #Checking for IPV4 Address field and setting the value
            set fields [ixNet getList $stack_element field]
            foreach field $fields {
            if {[regexp -nocase {srcIp} $field]} {
                if {$streamcount == 0} {
                if {[ixNet setAttr $field -singleValue "1.1.1.1"] != "::ixNet::OK"} {
                    log "FAILURE : Setting Source IP Address for Flow Group \
                         [expr $streamcount +1] TI [expr $streamcount +1] Failed"
                    ixNetCleanUp
                }
                }
                if {[ixNet commit] != "::ixNet::OK"} {
                log "FAILURE : Commiting Source IP Address for Flow Group \
                    [expr $streamcount +1] TI [expr $streamcount +1] Failed"
                ixNetCleanUp
                }
            } elseif {[regexp -nocase {dstIp} $field]} {
                if {$streamcount == 0} {
                if {[ixNet setAttr $field -singleValue "1.1.1.2"] != "::ixNet::OK"} {
                    log "FAILURE : Setting Destination IP Address for Flow Group \
                        [expr $streamcount +1] TI [expr $streamcount +1] Failed"
                     ixNetCleanUp
                }
                }
                if {[ixNet commit] != "::ixNet::OK"} {
                log "FAILURE : Commiting Destination IP Address for Flow Group \
                    [expr $streamcount +1] TI [expr $streamcount +1] Failed"
                ixNetCleanUp
                }
            }
            }
        }
        }
    }
    }
    log "Setting MAC Address, Source IP, Destination IP Passed"

    #Applying the configured traffic item to respective ports
    #Regenerating the TI will popup merge manager window. So Regenerate TI is not used
    log "!!!Applying the traffic !!!"
    set appTraffic [::ixNet exec apply $traffic]
    if {$appTraffic != "::ixNet::OK"} {
    log "FAILURE : Not able to apply the traffic.."
        ixNetCleanUp
        return $FAILED
    }
    log "Sleeping for 10 seconds to applying the traffic"
    after 10000

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
    log "Sleeping for 60 seconds to start the traffic"
    after 60000

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
    if {[checkAllPortTrafficStats "Data Plane Port Statistics" $txPortList $rxPortList] } {
        log "FAILURE : Not able to retrieve statistics values for Data plane traffic"
        ixNetCleanUp
        return $FAILED
    }
    }

    #Unassigning all the ports and removing the same
    ixNetCleanUp

    return $PASSED
}

#------------------------------------------------------------------------------#
# Execute the Action procedure defined above                                   #
#------------------------------------------------------------------------------#
Execute_Action
