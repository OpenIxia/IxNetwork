#-------------------------------------------------------------------------------
# Name          : test.1.12.01_PktEditor_VlanHdr.tcl
# Purpose       : To check if the fields of the VLAN header is editable from
#                 the packet editor view (accessed from highlevel stream
#                 hyararchy)
# Description   : The following test cases loads a config file which contains
#                    a) One raw traffic item
#                    b) The raw traffic item contains one ethernet header
#                    c) The raw traffic item contains one  VLAN Header/tag
# Steps         : 1. Load the config file
#                 2. generate traffic
#                 3. Start capture and check for expected VLAN Id and VLAN
#                    priority
#                 4. Change the values of VLAN Id and VLAN priority
#                 5. Generate and start traffic again
#                 6. Check the captured packet and look for the changed VLAN ID
#                    VLAN priority
#-------------------------------------------------------------------------------

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

proc Action {portData1 portData2} {
    #---------------------------------------------------------------------------
    # initialize return values
    #---------------------------------------------------------------------------
    set PASSED 0
    set FAILED 1

    #---------------------------------------------------------------------------
    # get port info 1
    #---------------------------------------------------------------------------
    set chassisIp1 [getChassisIp  $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    #---------------------------------------------------------------------------
    # get port info 2
    #---------------------------------------------------------------------------
    set chassisIp2 [getChassisIp  $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    #---------------------------------------------------------------------------
    # Connecting to client
    #---------------------------------------------------------------------------
    set connection_Result [connectToClient $portData1 $portData2 5.40]
    log "Connection Result: $connection_Result"
    if {[string equal $connection_Result "::ixNet::OK"] != 1} {
        log "connection to client unsuccessfill"
        return $FAILED
    }
    log "connectToClient Successful"

    #---------------------------------------------------------------------------
    # clean up all the existing configurations from client
    #---------------------------------------------------------------------------
    log "cleaning up the client"
    ixNetCleanUp

    #---------------------------------------------------------------------------
    # load the ixncfg config file
    #---------------------------------------------------------------------------
    set configFileName config.[getTestId].ixncfg
    if {[catch {ixNet exec loadConfig [ixNet readFrom \
        "$::pwd/$configFileName"]} errorMsg]} {
       log "Error in loading Config file: $errorMsg"
       ixNetCleanUp
       return $FAILED
    }

    #---------------------------------------------------------------------------
    # get the virtual port list and real port list
    #---------------------------------------------------------------------------
    log "getting virtual ports ...."
    set vPorts [ixNet getList [ixNet getRoot] vport]

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
        [list $chassisIp2 $card2 $port2] ]

    #---------------------------------------------------------------------------
    # Assign virtual ports to real ports
    #---------------------------------------------------------------------------
    log "Assign virtual ports to real ports ..."
    set force true
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    log "Assigned: $status"
    ixTclNet::CheckLinkState $vPorts doneList

    #---------------------------------------------------------------------------
    # Check if the ports are assigned if un assigned re-assign them
    #---------------------------------------------------------------------------
    after 5000
    ifUnassignedConnectAgain


    #---------------------------------------------------------------------------
    # Forcefully make the port mode "capture"
    #---------------------------------------------------------------------------
    if {[enableCaptureMode $vPorts]} {
        log "unable to make port mode capture"
        ixNetCleanUp
        return $FAILED
    }

    #---------------------------------------------------------------------------
    # generte the traffic
    #---------------------------------------------------------------------------
    generateApplyTraffic


    #---------------------------------------------------------------------------
    # Start packet capture
    #---------------------------------------------------------------------------
    if {[catch {ixNet exec startCapture} errorMsg]} {
        log "error in starting capture $errorMsg"
        ixNetCleanUp
        return $FAILED
    }
    after 1000

    #---------------------------------------------------------------------------
    # start the traffic
    #---------------------------------------------------------------------------
    set traffic [ixNet getRoot]/traffic
    if {[catch {startTraffic $traffic} errorMsg]} {
        log "error in stopping capture $errorMsg"
        ixNetCleanUp
        return $FAILED
    }

    #---------------------------------------------------------------------------
    # wait for desired amount of time
    #---------------------------------------------------------------------------
    set waitTime 10000
    log "wait for $waitTime ms"
    after $waitTime


    #---------------------------------------------------------------------------
    # Stop the traffic
    #---------------------------------------------------------------------------
    if {[catch {stopTraffic $traffic} errorMsg]} {
        log "error in stopping capture $errorMsg"
        ixNetCleanUp
        return $FAILED
    }

    #---------------------------------------------------------------------------
    # stop packet capture
    #---------------------------------------------------------------------------
    if {[catch {ixNet exec stopCapture} errorMsg]} {
        log "error in stopping capture $errorMsg"
        ixNetCleanUp
        return $FAILED
    }

    #---------------------------------------------------------------------------
    # verify capture
    #---------------------------------------------------------------------------
    set isFound 1
    set expectedPattern "00 0C"
    set startOffset     14
    set endOffset       15
    set expectedString [subst {$startOffset $endOffset "$expectedPattern"}]

    if {[verifyCapturedPackets $chassisIp2 $card2 $port2 \
         $expectedString]} {
         log "The string $expectedString not found in the offset $startOffset"
         set isFound 0
         ixNetCleanUp
         return $FAILED
    }

    #----------------------------------------------------------------------------
    # Change Vlan Id
    # Additional steps
    #   a) checks there is only one traffic item
    #   b) checks there is only one high level stream
    #   c) checks the initial
    #----------------------------------------------------------------------------
    set trafficItemList [ixNet getList $traffic trafficItem]
    if {[llength $trafficItemList] != 1} {
        log "There should be only one traffic item"
        ixNetCleanUp
        return $FAILED
    }
    set myTrafficItem  [lindex $trafficItemList 0]
    set hlsList        [ixNet getList $myTrafficItem highLevelStream]

    if {[llength $hlsList] != 1} {
        log "There should be only one High Level Stream item"
        ixNetCleanUp
        return $FAILED
    }
    set myHLS [lindex $hlsList 0]

    set configElement [lindex [ixNet getList [lindex [ixNet \
    getList [ixNet getRoot]/traffic trafficItem] 0] configElement] 0]

    set stackList [ixNet getList $configElement stack]
    set stack1 [lindex [ixNet getList $configElement stack] 0]
    set stack1 [lindex [ixNet getList $configElement stack] 1]
    set fields [ixNet getList $stack1 field]
    set fieldOneByOne [lindex $fields 2]

    set initialIdVal [ixNet getAttr $fieldOneByOne  -singleValue]
    if {$initialIdVal != 12} {
        log "Initial Id value was 12 MISMATCH !!"
        ixNetCleanUp
        return $FAILED
    }

    ixNet setAttr $fieldOneByOne  -valueType singleValue
    ixNet commit

    ixNet setAttr $fieldOneByOne  -singleValue 13
    ixNet commit

    set newIdVal [ixNet getAttr $fieldOneByOne  -singleValue]
    if {$newIdVal != 13} {
        log "VLAN Id value should be 13 MISMATCH !!"
        ixNetCleanUp
        return $FAILED
    }

    #---------------------------------------------------------------------------
    # generate the traffic
    #---------------------------------------------------------------------------
    log "Appling the traffic...."
    set appTraffic [::ixNet exec apply $traffic]
    if {$appTraffic != "::ixNet::OK"} {
        log "Not able to apply the traffic.."
        return $flag
    }
    after 10000
    #---------------------------------------------------------------------------
    # Start packet capture
    #---------------------------------------------------------------------------
    if {[catch {ixNet exec startCapture} errorMsg]} {
        log "error in starting capture $errorMsg"
        ixNetCleanUp
        return $FAILED
    }
    after 1000

    #---------------------------------------------------------------------------
    # start the traffic
    #---------------------------------------------------------------------------
    if {[catch {startTraffic $traffic} errorMsg]} {
        log "error in stopping capture $errorMsg"
        ixNetCleanUp
        return $FAILED
    }

    #---------------------------------------------------------------------------
    # wait for desired amount of time
    #---------------------------------------------------------------------------
    set waitTime 20000
    log "wait for $waitTime ms"
    after $waitTime

    #---------------------------------------------------------------------------
    # Stop the traffic
    #---------------------------------------------------------------------------
    if {[catch {stopTraffic $traffic} errorMsg]} {
        log "error in stopping capture $errorMsg"
        ixNetCleanUp
        return $FAILED
    }

    #---------------------------------------------------------------------------
    # stop packet capture
    #---------------------------------------------------------------------------
    if {[catch {ixNet exec stopCapture} errorMsg]} {
        log "error in stopping capture $errorMsg"
        ixNetCleanUp
        return $FAILED
    }

    #---------------------------------------------------------------------------
    # verify capture
    #---------------------------------------------------------------------------
    set isFound 1
    set expectedPattern "00 0D"
    set startOffset     14
    set endOffset       15
    set expectedString [subst {$startOffset $endOffset "$expectedPattern"}]

    if {[verifyCapturedPackets $chassisIp2 $card2 $port2 \
         $expectedString]} {
         log "The string $expectedString not found in the offset $startOffset"
         set isFound 0
         ixNetCleanUp
         return $FAILED
    }

    #---------------------------------------------------------------------------
    # Change Vlan Priority
    #---------------------------------------------------------------------------
    set configElement [lindex [ixNet getList [lindex [ixNet \
    getList [ixNet getRoot]/traffic trafficItem] 0] configElement] 0]

    set stackList [ixNet getList $configElement stack]
    set stack1 [lindex [ixNet getList $configElement stack] 0]
    set stack1 [lindex [ixNet getList $configElement stack] 1]
    set fields [ixNet getList $stack1 field]
    set fieldOneByOne [lindex $fields 0]

    set initialIdVal [ixNet getAttr $fieldOneByOne -singleValue]
    if {$initialIdVal != 0} {
        log "Initial Id value was 0 MISMATCH !!"
        ixNetCleanUp
        return $FAILED
    }

    ixNet setAttr $fieldOneByOne -valueType singleValue
    ixNet commit

    ixNet setAttr $fieldOneByOne -singleValue 1
    ixNet commit

    set newPriority [ixNet getAttr $fieldOneByOne -singleValue]
    if {$newPriority != 1} {
       log "Priority value should be 1 MISMATCH !!"
       ixNetCleanUp
       return $FAILED
    }

    #---------------------------------------------------------------------------
    # generte the traffic
    #---------------------------------------------------------------------------
    log "Appling the traffic...."
    set appTraffic [::ixNet exec apply $traffic]
    if {$appTraffic != "::ixNet::OK"} {
        log "Not able to apply the traffic.."
        return $flag
    }
    after 10000

    #---------------------------------------------------------------------------
    # Start packet capture
    #---------------------------------------------------------------------------
    if {[catch {ixNet exec startCapture} errorMsg]} {
        log "error in starting capture $errorMsg"
        ixNetCleanUp
        return $FAILED
    }
    after 1000

    #---------------------------------------------------------------------------
    # start the traffic
    #---------------------------------------------------------------------------
    startTraffic $traffic

    #---------------------------------------------------------------------------
    # wait for desired amount of time
    #---------------------------------------------------------------------------
    set waitTime 10000
    log "wait for $waitTime ms"
    after $waitTime

    #---------------------------------------------------------------------------
    # Stop the traffic
    #---------------------------------------------------------------------------
    stopTraffic $traffic

    #---------------------------------------------------------------------------
    # stop packet capture
    #---------------------------------------------------------------------------
    if {[catch {ixNet exec stopCapture} errorMsg]} {
        log "error in stopping capture $errorMsg"
        ixNetCleanUp
        return $FAILED
    }

    #---------------------------------------------------------------------------
    # verify capture
    #---------------------------------------------------------------------------
    set isFound 1
    set expectedPattern "20 0D"
    set startOffset     14
    set endOffset       15
    set expectedString [subst {$startOffset $endOffset "$expectedPattern"}]

    if {[verifyCapturedPackets $chassisIp2 $card2 $port2 \
         $expectedString]} {
         log "The string $expectedString not found in the offset $startOffset"
         set isFound 0
         ixNetCleanUp
         return $FAILED
    }

    ixNetCleanUp
    return $PASSED
}

#------------------------------------------------------------------------------#
# Execute the Action procedure defined above                                   #
#------------------------------------------------------------------------------#
Execute_Action
