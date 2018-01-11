source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#------------------------------------------------------------------------------
# Name                      : test.9.1_OspfPortLevelRateControl.tcl
# Purpose                   : Automate OSPF PORT Rate Control Functionality
#
# Configuration Procedure   : 1. Configure OSPF with 1 router per ports
#                           : 2. & 1000 route ranges per port
#                           : 3. rate control interval :1000 Flood LS update
#                                per interval :10
# Verification steps        : 1. Run the protocol.
#                           : 2. Verify the stats
#                           : 3. Disable/Enable the Route Range
#                           : 4. Start Capture
#                           : 5. Wait for 30 second & stop the capture
#                           : 6. check through analyser tht the LS update
#                                packets are being sent
#                           :    as per the rate control applied on the router
#                                and port level
#                           : 7. Repeat step 1 to 6 for Flood LS update per
#                                interval :12
# Config Format             :    ixncfg used
#------------------------------------------------------------------------------
proc matchInCapturedPkt {currentPkt matchFieldList} {
        # initialize return value
        set noError 0
        set error 1
        puts "match field list: $matchFieldList"
        foreach {stack fieldList} $matchFieldList {
            set isStackFound 0
            set stackList [ixNet getList $currentPkt stack]
            #puts "stack list: $stackList"
            foreach pktStack $stackList {
                set displayName [ixNet getAttr $pktStack -displayName]
                #puts "displayName == $displayName stack name == $stack"
                if {$displayName != $stack} {
                    continue
                } else {
                    set isStackFound 1
                    #puts "browsing $stack to match $fieldList"
                    foreach {fieldName fieldValue} $fieldList {
                        set isFound 0
                        set fldList [ixNet getList $pktStack field]
                        #puts "field list: $fldList"
                        foreach pktStackField $fldList {
                            set fieldDispName [ixNet getAttr $pktStackField\
                                 -displayName]
                            #puts "fieldDispName = $fieldDispName\
                                fieldName (wanted) = $fieldName"
                            if {$fieldDispName != $fieldName} {
                                continue
                            } else {
                                #set isFound 1
                                if {[ixNet getAttr $pktStackField -fieldValue] !=\
                                    $fieldValue} {
                                    #puts "$fieldName : [ixNet getAttr\
                                        $pktStackField -fieldValue] (obtained)\
                                        $fieldValue (expected)"
                                    #return $error
                    continue
                                } else {
                                   # puts "$fieldName : [ixNet getAttr $pktStackField\
                                        -fieldValue] (obtained)  $fieldValue (expected)"
                    set isFound 1
                                    break
                }
                            }
                        }
                        if {$isFound == 0} {
                           # puts "No match found for $fieldName"
                            set isStackFound 0
                            break
                        }
                    }
                    if {($isFound == 1) &&($isStackFound == 1)} {
                        # puts "All fields matched"
                        break
                    }
                }
            }
            if {$isStackFound == 0} {
                # puts "No matching $stack found to match $fieldList"
                return $error
            }
        }
        puts "All Field Patterns Matched for this Pkt!!"
        return $noError
    }



proc matchInControlCapturedPkt {vPort matchFieldList} {
        # initialize return value
        set noError 0
        set error 1

        set currentPkt [lindex [ixNet getList $vPort/capture currentPacket] 0]
        set numberOfCtrlPackets [ixNet getAttr $vPort/capture\
            -controlPacketCounter]
        #puts "number of ctrl packet captured $numberOfDataPackets"
        puts "number of ctrl packet captured $numberOfCtrlPackets"
        for {set i 0} {$i < $numberOfCtrlPackets} {incr i} {
            set status [ixNet exec getPacketFromControlCapture $currentPkt $i]
            puts "browsing Pkt $i"
            puts "$currentPkt"
            if {[matchInCapturedPkt $currentPkt $matchFieldList] == 0} {
                 puts "all field patterns matched !!"
                return $noError
            }
        }
        puts "not all field patterns matched"
        return $error
    }


