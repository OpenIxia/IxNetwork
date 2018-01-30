source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#-----------------------------------------------------------------------------#
# Name           : test.2.3_AT_IsisLevel1n2MultiTopologyTlv.tcl               #
# Purpose        : Multi-Topology TLV verification for Level-2 IS-IS          #
# Topology       : 1. Configure IS-IS (Level-1-Level-2) with Network Type as  #
#                     Point-to-Point.                                         #
#                  2. Set the ""Number of Network Ranges"" field in           #
#                     ""Router/RBridge"" tab to be 1.                         #
#                  3. Enable the checkbox ""Enable MT for IPv6"".             #
#                  4. Configure some value (other than default) in the        #
#                     "IPv6 MT Metric" field                                  #
#                     under both ""Interface"" tab & ""Network Ranges"" tab.  #
#                  5. Configure 4 IPv6 Route Ranges and 4 IPv6 Network Ranges.#
#                  6. Start the packet capture and Run the protocol.          #
# Verification   : 1. Verify stats data for L1 Session configured/Session Up, #
#                     Full State Count, Neighbors.                            #
#                  2. Verify the Learned Info and match the correct IPv6      #
#                     prefixes.                                               #
#                  3. Verify packet capture to check the existence of         #
#                     all three TLV types (TLV Nos. 229, 222, 237) in Hello & #
#                     LSPs.                                                   #
# Config Format  : ixncfg used                                                #
#-----------------------------------------------------------------------------#

proc configureIxNetworkGui {} {
    set isError  [catch {ixNet exec loadConfig [ixNet readFrom \
            $::pwd/config.2.3_AT_IsisLevel1n2MultiTopologyTlv.ixncfg]} errmsg]
    if {$isError} {
        puts "$errmsg"
    }
}

