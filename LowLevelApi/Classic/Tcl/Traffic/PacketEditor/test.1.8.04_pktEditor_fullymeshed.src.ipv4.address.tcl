#------------------------------------------------------------------------------
# Name              :   test.1.8.04_pktEd_fullymeshed.src.ipv4.address
# Purpose           :   packet editor :fully mesh : src ipv4
# Steps to recreate :   add a raw  traffic item with ethernet vlan trafic
#                   :   type , do a fully mesh  on src ipv4, check the
#                   :   packet count , check the packet count in preview
#                   :   page and flow group editor, apply the traffi and
#                   :   check the pakets in explorer , run the trafic and
#                   :   check the stats through statsviewer, now change
#                   :   the count of the fullymeshed field, and check the
#                   :   new no of packets , apply and run the traffic again
#
# Verify            :   check the no of packets formed as a result of the
#                   :   fully mesh . Verify through packet ditor , preview
#                   :   page and flow group editor , apply trafic and check
#                   :   the packets in the explorer page , run traffic and
#                   :   check the stats through statsviewer and analyser
# Topology          :   Back to Back
# ixncfg file       :   config.1.8.04_pktEd_fullymeshed.src.ipv4.address
# Scriptgen         :   not used
#-------------------------------------------------------------------------------

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

#-------------------------------------------------------------------------------
# 1) Following things are not doable from tcl
#     Check the packet count in preview page and flow group editor
# 2) We are ignoring the following setp
#    and check the pakets in explorer
#    check the packets in the explorer page
#-------------------------------------------------------------------------------
proc Action {portData1 portData2} {
    # initialize return value
    set PASSED 0
    set FAILED 1

    # Get real card1/port1 from portData
    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    # Get real card2/port2 from portData
    set chassisIp2 [getChassisIp $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    # create real port list (card1/port1 and card2/port2)
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]

    # Connect to client
    log "Connectng to client ..."
    set connection_Result [connectToClient $portData1 $portData2 5.40]
    log "connection_Result is = $connection_Result"

    if {[string equal $connection_Result "::ixNet::OK"] != 1} {
        log "connection to client unsuccessfill"
        return $FAILED
    }
    log "connectToClient Successful"

    log "Cleaning up the client .."
    ixNetCleanUp

    # load config files
    log "loading ixncfg file ..."
    set configFileName config.[getTestId].ixncfg
    if  {[ixNet exec loadConfig [ixNet readFrom "$::pwd/$configFileName"]] \
        != "::ixNet::OK"} {
        log "Loading IxNetwork config file FAILED "
        ixNetCleanUp
        return $FAILED
    }
    log "Loading IxNetwork config file : passed"

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
        return $flag
    }
    ixTclNet::CheckLinkState $vPorts doneList

    # if assign fails try to assign the ports again
    ifUnassignedConnectAgain

    # Generate and Apply Traffic
    log "Generating and Applying Traffic....."
    if {[generateApplyTraffic] == 1} {
        log "Failed to start traffic"
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic generated and applied successfully !!!"


    # Start Traffic
    set traffic [ixNet getRoot]/traffic
    if {[startTraffic $traffic] == 1} {
        log "Failed to start the traffic"
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic started successfully"

    log "Waiting for 20 seconds..."
    after 20000

    # Stop Traffic
    log "Stopping Traffic ....."
    if {[stopTraffic $traffic] == 1} {
        log "Failed to stop traffic"
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic stopped successfully !!!"
    after 10000


    log "Check Traffic Item Statistics..."
    if {[checkAllTrafficStats "Traffic Item Statistics" 5] == 1} {
        log "Not able to retrieve statistics values for Traffic Item Statistics"
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic Item Statistics is correct !!!"

    log "Check Flow Statistics..."
    if {[checkAllTrafficStats "Flow Statistics" 5] == 1} {
        log "Not able to retrieve statistics values for Flow Statistics"
        ixNetCleanUp
        return $FAILED
    }
    log "Flow Statistics is correct !!!"

    log "Check Data Plane Port Statistics"
    set txPortList [subst {{[ixNet getAttr $vPort1 -name]}}]
    set rxPortList [subst {{[ixNet getAttr $vPort2 -name]}}]
    if {[checkAllPortTrafficStats "Data Plane Port Statistics" \
        $txPortList $rxPortList 5] == 1} {
        log "Not able to retrieve statistics values for Data plane traffic"
        ixNetCleanUp
        return $FAILED
    }
    log "Data Plane Port Statistics is correct !!!"
    log "Traffic Stats Checking done successfully"

    # Capture Verification
    # Disable tracking option
    log "Disabling Tracking Options"
    set traffic [ixNet getRoot]/traffic
    set trafficItem [lindex [ixNet getList $traffic trafficItem] 0]
    if {[setAndCheckAttributeValue $trafficItem/tracking trackBy {{} y}] == 1} {
        log "Traffic Config is not correct"
        ixNetCleanUp
        return $FAILED
    }
    log "Tracking Options disabled successfully"


    if {[enableCaptureMode $vPorts]} {
        log "unable to make port mode capture"
        ixNetCleanUp
        return $FAILED
    }

    # Traffic Apply and Start
    set traffic [ixNet getRoot]/traffic
    if [generateApplyTraffic] {
        log "Failed to start traffic"
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic applyed successfully"

    # Start the capture
    log "Start Capturing packets"
    if {[catch {ixNet exec startCapture} err] == 1} {
        log  "Failed to start packet capture $err"
        ixNetCleanUp
        return $FAILED
    }
    log "capture started successfully"

    log "Starting the stateless Traffic"
    if {[catch {ixNet exec startStatelessTraffic $traffic} errMsg]} {
        puts "Start Traffic Failed - $errMsg"
        ixNetCleanUp
        return $FAILED
    }
    log "Stateless Traffic got started successfully"

    log "Wait for 5 seconds"
    after 5000

    log "stopping the sateless traffic"
    if {[catch {ixNet exec stopStatelessTraffic $traffic} errMsg]} {
        puts "stopping Traffic Failed - $errMsg"
        ixNetCleanUp
        return $FAILED
    }
    log "Stateless traffic stopped successfully"

    log "Stopping the capture"
    if {[catch {ixNet exec stopCapture} err] == 1} {
        log "Failed to stop packet capture "
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic stopped successfully"
    after 5000

    for {set i 1} {$i <= 5} {incr i} {
        for {set j 6} {$j <= 10} {incr j} {
            set srcIp "01 01 01 [format %0.2x $i]"
            set dstIp "01 01 01 [format %0.2x $j]"
            set srcIp1 [string toupper $srcIp]
            set dstIp1 [string toupper $dstIp]

            log "$srcIp1  $dstIp1"
            set packetsToVerify1 [subst {26 29 "$srcIp1" \
                                         30 33 "$dstIp1"}]

            log $packetsToVerify1

            log "chassisIp2 = $chassisIp2, card2 = $card2 port2 = $port2"
            if {[verifyCapturedPackets $chassisIp2 $card2 $port2 \
                $packetsToVerify1] == 1} {
                log "Packets not found --failed!!"
                return 1
            }
        }
    }
    log "Found expected packets in capture"

    ixNetCleanUp
    return $PASSED
}

#------------------------------------------------------------------------------#
# Execute the Action procedure defined above                                   #
#------------------------------------------------------------------------------#
Execute_Action