proc Action {portData1 portData2} {
    source $::pwd/rateControlUtils.tcl

    # initialize return value
    set FAILED 1
    set PASSED 0

    # Get real card1/port1 from portData
    set chassisIp1 [getChassisIp $portData1]
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
    if  {[ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]] \
               != "::ixNet::OK"} {
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
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    log "Assigned: $status"
    if {[string equal [lindex $status 0]  $vPort1] != 1 || \
        [string equal [lindex $status 1]  $vPort2] != 1} {
        ixNetCleanUp
        return $FAILED
    }
    ixTclNet::CheckLinkState $vPorts doneList
    after 2000

    # Enable Capture
    log "Enable & Start Capture..."
    ixNet exec startCapture
    after 5000
	
    # Repeat twice - once for floodLinkStateUpdatesPerInterval = 10 and once
    # for floodLinkStateUpdatesPerInterval = 12
    foreach floodLinkStateUpdatesPerInterval  {10  12 } {
        # Start Protocols
        log "Starting protocol ospf ..."
        if {([ixNet exec start $vPort1/protocols/ospf] != "::ixNet::OK") || \
            ([ixNet exec start $vPort2/protocols/ospf] != "::ixNet::OK")} {
            log "Failed to start protocol ospf ..."
            ixNetCleanUp
            return $FAILED
        }

        log "Protocol started. Waiting for 120 Sec for \
             protocol Sessions to be up"
        after 120000

        # Verify Starts
        log "Verifying ospf  protocol stats ..."
        set ospfStatsList { "Sess. Configured" 1 \
                            "Full Nbrs." 1}

        set portList [list [list $chassisIp1 $card1 $port1] \
                           [list $chassisIp2 $card2 $port2]]

        if {[checkAllProtocolStats $portList "OSPF Aggregated Statistics" \
                 $ospfStatsList]} {
            log "Did not get the expected ospf protocol stats value..."
            ixNetCleanUp
            return $FAILED
        }
        log "Got expected ospf protocol stats values..."

        set rateControlInterval 1000 ; # in ms
        if {$floodLinkStateUpdatesPerInterval == 12} {
            if {[setAndCheckAttributeValue $vPort1/protocols/ospf \
                     "floodLinkStateUpdatesPerInterval" {"12" y}] == 1} {
                log "Failed to set floodLinkStateUpdatesPerInterval!!!"
                ixNetCleanUp
                return $FAILED
            }
            if {[setAndCheckAttributeValue $vPort2/protocols/ospf \
                    "floodLinkStateUpdatesPerInterval" {"12" y}] == 1} {
                log "Failed to set floodLinkStateUpdatesPerInterval!!!"
                ixNetCleanUp
                return $FAILED
            }
        }

        log "Retriving ospf Rate Control Port Level Attribute \
             values as configured"
        set expectProp  [subst {rateControlInterval              \
                                $rateControlInterval             \
                                floodLinkStateUpdatesPerInterval \
                                $floodLinkStateUpdatesPerInterval}]

        if {[checkAttributeValue $vPort1/protocols/ospf $expectProp] == 1} {
            log "ospf Rate Control Port Level Attribute values not \
                 per configuration..."
            ixNetCleanUp
            return $FAILED
        }

        # Enable the packet capture
        ixNet exec startCapture

        log "Wait for 30 second"
        after 30000

        # Disable/Enable the Route Range & Network Range simultaneously.
        log "Disabling the Route Range simultaneously."
        foreach vPort $vPorts {
            set router [lindex [ixNet getList $vPort/protocols/ospf router] 0]
            foreach routeRange [ixNet getList $router routeRange] {
                if {[setAndCheckAttributeValue $routeRange "enabled" \
                         {"false" y}] == 1} {
                    log "Failed to disable Route Range!!!"
                    ixNetCleanUp
                    return $FAILED
                }
            }

            log "Waiting for 30 Sec..."
            after 30000

            log "Enabling the Route Range simultaneously."
            foreach routeRange [ixNet getList $router routeRange] {
                if {[setAndCheckAttributeValue $routeRange "enabled" \
                    {"true" y}] == 1} {
                    log "Failed to enable Route Range!!!"
                    ixNetCleanUp
                    return $FAILED
                }
            }

        }

        log "wait 60 sec"
        after 60000

        # Stop Capture
        ixNet exec stopCapture

        after 5000

        # Verify ospf LS Update in captured packet
        log "Checking for ospf LS Update in Captured Pkt..."
        
		#Match field List for Port1
		set matchFieldList1 [list "Open Shortest Path First" {"Message Type" "4"}\
                                  "Open Shortest Path First" {"Link-State Advertisement Type" "3"}\
                                  "Open Shortest Path First" {"Summary LSA (IP Network)" "True"}\
                                  "Open Shortest Path First" {"Advertising Router" "14.12.0.1"}\
					        ]

        if {[matchInControlCapturedPkt $vPort1 $matchFieldList1] == 1} {
            log "OSPF LS Update is not per configuration!!!"
			#ixNetCleanUp
            return $FAILED
        }
		
		#Match field List for Port2
		set matchFieldList2 [list "Open Shortest Path First" {"Message Type" "4"}\
                                  "Open Shortest Path First" {"Link-State Advertisement Type" "3"}\
                                  "Open Shortest Path First" {"Summary LSA (IP Network)" "True"}\
                                  "Open Shortest Path First" {"Advertising Router" "14.11.0.1"}\
					        ]

        if {[matchInControlCapturedPkt $vPort2 $matchFieldList2] == 1} {
            log "OSPF LS Update is not per configuration!!!"
			ixNetCleanUp
            return $FAILED
        }
		
        set rateList [subst {$floodLinkStateUpdatesPerInterval \
                             [expr $rateControlInterval/1000]}]

        set expectedPktCount [expr $floodLinkStateUpdatesPerInterval * 3]

        # Stop Protocols
        log "Stopping protocol ospf ..."
        if {([ixNet exec stop $vPort1/protocols/ospf] != "::ixNet::OK") || \
            ([ixNet exec stop $vPort2/protocols/ospf] != "::ixNet::OK")} {
            log "Failed to stop protocol ospf ..."
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