proc Action {portData1 portData2} {
    source $::pwd/isisUtilsQa.tcl

    set FAILED 1
    set PASSED 0

    # get port info 1
    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    # get port info 2
    set chassisIp2 [getChassisIp  $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    # Hostname, where IxNetwork TCL-Server client runs
    set hostName [lindex [getHostName $portData1] 0]

    # Version Number (IxNetwork Major version No i.e. 5.50)
    set version "5.50"

    # connect to client
    if {[ixNet connect $hostName -version 5.50] != "::ixNet::OK"} {
        puts "Test case failed unable to connect to IxNetwork"
        return $FAILED
    }

    # clean up config
    ixNet exec newConfig

    # Configure IxNetwork GUI
    configureIxNetworkGui

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]

    # get root object
    set root [ixNet getRoot]

    #Remove pre-existing chassis
    set availableHardware [ixNet getList $root availableHardware]
    set chassis [ixNet getList $availableHardware chassis]
    foreach c $chassis {
        ixNet remove $c
        ixNet commit
    }
    
    # Assign real ports to virtual ports
    puts "getting virtual ports ...."
    set vPorts [ixNet getList $root vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]

    # enable NS on Link Up option
    set globals $root/globals
    set interfaces $globals/interfaces
    ixNet setAttr $interfaces -nsOnLinkup true
    ixNet commit

    # Assign virtual ports to real ports
    puts "Assign virtual ports to real ports ..."
    if {[catch {ixTclNet::AssignPorts $realPortsList {} $vPorts}]} {
        puts "Error in assigning ports"
        ixNet exec newConfig
    }

    # Check if the ports are assigned; if un-assigned re-assign them
    if {[ifUnassignedConnectAgain] == 1} {
        puts "Not able to re-assign the ports !!!"
        ixNetCleanUp
        return $FAILED
    }
    puts "Ports are in assigned state !!!"
    after 5000

    # Check Ports Link Status
    puts "Checking Port Link Status ..."
    if {[ixTclNet::CheckLinkState $vPorts doneList]} {
        puts "Ports Link is down !!!"
        ixNetCleanUp
        return $FAILED
    }
    puts "Ports Link is Up !!!"


    # Enable & Start Capture
    log "Enable & Start Capture..."
    if {[enableCaptureMode [list $vPort2]] == 1} {
        log "Failed to enable capture on Port 2..."
        ixNetCleanUp
        return $FAILED
    }

    # start capture
    ixNet exec startCapture

    # Start Protocols
    log "Starting protocol ISIS (Level 1 Level 2)..."
    if {[ixNet exec startAllProtocols] != "::ixNet::OK"} {
        log "Failed to start protocol ISIS (Level 1 Level 2)..."
        ixNetCleanUp
        return $FAILED
    }

    log "Protocol started. Waiting for 40 Sec for protocol Sessions to be up.."
    after 40000

    # Stop Capture
    ixNet exec stopCapture

    # Verify Starts
    log "Verifying ISIS (Level 1 Level 2) protocol stats ..."
    set ISISStatsList { "L1 Sess. Configured" 1 \
                        "L1 Sess. Up"         1 \
                        "L1 Full State Count" 1 \
                        "L1 Neighbors"        1 \
                        "L2 Sess. Configured" 1 \
                        "L2 Sess. Up"         1 \
                        "L2 Full State Count" 1 \
                        "L2 Neighbors"        1}

    set portList [list [list $chassisIp1 $card1 $port1] \
                       [list $chassisIp2 $card2 $port2]]

    if {[checkAllProtocolStats $portList "ISIS Aggregated Statistics" \
         $ISISStatsList 1]} {
        log "Did not get the expected ISIS (Level 1 Level 2)protocol stats value..."
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected ISIS (Level 1 Level 2) protocol stats values..."

    # Verify learnt info
    log "Verify ISIS (Level 1 Level 2) Learnt Info..."
    set router1_vPort1 [lindex [ixNet getList $vPort1/protocols/isis router] 0]
    set checkLearntInfoList_vPort1 [list ipv6Prefixes \
        {hostName ipv6Prefix learnedVia lspId metric}                          \
        {{P2_Router1 22:0:0:0:0:0:0:0/64 L1 "05 26 00 01 00 00 00 00 " 0}      \
        {P2_Router1 22:0:0:1:0:0:0:0/64 L1 "05 26 00 01 00 00 00 00 " 0}       \
        {P2_Router1 22:22:0:0:0:0:0:0/64 L1 "05 26 00 01 00 00 00 00 " 222}    \
        {Prt2_Net2.1.1 22:22:0:1:0:0:0:0/64 L1 "22 00 C0 14 14 00 00 00 " 222} \
        {Prt2_Net2.1.1 22:22:0:3:0:0:0:0/64 L1 "22 00 C0 14 14 00 00 00 " 222} \
        {Prt2_Net2.1.1 22:22:0:0:0:0:0:0/64 L1 "22 00 C0 14 14 00 00 00 " 222} \
        {Prt2_Net2.1.2 22:22:0:1:0:0:0:0/64 L1 "22 00 C0 14 14 01 00 00 " 222} \
        {Prt2_Net2.1.2 22:22:0:4:0:0:0:0/64 L1 "22 00 C0 14 14 01 00 00 " 222} \
        {Prt2_Net2.2.1 22:22:0:2:0:0:0:0/64 L1 "22 00 C0 14 14 02 00 00 " 222} \
        {Prt2_Net2.2.1 22:22:0:3:0:0:0:0/64 L1 "22 00 C0 14 14 02 00 00 " 222} \
        {Prt2_Net2.2.2 22:22:0:2:0:0:0:0/64 L1 "22 00 C0 14 14 03 00 00 " 222} \
        {Prt2_Net2.2.2 22:22:0:4:0:0:0:0/64 L1 "22 00 C0 14 14 03 00 00 " 222} \
        {P2_Router1 22:0:0:0:0:0:0:0/64 L2 "05 26 00 01 00 00 00 00 " 0}       \
        {P2_Router1 22:0:0:1:0:0:0:0/64 L2 "05 26 00 01 00 00 00 00 " 0}       \
        {P2_Router1 22:22:0:0:0:0:0:0/64 L2 "05 26 00 01 00 00 00 00 " 222}    \
        {Prt2_Net2.1.1 22:22:0:1:0:0:0:0/64 L2 "22 00 C0 14 14 00 00 00 " 222} \
        {Prt2_Net2.1.1 22:22:0:3:0:0:0:0/64 L2 "22 00 C0 14 14 00 00 00 " 222} \
        {Prt2_Net2.1.1 22:22:0:0:0:0:0:0/64 L2 "22 00 C0 14 14 00 00 00 " 222} \
        {Prt2_Net2.1.2 22:22:0:1:0:0:0:0/64 L2 "22 00 C0 14 14 01 00 00 " 222} \
        {Prt2_Net2.1.2 22:22:0:4:0:0:0:0/64 L2 "22 00 C0 14 14 01 00 00 " 222} \
        {Prt2_Net2.2.1 22:22:0:2:0:0:0:0/64 L2 "22 00 C0 14 14 02 00 00 " 222} \
        {Prt2_Net2.2.1 22:22:0:3:0:0:0:0/64 L2 "22 00 C0 14 14 02 00 00 " 222} \
        {Prt2_Net2.2.2 22:22:0:2:0:0:0:0/64 L2 "22 00 C0 14 14 03 00 00 " 222} \
        {Prt2_Net2.2.2 22:22:0:4:0:0:0:0/64 L2 "22 00 C0 14 14 03 00 00 " 222}}]

    if {[checkISISLearnedInfo $router1_vPort1 \
             $checkLearntInfoList_vPort1 {filterLearnedIpv6Prefixes true}]} {
        log "Did not get ALL expected ISIS (Level 1 Level 2) Learnt Info..."
        ixNetCleanUp
        return $FAILED
    }
    log "Got ALL expected ISIS (Level 1 Level 2) Learnt Info..."

    # Verify Multi Topology TLV in captured packet
    log "Checking for ISIS (Level 1 Level 2) Multi Topology TLV \
         229(0x E5) in HELLO Pkt..."
    set helloMatchFieldList {21 21 "11" \
                             25 25 "03" \
                             54 54 "E5"}

    if {[verifyCapturedPackets $chassisIp2 $card2 $port2 \
        $helloMatchFieldList] == 1} {
        log "Expected field value match not found in capture buffer"
        ixNetCleanUp
        return $FAILED
    }

    log "Checking for ISIS (Level 1) Multi Topology TLV 229(0x E5), \
         222(0x DE), 237(0x ED) in LSP Pkt..."
    set lspMatchFieldList {21 21    "12" \
                            55 55   "E5" \
                            115 115 "DE" \
                            168 168 "ED"}

    if {[verifyCapturedPackets $chassisIp2 $card2 $port2 \
        $lspMatchFieldList] == 1} {
        log "Expected field value match not found in capture buffer"
        ixNetCleanUp
        return $FAILED
    }

    log "Checking for ISIS (Level 2) Multi Topology TLV 229(0x E5), \
         222(0x DE), 237(0x ED) in LSP Pkt..."

    set lspMatchFieldList {21 21   "14" \
                           55 55   "E5" \
                           115 115 "DE" \
                           168 168 "ED"}

    if {[verifyCapturedPackets $chassisIp2 $card2 $port2 \
         $lspMatchFieldList] == 1} {
        log "Expected field value match not found in capture buffer"
        ixNetCleanUp
        return $FAILED
    }


    # Stop Protocols
    log "Stopping protocol ISIS (Level 1 Level 2)..."
    if {([ixNet exec stopAllProtocols] != "::ixNet::OK")} {
        log "Failed to stop protocol ISIS (Level 1 Level 2)..."
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



